import json
import requests
import uuid
from swan.api.mcs_api import MCSAPI, File
from swan.common.utils import datetime_to_unixtime
from swan.object.cp_config import HardwareConfig


class SourceFilesInfo():
    
    def __init__(self):
        self.file_list = []
        self.mcs_client = None
        
    def mcs_connection(self, mcs_client: MCSAPI):
        """Add mcs connection.

        Args:
            mcs_client: mcs API object.
        """
        self.mcs_client = mcs_client

    def add_folder(self, bucket_name: str, object_name: str):
        """Add a folder/repo to the source file info.

        Args:
            bucket_name: bucket name of bucket locating the folder.
            object_name: folder object_name (directory)
        """
        folder_file = self.mcs_client._get_full_file_list(bucket_name, object_name)
        self.file_list += self.get_folder_files(bucket_name, folder_file)
        

    def add_file(self, bucket_name: str, object_name: str):
        """Add single file to source file info.

        Args:
            bucket_name: bucket name of bucket locating the folder.
            object_name: file object_name (directory + file name)
        """
        file = self.mcs_client.get_file(bucket_name, object_name)
        list.append(file)

    def _file_to_dict(self, file: File):
        return {
            "cid": file.payloadCid,
            "created_at": datetime_to_unixtime(file.created_at),
            "name": f'0x000000/spaces/{str(file.name)}',
            "updated_at": datetime_to_unixtime(file.updated_at),
            "url": file.ipfs_url
        }
    
    def get_folder_files(self, bucket_name: str, file_list: list):
        """Retrieve all files under folders.

        Args: 
            bucket_name: bucket name of bucket locating the folder.
            file_llist: list of directories (cotain folders).
        
        Returns:
            Updated file_list without folder and all files under given directories.
        """
        folder_list = []
        exist_folder = False
        for file in file_list:
            if file.is_folder:
                exist_folder = True
                folder_list.append(file)
                file_list.remove(file)
        for folder in folder_list:
            new_file_list = self.mcs_client.list_files(bucket_name, folder.object_name)
            file_list += new_file_list
        if exist_folder:
            file_list = self.get_folder_files(bucket_name, file_list)
        return file_list

    def to_dict(self):
        return {
            "data": {
                "files": [
                    self._file_to_dict(file) for file in self.file_list
                ]
            }
        }
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    

class Repository():

    def __init__(self):
        """Initialize repository for swan task.
        """
        self.folder_dir = None
        self.bucket = None
        self.path = None
        self.source_uri = None

    def update_bucket_info(self, bucket_name: str, object_name: str):
        """Update the current mcs bucket info on MCS.

        Args:
            bucket_name: name of bucket.
            object_name: directory + file_name.
        """
        self.bucket = bucket_name
        self.path = object_name

    def add_local_dir(self, folder_dir: str):
        """Initialize repository for swan task.

        Args:
            folder_dir: Directory of folder to upload to mcs.
        """
        self.folder_dir = folder_dir

    def mcs_connection(self, mcs_client: MCSAPI):
        """Add mcs connection.

        Args:
            mcs_client: mcs API object.
        """
        self.mcs_client = mcs_client

    def upload_local_to_mcs(self, bucket_name: str, obj_name: str, mcs_client: MCSAPI = None):
        """Upload repository to MCS to create remote source.

        Args:
            bucket_name: bucket to upload repository.
            obj_name: dir + file_name for repository.
            mcs_client: mcs API object.

        Returns:
            API response from uploading folder to MCS. Contain info of list of files uploaded.
        """
        if self.folder_dir:
            if mcs_client:
                self.mcs_connection(mcs_client)
            self.bucket = bucket_name
            self.path = obj_name
            upload = mcs_client.upload_folder(bucket_name, obj_name, self.folder_dir)
            return upload
        return None

    def generate_source_uri(self, bucket_name: str, obj_name: str, file_path: str, mcs_client: MCSAPI = None, replace: bool = True):
        """Generate source uri for task using MCS service.

        Args:
            bucket_name: bucket name to store source uri.
            obj_name: object name (dir + file name) to store source uri.
            file_path: local file path to store source uri JSON file.
            replace: replace existing file or not.
            mcs_client: mcs API object.

        Returns：
            API response from MCS after uploading. Contains file information.

        """
        if self.bucket and self.path:
            if mcs_client:
                self.mcs_connection(mcs_client)
                local_source = SourceFilesInfo()
                local_source.mcs_connection(mcs_client)
                local_source.add_folder(self.bucket, self.path)
                with open(file_path, "w") as file:
                    json.dump(local_source.to_dict(), file)
                res = mcs_client.upload_file(bucket_name, obj_name, file_path, replace)
                self.source_uri = res.ipfs_url
                return res
            
    def to_dict(self):
        return {
            "folder_dir": self.folder_dir,
            "bucket_name": self.bucket,
            "folder_path": self.path,
            "source_uri": self.source_uri
        }

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    

class LagrangeSpace():

    def __init__(self, space_owner: str, space_name: str, wallet_address: str, hardware_config: HardwareConfig):

        self.wallet_address = wallet_address
        self.space_name = space_name
        self.space_owner = space_owner
        self.hardware_config = hardware_config
        self.space_uuid = None
        self.source_uri = None
        self.file_list = []

    def get_space_info(self):
        space_file_uri = f'https://api.lagrangedao.org/spaces/{self.space_owner}/{self.space_name}/files'
        space_detail_uri = f'https://api.lagrangedao.org/spaces/{self.space_owner}/{self.space_name}'
        space_files = requests.get(space_file_uri).json()
        space_detail = requests.get(space_detail_uri).json()

        for file in space_files["data"]:
            self.file_list.append(file)
        
        self.space_uuid = space_detail["data"]["space"]["uuid"]
        

    def mcs_connection(self, mcs_client: MCSAPI):
        """Add mcs connection.

        Args:
            mcs_client: mcs API object.
        """
        self.mcs_client = mcs_client

    def to_dict(self):
        hardware_info = self.hardware_config.description
        hardware_info = hardware_info.split(" · ")

        return {
            "data": {
                "files": self.file_list,
                "owner": {
                    "public_address": self.wallet_address,
                },
                "space": {
                    "activeOrder": {
                        "config": {
                            "description": self.hardware_config.description,
                            "hardware": hardware_info[0],
                            "hardware_id": int(self.hardware_config.id),
                            "hardware_type": self.hardware_config.type,
                            "memory": [int(s) for s in hardware_info[2].split() if s.isdigit()][0],
                            "name": self.hardware_config.name,
                            "price_per_hour": float(self.hardware_config.price),
                            "vcpu": [int(s) for s in hardware_info[1].split() if s.isdigit()][0],
                        },
                    },
                    "name": self.space_name,
                    "uuid": self.space_uuid,
                }
            }
        }
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    
    def generate_source_uri(self, bucket_name: str, obj_name: str, file_path: str, mcs_client: MCSAPI = None, replace: bool = True):
        """Generate source uri for task using MCS service.

        Args:
            bucket_name: bucket name to store source uri.
            obj_name: object name (dir + file name) to store source uri.
            file_path: local file path to store source uri JSON file.
            replace: replace existing file or not.
            mcs_client: mcs API object.

        Returns：
            API response from MCS after uploading. Contains file information.

        """
        if mcs_client:
            self.mcs_connection(mcs_client)
            with open(file_path, "w") as file:
                json.dump(self.to_dict(), file)
            res = mcs_client.upload_file(bucket_name, obj_name, file_path, replace)
            self.source_uri = res.ipfs_url
            return res
        
class GithubRepo():

    def __init__(self, repo_owner: str, repo_name: str, repo_branch: str,  wallet_address: str, hardware_config: HardwareConfig, repo_uri: str = None):
    
        if repo_uri and not (repo_owner or repo_name):
            # TO DO: Add retrieve repo owner, name and branch from URI
            pass

        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_branch = repo_branch
        self.wallet_address = wallet_address
        self.hardware_config = hardware_config
        self.repo_uuid = str(uuid.uuid4())
        self.mcs_client = None
        self.source_uri = None
        self.file_list = []

    def mcs_connection(self, mcs_client: MCSAPI):
        """Add mcs connection.

        Args:
            mcs_client: mcs API object.
        """
        self.mcs_client = mcs_client
    
    def get_github_tree(self):
        github_tree_uri = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/git/trees/{self.repo_branch}?recursive=1"

        github_repo_files = requests.get(github_tree_uri).json()

        for file in github_repo_files["tree"]:
            if file["type"] == "blob":
                self.file_list.append(
                    {
                        "cid": file["sha"],
                        "created_at": None,
                        "name": file["path"],
                        "updated_at": None,
                        "url": f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.repo_branch}/{file['path']}"
                    }
                )
    
    def to_dict(self):
        hardware_info = self.hardware_config.description
        hardware_info = hardware_info.split(" · ")

        return {
            "data": {
                "files": self.file_list,
                "owner": {
                    "public_address": self.wallet_address,
                },
                "space": {
                    "activeOrder": {
                        "config": {
                            "description": self.hardware_config.description,
                            "hardware": hardware_info[0],
                            "hardware_id": int(self.hardware_config.id),
                            "hardware_type": self.hardware_config.type,
                            "memory": [int(s) for s in hardware_info[2].split() if s.isdigit()][0],
                            "name": self.hardware_config.name,
                            "price_per_hour": float(self.hardware_config.price),
                            "vcpu": [int(s) for s in hardware_info[1].split() if s.isdigit()][0],
                        },
                    },
                    "name": self.repo_name,
                    "uuid": self.repo_uuid,
                }
            }
        }

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def generate_source_uri(self, bucket_name: str, obj_name: str, file_path: str, mcs_client: MCSAPI = None, replace: bool = True):
        """Generate source uri for task using MCS service.

        Args:
            bucket_name: bucket name to store source uri.
            obj_name: object name (dir + file name) to store source uri.
            file_path: local file path to store source uri JSON file.
            replace: replace existing file or not.
            mcs_client: mcs API object.

        Returns：
            API response from MCS after uploading. Contains file information.

        """
        if mcs_client:
            self.mcs_connection(mcs_client)
            with open(file_path, "w") as file:
                json.dump(self.to_dict(), file)
            res = mcs_client.upload_file(bucket_name, obj_name, file_path, replace)
            self.source_uri = res.ipfs_url
            return res
import json
from swan.api.mcs_api import MCSAPI, File
from swan.common.utils import datetime_to_unixtime


class SourceFilesInfo():
    
    def __init__(self):
        self.file_list = []
        self.mcs_client = None
        
    def mcs_connection(self, mcs_client: MCSAPI):
        self.mcs_client = mcs_client

    def add_folder(self, bucket_name: str, object_name: str):
        folder_file = self.mcs_client._get_full_file_list(bucket_name, object_name)
        self.file_list += self.get_folder_files(bucket_name, folder_file)
        

    def add_file(self, bucket_name: str, object_name: str):
        file = self.mcs_client.get_file(bucket_name, object_name)
        list.append(file)

    def _file_to_dict(self, file: File):
        return {
            "cid": file.payloadCid,
            "created_at": datetime_to_unixtime(file.created_at),
            "name": file.name,
            "updated_at": datetime_to_unixtime(file.updated_at),
            "url": file.ipfs_url
        }
    
    def get_folder_files(self, bucket_name: str, file_list: list):
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
        return json.dump(self, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)
    

class Repository():

    def __init__(self):
        """Initialize repository for swan task.
        """
        self.folder_dir = None
        self.source_uri = None
        self.mcs_uri = None

    def update_repo_info(self, source_uri: str = None):
        """
        """

    def add_local_dir(self, folder_dir: str):
        """Initialize repository for swan task.

        Args:
            folder_dir: Directory of folder to upload to mcs.
        """
        self.folder_dir = folder_dir

    def mcs_connection(self, mcs_client: MCSAPI):
        self.mcs_client = mcs_client

    def upload_local_to_mcs(self, bucket_name: str, obj_name: str, mcs_client: MCSAPI = None):
        """Upload repository to MCS to create remote source.

        Args:

        Returns:
        """
        if self.folder_dir:
            if mcs_client:
                self.mcs_connection(mcs_client)
            upload = mcs_client.upload_folder(bucket_name, obj_name, self.folder_dir)
            self.mcs_uri = upload
            return upload
        return None

    def generate_source_uri(self, bucket_name: str, obj_name: str, file_path: str, replace: bool = True, mcs_client: MCSAPI = None):
        """Generate source uri for task using MCS service.

        Args:

        Returns：

        """
        if self.mcs_uri:
            if mcs_client:
                self.mcs_connection(mcs_client)
                local_source = SourceFilesInfo()
                local_source.add_folder(self.mcs_uri)
                upload = mcs_client.upload_file(bucket_name, obj_name, file_path, replace)
        return None
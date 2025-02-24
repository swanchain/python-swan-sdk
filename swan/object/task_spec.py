from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional
from abc import ABC, abstractmethod


class DeployType(IntEnum):
    # new CP ap: /lagrange/cp/deploy
    FIELD = 0
    DOCKERFILE = 1
    YAML = 2

    # old CP api: /lagrange/jobs
    SOURCE_URI = -99


@dataclass
class GpuSpec:
    gpu_model: str
    count: int


@dataclass
class HardwareSpec:
    cpu: int
    memory: float  # GiB
    storage: float  # GiB
    gpus: List[GpuSpec]
    instance_type: Optional[str] = None


class TaskSpec(ABC):
    """Abstract base class for all task types"""

    def __init__(
            self,
            hardware_spec: HardwareSpec,
            region: str = "global",
            start_in: int = 300,
            duration_in_secs: int = 3600,
            auto_pay_private_key: Optional[str] = None,
            preferred_cp_list: Optional[List[str]] = None,
            ip_whitelist: Optional[List[str]] = None,
    ):
        """Initialize a new TaskSpec instance.

        Args:
            wallet_address: The wallet_address that the user will pay for this task.
            hardware_spec (HardwareSpec): Specification of computing resources required for the task.
                Includes CPU, memory, storage, and GPU requirements.
            region (str, optional): Geographic region where the task should be deployed.
                Defaults to "global".
            start_in (int, optional): Expected start time of the task in seconds. Defaults to 300.
            duration_in_secs (int, optional): Duration for which computing resources should be
                allocated, in seconds. Defaults to 3600 (1 hour).
            auto_pay_private_key (Optional[str], optional): Private key for automatic payment
                processing. If not provided, manual payment will be required.
            preferred_cp_list (Optional[List[str]], optional): List of preferred computing
                providers for deployment. If not provided, all available providers will be considered.
            ip_whitelist (Optional[List[str]], optional): List of IP addresses allowed to access
                the deployed application. If not provided, access will not be restricted by IP.
        """
        self.region = region
        self.start_in = start_in
        self.duration_in_secs = duration_in_secs
        self.hardware_spec = hardware_spec
        self.auto_pay_private_key = auto_pay_private_key
        self.preferred_cp_list = preferred_cp_list
        self.ip_whitelist = ip_whitelist

    @abstractmethod
    def get_deployment_content(self) -> str:
        """Return the content needed for deployment"""
        pass

    @property
    @abstractmethod
    def deploy_type(self) -> DeployType:
        """Return the deployment type: None: old job deployment API,  0: field; 1: docker; 2: yaml """
        pass


class DockerfileTaskSpec(TaskSpec):
    def __init__(
            self,
            dockerfile_content: str,
            hardware_spec: HardwareSpec,
            *args,
            **kwargs
    ):
        """Initialize a new DockerfileTaskSpec instance.

        Args:
            dockerfile_content (str): Content of the Dockerfile to be used for deployment.
            *args: Variable length argument list for TaskSpec parameters.
            **kwargs: Arbitrary keyword arguments for TaskSpec parameters.
        """
        super().__init__(hardware_spec=hardware_spec, *args, **kwargs)
        self.dockerfile_content = dockerfile_content

    def get_deployment_content(self) -> str:
        return self.dockerfile_content

    @property
    def deploy_type(self) -> DeployType:
        return DeployType.DOCKERFILE


class YamlTaskSpec(TaskSpec):
    def __init__(
            self,
            yaml_content: str,
            hardware_spec: HardwareSpec,
            *args,
            **kwargs
    ):
        """Initialize a new YamlTaskSpec instance.

        Args:
            yaml_content (str): Content of the YAML file to be used for deployment.
            *args: Variable length argument list for TaskSpec parameters.
            **kwargs: Arbitrary keyword arguments for TaskSpec parameters.
        """
        super().__init__(hardware_spec=hardware_spec, *args, **kwargs)
        self.yaml_content = yaml_content

    def get_deployment_content(self) -> str:
        return self.yaml_content

    @property
    def deploy_type(self) -> DeployType:
        return DeployType.YAML


class ResourceUrlTaskSpec(TaskSpec):
    def __init__(
            self,
            resource_url: str,
            *args,
            **kwargs
    ):
        """Initialize a new ResourceUrlTaskSpec instance.

        Args:
            resource_url (str): URL pointing to the deployment resources
                (e.g., container registry, git repository, or other resource location).
            *args: Variable length argument list for TaskSpec parameters.
            **kwargs: Arbitrary keyword arguments for TaskSpec parameters.
        """
        super().__init__(*args, **kwargs)
        self.resource_url = resource_url

    @property
    def deploy_type(self) -> DeployType:
        return DeployType.SOURCE_URI

    def get_deployment_content(self) -> str:
        return self.resource_url


class TaskSpecFactory:
    """Factory class to create different types of task specifications"""

    @staticmethod
    def build_dockerfile_task(
            dockerfile_content: str,
            hardware_spec: HardwareSpec,
            region: str = "global",
            start_in: int = 300,
            duration_in_secs: int = 3600,
            auto_pay_private_key: Optional[str] = None,
            preferred_cp_list: Optional[List[str]] = None,
            ip_whitelist: Optional[List[str]] = None,
    ) -> DockerfileTaskSpec:
        return DockerfileTaskSpec(
            dockerfile_content=dockerfile_content,
            hardware_spec=hardware_spec,
            region=region,
            start_in=start_in,
            duration_in_secs=duration_in_secs,
            auto_pay_private_key=auto_pay_private_key,
            preferred_cp_list=preferred_cp_list,
            ip_whitelist=ip_whitelist
        )

    @staticmethod
    def build_yaml_task(
            yaml_content: str,
            hardware_spec: HardwareSpec,
            region: str = "global",
            start_in: int = 300,
            duration_in_secs: int = 3600,
            auto_pay_private_key: Optional[str] = None,
            preferred_cp_list: Optional[List[str]] = None,
            ip_whitelist: Optional[List[str]] = None,
    ) -> YamlTaskSpec:
        return YamlTaskSpec(
            yaml_content=yaml_content,
            hardware_spec=hardware_spec,
            region=region,
            start_in=start_in,
            duration_in_secs=duration_in_secs,
            auto_pay_private_key=auto_pay_private_key,
            preferred_cp_list=preferred_cp_list,
            ip_whitelist=ip_whitelist
        )

    @staticmethod
    def build_resource_url_task(
            resource_url: str,
            hardware_spec: HardwareSpec,
            region: str = "global",
            start_in: int = 300,
            duration_in_secs: int = 3600,
            auto_pay_private_key: Optional[str] = None,
            preferred_cp_list: Optional[List[str]] = None,
            ip_whitelist: Optional[List[str]] = None,
    ) -> ResourceUrlTaskSpec:
        return ResourceUrlTaskSpec(
            resource_url=resource_url,
            hardware_spec=hardware_spec,
            region=region,
            start_in=start_in,
            duration_in_secs=duration_in_secs,
            auto_pay_private_key=auto_pay_private_key,
            preferred_cp_list=preferred_cp_list,
            ip_whitelist=ip_whitelist
        )


# Example usage:
def example_usage():
    # Create hardware spec
    hardware = HardwareSpec(
        cpu=4,
        memory=16.0,
        storage=100.0,
        gpus=[GpuSpec(gpu_model="A100", count=1)]
    )

    # Create different types of tasks using the factory
    dockerfile_task = TaskSpecFactory.build_dockerfile_task(
        dockerfile_content="FROM python:3.9...",
        hardware_spec=hardware,
        preferred_cp_list=["0x2222", "0x3333"],
        ip_whitelist=["10.0.0.0/24"]
    )

    yaml_task = TaskSpecFactory.build_yaml_task(
        yaml_content="apiVersion: v1...",
        hardware_spec=hardware,
        region="us-east",
        auto_pay_private_key="private-key-123"
    )

    resource_task = TaskSpecFactory.build_resource_url_task(
        resource_url="https://registry.example.com/my-task",
        hardware_spec=hardware,
        duration_in_secs=7200
    )

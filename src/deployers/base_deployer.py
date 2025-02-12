from abc import ABC, abstractmethod
from src.utils.ssh_manager import SSHManager

class BaseDeployer(ABC):
    def __init__(self, ssh_manager: SSHManager):
        self.ssh = ssh_manager

    @abstractmethod
    def install_dependencies(self) -> bool:
        """Menginstall dependensi yang dibutuhkan"""
        pass

    @abstractmethod
    def setup_project(self, project_name: str) -> bool:
        """Menyiapkan proyek baru"""
        pass

    @abstractmethod
    def deploy(self, project_name: str) -> bool:
        """Mendeploy proyek"""
        pass

    def _run_command(self, command: str) -> bool:
        """Mengeksekusi command dan memeriksa hasilnya"""
        stdout, stderr = self.ssh.execute_command(command)
        if stderr:
            print(f"Error: {stderr}")
            return False
        print(f"Output: {stdout}")
        return True

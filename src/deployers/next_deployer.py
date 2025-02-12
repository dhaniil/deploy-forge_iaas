from src.deployers.base_deployer import BaseDeployer
from src.utils.ssh_manager import SSHManager

class NextDeployer(BaseDeployer):
    def __init__(self, ssh_manager: SSHManager):
        super().__init__(ssh_manager)

    def install_dependencies(self) -> bool:
        """Menginstall Node.js dan npm menggunakan NVM"""
        # Check if Node.js is already installed
        check_node_command = 'node --version'
        stdout, stderr = self.ssh.execute_command(check_node_command)
        if stdout:
            print("Node.js sudah terinstall.")
            return True
        
        commands = [
            # Install NVM
            'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash',
            # Install Node.js LTS
            'sudo export NVM_DIR="$HOME/.nvm" && sudo [ -s "$NVM_DIR/nvm.sh" ] && sudo . "$NVM_DIR/nvm.sh" && sudo nvm install --lts && sudo nvm use --lts',
            # Verifikasi instalasi
            # Verifikasi instalasi
            'node --version',
            'npm --version'
        ]
        
        for cmd in commands:
            if not self._run_command(cmd):
                return False
        return True

    def setup_project(self, project_name: str) -> bool:
        """Membuat proyek Next.js baru"""
        commands = [
            f'npx create-next-app@latest {project_name} --use-npm --typescript --tailwind --eslint --no-src-dir --app --import-alias "@/*"'
        ]
        
        for cmd in commands:
            if not self._run_command(cmd):
                return False
        return True

    def deploy(self, project_name: str) -> bool:
        """Menjalankan proyek Next.js dengan npm run dev"""
        commands = [
            f'cd {project_name}',
            'npm install',
            'npm run dev'
        ]
        
        for cmd in commands:
            if not self._run_command(cmd):
                return False
                
        return True

from src.deployers.base_deployer import BaseDeployer
from src.utils.ssh_manager import SSHManager
import time
import logging

logger = logging.getLogger(__name__)

class NextDeployer(BaseDeployer):
    def __init__(self, ssh_manager: SSHManager):
        super().__init__(ssh_manager)

    def install_dependencies(self) -> bool:
        """Menginstall Node.js dan npm menggunakan NVM"""
        # Cek versi Node.js dulu
        stdout, stderr = self.ssh.execute_command('node --version')
        if stdout.strip():
            logger.info(f"Node.js sudah terinstall: {stdout.strip()}")
            return True

        # Jika belum terinstall, install menggunakan NVM
        commands = [
            'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash',
            'export NVM_DIR="$HOME/.nvm"',
            '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"',
            'nvm install --lts',
            'nvm use --lts'
        ]
        
        for cmd in commands:
            logger.info(f"Menjalankan: {cmd}")
            stdout, stderr = self.ssh.execute_command(cmd)
            if stderr:
                logger.error(f"Error: {stderr}")
                return False
            logger.info(f"Output: {stdout}")
        return True

    def setup_project(self, project_name: str) -> bool:
        """Membuat proyek Next.js baru menggunakan create-next-app"""
        try:
            logger.info(f"Membuat proyek {project_name}...")
            create_cmd = (
                'printf "y\n" | ' +  # Jawab "Yes" untuk Turbopack
                f'npx create-next-app@latest {project_name} '
                '--typescript --tailwind --no-eslint --src-dir --no-app '
                '--import-alias "@/*" --no-git'
            )
            
            logger.info(f"Menjalankan: {create_cmd}")
            stdout, stderr = self.ssh.execute_command(create_cmd, wait_time=120)
            
            if stderr:
                logger.error(f"Error output: {stderr}")
            if stdout:
                logger.info(f"Command output: {stdout}")
            
            # Periksa apakah direktori project ada
            check_cmd = f'test -d {project_name} && echo "success"'
            stdout, _ = self.ssh.execute_command(check_cmd)
            if "success" in stdout:
                logger.info(f"✅ Proyek {project_name} berhasil dibuat!")
                return True
                
            logger.error(f"❌ Gagal membuat proyek: direktori tidak ditemukan")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error in setup_project: {str(e)}")
            return False

    def deploy(self, project_name: str) -> bool:
        """Menjalankan proyek Next.js dengan npm run dev"""
        try:
            # Kill proses yang mungkin masih berjalan di port 3000
            logger.info("Membersihkan port 3000...")
            self.ssh.execute_command("fuser -k 3000/tcp")
            time.sleep(2)
            
            # Install dependencies
            logger.info("Installing dependencies...")
            install_cmd = f'cd {project_name} && npm install'
            stdout, stderr = self.ssh.execute_command(install_cmd, wait_time=60)
            
            if stderr and "ERR!" in stderr:
                logger.error(f"Error installing dependencies: {stderr}")
                return False
            
            # Jalankan development server
            logger.info("Starting development server...")
            dev_cmd = (
                f'cd {project_name} && '
                'PORT=3000 npm run dev -- -p 3000 --hostname 0.0.0.0'
            )
            
            stdout, stderr = self.ssh.execute_command(dev_cmd, wait_time=15)
            
            # Verifikasi server berjalan
            time.sleep(10)
            check_cmd = 'curl -s http://localhost:3000 > /dev/null && echo "running"'
            stdout, _ = self.ssh.execute_command(check_cmd)
            
            if "running" in stdout:
                logger.info("✅ Development server berhasil dijalankan!")
                return True
                
            logger.error(f"❌ Error starting development server: {stderr}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error in deploy: {str(e)}")
            return False

from src.deployers.base_deployer import BaseDeployer
from src.utils.ssh_manager import SSHManager

class NodeDeployer(BaseDeployer):
    def __init__(self, ssh_manager: SSHManager):
        super().__init__(ssh_manager)

    def install_dependencies(self) -> bool:
        """Menginstall Node.js dan npm menggunakan NVM"""
        # Cek versi Node.js dulu
        stdout, stderr = self.ssh.execute_command('node --version')
        if stdout.strip():
            print(f"Node.js sudah terinstall: {stdout.strip()}")
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
            stdout, stderr = self.ssh.execute_command(cmd)
            print(f"Menjalankan: {cmd}")
            print(f"Output: {stdout}")
            if stderr:
                print(f"Error: {stderr}")
                return False
        return True

    def setup_project(self, project_name: str) -> bool:
        """Membuat proyek Node.js baru"""
        commands = [
            # Buat direktori proyek
            f'mkdir -p {project_name}',
            
            # Inisialisasi proyek npm
            f'''cd {project_name} && npm init -y && 
            npm install express && 
            echo 'const express = require("express");
const app = express();
const port = 3000;

app.get("/", (req, res) => {{
  res.send("Hello from Node.js!");
}});

app.listen(port, "0.0.0.0", () => {{
  console.log(`Server running at http://0.0.0.0:${{port}}`);
}});' > index.js'''
        ]
        
        for cmd in commands:
            print(f"Menjalankan: {cmd}")
            stdout, stderr = self.ssh.execute_command(cmd, wait_time=10)
            print(f"Output: {stdout}")
            if stderr:
                print(f"Error: {stderr}")
                return False
                
        return True

    def deploy(self, project_name: str) -> bool:
        """Menjalankan proyek Node.js"""
        run_cmd = f'cd {project_name} && node index.js'
        
        print(f"Menjalankan: {run_cmd}")
        stdout, stderr = self.ssh.execute_command(run_cmd)
        print(f"Output: {stdout}")
        if stderr:
            print(f"Error: {stderr}")
            return False
            
        return True

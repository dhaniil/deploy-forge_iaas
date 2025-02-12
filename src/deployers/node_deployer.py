from src.deployers.base_deployer import BaseDeployer
from src.utils.ssh_manager import SSHManager

class NodeDeployer(BaseDeployer):
    def __init__(self, ssh_manager: SSHManager):
        super().__init__(ssh_manager)

    def install_dependencies(self) -> bool:
        """Menginstall Node.js dan npm"""
        commands = [
            "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -",
            "sudo apt-get install -y nodejs",
            "sudo npm install -g npm@latest"
        ]
        
        for cmd in commands:
            if not self._run_command(cmd):
                return False
        return True

    def setup_project(self, project_name: str) -> bool:
        """Membuat proyek Node.js baru"""
        commands = [
            f"mkdir {project_name}",
            f"cd {project_name}",
            "npm init -y",
            "npm install express dotenv",
            # Membuat file server sederhana
            f"""echo 'const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

app.get("/", (req, res) => {{
  res.send("Hello from Node.js!");
}});

app.listen(port, () => {{
  console.log(`Server running at http://localhost:${{port}}`);
}});' > index.js"""
        ]
        
        for cmd in commands:
            if not self._run_command(cmd):
                return False
        return True

    def deploy(self, project_name: str) -> bool:
        """Mendeploy proyek Node.js"""
        commands = [
            f"cd {project_name}",
            # Install PM2 untuk process management
            "sudo npm install -g pm2",
            f"pm2 start index.js --name {project_name}"
        ]
        
        for cmd in commands:
            if not self._run_command(cmd):
                return False
        
        # Setup Nginx sebagai reverse proxy
        nginx_config = f"""
server {{
    listen 80;
    server_name _;

    location / {{
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }}
}}
"""
        
        # Menyimpan konfigurasi Nginx
        if not self._run_command(f"echo '{nginx_config}' | sudo tee /etc/nginx/sites-available/{project_name}"):
            return False
            
        nginx_commands = [
            f"sudo ln -s /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled/",
            "sudo nginx -t",
            "sudo systemctl restart nginx"
        ]
        
        for cmd in nginx_commands:
            if not self._run_command(cmd):
                return False
                
        return True

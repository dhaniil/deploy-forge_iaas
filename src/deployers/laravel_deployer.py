from src.deployers.base_deployer import BaseDeployer
from src.utils.ssh_manager import SSHManager

class LaravelDeployer(BaseDeployer):
    def install_dependencies(self) -> bool:
        # Memastikan composer tersedia dan menginstall dependensi
        if not self._run_command("command -v composer"):
            return False
        return self._run_command("composer install --no-dev")

    def setup_project(self, project_name: str) -> bool:
        commands = [
            "cp .env.example .env",
            "php artisan key:generate",
            "php artisan storage:link"
        ]
        return all(self._run_command(cmd) for cmd in commands)

    def deploy(self, project_name: str) -> bool:
        deploy_commands = [
            "php artisan migrate --force",
            "php artisan optimize:clear",
            "php artisan config:cache",
            "php artisan route:cache",
            "php artisan view:cache"
        ]
        return all(self._run_command(cmd) for cmd in deploy_commands)
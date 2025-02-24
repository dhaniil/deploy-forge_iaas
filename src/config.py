from typing import Dict, Type
from src.deployers.base_deployer import BaseDeployer
from src.deployers.next_deployer import NextDeployer
from src.deployers.node_deployer import NodeDeployer 
from src.deployers.laravel_deployer import LaravelDeployer

DEPLOYERS: Dict[str, Type[BaseDeployer]] = {
    "Next.js": NextDeployer,
    "Node.js": NodeDeployer,
    "Laravel": LaravelDeployer
}
import paramiko
import time
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class SSHManager:
    def __init__(self):
        self.client: Optional[paramiko.SSHClient] = None
        
    def connect(self, hostname: str, username: str, password: str, port: int = 22) -> bool:
        """Menghubungkan ke remote server menggunakan SSH"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=hostname, 
                              username=username,
                              password=password,
                              port=port)
            return True
        except Exception as e:
            logger.error(f"Kesalahan koneksi SSH: {str(e)}")
            return False
            
    def execute_command(self, command: str, wait_time: int = 5) -> Tuple[str, str]:
        """Mengeksekusi perintah di remote server dengan jeda waktu"""
        if not self.client:
            return "", "Tidak ada koneksi SSH yang aktif"
        
        try:
            # Setup environment dan path
            setup_env = '''
            export NVM_DIR="$HOME/.nvm"
            [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
            export PATH="$HOME/.nvm/versions/node/*/bin:$PATH"
            export NODE_OPTIONS="--max-old-space-size=4096"
            '''
            
            # Buat command dengan environment
            full_command = f'bash -c \'{setup_env}\n{command}\''
            
            logger.info("=== Menjalankan Command ===")
            logger.info(f"Command: {command}")
            
            # Jika command adalah npm run dev, tambahkan nohup
            if "npm run dev" in command:
                full_command = f'nohup {full_command} > /dev/null 2>&1 &'
            
            # Eksekusi command
            stdin, stdout, stderr = self.client.exec_command(full_command)
            
            # Untuk command panjang seperti create-next-app, stream output secara real-time
            if wait_time > 30:
                stdout_data = []
                stderr_data = []
                while not stdout.channel.exit_status_ready():
                    if stdout.channel.recv_ready():
                        chunk = stdout.channel.recv(1024).decode()
                        stdout_data.append(chunk)
                        logger.info(f"Progress: {chunk.strip()}")
                    if stderr.channel.recv_stderr_ready():
                        chunk = stderr.channel.recv_stderr(1024).decode()
                        stderr_data.append(chunk)
                        if "ERR!" in chunk:
                            logger.error(f"Error: {chunk.strip()}")
                        else:
                            logger.info(f"Info: {chunk.strip()}")
                    time.sleep(0.1)
                stdout_str = "".join(stdout_data)
                stderr_str = "".join(stderr_data)
            else:
                # Untuk command normal, tunggu sebentar lalu baca output
                time.sleep(wait_time)
                stdout_str = stdout.read().decode()
                stderr_str = stderr.read().decode()
            
            # Log output
            if stdout_str:
                logger.info(f"Output: {stdout_str}")
            if stderr_str and not any(x in stderr_str for x in ["npm WARN", "npm notice"]):
                logger.error(f"Error: {stderr_str}")
            
            logger.info("=========================")
            return stdout_str, stderr_str
            
        except Exception as e:
            error_msg = f"Kesalahan eksekusi command: {str(e)}"
            logger.error(error_msg)
            return "", error_msg
    
    def close(self):
        """Menutup koneksi SSH"""
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

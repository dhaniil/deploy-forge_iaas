import paramiko
from typing import Optional, Tuple

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
            print(f"Kesalahan koneksi SSH: {str(e)}")
            return False
            
    def execute_command(self, command: str) -> Tuple[str, str]:
        """Mengeksekusi perintah di remote server"""
        if not self.client:
            return "", "Tidak ada koneksi SSH yang aktif"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        except Exception as e:
            return "", f"Kesalahan eksekusi command: {str(e)}"
    
    def close(self):
        """Menutup koneksi SSH"""
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

import streamlit as st
from typing import Dict, Type

from src.deployers.base_deployer import BaseDeployer
from src.deployers.next_deployer import NextDeployer
from src.deployers.node_deployer import NodeDeployer
from src.utils.ssh_manager import SSHManager
from src.ui.forms import ssh_form, framework_form

def show_framework_page():
    """Menampilkan halaman utama deployer framework"""
    st.title("🚀 Framework Deployer")
    st.markdown("""
    Aplikasi ini membantu Anda mendeploy berbagai framework ke server remote melalui SSH.
    
    ### Cara Penggunaan:
    1. Masukkan kredensial SSH server Anda
    2. Pilih framework yang ingin di-deploy
    3. Tentukan nama proyek
    4. Klik tombol Deploy dan tunggu prosesnya selesai
    """)
    
    # SSH Form
    ssh_creds = ssh_form()
    
    if ssh_creds:
        with st.spinner("Menghubungkan ke server..."):
            ssh = SSHManager()
            if ssh.connect(
                hostname=ssh_creds.hostname,
                username=ssh_creds.username,
                password=ssh_creds.password,
                port=ssh_creds.port
            ):
                st.success("Berhasil terhubung ke server!")
                st.session_state.ssh = ssh
            else:
                st.error("Gagal terhubung ke server. Periksa kembali kredensial Anda.")
                return
    
    # Framework Form
    if hasattr(st.session_state, 'ssh'):
        framework, project_name = framework_form()
        
        if framework and project_name:
            deployers: Dict[str, Type[BaseDeployer]] = {
                "Next.js": NextDeployer,
                "Node.js": NodeDeployer
            }
            
            deployer = deployers[framework](st.session_state.ssh)
            
            with st.spinner("Menginstall dependensi..."):
                if not deployer.install_dependencies():
                    st.error("Gagal menginstall dependensi!")
                    return
                
            with st.spinner(f"Membuat proyek {project_name}..."):
                if not deployer.setup_project(project_name):
                    st.error("Gagal membuat proyek!")
                    return
                    
            with st.spinner("Mendeploy proyek..."):
                if not deployer.deploy(project_name):
                    st.error("Gagal mendeploy proyek!")
                    return
                    
            st.success(f"""
            ✅ Proyek berhasil di-deploy!
            
            Anda dapat mengakses aplikasi di:
            http://{st.session_state.ssh_creds.hostname}
            """)
            
            st.balloons()

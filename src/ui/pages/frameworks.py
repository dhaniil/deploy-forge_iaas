import streamlit as st
from typing import Dict, Type
import logging

from src.deployers.base_deployer import BaseDeployer
from src.deployers.next_deployer import NextDeployer
from src.deployers.node_deployer import NodeDeployer
from src.utils.ssh_manager import SSHManager
from src.ui.forms import ssh_form, framework_form

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_session_state():
    if 'ssh' not in st.session_state:
        st.session_state.ssh = None
    if 'ssh_creds' not in st.session_state:
        st.session_state.ssh_creds = None
    if 'deployer' not in st.session_state:
        st.session_state.deployer = None
    if 'log_output' not in st.session_state:
        st.session_state.log_output = []

def add_log(message: str):
    logger.info(message)
    st.session_state.log_output.append(message)
    
def show_logs():
    if st.session_state.log_output:
        with st.expander("📋 Log Output", expanded=True):
            log_text = "\n".join(st.session_state.log_output)
            st.text_area("", log_text, height=200)

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
    
    init_session_state()
    show_logs()
    
    # SSH Form
    if st.session_state.ssh is None:
        ssh_creds = ssh_form()
        if ssh_creds:
            with st.spinner("Menghubungkan ke server..."):
                add_log(f"Mencoba koneksi ke {ssh_creds.hostname}...")
                ssh = SSHManager()
                if ssh.connect(
                    hostname=ssh_creds.hostname,
                    username=ssh_creds.username,
                    password=ssh_creds.password,
                    port=ssh_creds.port
                ):
                    st.success("Berhasil terhubung ke server!")
                    add_log("✅ Koneksi SSH berhasil")
                    st.session_state.ssh = ssh
                    st.session_state.ssh_creds = ssh_creds
                else:
                    st.error("Gagal terhubung ke server. Periksa kembali kredensial Anda.")
                    add_log("❌ Koneksi SSH gagal")
                    return
    
    # Framework Form
    if st.session_state.ssh:
        framework, project_name = framework_form()
        
        if framework and project_name:
            status_container = st.empty()
            deployers: Dict[str, Type[BaseDeployer]] = {
                "Next.js": NextDeployer,
                "Node.js": NodeDeployer
            }
            
            if st.session_state.deployer is None:
                st.session_state.deployer = deployers[framework](st.session_state.ssh)
            
            with st.spinner(f"Memeriksa dependensi {framework}..."):
                add_log(f"Memeriksa Node.js dan npm...")
                status_container.info("Memeriksa Node.js dan npm...")
                if not st.session_state.deployer.install_dependencies():
                    st.error("Gagal menginstall dependensi!")
                    add_log("❌ Instalasi dependensi gagal")
                    return
                add_log("✅ Dependensi terinstall")
                status_container.success("✅ Dependensi terinstall")
                
            with st.spinner(f"Membuat proyek {project_name}..."):
                add_log(f"Membuat proyek {framework} baru: {project_name}")
                status_container.info(f"Membuat proyek {framework} baru...")
                if not st.session_state.deployer.setup_project(project_name):
                    st.error("Gagal membuat proyek!")
                    add_log("❌ Pembuatan proyek gagal")
                    return
                add_log("✅ Proyek berhasil dibuat")
                status_container.success("✅ Proyek berhasil dibuat")
                    
            with st.spinner("Menjalankan proyek..."):
                add_log("Memulai development server...")
                status_container.info("Memulai development server...")
                if not st.session_state.deployer.deploy(project_name):
                    st.error("Gagal menjalankan proyek!")
                    add_log("❌ Development server gagal dijalankan")
                    return
                add_log("✅ Development server berjalan")
                status_container.success("✅ Development server berjalan")
                    
            st.success(f"""
            ✅ Proyek berhasil di-deploy!
            
            Anda dapat mengakses aplikasi di:
            http://{st.session_state.ssh_creds.hostname}:3000
            """)
            
            st.info("""
            ℹ️ Tips:
            - Server berjalan dalam mode development
            - Akses menggunakan port 3000
            - Pastikan port 3000 sudah dibuka di firewall
            """)
            
            st.balloons()

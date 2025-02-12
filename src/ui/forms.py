import streamlit as st
from dataclasses import dataclass
from typing import Optional

@dataclass
class SSHCredentials:
    hostname: str
    username: str
    password: str
    port: int = 22

def ssh_form() -> Optional[SSHCredentials]:
    """Form untuk input kredensial SSH"""
    with st.form("ssh_credentials"):
        st.subheader("🔐 Kredensial SSH")
        
        col1, col2 = st.columns(2)
        with col1:
            hostname = st.text_input("IP Address/Hostname", placeholder="contoh: 192.168.1.100")
            username = st.text_input("Username", placeholder="contoh: ubuntu")
        
        with col2:
            password = st.text_input("Password", type="password")
            port = st.number_input("Port", min_value=1, max_value=65535, value=22)
            
        submitted = st.form_submit_button("Koneksi")
        
        if submitted:
            if not all([hostname, username, password]):
                st.error("Semua field harus diisi!")
                return None
                
            return SSHCredentials(
                hostname=hostname,
                username=username,
                password=password,
                port=port
            )
        
        return None

def framework_form():
    """Form untuk memilih framework yang akan diinstal"""
    st.subheader("🛠️ Pilih Framework")
    
    framework = st.selectbox(
        "Framework",
        options=["Next.js", "Node.js"],
        format_func=lambda x: {
            "Next.js": "Next.js - React Framework",
            "Node.js": "Node.js - JavaScript Runtime"
        }[x]
    )
    
    project_name = st.text_input(
        "Nama Proyek",
        placeholder="contoh: my-awesome-app",
        help="Nama ini akan digunakan sebagai nama direktori proyek"
    )
    
    deploy = st.button("Deploy")
    
    if deploy:
        if not project_name:
            st.error("Nama proyek harus diisi!")
            return None, None
            
        return framework, project_name
        
    return None, None

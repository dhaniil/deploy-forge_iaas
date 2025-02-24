import streamlit as st
from src.ui.pages.frameworks import show_framework_page

def main():
    st.set_page_config(
        page_title="DeployForge",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS untuk styling
    st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
        }
        .stTextInput > div > div > input {
            color: #31333F;
        }
        .stSelectbox > div > div > select {
            color: #31333F;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Tampilkan halaman utama
    show_framework_page()

if __name__ == "__main__":
    main()

"""
Sinhala Chatbot - Streamlit Web Interface
Offline chatbot using Ollama for local inference
"""

import streamlit as st
import time
import sys
import os

# Add modules directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ollama_client import OllamaClient
from modules.chat_manager import ChatManager
from modules.sinhala_utils import SinhalaUtils
from config.settings import STREAMLIT_TITLE, STREAMLIT_ICON, MODEL_NAME

# Page configuration
st.set_page_config(
    page_title=STREAMLIT_TITLE,
    page_icon=STREAMLIT_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better Sinhala rendering
st.markdown("""
<style>
    /* Improve Sinhala font rendering */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Sinhala:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Noto Sans Sinhala', 'Iskoola Pota', 'Segoe UI', 'Nirmala UI', sans-serif;
    }
    
    /* Chat message styling */
    .stChatMessage {
        margin-bottom: 1rem;
    }
    
    /* Input field styling */
    .stTextInput input {
        font-size: 1rem;
    }
    
    /* Better spacing for Sinhala text */
    .stMarkdown {
        line-height: 1.6;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: #00ff00;
        box-shadow: 0 0 5px #00ff00;
    }
    
    .status-offline {
        background-color: #ff0000;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    if "chat_manager" not in st.session_state:
        st.session_state.chat_manager = ChatManager()
    
    if "ollama_client" not in st.session_state:
        st.session_state.ollama_client = OllamaClient()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "connection_checked" not in st.session_state:
        st.session_state.connection_checked = False
    
    if "is_connected" not in st.session_state:
        st.session_state.is_connected = False
    
    if "model_exists" not in st.session_state:
        st.session_state.model_exists = False

def check_ollama_connection():
    """Check if Ollama is running"""
    if not st.session_state.connection_checked:
        st.session_state.is_connected = st.session_state.ollama_client.check_connection()
        if st.session_state.is_connected:
            st.session_state.model_exists = st.session_state.ollama_client.check_model_exists()
        st.session_state.connection_checked = True
    
    return st.session_state.is_connected

def display_chat_messages():
    """Display all chat messages"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Add timestamp if available
            if "timestamp" in message:
                st.caption(f"🕐 {message['timestamp'][:19]}")

def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ පාලන පුවරුව")
        st.markdown("---")
        
        # Connection Status
        st.subheader("🔌 සම්බන්ධතා තත්ත්වය")
        
        if check_ollama_connection():
            st.markdown('<span class="status-indicator status-online"></span> **Ollama**: සම්බන්ධයි', unsafe_allow_html=True)
            st.info(f"📦 **මාදිලිය**: `{MODEL_NAME}`")
            
            if not st.session_state.model_exists:
                st.warning(f"""
                ⚠️ **'{MODEL_NAME}' මාදිලිය සොයා ගත නොහැක**
                
                පහත විධානය ධාවනය කරන්න:
                ```bash
                ollama pull {MODEL_NAME}
                ```
                """)
"""
Configuration package for Sinhala Chatbot
"""

from .settings import *

__all__ = [
    'MODEL_NAME',
    'MAX_HISTORY_LENGTH',
    'MAX_RESPONSE_TOKENS',
    'TEMPERATURE',
    'OLLAMA_HOST',
    'OLLAMA_API_URL',
    'OLLAMA_TAGS_URL',
    'STREAMLIT_TITLE',
    'STREAMLIT_ICON',
    'SYSTEM_PROMPT'
]
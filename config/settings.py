"""
Configuration settings for the Sinhala Chatbot
"""

import os
import platform

# Model Configuration
MODEL_NAME = "llama2"  # or "gemma:2b" for faster responses

# Chat Configuration
MAX_HISTORY_LENGTH = 50
MAX_RESPONSE_TOKENS = 500
TEMPERATURE = 0.7

# Ollama Configuration - Update to use port 11435
if platform.system() == "Windows":
    OLLAMA_HOST = "http://127.0.0.1:11435"  # Changed from 11434 to 11435
else:
    OLLAMA_HOST = "http://127.0.0.1:11435"

# Override with environment variable if set
OLLAMA_HOST = os.getenv("OLLAMA_HOST", OLLAMA_HOST)
OLLAMA_API_URL = f"{OLLAMA_HOST}/api/generate"
OLLAMA_TAGS_URL = f"{OLLAMA_HOST}/api/tags"

# Streamlit Configuration
STREAMLIT_TITLE = "සිංහල චැට්බොට් - Sinhala Chatbot"
STREAMLIT_ICON = "🇱🇰"

# System Prompt for Sinhala responses
SYSTEM_PROMPT = """ඔබ සිංහල භාෂාවෙන් පිළිතුරු දෙන චැට්බොට් එකකි. 
ඔබගේ සියලු පිළිතුරු සිංහල භාෂාවෙන් පමණක් ලබා දිය යුතුය.
සංස්කෘතික වශයෙන් ගරුත්වයෙන් හා නිවැරදිව පිළිතුරු දෙන්න.
ඔබ ශ්‍රී ලාංකික සංස්කෘතිය, ඉතිහාසය සහ වටිනාකම් පිළිබඳ දැනුමක් ඇති අයෙකු ලෙස පිළිතුරු දෙන්න.

You are a chatbot that responds in Sinhala language only. 
All your responses must be in Sinhala language.
Respond with cultural respect and accuracy.
Respond as someone knowledgeable about Sri Lankan culture, history, and values."""
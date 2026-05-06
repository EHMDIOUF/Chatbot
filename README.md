# 🇱🇰 Sinhala Chatbot - Offline LLM Chatbot with Ollama

A fully offline Sinhala language chatbot powered by Ollama and Streamlit.

## Features

- 🗣️ **Sinhala Language Support**: Accepts input and generates responses in Sinhala
- 🔌 **Fully Offline**: No internet connection required after initial setup
- 💾 **Chat History**: Maintains conversation history within the session
- 🎨 **Streamlit UI**: Modern, responsive chat interface
- 📊 **Session Management**: Save and load chat sessions
- 🔧 **Local LLM**: Uses Ollama for local model inference

## Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. At least one model pulled (e.g., llama2, gemma, mistral)

## Installation

### Step 1: Clone or Create Project
```bash
mkdir sinhala-chatbot
cd sinhala-chatbot

(venv) PS C:\Users\LENOVO\Desktop\sinhala-chatbot> streamlit run app.py
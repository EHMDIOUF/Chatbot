"""
Ollama client for local LLM inference
"""

import json
import requests
from typing import Optional, List, Dict
import logging

from config.settings import (
    OLLAMA_API_URL,
    OLLAMA_TAGS_URL,
    MODEL_NAME,
    MAX_RESPONSE_TOKENS,
    TEMPERATURE,
    SYSTEM_PROMPT
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.api_url = OLLAMA_API_URL
        self.tags_url = OLLAMA_TAGS_URL
        self.system_prompt = SYSTEM_PROMPT
        
    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(self.tags_url, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama connection failed: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """List available models in Ollama"""
        try:
            response = requests.get(self.tags_url, timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model.get("name", "") for model in models]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
        return []
    
    def check_model_exists(self) -> bool:
        """Check if the configured model exists in Ollama"""
        models = self.list_models()
        return any(self.model_name in model for model in models)
    
    def generate_response(
        self, 
        user_message: str, 
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a response using Ollama
        
        Args:
            user_message: The user's input message
            chat_history: List of previous messages with 'role' and 'content'
        
        Returns:
            Generated response as string
        """
        # Prepare messages for Ollama
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add chat history
        if chat_history:
            # Limit history to prevent token overflow
            recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
            messages.extend(recent_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Prepare request payload
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": TEMPERATURE,
                "num_predict": MAX_RESPONSE_TOKENS
            }
        }
        
        try:
            # Make request to Ollama
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=120  # 120 second timeout for response generation
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "")
            elif response.status_code == 404:
                return f"සමාවන්න, '{self.model_name}' මාදිලිය සොයා ගත නොහැක. කරුණාකර 'ollama pull {self.model_name}' විධානය ධාවනය කරන්න."
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return "සමාවන්න, මට පිළිතුරු උත්පාදනය කිරීමට නොහැකි විය. කරුණාකර නැවත උත්සාහ කරන්න."
                
        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
            return "සමාවන්න, පිළිතුරු උත්පාදනයට වැඩි කාලයක් ගතවේ. කරුණාකර නැවත උත්සාහ කරන්න."
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama")
            return "සමාවන්න, Ollama සේවාදායකයට සම්බන්ධ විය නොහැක. කරුණාකර Ollama ධාවනය වන බවට තහවුරු කරගන්න."
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return f"සමාවන්න, දෝෂයක් ඇති විය. කරුණාකර නැවත උත්සාහ කරන්න."
    
    def generate_with_fallback(self, user_message: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate response with fallback for non-Sinhala responses
        """
        from modules.sinhala_utils import SinhalaUtils
        
        # First attempt
        response = self.generate_response(user_message, chat_history)
        
        # Check if response is in Sinhala
        if not SinhalaUtils.contains_sinhala(response):
            logger.info("Response not in Sinhala, trying with enhanced prompt")
            
            # Try with additional Sinhala instruction
            enhanced_message = f"කරුණාකර සිංහලෙන් පමණක් පිළිතුරු දෙන්න. ප්‍රශ්නය: {user_message}"
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\nIMPORTANT: You MUST respond in Sinhala language only."},
                {"role": "user", "content": enhanced_message}
            ]
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": TEMPERATURE,
                    "num_predict": MAX_RESPONSE_TOKENS
                }
            }
            
            try:
                response_obj = requests.post(self.api_url, json=payload, timeout=120)
                if response_obj.status_code == 200:
                    result = response_obj.json()
                    fallback_response = result.get("message", {}).get("content", "")
                    if SinhalaUtils.contains_sinhala(fallback_response):
                        return fallback_response
            except Exception as e:
                logger.error(f"Fallback failed: {e}")
        
        return response
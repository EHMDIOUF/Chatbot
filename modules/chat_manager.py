"""
Chat history management module
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class ChatManager:
    """Manages chat history and sessions"""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.current_session = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the current session
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.current_session.append(message)
        
        # Trim if exceeds max history
        if len(self.current_session) > self.max_history:
            self.current_session = self.current_session[-self.max_history:]
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages in current session"""
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.current_session
        ]
    
    def get_full_history(self) -> List[Dict]:
        """Get full history with timestamps"""
        return self.current_session.copy()
    
    def get_last_n_messages(self, n: int) -> List[Dict[str, str]]:
        """Get last N messages"""
        return self.get_messages()[-n:]
    
    def clear_history(self) -> None:
        """Clear current session history"""
        self.current_session = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def save_session(self, filepath: Optional[str] = None) -> str:
        """
        Save current session to file
        
        Args:
            filepath: Optional custom filepath
        
        Returns:
            Path where session was saved
        """
        if filepath is None:
            # Create data directory if it doesn't exist
            os.makedirs("data/chat_history", exist_ok=True)
            filepath = f"data/chat_history/session_{self.session_id}.json"
        
        session_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "total_messages": len(self.current_session),
            "messages": self.current_session
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            return filepath
        except Exception as e:
            print(f"Error saving session: {e}")
            return ""
    
    def load_session(self, filepath: str) -> bool:
        """
        Load a saved session from file
        
        Args:
            filepath: Path to session file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            self.current_session = session_data.get("messages", [])
            self.session_id = session_data.get("session_id", self.session_id)
            return True
        except Exception as e:
            print(f"Error loading session: {e}")
            return False
    
    def list_saved_sessions(self) -> List[str]:
        """List all saved session files"""
        sessions_dir = "data/chat_history"
        if not os.path.exists(sessions_dir):
            return []
        
        return [f for f in os.listdir(sessions_dir) if f.endswith('.json')]
    
    def get_session_stats(self) -> Dict:
        """Get statistics about current session"""
        user_messages = [m for m in self.current_session if m["role"] == "user"]
        assistant_messages = [m for m in self.current_session if m["role"] == "assistant"]
        
        # Calculate average message length
        user_lengths = [len(m["content"]) for m in user_messages] if user_messages else [0]
        assistant_lengths = [len(m["content"]) for m in assistant_messages] if assistant_messages else [0]
        
        return {
            "total_messages": len(self.current_session),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "avg_user_length": sum(user_lengths) / len(user_lengths) if user_lengths else 0,
            "avg_assistant_length": sum(assistant_lengths) / len(assistant_lengths) if assistant_lengths else 0,
            "session_id": self.session_id,
            "session_start": self.current_session[0]["timestamp"] if self.current_session else None
        }
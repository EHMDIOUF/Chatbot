"""
Sinhala language utilities for text processing
"""

import re
from typing import Optional, List

class SinhalaUtils:
    """Utility class for Sinhala text processing"""
    
    # Sinhala Unicode range: U+0D80 to U+0DFF
    SINHALA_UNICODE_RANGE = range(0x0D80, 0x0DFF)
    
    @staticmethod
    def is_sinhala_char(char: str) -> bool:
        """Check if a character is in Sinhala Unicode range"""
        if not char or len(char) == 0:
            return False
        try:
            code_point = ord(char[0])
            return code_point in SinhalaUtils.SINHALA_UNICODE_RANGE
        except TypeError:
            return False
    
    @staticmethod
    def contains_sinhala(text: str) -> bool:
        """Check if text contains any Sinhala characters"""
        if not text:
            return False
        return any(SinhalaUtils.is_sinhala_char(c) for c in text)
    
    @staticmethod
    def get_sinhala_words(text: str) -> List[str]:
        """Extract Sinhala words from text"""
        if not text:
            return []
        
        # Pattern to match Sinhala words (including combining characters)
        pattern = r'[\u0D80-\u0DFF]+(?:[\u0D82-\u0DFF])?'
        return re.findall(pattern, text)
    
    @staticmethod
    def clean_sinhala_text(text: str) -> str:
        """Clean and normalize Sinhala text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove zero-width joiners and other non-printable characters
        text = re.sub(r'[\u200B-\u200F\u202A-\u202E\uFEFF]', '', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\u0D80-\u0DFF\s\d\.,!?;:()\-]', '', text)
        
        return text.strip()
    
    @staticmethod
    def validate_sinhala_response(response: str) -> bool:
        """
        Validate if response contains sufficient Sinhala content
        Returns True if response has at least 30% Sinhala characters
        """
        if not response:
            return False
        
        total_chars = len(response.strip())
        if total_chars == 0:
            return False
        
        sinhala_chars = sum(1 for c in response if SinhalaUtils.is_sinhala_char(c))
        sinhala_ratio = sinhala_chars / total_chars
        
        # Accept if at least 30% of characters are Sinhala
        # Lower threshold to account for punctuation, numbers, etc.
        return sinhala_ratio >= 0.3
    
    @staticmethod
    def get_sinhala_percentage(text: str) -> float:
        """Calculate percentage of Sinhala characters in text"""
        if not text:
            return 0.0
        
        total_chars = len(text.strip())
        if total_chars == 0:
            return 0.0
        
        sinhala_chars = sum(1 for c in text if SinhalaUtils.is_sinhala_char(c))
        return (sinhala_chars / total_chars) * 100
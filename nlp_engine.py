"""
JARVIS Voice Agent - NLP Module
Handles natural language processing and intent recognition
"""

import re
import logging
from difflib import SequenceMatcher
from typing import Tuple, Dict, List, Any, Optional
from config import COMMANDS, CONFIDENCE_THRESHOLD

# Setup logging
logger = logging.getLogger(__name__)


class IntentRecognizer:
    """Recognizes user intent from text input using NLP techniques"""
    
    def __init__(self):
        """Initialize intent recognizer with commands from config"""
        self.commands = COMMANDS
        logger.info(f"IntentRecognizer initialized with {len(COMMANDS)} commands")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from user text"""
        try:
            entities = {
                "app_names": self._extract_app_names(text),
                "time_references": self._extract_time_refs(text),
                "numbers": re.findall(r'\d+', text),
                "email_addresses": self._extract_emails(text),
                "urls": self._extract_urls(text)
            }
            logger.debug(f"Extracted entities: {entities}")
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return {}
    
    def _extract_app_names(self, text: str) -> List[str]:
        """Extract application names from text"""
        common_apps = [
            "notepad", "calculator", "browser", "chrome", "firefox",
            "vscode", "spotify", "vlc", "terminal", "python", "git"
        ]
        found = []
        text_lower = text.lower()
        for app in common_apps:
            if app in text_lower:
                found.append(app)
        return found
    
    def _extract_time_refs(self, text: str) -> List[str]:
        """Extract time references from text"""
        time_patterns = [
            r'\b(\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?)\b',
            r'\b(morning|afternoon|evening|night|noon|midnight)\b',
            r'\b(today|tomorrow|yesterday)\b',
            r'\b(\d{1,2}(?:st|nd|rd|th))\b'
        ]
        matches = []
        for pattern in time_patterns:
            matches.extend(re.findall(pattern, text, re.IGNORECASE))
        return matches
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def recognize_intent(self, user_text: str) -> Tuple[Optional[str], float, Dict[str, Any]]:
        """
        Recognize user intent from text
        
        Returns:
            Tuple of (intent_name, confidence, entities)
        """
        try:
            user_text_normalized = user_text.lower().strip()
            best_intent = None
            best_confidence = 0.0
            best_specificity = 0
            
            logger.debug(f"Recognizing intent for: {user_text_normalized}")
            
            for intent_name, intent_config in self.commands.items():
                confidence = self._calculate_intent_confidence(
                    user_text_normalized,
                    intent_config["keywords"]
                )
                specificity = self._calculate_specificity(
                    user_text_normalized,
                    intent_config["keywords"]
                )
                
                # Update best match if this is better
                if confidence > best_confidence or (
                    confidence == best_confidence and specificity > best_specificity
                ):
                    best_confidence = confidence
                    best_intent = intent_name
                    best_specificity = specificity
            
            if best_confidence >= CONFIDENCE_THRESHOLD:
                logger.info(
                    f"Intent recognized: {best_intent} "
                    f"(confidence: {best_confidence:.2f}, specificity: {best_specificity})"
                )
                return best_intent, best_confidence, self.extract_entities(user_text_normalized)
            
            logger.warning(
                f"No intent recognized above threshold. "
                f"Best: {best_intent} ({best_confidence:.2f})"
            )
            return None, 0.0, {}
        
        except Exception as e:
            logger.error(f"Error recognizing intent: {e}", exc_info=True)
            return None, 0.0, {}
    
    def _calculate_intent_confidence(self, text: str, keywords: List[str]) -> float:
        """Calculate confidence score for matching keywords"""
        try:
            max_similarity = 0.0
            text_lower = text.lower()
            text_tokens = set(re.findall(r"\w+", text_lower))
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                keyword_tokens = set(re.findall(r"\w+", keyword_lower))
                
                # String similarity
                string_similarity = SequenceMatcher(None, text_lower, keyword_lower).ratio()
                
                # Token similarity
                token_similarity = 0.0
                if keyword_tokens:
                    shared_tokens = text_tokens.intersection(keyword_tokens)
                    token_similarity = len(shared_tokens) / len(keyword_tokens)
                
                # Combine both
                similarity = max(string_similarity, token_similarity)
                max_similarity = max(max_similarity, similarity)
            
            return max_similarity
        
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.0
    
    def _calculate_specificity(self, text: str, keywords: List[str]) -> int:
        """Calculate how specific the intent match is based on keyword match size"""
        try:
            specificity = 0
            text_lower = text.lower()
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                # Use word boundaries for exact keyword matching
                if re.search(rf"\b{re.escape(keyword_lower)}\b", text_lower):
                    specificity += len(keyword_lower.split())
            
            return specificity
        
        except Exception as e:
            logger.error(f"Error calculating specificity: {e}")
            return 0
    
    def extract_parameters(self, user_text: str, intent_name: str) -> Dict[str, Any]:
        """Extract specific parameters based on intent"""
        try:
            params = {}
            user_text_lower = user_text.lower()
            
            if intent_name == "open_app":
                entities = self.extract_entities(user_text_lower)
                if entities.get("app_names"):
                    params["app"] = entities["app_names"][0]
                    logger.debug(f"Extracted app parameter: {params['app']}")
            
            elif intent_name == "reminder":
                # Extract reminder text
                words = user_text.split()
                reminder_start = -1
                for i, word in enumerate(words):
                    if word.lower() in ["remind", "reminder", "remember"]:
                        reminder_start = i + 1
                        break
                if reminder_start != -1 and reminder_start < len(words):
                    params["reminder_text"] = " ".join(words[reminder_start:])
                    logger.debug(f"Extracted reminder: {params['reminder_text']}")
            
            elif intent_name == "search":
                # Extract search query
                words = user_text.split()
                search_start = -1
                for i, word in enumerate(words):
                    if word.lower() in ["search", "find", "look", "lookup"]:
                        search_start = i + 1
                        break
                if search_start != -1 and search_start < len(words):
                    params["query"] = " ".join(words[search_start:])
                    logger.debug(f"Extracted search query: {params['query']}")
            
            return params
        
        except Exception as e:
            logger.error(f"Error extracting parameters: {e}")
            return {}
    
    def get_supported_intents(self) -> List[str]:
        """Get list of all supported intents"""
        return list(self.commands.keys())
    
    def get_intent_info(self, intent_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific intent"""
        if intent_name in self.commands:
            return self.commands[intent_name]
        return None

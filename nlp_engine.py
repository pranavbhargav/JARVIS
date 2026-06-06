"""
JARVIS Voice Agent - NLP Module
Handles natural language processing and intent recognition
"""

import re
from difflib import SequenceMatcher
from config import COMMANDS, CONFIDENCE_THRESHOLD

class IntentRecognizer:
    """Recognizes user intent from text input"""
    
    def __init__(self):
        self.commands = COMMANDS
        
    def extract_entities(self, text):
        """Extract entities from user text"""
        entities = {
            "app_names": self._extract_app_names(text),
            "time_references": self._extract_time_refs(text),
            "numbers": re.findall(r'\d+', text)
        }
        return entities
    
    def _extract_app_names(self, text):
        """Extract application names from text"""
        common_apps = ["notepad", "calculator", "browser", "chrome", "firefox", 
                      "vscode", "spotify", "vlc"]
        found = []
        for app in common_apps:
            if app.lower() in text.lower():
                found.append(app)
        return found
    
    def _extract_time_refs(self, text):
        """Extract time references from text"""
        time_patterns = [
            r'\b(\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?)\b',
            r'\b(morning|afternoon|evening|night|noon|midnight)\b'
        ]
        matches = []
        for pattern in time_patterns:
            matches.extend(re.findall(pattern, text, re.IGNORECASE))
        return matches
    
    def recognize_intent(self, user_text):
        """
        Recognize user intent from text
        Returns: (intent_name, confidence, entities)
        """
        user_text = user_text.lower().strip()
        best_intent = None
        best_confidence = 0
        best_specificity = 0
        
        for intent_name, intent_config in self.commands.items():
            confidence = self._calculate_intent_confidence(
                user_text, 
                intent_config["keywords"]
            )
            specificity = self._calculate_specificity(user_text, intent_config["keywords"])
            
            if confidence > best_confidence or (
                confidence == best_confidence and specificity > best_specificity
            ):
                best_confidence = confidence
                best_intent = intent_name
                best_specificity = specificity
        
        if best_confidence >= CONFIDENCE_THRESHOLD:
            return best_intent, best_confidence, self.extract_entities(user_text)
        
        return None, 0.0, {}
    
    def _calculate_intent_confidence(self, text, keywords):
        """Calculate confidence score for matching keywords"""
        max_similarity = 0
        text = text.lower()
        text_tokens = set(re.findall(r"\w+", text))
        
        for keyword in keywords:
            keyword_text = keyword.lower()
            keyword_tokens = set(re.findall(r"\w+", keyword_text))
            similarity = SequenceMatcher(None, text, keyword_text).ratio()
            
            if keyword_tokens:
                shared_tokens = text_tokens.intersection(keyword_tokens)
                token_similarity = len(shared_tokens) / len(keyword_tokens)
                similarity = max(similarity, token_similarity)
            
            max_similarity = max(max_similarity, similarity)
        
        return max_similarity

    def _calculate_specificity(self, text, keywords):
        """Calculate how specific the intent match is based on keyword match size"""
        specificity = 0
        for keyword in keywords:
            keyword_text = keyword.lower()
            if re.search(rf"\b{re.escape(keyword_text)}\b", text):
                specificity += len(keyword_text.split())
        return specificity
    
    def extract_parameters(self, user_text, intent_name):
        """Extract specific parameters based on intent"""
        params = {}
        user_text = user_text.lower()
        
        if intent_name == "open_app":
            entities = self.extract_entities(user_text)
            if entities["app_names"]:
                params["app"] = entities["app_names"][0]
        
        elif intent_name == "reminder":
            # Extract reminder text
            words = user_text.split()
            reminder_start = -1
            for i, word in enumerate(words):
                if word in ["remind", "reminder"]:
                    reminder_start = i + 1
                    break
            if reminder_start != -1:
                params["reminder_text"] = " ".join(words[reminder_start:])
        
        elif intent_name == "search":
            # Extract search query
            words = user_text.split()
            search_start = -1
            for i, word in enumerate(words):
                if word in ["search", "find", "look"]:
                    search_start = i + 1
                    break
            if search_start != -1:
                params["query"] = " ".join(words[search_start:])
        
        return params

"""
JARVIS Voice Agent - Utilities
Helper functions and utilities
"""

import json
import os
from datetime import datetime


class Logger:
    """Simple logging utility"""
    
    def __init__(self, log_file="jarvis_log.txt"):
        self.log_file = log_file
    
    def log(self, message, level="INFO"):
        """Log a message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level}: {message}"
        
        print(log_message)
        
        with open(self.log_file, "a") as f:
            f.write(log_message + "\n")
    
    def log_intent(self, user_input, intent_name, confidence):
        """Log recognized intent"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "intent": intent_name,
            "confidence": confidence
        }
        
        self.log(json.dumps(log_entry), level="INTENT")


class ConfigManager:
    """Manage agent configuration"""
    
    @staticmethod
    def load_config(config_file):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_config(config_file, config):
        """Save configuration to JSON file"""
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)


class CommandRegistry:
    """Registry for managing custom commands"""
    
    def __init__(self):
        self.custom_commands = {}
    
    def register(self, command_name, keywords, handler):
        """Register a new command"""
        self.custom_commands[command_name] = {
            "keywords": keywords,
            "handler": handler
        }
    
    def get_command(self, command_name):
        """Get a registered command"""
        return self.custom_commands.get(command_name)
    
    def list_commands(self):
        """List all registered commands"""
        return list(self.custom_commands.keys())


def validate_intent_config(config):
    """Validate intent configuration"""
    required_fields = ["keywords", "responses", "action"]
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    if not isinstance(config["keywords"], list):
        raise ValueError("Keywords must be a list")
    
    if not isinstance(config["responses"], list):
        raise ValueError("Responses must be a list")
    
    return True


def extract_domain_from_intent(intent_name):
    """Extract domain category from intent name"""
    domains = {
        "greeting": "communication",
        "goodbye": "communication",
        "time": "information",
        "date": "information",
        "weather": "information",
        "reminder": "productivity",
        "open_app": "system",
        "search": "information"
    }
    
    return domains.get(intent_name, "general")

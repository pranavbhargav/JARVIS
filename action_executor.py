"""
JARVIS Voice Agent - Action Executor
Executes actions based on recognized intents
"""

import os
import subprocess
import webbrowser
import random
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable
from config import COMMANDS
from enum import Enum


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Enumeration of supported action types"""
    RESPOND = "respond"
    GET_TIME = "get_time"
    GET_DATE = "get_date"
    GET_WEATHER = "get_weather"
    SET_REMINDER = "set_reminder"
    OPEN_APPLICATION = "open_application"
    SEARCH_WEB = "search_web"
    TELL_JOKE = "tell_joke"
    EXIT = "exit"


class ActionExecutor:
    """Executes actions based on recognized intents"""
    
    # Default joke collection
    DEFAULT_JOKES = [
        "Why did the programmer quit his job? Because he didn't get arrays!",
        "Why do Java developers wear glasses? Because they don't C#!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        "Why was the computer cold? It left its Windows open!"
    ]
    
    # Application command mappings per OS
    APP_COMMANDS = {
        "notepad": {
            "nt": "notepad.exe",
            "default": "gedit"
        },
        "calculator": {
            "nt": "calc.exe",
            "default": "gnome-calculator"
        },
        "chrome": {
            "nt": "chrome.exe",
            "default": "chrome"
        },
        "firefox": {
            "nt": "firefox.exe",
            "default": "firefox"
        },
        "vscode": {
            "nt": "code.exe",
            "default": "code"
        },
        "spotify": {
            "nt": "spotify.exe",
            "default": "spotify"
        },
        "vlc": {
            "nt": "vlc.exe",
            "default": "vlc"
        }
    }
    
    def __init__(self, voice_output):
        """
        Initialize ActionExecutor
        
        Args:
            voice_output: VoiceOutput instance for speaking responses
        """
        self.voice_output = voice_output
        self.reminders = []
        self.jokes = self.DEFAULT_JOKES.copy()
        
        # Action handler mapping
        self.action_handlers: Dict[ActionType, Callable] = {
            ActionType.RESPOND: self._handle_response,
            ActionType.GET_TIME: self._handle_get_time,
            ActionType.GET_DATE: self._handle_get_date,
            ActionType.GET_WEATHER: self._handle_get_weather,
            ActionType.SET_REMINDER: self._handle_set_reminder,
            ActionType.OPEN_APPLICATION: self._handle_open_app,
            ActionType.SEARCH_WEB: self._handle_search_web,
            ActionType.TELL_JOKE: self._handle_tell_joke,
            ActionType.EXIT: self._handle_exit,
        }
    
    def execute(self, intent_name: str, parameters: Optional[Dict[str, Any]] = None) -> bool:
        """
        Execute action based on intent
        
        Args:
            intent_name: Name of the intent to execute
            parameters: Optional parameters for the intent
            
        Returns:
            True if execution was successful, False otherwise
        """
        try:
            if intent_name not in COMMANDS:
                logger.warning(f"Unknown intent: {intent_name}")
                self.voice_output.speak("I'm not sure what you mean.")
                return False
            
            intent_config = COMMANDS[intent_name]
            action_type_str = intent_config.get("action")
            
            # Validate action type
            try:
                action_type = ActionType(action_type_str)
            except ValueError:
                logger.error(f"Unknown action type: {action_type_str}")
                self.voice_output.speak("I can't perform that action yet.")
                return False
            
            # Get and execute handler
            handler = self.action_handlers.get(action_type)
            if handler:
                handler(intent_config, parameters)
                return True
            else:
                logger.error(f"No handler for action type: {action_type}")
                self.voice_output.speak("I can't perform that action yet.")
                return False
                
        except Exception as e:
            logger.error(f"Error executing intent '{intent_name}': {e}", exc_info=True)
            self.voice_output.speak("An error occurred while performing that action.")
            return False
    
    def _handle_response(self, intent_config: Dict, parameters: Optional[Dict] = None):
        """Handle simple text response"""
        response = random.choice(intent_config["responses"])
        self.voice_output.speak(response)
    
    def _handle_get_time(self, intent_config: Dict, parameters: Optional[Dict] = None):
        """Get and speak current time"""
        try:
            current_time = datetime.now().strftime("%I:%M %p")
            response = random.choice(intent_config["responses"]).format(data=current_time)
            self.voice_output.speak(response)
        except Exception as e:
            logger.error(f"Error getting time: {e}")
            self.voice_output.speak("I couldn't get the current time.")
    
    def _handle_get_date(self, intent_config: Dict, parameters: Optional[Dict] = None):
        """Get and speak current date"""
        try:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            response = random.choice(intent_config["responses"]).format(data=current_date)
            self.voice_output.speak(response)
        except Exception as e:
            logger.error(f"Error getting date: {e}")
            self.voice_output.speak("I couldn't get the current date.")
    
    def _handle_get_weather(self, intent_config: Dict, parameters: Optional[Dict] = None):
        """Fetch and speak weather information"""
        try:
            import requests
            response = requests.get(
                "https://wttr.in/?format=3",
                timeout=5
            )
            response.raise_for_status()
            weather_data = response.text.strip()
            response_text = random.choice(intent_config["responses"]).format(data=weather_data)
            self.voice_output.speak(response_text)
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API request error: {e}")
            self.voice_output.speak("Sorry, I couldn't fetch weather information.")
        except Exception as e:
            logger.error(f"Weather handling error: {e}")
            self.voice_output.speak("Sorry, I couldn't fetch weather information.")
    
    def _handle_set_reminder(self, intent_config: Dict, parameters: Optional[Dict] = None):
        """Set a reminder"""
        try:
            reminder_text = (
                parameters.get("reminder_text", "Reminder set") 
                if parameters 
                else "Reminder set"
            )
            
            reminder = {
                "text": reminder_text,
                "created_at": datetime.now(),
                "id": len(self.reminders) + 1
            }
            
            self.reminders.append(reminder)
            response = random.choice(intent_config["responses"]).format(data=reminder_text)
            self.voice_output.speak(response)
            logger.info(f"Reminder set: {reminder_text}")
        except Exception as e:
            logger.error(f"Error setting reminder: {e}")
            self.voice_output.speak("I couldn't set the reminder.")
    
    def _handle_open_app(self, intent_config: Dict, parameters: Optional[Dict] = None):
        """Open an application"""
        try:
            app = parameters.get("app") if parameters else None
            
            if not app:
                self.voice_output.speak("Which application would you like me to open?")
                return
            
            app_lower = app.lower()
            
            if app_lower not in self.APP_COMMANDS:
                logger.warning(f"Unknown application: {app}")
                self.voice_output.speak(f"I don't know how to open {app}.")
                return
            
            # Get appropriate command for OS
            app_cmd_config = self.APP_COMMANDS[app_lower]
            command = app_cmd_config.get(
                os.name, 
                app_cmd_config.get("default", app_lower)
            )
            
            subprocess.Popen(command)
            response = random.choice(intent_config["responses"]).format(data=app)
            self.voice_output.speak(response)
            logger.info(f"Opened application: {app}")
            
        except FileNotFoundError:
            logger.error(f"Application not found: {app}")
            self.voice_output.speak(f"I couldn't find {app} on your system.")
        except Exception as e:
            logger.error(f"Error opening app '{app}': {e}")
            self.voice_output.speak(f"I couldn't open {app}.")
    
    def _handle_search_web(self, intent_config: Dict, parameters: Optional[Dict] = None):
        """Search on the web"""
        try:
            query = parameters.get("query") if parameters else None
            
            if not query:
                self.voice_output.speak("What would you like me to search for?")
                return
            
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            response = random.choice(intent_config["responses"]).format(data=query)
            self.voice_output.speak(response)
            logger.info(f"Web search performed: {query}")
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            self.voice_output.speak("I couldn't perform the search.")
    
    def _handle_tell_joke(self, intent_config: Dict = None, parameters: Optional[Dict] = None):
        """Tell a random joke"""
        try:
            joke = random.choice(self.jokes)
            self.voice_output.speak(joke)
            logger.info("Joke told")
        except Exception as e:
            logger.error(f"Error telling joke: {e}")
            self.voice_output.speak("I couldn't tell a joke right now.")
    
    def _handle_exit(self, intent_config: Dict, parameters: Optional[Dict] = None):
        """Handle exit gracefully"""
        try:
            response = random.choice(intent_config["responses"])
            self.voice_output.speak(response)
            logger.info("JARVIS shutting down")
        except Exception as e:
            logger.error(f"Error during exit: {e}")
    
    def get_reminders(self) -> list:
        """
        Get list of all reminders
        
        Returns:
            List of reminder dictionaries
        """
        return self.reminders
    
    def get_pending_reminders(self) -> list:
        """
        Get reminders created in the last hour
        
        Returns:
            List of recent reminder dictionaries
        """
        one_hour_ago = datetime.now() - timedelta(hours=1)
        return [
            reminder for reminder in self.reminders
            if reminder["created_at"] > one_hour_ago
        ]
    
    def clear_reminders(self):
        """Clear all reminders"""
        self.reminders.clear()
        logger.info("All reminders cleared")
    
    def clear_reminder_by_id(self, reminder_id: int) -> bool:
        """
        Clear a specific reminder by ID
        
        Args:
            reminder_id: ID of the reminder to clear
            
        Returns:
            True if reminder was found and cleared, False otherwise
        """
        for i, reminder in enumerate(self.reminders):
            if reminder.get("id") == reminder_id:
                self.reminders.pop(i)
                logger.info(f"Reminder {reminder_id} cleared")
                return True
        return False
    
    def add_custom_joke(self, joke: str):
        """
        Add a custom joke to the joke collection
        
        Args:
            joke: Joke text to add
        """
        self.jokes.append(joke)
        logger.info(f"Custom joke added: {joke}")
    
    def add_application_command(self, app_name: str, windows_cmd: str, default_cmd: str):
        """
        Add a custom application command
        
        Args:
            app_name: Name of the application
            windows_cmd: Command for Windows systems
            default_cmd: Command for other systems
        """
        self.APP_COMMANDS[app_name.lower()] = {
            "nt": windows_cmd,
            "default": default_cmd
        }
        logger.info(f"Application command added: {app_name}")

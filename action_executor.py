"""
JARVIS Voice Agent - Action Executor
Executes actions based on recognized intents
"""

import os
import subprocess
import webbrowser
import random
from datetime import datetime
from config import COMMANDS


class ActionExecutor:
    """Executes actions based on recognized intents"""
    
    def __init__(self, voice_output):
        self.voice_output = voice_output
        self.reminders = []
    
    def execute(self, intent_name, parameters=None):
        """
        Execute action based on intent
        """
        if intent_name not in COMMANDS:
            self.voice_output.speak("I'm not sure what you mean.")
            return False
        
        intent_config = COMMANDS[intent_name]
        action_type = intent_config.get("action")
        
        # Route to appropriate action handler
        if action_type == "respond":
            self._handle_response(intent_config)
        elif action_type == "get_time":
            self._handle_get_time(intent_config)
        elif action_type == "get_date":
            self._handle_get_date(intent_config)
        elif action_type == "get_weather":
            self._handle_get_weather(intent_config)
        elif action_type == "set_reminder":
            self._handle_set_reminder(intent_config, parameters)
        elif action_type == "open_application":
            self._handle_open_app(intent_config, parameters)
        elif action_type == "search_web":
            self._handle_search_web(intent_config, parameters)
        elif action_type == "tell_joke":
            self._handle_tell_joke()
        elif action_type == "exit":
            self._handle_exit(intent_config)
        else:
            self.voice_output.speak("I can't perform that action yet.")
            return False
        
        return True
    
    def _handle_response(self, intent_config):
        """Handle simple response"""
        response = random.choice(intent_config["responses"])
        self.voice_output.speak(response)
    
    def _handle_get_time(self, intent_config):
        """Get current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        response = random.choice(intent_config["responses"]).format(data=current_time)
        self.voice_output.speak(response)
    
    def _handle_get_date(self, intent_config):
        """Get current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        response = random.choice(intent_config["responses"]).format(data=current_date)
        self.voice_output.speak(response)
    
    def _handle_get_weather(self, intent_config):
        """Get weather information"""
        try:
            import requests
            response = requests.get(
                "https://wttr.in/?format=3",
                timeout=5
            )
            weather_data = response.text.strip()
            response_text = random.choice(intent_config["responses"]).format(data=weather_data)
            self.voice_output.speak(response_text)
        except Exception as e:
            self.voice_output.speak("Sorry, I couldn't fetch weather information.")
            print(f"Weather API error: {e}")
    
    def _handle_set_reminder(self, intent_config, parameters):
        """Set a reminder"""
        reminder_text = parameters.get("reminder_text", "Reminder set") if parameters else "Reminder set"
        self.reminders.append({
            "text": reminder_text,
            "created_at": datetime.now()
        })
        response = random.choice(intent_config["responses"]).format(data=reminder_text)
        self.voice_output.speak(response)
    
    def _handle_open_app(self, intent_config, parameters):
        """Open an application"""
        app = parameters.get("app") if parameters else None
        
        if not app:
            self.voice_output.speak("Which application would you like me to open?")
            return
        
        app_commands = {
            "notepad": ("notepad.exe" if os.name == "nt" else "gedit"),
            "calculator": ("calc.exe" if os.name == "nt" else "gnome-calculator"),
            "chrome": ("chrome" if os.name != "nt" else "chrome.exe"),
            "firefox": "firefox",
            "vscode": "code",
            "spotify": "spotify",
            "vlc": "vlc"
        }
        
        app_lower = app.lower()
        if app_lower in app_commands:
            try:
                subprocess.Popen(app_commands[app_lower])
                response = random.choice(intent_config["responses"]).format(data=app)
                self.voice_output.speak(response)
            except Exception as e:
                self.voice_output.speak(f"I couldn't open {app}.")
                print(f"Error opening app: {e}")
        else:
            self.voice_output.speak(f"I don't know how to open {app}.")
    
    def _handle_search_web(self, intent_config, parameters):
        """Search on the web"""
        query = parameters.get("query") if parameters else None
        
        if not query:
            self.voice_output.speak("What would you like me to search for?")
            return
        
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            response = random.choice(intent_config["responses"]).format(data=query)
            self.voice_output.speak(response)
        except Exception as e:
            self.voice_output.speak("I couldn't perform the search.")
            print(f"Search error: {e}")
    
    def _handle_tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "Why do Java developers wear glasses? Because they don't C#!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why was the computer cold? It left its Windows open!"
        ]
        joke = random.choice(jokes)
        self.voice_output.speak(joke)
    
    def _handle_exit(self, intent_config):
        """Exit the agent"""
        response = random.choice(intent_config["responses"])
        self.voice_output.speak(response)
    
    def get_reminders(self):
        """Get list of reminders"""
        return self.reminders
    
    def clear_reminders(self):
        """Clear all reminders"""
        self.reminders.clear()

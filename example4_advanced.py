"""
Example 4: Advanced - Custom Action Handlers
Extend JARVIS with custom action handlers for specific intents
"""

from agent import VoiceAgent
from action_executor import ActionExecutor
from voice_io import VoiceOutput
from config import COMMANDS


class ExtendedActionExecutor(ActionExecutor):
    """Extended action executor with custom handlers"""
    
    def execute(self, intent_name, parameters=None):
        """Execute action with custom handlers"""
        
        # Call custom handlers first
        if intent_name == "joke":
            self._handle_tell_joke()
            return True
        
        elif intent_name == "system_info":
            self._handle_system_info()
            return True
        
        # Fall back to default executor
        return super().execute(intent_name, parameters)
    
    def _handle_tell_joke(self):
        """Handle joke command"""
        jokes = [
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "Why do Java developers wear glasses? Because they don't C sharp!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why did the developer go broke? Because he used up all his cache!"
        ]
        import random
        joke = random.choice(jokes)
        self.voice_output.speak(joke)
    
    def _handle_system_info(self):
        """Handle system info command"""
        try:
            import platform
            import psutil
            
            info = f"System: {platform.system()} {platform.release()}. "
            info += f"Processor: {platform.processor()}. "
            info += f"CPU Usage: {psutil.cpu_percent()}%"
            
            self.voice_output.speak(info)
        except ImportError:
            self.voice_output.speak("System information module not available.")


def main():
    # Create agent
    agent = VoiceAgent(name="JARVIS", use_voice=False)
    
    # Replace default executor with extended one
    agent.action_executor = ExtendedActionExecutor(agent.voice_output)
    
    # Add custom commands
    agent.add_custom_command(
        intent_name="joke",
        keywords=["tell joke", "make me laugh", "funny"],
        responses=["Here's a joke for you"],
        action="tell_joke"
    )
    
    agent.add_custom_command(
        intent_name="system_info",
        keywords=["system info", "computer info", "about this computer"],
        responses=["Here's your system information"],
        action="system_info"
    )
    
    print("\n✅ Extended agent with custom handlers ready!")
    print("Try saying: 'tell me a joke' or 'system info'\n")
    
    # Start the agent
    agent.start()


if __name__ == "__main__":
    main()

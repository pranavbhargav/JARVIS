"""
Example 3: Custom Commands
Add custom commands to extend JARVIS functionality
"""

from agent import VoiceAgent
from config import COMMANDS


def main():
    # Create agent
    agent = VoiceAgent(name="JARVIS", use_voice=False)
    
    # Add custom commands
    agent.add_custom_command(
        intent_name="joke",
        keywords=["tell joke", "make me laugh", "funny"],
        responses=["Why did the scarecrow win an award? Because he was outstanding in his field!"],
        action="tell_joke"
    )
    
    agent.add_custom_command(
        intent_name="system_info",
        keywords=["system info", "computer info", "about this computer"],
        responses=["Here's your system information"],
        action="get_system_info"
    )
    
    print("\n✅ Custom commands added!")
    print("Try saying: 'tell me a joke' or 'system info'\n")
    
    # Start the agent
    agent.start()


if __name__ == "__main__":
    main()

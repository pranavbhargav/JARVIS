"""
Example 1: Basic Voice Agent
Run JARVIS in voice mode with default settings
"""

from agent import VoiceAgent


def main():
    # Create agent with default settings
    agent = VoiceAgent(name="JARVIS", use_voice=True)
    
    # Start the agent
    agent.start()


if __name__ == "__main__":
    main()

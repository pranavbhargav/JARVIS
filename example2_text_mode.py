"""
Example 2: Text Mode Agent
Run JARVIS in text mode (useful for testing without microphone)
"""

from agent import VoiceAgent


def main():
    # Create agent in text mode
    agent = VoiceAgent(name="JARVIS", use_voice=False)
    
    # Start the agent
    agent.start()


if __name__ == "__main__":
    main()

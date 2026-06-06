"""
JARVIS Voice Agent - Main Agent
Main class that orchestrates the voice agent functionality
"""

from voice_io import VoiceInput, VoiceOutput
from nlp_engine import IntentRecognizer
from action_executor import ActionExecutor


class VoiceAgent:
    """Main voice agent class"""
    
    def __init__(self, name="JARVIS", use_voice=True):
        """
        Initialize the voice agent
        
        Args:
            name: Agent name
            use_voice: Whether to use voice I/O (True) or text I/O (False)
        """
        self.name = name
        self.use_voice = use_voice
        self.running = False
        
        # Initialize components
        self.voice_output = VoiceOutput()
        self.voice_input = VoiceInput() if use_voice else None
        
        # Auto-fallback to text mode if voice not available
        if use_voice and self.voice_input and not self.voice_input.voice_available:
            print("\n⚠️ Voice input not available. Switching to text mode.")
            self.use_voice = False
            self.voice_input = None
        
        self.intent_recognizer = IntentRecognizer()
        self.action_executor = ActionExecutor(self.voice_output)
        
        self._print_header()
    
    def _print_header(self):
        """Print agent header"""
        print("\n" + "="*50)
        print(f"🤖 {self.name} Voice Assistant Started")
        print("="*50)
        print(f"Mode: {'Voice' if self.use_voice else 'Text'}")
        print("Say a command or ask for help.")
        print("="*50 + "\n")

    def _show_help(self):
        """Show voice assistant help information"""
        help_text = (
            "I can help you with voice commands like telling the time, "
            "giving the date, checking the weather, setting reminders, "
            "opening applications, searching the web, or telling jokes."
        )
        print("\n🤖 Voice Assistant Help")
        print("I can help with:")
        print("  - time and date")
        print("  - weather updates")
        print("  - reminders")
        print("  - opening applications")
        print("  - web search")
        print("  - jokes and simple responses")
        print("  - exit when you're done")
        print()
        self.voice_output.speak(help_text)
    
    def start(self):
        """Start the voice agent"""
        self.running = True
        self.voice_output.speak(f"Hello! I'm {self.name}. How can I help?")
        
        while self.running:
            try:
                if self.use_voice:
                    user_input = self.voice_input.listen()
                else:
                    user_input = self._get_text_input()
                
                if user_input is None:
                    continue
                
                self._process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n⏹️ Stopping agent...")
                self.voice_output.speak("Goodbye!")
                self.running = False
            except Exception as e:
                print(f"❌ Error: {e}")
                self.voice_output.speak("An error occurred. Please try again.")
    
    def _get_text_input(self):
        """Get text input from user (for text mode)"""
        try:
            user_input = input("\n📝 You: ").strip()
            if not user_input:
                return None
            return user_input
        except EOFError:
            return "goodbye"
    
    def _process_input(self, user_input):
        """Process user input and execute the voice assistant response"""
        normalized = user_input.lower().strip()
        if normalized in ["help", "?", "what can you do", "list commands"]:
            self._show_help()
            return

        intent_name, confidence, entities = self.intent_recognizer.recognize_intent(user_input)
        if intent_name is None:
            print("⚠️ Intent not recognized")
            self.voice_output.speak("Sorry, I didn't understand that. Please try again.")
            return

        print(f"✅ Intent: {intent_name} (confidence: {confidence:.2f})")

        parameters = self.intent_recognizer.extract_parameters(user_input, intent_name)
        self.action_executor.execute(intent_name, parameters)

        if intent_name == "goodbye":
            self.running = False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="JARVIS Voice Agent")
    parser.add_argument(
        "--text-mode",
        action="store_true",
        help="Run in text mode instead of voice mode"
    )
    parser.add_argument(
        "--name",
        default="JARVIS",
        help="Agent name (default: JARVIS)"
    )
    
    args = parser.parse_args()
    
    # Create and start agent
    agent = VoiceAgent(name=args.name, use_voice=not args.text_mode)
    agent.start()


if __name__ == "__main__":
    main()

"""
JARVIS Voice Agent - Main Agent
Main class that orchestrates the voice agent functionality
"""

import logging
from typing import Optional, Dict, Any
from voice_io import VoiceInput, VoiceOutput
from nlp_engine import IntentRecognizer
from action_executor import ActionExecutor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceAgent:
    """Main voice agent class that orchestrates all components"""
    
    def __init__(self, name: str = "JARVIS", use_voice: bool = True):
        """
        Initialize the voice agent
        
        Args:
            name: Agent name
            use_voice: Whether to use voice I/O (True) or text I/O (False)
        """
        self.name = name
        self.use_voice = use_voice
        self.running = False
        self.conversation_history: list = []
        
        logger.info(f"Initializing {name} Voice Agent")
        
        # Initialize components
        self.voice_output = VoiceOutput()
        self.voice_input = VoiceInput() if use_voice else None
        
        # Auto-fallback to text mode if voice not available
        if use_voice and self.voice_input and not self.voice_input.voice_available:
            logger.warning("Voice input not available. Switching to text mode.")
            print("\n⚠️ Voice input not available. Switching to text mode.")
            self.use_voice = False
            self.voice_input = None
        
        self.intent_recognizer = IntentRecognizer()
        self.action_executor = ActionExecutor(self.voice_output)
        
        logger.info(f"Agent initialized in {'voice' if self.use_voice else 'text'} mode")
        self._print_header()
    
    def _print_header(self) -> None:
        """Print agent header"""
        print("\n" + "="*60)
        print(f"🤖 {self.name} Voice Assistant Started")
        print("="*60)
        print(f"Mode: {'Voice 🎤' if self.use_voice else 'Text 📝'}")
        print(f"Version: 2.0 | Status: Ready")
        print("Type 'help' for commands or speak naturally")
        print("="*60 + "\n")
    
    def _show_help(self) -> None:
        """Show voice assistant help information"""
        help_text = (
            "I can help you with voice commands like telling the time, "
            "giving the date, checking the weather, setting reminders, "
            "opening applications, searching the web, or telling jokes. "
            "You can also ask for help, show reminders, or exit."
        )
        print("\n" + "="*60)
        print("🤖 JARVIS Voice Assistant - Help")
        print("="*60)
        print("I can help with:")
        print("  ⏰ time and date")
        print("  🌤️  weather updates")
        print("  📋 reminders (set, show, clear)")
        print("  📱 opening applications")
        print("  🔍 web search")
        print("  😂 jokes and fun")
        print("  👋 exit when done")
        print("\nSpecial commands:")
        print("  help or ? - Show this help")
        print("  reminders - Show all reminders")
        print("  bye/goodbye - Exit gracefully")
        print("="*60 + "\n")
        self.voice_output.speak(help_text)
        logger.info("Help information displayed")
    
    def start(self) -> None:
        """Start the voice agent"""
        logger.info(f"Starting {self.name}")
        self.running = True
        self.voice_output.speak(f"Hello! I'm {self.name}. How can I help you today?")
        
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
                logger.info("Keyboard interrupt received")
                print("\n\n⏹️  Stopping agent...")
                self.voice_output.speak(f"Goodbye! It was nice talking to you.")
                self.running = False
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
                print(f"❌ Error: {e}")
                self.voice_output.speak("An error occurred. Please try again.")
    
    def _get_text_input(self) -> Optional[str]:
        """Get text input from user (for text mode)"""
        try:
            user_input = input("\n📝 You: ").strip()
            if not user_input:
                return None
            logger.debug(f"User input received: {user_input}")
            return user_input
        except EOFError:
            logger.info("EOF received - returning goodbye")
            return "goodbye"
        except Exception as e:
            logger.error(f"Error getting text input: {e}")
            return None
    
    def _process_input(self, user_input: str) -> None:
        """Process user input and execute the voice assistant response"""
        try:
            normalized = user_input.lower().strip()
            
            # Store in conversation history
            self.conversation_history.append({
                "type": "user",
                "content": user_input,
                "timestamp": self._get_timestamp()
            })
            
            # Handle special commands
            if normalized in ["help", "?", "what can you do", "list commands"]:
                self._show_help()
                return
            
            if normalized in ["reminders", "show reminders", "list reminders"]:
                self._show_reminders()
                return
            
            # Recognize intent
            logger.debug(f"Recognizing intent for: {user_input}")
            intent_name, confidence, entities = self.intent_recognizer.recognize_intent(user_input)
            
            if intent_name is None:
                logger.warning(f"Intent not recognized for: {user_input}")
                print("⚠️  Intent not recognized")
                self.voice_output.speak("Sorry, I didn't understand that. Could you please rephrase?")
                return
            
            logger.info(f"Intent recognized: {intent_name} (confidence: {confidence:.2f})")
            print(f"✅ Intent: {intent_name} (confidence: {confidence:.2f})")
            
            # Extract parameters
            parameters = self.intent_recognizer.extract_parameters(user_input, intent_name)
            logger.debug(f"Extracted parameters: {parameters}")
            
            # Execute action
            success = self.action_executor.execute(intent_name, parameters)
            
            if success:
                logger.info(f"Action executed successfully: {intent_name}")
            
            # Store response in history
            self.conversation_history.append({
                "type": "assistant",
                "intent": intent_name,
                "confidence": confidence,
                "timestamp": self._get_timestamp()
            })
            
            # Handle exit
            if intent_name == "goodbye":
                logger.info("Goodbye intent received - shutting down")
                self.running = False
        
        except Exception as e:
            logger.error(f"Error processing input: {e}", exc_info=True)
            print(f"❌ Error: {e}")
            self.voice_output.speak("An error occurred while processing your request.")
    
    def _show_reminders(self) -> None:
        """Show all reminders"""
        try:
            reminders = self.action_executor.get_reminders()
            if not reminders:
                self.voice_output.speak("You don't have any reminders set.")
                print("\n📋 No reminders set.")
                return
            
            print("\n" + "="*60)
            print("📋 Your Reminders")
            print("="*60)
            for reminder in reminders:
                print(f"  [{reminder.get('id')}] {reminder.get('text')}")
                print(f"      Created: {reminder.get('created_at')}")
            print("="*60)
            
            reminder_text = f"You have {len(reminders)} reminder(s) set."
            self.voice_output.speak(reminder_text)
            logger.info(f"Displayed {len(reminders)} reminders")
        except Exception as e:
            logger.error(f"Error showing reminders: {e}")
            self.voice_output.speak("Error retrieving reminders.")
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="JARVIS Voice Agent - Your intelligent voice assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent.py              # Run in voice mode
  python agent.py --text-mode  # Run in text mode
  python agent.py --name STELLA # Custom agent name
        """
    )
    
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
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging level"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(args.log_level)
    logger.info(f"Logging level set to {args.log_level}")
    
    # Create and start agent
    logger.info(f"Creating agent: {args.name}")
    agent = VoiceAgent(name=args.name, use_voice=not args.text_mode)
    agent.start()


if __name__ == "__main__":
    main()

# 🤖 JARVIS - Voice Agent with NLP

A sophisticated Python-based voice agent that understands natural language commands and executes actions accordingly. JARVIS combines speech recognition, natural language processing, and text-to-speech capabilities.

## Features

✨ **Voice Recognition** - Captures and transcribes voice commands (optional, with PyAudio)
🧠 **NLP Engine** - Intelligent intent recognition and parameter extraction
🎤 **Text-to-Speech** - Natural voice responses (optional, with espeak)
⚡ **Multi-intent Support** - Handles 8+ command categories
🎯 **Extensible Architecture** - Easy to add custom commands and actions
📋 **Reminder System** - Set and manage reminders
🌐 **Web Integration** - Search the web, get weather information
💬 **Text-Only Mode** - Works perfectly without microphone or audio hardware
🔄 **Graceful Degradation** - Auto-fallback to text mode when dependencies missing
☁️ **Cloud-Ready** - Runs in cloud environments without audio hardware

## Architecture

```
┌─────────────────────────────────────────────────────┐
│           JARVIS Voice Agent                        │
├─────────────────────────────────────────────────────┤
│  Input: Voice (Microphone) / Text (Console)         │
│     ↓                                                │
│  Voice I/O Layer (voice_io.py)                      │
│     ↓                                                │
│  NLP Engine (nlp_engine.py)                         │
│     ├─ Intent Recognition                           │
│     ├─ Entity Extraction                            │
│     └─ Parameter Extraction                         │
│     ↓                                                │
│  Action Executor (action_executor.py)               │
│     ├─ Time/Date                                    │
│     ├─ Weather Information                          │
│     ├─ Application Launcher                         │
│     ├─ Web Search                                   │
│     ├─ Reminders                                    │
│     └─ Custom Actions                               │
│     ↓                                                │
│  Output: Speech + Console Feedback                  │
└─────────────────────────────────────────────────────┘
```

## Project Structure

```
JARVIS/
├── agent.py                 # Main agent orchestrator
├── config.py                # Configuration and commands
├── nlp_engine.py           # NLP and intent recognition
├── voice_io.py             # Voice input/output handling
├── action_executor.py      # Action execution logic
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── example1_basic_voice.py # Basic voice mode example
├── example2_text_mode.py   # Text mode example
├── example3_custom_commands.py # Custom commands example
└── example4_advanced.py    # Advanced usage example
```

## Installation

### Prerequisites
- Python 3.7 or higher
- Microphone (for voice mode)
- Internet connection (for weather, web search, Google Speech Recognition)
- Optional: Text-to-speech libraries (for voice output)

### Setup

1. **Clone the repository**
   ```bash
   cd /workspaces/JARVIS
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install optional text-to-speech support** (for voice output)
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install espeak
   
   # Then install PyAudio
   pip install pyaudio
   ```

5. **Download NLP models** (optional for enhanced NLP)
   ```bash
   python -m nltk.downloader punkt
   ```

**Note**: The agent works in text-only mode even if text-to-speech or microphone is unavailable. This is useful for cloud environments and testing.

## Quick Start

For a comprehensive guide, see [QUICKSTART.md](QUICKSTART.md).

### Text Mode (Recommended for First Run)
```bash
python agent.py --text-mode
```
Perfect for testing without a microphone or audio hardware.

### Voice Mode (Auto-fallback to Text)
```bash
python agent.py
```
Attempts voice mode, automatically switches to text mode if microphone/PyAudio unavailable.

### Run Examples
```bash
# Text mode demo
python example2_text_mode.py

# With custom commands
python example3_custom_commands.py
```

## Supported Commands

### 1. **Greeting**
- Keywords: `hello`, `hi`, `hey`, `greetings`
- Examples:
  - "Hello"
  - "Hi there"

### 2. **Time**
- Keywords: `time`, `what time`, `current time`, `tell me time`
- Examples:
  - "What time is it?"
  - "Tell me the time"

### 3. **Date**
- Keywords: `date`, `what date`, `today`, `current date`
- Examples:
  - "What's today's date?"
  - "Tell me today"

### 4. **Weather**
- Keywords: `weather`, `how is weather`, `temperature`
- Examples:
  - "What's the weather?"
  - "Tell me the weather"

### 5. **Reminders**
- Keywords: `remind`, `set reminder`, `remember`
- Examples:
  - "Remind me to buy groceries"
  - "Set a reminder for the meeting"

### 6. **Open Application**
- Keywords: `open`, `launch`, `start`
- Examples:
  - "Open notepad"
  - "Launch Chrome"
  - Supported apps: notepad, calculator, chrome, firefox, vscode, spotify, vlc

### 7. **Web Search**
- Keywords: `search`, `find`, `look up`
- Examples:
  - "Search for Python tutorials"
  - "Find information about machine learning"

### 8. **Goodbye**
- Keywords: `bye`, `goodbye`, `exit`, `quit`
- Examples:
  - "Goodbye"
  - "Exit"

### Special Commands
- `help` or `?` - Show help information
- `reminders` - Show all reminders

## Usage Examples

### Example 1: Basic Voice Mode
```python
from agent import VoiceAgent

agent = VoiceAgent(name="JARVIS", use_voice=True)
agent.start()
```

### Example 2: Text Mode
```python
from agent import VoiceAgent

agent = VoiceAgent(name="JARVIS", use_voice=False)
agent.start()
```

### Example 3: Add Custom Commands
```python
from agent import VoiceAgent

agent = VoiceAgent(name="JARVIS", use_voice=False)

# Add custom command
agent.add_custom_command(
    intent_name="joke",
    keywords=["tell joke", "make me laugh"],
    responses=["Why did the chicken cross the road?"],
    action="tell_joke"
)

agent.start()
```

### Example 4: Custom Action Handlers
```python
from agent import VoiceAgent
from action_executor import ActionExecutor

class CustomExecutor(ActionExecutor):
    def execute(self, intent_name, parameters=None):
        if intent_name == "custom_action":
            print("Executing custom action!")
            return True
        return super().execute(intent_name, parameters)

agent = VoiceAgent(name="JARVIS", use_voice=False)
agent.action_executor = CustomExecutor(agent.voice_output)
agent.start()
```

## Configuration

Edit `config.py` to customize:

- **Commands**: Add or modify supported intents
- **Keywords**: Change trigger words
- **Responses**: Customize agent responses
- **Speech Recognition**: Adjust language, timeout, phrase limit
- **Text-to-Speech**: Modify speech rate and volume

Example:
```python
COMMANDS = {
    "greeting": {
        "keywords": ["hello", "hi", "hey"],
        "responses": ["Hello! I'm JARVIS."],
        "action": "respond"
    },
    # Add more commands...
}
```

## API Reference

### VoiceAgent

Main class orchestrating the voice agent.

```python
# Initialize
agent = VoiceAgent(name="JARVIS", use_voice=True)

# Start agent
agent.start()

# Add custom command
agent.add_custom_command(
    intent_name="name",
    keywords=["keyword1", "keyword2"],
    responses=["Response template"],
    action="action_name"
)
```

### IntentRecognizer

Handles NLP and intent recognition.

```python
recognizer = IntentRecognizer()

# Recognize intent
intent_name, confidence, entities = recognizer.recognize_intent("what time is it?")

# Extract parameters
params = recognizer.extract_parameters(user_text, intent_name)
```

### VoiceInput / VoiceOutput

Handle voice I/O operations.

```python
# Voice input
voice_input = VoiceInput()
text = voice_input.listen()
command = voice_input.listen_for_command("Say something:")

# Voice output
voice_output = VoiceOutput()
voice_output.speak("Hello!")
voice_output.set_voice_gender("female")
voice_output.set_speed(150)
```

### ActionExecutor

Executes recognized intents.

```python
executor = ActionExecutor(voice_output)

# Execute action
executor.execute("time")
executor.execute("search", {"query": "Python"})

# Get reminders
reminders = executor.get_reminders()
executor.clear_reminders()
```

## Advanced Features

### Extending with Custom Actions

Create your own action handlers by subclassing `ActionExecutor`:

```python
class MyExecutor(ActionExecutor):
    def execute(self, intent_name, parameters=None):
        if intent_name == "my_custom_action":
            # Your custom logic here
            self.voice_output.speak("Action executed!")
            return True
        return super().execute(intent_name, parameters)
```

### NLP Customization

Modify intent recognition by adjusting `nlp_engine.py`:

```python
# Adjust confidence threshold
CONFIDENCE_THRESHOLD = 0.6

# Add custom entity extraction
def _extract_custom_entities(self, text):
    # Your extraction logic
    pass
```

### Integration with Other Systems

JARVIS can be integrated with:
- Smart home systems (using action handlers)
- Chat applications (text-only mode)
- IoT devices (custom action executors)
- Databases (store reminders, logs)

## Troubleshooting

### "No module named 'speech_recognition'"
- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in the correct virtual environment if using one

### "libespeak.so.1: cannot open shared object file"
- Install espeak library: `sudo apt-get install espeak`
- The agent will run in text-only mode if unavailable
- This is expected in cloud environments without audio support

### "No microphone detected"
- Check if microphone is properly connected
- Test with text mode: `python agent.py --text-mode`
- Verify microphone permissions

### "Speech not recognized"
- Speak clearly and slowly
- Reduce background noise
- Check internet connection (for Google Speech Recognition)
- Increase `phrase_time_limit` in config.py

### "Action not executing"
- Check if application is installed
- Verify correct keywords in config.py
- Run with text-mode to test intent recognition

### "Import errors"
- Ensure all requirements are installed: `pip install -r requirements.txt`
- Use Python 3.7+
- Create virtual environment if needed

## Performance Tips

1. **Reduce latency**: Run in text mode for development
2. **Improve accuracy**: Speak clearly and use standard keywords
3. **Better responses**: Extend command keywords for more variations
4. **Custom intents**: Add domain-specific commands for better accuracy

## Future Enhancements

- 🤖 Machine learning model for improved intent recognition
- 🌍 Multi-language support
- 🔌 Plugin system for third-party integrations
- 📊 Analytics and usage statistics
- 🔐 User authentication
- ☁️ Cloud-based NLP backend
- 🎓 Context-aware conversations
- 📱 Mobile app interface

## Dependencies

- **SpeechRecognition**: Voice input capture
- **pyttsx3**: Text-to-speech
- **requests**: HTTP requests for weather/search
- **python-dotenv**: Environment configuration
- **spacy**: Advanced NLP (optional)
- **nltk**: Natural Language Toolkit (optional)

## Contributing

Feel free to extend JARVIS with:
- New commands and intents
- Better NLP algorithms
- Additional action handlers
- Improved voice quality
- Language support
- Test cases

## License

MIT License - Feel free to use for personal and commercial projects.

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review example files
3. Refer to inline code documentation
4. Create detailed issue reports

---

**Happy coding with JARVIS! 🚀**
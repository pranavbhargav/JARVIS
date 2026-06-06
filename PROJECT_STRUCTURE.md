# JARVIS Project Structure & Quick Reference

## 📁 Project Files Overview

### Core Application Files

| File | Purpose | Lines |
|------|---------|-------|
| `agent.py` | Main agent orchestrator | 200+ |
| `config.py` | Configuration and commands | 70+ |
| `nlp_engine.py` | NLP and intent recognition | 150+ |
| `voice_io.py` | Voice I/O handling | 130+ |
| `action_executor.py` | Action execution | 180+ |
| `utils.py` | Utility functions | 100+ |

### Example Files

| File | Purpose |
|------|---------|
| `example1_basic_voice.py` | Basic voice mode usage |
| `example2_text_mode.py` | Text mode for testing |
| `example3_custom_commands.py` | Adding custom commands |
| `example4_advanced.py` | Advanced custom handlers |

### Configuration & Setup

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `config.py` | Command configuration |
| `setup.py` | Installation wizard |

### Testing & Documentation

| File | Purpose |
|------|---------|
| `test_agent.py` | Unit tests |
| `README.md` | Main documentation |
| `DEVELOPER_GUIDE.md` | Developer documentation |
| `INTEGRATION_GUIDE.md` | Integration examples |
| `PROJECT_STRUCTURE.md` | This file |

## 🚀 Quick Start Commands

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run setup wizard
python setup.py
```

### Running Agent
```bash
# Text mode (recommended first)
python agent.py --text-mode

# Voice mode
python agent.py

# With custom name
python agent.py --text-mode --name "Assistant"
```

### Running Examples
```bash
python example1_basic_voice.py
python example2_text_mode.py
python example3_custom_commands.py
python example4_advanced.py
```

### Testing
```bash
python test_agent.py
```

## 🎯 Key Classes & Methods

### VoiceAgent
```python
agent = VoiceAgent(name="JARVIS", use_voice=True)
agent.start()
agent.add_custom_command(intent_name, keywords, responses, action)
```

### IntentRecognizer
```python
recognizer = IntentRecognizer()
intent, confidence, entities = recognizer.recognize_intent(text)
parameters = recognizer.extract_parameters(text, intent_name)
```

### VoiceInput / VoiceOutput
```python
voice_in = VoiceInput()
text = voice_in.listen()

voice_out = VoiceOutput()
voice_out.speak("Hello!")
voice_out.set_voice_gender("female")
voice_out.set_speed(150)
```

### ActionExecutor
```python
executor = ActionExecutor(voice_output)
executor.execute("time")
executor.get_reminders()
```

## 📋 Supported Commands

**Communication**
- greeting: hello, hi, hey
- goodbye: bye, goodbye, exit

**Information**
- time: what time, current time
- date: what date, today
- weather: weather, temperature
- search: search, find, look up

**Productivity**
- reminder: remind me, set reminder

**System**
- open_app: open, launch, start
  - Apps: chrome, firefox, vscode, notepad, calculator

## ⚙️ Configuration Guide

### Add Command to config.py
```python
COMMANDS["new_command"] = {
    "keywords": ["trigger1", "trigger2"],
    "responses": ["Response template {data}"],
    "action": "handler_name"
}
```

### Adjust Settings
```python
# Confidence threshold
CONFIDENCE_THRESHOLD = 0.5  # Higher = stricter

# Speech recognition
SPEECH_RECOGNITION = {
    "language": "en-US",
    "timeout": 10,
    "phrase_time_limit": 15
}

# Text-to-speech
TEXT_TO_SPEECH = {
    "rate": 150,
    "volume": 0.9
}
```

## 🧩 Extension Points

### Custom Commands
```python
agent.add_custom_command(
    intent_name="music",
    keywords=["play music"],
    responses=["Playing music"],
    action="play_music"
)
```

### Custom Action Handlers
```python
class CustomExecutor(ActionExecutor):
    def execute(self, intent_name, parameters=None):
        if intent_name == "custom":
            # Handle custom action
            return True
        return super().execute(intent_name, parameters)
```

### Custom Intent Recognition
```python
class CustomRecognizer(IntentRecognizer):
    def _calculate_intent_confidence(self, text, keywords):
        # Your custom matching logic
        pass
```

## 📊 Data Flow

```
User Input (Voice/Text)
    ↓
Voice Input Module (transcription if voice)
    ↓
NLP Engine (intent recognition)
    ↓
Intent Recognized → Parameters Extracted
    ↓
Action Executor (execute action)
    ↓
Voice Output Module
    ↓
User Output (speech/text)
```

## 🔧 Troubleshooting Quick Guide

| Issue | Solution |
|-------|----------|
| Microphone not detected | Use text mode: `--text-mode` |
| Speech not recognized | Speak slowly, reduce noise, check internet |
| Command not executing | Verify keywords in config.py |
| Import errors | Run: `pip install -r requirements.txt` |
| Confidence too low | Lower CONFIDENCE_THRESHOLD in config.py |

## 📚 Documentation Quick Links

- **README.md** - Full user documentation
- **DEVELOPER_GUIDE.md** - Development guide
- **INTEGRATION_GUIDE.md** - Integration examples
- **Code Comments** - Inline documentation

## 🎓 Learning Path

1. **Beginner**: Run `example2_text_mode.py`
2. **Intermediate**: Read README.md, try `example3_custom_commands.py`
3. **Advanced**: Study DEVELOPER_GUIDE.md, create custom executors
4. **Integration**: Check INTEGRATION_GUIDE.md for advanced patterns

## 📦 Dependencies

- **SpeechRecognition** - Voice input
- **pyttsx3** - Text-to-speech
- **spacy** - Advanced NLP (optional)
- **nltk** - NLP toolkit (optional)
- **requests** - HTTP requests
- **python-dotenv** - Environment config

## 🔐 Best Practices

1. **Error Handling**: Always wrap external calls in try-except
2. **User Feedback**: Always acknowledge commands
3. **Testing**: Write tests for new intents
4. **Documentation**: Document custom commands
5. **Performance**: Cache expensive operations

## 📈 Performance Metrics

- Average intent recognition: ~100ms
- Voice input latency: ~1-2s (depends on network)
- Text-to-speech latency: ~500ms-1s

## 🐛 Debug Mode

Add logging to agent:
```python
from utils import Logger

logger = Logger("debug.log")
logger.log_intent(user_input, intent_name, confidence)
```

## 🚀 Production Deployment

1. Use text mode for web services
2. Implement error recovery
3. Add comprehensive logging
4. Set up monitoring
5. Consider using async operations

---

**Quick Help**: `python agent.py --help`

**For detailed help**: See README.md or DEVELOPER_GUIDE.md

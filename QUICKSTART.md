# JARVIS Quick Start Guide

## 🚀 Getting Started

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Optional: Install text-to-speech support
sudo apt-get install espeak  # Ubuntu/Debian
pip install pyaudio
```

### Running JARVIS

#### Option 1: Text Mode (Recommended for Testing)
```bash
python agent.py --text-mode
```

#### Option 2: Voice Mode (Auto-fallback to Text if Unavailable)
```bash
python agent.py
```
*Note: If microphone/PyAudio not available, automatically switches to text mode*

#### Option 3: With Custom Name
```bash
python agent.py --text-mode --name "Assistant"
python agent.py --name "MyBot"
```

## 📋 Available Commands

### Communication
- **Greeting**: "Hello", "Hi", "Hey" 👋
- **Goodbye**: "Bye", "Goodbye", "Exit", "Quit" 👋

### Information
- **Time**: "What time is it?", "Tell me the time" ⏰
- **Date**: "What's the date?", "Today's date" 📅
- **Weather**: "What's the weather?", "Temperature" 🌤️
- **Search**: "Search for Python", "Find Python tutorials" 🔍

### Productivity
- **Reminders**: "Remind me to buy groceries", "Set reminder" 📝

### System
- **Open Apps**: "Open Chrome", "Launch Notepad", "Start VS Code" 💻
  - Supported: chrome, firefox, vscode, notepad, calculator, spotify, vlc

### Special Commands
- **Help**: Type "help" or "?" for help 📖
- **Reminders**: Type "reminders" to see all reminders 📋

## 🎯 Quick Examples

```bash
# Run in text mode
python agent.py --text-mode

# You can then type:
# >>> hello
# JARVIS: Hi there! What do you need?

# >>> what time is it
# JARVIS: The current time is 02:44 PM

# >>> search for python tutorials
# JARVIS: Searching for python tutorials

# >>> goodbye
# JARVIS: See you later!
```

## 🔧 Configuration

Edit `config.py` to customize:
- Command keywords
- Agent responses
- Speech settings
- Confidence threshold

Example:
```python
COMMANDS["greeting"] = {
    "keywords": ["hello", "hi", "hey"],
    "responses": ["Hello! I'm JARVIS."],
    "action": "respond"
}
```

## 📚 Learn More

- **README.md** - Full documentation
- **DEVELOPER_GUIDE.md** - Development guide
- **INTEGRATION_GUIDE.md** - Integration examples
- **example*.py** - Example scripts

## ⚠️ Troubleshooting

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Text-to-Speech Not Working
```bash
# Ubuntu/Debian
sudo apt-get install espeak

# Then install PyAudio
pip install pyaudio
```

### Voice Input Not Working
- Ensure microphone is connected
- Install PyAudio: `pip install pyaudio`
- Try text mode: `python agent.py --text-mode`

### Command Not Recognized
- Check keywords in `config.py`
- Try saying command more clearly
- Use text mode to verify keywords

## 🚀 Next Steps

1. **Try text mode**: `python agent.py --text-mode`
2. **Explore examples**: `python example2_text_mode.py`
3. **Add custom commands**: See DEVELOPER_GUIDE.md
4. **Integrate with other apps**: See INTEGRATION_GUIDE.md

---

**Happy coding! 🎉**

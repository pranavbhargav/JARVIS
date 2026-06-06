# Developer Guide - JARVIS Voice Agent

## Table of Contents
1. [Architecture](#architecture)
2. [Module Overview](#module-overview)
3. [Creating Custom Commands](#creating-custom-commands)
4. [Creating Custom Actions](#creating-custom-actions)
5. [NLP Customization](#nlp-customization)
6. [Testing](#testing)
7. [Best Practices](#best-practices)

## Architecture

JARVIS follows a modular, layered architecture:

```
┌─────────────────────────────────────────┐
│       Agent (agent.py)                   │
│    - Orchestrates components              │
│    - Manages main loop                    │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
VoiceI/O   NLP Engine  Action Executor
(voice_io) (nlp_engine) (action_executor)
```

## Module Overview

### agent.py - Main Agent
The orchestrator that ties everything together.

**Key Classes:**
- `VoiceAgent`: Main agent class

**Key Methods:**
- `start()`: Start the agent loop
- `_process_input()`: Process user input
- `add_custom_command()`: Register custom commands

### config.py - Configuration
Centralized configuration for all intents and settings.

**Key Elements:**
- `COMMANDS`: Dict of all supported intents
- `CONFIDENCE_THRESHOLD`: Minimum confidence for intent matching
- `SPEECH_RECOGNITION`: Speech settings
- `TEXT_TO_SPEECH`: Voice settings

### nlp_engine.py - NLP & Intent Recognition
Handles natural language processing and intent recognition.

**Key Classes:**
- `IntentRecognizer`: Recognizes intents from text

**Key Methods:**
- `recognize_intent()`: Main intent recognition
- `extract_entities()`: Extract entities from text
- `extract_parameters()`: Extract specific parameters

### voice_io.py - Voice I/O
Handles microphone input and speaker output.

**Key Classes:**
- `VoiceInput`: Captures voice input
- `VoiceOutput`: Produces voice output

**Key Methods:**
- `VoiceInput.listen()`: Listen and transcribe
- `VoiceOutput.speak()`: Speak text

### action_executor.py - Action Execution
Executes actions based on recognized intents.

**Key Classes:**
- `ActionExecutor`: Executes intents

**Key Methods:**
- `execute()`: Main execution method
- Individual handlers: `_handle_get_time()`, etc.

### utils.py - Utilities
Helper functions and utilities.

**Key Classes:**
- `Logger`: Simple logging
- `ConfigManager`: Config management
- `CommandRegistry`: Custom command registry

## Creating Custom Commands

### Method 1: Using add_custom_command()

```python
from agent import VoiceAgent

agent = VoiceAgent(use_voice=False)

agent.add_custom_command(
    intent_name="music",
    keywords=["play music", "start music", "play song"],
    responses=["Playing music for you"],
    action="play_music"
)

agent.start()
```

### Method 2: Direct Configuration

Edit `config.py` and add to `COMMANDS`:

```python
COMMANDS = {
    # ... existing commands ...
    "music": {
        "keywords": ["play music", "start music"],
        "responses": ["Playing music"],
        "action": "play_music"
    }
}
```

### Method 3: Programmatic Addition

```python
from config import COMMANDS

COMMANDS["music"] = {
    "keywords": ["play music", "start music"],
    "responses": ["Playing music"],
    "action": "play_music"
}
```

## Creating Custom Actions

### Basic Custom Action Handler

```python
from agent import VoiceAgent
from action_executor import ActionExecutor
from voice_io import VoiceOutput

class MyActionExecutor(ActionExecutor):
    def execute(self, intent_name, parameters=None):
        # Handle custom intents
        if intent_name == "music":
            self._handle_music(parameters)
            return True
        
        # Fall back to parent
        return super().execute(intent_name, parameters)
    
    def _handle_music(self, parameters):
        song = parameters.get("song", "default song") if parameters else "default song"
        self.voice_output.speak(f"Now playing {song}")
        # Your music playing logic here

# Use custom executor
agent = VoiceAgent(use_voice=False)
agent.action_executor = MyActionExecutor(agent.voice_output)
agent.start()
```

### Advanced: Action Handler with Parameters

```python
class AdvancedExecutor(ActionExecutor):
    def execute(self, intent_name, parameters=None):
        if intent_name == "weather":
            city = parameters.get("city", "current location") if parameters else "current location"
            self._get_weather_for_city(city)
            return True
        
        return super().execute(intent_name, parameters)
    
    def _get_weather_for_city(self, city):
        # Fetch weather for specific city
        import requests
        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url)
            weather = response.text.strip()
            self.voice_output.speak(f"Weather in {city}: {weather}")
        except Exception as e:
            self.voice_output.speak(f"Couldn't get weather for {city}")
```

## NLP Customization

### Adjusting Intent Recognition

Modify `nlp_engine.py`:

```python
# Increase confidence requirement
CONFIDENCE_THRESHOLD = 0.7  # Higher = stricter matching

# Customize similarity calculation
def _calculate_intent_confidence(self, text, keywords):
    # Your custom logic here
    pass
```

### Adding Custom Entity Extraction

```python
from nlp_engine import IntentRecognizer

class CustomRecognizer(IntentRecognizer):
    def extract_entities(self, text):
        entities = super().extract_entities(text)
        
        # Add custom entity extraction
        entities["custom_entity"] = self._extract_custom(text)
        
        return entities
    
    def _extract_custom(self, text):
        # Your extraction logic
        return []
```

### Improving Intent Matching

```python
# Use more sophisticated matching (e.g., with spaCy)
import spacy

nlp = spacy.load("en_core_web_sm")

def advanced_intent_matching(self, text):
    doc = nlp(text)
    
    # Use NER, dependency parsing, etc.
    for token in doc:
        print(token.text, token.pos_, token.dep_)
```

## Testing

### Run Test Suite

```bash
python test_agent.py
```

### Write Custom Tests

```python
import unittest
from nlp_engine import IntentRecognizer

class TestCustomIntent(unittest.TestCase):
    def setUp(self):
        self.recognizer = IntentRecognizer()
    
    def test_custom_intent(self):
        intent, conf, _ = self.recognizer.recognize_intent("your test input")
        self.assertEqual(intent, "expected_intent")
        self.assertGreater(conf, 0.5)

if __name__ == "__main__":
    unittest.main()
```

### Unit Testing Components

```python
# Test intent recognizer
recognizer = IntentRecognizer()
intent, conf, entities = recognizer.recognize_intent("hello")
print(f"Intent: {intent}, Confidence: {conf}")

# Test voice output
from voice_io import VoiceOutput
voice = VoiceOutput()
voice.speak("Testing text-to-speech")

# Test action executor
from action_executor import ActionExecutor
executor = ActionExecutor(voice)
executor.execute("time")
```

## Best Practices

### 1. **Command Design**
- Use clear, natural keywords
- Include variations of keywords
- Keep keywords short (1-3 words typically)

```python
# Good
"keywords": ["play music", "start music", "play song", "music"]

# Avoid
"keywords": ["please play some music if you don't mind"]
```

### 2. **Response Templates**
- Use templates with placeholders
- Keep responses natural
- Add variety with multiple responses

```python
# Good
"responses": [
    "Playing {data}",
    "Now playing {data}",
    "Started {data} for you"
]

# Avoid
"responses": ["OK"]
```

### 3. **Error Handling**
- Always wrap external calls in try-except
- Provide user-friendly error messages
- Log errors for debugging

```python
try:
    # External API call
    result = some_api_call()
except Exception as e:
    self.voice_output.speak("Couldn't complete that action")
    print(f"Error: {e}")  # Log for debugging
```

### 4. **Parameter Extraction**
- Always check if parameters exist
- Provide defaults
- Validate parameter values

```python
def extract_parameters(self, text, intent_name):
    params = {}
    
    # Safe parameter extraction
    param_value = self._extract_value(text)
    if param_value:
        params["key"] = param_value
    else:
        params["key"] = "default_value"
    
    return params
```

### 5. **Extensibility**
- Design for easy extension
- Use inheritance and composition
- Document extension points

```python
# Good - Easy to extend
class ActionExecutor:
    def execute(self, intent_name, parameters=None):
        if intent_name in self.custom_handlers:
            return self.custom_handlers[intent_name](parameters)
        return self._default_execute(intent_name, parameters)

# Register custom handler
executor.custom_handlers["custom"] = my_handler
```

### 6. **Performance**
- Cache expensive operations
- Use async for long operations
- Optimize NLP matching

```python
# Cache command loading
self._command_cache = COMMANDS

# Async operation
async def long_operation():
    # Time-consuming task
    pass
```

### 7. **Documentation**
- Document custom commands
- Add docstrings to classes/methods
- Provide usage examples

```python
def my_custom_command(self, parameters):
    """
    Execute custom command.
    
    Args:
        parameters: Dict with 'param1' and 'param2'
    
    Returns:
        Boolean indicating success
    """
    pass
```

## Integration Examples

### Integration with Database

```python
class DatabaseExecutor(ActionExecutor):
    def __init__(self, voice_output, db_connection):
        super().__init__(voice_output)
        self.db = db_connection
    
    def _handle_set_reminder(self, intent_config, parameters):
        reminder_text = parameters.get("reminder_text")
        self.db.save_reminder(reminder_text)
        # Continue with parent implementation
        super()._handle_set_reminder(intent_config, parameters)
```

### Integration with Web API

```python
import requests

class APIExecutor(ActionExecutor):
    def _handle_custom_api_call(self, parameters):
        query = parameters.get("query")
        
        response = requests.post(
            "https://api.example.com/endpoint",
            json={"query": query}
        )
        
        result = response.json()
        self.voice_output.speak(result.get("message"))
```

---

For more examples, see the example files in the project root.

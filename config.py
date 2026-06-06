"""
JARVIS Voice Agent - Configuration
Defines all commands and intents the agent can understand
"""

COMMANDS = {
    "greeting": {
        "keywords": [
            "hello",
            "hi",
            "hey",
            "greetings",
            "how are you",
            "how are you doing",
            "what's up",
            "whats up"
        ],
        "responses": [
            "Hello! I'm JARVIS. How can I assist you?",
            "Hi there! What would you like to talk about?",
            "Hey! I'm here to help."
        ],
        "action": "respond"
    },
    "thanks": {
        "keywords": ["thank you", "thanks", "thanks a lot", "thank you so much"],
        "responses": [
            "You're welcome!",
            "Glad I could help.",
            "Anytime!"
        ],
        "action": "respond"
    },
    "joke": {
        "keywords": ["tell me a joke", "joke", "make me laugh", "say something funny"],
        "responses": ["Sure, here's one:"],
        "action": "tell_joke"
    },
    "time": {
        "keywords": ["time", "what time", "current time", "tell me time"],
        "responses": ["The current time is {data}"],
        "action": "get_time"
    },
    "weather": {
        "keywords": ["weather", "how is weather", "temperature"],
        "responses": ["The weather information is {data}"],
        "action": "get_weather"
    },
    "date": {
        "keywords": ["date", "what date", "today", "current date"],
        "responses": ["Today's date is {data}"],
        "action": "get_date"
    },
    "reminder": {
        "keywords": ["remind", "set reminder", "remember", "reminder", "show reminders"],
        "responses": ["Reminder set: {data}"],
        "action": "set_reminder"
    },
    "open_app": {
        "keywords": ["open", "launch", "start"],
        "responses": ["Opening {data}."],
        "action": "open_application"
    },
    "search": {
        "keywords": ["search", "find", "look up", "look for"],
        "responses": ["Searching for {data}."],
        "action": "search_web"
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "exit", "quit", "see you", "talk later"],
        "responses": [
            "Goodbye! Have a great day!",
            "See you later!",
            "Bye! Take care!"
        ],
        "action": "exit"
    }
}

# Confidence threshold for intent matching
CONFIDENCE_THRESHOLD = 0.75

# Speech recognition settings
SPEECH_RECOGNITION = {
    "language": "en-US",
    "timeout": 10,
    "phrase_time_limit": 15
}

# Text-to-speech settings
TEXT_TO_SPEECH = {
    "rate": 150,
    "volume": 0.9
}

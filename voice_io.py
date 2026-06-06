"""
JARVIS Voice Agent - Voice I/O Module
Handles speech recognition and text-to-speech
"""

import speech_recognition as sr
import pyttsx3
from config import SPEECH_RECOGNITION, TEXT_TO_SPEECH

class VoiceInput:
    """Captures voice input from microphone"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.voice_available = False
        try:
            self.microphone = sr.Microphone()
            self.voice_available = True
        except Exception as e:
            print(f"⚠️ Microphone not available: {e}")
            print("   Running in text-only mode. Install PyAudio: pip install pyaudio")
            self.voice_available = False
    
    def listen(self):
        """
        Listen for voice input from microphone
        Returns: transcribed text or None if error
        """
        if not self.voice_available or self.microphone is None:
            print("❌ Microphone not available. Use text mode or install PyAudio")
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                audio = self.recognizer.listen(
                    source,
                    timeout=SPEECH_RECOGNITION["timeout"],
                    phrase_time_limit=SPEECH_RECOGNITION["phrase_time_limit"]
                )
            
            print("⏳ Processing audio...")
            text = self.recognizer.recognize_google(
                audio,
                language=SPEECH_RECOGNITION["language"]
            )
            print(f"📝 You said: {text}")
            return text
            
        except sr.UnknownValueError:
            print("❌ Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def listen_for_command(self, prompt=""):
        """Listen for voice command with optional prompt"""
        if not self.voice_available:
            if prompt:
                print(f"\n{prompt}")
            return self._get_fallback_input()
        
        if prompt:
            print(f"\n{prompt}")
        return self.listen()
    
    def _get_fallback_input(self):
        """Get text input when voice is unavailable"""
        try:
            return input("📝 You: ").strip() or None
        except EOFError:
            return None


class VoiceOutput:
    """Handles text-to-speech output"""
    
    def __init__(self):
        self.engine = None
        self.tts_available = False
        try:
            self.engine = pyttsx3.init()
            self._configure_engine()
            self.tts_available = True
        except Exception as e:
            print(f"⚠️ Text-to-speech not available: {e}")
            print("   Running in text-only mode. Install espeak: sudo apt-get install espeak")
            self.tts_available = False
    
    def _configure_engine(self):
        """Configure text-to-speech engine"""
        self.engine.setProperty('rate', TEXT_TO_SPEECH['rate'])
        self.engine.setProperty('volume', TEXT_TO_SPEECH['volume'])
        
        # Set voice (optional: you can select male/female voice)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text):
        """Speak text using text-to-speech"""
        print(f"🗣️ JARVIS: {text}")
        if not self.tts_available or self.engine is None:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
    
    def speak_async(self, text):
        """Speak text asynchronously (non-blocking)"""
        print(f"🗣️ JARVIS: {text}")
        if not self.tts_available or self.engine is None:
            return
        try:
            self.engine.say(text)
            # Don't wait for completion in async mode
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
    
    def set_voice_gender(self, gender="male"):
        """Set voice gender (male/female)"""
        if not self.tts_available or self.engine is None:
            return
        voices = self.engine.getProperty('voices')
        if voices:
            voice_index = 0 if gender.lower() == "male" else 1 if len(voices) > 1 else 0
            self.engine.setProperty('voice', voices[voice_index].id)
    
    def set_speed(self, rate):
        """Set speech rate"""
        if not self.tts_available or self.engine is None:
            return
        self.engine.setProperty('rate', rate)

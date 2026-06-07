"""
JARVIS Voice Agent - Voice I/O Module
Handles speech recognition and text-to-speech
"""

import logging
from typing import Optional

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    sr = None

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    pyttsx3 = None

from config import SPEECH_RECOGNITION, TEXT_TO_SPEECH

# Setup logging
logger = logging.getLogger(__name__)


class VoiceInput:
    """Captures voice input from microphone with error handling"""
    
    def __init__(self):
        """Initialize voice input"""
        self.recognizer = None
        self.microphone = None
        self.voice_available = False
        
        if not SR_AVAILABLE:
            logger.warning("SpeechRecognition module not available")
            print("⚠️  Install speech_recognition: pip install SpeechRecognition")
            return
        
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.voice_available = True
            logger.info("Voice input initialized successfully")
        except Exception as e:
            logger.error(f"Microphone initialization failed: {e}")
            print(f"⚠️  Microphone not available: {e}")
            print("   Install PyAudio: pip install pyaudio")
            self.voice_available = False
    
    def listen(self, timeout: Optional[int] = None) -> Optional[str]:
        """
        Listen for voice input from microphone
        
        Args:
            timeout: Custom timeout in seconds
            
        Returns:
            Transcribed text or None if error
        """
        if not self.voice_available or self.microphone is None:
            logger.error("Microphone not available")
            print("❌ Microphone not available. Use text mode.")
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                logger.debug("Adjusting for ambient noise")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                timeout_val = timeout or SPEECH_RECOGNITION["timeout"]
                phrase_limit = SPEECH_RECOGNITION["phrase_time_limit"]
                
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout_val,
                    phrase_time_limit=phrase_limit
                )
            
            print("⏳ Processing audio...")
            logger.debug("Recognizing speech with Google API")
            
            text = self.recognizer.recognize_google(
                audio,
                language=SPEECH_RECOGNITION["language"]
            )
            
            logger.info(f"Speech recognized: {text}")
            print(f"📝 You said: {text}")
            return text
        
        except sr.UnknownValueError:
            logger.warning("Speech not understood")
            print("❌ Sorry, I didn't catch that. Could you repeat?")
            return None
        
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            print(f"❌ Speech recognition error: {e}")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected error during listening: {e}", exc_info=True)
            print(f"❌ Error: {e}")
            return None
    
    def listen_for_command(self, prompt: str = "") -> Optional[str]:
        """Listen for voice command with optional prompt"""
        if prompt:
            print(f"\n{prompt}")
        
        if not self.voice_available:
            logger.debug("Using text fallback")
            return self._get_fallback_input()
        
        return self.listen()
    
    @staticmethod
    def _get_fallback_input() -> Optional[str]:
        """Get text input when voice is unavailable"""
        try:
            return input("📝 You: ").strip() or None
        except EOFError:
            return None


class VoiceOutput:
    """Handles text-to-speech output with error handling"""
    
    def __init__(self):
        """Initialize text-to-speech engine"""
        self.engine = None
        self.tts_available = False
        
        if not TTS_AVAILABLE:
            logger.warning("pyttsx3 module not available")
            print("⚠️  Install pyttsx3: pip install pyttsx3")
            return
        
        try:
            self.engine = pyttsx3.init()
            self._configure_engine()
            self.tts_available = True
            logger.info("Text-to-speech initialized successfully")
        except Exception as e:
            logger.error(f"TTS initialization failed: {e}")
            print(f"⚠️  Text-to-speech not available: {e}")
            print("   Install espeak (Linux): sudo apt-get install espeak")
            print("   Install espeak (Mac): brew install espeak")
            self.tts_available = False
    
    def _configure_engine(self) -> None:
        """Configure text-to-speech engine"""
        try:
            self.engine.setProperty('rate', TEXT_TO_SPEECH['rate'])
            self.engine.setProperty('volume', TEXT_TO_SPEECH['volume'])
            
            # Set voice
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
                logger.debug(f"TTS configured with voice: {voices[0].name}")
        except Exception as e:
            logger.error(f"Error configuring TTS engine: {e}")
    
    def speak(self, text: str) -> None:
        """
        Speak text using text-to-speech
        
        Args:
            text: Text to speak
        """
        try:
            print(f"🗣️  JARVIS: {text}")
            logger.debug(f"Speaking: {text}")
            
            if not self.tts_available or self.engine is None:
                logger.debug("TTS not available, output to console only")
                return
            
            self.engine.say(text)
            self.engine.runAndWait()
        
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            print(f"❌ TTS error: {e}")
    
    def speak_async(self, text: str) -> None:
        """
        Speak text asynchronously (non-blocking)
        
        Args:
            text: Text to speak
        """
        try:
            print(f"🗣️  JARVIS: {text}")
            logger.debug(f"Speaking (async): {text}")
            
            if not self.tts_available or self.engine is None:
                return
            
            self.engine.say(text)
            # Don't wait for completion in async mode
        
        except Exception as e:
            logger.error(f"Async TTS error: {e}")
    
    def set_voice_gender(self, gender: str = "male") -> None:
        """
        Set voice gender (male/female)
        
        Args:
            gender: 'male' or 'female'
        """
        if not self.tts_available or self.engine is None:
            return
        
        try:
            voices = self.engine.getProperty('voices')
            if voices:
                voice_index = 0 if gender.lower() == "male" else (
                    1 if len(voices) > 1 else 0
                )
                self.engine.setProperty('voice', voices[voice_index].id)
                logger.info(f"Voice gender set to: {gender}")
        except Exception as e:
            logger.error(f"Error setting voice gender: {e}")
    
    def set_speed(self, rate: int) -> None:
        """
        Set speech rate
        
        Args:
            rate: Speech rate (typically 50-300)
        """
        if not self.tts_available or self.engine is None:
            return
        
        try:
            self.engine.setProperty('rate', rate)
            logger.info(f"Speech rate set to: {rate}")
        except Exception as e:
            logger.error(f"Error setting speech rate: {e}")
    
    def set_volume(self, volume: float) -> None:
        """
        Set volume level
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if not self.tts_available or self.engine is None:
            return
        
        try:
            if 0.0 <= volume <= 1.0:
                self.engine.setProperty('volume', volume)
                logger.info(f"Volume set to: {volume}")
            else:
                logger.warning(f"Invalid volume: {volume}. Must be 0.0 to 1.0")
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
    
    def is_available(self) -> bool:
        """Check if TTS is available"""
        return self.tts_available

#!/usr/bin/env python3
"""
JARVIS Setup Script
Helps with initial setup and configuration
"""

import os
import sys
import subprocess


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required!")
        return False
    
    print("✅ Python version OK")
    return True


def install_requirements():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def download_spacy_models():
    """Download spaCy language models"""
    print_header("Optional: Download spaCy Models")
    
    response = input("Download spaCy English model? (y/n): ").strip().lower()
    
    if response == 'y':
        try:
            subprocess.check_call(
                [sys.executable, "-m", "spacy", "download", "en_core_web_sm"]
            )
            print("✅ spaCy model downloaded")
            return True
        except subprocess.CalledProcessError:
            print("⚠️ Failed to download spaCy model (optional)")
            return False
    
    return True


def download_nltk_data():
    """Download NLTK data"""
    print_header("Optional: Download NLTK Data")
    
    response = input("Download NLTK data? (y/n): ").strip().lower()
    
    if response == 'y':
        try:
            import nltk
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
            print("✅ NLTK data downloaded")
            return True
        except Exception as e:
            print(f"⚠️ Failed to download NLTK data (optional): {e}")
            return False
    
    return True


def test_microphone():
    """Test microphone"""
    print_header("Optional: Test Microphone")
    
    response = input("Test microphone? (y/n): ").strip().lower()
    
    if response == 'y':
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("🎤 Listening for 5 seconds...")
                audio = recognizer.listen(source, timeout=5)
            
            print("📝 Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"✅ Microphone works! Heard: {text}")
            return True
        except sr.UnknownValueError:
            print("⚠️ Microphone works, but speech not recognized")
            return True
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            return False
    
    return True


def test_text_to_speech():
    """Test text-to-speech"""
    print_header("Optional: Test Text-to-Speech")
    
    response = input("Test text-to-speech? (y/n): ").strip().lower()
    
    if response == 'y':
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            engine.say("Hello! JARVIS is ready.")
            engine.runAndWait()
            
            print("✅ Text-to-speech works!")
            return True
        except Exception as e:
            print(f"❌ Text-to-speech test failed: {e}")
            return False
    
    return True


def create_config_backup():
    """Create backup of config"""
    print_header("Creating Config Backup")
    
    if os.path.exists("config.py"):
        try:
            with open("config.py", "r") as f:
                content = f.read()
            
            with open("config.py.backup", "w") as f:
                f.write(content)
            
            print("✅ Config backup created: config.py.backup")
            return True
        except Exception as e:
            print(f"⚠️ Failed to create backup: {e}")
            return False
    
    return True


def show_quick_start():
    """Show quick start guide"""
    print_header("Quick Start Guide")
    
    print("""
1. Start in Text Mode (recommended for first run):
   python agent.py --text-mode
   
2. Try these commands:
   - "Hello" or "Hi"
   - "What time is it?"
   - "What's the weather?"
   - "Open notepad"
   - "Search for Python"
   
3. View examples:
   - example1_basic_voice.py - Basic voice mode
   - example2_text_mode.py - Text mode
   - example3_custom_commands.py - Custom commands
   - example4_advanced.py - Advanced features

4. View documentation:
   - README.md - Full documentation
   - config.py - Configuration options
   - Code comments - Implementation details
    """)


def main():
    """Run setup"""
    print("""
╔══════════════════════════════════════════════════════╗
║        🤖 JARVIS Voice Agent - Setup Wizard          ║
╚══════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        print("\n⚠️ Setup incomplete. Please install requirements manually:")
        print("   pip install -r requirements.txt")
        return False
    
    # Optional installations
    download_spacy_models()
    download_nltk_data()
    
    # Optional tests
    test_microphone()
    test_text_to_speech()
    
    # Create backup
    create_config_backup()
    
    # Show quick start
    show_quick_start()
    
    print_header("Setup Complete!")
    print("✅ JARVIS is ready to use!")
    print("\nRun: python agent.py --text-mode")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

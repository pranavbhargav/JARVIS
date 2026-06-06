"""
Integration Guide - Using JARVIS as a Library
Shows how to integrate JARVIS into other Python applications
"""

# Example 1: Basic Integration
def example_basic_integration():
    """Simple integration example"""
    from agent import VoiceAgent
    
    # Create agent
    agent = VoiceAgent(name="Assistant", use_voice=False)
    
    # Programmatically process input
    agent._process_input("what time is it")


# Example 2: Custom Integration with Text Processing
def example_text_processing():
    """Process specific text inputs"""
    from nlp_engine import IntentRecognizer
    
    recognizer = IntentRecognizer()
    
    # Process batch of inputs
    inputs = [
        "Hello",
        "What's the weather?",
        "Search for Python",
        "Goodbye"
    ]
    
    for user_input in inputs:
        intent, confidence, entities = recognizer.recognize_intent(user_input)
        print(f"Input: {user_input}")
        print(f"Intent: {intent} ({confidence:.2f})")
        print(f"Entities: {entities}\n")


# Example 3: Voice-Only Processing
def example_voice_processing():
    """Process only voice input/output"""
    from voice_io import VoiceInput, VoiceOutput
    from nlp_engine import IntentRecognizer
    
    voice_in = VoiceInput()
    voice_out = VoiceOutput()
    recognizer = IntentRecognizer()
    
    # Listen and process
    text = voice_in.listen()
    if text:
        intent, conf, _ = recognizer.recognize_intent(text)
        
        if intent:
            voice_out.speak(f"I recognized the intent: {intent}")
        else:
            voice_out.speak("I didn't understand that")


# Example 4: Custom Action Executor
def example_custom_executor():
    """Create custom executor for specific domain"""
    from action_executor import ActionExecutor
    from voice_io import VoiceOutput
    
    class MedicalAssistant(ActionExecutor):
        """Medical assistant executor"""
        
        def execute(self, intent_name, parameters=None):
            if intent_name == "symptoms":
                self._handle_symptoms(parameters)
                return True
            elif intent_name == "medication":
                self._handle_medication(parameters)
                return True
            
            return super().execute(intent_name, parameters)
        
        def _handle_symptoms(self, parameters):
            self.voice_output.speak("Please describe your symptoms in detail")
        
        def _handle_medication(self, parameters):
            drug = parameters.get("drug", "medication") if parameters else "medication"
            self.voice_output.speak(f"Information about {drug}...")
    
    # Use the custom executor
    from agent import VoiceAgent
    
    agent = VoiceAgent(use_voice=False)
    agent.action_executor = MedicalAssistant(agent.voice_output)
    
    return agent


# Example 5: Web API Integration
def example_web_api_integration():
    """Integrate with web APIs"""
    from flask import Flask, request, jsonify
    from nlp_engine import IntentRecognizer
    from action_executor import ActionExecutor
    from voice_io import VoiceOutput
    
    app = Flask(__name__)
    recognizer = IntentRecognizer()
    voice_out = VoiceOutput()
    executor = ActionExecutor(voice_out)
    
    @app.route('/process', methods=['POST'])
    def process_voice():
        """Process voice command from API"""
        data = request.json
        user_input = data.get('text')
        
        if not user_input:
            return jsonify({"error": "No text provided"}), 400
        
        # Recognize intent
        intent, confidence, entities = recognizer.recognize_intent(user_input)
        
        if not intent:
            return jsonify({
                "status": "error",
                "message": "Intent not recognized"
            }), 400
        
        # Execute action
        try:
            executor.execute(intent)
            return jsonify({
                "status": "success",
                "intent": intent,
                "confidence": confidence
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    return app


# Example 6: Database Integration
def example_database_integration():
    """Integrate with database"""
    from action_executor import ActionExecutor
    from voice_io import VoiceOutput
    import json
    from datetime import datetime
    
    class DatabaseExecutor(ActionExecutor):
        """Executor with database support"""
        
        def __init__(self, voice_output, db_file="interactions.json"):
            super().__init__(voice_output)
            self.db_file = db_file
        
        def _log_interaction(self, user_input, intent, confidence):
            """Log interaction to database"""
            record = {
                "timestamp": datetime.now().isoformat(),
                "input": user_input,
                "intent": intent,
                "confidence": confidence
            }
            
            try:
                with open(self.db_file, "r") as f:
                    data = json.load(f)
            except:
                data = []
            
            data.append(record)
            
            with open(self.db_file, "w") as f:
                json.dump(data, f, indent=2)
        
        def execute(self, intent_name, parameters=None):
            # Log interaction
            self._log_interaction("", intent_name, 0.9)
            
            # Execute normally
            return super().execute(intent_name, parameters)


# Example 7: Real-time Callback Handler
def example_callback_handler():
    """Use callbacks for real-time events"""
    from agent import VoiceAgent
    
    class CallbackAgent(VoiceAgent):
        """Agent with callback support"""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.on_intent_recognized = None
            self.on_action_executed = None
        
        def _process_input(self, user_input):
            intent_name, confidence, entities = self.intent_recognizer.recognize_intent(user_input)
            
            # Call callback
            if self.on_intent_recognized:
                self.on_intent_recognized(intent_name, confidence, entities)
            
            # Execute action
            success = self.action_executor.execute(intent_name)
            
            # Call callback
            if self.on_action_executed:
                self.on_action_executed(intent_name, success)
    
    # Use with callbacks
    agent = CallbackAgent(use_voice=False)
    
    def on_intent(intent, conf, entities):
        print(f"Intent recognized: {intent} ({conf:.2f})")
    
    def on_action(intent, success):
        print(f"Action executed: {intent} - {'Success' if success else 'Failed'}")
    
    agent.on_intent_recognized = on_intent
    agent.on_action_executed = on_action
    
    return agent


# Example 8: Batch Processing
def example_batch_processing():
    """Process batch of commands"""
    from nlp_engine import IntentRecognizer
    from action_executor import ActionExecutor
    from voice_io import VoiceOutput
    
    recognizer = IntentRecognizer()
    voice_out = VoiceOutput()
    executor = ActionExecutor(voice_out)
    
    commands = [
        "What time is it?",
        "Tell me a joke",
        "Search for Python programming",
        "What's the date today?"
    ]
    
    results = []
    for command in commands:
        intent, confidence, entities = recognizer.recognize_intent(command)
        
        if intent:
            executor.execute(intent)
            results.append({
                "command": command,
                "intent": intent,
                "confidence": confidence
            })
    
    return results


# Example 9: Configuration Override
def example_config_override():
    """Override configuration for specific use case"""
    from agent import VoiceAgent
    from config import COMMANDS
    
    # Create custom configuration
    custom_config = {
        "greeting": {
            "keywords": ["hello", "hi", "hey"],
            "responses": ["Good day, how can I assist?"],
            "action": "respond"
        },
        "farewell": {
            "keywords": ["bye", "goodbye", "see you"],
            "responses": ["Farewell! Take care!"],
            "action": "exit"
        }
    }
    
    # Override commands
    COMMANDS.clear()
    COMMANDS.update(custom_config)
    
    agent = VoiceAgent(use_voice=False)
    return agent


# Example 10: Performance Monitoring
def example_performance_monitoring():
    """Monitor agent performance"""
    import time
    from nlp_engine import IntentRecognizer
    
    recognizer = IntentRecognizer()
    
    test_inputs = [
        "hello",
        "what time",
        "search for python",
        "goodbye",
        "weather",
        "open notepad"
    ]
    
    times = []
    
    for input_text in test_inputs:
        start = time.time()
        intent, conf, _ = recognizer.recognize_intent(input_text)
        elapsed = time.time() - start
        times.append(elapsed)
        
        print(f"Input: '{input_text}' -> Intent: {intent} ({elapsed*1000:.2f}ms)")
    
    avg_time = sum(times) / len(times)
    print(f"\nAverage recognition time: {avg_time*1000:.2f}ms")


if __name__ == "__main__":
    print("JARVIS Integration Examples\n")
    
    print("1. Basic Integration")
    # example_basic_integration()
    
    print("2. Text Processing")
    example_text_processing()
    
    print("\n3. Custom Executor")
    agent = example_custom_executor()
    print(f"Created custom agent: {agent}")
    
    print("\n4. Performance Monitoring")
    example_performance_monitoring()

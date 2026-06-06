"""
Test Suite for JARVIS Voice Agent
Verifies all components are working correctly
"""

import unittest
from nlp_engine import IntentRecognizer
from config import COMMANDS


class TestIntentRecognizer(unittest.TestCase):
    """Test NLP intent recognition"""
    
    def setUp(self):
        self.recognizer = IntentRecognizer()
    
    def test_greeting_recognition(self):
        """Test greeting intent recognition"""
        intent, confidence, _ = self.recognizer.recognize_intent("hello")
        self.assertEqual(intent, "greeting")
        self.assertGreater(confidence, 0.5)
    
    def test_time_recognition(self):
        """Test time intent recognition"""
        intent, confidence, _ = self.recognizer.recognize_intent("what time is it")
        self.assertEqual(intent, "time")
        self.assertGreater(confidence, 0.5)
    
    def test_goodbye_recognition(self):
        """Test goodbye intent recognition"""
        intent, confidence, _ = self.recognizer.recognize_intent("goodbye")
        self.assertEqual(intent, "goodbye")
        self.assertGreater(confidence, 0.5)
    
    def test_entity_extraction(self):
        """Test entity extraction"""
        entities = self.recognizer.extract_entities("open chrome")
        self.assertIn("app_names", entities)
        self.assertIn("chrome", entities["app_names"])
    
    def test_parameter_extraction(self):
        """Test parameter extraction"""
        params = self.recognizer.extract_parameters("search for python", "search")
        self.assertIn("query", params)
        self.assertIn("python", params["query"])
    
    def test_confidence_threshold(self):
        """Test confidence threshold"""
        intent, confidence, _ = self.recognizer.recognize_intent("xyz123")
        if intent is not None:
            self.assertGreater(confidence, 0.5)


class TestConfiguration(unittest.TestCase):
    """Test configuration"""
    
    def test_commands_exist(self):
        """Test that commands are defined"""
        self.assertGreater(len(COMMANDS), 0)
    
    def test_command_structure(self):
        """Test command structure"""
        for intent_name, intent_config in COMMANDS.items():
            self.assertIn("keywords", intent_config)
            self.assertIn("responses", intent_config)
            self.assertIn("action", intent_config)
            self.assertIsInstance(intent_config["keywords"], list)
            self.assertIsInstance(intent_config["responses"], list)
    
    def test_required_intents(self):
        """Test that required intents exist"""
        required_intents = ["greeting", "goodbye", "time", "search"]
        for intent in required_intents:
            self.assertIn(intent, COMMANDS)


class TestUtilities(unittest.TestCase):
    """Test utility functions"""
    
    def test_entity_extraction_apps(self):
        """Test app name extraction"""
        recognizer = IntentRecognizer()
        entities = recognizer.extract_entities("open chrome and firefox")
        self.assertTrue(len(entities["app_names"]) > 0)
    
    def test_time_reference_extraction(self):
        """Test time reference extraction"""
        recognizer = IntentRecognizer()
        entities = recognizer.extract_entities("remind me in morning")
        self.assertIn("morning", entities["time_references"])


def run_tests():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════╗
║        🤖 JARVIS Test Suite                          ║
╚══════════════════════════════════════════════════════╝
    """)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestIntentRecognizer))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilities))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

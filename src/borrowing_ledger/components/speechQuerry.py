from src.borrowing_ledger.components.speech_recog import SpeechRecognizer
from src.borrowing_ledger.components.nlp_processor import ExpandedNLPProcessor
from src.borrowing_ledger.components.query_generator import MongoDBQueryGenerator
from typing import Dict, Any

class IntegratedSpeechQuerySystem:
    def __init__(self, mongo_connection_string: str, language: str = "en-IN", wake_word: str = "chhotu"):
        self.speech_recognizer = SpeechRecognizer(language=language, wake_word=wake_word)
        self.nlp_processor = ExpandedNLPProcessor()
        self.query_generator = MongoDBQueryGenerator(mongo_connection_string)

    def process_speech_input(self) -> Dict[str, Any]:
        while True:
            transcribed_text = self.speech_recognizer.recognize_speech()
            if transcribed_text:
                print(f"Transcribed text: {transcribed_text}")
                processed_info = self.nlp_processor.process_text(transcribed_text)
                intent = processed_info['intent']
                entities = {
                    "customer_name": processed_info['name'],
                    "amount": processed_info['amount'],
                    "items": processed_info['item'],
                    "phrase": transcribed_text
                }
                result = self.query_generator.generate_query(intent, entities)
                print(f"Query result: {result}")
                return result
            else:
                print("Speech recognition failed or was interrupted. Trying again...")

    def run(self):
        print(f"Listening for wake word '{self.speech_recognizer.wake_word}'...")
        while True:
            result = self.process_speech_input()
            # Here you can add logic to handle the result, e.g., speak it back to the user
            print("Waiting for next command...")

    def close(self):
        self.query_generator.close_connection()

# Usage example:
if __name__ == "__main__":
    mongo_connection_string = "mongodb://localhost:27017/"
    integrated_system = IntegratedSpeechQuerySystem(mongo_connection_string, language="en-IN", wake_word="chhotu")
    
    try:
        integrated_system.run()
    except KeyboardInterrupt:
        print("\nStopping the system...")
    finally:
        integrated_system.close()
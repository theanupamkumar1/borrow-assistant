# src/borrowing_ledger/components/nlp_processor.py
from src.borrowing_ledger.components.intent_classifer import IntentClassifier
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

class ExpandedNLPProcessor:
    def __init__(self):
        self.amount_pattern = r'\d+'
        self.name_pattern = r'\b[A-Za-z]+\b'
        self.item_keywords = ['ke', 'ka', 'ki']
        self.intent_keywords = {
            'add_entry': ['likh', 'add', 'jama'],
            'show_balance': ['dikha', 'show', 'batao'],
            'delete_entry': ['mita', 'delete', 'hata'],
            'calculation': ['calculate', 'gin'],
            'subtraction': ['minus', 'ghata', 'kam']
        }

    def process_text(self, text):
        # Transliterate the text to Latin script
        latin_text = transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
        
        # Convert to lowercase for easier processing
        latin_text = latin_text.lower()
        
        # Extract information
        intent = self._determine_intent(latin_text)
        result = {
            'intent': intent,
            'amount': self._extract_amount(latin_text),
            'name': self._extract_name(latin_text),
            'item': self._extract_item(latin_text)
        }

        # Additional processing based on intent
        if intent == 'calculation' or intent == 'subtraction':
            result['operands'] = self._extract_operands(latin_text)

        return result

    def _extract_amount(self, text):
        matches = re.findall(self.amount_pattern, text)
        return int(matches[0]) if matches else None

    def _extract_name(self, text):
        words = text.split()
        for i, word in enumerate(words):
            if word in ['ke', 'ka', 'ki'] and i > 0:
                return words[i-1].capitalize()
        return None

    def _extract_item(self, text):
        words = text.split()
        for i, word in enumerate(words):
            if word in self.item_keywords and i < len(words) - 1:
                return words[i+1]
        return None

    def _determine_intent(self, text):
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in text for keyword in keywords):
                return intent
        return 'unknown'

    def _extract_operands(self, text):
        numbers = re.findall(self.amount_pattern, text)
        return [int(num) for num in numbers]




# Usage example
if __name__ == "__main__":

    input_text = "15 rupaye likho geeta ke liye"
    classifier = IntentClassifier()
  # Assuming this is the file where we defined the IntentClassifier class
    model_path=r"C:\Users\anupam kumar\Downloads\borrow-assistant\src\borrowing_ledger\components\intent_classifier_model.joblib"
    def predict_intent(input_text, model_path):
    # Load the saved model
        classifier = IntentClassifier()
        classifier.load_model(model_path)
        
        # Predict the intent
        intent = classifier.predict_intent(input_text)
        return intent
    
    model_path = r'intent_classification_pipeline.joblib'  # Path to your saved model
    
    # Test phrases
    test_phrases = [
        "subham ka total kitna hai",
        "meena ke 40 rupee kaat do",
        "Hata do 30 rupaye wali entry",
        "40 rupee likh do mina ke",
        "aau ke 30 rupee jama kar do",
        "bhvaesh ke 20 rupee likh do"
    ]
    
    # Predict intents for test phrases
    for phrase in test_phrases:
        predicted_intent = predict_intent(phrase, model_path)
        print(f"Phrase: {phrase}")
        print(f"Predicted Intent: {predicted_intent}\n")
    
    # Interactive prediction
    while True:
        user_input = input("Enter a phrase (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        predicted_intent = predict_intent(user_input, model_path)
        print(f"Predicted Intent: {predicted_intent}\n")



processor = ExpandedNLPProcessor()




        

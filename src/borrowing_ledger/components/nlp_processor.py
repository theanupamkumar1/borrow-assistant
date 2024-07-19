from intent_classifer import IntentClassifier
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

class ExpandedNLPProcessor:
    def __init__(self, input_text=""):
        self.input_text = input_text 
        self.amount_pattern = r'\d+'
        self.name_pattern = r'\b[A-Za-z]+\b'
        self.item_keywords = ['ke', 'ka', 'ki']
        self.intent_keywords = {
            'add_entry': ['likh', 'add', 'jama'],
            'show_balance': ['dikha', 'show', 'batao'],
            'delete_entry': ['mita', 'delete', 'hata'],
            'calculation': ['calculate', 'gin'],
            'subtraction': ['minus', 'ghata', 'kam'],
            'actions': ['mail', 'email', 'e-mail', 'send', 'bhej', 'forward', 'share', 'transfer','whatsapp']
        }

    def set_input_text(self, input_text):
        self.input_text = input_text

    def get_input_text(self):
        return self.input_text

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

   

# Usage example
if __name__ == "__main__":

    input_text = "15 rupaye kaat do geeta ke liye"

    processor = ExpandedNLPProcessor(input_text)
    input = processor.get_input_text()
    print(f"Input from processor: {input}")
    processed_info = processor.process_text(input_text)
    print(processed_info)

    # Assuming this is the file where we defined the IntentClassifier class
    model_path = r"C:\Users\anupam kumar\Downloads\borrow-assistant\src\borrowing_ledger\components\intent_classifier_model.joblib"
    
    def predict_intent(input_text, model_path):
        classifier = IntentClassifier()
        classifier.load_model(model_path)
        
        # Predict the intent
        intent = classifier.predict_intent(input_text)
        print(f"Predicted Intent: {intent}")
        return intent

    intent = predict_intent(input_text, model_path)
    print(f"Predicted Intent: {intent}")

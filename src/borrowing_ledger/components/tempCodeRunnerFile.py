# src/borrowing_ledger/components/nlp_processor.py

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
    processor = ExpandedNLPProcessor()
    
    # Test cases
    test_cases = [
        "5 rupee likh do arun ke biscuit ke",
        "10 rupaye add karo rahul ke chai ke",
        "Priya ka balance dikha do",
        "Delete karo 15 rupaye wala entry amit ka",
        "Calculate karo 50 aur 30",
        "20 minus 7 karo",
        "Suman ke 100 rupaye ghata do",
    ]

    for text in test_cases:
        result = processor.process_text(text)
        print(f"Input: {text}")
        print(f"Output: {result}\n")
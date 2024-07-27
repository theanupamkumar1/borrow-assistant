from pymongo import MongoClient
from datetime import datetime
import pyttsx3

class MongoDBHandler:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['borrowing_ledger']
        self.tts_engine = pyttsx3.init()

    def speak(self, message):
        self.tts_engine.say(message)
        self.tts_engine.runAndWait()

    def add_customer_entry(self, customer_name, date, items, amount, phrase, total):
        collection = self.db[customer_name]
        entry = {
            "date": date,
            "items": items,
            "amount": amount,
            "phrase": phrase,
            "total": total,
            "created_at": datetime.utcnow()
        }
        result = collection.insert_one(entry)
        self.speak("Entry added successfully")
        return result.inserted_id
    
    def get_customer_entries(self, customer_name):
        collection = self.db[customer_name]
        return list(collection.find())

    def get_total_balance(self, customer_name):
        collection = self.db[customer_name]
        pipeline = [
            {"$group": {"_id": None, "total_balance": {"$sum": "$amount"}}}
        ]
        result = list(collection.aggregate(pipeline))
        total_balance = result[0]['total_balance'] if result else 0
        self.speak(f"Total balance for {customer_name} is {total_balance}")
        return total_balance

    def delete_entry(self, customer_name, amount):
        collection = self.db[customer_name]
        result = collection.delete_one({"amount": amount})
        if result.deleted_count > 0:
            self.speak("Entry deleted successfully")
            return True
        else:
            self.speak("Entry not found")
            return False

# Usage example:
if __name__ == '__main__':
    mongo_handler = MongoDBHandler("mongodb://localhost:27017/")
    
    # Add a root user
    mongo_handler.add_root_user("John Doe", "Johnny")
    
    # Add an entry for the customer
    mongo_handler.add_customer_entry("John Doe", "2023-07-17", "Book", 20.5, "Borrowed for study", 20.5)
    
    # Get all entries for the customer
    entries = mongo_handler.get_customer_entries("John Doe")
    print(entries)
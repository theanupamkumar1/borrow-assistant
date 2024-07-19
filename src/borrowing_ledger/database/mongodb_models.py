from pymongo import MongoClient
from datetime import datetime

class MongoDBHandler:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['borrowing_ledger']
        self.root_users = self.db['root_users']
        
    def add_root_user(self, customer_name, alias=None):
    # Check if the user already exists
        if self.root_users.count_documents({"customer_name": customer_name}) == 0:
            user = {
                "customer_name": customer_name,
                "alias": alias,
                "created_at": datetime.utcnow()
            }
            return self.root_users.insert_one(user).inserted_id
        else:
            print(f"User {customer_name} already exists.")
        return None
    
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
        return collection.insert_one(entry).inserted_id
    
    def get_customer_entries(self, customer_name):
        collection = self.db[customer_name]
        return list(collection.find())

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
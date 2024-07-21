from src.borrowing_ledger.components.nlp_processor import ExpandedNLPProcessor
# from src.borrowing_ledger.components.intent_classifer import IntentClassifier

from typing import Dict, Any
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDBQueryGenerator:
    def __init__(self, connection_string: str, db_name: str = 'borrowing_ledger'):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

    def generate_query(self, intent: str, entities: Dict[str, Any]) -> Any:
        if intent == "add_entry":
            return self.add_entry_query(entities)
        elif intent == "show_balance":
            return self.show_balance_query(entities)
        elif intent == "subtraction":
            return self.subtraction(entities)
        elif intent == "update_entry":
            return self.update_entry_query(entities)
        elif intent == "add_user":
            return self.add_user_query(entities)
        elif intent == "actions":
            return self.add_user_query(entities)
        else:
            print(f"Unsupported intent: {intent}. No action taken.")
            return {"status": "error", "message": "Unsupported intent"}

    def add_entry_query(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        customer_name = entities.get('customer_name')
        amount = entities.get('amount')
        
        if not all([customer_name, amount]):
            raise ValueError("Customer name and amount are required for adding an entry")
        
        entry = {
            "customer_name": customer_name,
            "date": entities.get('date') or datetime.now(),
            "items": entities.get('items'),
            "amount": amount,
            "phrase": entities.get('phrase'),
            "total": amount,
            "created_at": datetime.now()
        }
        
        result = self.db.ledger_entries.insert_one(entry)
        return {"status": "success", "message": "Entry added successfully", "id": str(result.inserted_id)}

    def show_balance_query(self, entities: Dict[str, Any]) -> Dict[str, float]:
        customer_name = entities.get('customer_name')
        if not customer_name:
            raise ValueError("Customer name is required for showing balance")
        
        pipeline = [
            {"$match": {"customer_name": customer_name}},
            {"$group": {"_id": None, "total_balance": {"$sum": "$amount"}}}
        ]
        result = list(self.db.ledger_entries.aggregate(pipeline))
        
        total_balance = result[0]['total_balance'] if result else 0
        return {"customer": customer_name, "balance": total_balance}

    def subtraction(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = entities.get('entry_id')
        if not entry_id:
            raise ValueError("Entry ID is required for deleting an entry")
        
        result = self.db.ledger_entries.delete_one({"_id": ObjectId(entry_id)})
        if result.deleted_count:
            return {"status": "success", "message": "Entry deleted successfully"}
        else:
            return {"status": "error", "message": "Entry not found"}

    def update_entry_query(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = entities.get('entry_id')
        amount = entities.get('amount')
        
        if not all([entry_id, amount]):
            raise ValueError("Entry ID and amount are required for updating an entry")
        
        update_data = {
            "date": entities.get('date') or datetime.now(),
            "items": entities.get('items'),
            "amount": amount,
            "phrase": entities.get('phrase'),
            "total": amount,
            "updated_at": datetime.now()
        }
        
        result = self.db.ledger_entries.update_one(
            {"_id": ObjectId(entry_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return {"status": "success", "message": "Entry updated successfully"}
        else:
            return {"status": "error", "message": "Entry not found or no changes made"}

    def add_user_query(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        customer_name = entities.get('customer_name')
        alias = entities.get('alias')
        if not customer_name:
            raise ValueError("Customer name is required for adding a user")
        
        user = {
            "customer_name": customer_name,
            "alias": alias,
            "created_at": datetime.now()
        }
        
        result = self.db.users.insert_one(user)
        return {"status": "success", "message": "User added successfully", "id": str(result.inserted_id)}

    def close_connection(self):
        self.client.close()

# Usage example:
if __name__ == "__main__":
    query_gen = MongoDBQueryGenerator("mongodb://localhost:27017/")
    
    # Example: Add a new user
    result = query_gen.generate_query("add_user", {"customer_name": "Jane Doe", "alias": "Janey"})
    print(result)
    
    # Example: Add an entry
    result = query_gen.generate_query("add_entry", {
        "customer_name": "Jane Doe",
        "amount": 50.0,
        "items": "Groceries",
        "phrase": "Weekly shopping"
    })
    print(result)
    
    # Example: Show balance
    result = query_gen.generate_query("show_balance", {"customer_name": "Jane Doe"})
    print(result)
    

    processor = ExpandedNLPProcessor()

    input_text = "15 rupaye jama do shubham ke liye"
    processed_info = processor.process_text(input_text)
    print(processed_info)
    intent = processed_info['intent']
    entities = {
        "customer_name": processed_info['name'],
        "amount": processed_info['amount'],
        "items": processed_info['item'],
        "phrase": input_text
    }
    print(intent, entities)
    result = query_gen.generate_query(intent, entities)
    print(result)
    query_gen.close_connection()

from typing import Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
from src.borrowing_ledger.database.mongodb_models import MongoDBHandler  # Import the MongoDBHandler

class MongoDBQueryGenerator:
    def __init__(self, connection_string: str):
        self.handler = MongoDBHandler(connection_string)

    def generate_query(self, intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        if intent == "add_entry":
            return self.add_entry_query(entities)
        elif intent == "show_balance":
            return self.show_balance_query(entities)
        elif intent == "subtraction":
            return self.subtraction(entities)
        else:
            self.handler.speak("Unsupported intent")
            return {"status": "error", "message": "Unsupported intent"}

    def add_entry_query(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        customer_name = entities.get('customer_name')
        amount = entities.get('amount')
        
        if not all([customer_name, amount]):
            raise ValueError("Customer name and amount are required for adding an entry")
        
        entry_id = self.handler.add_customer_entry(
            customer_name,
            entities.get('date') or datetime.now(),
            entities.get('items'),
            amount,
            entities.get('phrase'),
            amount
        )
        return {"status": "success", "message": "Entry added successfully", "id": str(entry_id)}

    def show_balance_query(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        customer_name = entities.get('customer_name')
        if not customer_name:
            raise ValueError("Customer name is required for showing balance")
        
        total_balance = self.handler.get_total_balance(customer_name)
        return {"customer": customer_name, "balance": total_balance}

    def subtraction(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        customer_name = entities.get('customer_name')
        amount = entities.get('amount')
        
        if not all([customer_name, amount]):
            raise ValueError("Customer name and amount are required for subtraction")
        
        success = self.handler.delete_entry(customer_name, amount)
        if success:
            return {"status": "success", "message": "Entry deleted successfully"}
        else:
            return {"status": "error", "message": "Entry not found"}

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
    

    # processor = ExpandedNLPProcessor()

    # input_text = "15 rupaye jama do shubham ke liye"
    # processed_info = processor.process_text(input_text)
    # print(processed_info)
    # intent = processed_info['intent']
    # entities = {
    #     "customer_name": processed_info['name'],
    #     "amount": processed_info['amount'],
    #     "items": processed_info['item'],
    #     "phrase": input_text
    # }
    # print(intent, entities)
    # result = query_gen.generate_query(intent, entities)
    # print(result)
    # query_gen.close_connection()

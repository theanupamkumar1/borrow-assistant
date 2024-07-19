import sqlite3
from pymongo import MongoClient
from datetime import datetime
from pymongo import MongoClient
from query_generator import MongoDBQueryGenerator

class DatabaseManager:
    def __init__(self, sqlite_db_path, mongo_connection_string):
        # SQLite setup
        self.sqlite_conn = sqlite3.connect(sqlite_db_path)
        self.sqlite_cursor = self.sqlite_conn.cursor()

        # MongoDB setup
        self.mongo_client = MongoClient(mongo_connection_string)
        self.mongo_db = self.mongo_client['borrowing_ledger']

    def add_root_user(self, customer_name, alias=None):
        # Add to SQLite
        sqlite_query = "INSERT INTO root_users (customer_name, alias) VALUES (?, ?)"
        self.sqlite_cursor.execute(sqlite_query, (customer_name, alias))
        self.sqlite_conn.commit()

        # Add to MongoDB
        mongo_collection = self.mongo_db['root_users']
        mongo_collection.insert_one({
            "customer_name": customer_name,
            "alias": alias,
            "created_at": datetime.utcnow()
        })

    def get_root_users(self):
        # Fetch from SQLite (primary source for offline mode)
        sqlite_query = "SELECT customer_name, alias FROM root_users"
        self.sqlite_cursor.execute(sqlite_query)
        return self.sqlite_cursor.fetchall()

    def add_customer_entry(self, customer_name, date, items, amount, phrase, total):
        # Add to SQLite
        sqlite_query = f"INSERT INTO '{customer_name}' (date, items, amount, phrase, total) VALUES (?, ?, ?, ?, ?)"
        self.sqlite_cursor.execute(sqlite_query, (date, items, amount, phrase, total))
        self.sqlite_conn.commit()

        # Add to MongoDB
        mongo_collection = self.mongo_db[customer_name]
        mongo_collection.insert_one({
            "date": date,
            "items": items,
            "amount": amount,
            "phrase": phrase,
            "total": total,
            "created_at": datetime.utcnow()
        })

    def get_customer_entries(self, customer_name):
        # Fetch from SQLite (primary source for offline mode)
        sqlite_query = f"SELECT date, items, amount, phrase, total FROM '{customer_name}'"
        self.sqlite_cursor.execute(sqlite_query)
        return self.sqlite_cursor.fetchall()

    def update_customer_entry(self, customer_name, entry_id, date, items, amount, phrase, total):
        # Update in SQLite
        sqlite_query = f"UPDATE '{customer_name}' SET date=?, items=?, amount=?, phrase=?, total=? WHERE id=?"
        self.sqlite_cursor.execute(sqlite_query, (date, items, amount, phrase, total, entry_id))
        self.sqlite_conn.commit()

        # Update in MongoDB
        mongo_collection = self.mongo_db[customer_name]
        mongo_collection.update_one(
            {"_id": entry_id},
            {"$set": {
                "date": date,
                "items": items,
                "amount": amount,
                "phrase": phrase,
                "total": total,
                "updated_at": datetime.utcnow()
            }}
        )

    def delete_customer_entry(self, customer_name, entry_id):
        # Delete from SQLite
        sqlite_query = f"DELETE FROM '{customer_name}' WHERE id=?"
        self.sqlite_cursor.execute(sqlite_query, (entry_id,))
        self.sqlite_conn.commit()

        # Delete from MongoDB
        mongo_collection = self.mongo_db[customer_name]
        mongo_collection.delete_one({"_id": entry_id})

    def sync_databases(self):
        # This method would handle syncing between SQLite and MongoDB
        # It's a complex operation that depends on your specific sync requirements
        # Here's a basic outline:
        
        # 1. Get all root users from SQLite
        sqlite_users = self.get_root_users()
        
        # 2. For each user, get their entries from SQLite
        for user in sqlite_users:
            customer_name = user[0]
            sqlite_entries = self.get_customer_entries(customer_name)
            
            # 3. Compare with MongoDB entries and sync
            mongo_collection = self.mongo_db[customer_name]
            mongo_entries = list(mongo_collection.find())
            
            # Here you would implement logic to compare entries and update accordingly
            # This could involve comparing timestamps, handling conflicts, etc.
            
        # Note: This is a simplified example. Real-world sync would be more complex.

    def close_connections(self):
        self.sqlite_conn.close()
        self.mongo_client.close()

class MongoDBCRUD:
    def __init__(self, uri: str):
        self.client = MongoClient(uri)
        self.query_generator = MongoDBQueryGenerator()
        self.db = self.client[self.query_generator.db_name]

    def execute_query(self, intent: str, entities: dict):
        query = self.query_generator.generate_query(intent, entities)
        collection = self.db[query['collection']]

        if query['operation'] == 'insert_one':
            result = collection.insert_one(query['document'])
            print(f"Inserted one document: {result.inserted_id}")
        elif query['operation'] == 'find':
            documents = collection.find(query['filter'])
            for doc in documents:
                print(doc)
        elif query['operation'] == 'delete_one':
            result = collection.delete_one(query['filter'])
            print(f"Deleted {result.deleted_count} document(s)")
        elif query['operation'] == 'update_one':
            result = collection.update_one(query['filter'], query['update'])
            print(f"Updated {result.modified_count} document(s)")
        else:
            print("Unsupported operation")

# Example usage
if __name__ == "__main__":
    crud = MongoDBCRUD("mongodb://localhost:27017/")
    crud.execute_query("add_entry", {"customer_name": "John Doe", "amount": 100})
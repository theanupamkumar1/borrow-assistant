import os
from dotenv import load_dotenv
from src.borrowing_ledger.components.speechQuerry import IntegratedSpeechQuerySystem

def main():
    # Load environment variables
    load_dotenv()

    # Get MongoDB connection string from environment variable
    # Temporary for testing
    # MONGO_CONNECTION_STRING = "mongodb://localhost:27017/yourDatabaseName"
    mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')
    if not mongo_connection_string:
        raise ValueError("MongoDB connection string not found in environment variables")

    # Create and run the integrated system
    integrated_system = IntegratedSpeechQuerySystem(
        mongo_connection_string=mongo_connection_string,
        language="en-IN",
        wake_word="chhotu"
    )

    try:
        print("Starting the Borrowing Ledger Voice Assistant...")
        integrated_system.run()
    except KeyboardInterrupt:
        print("\nStopping the system...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        integrated_system.close()

if __name__ == "__main__":
    main()
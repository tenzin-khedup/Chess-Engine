from pymongo import MongoClient
from pprint import pprint

def check_mongodb_contents():
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017")
        
        # Get the database
        db = client['AIchessplayer']
        
        # Get list of all collections
        collections = db.list_collection_names()
        
        if not collections:
            print("No collections found in the database 'AIchessplayer'")
            return
            
        print(f"\nFound collections: {collections}")
        
        # Display contents of each collection
        for collection_name in collections:
            print(f"\n=== Contents of {collection_name} collection ===")
            collection = db[collection_name]
            documents = list(collection.find())
            
            if not documents:
                print(f"No documents found in {collection_name}")
            else:
                print(f"Number of documents: {len(documents)}")
                for doc in documents:
                    print("\nDocument:")
                    pprint(doc)
                    
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

if __name__ == "__main__":
    print("Checking MongoDB contents...")
    check_mongodb_contents() 
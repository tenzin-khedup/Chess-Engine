from db_config import get_database
from datetime import datetime
from pprint import pprint

def test_db_connection():
    db = get_database()
    if db is not None:
        print("Successfully connected to MongoDB database 'AIchessplayer'!")
        # List all collections in the database
        collections = db.list_collection_names()
        print(f"Available collections: {collections}")
        return True
    else:
        print("Failed to connect to MongoDB!")
        return False

def add_sample_chess_data():
    db = get_database()
    if db is None:
        print("Failed to connect to MongoDB!")
        return False

    # Add sample data to the chess collection
    chess_collection = db['chess']
    
    # First, let's check if we already have data
    existing_games = list(chess_collection.find())
    if existing_games:
        print(f"Found {len(existing_games)} existing games in the collection")
    
    # Add a new game
    sample_game = {
        'game_id': len(existing_games) + 1,
        'moves': ['e2e4', 'e7e5', 'g1f3'],
        'result': 'ongoing',
        'timestamp': datetime.utcnow(),
        'player_color': 'white',
        'board_position': 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
    }
    
    try:
        result = chess_collection.insert_one(sample_game)
        print(f"Successfully added game with ID: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"Error adding game: {e}")
        return False

def display_chess_collection():
    db = get_database()
    if db is None:
        print("Failed to connect to MongoDB!")
        return

    # Display chess collection contents
    print("\n=== Chess Collection Contents ===")
    try:
        games = list(db['chess'].find())
        if not games:
            print("No games found in the collection")
            return
            
        for game in games:
            print("\nGame Document:")
            # Convert ObjectId to string for better display
            game['_id'] = str(game['_id'])
            pprint(game)
    except Exception as e:
        print(f"Error displaying games: {e}")

# Run the connection test, add sample data, and display contents
if __name__ == "__main__":
    if test_db_connection():
        add_sample_chess_data()
        print("\nDisplaying chess collection contents:")
        display_chess_collection() 
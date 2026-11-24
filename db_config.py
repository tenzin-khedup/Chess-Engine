from pymongo import MongoClient
from datetime import datetime

def get_database():
    # Replace with your MongoDB connection string
    CONNECTION_STRING = "mongodb://localhost:27017"
    
    try:
        client = MongoClient(CONNECTION_STRING)
        # Create/connect to database
        db = client['AIchessplayer']
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def save_game_data(db, episode, total_reward, moves, final_position):
    try:
        games_collection = db['chess']
        game_data = {
            'episode': episode,
            'total_reward': total_reward,
            'moves': moves,
            'final_position': final_position,
            'timestamp': datetime.utcnow()
        }
        games_collection.insert_one(game_data)
    except Exception as e:
        print(f"Error saving game data: {e}")

def save_model_weights(db, model_weights, episode):
    try:
        weights_collection = db['model_weights']
        weights_data = {
            'episode': episode,
            'weights': model_weights,
            'timestamp': datetime.utcnow()
        }
        weights_collection.insert_one(weights_data)
    except Exception as e:
        print(f"Error saving model weights: {e}") 
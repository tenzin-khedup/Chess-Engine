import chess
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models 
import random
from collections import deque

# Hyperparameters
STATE_SHAPE = (64,)  # 8x8 board flattened
ACTION_SPACE = 4672  # Total possible moves in chess
GAMMA = 0.99         # Discount factor
EPSILON_START = 1.0  # Exploration rate
EPSILON_MIN = 0.1
EPSILON_DECAY = 0.995
LEARNING_RATE = 0.001
BATCH_SIZE = 64
MEMORY_SIZE = 10000

# Create the DQN model
def create_dqn():
    model = models.Sequential([
        layers.Input(shape=STATE_SHAPE),
        layers.Dense(256, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(ACTION_SPACE, activation='linear')  # Output Q-values for all actions
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
                  loss='mse')
    return model

# Encode the chessboard into a flat array
def encode_board(board):
    board_matrix = np.zeros(64, dtype=int)
    piece_map = board.piece_map()
    for square, piece in piece_map.items():
        board_matrix[square] = piece.piece_type if piece.color else -piece.piece_type
    return board_matrix

# Select an action using epsilon-greedy policy
def select_action(model, state, legal_moves, epsilon):
    if np.random.rand() < epsilon:
        return random.choice(legal_moves)  # Explore
    else:
        q_values = model.predict(state[np.newaxis], verbose=0)[0]
        legal_q_values = [q_values[move.to_square * 64 + move.from_square] for move in legal_moves]
        return legal_moves[np.argmax(legal_q_values)]  # Exploit

# Replay buffer for experience replay
class ReplayBuffer:
    def __init__(self, size):
        self.buffer = deque(maxlen=size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

# Train the model
def train_dqn(model, target_model, memory, batch_size):
    if len(memory.buffer) < batch_size:
        return

    batch = memory.sample(batch_size)
    states, actions, rewards, next_states, dones = zip(*batch)

    states = np.array(states)
    next_states = np.array(next_states)
    targets = model.predict(states, verbose=0)

    # Update Q-values
    next_q_values = target_model.predict(next_states, verbose=0)
    for i in range(batch_size):
        action_index = actions[i].to_square * 64 + actions[i].from_square
        if dones[i]:
            targets[i, action_index] = rewards[i]
        else:
            targets[i, action_index] = rewards[i] + GAMMA * np.max(next_q_values[i])

    model.fit(states, targets, epochs=1, verbose=0, batch_size=batch_size)

# Main training loop
def train_chess_dqn():
    env = chess.Board()
    dqn = create_dqn()
    target_dqn = create_dqn()
    target_dqn.set_weights(dqn.get_weights())
    memory = ReplayBuffer(MEMORY_SIZE)

    epsilon = EPSILON_START

    for episode in range(1000):  # Number of episodes
        env.reset()
        state = encode_board(env)
        total_reward = 0

        while not env.is_game_over():
            legal_moves = list(env.legal_moves)
            action = select_action(dqn, state, legal_moves, epsilon)

            # Make the move and observe the reward
            env.push(action)
            next_state = encode_board(env)
            reward = 0  # Define a reward system (e.g., material advantage, checkmate)
            done = env.is_game_over()

            # Add experience to replay buffer
            memory.add((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward

            # Train the model
            train_dqn(dqn, target_dqn, memory, BATCH_SIZE)

        # Decay epsilon
        epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)

        # Update the target network
        if episode % 10 == 0:
            target_dqn.set_weights(dqn.get_weights())

        print(f"Episode {episode}, Total Reward: {total_reward}")

    return dqn

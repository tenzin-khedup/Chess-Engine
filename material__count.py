import chess






def calculate_reward(board, previous_material, done):
    """
    Calculate the reward for a move.

    Args:
        board (chess.Board): Current board state.
        previous_material (int): Material value before the move.
        done (bool): True if the game is over, otherwise False.

    Returns:
        float: Reward for the move.
    """
    # Define material values
    material_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0,  # King has no material value but is essential
    }

    # Calculate material score
    def material_score(board):
        score = 0
        for piece_type, value in material_values.items():
            score += len(board.pieces(piece_type, chess.WHITE)) * value
            score -= len(board.pieces(piece_type, chess.BLACK)) * value
        return score

    # Check game outcome
    if done:
        if board.is_checkmate():
            return 1.0 if board.turn == chess.BLACK else -1.0  # Reward winning player
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
            return 0.5  # Draw
        else:
            return 0  # No outcome yet (rare case)

    # Calculate material reward
    current_material = material_score(board)
    material_reward = current_material - previous_material

    # Check reward
    check_reward = 0.05 if board.is_check() else 0

    # Combine rewards
    total_reward = material_reward * 0.1 + check_reward
    return total_reward

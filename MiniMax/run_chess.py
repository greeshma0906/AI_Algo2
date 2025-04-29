import gym
import gym_chess
import chess
import numpy as np

def evaluate_board(board):
    """Basic material evaluation: +1 for pawn, +3 for knight/bishop, +5 for rook, +9 for queen."""
    if board.is_checkmate():
        return -9999 if board.turn else 9999  # Checkmate is good for the side that caused it

    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }

    score = 0
    for piece_type in piece_values:
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    return score

def minimax(board, depth, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if is_maximizing:
        max_eval = -np.inf
        for move in board.legal_moves:
            board.push(move)
            eval_score, _ = minimax(board, depth - 1, False)
            board.pop()
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = np.inf
        for move in board.legal_moves:
            board.push(move)
            eval_score, _ = minimax(board, depth - 1, True)
            board.pop()
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

# Example of using it in a gym_chess environment
env = gym.make('Chess-v0')
obs = env.reset()

done = False
while not done:

    board = env.unwrapped._board

    if board.turn:  # White (your agent)
        _, best_move = minimax(board.copy(), depth=2, is_maximizing=True)
        #action = env.encode(best_move)
        action = best_move
    else:  # Random black move
        legal_moves = list(board.legal_moves)
        #action = env.encode(np.random.choice(legal_moves))
        action = np.random.choice(list(board.legal_moves))  



    obs, reward, done, info = env.step(action)
    print(board)

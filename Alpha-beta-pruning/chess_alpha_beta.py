import chess
import random

# Define piece values for evaluation
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 1000
}

# Evaluation function
def evaluate_board(board):
    evaluation = 0
    for piece_type in piece_values.keys():
        evaluation += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        evaluation -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return evaluation

# Alpha-Beta Pruning
def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    legal_moves = list(board.legal_moves)
    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval, _ = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval, _ = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# Play game
def play_game(depth=3):
    board = chess.Board()
    move_count = 1

    while not board.is_game_over():
        print(f"\nMove {move_count}:")
        print(board)

        if board.turn == chess.WHITE:
            _, move = alpha_beta(board, depth, float('-inf'), float('inf'), True)
        else:
            _, move = alpha_beta(board, depth, float('-inf'), float('inf'), False)

        print(f"Selected move: {move}")
        board.push(move)
        move_count += 1

    print("\nGame Over!")
    print("Result:", board.result())

if __name__ == "__main__":
    play_game(depth=3)

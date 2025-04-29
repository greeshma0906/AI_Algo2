# import chess
# import random

# # Define piece values for evaluation
# piece_values = {
#     chess.PAWN: 1,
#     chess.KNIGHT: 3,
#     chess.BISHOP: 3,
#     chess.ROOK: 5,
#     chess.QUEEN: 9,
#     chess.KING: 1000
# }

# # Evaluation function
# def evaluate_board(board):
#     evaluation = 0
#     for piece_type in piece_values.keys():
#         evaluation += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
#         evaluation -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
#     return evaluation

# # Alpha-Beta Pruning
# def alpha_beta(board, depth, alpha, beta, maximizing_player):
#     if depth == 0 or board.is_game_over():
#         return evaluate_board(board), None

#     legal_moves = list(board.legal_moves)
#     best_move = None

#     if maximizing_player:
#         max_eval = float('-inf')
#         for move in legal_moves:
#             board.push(move)
#             eval, _ = alpha_beta(board, depth - 1, alpha, beta, False)
#             board.pop()

#             if eval > max_eval:
#                 max_eval = eval
#                 best_move = move

#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval, best_move
#     else:
#         min_eval = float('inf')
#         for move in legal_moves:
#             board.push(move)
#             eval, _ = alpha_beta(board, depth - 1, alpha, beta, True)
#             board.pop()

#             if eval < min_eval:
#                 min_eval = eval
#                 best_move = move

#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval, best_move

# # Play game
# def play_game(depth=3):
#     board = chess.Board()
#     move_count = 1

#     while not board.is_game_over():
#         print(f"\nMove {move_count}:")
#         print(board)

#         if board.turn == chess.WHITE:
#             _, move = alpha_beta(board, depth, float('-inf'), float('inf'), True)
#         else:
#             _, move = alpha_beta(board, depth, float('-inf'), float('inf'), False)

#         print(f"Selected move: {move}")
#         board.push(move)
#         move_count += 1

#     print("\nGame Over!")
#     print("Result:", board.result())

# if __name__ == "__main__":
#     play_game(depth=3)

import pygame
import chess
import chess.svg
from io import BytesIO
import cairosvg
import random
import time
import imageio
import os

# Initialize board
board = chess.Board()

# Set up display
WIDTH, HEIGHT = 512, 512
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alpha-Beta Chess")

# Load piece images from SVGs
def render_board(board):
    svg_data = chess.svg.board(board=board).encode("utf-8")
    png_bytes = cairosvg.svg2png(bytestring=svg_data)
    image_io = BytesIO(png_bytes)
    return pygame.image.load(image_io, 'board.png')

# Evaluation
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 1000
}

def evaluate_board(board):
    evaluation = 0
    for piece_type in piece_values:
        evaluation += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        evaluation -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return evaluation

# Alpha-Beta
def alpha_beta(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    legal_moves = list(board.legal_moves)

    if maximizing:
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

# Game loop

def play_game():
    running = True
    clock = pygame.time.Clock()
    move_delay = 1.0  # shorter delay for smoother video
    frames = []       # list to store frames

    temp_dir = "frames"
    os.makedirs(temp_dir, exist_ok=True)

    frame_count = 0

    while running:
        screen.blit(render_board(board), (0, 0))
        pygame.display.flip()

        # Save frame to temp file
        frame_path = os.path.join(temp_dir, f"frame_{frame_count:04d}.png")
        pygame.image.save(screen, frame_path)
        frames.append(frame_path)
        frame_count += 1

        if board.is_game_over():
            print("Game Over:", board.result())
            time.sleep(2)
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        _, move = alpha_beta(board, 3, float('-inf'), float('inf'), board.turn)
        if move:
            board.push(move)
            print(f"Move: {move.uci()[:2]} -> {move.uci()[2:]}")
            time.sleep(move_delay)

        clock.tick(30)

    pygame.quit()

    # Create video
    print("Creating video...")
    with imageio.get_writer("chess_game.mp4", fps=2) as writer:
        for filename in frames:
            image = imageio.imread(filename)
            writer.append_data(image)

    print("Video saved as chess_game.mp4")

    # Clean up frame files
    for f in frames:
        os.remove(f)
    os.rmdir(temp_dir)


if __name__ == "__main__":
    play_game()

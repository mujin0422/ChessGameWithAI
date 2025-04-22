import random
import copy
from move import Move

class AI:
    def __init__(self, board):
        self.board = board

    def evaluate_board(self):
        value_map = {
            'Pawn': 10,
            'Knight': 30,
            'Bishop': 30,
            'Rook': 50,
            'Queen': 90,
            'King': 900
        }
        score = 0
        for row in self.board.squares:
            for square in row:
                piece = square.piece
                if piece:
                    value = value_map.get(piece.__class__.__name__, 0)
                    score += value if piece.color == 'black' else -value
        return score

    def get_all_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                square = self.board.squares[row][col]
                piece = square.piece
                if piece and piece.color == color:
                    self.board.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        moves.append((piece, move))
        return moves


class AI_Minimax(AI):
    def __init__(self, board):
        super().__init__(board)

    def minimax(self, board, color, depth, alpha, beta):
        if depth == 0:
            return [self.evaluate_board(), None, None]

        maximizing = (color == 'black')
        best_value = -float('inf') if maximizing else float('inf')
        best_move = (None, None)

        moves = self.get_all_moves(color)
        random.shuffle(moves)

        for piece, move in moves:
            copied_board = copy.deepcopy(board)
            copied_board.move(piece, move, testing=True)
            next_color = 'white' if color == 'black' else 'black'
            eval_result = self.minimax(copied_board, next_color, depth - 1, alpha, beta)
            eval_score = eval_result[0]

            pos = (piece.row, piece.col) if hasattr(piece, 'row') else self.find_piece_position(piece)

            if maximizing:
                if eval_score > best_value:
                    best_value = eval_score
                    best_move = (pos, move)
                alpha = max(alpha, best_value)
            else:
                if eval_score < best_value:
                    best_value = eval_score
                    best_move = (pos, move)
                beta = min(beta, best_value)

            if beta <= alpha:
                break

        return [best_value, best_move[0], best_move[1]]

    def find_piece_position(self, piece):
        for row in range(8):
            for col in range(8):
                if self.board.squares[row][col].piece == piece:
                    return (row, col)
        return None

    def get_best_move(self, color, depth=2):
        _, pos, move = self.minimax(self.board, color, depth, -float('inf'), float('inf'))
        if pos is not None and move is not None:
            row, col = pos
            real_piece = self.board.squares[row][col].piece
            return real_piece, move
        return None

class AI_Stupid(AI):
    def __init__(self, board):
        super().__init__(board)

    def get_random_move(self, color):
        moves = self.get_all_moves(color)
        return random.choice(moves) if moves else None

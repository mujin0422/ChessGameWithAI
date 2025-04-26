import random
import copy
import time
from collections import defaultdict
from move import Move
from point_maps import get_piece_position_score

class AI:
    def __init__(self, board):
        self.board = board
        self.piece_values = {
            'Pawn': 1.0,
            'Knight': 3.2,
            'Bishop': 3.3, 
            'Rook': 5.0,
            'Queen': 9.0,
            'King': 200.0
        }

    def get_all_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col].piece
                if piece and piece.color == color:
                    self.board.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        moves.append((piece, move))
        return moves

    def get_piece_value(self, piece):
        return self.piece_values.get(piece.__class__.__name__, 0.0)

    def find_piece_position(self, piece, board):
        for row in range(8):
            for col in range(8):
                if board.squares[row][col].piece == piece:
                    return (row, col)
        return None

class AI_Minimax(AI):
    def __init__(self, board):
        super().__init__(board)
        self.time_limit = 3
        self.max_depth = 4
        self.max_nodes = 50000
        self.nodes_searched = 0
        self.start_time = 0
        self.transposition_table = {}
        self.killer_moves = defaultdict(list)
        self.move_history = []

    def evaluate_board(self):
        score = 0.0
        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col].piece
                if piece:
                    value = self.piece_values.get(piece.__class__.__name__, 0.0)
                    position_score = float(get_piece_position_score(piece)[row][col])
                    final_value = value + position_score
                    score += final_value if piece.color == 'black' else -final_value
        return score

    def get_sorted_moves(self, color, depth=0):
        moves = super().get_all_moves(color)
        scored_moves = []
        
        for piece, move in moves:
            score = 0
            target = self.board.squares[move.final.row][move.final.col].piece       
            # Score captures
            if target:
                score = 1000 + self.get_piece_value(target) - self.get_piece_value(piece)
                if self.get_piece_value(target) > self.get_piece_value(piece):
                    score += 500
            
            if getattr(move, 'is_check', False):
                score += 300
            if piece.__class__.__name__ == 'Pawn' and move.final.row in [0, 7]:
                score += 800
            
            # Score killer moves
            if (piece.square.row, piece.square.col, move.final.row, move.final.col) in self.killer_moves[depth]:
                score += 200
                
            scored_moves.append((piece, move, score))
            
        scored_moves.sort(key=lambda x: x[2], reverse=True)
        return [(p, m) for p, m, _ in scored_moves]

    def quiescence(self, alpha, beta, depth=0):
        self.nodes_searched += 1
        stand_pat = self.evaluate_board()
        
        if stand_pat >= beta: return beta
        alpha = max(alpha, stand_pat)
        
        captures = self.get_sorted_moves(self.board.next_player)
        captures = [(p,m) for p,m in captures if self.board.squares[m.final.row][m.final.col].has_piece()]
        
        for piece, move in captures[:8]:  # Only check top 8 captures
            copied_board = copy.deepcopy(self.board)
            copied_board.move(piece, move, testing=True)
            score = -self.quiescence(-beta, -alpha, depth+1)
            if score >= beta: return beta
            alpha = max(alpha, score)
            
        return alpha

    def minimax(self, depth, alpha, beta, color):
        self.nodes_searched += 1
        
        if time.time() - self.start_time > self.time_limit:
            raise TimeoutError
            
        if depth == 0:
            return self.quiescence(alpha, beta)
            
        moves = self.get_sorted_moves(color)
        best_move = None
        
        for piece, move in moves:
            copied_board = copy.deepcopy(self.board)
            copied_board.move(piece, move, testing=True)
            score = -self.minimax(depth-1, -beta, -alpha, 'white' if color == 'black' else 'black')
            
            if score >= beta:
                if not self.board.squares[move.final.row][move.final.col].has_piece():
                    self.killer_moves[depth].append((piece.square.row, piece.square.col, move.final.row, move.final.col))
                    if len(self.killer_moves[depth]) > 2:
                        self.killer_moves[depth].pop(0)
                return beta
                
            if score > alpha:
                alpha = score
                best_move = (piece, move)
                
        return alpha

    def get_best_move(self, color):
        self.start_time = time.time()
        self.nodes_searched = 0
        best_move = None
        
        try:
            for depth in range(1, self.max_depth + 1):
                alpha = float('-inf')
                beta = float('inf')
                moves = self.get_sorted_moves(color)
                for piece, move in moves:
                    copied_board = copy.deepcopy(self.board)
                    copied_board.move(piece, move, testing=True)
                    
                    score = -self.minimax(depth-1, -beta, -alpha, 'white' if color == 'black' else 'black')
                    
                    if score > alpha:
                        alpha = score
                        best_move = (piece, move)
                        
                if time.time() - self.start_time > self.time_limit * 0.8:
                    break
                    
        except TimeoutError:
            pass
            
        return best_move or self.get_fallback_move(color)

    def get_fallback_move(self, color):
        moves = self.get_all_moves(color)
        if not moves:
            return None
        captures = [(p, m) for p, m in moves if self.board.squares[m.final.row][m.final.col].has_piece()]
        if captures:
            return random.choice(captures)
        return random.choice(moves)
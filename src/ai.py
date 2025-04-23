import random
import copy
import time
from collections import defaultdict
from move import Move

class AI:
    def __init__(self, board):
        self.board = board

    def evaluate_board(self):
        # Bảng giá trị vị trí cho từng loại quân
        piece_square_tables = {
            'Pawn': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5,  5, 10, 25, 25, 10,  5,  5],
                [0,  0,  0, 20, 20,  0,  0,  0],
                [5, -5,-10,  0,  0,-10, -5,  5],
                [5, 10, 10,-20,-20, 10, 10,  5],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],
            'Knight': [
                [-50,-40,-30,-30,-30,-30,-40,-50],
                [-40,-20,  0,  0,  0,  0,-20,-40],
                [-30,  0, 10, 15, 15, 10,  0,-30],
                [-30,  5, 15, 20, 20, 15,  5,-30],
                [-30,  0, 15, 20, 20, 15,  0,-30],
                [-30,  5, 10, 15, 15, 10,  5,-30],
                [-40,-20,  0,  5,  5,  0,-20,-40],
                [-50,-40,-30,-30,-30,-30,-40,-50]
            ],
            'Bishop': [
                [-20,-10,-10,-10,-10,-10,-10,-20],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-10,  0,  5, 10, 10,  5,  0,-10],
                [-10,  5,  5, 10, 10,  5,  5,-10],
                [-10,  0, 10, 10, 10, 10,  0,-10],
                [-10, 10, 10, 10, 10, 10, 10,-10],
                [-10,  5,  0,  0,  0,  0,  5,-10],
                [-20,-10,-10,-10,-10,-10,-10,-20]
            ],
            'Rook': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [5, 10, 10, 10, 10, 10, 10,  5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [0,  0,  0,  5,  5,  0,  0,  0]
            ],
            'Queen': [
                [-20,-10,-10, -5, -5,-10,-10,-20],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-10,  0,  5,  5,  5,  5,  0,-10],
                [-5,  0,  5,  5,  5,  5,  0, -5],
                [0,  0,  5,  5,  5,  5,  0, -5],
                [-10,  5,  5,  5,  5,  5,  0,-10],
                [-10,  0,  5,  0,  0,  0,  0,-10],
                [-20,-10,-10, -5, -5,-10,-10,-20]
            ],
            'King': [
                [-30,-40,-40,-50,-50,-40,-40,-30],
                [-30,-40,-40,-50,-50,-40,-40,-30],
                [-30,-40,-40,-50,-50,-40,-40,-30],
                [-30,-40,-40,-50,-50,-40,-40,-30],
                [-20,-30,-30,-40,-40,-30,-30,-20],
                [-10,-20,-20,-20,-20,-20,-20,-10],
                [20, 20,  0,  0,  0,  0, 20, 20],
                [20, 30, 10,  0,  0, 10, 30, 20]
            ]
        }
        
        value_map = {
            'Pawn': 100,
            'Knight': 320,
            'Bishop': 330,
            'Rook': 500,
            'Queen': 900,
            'King': 20000
        }
        
        score = 0
        mobility = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col].piece
                if piece:
                    # Giá trị cơ bản
                    value = value_map.get(piece.__class__.__name__, 0)
                    # Giá trị vị trí
                    if piece.__class__.__name__ in piece_square_tables:
                        table = piece_square_tables[piece.__class__.__name__]
                        value += table[row][col] if piece.color == 'black' else table[7-row][col]
                    
                    score += value if piece.color == 'black' else -value
                    
                    # Tính toán khả năng di chuyển (mobility)
                    self.board.calc_moves(piece, row, col, bool=True)
                    mobility += len(piece.moves) * (1 if piece.color == 'black' else -1)
        
        # Thêm các yếu tố đánh giá khác
        score += mobility * 0.1  # Trọng số mobility
        
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


import time
import copy
import random
from collections import defaultdict

class AI_Minimax(AI):
    def __init__(self, board):
        super().__init__(board)
        # Cấu hình thời gian
        self.time_limit = 3  # Giới hạn 3 giây cho mỗi nước đi
        self.max_nodes = 50000  # Giới hạn số node tối đa
        
        # Cấu hình giai đoạn game
        self.endgame_threshold = 6  # Số quân tối đa để xem là endgame
        self.midgame_depth = 3  # Độ sâu midgame
        self.endgame_depth = 5   # Độ sâu endgame
        
        # Hệ thống tối ưu
        self.transposition_table = {}
        self.killer_moves = defaultdict(list)
        self.nodes_searched = 0
        self.start_time = 0

    def is_endgame(self, board):
        """Xác định có phải endgame dựa trên số quân còn lại (không tính vua)"""
        piece_count = 0
        for row in range(8):
            for col in range(8):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.__class__.__name__ not in ['King']:
                        piece_count += 1
                        if piece_count > self.endgame_threshold:
                            return False
        return True

    def get_search_depth(self, is_endgame):
        """Điều chỉnh độ sâu theo giai đoạn game"""
        return self.endgame_depth if is_endgame else self.midgame_depth

    def get_board_hash(self, board):
        """Tạo hash cho bàn cờ bao gồm cả giai đoạn game"""
        hash_str = []
        for row in board.squares:
            for square in row:
                piece = square.piece
                if piece:
                    hash_str.append(f"{piece.color[0]}{piece.__class__.__name__[0]}")
                else:
                    hash_str.append("--")
        return "|".join(hash_str) + f"|{'E' if self.is_endgame(board) else 'M'}"

    def evaluate_board(self):
        """Mở rộng phương thức evaluate_board của lớp cha"""
        score = super().evaluate_board()  # Sử dụng đánh giá cơ bản từ lớp cha
        
        # Bổ sung đánh giá endgame
        if self.is_endgame(self.board):
            for row in range(8):
                for col in range(8):
                    piece = self.board.squares[row][col].piece
                    if piece and piece.__class__.__name__ == 'King':
                        # Ưu tiên đưa vua vào trung tâm trong endgame
                        center_dist = max(abs(row-3.5), abs(col-3.5))
                        score += (4 - center_dist) * (10 if piece.color == 'black' else -10)
        
        return score

    def get_all_moves(self, color, depth=0):
        """Mở rộng phương thức get_all_moves với move ordering"""
        moves = super().get_all_moves(color)  # Lấy tất cả nước đi cơ bản
        
        # Thêm điểm số cho move ordering
        scored_moves = []
        for piece, move in moves:
            score = 0
            
            # Ưu tiên nước bắt quân
            target = self.board.squares[move.final.row][move.final.col].piece
            if target:
                score = 1000 + self.get_piece_value(target) - self.get_piece_value(piece)
            
            # Ưu tiên chiếu tướng
            elif getattr(move, 'is_check', False):
                score = 500
                
            # Killer moves
            initial_pos = self.find_piece_position(piece, self.board)
            if initial_pos and (initial_pos[0], initial_pos[1], move.final.row, move.final.col) in self.killer_moves[depth]:
                score += 400
                
            scored_moves.append((piece, move, score))
        
        # Sắp xếp theo điểm số
        scored_moves.sort(key=lambda x: x[2], reverse=True)
        return [(p, m) for p, m, _ in scored_moves]

    def get_piece_value(self, piece):
        """Lấy giá trị quân cờ từ value_map"""
        value_map = {
            'Pawn': 100,
            'Knight': 320,
            'Bishop': 330,
            'Rook': 500,
            'Queen': 900,
            'King': 20000
        }
        return value_map.get(piece.__class__.__name__, 0)

    def find_piece_position(self, piece, board):
        """Tìm vị trí quân cờ trên bàn cờ"""
        for row in range(8):
            for col in range(8):
                if board.squares[row][col].piece == piece:
                    return (row, col)
        return None

    def quiescence(self, board, color, alpha, beta, depth=0):
        """Tìm kiếm ổn định - chỉ xét nước bắt quân/chiếu"""
        self.nodes_searched += 1
        
        # Giới hạn số node và độ sâu
        if self.nodes_searched > self.max_nodes or depth > 6:
            return self.evaluate_board()
            
        stand_pat = self.evaluate_board()
        if color == 'black':
            if stand_pat >= beta:
                return beta
            alpha = max(alpha, stand_pat)
        else:
            if stand_pat <= alpha:
                return alpha
            beta = min(beta, stand_pat)

        # Chỉ xét các nước đi bắt quân hoặc chiếu
        captures = []
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col].piece
                if piece and piece.color == color:
                    board.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        target = board.squares[move.final.row][move.final.col].piece
                        if target or getattr(move, 'is_check', False):
                            score = self.get_piece_value(target) if target else 0
                            score += 50 if getattr(move, 'is_check', False) else 0
                            captures.append((piece, move, score))
        
        # Sắp xếp và giới hạn số nước đi xét
        captures.sort(key=lambda x: x[2], reverse=True)
        captures = captures[:12]  # Chỉ xét 12 nước đi tốt nhất
        
        for piece, move, _ in captures:
            copied_board = copy.deepcopy(board)
            copied_board.move(piece, move, testing=True)
            score = self.quiescence(copied_board, 'white' if color == 'black' else 'black', alpha, beta, depth+1)
            
            if color == 'black':
                if score >= beta:
                    return beta
                alpha = max(alpha, score)
            else:
                if score <= alpha:
                    return alpha
                beta = min(beta, score)
        
        return alpha if color == 'black' else beta

    def minimax(self, board, color, depth, alpha, beta, current_depth=0):
        """Thuật toán minimax với alpha-beta pruning và transposition table"""
        self.nodes_searched += 1
        
        # Kiểm tra giới hạn
        if (time.time() - self.start_time > self.time_limit or 
            self.nodes_searched > self.max_nodes):
            raise TimeoutError()
            
        board_hash = self.get_board_hash(board)
        if board_hash in self.transposition_table:
            entry = self.transposition_table[board_hash]
            if entry['depth'] >= depth:
                return entry['value']
        
        is_endgame = self.is_endgame(board)
        
        # Đến độ sâu tối đa thì chuyển sang quiescence
        if depth == 0:
            q_score = self.quiescence(board, color, alpha, beta)
            return [q_score, None, None]

        # Lấy các nước đi đã sắp xếp
        moves = self.get_all_moves(color, current_depth)
        best_move = (None, None)
        best_value = -float('inf') if color == 'black' else float('inf')

        for piece, move in moves:
            pos = self.find_piece_position(piece, board)
            if not pos:
                continue
                
            copied_board = copy.deepcopy(board)
            copied_board.move(piece, move, testing=True)
            
            eval_result = self.minimax(
                copied_board, 
                'white' if color == 'black' else 'black',
                depth - 1, 
                alpha, 
                beta,
                current_depth + 1
            )
            eval_score = eval_result[0]

            if color == 'black':
                if eval_score > best_value:
                    best_value = eval_score
                    best_move = (pos, move)
                    # Cập nhật killer move
                    if not board.squares[move.final.row][move.final.col].piece:
                        self.killer_moves[current_depth].append((
                            pos[0], pos[1], 
                            move.final.row, move.final.col
                        ))
                        if len(self.killer_moves[current_depth]) > 2:
                            self.killer_moves[current_depth].pop(0)
                alpha = max(alpha, best_value)
            else:
                if eval_score < best_value:
                    best_value = eval_score
                    best_move = (pos, move)
                beta = min(beta, best_value)

            if beta <= alpha:
                break

        # Lưu vào transposition table
        self.transposition_table[board_hash] = {
            'value': [best_value, best_move[0], best_move[1]],
            'depth': depth
        }
        
        return [best_value, best_move[0], best_move[1]]

    def get_best_move(self, color):
        """Tìm nước đi tốt nhất với iterative deepening"""
        self.start_time = time.time()
        self.nodes_searched = 0
        self.transposition_table.clear()
        best_move = None
        
        is_endgame = self.is_endgame(self.board)
        max_depth = self.get_search_depth(is_endgame)
        
        try:
            for depth in range(1, max_depth + 1):
                _, pos, move = self.minimax(
                    self.board, 
                    color, 
                    depth,
                    -float('inf'),
                    float('inf'),
                    0
                )
                if pos and move:
                    row, col = pos
                    best_move = (self.board.squares[row][col].piece, move)
                
                # Thoát sớm nếu hết thời gian hoặc tìm thấy chiếu hết
                if (time.time() - self.start_time > self.time_limit * 0.9 or
                    (best_move and getattr(best_move[1], 'is_checkmate', False))):
                    break
                    
        except TimeoutError:
            pass
            
        # Log thông tin debug
        print(f"Depth: {depth}, Nodes: {self.nodes_searched}, "
              f"Time: {time.time()-self.start_time:.2f}s, "
              f"Stage: {'Endgame' if is_endgame else 'Midgame'}")
        
        return best_move or self.get_fallback_move(color)

    def get_fallback_move(self, color):
        """Nước đi dự phòng nếu hết thời gian"""
        moves = super().get_all_moves(color)
        return random.choice(moves) if moves else None
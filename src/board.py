""" =========================(LỚP QUẢN LÝ BÀN CỜ - Board)============================
| Chịu trách nhiệm quản lý bàn cờ trong trò chơi cờ vua, bao gồm:                   |
|   1 Khởi tạo bàn cờ 8x8 ô                                                         |
|     - Tạo bàn bàn cờ 8x8 theo dạng mảng 2 chiều                                   |
|     - Tạo biến lưu trữ nước đi cưối cùng (lưu move)                               |
|     - Tạo các ô trên bàn cờ (_create())                                           |
|     - Thêm các quân cờ vào bàn tại vị trí ban đầu (_add_pieces())                 |
|   2                         
|   - Xử lý các nước đi hợp lệ của từng quân cờ.                                    |
|   - Kiểm tra các điều kiện đặc biệt như phong cấp, nhập thành, bắt tốt qua đường. |
|   - Lưu trạng thái của bàn cờ và nước đi cuối cùng.                               |
=================================================================================="""

from const import *
from pieces import *
from square import Square
from move import Move
from config import Sound
import copy
import os

class Board:
  """Khởi tạo bàn cờ với 8x8 ô và thêm các quân cờ vào vị trí ban đầu."""
  def __init__(self):
    self.squares = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    self.last_move = None
    self._create()
    self._add_pieces("white") 
    self._add_pieces("black") 


  """============== TẠO CÁC Ô TRÊN BÀN CỜ DƯỚI DẠNG Square =============== """
  def _create(self):
    for row in range(ROWS):
      for col in range(COLS):
        self.squares[row][col] = Square(row, col)

  """================ THÊM QUÂN CỜ VÀO BÀN CỜ THEO MÀU SẮC =============== """
  def _add_pieces(self,color):
    row_pawn, row_other = (6, 7) if color == "white" else (1, 0)
    # Thêm pawns(tốt)
    for col in range(COLS):
      self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
    # Thêm knight(mã) 
    self.squares[row_other][1] = Square(row_other, 1, Knight(color))
    self.squares[row_other][6] = Square(row_other, 6, Knight(color))
    # Thêm bishop(tượng)
    self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
    self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
    # Thêm rook(xe) 
    self.squares[row_other][0] = Square(row_other, 0, Rook(color))
    self.squares[row_other][7] = Square(row_other, 7, Rook(color))
    # Thêm king(vua)
    self.squares[row_other][4] = Square(row_other, 4, King(color))
  	# Thêm queen(hậu)  
    self.squares[row_other][3] = Square(row_other, 3, Queen(color))


  """ DI CHUYẺN QUÂN CỜ TỪ Ô HIỆN TẠI ĐẾN Ô ĐƯỢC CHỌN VỚI CÁC TRƯỜNG HỢP ĐẶC BIỆT """
  def move(self, piece, move, testing = False):
    initial = move.initial
    final = move.final

    en_passant_empty = self.squares[final.row][final.col].isempty() # ô điểm đến trống 
    if isinstance(piece, Pawn):
        piece.has_moved = True
    # console board move update
    self.squares[initial.row][initial.col].piece = None
    self.squares[final.row][final.col].piece = piece

    # PHONG CẤP QUÂN TỐT
    if isinstance(piece, Pawn):
      differecne = final.col - initial.col 
      if differecne != 0 and en_passant_empty:
        self.squares[initial.row][initial.col + differecne].piece = None # xóa tốt bị bắt 
        self.squares[final.row][final.col].piece = piece
        if not testing:
          sound = Sound(os.path.join('assets/sounds/capture.wav'))
          sound.play()
      # pawn
      else:
        self.promote_pawn(piece, final)

    # king castling 
    if isinstance(piece, King):
      if self.check_castling(initial, final) and not testing:
        differecne = final.col - initial.col
        rook = piece.left_rook if (differecne < 0) else piece.right_rook
        # if rook is not None and rook.moves: 
        self.move(rook, rook.moves[-1])

    piece.moved = True
    piece.clear_move()
    self.last_move = move


  """===============================================KIỂM TRA TRẠNG THÁI================================================"""
  def check_game_status(self, color):
    # Tìm Vua
    print(f"\n=== Kiem tra trang thai cho {color} ===")
    king_pos = None
    for row in range(ROWS):
        for col in range(COLS):
            piece = self.squares[row][col].piece
            if isinstance(piece, King) and piece.color == color:
                king_pos = (row, col)
                print(f"[DEBUG] Tim thay Vua tai ({row}, {col})")
                break
        if king_pos:
            break
    
    if not king_pos:
        print("[DEBUG] Không tìm thấy Vua!")
        return None

    # Kiểm tra chiếu
    in_check = False
    for row in range(ROWS):
        for col in range(COLS):
            piece = self.squares[row][col].piece
            if piece and piece.color != color:
                self.calc_moves(piece, row, col, bool=False)
                for move in piece.moves:
                    if (move.final.row, move.final.col) == king_pos:
                        print(f"[DEBUG] {piece.__class__.__name__} tại ({row}, {col}) đang chiếu Vua!")
                        in_check = True
                piece.clear_move()
                if in_check:
                    break
        if in_check:
            break

    # Kiểm tra nước đi hợp lệ
    has_legal_move = False
    for row in range(ROWS):
        for col in range(COLS):
            piece = self.squares[row][col].piece
            if piece and piece.color == color:
                self.calc_moves(piece, row, col, bool=True)
                if piece.moves:
                    print(f"[DEBUG] {piece.__class__.__name__} tai ({row}, {col}) co nuoc di hop le")
                    has_legal_move = True
                piece.clear_move()
                if has_legal_move:
                    break
        if has_legal_move:
            break

    # Xác định trạng thái
    if in_check:
        if not has_legal_move:
            print("[DEBUG] Kết quả: CHIẾU BÍ!")
            return 'checkmate'
        print("[DEBUG] Kết quả: Đang bị chiếu nhưng còn nước đi")
        return 'check'
    elif not has_legal_move:
        print("[DEBUG] Kết quả: HẾT NƯỚC ĐI (hòa)")
        return 'stalemate'
    print("[DEBUG] Ket qua: Trang thai binh thuong")
    return None
  
  """=============================================END KIỂM TRA TRẠNG THÁI============================================"""


  """===================== KIỂM TRA NƯỚC ĐI HỢP LỆ ======================="""
  def valid_move(self, piece, move):
    return move in piece.moves
  

  """===============THĂNG CẤP QUÂN TỐT KHI ĐẾN CUỐI BÀN CỜ ==============="""
  def promote_pawn(self, piece, final):
    if final.row == 0 or final.row == 7:
      self.squares[final.row][final.col].piece = Queen(piece.color)


  """======================== KIỂM TRA NHẬP THÀNH ========================"""
  def check_castling(self, initial, final):
    return abs(initial.col - final.col) == 2
  

  """============ ĐÁNH DẤU QUÂN TỐT CÓ THỂ BÁT TỐT QUA ĐƯỜNG ============="""
  def set_true_en_passant(self, piece):
    if not isinstance(piece, Pawn):
      return
    for row in range(ROWS):
      for col in range(COLS):
        if isinstance(self.squares[row][col].piece, Pawn):
          self.squares[row][col].piece.en_passant = False
    piece.en_passant = True
  

  """===== KIỂM TRA NƯỚC ĐI CÓ ĐẶT VUA VÀO TÌNH TRẠNG BỊ CHIẾU KHÔNG ===== """
  def in_check(self, piece, move):
    temp_piece = copy.deepcopy(piece)
    temp_board = copy.deepcopy(self)
    temp_board.move(temp_piece, move, testing=True)

    # Tìm vị trí vua sau nước đi
    king_pos = None
    for r in range(ROWS):
        for c in range(COLS):
            p = temp_board.squares[r][c].piece
            if isinstance(p, King) and p.color == piece.color:
                king_pos = (r, c)
                break
        if king_pos:
            break

    # Kiểm tra xem quân địch có thể tấn công vị trí vua không
    for row in range(ROWS):
        for col in range(COLS):
            if temp_board.squares[row][col].has_enemy_piece(piece.color):
                enemy_piece = temp_board.squares[row][col].piece
                temp_board.calc_moves(enemy_piece, row, col, bool=False)
                for m in enemy_piece.moves:
                    if (m.final.row, m.final.col) == king_pos:
                        return True
    return False


  """============ TÍNH TOÁN CÁC NƯỚC ĐI HỢP LỆ CẢU QUÂN CỜ =============== """
  def calc_moves(self, piece, row, col, bool = True):
    def pawn_moves():
      steps = 1 if piece.moved else 2
      possible_move_row = row + piece.dir
      if Square.in_range(possible_move_row) and self.squares[possible_move_row][col].isempty():
        initial = Square(row, col)
        final = Square(possible_move_row, col)
        move = Move(initial, final)
        if bool:
            if not self.in_check(piece, move):
                piece.add_move(move)
        else:
            piece.add_move(move)

    # Bước đi đầu tiên (2 ô) - kiểm tra bằng vị trí ban đầu
      if (piece.color == "white" and row == 6) or (piece.color == "black" and row == 1):
        possible_move_row = row + (piece.dir * 2)
        intermediate_row = row + piece.dir
        if (Square.in_range(possible_move_row) and 
            self.squares[possible_move_row][col].isempty() and
            self.squares[intermediate_row][col].isempty()):
            initial = Square(row, col)
            final = Square(possible_move_row, col)
            move = Move(initial, final)
            if bool:
                if not self.in_check(piece, move):
                    piece.add_move(move)
            else: piece.add_move(move)
      # diagonal moves
      possible_move_row = row + piece.dir
      possible_move_cols = [col-1, col+1]
      for possible_move_col in possible_move_cols:
        if Square.in_range(possible_move_row, possible_move_col):
          if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
            # create initial and final move squares
            initial = Square(row, col)
            final_piece = self.squares[possible_move_row][possible_move_col].piece
            final= Square(possible_move_row, possible_move_col, final_piece)
            # create a new move
            move = Move(initial,final)
            # check potencial checks
            if bool:
              if not self.in_check(piece, move):
                #append new move
                piece.add_move(move)
            else:
              #append new move
              piece.add_move(move)


      # en passant moves
      r = 3 if piece.color == "white" else 4
      fr = 2 if piece.color == "white" else 5
      if Square.in_range(col - 1) and row == r:
        if self.squares[row][col-1].has_enemy_piece(piece.color):
          p = self.squares[row][col-1].piece
          if isinstance(p, Pawn):
            if p.en_passant:
              # create initial and final move squares
              initial = Square(row, col)
              final= Square(fr, col - 1, p)
              # create a new move
              move = Move(initial,final)
              # check potencial checks
              if bool:
                if not self.in_check(piece, move):
                  #append new move
                  piece.add_move(move)
              else:
                #append new move
                piece.add_move(move)

      if Square.in_range(col+1) and row == r:
        if self.squares[row][col+1].has_enemy_piece(piece.color):
          p = self.squares[row][col+1].piece
          if isinstance(p, Pawn):
            if p.en_passant:
              # create initial and final move squares
              initial = Square(row, col)
              final= Square(fr, col+1, p)
              # create a new move
              move = Move(initial,final)
              # check potencial checks
              if bool:
                if not self.in_check(piece, move):
                  #append new move
                  piece.add_move(move)
              else:
                #append new move
                piece.add_move(move)

    def knight_moves():
      # 8 possive moves
      possible_moves = [
        (row-2, col+1),
        (row-1, col+2),
        (row+1, col+2),
        (row+2, col+1),
        (row+2, col-1),
        (row+1, col-2),
        (row-1, col-2),
        (row-2, col-1),
      ]

      for possible_move in possible_moves:
        possible_move_row, possible_move_col = possible_move
        if Square.in_range(possible_move_row, possible_move_col):
          if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
            #create squares of new move
            initial = Square(row, col)
            final_piece = self.squares[possible_move_row][possible_move_col].piece
            final= Square(possible_move_row, possible_move_col, final_piece)
            # create a new move
            move = Move(initial, final)
            # append new valid move
            if bool:
              if not self.in_check(piece, move):
                #append new move
                piece.add_move(move)
              else: 
                break
            else:
              #append new move
              piece.add_move(move)
      
    def straightlinr_moves(incrs):
      for incr in incrs:
        row_incr, col_incr = incr
        possible_move_row = row + row_incr
        possible_move_col = col + col_incr

        while True:
          if Square.in_range(possible_move_row, possible_move_col):
            #create squares of new move
            initial = Square(row, col)
            final_piece = self.squares[possible_move_row][possible_move_col].piece
            final= Square(possible_move_row, possible_move_col, final_piece)
            # create a new move
            move = Move(initial, final)

            # empty = countinue looping
            if self.squares[possible_move_row][possible_move_col].isempty():
              if bool:
                if not self.in_check(piece, move):
                  #append new move
                  piece.add_move(move)
              else:
                #append new move
                piece.add_move(move)

            # has enemy piece = add_move + break
            elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
              if bool:
                if not self.in_check(piece, move):
                  #append new move
                  piece.add_move(move)
              else:
                #append new move
                piece.add_move(move)
              break

            # has team piece = break 
            elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
              break

          else: break

          possible_move_row = possible_move_row + row_incr
          possible_move_col = possible_move_col + col_incr

    def king_moves():
      # Các ô xung quanh vua
      adjs = [
          (row - 1, col), (row - 1, col + 1),
          (row,     col + 1), (row + 1, col + 1),
          (row + 1, col), (row + 1, col - 1),
          (row,     col - 1), (row - 1, col - 1)
      ]

      # Các nước đi thông thường
      for r, c in adjs:
          if Square.in_range(r, c):
              if self.squares[r][c].isempty_or_enemy(piece.color):
                  initial = Square(row, col)
                  final = Square(r, c)
                  move = Move(initial, final)

                  if bool:
                      if not self.in_check(piece, move):
                          piece.add_move(move)
                  else:
                      piece.add_move(move)

      # Kiểm tra castling nếu vua chưa di chuyển
      if not piece.moved:
          # Queen-side castling (bên trái)
          left_rook = self.squares[row][0].piece
          if isinstance(left_rook, Rook) and not left_rook.moved:
              if all(not self.squares[row][c].has_piece() for c in range(1, 4)):
                  moveK = Move(Square(row, col), Square(row, 2))
                  moveR = Move(Square(row, 0), Square(row, 3))

                  if bool:
                      if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                          piece.left_rook = left_rook
                          piece.add_move(moveK)
                          left_rook.add_move(moveR)
                  else:
                      piece.left_rook = left_rook
                      piece.add_move(moveK)
                      left_rook.add_move(moveR)

          # King-side castling (bên phải)
          right_rook = self.squares[row][7].piece
          if isinstance(right_rook, Rook) and not right_rook.moved:
              if all(not self.squares[row][c].has_piece() for c in range(5, 7)):
                  moveK = Move(Square(row, col), Square(row, 6))
                  moveR = Move(Square(row, 7), Square(row, 5))

                  if bool:
                      if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                          piece.right_rook = right_rook
                          piece.add_move(moveK)
                          right_rook.add_move(moveR)
                  else:
                      piece.right_rook = right_rook
                      piece.add_move(moveK)
                      right_rook.add_move(moveR)

    if isinstance(piece ,Pawn): 
      pawn_moves()
      
    elif isinstance(piece, Knight): 
      knight_moves()

    elif isinstance(piece, Bishop): 
      straightlinr_moves([
        (-1, 1), # up-right
        (-1, -1), # up-left
        (1, 1), # down-right
        (1, -1) # down-left
      ])

    elif isinstance(piece,Rook): 
      straightlinr_moves([
        (-1, 0), # up
        (0 ,1), # right
        (1, 0), # down
        (0, -1) # left
      ])

    elif isinstance(piece, Queen): 
      straightlinr_moves([
        (-1, 1),
        (-1, -1),
        (1, 1),
        (1, -1),
        (-1, 0),
        (0 ,1),
        (1, 0),
        (0, -1)
      ])

    elif isinstance(piece,King): 
      king_moves()
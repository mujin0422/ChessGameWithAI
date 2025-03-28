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
    temp_board.move(temp_piece, move, testing = True)

    for row in range(ROWS):
      for col in range(COLS):
        if temp_board.squares[row][col].has_enemy_piece(piece.color):
          p = temp_board.squares[row][col].piece
          temp_board.calc_moves(p, row, col, bool = False)
          for m in p.moves:
            if isinstance(m.final.piece, King):
              return True
    return False


  """============ TÍNH TOÁN CÁC NƯỚC ĐI HỢP LỆ CẢU QUÂN CỜ =============== """
  def calc_moves(self, piece, row, col, bool = True):
    
    def pawn_moves():
      steps = 1 if piece.moved else 2
      # vertical moves
      start = row + piece.dir
      end = row + (piece.dir * (1 + steps))
      for possible_move_row in range(start, end, piece.dir):
        if Square.in_range(possible_move_row):
          if self.squares[possible_move_row][col].isempty():
            # create initial and final move squares
            initial = Square(row, col)
            final= Square(possible_move_row, col)
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
          else: break
        else: break
      
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
      adjs = [
        (row - 1, col + 0),
        (row - 1, col + 1),
        (row + 0, col + 1),
        (row + 1, col + 1),
        (row + 1, col + 0),
        (row + 1, col - 1),
        (row + 0, col - 1),
        (row - 1, col - 1)
      ]

      # normal moves
      for possible_move in adjs:
        possible_move_row, possible_move_col = possible_move
        if Square.in_range(possible_move_row, possible_move_col):
          if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
            #create squares of new move
            initial = Square(row, col)
            final = Square(possible_move_row, possible_move_col) # piece = piece
            # create a new move
            move = Move(initial, final)
            # check potencial checks
            if bool:
              if not self.in_check(piece, move):
                #append new move
                piece.add_move(move)
              else: break
            else:
              #append new move
              piece.add_move(move)

      # castling moves
      if not piece.moved:
        # queen castling
        left_rook = self.squares[row][0].piece
        if isinstance(left_rook, Rook):
          if not left_rook.moved:
            for c in range(1, 4):
              # castling is not possible (has pieces betwwen)
              if self.squares[row][c].has_piece(): 
                break
              if c == 3:
                # add left rook to king 
                piece.left_rook = left_rook
                # rook move
                initial = Square(row, 0)
                final = Square(row, 3)
                moveR = Move(initial, final)
               
                # king move
                initial = Square(row, col)
                final = Square(row, 2)
                moveK = Move(initial, final)
            
                # check potencial checks
                if bool:
                  if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                    # append new move to rook
                    left_rook.add_move(moveR)
                    # append new move to king
                    piece.add_move(moveK)
                  else: break
                else:
                  # append new move to rook
                  left_rook.add_move(moveR)
                  # append new move to king
                  piece.add_move(moveK)

        # king castling
        right_rook = self.squares[row][7].piece
        if isinstance(right_rook, Rook):
          if not right_rook.moved:
            for c in range(5, 7):
              # castling is not possible (has pieces betwwen)
              if self.squares[row][c].has_piece(): 
                break
              if c == 6:
                # add right rook to king 
                piece.right_rook = right_rook
                # rook move
                initial = Square(row, 7)
                final = Square(row, 5)
                moveR = Move(initial, final)

                # king move
                initial = Square(row, col)
                final = Square(row, 6)
                moveK = Move(initial, final)


                # check potencial checks
                if bool:
                  if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                    # append new move to rook
                    right_rook.add_move(moveR)
                    # append new move to king
                    piece.add_move(moveK)
                  else: break
                else:
                  # append new move to rook
                  right_rook.add_move(moveR)
                  # append new move to king
                  piece.add_move(moveK)

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
  
  





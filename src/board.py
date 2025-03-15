""" QUẢN LÍ BÀN CỜ 
- Tạo bàn cờ 8x8
- Thêm quân cờ vào bàn tại đúng vị trí ban đầu 
- Lưu trạng thái của bàn cờ (quân nào đang ở đâu)
"""

from const import *
from square import Square
from pieces import *
from move import Move
from sound import Sound
import copy
import os

class Board:

  def __init__(self):
    # Khởi tạo bàn cờ với 8x8 ô, mỗi ô ban đầu có giá trị 0 (chưa có quân cờ)
    self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]    

    self.last_move= None
    # Tạo các ô trên bàn cờ
    self._create()
    # Thêm quân cờ trắng vào bàn cờ
    self._add_pieces("white")
    # Thêm quân cờ đen vào bàn cờ
    self._add_pieces("black")

  def move(self, piece, move, testing = False):
    initial = move.initial
    final = move.final

    en_passant_empty = self.squares[final.row][final.col].isempty()
    # console board move update
    self.squares[initial.row][initial.col].piece = None
    self.squares[final.row][final.col].piece = piece

    # pawn promotion 
    if isinstance(piece, Pawn):
      # pawn en passant capture
      diff = final.col - initial.col
      if diff != 0 and en_passant_empty:
        self.squares[initial.row][initial.col + diff].piece = None
        self.squares[final.row][final.col].piece = piece
        if not testing:
          sound = Sound(os.path.join('assets/sounds/capture.wav'))
          sound.play()
      # paww
      else:
        self.check_promotion(piece, final)

    # king castling 
    if isinstance(piece, King):
      if self.castling(initial, final) and not testing:
        diff = final.col - initial.col
        rook = piece.left_rook if (diff < 0) else piece.right_rook
        # if rook is not None and rook.moves: 
        self.move(rook, rook.moves[-1])

    # move
    piece.moved = True
    # clear valid moves
    piece.clear_move()
    # set last move
    self.last_move = move


  """ KIỂM TRA NƯỚC ĐI HỢP LỆLỆ"""
  def valid_move(self, piece, move):
    return move in piece.moves
  
  """ KIỂM TRA THĂNG CẤP QUÂN TỐT KHI ĐẾN CUỐI BÀN CỜ """
  def check_promotion(self, piece, final):
    if final.row == 0 or final.row == 7:
      self.squares[final.row][final.col].piece = Queen(piece.color)

  """ KIỂM TRA NHẬP THÀNH """
  def castling(self, initial, final):
    return abs(initial.col - final.col) == 2
  
  def set_true_en_passant(self, piece):
    if not isinstance(piece, Pawn):
      return
    for row in range(ROWS):
      for col in range(COLS):
        if isinstance(self.squares[row][col].piece, Pawn):
          self.squares[row][col].piece.en_passant = False
    piece.en_passant = True
  
  """ KIỂM TRA NƯỚC ĐI CÓ ĐẶT VUA VÀO TÌNH TRẠNG BỊ CHIẾU KHÔNG """
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

  
  def calc_moves(self, piece, row, col, bool = True):
    """ calcuate all the possible valid moves """
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

  def _create(self):
    """Tạo các ô trên bàn cờ dưới dạng đối tượng Square."""
    for row in range(ROWS):
      for col in range(COLS):
        self.squares[row][col] = Square(row, col)

  def _add_pieces(self,color):
    """Thêm quân cờ vào bàn cờ theo màu sắc (trắng hoặc đen)."""
    if color == "white":
      row_pawn, row_other = (6, 7) # Quân tốt ở hàng 6, các quân khác ở hàng 7
    else:
      row_pawn, row_other = (1, 0) # Quân tốt ở hàng 1, các quân khác ở hàng 0

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





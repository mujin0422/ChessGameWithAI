from const import *

class Selector:
    def __init__(self):
        self.piece = None             # Quân cờ đang được chọn
        self.selecting = False        # Đang trong trạng thái đã chọn quân cờ
        self.initial_row = None       # Vị trí ban đầu (nơi quân cờ được chọn)
        self.initial_col = None

    def save_initial(self, row, col):
        self.initial_row = row
        self.initial_col = col

    def select_piece(self, piece, rowcol): 
      self.selecting = True
      self.piece = piece
      self.rowcol = rowcol

    def unselect_piece(self):
        self.piece = None
        self.selecting = False
        self.initial_row = None
        self.initial_col = None

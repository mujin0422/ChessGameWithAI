""" ĐỊNH NGHĨA Ô CỜ 
- Đại diện cho một ô trên bàn cờ.
- Kiểm tra xem ô có chứa quân cờ không
- XXác định mối quan hệ giữa các quân cờờ
"""

class Square:

  ALPHACOLS = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}

  """ KHỞI TẠO MỘT Ô CỜ VỚI : HÀNG(row), CỘT(col), QUÂN CỜ(piece-nếu có) """
  def __init__(self, row, col, piece = None):
    self.row = row
    self.col = col 
    self.piece = piece
    self.alphacol = self.ALPHACOLS[col]

  """So sánh hai ô cờ dựa trên vị trí hàng và cột."""
  def __eq__(self, other):
    return self.row == other.row and self.col == other.col

  """Kiểm tra xem ô cờ có chứa quân cờ hay không."""
  def has_piece(self):
    return self.piece != None
  
  """Kiểm tra xem ô cờ có trống không."""
  def isempty(self):
    return not self.has_piece()
  
  """Kiểm tra xem ô có chứa quân cờ của cùng một đội (màu) hay không."""
  def has_team_piece(self, color):
    return self.has_piece() and self.piece.color == color

  """Kiểm tra xem ô có chứa quân cờ của đối thủ hay không."""
  def has_enemy_piece(self, color):
    return self.has_piece() and self.piece.color != color

  """Kiểm tra xem ô có trống hoặc chứa quân cờ của đối thủ hay không."""
  def isempty_or_enemy(self, color):
    return self.isempty() or self.has_enemy_piece(color)

  """Kiểm tra xem các giá trị hàng, cột có nằm trong phạm vi hợp lệ (0-7) hay không."""
  @staticmethod
  def in_range(*args):
    for arg in args:
      if arg < 0 or arg > 7:
        return False
    return True
  
  """Trả về ký tự chữ cái tương ứng với số cột (A-H)."""
  @staticmethod
  def get_alphacol(col):
    ALPHACOLS = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}
    return ALPHACOLS[col]
  
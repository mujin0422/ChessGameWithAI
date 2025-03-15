""" ĐỊNH NGĨA CÁC QUÂN CỜ 
- Chứa các class đại diện cho từng quân cờ 
- Định nghĩa hình ảnh, màu sắc, cách di chuyển của các quân cờ
"""
import os

class Piece:
  """ Lớp cha của các quân cờ """
  def __init__(self, name, color, value, texture = None, texture_rect = None):
    """ Khởi tạo một quân cờ.
    :param name: Tên quân cờ (pawn, knight, bishop, rook, queen, king).
    :param color: Màu quân cờ ("white" hoặc "black").
    :param value: Giá trị điểm số của quân cờ.
    :param texture: Đường dẫn hình ảnh quân cờ.
    :param texture_rect: Vị trí và kích thước hình ảnh trên màn hình.
    """
    self.name = name
    self.color = color

    # khi huan luyen AI quan den se co gia tri am, quan trang co gia tri duong 
    value_sign = 1 if color == "white" else -1
    self.value = value * value_sign

    self.moves = [] # Danh sách các nước đi hợp lệ 
    self.moved = False # Kiểm tra quân cờ đã di chuyển chưa 

    self.set_texture() # Gán đường dẫn hình ảnh cho các quâ cờ 
    self.texture_rect  = texture_rect # Lưu vị trí hình ảnh trên màn hình


  def set_texture(self, size = 80):
    """ Thiết lập đường dẫn ảnh của quân cờ dựa trên tên, màu sắc """
    self.texture = os.path.join(
      f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
    )

  def add_move(self, move):
    """ Thêm một nước đi hợp lệ vào danh sách moves """
    self.moves.append(move)

  def clear_move(self):
    self.moves = []

class Pawn(Piece):
  """ Khởi tạo quân tốt với màu sắc và giá trị 1.0.
  - Trắng đi lên (hướng -1)
  - Đen đi xuống (hướng +1)
  """
  def __init__(self, color):
    if color == "white":
      self.dir = -1
    else: 
      self.dir = 1
    self.en_passant = False
    super().__init__("pawn", color, 1.0)


class Knight(Piece):
  """ Khởi tạo quân mã với giá trị 3.0. """
  def __init__(self, color):
    super().__init__("knight", color, 3.0)


class Bishop(Piece):
  """ Khởi tạo quân tượng với giá trị 3.0. """
  def __init__(self, color):
    super().__init__("bishop", color, 3.0)


class Rook(Piece):
  """ Khởi tạo quân xe với giá trị 5.0. """
  def __init__(self, color):
    super().__init__("rook", color, 5.0)


class Queen(Piece):
  """ Khởi tạo quân hậu với giá trị 9.0. """
  def __init__(self, color):
    super().__init__("queen", color, 9.0)


class King(Piece):
  """ Khởi tạo quân vua với giá trị 1000.0 (vô giá). """
  def __init__(self, color):
    self.left_rook = None
    self.right_rook = None
    super().__init__("king", color, 1000.0)


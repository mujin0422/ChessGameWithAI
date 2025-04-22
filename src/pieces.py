""" ========================== LỚP QUẢN LÝ QUÂN CỜ - Piece ===========================
|   1 Khởi tạo các quân cờ                                                      |
|     - Tạo bàn cờ (_create())                                                       |
|     - Thêm các quân cờ vào bàn tại vị trí ban đầu (_add_pieces())                  |
                             |
|   - Xử lý các nước đi hợp lệ của từng quân cờ.                                     |
|   - Kiểm tra các điều kiện đặc biệt như phong cấp, nhập thành, bắt tốt qua đường.  |
|   - Lưu trạng thái của bàn cờ và nước đi cuối cùng.                                |
==================================================================================="""
import os


""" LỚP (Piece): lớp cha của các quân cờ  """
class Piece:
  
  def __init__(self, name, color, value, texture = None, texture_rect = None):
    self.name = name
    self.color = color
    # khi huan luyen AI quan den se co gia tri am, quan trang co gia tri duong 
    value_sign = 1 if color == "white" else -1
    self.value = value * value_sign
    self.moves = [] # Danh sách các nước đi hợp lệ 
    self.moved = False # Kiểm tra quân cờ đã di chuyển chưa 
    self.set_texture() # Gán đường dẫn hình ảnh cho các quâ cờ 
    self.texture_rect  = texture_rect # Lưu vị trí hình ảnh trên màn hình


  """============== THIẾT LẬP HÌNH ẢNH QUÂN CỜ THEO MÀU VÀ TÊN =============="""
  def set_texture(self, size = 80):
    self.texture = os.path.join(
      f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
    )

  """======= THÊM MỘT BƯỚC ĐI HỢP LỆ VÀO DANH SÁCH CÁC BƯỚC ĐI HỌP LỆ ======="""
  def add_move(self, move):
    self.moves.append(move)

  """============ LÀM MỚI DANH SÁCH CÁC BƯỚC ĐI HỢP LỆ VỀ RỖNG =============="""
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


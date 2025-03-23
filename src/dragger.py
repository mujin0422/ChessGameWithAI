import pygame
from const import *

class Dragger:
  
  def __init__(self):
    self.piece = None  # Quân cờ hiện tại đang được kéo
    self.dragging = False  # Trạng thái kéo (True nếu đang kéo, False nếu không)
    self.mouseX = 0  # Tọa độ X của chuột
    self.mouseY = 0  # Tọa độ Y của chuột
    self.initial_row = 0  # Hàng ban đầu của quân cờ trước khi kéo
    self.initial_col = 0  # Cột ban đầu của quân cờ trước khi kéo

  """Cập nhật và vẽ quân cờ theo vị trí chuột khi đang kéo."""
  def update_blit(self, surface):
    self.piece.set_texture(size = 80)
    texture = self.piece.texture

    img = pygame.image.load(texture)
    img_center = (self.mouseX, self.mouseY)
    self.piece.texture_rect = img.get_rect(center = img_center)

    surface.blit(img, self.piece.texture_rect)


  def update_mouse(self, pos):
    self.mouseX, self.mouseY = pos #{xcor, ycor}MAN


  def save_initial(self, pos):
    self.initial_col = (pos[0] - BOARD_X) // SQSIZE
    self.initial_row = (pos[1] - BOARD_Y) // SQSIZE


  def drag_piece(self, piece):
    self.piece = piece
    self.dragging = True


  def undrag_piece(self):
    self.piece = None
    self.dragging = False
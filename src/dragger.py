import pygame
from const import *

class Dragger:
  
  def __init__(self):
    self.piece = None
    self.dragging = False
    self.mouseX = 0
    self.mouseY = 0
    self.initial_row = 0
    self.initial_col = 0


  def update_blit(self, surface):
    self.piece.set_texture(size = 80)
    texture = self.piece.texture

    img = pygame.image.load(texture)

    img_center = (self.mouseX, self.mouseY)
    self.piece.texture_rect = img.get_rect(center = img_center)

    surface.blit(img, self.piece.texture_rect)



  def update_mouse(self, pos):
    self.mouseX, self.mouseY = pos #{xcor, ycor}


  def save_initial(self, pos):
    self.initial_col = (pos[0] - BOARD_X) // SQSIZE
    self.initial_row = (pos[1] - BOARD_Y) // SQSIZE


  def drag_piece(self, piece):
    self.piece = piece
    self.dragging = True


  def undrag_piece(self):
    self.piece = None
    self.dragging = False
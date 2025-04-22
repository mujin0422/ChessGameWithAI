""" QUẢN LÍ LUẬT CHƠI (NƯỚC ĐI) VÀ HIỂN THỊ ĐỒ HỌA
- Hiển thị bàn cờ (show_bg) và quân cờ (show_pieces) 
- Xử lí luật chơi và tương tác với người chơi """
import pygame
from const import *
from board import Board
from config import Config
from square import Square
from selector import Selector

class Game:
  def __init__(self):
    """ Khởi tạo trò chơi với một bàn cờ. """
    self.next_player = "white"
    self.hovered_sqr = None
    self.board = Board()
    self.config = Config()
    self.selector = Selector()
    self.game_over = False  # Thêm trạng thái kết thúc game
    self.winner = None      # Lưu màu người thắng ('white'/'black')
    self.result = None      # Lưu kết quả ('checkmate'/'stalemate')

  
  def show_bg(self, surface):
    theme = self.config.theme
    """ Hiển thị nền bàn cờ với hai màu ô xen kẽ."""
    for row in range(ROWS):
      for col in range(COLS):
        # Xác định màu sắc ô dựa trên vị trí của nó (ô sáng hoặc tối)
        color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
        # Xác định hình chữ nhật tương ứng với ô cờ
        rect = (col * SQSIZE + BOARD_X, row * SQSIZE + BOARD_Y, SQSIZE, SQSIZE)
        # Vẽ ô cờ lên màn hình
        pygame.draw.rect(surface, color, rect)

        # Hiển thị số hàng (1-8) bên trái bàn cờ
        if col == 0:
          color = theme.bg.dark if row % 2 == 0 else theme.bg.light
          lbl = self.config.font.render(str(ROWS - row), 1, color)
          lbl_x = BOARD_X - 20  # Đẩy số ra ngoài bàn cờ
          lbl_y = BOARD_Y + row * SQSIZE + (SQSIZE - lbl.get_height()) // 2
          surface.blit(lbl, (lbl_x, lbl_y))

        # Hiển thị chữ cái cột (A-H) ở hàng dưới cùng
        if row == 7:
          color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
          lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
          lbl_x = BOARD_X + col * SQSIZE + (SQSIZE - lbl.get_width()) // 2
          lbl_y = BOARD_Y + ROWS * SQSIZE + 5  # Đẩy chữ xuống dưới bàn cờ
          surface.blit(lbl, (lbl_x, lbl_y))


  
  """ Hiển thị tất cả quân cờ lên bàn cờ (trừ quân đang được chọn)."""
  def show_pieces(self, surface):
    for row in range(ROWS):
        for col in range(COLS):
            square = self.board.squares[row][col]
            if square.has_piece():
                piece = square.piece

                if self.selector.selecting and piece == self.selector.piece:
                    continue

                piece.set_texture(size=80)
                img = pygame.image.load(piece.texture)
                img = pygame.transform.scale(img, (80, 160))

                img_width, img_height = img.get_size()
                img_x = col * SQSIZE + BOARD_X + (SQSIZE - img_width) // 2
                img_y = row * SQSIZE + BOARD_Y + (SQSIZE - img_height - 128 + 48) // 2
                piece.texture_rect = pygame.Rect(img_x, img_y, img_width, img_height)

                surface.blit(img, piece.texture_rect)
    # THÊM CÁI NÀY VÀO NÈ TIẾN ++++++++++++++++++++++++++++++++
    if self.selector.selecting and self.selector.piece:
      piece = self.selector.piece
      
      for row in range(ROWS):
          for col in range(COLS):
              if self.board.squares[row][col].piece == piece:
                  piece.set_texture(size=80)
                  img = pygame.image.load(piece.texture)
                  img = pygame.transform.scale(img, (80, 160))

                  img_width, img_height = img.get_size()
                  img_x = col * SQSIZE + BOARD_X + (SQSIZE - img_width) // 2
                  img_y = row * SQSIZE + BOARD_Y + (SQSIZE - img_height - 128 + 48) // 2
                  piece.texture_rect = pygame.Rect(img_x, img_y, img_width, img_height)

                  surface.blit(img, piece.texture_rect)
                  break 

  """ Hiển thị nước đi hợp lệ của quân cờ đang được chọn. """
  def show_moves(self, surface):
    theme = self.config.theme
    if self.selector.selecting:
        piece = self.selector.piece

        for move in piece.moves:
            # Chọn màu nền cho nước đi (tuỳ theo màu ô bàn cờ)
            color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
            rect = ( move.final.col * SQSIZE + BOARD_X, move.final.row * SQSIZE + BOARD_Y, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect)


  """ Hiển thị nước đi cuối cùng (tức là quân cờ vừa đi: vị trí bắt đầu và vị trí hiện tạitại) """
  def show_last_move(self, surface):
    theme = self.config.theme
    if self.board.last_move:
      initial = self.board.last_move.initial
      final = self.board.last_move.final

      for pos in [initial, final]:
        color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
        rect = (pos.col * SQSIZE + BOARD_X, pos.row * SQSIZE + BOARD_Y, SQSIZE, SQSIZE)
        pygame.draw.rect(surface, color, rect)


  """ Hiển thị viền ô cờ khi di chuột qua. """
  def show_hover(self, surface):
    if self.hovered_sqr:
      color = (180, 180, 180) 
      rect = (self.hovered_sqr.col * SQSIZE + BOARD_X, self.hovered_sqr.row * SQSIZE + BOARD_Y, SQSIZE, SQSIZE)
      pygame.draw.rect(surface, color, rect, width = 3)

  def next_turn(self):
    self.next_player = "white" if self.next_player == "black" else "black"

  def set_hover(self, row, col):
    if 0 <= row < ROWS and 0 <= col < COLS:
      self.hovered_sqr = self.board.squares[row][col]
    else:
      self.hovered_sqr = None

  def change_theme(self):
    self.config.change_theme()

  def play_sound(self, capture = False):
    if capture:
      self.config.capture_sound.play()
    else:
      self.config.move_sound.play()

  def reset(self):
    self.__init__()
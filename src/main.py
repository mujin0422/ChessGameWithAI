""" CHẠY GAME
- Tạo cửa sổ game, vòng lặp game, xử lí các sự kiện
- Gọi các hàm hiển thị bàn cờ và quân cờ
"""
import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('CHESS GAME')
    self.game = Game()
  
  def mainLoop(self):
    game = self.game
    screen = self.screen
    board = self.game.board
    dragger = self.game.dragger

    while True:
      screen.fill((0, 0, 0))

      game.show_bg(screen)
      game.show_last_move(screen)
      game.show_moves(screen)
      game.show_hover(screen)
      game.show_pieces(screen)


      if dragger.dragging:
        dragger.update_blit(screen)


      for event in pygame.event.get():

        #click
        if event.type == pygame.MOUSEBUTTONDOWN:
          dragger.update_mouse(event.pos)
          
          clicked_col = (dragger.mouseX - BOARD_X) // SQSIZE
          clicked_row = (dragger.mouseY - BOARD_Y) // SQSIZE

          # Kiểm tra xem tọa độ có nằm trong phạm vi bàn cờ không
          if 0 <= clicked_row < ROWS and 0 <= clicked_col < COLS:

            #if cliced sqaure has a piece
            if board.squares[clicked_row][clicked_col].has_piece():
              piece = board.squares[clicked_row][clicked_col].piece
              # valid piece color
              if piece.color == game.next_player:
                board.calc_moves(piece, clicked_row, clicked_col, bool = True)
                dragger.save_initial(event.pos)
                dragger.drag_piece(piece)
                  
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)

        #mouse motion
        elif event.type == pygame.MOUSEMOTION:
          motion_row =(event.pos[1] - BOARD_Y) // SQSIZE
          motion_col =(event.pos[0] - BOARD_X) // SQSIZE
          game.set_hover(motion_row, motion_col)

          if dragger.dragging:
            dragger.update_mouse(event.pos)
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_hover(screen)
            game.show_pieces(screen)

            dragger.update_blit(screen)

        #click release
        elif event.type == pygame.MOUSEBUTTONUP:
          if dragger.dragging:
            dragger.update_mouse(event.pos)
            released_row = (dragger.mouseY - BOARD_Y) // SQSIZE
            released_col = (dragger.mouseX - BOARD_X) // SQSIZE

            initial = Square(dragger.initial_row, dragger.initial_col)
            final = Square(released_row, released_col)
            move = Move(initial, final)

            # valid move right
            if board.valid_move(dragger.piece, move):
              captured = board.squares[released_row][released_col].has_piece()

              board.move(dragger.piece, move)
              board.set_true_en_passant(dragger.piece)

              game.play_sound(captured)
              game.show_bg(screen)
              game.show_last_move(screen)
              game.show_pieces(screen)

              game.next_turn()

          dragger.undrag_piece()

        # key press
        elif event.type == pygame.KEYDOWN:
          # change themes
          if event.key == pygame.K_t:
            game.change_theme()

          if event.key == pygame.K_r:
            game.reset()
            game = self.game
            board = self.game.board
            dragger = self.game.dragger

        # quit game
        elif event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()


      pygame.display.update()



main = Main()
main.mainLoop()






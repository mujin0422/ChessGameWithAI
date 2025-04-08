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
    board = game.board
    selector = game.selector

    while True:
        screen.fill((0, 0, 0))

        # Vẽ các thành phần
        game.show_bg(screen)
        game.show_last_move(screen)
        game.show_moves(screen)
        game.show_hover(screen)
        game.show_pieces(screen)

        # Vòng xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_col = (mouseX - BOARD_X) // SQSIZE
                clicked_row = (mouseY - BOARD_Y) // SQSIZE

                if 0 <= clicked_row < ROWS and 0 <= clicked_col < COLS:
                    clicked_square = board.squares[clicked_row][clicked_col]

                    # Đã chọn quân cờ từ trước
                    if selector.selecting:
                        selected_piece = selector.piece
                        start_row, start_col = selector.rowcol
                        move = Move(Square(start_row, start_col), Square(clicked_row, clicked_col))

                        if board.valid_move(selected_piece, move):
                            captured = clicked_square.has_piece()
                            board.move(selected_piece, move)
                            board.set_true_en_passant(selected_piece)

                            game.play_sound(captured)
                            game.next_turn()

                        # Hủy chọn dù có đi hay không
                        selector.unselect_piece()

                    else:
                        # Nếu click vào quân cờ đúng lượt
                        if clicked_square.has_piece():
                            piece = clicked_square.piece
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, True)
                                selector.select_piece(piece, (clicked_row, clicked_col))

            elif event.type == pygame.MOUSEMOTION:
                hover_row = (event.pos[1] - BOARD_Y) // SQSIZE
                hover_col = (event.pos[0] - BOARD_X) // SQSIZE
                game.set_hover(hover_row, hover_col)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    game.change_theme()

                elif event.key == pygame.K_r:
                    game.reset()
                    game = self.game
                    board = game.board
                    selector = game.selector

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()



main = Main()
main.mainLoop()






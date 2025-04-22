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

                            """=============KIỂM TRA THĂNG THUA============="""
                            for color in ['white', 'black']:
                                status = board.check_game_status(color)
                                if status == 'checkmate':
                                    game.game_over = True
                                    game.winner = 'black' if color == 'white' else 'white'
                                    game.result = 'checkmate'
                                    break
                                elif status == 'stalemate':
                                    game.game_over = True
                                    game.result = 'stalemate'
                                    break
                            """==========end KIỂM TRA THĂNG THUA============"""

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
                    # Reset trạng thái kết thúc của lớp GAME
                    game.game_over = False  
                    game.winner = None
                    game.result = None
                    # Cập nhật lại các biến tham chiếu
                    board = game.board
                    selector = game.selector
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # =========== HIỂN THỊ THÔNG BÁO KHI GAME KẾT THÚC ==============
        if game.game_over:
            # Tạo overlay mờ
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Màu đen với độ trong suốt
            screen.blit(overlay, (0, 0))
            # Hiển thị thông báo
            font = pygame.font.SysFont('Arial', 50, bold=True)
            if game.result == 'checkmate':
                winner = 'WHITE' if game.winner == 'white' else 'ĐEN'
                text = f"{winner} WIN!"
                color = (255, 215, 0)  
            else:
                text = "DRAW!"
                color = (255, 255, 255) 
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text_surface, text_rect)
            
            # Hướng dẫn chơi lại
            font_small = pygame.font.SysFont('Arial', 30)
            restart_text = font_small.render("Press R To Rematch", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            screen.blit(restart_text, restart_rect)
        # ========= END HIỂN THỊ THÔNG BÁO KHI GAME KẾT THÚC ==========

        pygame.display.update()



main = Main()
main.mainLoop()

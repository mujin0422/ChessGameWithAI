import pygame
import sys
import copy
from const import *
from game import Game
from square import Square
from move import Move
from ai import AI_Minimax
from menu import get_game_mode


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('CHESS GAME')
        self.game = Game()
        self.restart_to_menu = False
        self.ai_enabled = True
        self.ai_thinking = False
        self.ai_move = None
        self.ai_delay = 400  # Thời gian delay để quan sát nước đi AI (ms)

    def handle_ai_turn(self):
        """Xử lý lượt đi của AI cho quân đen giống như Minimax folder"""
        if (self.ai_enabled 
            and not self.ai_thinking 
            and self.game.next_player == 'black' 
            and not self.game.game_over):
            
            self.ai_thinking = True
            
            # Tạo AI với độ sâu 3, bật alpha-beta và bảng điểm vị trí
            ai = AI_Minimax(self.game.board)
            ai.depth = 3
            ai.AlphaBetaPruning = True 
            ai.UsePointMaps = True

            # Tìm nước đi tốt nhất từ vị trí hiện tại
            try:
                depth = ai.get_search_depth(ai.is_endgame(self.game.board))
                _, pos, move = ai.minimax(
                    self.game.board,
                    'black',
                    depth,
                    -float('inf'),
                    float('inf'),
                    0
                )
                if pos and move:
                    row, col = pos
                    self.ai_move = (self.game.board.squares[row][col].piece, move)
                    # Lưu lịch sử để tránh lặp
                    if self.ai_move:
                        ai.update_move_history(self.ai_move[0], self.ai_move[1])
            except:
                # Nếu có lỗi, dùng fallback move
                self.ai_move = ai.get_fallback_move('black')
                
            self.ai_thinking = False

    def execute_ai_move(self):
        """Thực hiện nước đi của AI"""
        if self.ai_move and not self.game.game_over:
            piece, move = self.ai_move
            final_square = self.game.board.squares[move.final.row][move.final.col]
            captured = final_square.has_piece()
            
            # Thực hiện nước đi
            self.game.board.move(piece, move)
            self.game.board.set_true_en_passant(piece)
            self.game.play_sound(captured)
            self.game.next_turn()
            
            # Kiểm tra trạng thái game
            self.check_game_status()
            
            self.ai_move = None

    def check_game_status(self):
        """Kiểm tra trạng thái kết thúc game"""
        for color in ['white', 'black']:
            status = self.game.board.check_game_status(color)
            if status == 'checkmate':
                self.game.game_over = True
                self.game.winner = 'black' if color == 'white' else 'white'
                self.game.result = 'checkmate'
                break
            elif status == 'stalemate':
                self.game.game_over = True
                self.game.result = 'stalemate'
                break

    def handle_events(self):
        """Xử lý tất cả sự kiện đầu vào"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if not self.game.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
            
            if event.type == pygame.KEYDOWN:
                self.handle_key_press(event)

    def handle_mouse_click(self, event):
        """Xử lý click chuột của người chơi"""
        mouseX, mouseY = event.pos
        clicked_col = (mouseX - BOARD_X) // SQSIZE
        clicked_row = (mouseY - BOARD_Y) // SQSIZE

        if 0 <= clicked_row < ROWS and 0 <= clicked_col < COLS:
            clicked_square = self.game.board.squares[clicked_row][clicked_col]
            selector = self.game.selector

            # Đã chọn quân cờ trước đó
            if selector.selecting:
                self.handle_piece_move(clicked_row, clicked_col, clicked_square)
            # Chọn quân cờ mới
            elif clicked_square.has_piece() and clicked_square.piece.color == self.game.next_player:
                self.select_piece(clicked_row, clicked_col, clicked_square)

    def handle_piece_move(self, row, col, square):
        selector = self.game.selector
        selected_piece = selector.piece
        start_row, start_col = selector.rowcol
        move = Move(Square(start_row, start_col), Square(row, col))

        if self.game.board.valid_move(selected_piece, move):
            captured = square.has_piece()
            self.game.board.move(selected_piece, move)
            self.game.board.set_true_en_passant(selected_piece)
            self.game.play_sound(captured)
            
            # Vẽ lại ngay lập tức
            self.draw_game()
            pygame.display.update()
            
            self.game.next_turn()
            self.check_game_status()
        
        selector.unselect_piece()

    def select_piece(self, row, col, square):
        """Chọn quân cờ để di chuyển"""
        piece = square.piece
        if piece.color == self.game.next_player:
            self.game.board.calc_moves(piece, row, col, True)
            self.game.selector.select_piece(piece, (row, col))

    def handle_mouse_motion(self, event):
        """Xử lý di chuyển chuột"""
        hover_row = (event.pos[1] - BOARD_Y) // SQSIZE
        hover_col = (event.pos[0] - BOARD_X) // SQSIZE
        self.game.set_hover(hover_row, hover_col)

    def handle_key_press(self, event):
        """Xử lý phím bấm"""
        if event.key == pygame.K_t:
            self.game.change_theme()
        elif event.key == pygame.K_r:
            self.reset_game()
        elif event.key == pygame.K_a:
            self.ai_enabled = not self.ai_enabled  # Bật/tắt AI
        elif event.key == pygame.K_ESCAPE:
            self.restart_to_menu = True  # Đặt cờ để thoát về menu

    def reset_game(self):
        """Reset game về trạng thái ban đầu"""
        self.game.reset()
        self.game.game_over = False
        self.game.winner = None
        self.game.result = None
        self.ai_thinking = False
        self.ai_move = None

    def draw_game(self):
        """Vẽ tất cả thành phần game"""
        self.screen.fill((0, 0, 0))
        self.game.show_bg(self.screen)
        self.game.show_last_move(self.screen)
        self.game.show_moves(self.screen)
        self.game.show_hover(self.screen)
        self.game.show_pieces(self.screen)
        
        if self.game.game_over:
            self.draw_game_over()

    def draw_game_over(self):
        """Hiển thị thông báo kết thúc game"""
        # Overlay mờ
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Thông báo chính
        font = pygame.font.SysFont('Arial', 50, bold=True)
        if self.game.result == 'checkmate':
            winner = 'WHITE' if self.game.winner == 'white' else 'BLACK'
            text = f"{winner} WINS!"
            color = (255, 215, 0)  # Gold color
        else:
            text = "DRAW!"
            color = (255, 255, 255)  # White color
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text_surface, text_rect)
        
        # Hướng dẫn chơi lại
        font_small = pygame.font.SysFont('Arial', 30)
        restart_text = font_small.render("Press R to Rematch", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        self.screen.blit(restart_text, restart_rect)

    def mainLoop(self):
        clock = pygame.time.Clock()
        
        while True:
            # Xử lý sự kiện
            self.handle_events()

            # Nếu người dùng bấm ESC, thoát vòng lặp để quay lại menu
            if self.restart_to_menu:
                pygame.display.quit()  
                break
            
            # Xử lý AI
            if not self.game.game_over and self.game.next_player == 'black' and self.ai_enabled:
                self.handle_ai_turn()
                if self.ai_move:
                    pygame.time.delay(self.ai_delay)  # Delay để quan sát
                    self.execute_ai_move()
                    self.draw_game()  # Vẽ lại sau khi AI đi
                    pygame.display.update()
            
            # Vẽ game (bao gồm cả khi người chơi đi)
            self.draw_game()
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    while True:
        # Gọi giao diện chọn chế độ
        mode = get_game_mode()

        if mode is None:
            sys.exit()  # Người dùng bấm "EXIT"

        # Khởi chạy game
        main = Main()
        main.ai_enabled = mode
        main.mainLoop()

        # Nếu không nhấn ESC trong game, thoát
        if not main.restart_to_menu:
            break

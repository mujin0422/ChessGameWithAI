""" LƯU HẰNG SỐ CỦA GAME
- Lưu các giá trị cố đinh như kích thước bàn cờ, tọa độ """
WIDTH = 450
HEIGHT = 450

# SCREEN DIMENSION
SCREEN_WIDTH = WIDTH + 500
SCREEN_HEIGHT = HEIGHT + 200

# BROAD DIMENSION
ROWS = 8 
COLS = 8
SQSIZE = WIDTH // COLS # Kích thước một ô cờcờ
BOARD_WIDTH = SQSIZE * COLS  # Tổng chiều rộng bàn cờ
BOARD_HEIGHT = SQSIZE * ROWS  # Tổng chiều cao bàn cờ

# BOARD ALIGNMENT (Căn giữa bàn cờ trong cửa sổ)
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2

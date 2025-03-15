# Quản lý xác thực


from ChessGameWithAI.db.database import get_connection
import bcrypt

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Mã hóa mật khẩu bằng bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    
    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        return True
    return False

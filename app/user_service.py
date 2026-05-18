from app.auth import hash_password, verify_password
from app.database import get_connection


def create_user(username: str, password: str, email: str):
    """
    创建用户。
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (username, email, hash_password(password))
        )
        conn.commit()

        return {
            "success": True,
            "message": "注册成功"
        }

    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return {
                "success": False,
                "message": "用户名已存在"
            }

        return {
            "success": False,
            "message": "注册失败"
        }

    finally:
        conn.close()


def authenticate_user(username: str, password: str):
    """
    校验用户名和密码。
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return user


def get_user_by_username(username: str):
    """
    根据用户名查询用户信息。
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email, created_at
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    return dict(user)
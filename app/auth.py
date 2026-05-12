import hashlib
import secrets


TOKEN_STORE = {}


def hash_password(password: str) -> str:
    """
    对密码做哈希处理。
    练习项目中使用 sha256，真实项目中更推荐 bcrypt / argon2。
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """
    校验密码。
    """
    return hash_password(password) == password_hash


def generate_token(username: str) -> str:
    """
    生成登录 token，并保存到内存中。
    """
    token = secrets.token_hex(16)
    TOKEN_STORE[token] = username
    return token


def get_username_by_token(token: str):
    """
    根据 token 获取用户名。
    """
    return TOKEN_STORE.get(token)
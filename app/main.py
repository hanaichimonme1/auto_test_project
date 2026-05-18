from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse

from app.auth import generate_token, get_username_by_token
from app.database import init_db
from app.user_service import create_user, authenticate_user, get_user_by_username
from fastapi import FastAPI, Depends


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Lightweight User System")
security = HTTPBearer(auto_error=False)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")

@app.get("/")
def index_page():
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/login-page")
def login_page():
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/register-page")
def register_page():
    return FileResponse(FRONTEND_DIR / "register.html")


@app.get("/profile-page")
def profile_page():
    return FileResponse(FRONTEND_DIR / "profile.html")



@app.on_event("startup")
def startup():
    init_db()


@app.post("/api/register")
def register(data: dict):
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "用户名、密码和邮箱不能为空"
            }
        )

    result = create_user(username, password, email)

    if not result["success"]:
        return JSONResponse(
            status_code=400,
            content=result
        )

    return result


@app.post("/api/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "用户名和密码不能为空"
            }
        )

    user = authenticate_user(username, password)

    if user is None:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "用户名或密码错误"
            }
        )

    token = generate_token(username)

    return {
        "success": True,
        "message": "登录成功",
        "token": token
    }


@app.get("/api/profile")
def profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "缺少或非法 token"
            }
        )

    if credentials.scheme.lower() != "bearer":
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "token 类型错误"
            }
        )

    token = credentials.credentials
    print("收到的 token:", token)

    username = get_username_by_token(token)

    if username is None:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "token 无效或已过期"
            }
        )

    user = get_user_by_username(username)

    if user is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "用户不存在"
            }
        )

    return {
        "success": True,
        "message": "查询成功",
        "data": user
    }
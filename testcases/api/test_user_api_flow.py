import time
import pytest
from common.request_util import RequestUtil

BASE_URL = "http://127.0.0.1:8000"


def generate_test_user():
    timestamp = int(time.time())
    return {
        "username": f"api_user_{timestamp}",
        "email": f"api_user_{timestamp}@test.com",
        "password": "123456"
    }


@pytest.mark.api
@pytest.mark.e2e
@pytest.mark.login
def test_register_login_profile_api_flow():
    user = generate_test_user()

    # 1. 注册用户
    register_res=RequestUtil.send_method(
        method="post",
        url=f"{BASE_URL}/api/register",
                                         json={
                                             "username": user["username"],
                                             "email": user["email"],
                                             "password": user["password"]
                                         }
                                         )
    assert register_res.status_code == 200
    register_json = register_res.json()
    assert register_json["success"] is True
    assert register_json["message"] == "注册成功"

    # 2. 重复注册应该失败

    duplicate_res = RequestUtil.send_method(
        method="post",
        url=f"{BASE_URL}/api/register",
                                         json={
                                             "username": user["username"],
                                             "email": user["email"],
                                             "password": user["password"]
                                         }
                                         )

    assert duplicate_res.status_code == 400
    duplicate_json = duplicate_res.json()
    assert duplicate_json["success"] is False
    assert duplicate_json["message"] == "用户名已存在"

    # 3. 登录用户
    login_res= RequestUtil.send_method(
        method="post",
        url=f"{BASE_URL}/api/login",
        json={
        "username": user["username"],
        "password": user["password"]
        }
        )
    assert login_res.status_code == 200
    login_json = login_res.json()
    assert login_json["success"] is True
    assert login_json["message"] == "登录成功"
    assert "token" in login_json
    assert login_json["token"]

    token = login_json["token"]

    # 4. 带 token 查询个人信息
    profile_res = RequestUtil.send_method(method="get",
                                          url=f"{BASE_URL}/api/profile",
                                          headers={
                                              "Authorization": f"Bearer {token}"
                                          }
                                          )

    assert profile_res.status_code == 200
    profile_json = profile_res.json()
    assert profile_json["success"] is True
    assert profile_json["message"] == "查询成功"
    assert profile_json["data"]["username"] == user["username"]
    assert profile_json["data"]["email"] == user["email"]


@pytest.mark.api
@pytest.mark.login
def test_login_with_wrong_password():
    user = generate_test_user()

    # 先注册一个用户
    RequestUtil.send_method(method="post",
                            url=f"{BASE_URL}/api/register",
                            json={
                                "username": user["username"],
                                "email": user["email"],
                                "password": user["password"]
                            }
                            )

    # 使用错误密码登录
    login_res = RequestUtil.send_method(method="post",
                                        url=f"{BASE_URL}/api/login",
                                        json={
                                            "username": user["username"],
                                            "password": "wrong_password"
                                        }
                                        )

    assert login_res.status_code == 401
    login_json = login_res.json()
    assert login_json["success"] is False
    assert login_json["message"] == "用户名或密码错误"


@pytest.mark.api
def test_profile_without_token():
    profile_res = RequestUtil.send_method(method="get",url=f"{BASE_URL}/api/profile")

    assert profile_res.status_code == 401
    profile_json = profile_res.json()
    assert profile_json["success"] is False
    assert profile_json["message"] == "缺少或非法 token"
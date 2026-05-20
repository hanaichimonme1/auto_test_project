import time
import pytest
from selenium.webdriver.common.by import By
from common.browser_util import wait_find, wait_click, wait_url_contains, wait_text_present
from common.config import config

BASE_URL = config["local_base_url"]


def generate_test_user():
    """
    生成唯一测试用户，避免重复注册导致用户名已存在。
    """
    timestamp = int(time.time())
    return {
        "username": f"ui_user_{timestamp}",
        "email": f"ui_user_{timestamp}@test.com",
        "password": "123456"
    }


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.login
def test_register_login_profile_flow(driver):
    user = generate_test_user()

    # 1. 打开注册页
    driver.get(f"{BASE_URL}/register-page")

    # 2. 输入注册信息
    wait_find(driver, By.ID, "username").send_keys(user["username"])
    wait_find(driver, By.ID, "email").send_keys(user["email"])
    wait_find(driver, By.ID, "password").send_keys(user["password"])
    wait_click(driver, By.ID, "register-btn")

    # 3. 断言注册成功后跳转到登录页
    wait_url_contains(driver, "/login-page", timeout=5)

    # 4. 输入登录信息
    wait_find(driver, By.ID, "username").send_keys(user["username"])
    wait_find(driver, By.ID, "password").send_keys(user["password"])
    wait_click(driver, By.ID, "login-btn")

    # 5. 断言登录成功后跳转到个人信息页
    wait_url_contains(driver, "/profile-page", timeout=5)

    # 6. 断言个人信息页展示正确
    wait_text_present(driver, By.ID, "username", user["username"], timeout=5)
    wait_text_present(driver, By.ID, "email", user["email"], timeout=5)

    page_username = wait_find(driver, By.ID, "username").text
    page_email = wait_find(driver, By.ID, "email").text

    assert page_username == user["username"]
    assert page_email == user["email"]
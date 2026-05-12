from pathlib import Path

import pytest
from selenium.webdriver.common.by import By

from common.browser_util import wait_find, wait_click
from common.data_util import load_json_data , validate_login_cases


BASE_DIR = Path(__file__).resolve().parents[2]
BASE_HTML = BASE_DIR / "demo_login.html"
DATA_FILE = BASE_DIR / "data" / "login_ui_data.json"


login_cases = load_json_data(DATA_FILE)
validate_login_cases(login_cases)

def open_login_page(driver):
    driver.get(BASE_HTML.as_uri())


def input_login_info(driver, username, password):
    wait_find(driver, By.ID, "username").send_keys(username)
    wait_find(driver, By.ID, "password").send_keys(password)


def get_message(driver):
    return wait_find(driver, By.ID, "message").text



@pytest.mark.ui
@pytest.mark.login
@pytest.mark.parametrize(
    "case",
    login_cases,
    ids=[case["case_name"] for case in login_cases]
)
def test_login_ui(driver, case):
    open_login_page(driver)

    input_login_info(driver, case["username"], case["password"])
    wait_click(driver, By.ID, "login-btn")

    assert get_message(driver) == case["expected_message"]
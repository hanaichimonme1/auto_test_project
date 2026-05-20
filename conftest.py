import re
from datetime import datetime
from pathlib import Path

import pytest

from common.browser_util import create_driver, save_screenshot
from common.config import config
from common.request_util import RequestUtil

BASE_DIR = Path(__file__).resolve().parent
SCREENSHOT_DIR = BASE_DIR / "reports" / "screenshots"
@pytest.fixture
def driver():
    driver = create_driver()

    yield driver

    driver.quit()

def safe_filename(name: str):
    """
    将用例名转换成适合作为文件名的字符串。
    """
    return re.sub(r'[\\/:*?"<>|]', "_", name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 钩子函数：
    当测试用例执行失败时，自动保存浏览器截图。
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")

        if driver is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            case_name = safe_filename(item.name)
            screenshot_path = SCREENSHOT_DIR / f"{case_name}_{timestamp}.png"

            save_screenshot(driver, screenshot_path)

            print(f"\n失败截图已保存: {screenshot_path}")

@pytest.fixture(scope="session")
def get_token():
    url=config.get("base_url")
    data={
        "email":"eve.holt@reqres.in","password":"pistol"
    }
    res=RequestUtil.send_method(url,"POST",json=data)
    token=res.json().get("token")
    # assert res.status_code == 200
    # assert "token" in res.json()
    return token
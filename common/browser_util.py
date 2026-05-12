from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
def create_driver(headless: bool = False):
    """
    创建浏览器对象。
    headless=True 时使用无头模式，适合服务器或 CI 环境运行。
    """
    options = Options()

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=options)

    if not headless:
        driver.maximize_window()

    return driver


def wait_find(driver, by, value, timeout: int = 5):
    """
    显式等待元素出现，并返回该元素。
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_click(driver, by, value, timeout: int = 5):
    """
    显式等待元素可以点击，然后点击。
    """
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()
    return element

def save_screenshot(driver, file_path):
    """
    保存当前浏览器截图。
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(path))
    return path
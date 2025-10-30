import os
import time

from dotenv import load_dotenv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# 게이트 정보 로드
load_dotenv()
info = {
    "gate_url" : os.getenv("GATE_URL"),
    "gate_id" : os.getenv("GATE_ID"),
    "gate_pw" : os.getenv("GATE_PW")
}

def alert(message):
    print(f"[알림] {message}")

# chrome 열기
def load_browser(url):
    alert('start load browser')
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--log-level=3')

    # options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

# 브라우저 열려잇는지 확인
def is_browser_open(driver):
    if not driver:
        return False
    try:
        driver.window_handles
        return True
    except WebDriverException:
        return False

# 로그인
def login_proc(driver):
    try:
        # 로그인 input이 보일때까지 0.2초마다 체크 (최대 10초 대기)
        WebDriverWait(driver, 10, poll_frequency=0.2).until(
            # visible이 true일때까지 대기
            EC.visibility_of_element_located((By.ID, 'loginId'))
        )
        driver.find_element(By.ID,'loginId').send_keys(info['gate_id'])
        driver.find_element(By.ID,'loginPw').send_keys(info['gate_pw'])
        driver.find_element(By.ID,'loginBtn').click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[data-original-title="Logout"]'))

        )
        return True
    except:
        return False


# 브라우저 열기
browser = load_browser(info['gate_url'])
print(browser.session_id)





while True:
    if not is_browser_open(browser):
        browser = load_browser(info['gate_url'])
    if login_proc(browser):
        alert("로그인 성공")
    else:
        alert("로그인 실패")
    alert(browser.current_url)

    time.sleep(5)


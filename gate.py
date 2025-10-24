from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

import os
import time

# URL, LOGIN Data 가져오기
load_dotenv()

# Gate 로그인 url
GATE_URL = os.getenv("GATE_URL")
GATE_ID = os.getenv("GATE_ID")
GATE_PW = os.getenv("GATE_PW")

driver = webdriver.Chrome()

# 로그인 페이지 이동
driver.get(GATE_URL);
time.sleep(2)

# 로그인 폼 입력
driver.find_element(By.ID, 'loginId').send_keys(GATE_ID)
driver.find_element(By.ID, 'loginPw').send_keys(GATE_PW)
driver.find_element(By.ID, 'loginBtn').click()
time.sleep(2)



# 1. 차단기 바 우클릭
target_bar = driver.find_element(By.ID, 'bar0101')
actions = ActionChains(driver)
actions.context_click(target_bar).perform()
time.sleep(0.5)

# 2. 활성화된 메뉴 클릭 (visible, clickable 상태 검사)
menu_open = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-action="Open"]'))
)
menu_open.click()

# 모달/입력창이 보일 때까지 대기
# <div class="modal-backdrop fade in"></div>
input_elem = WebDriverWait(driver, 6).until(
    EC.visibility_of_element_located((By.ID, "coment"))
)
input_elem.clear()
input_elem.send_keys('자동화 테스트')

time.sleep(5)
# 이후 버튼 클릭 등
driver.find_element(By.ID, "sendBtn").click()
time.sleep(105)

# 누르면 열림 누르면 <div class="alertify-notifier ajs-bottom ajs-right"><div class="ajs-message ajs-success ajs-visible">처리되었습니다.</div></div>

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

import pymysql

import os
import time
from datetime import datetime

# get url, login data
load_dotenv()
gate_url = os.getenv("GATE_URL")
gate_id = os.getenv("GATE_ID")
gate_pw = os.getenv("GATE_PW")

driver = None




###########
# function
###########

# chrome 열기
def start_driver():
	driver = webdriver.Chrome()
	driver.get(gate_url)
	return driver

def alert(message):
	print(f"[알림] ✓{message}")

def connecting():
	alert(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ 작동중.")

# 로그인 체크
def is_logged_in(driver):
	#로그인 상태 확인. 버튼이 있으면 로그아웃 상태
	try:
		driver.find_element(By.ID, 'loginId')
		return False
	except:
		return True

# chrome 열려있는지 확인
def is_driver_alive(driver):
	try:
		if driver.session_id is None:
			return False
		_ = driver.title
		return True
	except WebDriverException:
		return False



##########
try:
	# 브라우저 실행
	if driver is None or not is_driver_alive(driver):
		driver = start_driver()


	# 로그인 페이지 이동
	# loginId가 보일때 까지 0.2 초마다 체크(최대 10초 대기)
	WebDriverWait(driver, 10, poll_frequency=0.2).until(
		# visible 이 true일때 까지 대기
		EC.visibility_of_element_located((By.ID, 'loginId'))
	)
	driver.find_element(By.ID, 'loginId').send_keys(gate_id)
	driver.find_element(By.ID, 'loginPw').send_keys(gate_pw)
	driver.find_element(By.ID, 'loginBtn').click()

	#[알림] ✓[{'domain': '106.240.156.196', 'httpOnly': True, 'name': 'ParkNManage', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '8B3F1BB5160BA85CCF5C18A5E3811D8D'}]

	print("=" * 50)
	print("로그인 완료!")
	print("=" * 50)
	print("사용 가능한 명령:")
	print("  open  - 게이트 열기")
	print("  close - 게이트 닫기")
	print("  quit  - 프로그램 종료")
	print("=" * 50)


	while True:
		connecting()

		alert(is_logged_in(driver))
		time.sleep(1)


		# 브라우저가 꺼지면 재실행
		if not is_driver_alive(driver):
			driver = start_driver()


except TimeoutException:
	print("요소를 찾을 수 없거나 로딩 시간이 오래걸립니다.")
except KeyboardInterrupt:
	print("n\nCtrl+C가 감지되었습니다. 프로그램을 종료합니다.")
finally:
	if driver is not None:
		driver.quit()





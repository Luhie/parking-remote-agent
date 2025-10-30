from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

import pymysql

import os
import time
from datetime import datetime

# 알림 계속 출력되게 쓰레드
import threading
from queue import Queue
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

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
	options = Options()
	# 2. 헤드리스 모드 옵션 추가 ('new'가 최신 방식)
	# options.add_argument('--headless=new')
	# 3. (권장) 헤드리스에서 발생할 수 있는 문제 방지 옵션
	options.add_argument('--disable-gpu') # GPU 가속 비활성화 (헤드리스 환경에서 종종 필요)
	options.add_argument('--window-size=1920,1080') # 창 크기를 지정 (레이아웃 깨짐 방지)
	# 불필요한 로그 숨기기
	options.add_argument('--log-level=3')
	driver = webdriver.Chrome(options=options)
	driver.get(gate_url)
	return driver

def alert(message):
	print(f"[알림] ✓{message}")

def connecting_worker(stop_event):
	while not stop_event.is_set():
		alert(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ 작동중.")
		stop_event.wait(5)

# 로그인 체크
def is_logged_in(driver):
	#로그인 상태 확인. 버튼이 있으면 로그아웃 상태
	try:
		driver.find_element(By.ID, 'loginId')
		login_proc(driver)
	except:
		return True

def login_proc(driver):
	try:
		# 로그인 페이지 이동
		# loginId가 보일때 까지 0.2 초마다 체크(최대 10초 대기)
		WebDriverWait(driver, 10, poll_frequency=0.2).until(
			# visible 이 true일때 까지 대기
			EC.visibility_of_element_located((By.ID, 'loginId'))
		)
		driver.find_element(By.ID, 'loginId').send_keys(gate_id)
		driver.find_element(By.ID, 'loginPw').send_keys(gate_pw)
		driver.find_element(By.ID, 'loginBtn').click()
		return True
	except:
		return False

# chrome 열려있는지 확인
def is_driver_alive(driver):
	try:
		if driver.session_id is None:
			return False
		_ = driver.title
		return True
	except WebDriverException:
		return False


def open_gate(driver):
	try:
		# 1. 차단기 바 우클릭
		target_bar = driver.find_element(By.ID, 'bar0101')
		actions = ActionChains(driver)
		actions.context_click(target_bar).perform()
		time.sleep(0.5)

		# 2. 활성화된 메뉴 클릭 (visible, clickable 상태 검사)
		menu_open = WebDriverWait(driver, 5).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#context-menu a[data-action="Open"]'))
		)
		menu_open.click()

		# 모달/입력창이 보일 때까지 대기
		# <div class="modal-backdrop fade in"></div>
		input_elem = WebDriverWait(driver, 6).until(
			EC.visibility_of_element_located((By.ID, "coment"))
		)
		input_elem.clear()
		input_elem.send_keys('자동화 테스트')

		# 이후 버튼 클릭 등
		driver.find_element(By.ID, "sendBtn").click()

		print("게이트를 열었습니다.")
	except TimeoutException:
		print("게이트 열기 버튼을 찾을 수 없습니다.")



##########
try:
	# 브라우저 실행
	if driver is None or not is_driver_alive(driver):
		driver = start_driver()
		login_proc(driver)

	print("=" * 50)
	print("로그인 완료!")
	print("=" * 50)
	print("사용 가능한 명령:")
	print("  open  - 게이트 열기")
	print("  close - 게이트 닫기")
	print("  exit  - 프로그램 종료")
	print("=" * 50)

	# 스레드시작
	stop_event = threading.Event()
	conn_thread = threading.Thread(target=connecting_worker, args=(stop_event,))
	# 메인 프로그램 종료시 같이 종료
	conn_thread.daemon = True
	conn_thread.start()

	session = PromptSession()

	with patch_stdout():

		while True:
			try:
				command = session.prompt("명령 입력 > ").strip().lower()
			except (KeyboardInterrupt, EOFError):
				# Ctrl+c, Ctrl+D 입력시 종료
				print("프로그램을 종료합니다.")
				break

			if command == 'exit':
				# Ctrl+c, Ctrl+D 입력시 종료
				print("프로그램을 종료합니다.")
				break

			if command == 'open':
				# 드라이버가 죽었는지 체크
				if not is_driver_alive(driver):
					alert("브라우저가 꺼졌으므로 재시작합니다.")
					try:
						driver.quit()
					except:
						pass
					driver = start_driver()
					# 로그인 처리
					is_logged_in(driver)
				else:
					alert("브라우저가 살아있으므로 기존 창에서 진행합니다.")
					is_logged_in(driver)

				try:
					open_gate(driver)
				except Exception as e:
					print(f"게이트 열기 실패: {e}")

except TimeoutException:
	print("요소를 찾을 수 없거나 로딩 시간이 오래걸립니다.")
except KeyboardInterrupt:
	print("n\nCtrl+C가 감지되었습니다. 프로그램을 종료합니다.")
finally:
	if 'stop_event' in locals():
		stop_event.set() # 스레드 종료
	if driver is not None:
		try:
			driver.quit()
		except:
			pass


# 차단기 열기
# EC.element_to_be_clickable((By.CSS_SELECTOR, '#context-menu a[data-action="Open"]'))
# 차단기 닫기
# EC.element_to_be_clickable((By.CSS_SELECTOR, '#context-menu a[data-action="Close"]'))
# 차단기 열림 고정
# EC.element_to_be_clickable((By.CSS_SELECTOR, '#context-menu a[data-action="Uplock"]'))
# 차단기 고정 해제
# EC.element_to_be_clickable((By.CSS_SELECTOR, '#context-menu a[data-action="Unlock"]'))

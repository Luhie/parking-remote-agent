from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import os

# get url, login data
load_dotenv()
gate_url = os.getenv("GATE_URL")
gate_id = os.getenv("GATE_ID")
gate_pw = os.getenv("GATE_PW")

# 브라우저 종료 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 로그인 페이지 이동
driver = webdriver.Chrome(options=chrome_options)
driver.get(gate_url)

try:
    # loginId가 보일때 까지 0.2 초마다 체크(최대 10초 대기)
    WebDriverWait(driver, 10, poll_frequency=0.2).until(
        EC.visibility_of_element_located((By.ID, 'loginId'))
    )
    driver.find_element(By.ID, 'loginId').send_keys(gate_id)
    driver.find_element(By.ID, 'loginPw').send_keys(gate_pw)
    driver.find_element(By.ID, 'loginBtn').click()
    
    print("=" * 50)
    print("로그인 완료!")
    print("=" * 50)
    print("사용 가능한 명령:")
    print("  open  - 게이트 열기")
    print("  close - 게이트 닫기")
    print("  quit  - 프로그램 종료")
    print("=" * 50)
    
    # 명령 대기 루프
    while True:
        command = input("\n명령 입력 > ").strip().lower()
        
        if command == 'quit':
            print("프로그램을 종료합니다.")
            break
        elif command == 'open':
            try:
                # 게이트 열기 버튼 클릭
                open_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, 'openGateBtn'))
                )
                open_btn.click()
                print("✓ 게이트를 열었습니다.")
            except TimeoutException:
                print("✗ 게이트 열기 버튼을 찾을 수 없습니다.")
        elif command == 'close':
            try:
                # 게이트 닫기 버튼 클릭
                close_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, 'closeGateBtn'))
                )
                close_btn.click()
                print("✓ 게이트를 닫았습니다.")
            except TimeoutException:
                print("✗ 게이트 닫기 버튼을 찾을 수 없습니다.")
        else:
            print(f"✗ 알 수 없는 명령: '{command}'")
            print("   사용 가능한 명령: open, close, quit")

except TimeoutException:
    print("요소를 찾을 수 없거나 로딩 시간이 오래걸립니다.")
except KeyboardInterrupt:
    print("\n\nCtrl+C가 감지되었습니다. 프로그램을 종료합니다.")
finally:
    # detach 옵션 때문에 quit()을 호출해도 브라우저는 열린 상태로 유지됨
    # 브라우저를 닫고 싶다면 이 줄을 주석 처리하세요
    driver.quit()

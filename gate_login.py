from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql

import os
import time

# get url, login data
load_dotenv()

gate_url = os.getenv("GATE_URL")
gate_id = os.getenv("GATE_ID")
gate_pw = os.getenv("GATE_PW")


driver = webdriver.Chrome()

# 로그인 페이지 이동
driver.get(gate_url)
time.sleep(2)

driver.find_element(By.ID, 'loginId').send_keys(gate_id)
driver.find_element(By.ID, 'loginPw').send_keys(gate_pw)
driver.find_element(By.ID, 'loginBtn').click()



time.sleep(100)
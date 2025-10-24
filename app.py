import requests


"""
" 1. 메시지 출력 함수
"""
def alert(message):
	print(f"[알림] {message}")

# Gate 로그인 url
GATE_URL = "http://106.240.156.196:9090/login.htm"

##
login_data = {
	'loginId': '1234',
	'loginPw': '1234',
	'saveId': 'on'
}

alert(f" 게이트 로그인 시도 (ID: {login_data['loginId']})")

session = requests.Session()

res = session.post(GATE_URL, data=login_data)


alert(f" 로그인 확인: {res.ok}")
alert(f" 로그인 확인: {res.status_code}")
alert(f" 로그인 확인: {res.url}")
alert(f" 로그인 확인: {res.headers}")
alert(f" 로그인 확인: {res.cookies}")
alert(f" 로그인 확인: {res.text[:500]}")

if res.ok and '차단기 제어' in res.text:
	print('로그인 성공')
else:
	print('로그인 실패')


# <form id="loginform" name="loginform" method="post" onsubmit="return loginsubmit()">
# 					<input type="hidden" id="authexctioncode" value="">
# 					<p class="text-muted text-center">사용자 id와 패스워드를 입력하세요</p>
# 					<div id="alertmsg" class="alert alert-danger" style="display: none;"></div>
# 					<input type="text" id="loginid" name="loginid" placeholder="사용자 id" class="form-control top" value="">
# 					<input type="password" id="loginpw" name="loginpw" placeholder="사용자 패스워드" class="form-control bottom">
# 					<div class="checkbox">
# 						<label> <input type="checkbox" id="saveid" name="saveid"> 사용자id 저장
# 						</label>
# 					</div>
# 					<button class="btn btn-lg btn-primary btn-block" type="submit" id="loginbtn">sign in</button>
# 				</form>in</button>





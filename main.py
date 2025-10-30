from db import MySQLConnector
import time
my = MySQLConnector()


if my.conn('som_ai'):
    uid=1
    data=my.get("SELECT * FROM sv_)
else:
    print("som_ai에 연결이 실패되었습니다.")
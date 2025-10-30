import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os
import time

load_dotenv()

class MySQLConnector:
    def __init__(self):
        self.DB_INFO = {
            'host' : os.getenv("HOST_NAME"),
            'user' : os.getenv("HOST_USER"),
            'password' : os.getenv("HOST_PW"),
            'charset' : 'utf8mb4'
        }
        self.conn = None


    def conn(self, db_name):
        """DB 연결"""
        if self.conn:
            self.close()

        self.DB_INFO['database'] = db_name
        try:
            self.conn = pymysql.connect(**self.DB_INFO, cursorclass=pymysql.cursors.DictCursor)
            print("DB 연결 성공")
            return True
        except Exception as e:
            print("DB 연결 실패", e)
            return False

    def get(self, query, parmas=None):
        """ 쿼리 실행 """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Exception as e:
            print("쿼리 에러",e )
            return None

    def gets(self, query):
        """ 여러 데이터 조회 """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print("쿼리 에레",e)
            return None

    def qry(self, query):
        """여러데이터 입력"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print("쿼리에러",e)
            self.conn.rollback()
            return False

    def close(self):
        """DB 연결 종료"""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("DB 연결 종료")






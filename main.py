# PyMySQL - DB서버 연동 체험
# main.py - 단순 동작 위주의 코드만 작성할 예정
# DB연결 관련된 기타 기능 : phone_book.py 모듈 이용 예정

import pymysql

# DB에 연결을 해야 쿼리를 날릴 수 있다

# DB 연결부터 진행
# DB 연결시도의 결과를 변수에 담자
db = pymysql.connect(
    host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com', 
    port=3306, 
    user='admin', 
    passwd='Vmfhwprxm!123',
    db= 'test_phone_book',
    charset='utf8')

# cursor : DB에 쿼리를 날려주는 역할을 하는 인스턴스 + SELECT는 실행 결과를 받아와주는 역할도 담당한다
cursor = db.cursor()

# users에 모든 데이터를 SELECT로 확인해보자(예시)

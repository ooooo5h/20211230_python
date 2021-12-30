# PyMySQL - DB서버 연동 체험
# main.py - 단순 동작 위주의 코드만 작성할 예정
# DB연결 관련된 기타 기능 : phone_book.py 모듈 이용 예정

import pymysql
from phone_book import set_db_info

# DB에 연결을 해야 쿼리를 날릴 수 있다

# DB 연결부터 진행
# DB 연결시도의 결과를 변수에 담자

# 접속 정보만 명시
db = pymysql.connect(
    host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com', 
    port=3306, 
    user='admin', 
    passwd='Vmfhwprxm!123',
    db= 'test_phone_book',
    charset='utf8')


# phone_book.py에서 로직 작성 => 연결정보를 넘겨주고, 그 파일에서 활용하게끔 코드작성
set_db_info(db)
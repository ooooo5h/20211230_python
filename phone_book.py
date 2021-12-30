import pymysql
from time import sleep
# DB 연결자체는 main.py에서 설정
# 여기서는 만들어진 연결정보를 받아서 사용하자

db_connect = pymysql.connect(
    host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com', 
    port=3306, 
    user='admin', 
    passwd='Vmfhwprxm!123',
    db= 'test_phone_book',
    charset='utf8')

# 쿼리를 날리는 역할
cursor = db_connect.cursor()


def print_main_menu():
    print('===== 전화번호부 =====')
    print('1. 로그인')
    print('2. 회원가입')
    print('0. 프로그램 종료')
    print('======================')
    
    menu_num = int(input('메뉴 선택 : '))
    return menu_num

# 회원가입 실행하는 함수 -> DB에 쿼리를 날리자
# 회원가입은 users라는 테이블에, 회원정보가 담긴 row를 추가하자 => INSERT INTO 쿼리 활용
def sign_up():
    input_email = input('가입 이메일 : ')
    input_password = input('사용할 비밀번호 : ')
    input_nickname = input('닉네임 : ')
    
    # INSERT INTO 쿼리의 VALUES에 집어넣자
    # f string으로 실제 입력된 내용을 쿼리에 반영시키고 싶은 데
    # SQL (쿼리)를 짤 때, 'string'형태로 처리를 해야하는 일이 빈번함으로 f"문장" 형태로, " "로 감싸주기!!!
    sql = f"INSERT INTO users (users.email, users.password, users.nickname) VALUES ('{input_email}', '{input_password}', '{input_nickname}')"
    
    cursor.execute(sql)
    db_connect.commit()
    
    print('회원가입이 완료되었습니다. 메인화면으로 돌아갑니다.')
    sleep(2)
    
# 로그인 (sing in) 기능
# : 아이디/비밀번호를 입력받고, DB에 등록된 정보인지 검색한 후 결과는 TRUE/FALSE로 리턴하자
def sign_in():
    input_email = input('이메일 : ')
    input_pw = input('비밀번호 : ')
    
    # email,pw가 모두 맞는 회원이 있나 조회하기 => SELECT쿼리
    sql = f"SELECT * FROM users WHERE users.email = '{input_email}' AND users.password = '{input_pw}'"
    
    # SELECT 쿼리를 실행해보자
    cursor.execute(sql)
    
    # cursor에는 실행 결과가 표로 담겨있는데, tuple로 변환해보자
    user_list = cursor.fetchall()
    
    # # 반복문을 돌면서 내용 확인
    # for user in user_list:
    #     print(user)
        
    # 로그인 성공 유무 판별 기준은, user_list의 갯수가 0이면 실패, 1이면 성공
    if len(user_list) == 0:
        print('잘못된 회원 정보입니다. 다시 로그인 해주세요.')
        sleep(2)
        return False
    else:
        # 아이디/비밀번호 일치하는 회원 발견했으니 성공으로 처리
        print(f'로그인에 성공했습니다.')
        sleep(2)
        return True

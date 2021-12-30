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

# 로그인한 사용자가 몇번 사용자인지 변수로 저장
login_user_id = 0  # 0으로 초기화 (임시작업)


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
        # user_list에서는 0번째 아이템이 로그인에 성공한 사람의 정보
        
        login_user = user_list[0]   # 최소한 0번째는 있을 것이다.
        print(login_user)           # 로그인 사용자 정보를 , tuple로 모든 정보를 들고 있음        
        user_nickname = login_user[3]     # 사용자 정보 튜플에서 닉네임을 추출했다
        
        global login_user_id   # 상단에 만든 login_user_id 변수를 끌어다 쓰겠다 
        login_user_id = login_user[0]   # 로그인한 사용자(내가) 몇번 id를 가지고 있는지 추출
        
        print(f'{user_nickname}님 환영합니다.')   # 로그인에 성공한 사람의 닉네임이 뭔지 궁금하다
        sleep(2)
        return True

        
# 로그인 이후의 기능 메뉴
def print_phone_book_menu():
    print('===== 메인메뉴 =====')
    print('1. 전화번호 추가 등록')
    print('2. 전화번호 목록 조회')
    print('0. 로그아웃')
    print('===================')
    
    num = int(input('메뉴 선택 : '))
    return num

# 전화번호 추가 등록
def add_phone_num():
    # 1. DB에 넣어야할 항목들을 입력받기
    input_name = input('이름 : ')
    input_phone_num = input('연락처 : ')
    input_memo = input('특이사항 : ')
    
    # print('로그인한 사용자 아이디 : ', login_user_id)
    
    # 2. SQL 작성 (INSERT INTO로 데이터 추가) => user_id = ??처럼, DB의 본인 숫자를 찾아서 하드코딩으로 INSERT
    sql = f"INSERT INTO contacts (contacts.name, contacts.phone_num, contacts.memo, contacts.user_id) VALUES ('{input_name}', '{input_phone_num}', '{input_memo}', {login_user_id})"
    
    # 3. cursor / db_connect를 이용해서 실제 DB에 쿼리 날리기
    cursor.execute(sql)
    db_connect.commit()
    
    # 4. 안내메세지 2초간 출력 ('연락처 등록이 완료되었습니다.')
    print('연락처 등록이 완료되었습니다.')
    sleep(2)
    
    
    
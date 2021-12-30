import pymysql
from time import sleep
from datas import Contact

# DB 연결자체는 main.py에서 설정
# 여기서는 만들어진 연결정보를 받아서 사용하자

db_connect = pymysql.connect(
    host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com', 
    port=3306, 
    user='admin', 
    passwd='Vmfhwprxm!123',
    db= 'test_phone_book',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)  # SELECT의 결과를 tuple이 아니라 dict형태로 가져오도록 셋팅

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
        print(login_user)           # 로그인 사용자 정보를 , 딕셔너리형태로 모든 정보를 들고 있음        
        user_nickname = login_user['nickname']     # 사용자 정보 튜플에서 닉네임을 추출했다
        
        global login_user_id   # 상단에 만든 login_user_id 변수를 끌어다 쓰겠다 
        login_user_id = login_user['id']   # 로그인한 사용자(내가) 몇번 id를 가지고 있는지 추출
        
        print(f'{user_nickname}님 환영합니다.')   # 로그인에 성공한 사람의 닉네임이 뭔지 궁금하다
        sleep(2)
        return True

        
# 로그인 이후의 기능 메뉴
def print_phone_book_menu():
    print('===== 메인메뉴 =====')
    print('1. 전화번호 추가 등록')
    print('2. 전화번호 목록 조회')
    print('3. 내 전화번호부 검색')
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
 
 
# 로그인한 사용자가 등록한 모든 연락처 출력   
def show_all_contacts():
    # login_user_id만 갖고 있으면, 내가 가진 연락처 목록을 조회하는게 가능함
    # 추가 input은 필요 없다
    
    # 1. SQL 작성 -> 내 연락처 목록 불러오는 쿼리
    sql = f'SELECT * FROM contacts WHERE contacts.user_id = {login_user_id}'
    
    # 2. cursor => 쿼리 실행/실행 결과를 별도의 tuple에 담자
    cursor.execute(sql)
    contact_list = cursor.fetchall()
    
    # 3. 목록을 돌면서, 이름/연락처/메모를 가공하자 -> 조경진(메모사항) : 010-0000-0000
    for contact in contact_list:
        # print(contact)
        contact_name = contact['name']
        contact_phone = contact['phone_num']
        contact_memo = contact['memo']
        
        print(f'{contact_name}({contact_memo}) : {contact_phone}')
    
    print('모든 연락처를 불러왔습니다.')
    sleep(2)
    
    
# 전화번호부에서, 이름 기준으로 검색
def search_my_contact_list():
    input_keyword = input('검색할 이름의 일부를 입력 : ')  
    
    # 이름에 input_keyword를 포함하고있는 (내가 가진) 모든 연락처 목록을 조회
    sql = f"SELECT * FROM contacts WHERE contacts.user_id = {login_user_id} AND contacts.name LIKE '%{input_keyword}%'"
    # print('완성된 쿼리 : ', sql)
    
    # DB에서 쿼리 실행 -> 결과 출력
    cursor.execute(sql)
    result = cursor.fetchall()  # DB row들의 목록을 들고 있음 : 무조건 tuple형태로 반환
    
    # result : 검색 결과 목록 => 0개 ? 검색 결과 없음
    if len(result) == 0:
        print('검색 결과가 없습니다.')
        sleep(2)
    else:
        
        print('===== 검색결과 =====')
        # 검색 결과 확인 => 1. 이름(메모) ... 4. 이름4(메모4)
        for idx, row in enumerate (result):         # enumerate함수는 인덱스값과 데이터값 동시에 리턴
            line = f"{idx+1}.{row['name']} ({row['memo']})"
            print(line)
            
        # 몇번 연락처를 상세보기 할건지?
        contact_num = int(input('상세 보기 연락처 선택 : '))
        
        # contact_num에 맞는 line을 가지고 => (dict가 나옴) Contact 형태의 객체로 변환(클래스 활용)
        contact = Contact()    # 임시로, 기본값만 가지고 있는 연락처를 생성했다
        
        # 위치에 맞는 dict 꺼내오자 => dict의 내용을 가지고 contact객체의 내용물변수들을 채워주자
        #(클래스의 메쏘드를 추가하는 작업으로 대체하자 너무 반복되니까)
        select_line = result[contact_num-1]   # 위치에 맞는 dict 꺼내오는 작업
        
        contact.set_data(select_line)    # dict형태를 가지고, 클래스 인스턴스 만든 예제
        
        # cf) 클래스 객체를 가지고, dict로 변환해야하는 경우도 많다.
        # ==> 이 때도 메쏘드로 만들고 활용하자(향후 체험 예정)
        
        # 데이터 세팅 성공 여부 확인
        print(contact.name)
        
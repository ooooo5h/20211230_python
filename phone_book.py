import pymysql
from time import sleep
from datas import Contact
# DB 연결자체는 main.py에서 설정
# 만들어진 연결정보를 받아서 사용해보자
# 질문사항 추가사항들 커밋해보자.

db_connect = pymysql.Connect(
    host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com', 
    port=3306,
    user='admin',
    passwd='Vmfhwprxm!123',
    db='test_phone_book',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)     # SELECT의 결과를, 튜플이 아니라 dict형태로 가져오도록


# 쿼리를 날려주는 역할
cursor = db_connect.cursor()

# 로그인한 사용자가 몇번인지 변수로 저장
login_user_id = 0
###### 질문1: login_user_id변수를 앞단에 만든 이유는 아래 여러가지 함수들에서 끌어다써야하기때문인가?

def print_main_menu():
    print('===== 전화번호부 =====')
    print('1. 로그인 ')
    print('2. 회원가입')
    print('0. 프로그램 종료')
    print('=====================')
    menu_num = int(input('메뉴 선택 : '))
    return menu_num

# 회원가입 실행 함수 : DB에 쿼리를 날려주자
# 회원가입 => users 테이블에, 회원정보가 담긴 row 를 추가하자 => INSERT INTO 활용
def sign_up():
    input_email = input('가입 이메일 : ')
    input_password = input('비밀번호 : ')
    input_nickname = input('닉네임 : ')
    
    # INSERT INTO 쿼리의 VALUES에 들어가도록 처리하자
    # f string으로 실제 입력된 내용을 쿼리에 반영하자
    # SQL을 짤 때는 'string'형태로 처리를 해야하는 일이 빈번함
    # f"문장" 형태로, 큰 string은 " "로 감싸자
    sql = f"INSERT INTO users (users.email, users.password, users.nickname) VALUES ('{input_email}', '{input_password}', '{input_nickname}')"
    
    # print(sql)   # SQL어떻게 날라가는지 확인을 해보자
    
    cursor.execute(sql)
    db_connect.commit()
    
    print('회원가입이 완료되었습니다. 메인화면으로 돌아갑니다.')
    sleep(2)
    
# 로그인 (sign in) 기능
# 아이디/비밀번호를 입력받아서, DB에 정봊가 맞는 회원이 있는지 검색
# T/F 로 결과를 리턴
def sign_in():
    input_email = input('이메일 : ')
    input_pw = input('비밀번호 : ')
    
    # 아이디/비밀번호가 맞는 회원이 있는 지 조회하는 SELECT 쿼리를 날리자
    sql = f"SELECT * FROM users WHERE users.email = '{input_email}' AND users.password = '{input_pw}'"
    
    # 조회 쿼리 실행
    cursor.execute(sql)
    
    # cursor에는 실행 결과가 표로 담겨있음 이걸 튜플로 변환하자
    user_list = cursor.fetchall()
    
    # for문 => 내용확인용
    # for user in user_list:
    #     print(user)
    
    # 로그인에 성공이냐 실패의 판별 기준은  user_list의 갯수로!
    if len(user_list) == 0:
        print('잘못된 회원 정보입니다. 다시 로그인해주세요.')
        sleep(2)
        return False
    else:
        # user_list의 0번째 아이템에는 로그인에 성공한 사람의 정보가 담겨있다      
        login_user = user_list[0]
        # print(login_user)   # 로그인한 사용자의 모든 정보를 튜플이 아닌 딕셔너리로 담고있다.
        user_nickname = login_user['nickname']
        
        global login_user_id  ###### 최상단에서 만든 login_user_id변수를 끌어와서 사용하겠다고 명시
        login_user_id = login_user['id']  # 로그인한 사용자가 몇번 id를 가지고 있는지 추출
        ####### 질문1 : 그래서 로그인한 사용자의 id를 로긴유저id에 담아준거까지 이해했음

        print(f'{user_nickname}님, 환영합니다!')
        sleep(2)
        return True
    
# 로그인 이후의 기능 메뉴
def print_phone_book_menu():
    print('===== 메인 메뉴 =====')
    print('1. 전화번호 추가 등록')
    print('2. 전화번호 목록 조회')
    print('3. 내 전화번호부 검색')
    print('0. 로그아웃')
    print('=====================')
    num = int(input('메뉴 선택 : '))
    return num

# 추가 등록 함수
def add_phone_num():
    
    input_name = input('이름 : ')
    input_phone_num = input('연락처 : ')
    input_memo = input('특이사항 : ')
    
    sql = f"INSERT INTO contacts (contacts.name, contacts.phone_num, contacts.memo, contacts.user_id) VALUES ('{input_name}', '{input_phone_num}', '{input_memo}', {login_user_id})"
    ###### 질문2 : 앞단에서 만든 변수를 다른 함수에서 값을 대입시켰음 global을 써서.
    ###### 근데 또 새로운 함수에서 login_user_id를 호출할때, 앞단의 0이 담긴 변수가 아니라 다른 함수에서 이미 값이 변경된 변수를 가져온다???
    
    cursor.execute(sql)
    db_connect.commit()
    
    print('연락처 등록이 완료되었습니다.')
    sleep(2)
    
# 로그인한 사용자가 등록한 모든 폰번 출력
def show_all_contacts():
    # login_user_id만 갖고 있으면, 내가 가진 연락처 목록 조회가 가능하다
    # 추가 input필요없이, SQL 작성 / cursor 쿼리 실행 / 실행결과를 tuple에 담고, 목록을 돌면서 이름/폰번/메모를 조경진(메모사항) : 010-3333-3333 가공하기
    sql = f"SELECT * FROM contacts WHERE contacts.user_id = {login_user_id}"
    
    cursor.execute(sql)
    contacts_list = cursor.fetchall()
    
    for contact in contacts_list:
        name = contact['name']
        phone = contact['phone_num']
        memo = contact['memo']
        
        result_str = f'{name}({memo}) : {phone}'
        print(result_str)
        
    sleep(2)
    
# 내 전화번호부에서, 이름 기준 검색
def search_my_contact_list():
    input_keyword = input('검색할 이름의 일부를 입력 : ')
    
    # 이름에 input_keyword를 포함하고 있는 (내가 가진) 모든 연락처 목록을 조회
    sql = f"SELECT * FROM contacts WHERE contacts.user_id = {login_user_id} AND contacts.name LIKE '%{input_keyword}%'"
    # print('완성된 쿼리 ' ,sql)
    
    cursor.execute(sql)
    
    result = cursor.fetchall()   # DB row들의 목록을 담고 있는 tuple형태로 반환
    
    # result 검색결과목록 => 0개?면 검색결과 없음
    if len(result) == 0:
        print('검색 결과가 없습니다.')
        sleep(2)
    else: 
        print('===== 검색 결과 ======')
        # 검색 결과 확인
        for idx, row in enumerate(result):
            # print(row)    # 각각의 한줄은 dict로 불러옴
            line = f" {idx+1}. {row['name']} ({row['memo']})"
            print(line)
        
        # 몇번 연락처를 상세보기 할건지
        contact_num = int(input('상세보기 연락처 선택 : '))
        
        # contact_num에 맞는 line을 가지고 => 딕셔너리가 나옴 => Contact형태의 객체로 변환을 하자
        contact = Contact()  # 임시로, 기본값을 가지고 있는 연락처를 생성했다
        
        # 위치에 맞는 dict를 꺼내오고 => dict의 내용을 가지고 contact 객체의 내용물 변수들을 채워주자 (===> 클래스의 메쏘드로 추가하자)
        select_line = result[contact_num-1]    # 위치에 맞는 한 줄의 dict꺼내왔음
        contact.set_data(select_line)           # dict 형태를 가지고 클래스 인스턴스를 만든 예제
        
        # 연락처의 상세 정보 표시(메쏘드로 만들고 활용)
        detail_num = contact.show_detail_info()
        if detail_num == 1:
            new_name = input('변경할 이름 : ')
            update_contact(contact, new_name)
        elif detail_num == 2:
            delete_contact(contact)
        
# 연락처 수정
def update_contact(contact, value):
    # INSERT INTO를 실행시키는 파이썬 코드와 유사함
    sql = f"UPDATE contacts SET contacts.name = '{value}' WHERE contacts.id = {contact.id}"  ##### 질문3 : 여기서 쓰는 contact는 앞에서 만든 인스턴스를 끌어다가? 
    
    cursor.execute(sql)   # 변경 사항 알려줌
    db_connect.commit()   # 변경사항 실제 반영
    print('연락처 변경 완료')
    sleep(2)

# 연락처 삭제
def delete_contact(contact):
    # DELETE문을 선택한 연락처만 지우자
    sql = f"DELETE FROM contacts WHERE contacts.id = {contact.id}"
    
    cursor.execute(sql)
    db_connect.commit()
    print('연락처 삭제 완료')
    sleep(2)
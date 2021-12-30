# PyMySQL - DB서버 연동 체험
# main.py - 단순 동작 위주의 코드만 작성할 예정
# DB연결 관련된 기타 기능 : phone_book.py 모듈 이용 예정

from time import sleep
from phone_book import add_phone_num, print_main_menu, sign_up, sign_in, print_phone_book_menu

# 프로그램이 종료될 사유가 생길때까지 무한반복 시켜주기
while True:
    menu_num = print_main_menu()

    if menu_num == 1:
        login_result = sign_in()
        
        # 로그인에 성공하면 개인별 연락처 메뉴로 이동시키기
        if login_result:
            while True:
                num = print_phone_book_menu()
                if num == 0:
                    print('로그아웃 후 메인으로 돌아갑니다.')
                    sleep(2)
                    break
                
                if num == 1:
                    add_phone_num()
                
    elif menu_num == 2:
        sign_up()
    elif menu_num == 0:
        print('프로그램을 종료합니다.')
        break
    
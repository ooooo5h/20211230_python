# PyMySQL - DB서버 연동 체험
# main.py - 단순 동작 위주의 코드만 작성할 예정
# DB연결 관련된 기타 기능 : phone_book.py 모듈 이용 예정

from phone_book import print_main_menu, sign_up

menu_num = print_main_menu()

if menu_num == 1:
    pass
elif menu_num == 2:
    sign_up()
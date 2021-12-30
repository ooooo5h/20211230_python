# PyMySQL - DB서버 연동 체험
# main.py - 단순 동작 위주의 코드만 작성할 예정
# DB연결 관련된 기타 기능 : phone_book.py 모듈 이용 예정

from phone_book import print_main_menu, sign_up, sign_in

# 프로그램이 종료될 사유가 생길때까지 무한반복 시켜주기
while True:
    menu_num = print_main_menu()

    if menu_num == 1:
        sign_in()
    elif menu_num == 2:
        sign_up()
    elif menu_num == 0:
        print('프로그램을 종료합니다.')
        break
    
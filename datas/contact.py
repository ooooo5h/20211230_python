# 연락처를 표현하는 파일 (DB에 있는 contacts 테이블에 대응)
# 연락처 관련된 메쏘드들을 내포할 예정

class Contact:
    def __init__(self):
        # 객체 변수 생성해서, 기본값들만 대입을 해보자
        self.id = 0      # 임시로 int인 0으로 대입(나중에 int가 올거라 암시)
        self.user_id = 0
        self.name = ''
        self.phone_num = ''
        self.memo = ''
        
    # dict를 재료로 받아서, 객체 변수의 값들을 채워주는 기능
    def set_data(self, info_dict):
        self.id = info_dict['id']
        self.user_id = info_dict['user_id']
        self.name = info_dict['name']
        self.phone_num = info_dict['phone_num']
        self.memo = info_dict['memo']
        
    # 상세보기 기능 추가
    def show_detail_info(self):
        print('===== 연락처 상세 보기 =====')
        print(f'이름 : {self.name}')
        print(f'연락처 : {self.phone_num}')
        print(f'메모사항 : {self.memo}')
        
        # 정보 수정 / 삭제하는 기능도 선택 지원하자
        print('===========================')
        print('1. 연락처 수정')
        print('2. 연락처 삭제')
        print('0. 이전 메뉴로 돌아가기')
        print('===========================')
        return int(input('추가 행동 선택 : '))
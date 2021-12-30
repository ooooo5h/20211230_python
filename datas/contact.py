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
        
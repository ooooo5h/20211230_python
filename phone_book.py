# DB 연결자체는 main.py에서 설정
# 여기서는 만들어진 연결정보를 받아서 사용하자

db_connect = None

# 쿼리를 날리는 역할
cursor = None

def set_db_info(connect):
    # 비어있는 db_connect 변수에 연결정보를 대입하자
    db_connect = connect 
    cursor = db_connect.cursor()
from sqlalchemy import text

def get_check_user_id_stmt(user_id: str):
    print(f"🔍 사용자 ID 확인 쿼리 실행: user_id={user_id}")
    return text("""
        SELECT 1 FROM members
        WHERE user_id = :user_id
        LIMIT 1
    """), {"user_id": user_id}


def get_login_stmt(user_id: str, password: str):
    print(f"🔐 로그인 쿼리 실행: user_id={user_id}, password='***'")
    return text("""
        SELECT * FROM members
        WHERE user_id = :user_id AND password = :password
        LIMIT 1
    """), {
        "user_id": user_id,
        "password": password
    }
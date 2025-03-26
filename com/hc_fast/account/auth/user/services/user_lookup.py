from sqlalchemy import Result
from com.hc_fast.account.auth.user.repository.find_user import get_check_user_id_stmt, get_login_stmt
from com.hc_fast.utils.creational.abstract.abstract_service import AbstractService
import traceback


class Login(AbstractService):
    async def handle(self, **kwargs):
        print("😁😁😁😁Login 진입함")
        try:
            user_schema = kwargs.get("user_schema")
            db = kwargs.get("db")
            print("🐍🐍🐍🐍user_schema : ", user_schema)
            # user_schema는 dict 또는 객체라고 가정
            # user_schema는 dict 또는 Pydantic 모델
            user_dict = user_schema if isinstance(user_schema, dict) else user_schema.dict()

            user_id = user_dict.get("user_id")
            password = user_dict.get("password")

            print(f"🔑 로그인 시도: user_id={user_id}, 비밀번호 길이={len(password)}")

            # 1단계: user_id 존재 여부 확인
            check_stmt, check_params = get_check_user_id_stmt(user_id)
            check_result: Result = await db.execute(check_stmt, check_params)

            user_exists = check_result.fetchone()
            print(f"👤 사용자 ID 존재 확인 결과: {user_exists is not None}")

            if user_exists is None:
                return {
                    "status": "error",
                    "message": "고객에서 등록된 ID가 없습니다",
                    "user": None
                }

            # 2단계: user_id + password 검사
            login_stmt, login_params = get_login_stmt(user_id, password)
            login_result: Result = await db.execute(login_stmt, login_params)

            logged_in_user = login_result.fetchone()
            print(f"🔐 로그인 결과: {logged_in_user is not None}")

            if logged_in_user is None:
                return {
                    "status": "error",
                    "message": "비밀번호가 일치하지 않습니다",
                    "user": None
                }

            # 3단계: 로그인 성공
            user_data = dict(logged_in_user._mapping)
            # 비밀번호 필드 제거
            user_data.pop('password', None)
            
            print("✅ 로그인 성공: 사용자 데이터=", user_data)
            
            return {
                "status": "success",
                "message": "로그인에 성공했습니다",
                "user": user_data
            }
        except Exception as e:
            print(f"❌ 로그인 처리 중 오류 발생: {str(e)}")
            traceback.print_exc()
            return {
                "status": "error",
                "message": f"로그인 처리 중 오류가 발생했습니다: {str(e)}",
                "user": None
            }

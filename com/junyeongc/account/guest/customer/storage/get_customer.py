from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService
from com.junyeongc.account.auth.user.model.user_entity import UserEntity
import logging

# 로거 설정
logger = logging.getLogger(__name__)

class GetAllRepository(AbstractService):
    async def handle(self, **kwargs):
        logger.info("🎉 GetAllRepository.retrieve 메서드 실행")
        db: AsyncSession = kwargs.get('db')
        try:
            # SQLAlchemy Core를 사용한 쿼리 (명시적으로 text() 함수 사용)
            stmt = select(UserEntity)
            logger.info(f"💬 실행할 쿼리: {stmt}")
            
            result = await db.execute(stmt)
            rows = result.fetchall()
            
            logger.info(f"💯 조회된 행 수: {len(rows) if rows else 0}")
            
            if rows:
                # Row 객체를 딕셔너리로 변환하고 비밀번호 필드 제거
                customers = []
                for row in rows:
                    customer_dict = row[0].__dict__.copy()  # UserEntity 객체를 딕셔너리로 변환
                    customer_dict.pop('_sa_instance_state', None)  # SQLAlchemy 내부 상태 제거
                    customer_dict.pop('password', None)  # 비밀번호 필드 제거
                    customers.append(customer_dict)
                
                logger.info(f"💯 변환된 고객 데이터 수: {len(customers)}")
                return {
                    "status": "success",
                    "message": "회원 목록 조회 성공",
                    "customers": customers
                }
            else:
                logger.warning("⚠️ 조회된 데이터가 없습니다.")
                return {
                    "status": "success",
                    "message": "조회된 회원이 없습니다",
                    "customers": []
                }
                
        except Exception as e:
            logger.error(f"⚠️ 데이터 조회 중 오류 발생: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "message": f"데이터 조회 중 오류가 발생했습니다: {str(e)}",
                "customers": []
            }

class GetDetailRepository(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.retrieve(db, user_id)
        
    async def retrieve(self, db: AsyncSession, user_id: str):
        try:
            logger.info(f"🔍 GetDetailRepository.retrieve 메서드 실행 - user_id: {user_id}")
            
            # SQLAlchemy Core를 사용한 쿼리
            stmt = select(UserEntity).where(UserEntity.user_id == user_id)
            result = await db.execute(stmt)
            row = result.first()
            
            if row:
                customer_dict = row[0].__dict__.copy()
                customer_dict.pop('_sa_instance_state', None)
                customer_dict.pop('password', None)
                
                logger.info(f"✅ 회원 상세 조회 성공: {user_id}")
                return {
                    "status": "success",
                    "message": "회원 상세 조회 성공",
                    "customer": customer_dict
                }
            else:
                logger.warning(f"⚠️ 회원을 찾을 수 없음: {user_id}")
                return {
                    "status": "error",
                    "message": "해당 회원을 찾을 수 없습니다",
                    "customer": None
                }
                
        except Exception as e:
            logger.error(f"⚠️ 회원 상세 조회 중 오류 발생: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "message": f"회원 상세 조회 중 오류가 발생했습니다: {str(e)}",
                "customer": None
            }
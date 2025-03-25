from fastapi import APIRouter, Depends
from sqlalchemy import text
from com.junyeongc.account.staff.manager.web.manager_controller import ManagerController
from com.junyeongc.utils.creational.builder.db_builder import get_db
import logging

# 로거 설정
logger = logging.getLogger(__name__)

router = APIRouter()
controller = ManagerController()

@router.post(path="/create")
async def create_manager():
    return controller.create_manager()

@router.post(path="/detail")
async def get_manager_detail():
    return controller.hello_manager()

@router.get("/list")
async def get_manager_list(db=Depends(get_db)):
    logger.info("🎉 get_managers 엔드포인트 호출됨")
    # text() 함수로 SQL 쿼리 감싸기
    query = text("SELECT * FROM members")  

    try:
        logger.info(f"💬 실행할 쿼리: {query}")
        rows = await db.fetch(query)  
        logger.info(f"💯 데이터 조회 결과: {len(rows)}개 행 반환됨")
        
        managers = [dict(record) for record in rows]
        return {"managers": managers}
    except Exception as e:
        error_msg = f"⚠️ 데이터 조회 중 오류 발생: {str(e)}"
        logger.error(error_msg)
        import traceback
        logger.error(traceback.format_exc())
        return {"status": "error", "message": f"데이터 조회 중 오류가 발생했습니다: {str(e)}"}
    
@router.post(path="/update")
async def update_manager():
    return controller.hello_manager()

@router.post(path="/delete")
async def delete_manager():
    return controller.hello_manager()
    
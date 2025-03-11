from fastapi import APIRouter, Depends
from sqlalchemy import text
from com.junyeongc.account.staff.manager.web.manager_controller import ManagerController
from com.junyeongc.utils.creational.builder.db_builder import get_db

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
    print("🎉🎉 get_managers 로 진입함")
    query = "SELECT * FROM members"  

    try:
        rows = await db.fetch(query)  
        print("💯🌈 데이터 조회 결과:", rows)
        managers = [dict(record) for record in rows]
        return {"managers": managers}
    except Exception as e:
        print("⚠️ 데이터 조회 중 오류 발생:", str(e))
        return {"error": "데이터 조회 중 오류가 발생했습니다."}
    
@router.post(path="/update")
async def update_manager():
    return controller.hello_manager()

@router.post(path="/delete")
async def delete_manager():
    return controller.hello_manager()
    
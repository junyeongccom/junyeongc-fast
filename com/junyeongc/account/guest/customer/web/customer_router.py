from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.web.customer_controller import CustomerController
from com.junyeongc.utils.creational.builder.db_builder import get_db

router = APIRouter()
controller = CustomerController()

@router.post(path="/create")
async def create_customer():
    return controller.create_customer()

@router.post(path="/detail")
async def get_customer_detail():
    return controller.hello_customer()

@router.get("/list")
async def get_customer_list(db:AsyncSession=Depends(get_db)):  
    print("🎉🎉 get_customers 로 진입함")
    query = text("SELECT * FROM members")  # ✅ Raw SQL 사용

    try:
        results = await db.fetch(query)  # ✅ `fetch()` 사용하여 모든 데이터 가져오기
        print("💯🌈 데이터 조회 결과:", results)

        # ✅ `dict(record)`를 사용하여 JSON 변환
        customers = [dict(record) for record in results]
        return {"customers": customers}
    except Exception as e:
        print("⚠️ 데이터 조회 중 오류 발생:", str(e))
        return {"error": "데이터 조회 중 오류가 발생했습니다."}
    
@router.post(path="/update")
async def update_customer():
    return controller.hello_customer()

@router.post(path="/delete")
async def delete_customer():
    return controller.hello_customer()
    
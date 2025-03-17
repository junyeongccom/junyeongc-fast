from fastapi import APIRouter, Depends, Body
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.api.customer_controller import CustomerController
from com.junyeongc.utils.creational.builder.db_builder import get_db
from com.junyeongc.account.guest.customer.models.customer_schema import CustomerSchema

router = APIRouter()
controller = CustomerController()

@router.post(path="/create")
async def create_customer(customer: CustomerSchema = Body(...), db: AsyncSession = Depends(get_db)):
    print("🎉🎉 create_customer 라우터 진입")
    print("📝 받은 회원 정보:", customer)
    try:
        result = await controller.create_customer(db=db, customer_data=customer)
        print("✅ 회원가입 결과:", result)
        return result
    except Exception as e:
        print("⚠️ 회원가입 처리 중 오류 발생:", str(e))
        return {"status": "error", "message": f"회원가입 처리 중 오류가 발생했습니다: {str(e)}"}

@router.get(path="/detail")
async def get_customer_detail(db:AsyncSession=Depends(get_db)):
    print("🎉🎉 get_customer_detail 라우터 진입")
    return await controller.get_customer_detail(db=db)

@router.get("/list")
async def get_customer_list(db:AsyncSession=Depends(get_db)):  
    print("🎉🎉 get_customers 라우터 진입")
    return await controller.get_customer_list(db=db)
    
@router.post(path="/update")
async def update_customer(db:AsyncSession=Depends(get_db)):
    print("🎉🎉 update_customer 라우터 진입")
    return await controller.update_customer(db=db)

@router.post(path="/delete")
async def delete_customer(db:AsyncSession=Depends(get_db)):
    print("🎉🎉 delete_customer 라우터 진입")
    return await controller.delete_customer(db=db)
    
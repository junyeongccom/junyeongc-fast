from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.models.customer_schema import CustomerSchema
from com.junyeongc.account.guest.customer.storage.create_customer import DefaultCreateRepository
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService


class CustomerCreate(AbstractService):

    async def handle(self, db: AsyncSession, **kwargs):
        new_customer = kwargs.get('customer_data')
        customer_repo = DefaultCreateRepository()
        return await customer_repo.create(db, new_customer)

# 팩토리 패턴에서 사용할 전략 클래스 추가
class DefaultCreateStrategy:
    async def create(self, db: AsyncSession, **kwargs):
        customer_data = kwargs.get('customer_data')
        print("🔍 DefaultCreateStrategy에서 받은 데이터:", customer_data)
        customer_service = CustomerCreate()
        return await customer_service.handle(db, customer_data=customer_data)

class ValidatedCreateStrategy:
    async def create(self, db: AsyncSession, **kwargs):
        # 유효성 검사 로직 추가
        customer_data = kwargs.get('customer_data')
        print("🔍 ValidatedCreateStrategy에서 받은 데이터:", customer_data)
        # 여기에 유효성 검사 코드 추가
        
        customer_service = CustomerCreate()
        return await customer_service.handle(db, customer_data=customer_data)
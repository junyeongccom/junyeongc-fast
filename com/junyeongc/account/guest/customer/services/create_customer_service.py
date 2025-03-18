from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.guest.customer.models.customer_schema import CustomerSchema
from com.junyeongc.account.guest.customer.storage.create_customer import DefaultCreateRepository
from com.junyeongc.utils.creational.abstract.abstract_service import AbstractService


class CreateCustomer(AbstractService):

    async def handle(self, db: AsyncSession, **kwargs):
        # 모든 로직을 handle 메서드로 통합
        customer_data = kwargs.get('customer_data')
        print("🔍 CreateCustomer에서 받은 데이터:", customer_data)
        customer_repo = DefaultCreateRepository()
        return await customer_repo.create(db, customer_data)

# ValidatedCreateStrategy는 handle 메서드로 변경
class ValidatedCreateStrategy(AbstractService):
    async def handle(self, db: AsyncSession, **kwargs):
        # 유효성 검사 로직 추가
        customer_data = kwargs.get('customer_data')
        print("🔍 ValidatedCreateStrategy에서 받은 데이터:", customer_data)
        # 여기에 유효성 검사 코드 추가
        
        customer_service = CreateCustomer()
        return await customer_service.handle(db, customer_data=customer_data)
from sqlalchemy.ext.asyncio import AsyncSession
from com.junyeongc.account.staff.manager.model.manager_entity import ManagerEntity
from com.junyeongc.account.staff.manager.model.manager_schema import ManagerSchema
from com.junyeongc.account.staff.manager.service.create_service import CreateService



class DefaultCreateRepository(CreateService):
    async def create(self, db: AsyncSession, new_customer: ManagerSchema):
        print("😃😃Repository new_customer wjdqh:", new_customer)
        db.add(ManagerEntity(
            user_id = new_customer.user_id,
            name = new_customer.name,
            password = new_customer.password,
            email = new_customer.email
        ))
        db.commit()
        db.refresh(new_customer)
        return new_customer
        
class ValidatedCreateRepository(CreateService):
    async def create(self, db: AsyncSession, new_customer: ManagerSchema):
        pass
from sqlalchemy.orm import Session
from com.junyeongc.account.staff.manager.model.manager_schema import ManagerSchema
from com.junyeongc.account.staff.manager.service.create_service import CreateService



class DefaultCreateStrategy(CreateService):
    def create(self, db: Session, new_manager: ManagerSchema):
        manager_repo = DefaultCreateStrategy(db)
        return manager_repo.create(new_manager)

class ValidatedCreateStrategy(CreateService):
    def create(self, db: Session, new_manager: ManagerSchema):
        pass
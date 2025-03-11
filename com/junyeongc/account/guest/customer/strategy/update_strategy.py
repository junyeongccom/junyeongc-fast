from sqlalchemy.orm import Session
from com.junyeongc.account.guest.customer.service.update_service import UpdateService

class FullUpdateStrategy(UpdateService):
    def update(self, db: Session, user_id: str):
        pass

class PartialUpdateStrategy(UpdateService):
    def update(self, db: Session, user_id: str):
        pass
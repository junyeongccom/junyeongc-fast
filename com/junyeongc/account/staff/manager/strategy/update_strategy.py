from sqlalchemy.orm import Session
from com.junyeongc.account.staff.manager.service.update_service import UpdateService


class FullUpdateStrategy(UpdateService):
    def delete(self, db: Session, user_id: str):
        pass

class PartialUpdateStrategy(UpdateService):
    def delete(self, db: Session, user_id: str):
        pass
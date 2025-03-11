from sqlalchemy.orm import Session
from com.junyeongc.account.guest.customer.service.delete_service import DeleteService


class SoftDeleteStrategy(DeleteService):
    def delete(self, db: Session, user_id: str):
        pass


class HardDeleteStrategy(DeleteService):
    def delete(self, db: Session, user_id: str):
        pass

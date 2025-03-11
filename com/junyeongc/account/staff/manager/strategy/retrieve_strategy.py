from sqlalchemy.orm import Session
from com.junyeongc.account.staff.manager.service.retrieve_service import RetrieveService

class GeatAllStrategy(RetrieveService):
    def retrieve(self, db: Session, **kwargs):
        pass

class GetListStrategy(RetrieveService):
    def delete(self, db: Session, user_id: str):
        pass

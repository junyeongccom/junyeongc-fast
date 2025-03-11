from com.junyeongc.account.guest.customer.service.retrieve_service import RetrieveService
from sqlalchemy.orm import Session

class GetAllStrategy(RetrieveService):
    def retrieve(self, db: Session, **kwargs):
        pass

class GetDetailStrategy(RetrieveService):
    def retrieve(self, db: Session, user_id: str):
        pass

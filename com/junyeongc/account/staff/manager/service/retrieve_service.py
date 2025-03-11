from abc import ABC, abstractmethod
from sqlalchemy.orm import Session



class RetrieveService(ABC):

    @abstractmethod
    def retrieve(self, db: Session, **kwargs):
        pass


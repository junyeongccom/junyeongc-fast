from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()

class UserEntity(Base):
    __tablename__ = "members"

    user_id = Column(String(15), primary_key=True, index=True)
    email = Column(String(20), unique=True, nullable=False)
    password = Column(String(15), nullable=False)
    name = Column(String(10), nullable=False)

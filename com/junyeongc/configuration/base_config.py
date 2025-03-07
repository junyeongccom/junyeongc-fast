from pydantic import BaseModel

class BaseConfig(BaseModel):
    """공통 설정을 위한 베이스 클래스"""

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
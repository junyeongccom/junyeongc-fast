from pydantic import BaseModel

class MemberSchema(BaseModel):
    user_id: str  
    name: str
    email: str

    class Config:
        from_attributes = True 

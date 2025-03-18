from pydantic import BaseModel

class UserSchema(BaseModel):
    user_id: str  
    name: str
    email: str
    password : str
    class Config:
        from_attributes = True

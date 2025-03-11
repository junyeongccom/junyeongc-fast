from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    user_id: str  
    name: str
    email: EmailStr
    password : str
    class Config:
        from_attributes = True

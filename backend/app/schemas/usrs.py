from pydantic import BaseModel, ConfigDict
from typing import Optional
class UsersRegister_Base(BaseModel):
    username: str
    email: str 
    password: str
    phone: Optional[str] = None
    city: Optional[str] = None

class UserLogin_Base(BaseModel):
    email:str
    password:str 

class UserResponse_Base(BaseModel):
    id:int 
    username: str
    email:str
    role:str
    is_active:int 
    phone: Optional[str] = None
    city: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
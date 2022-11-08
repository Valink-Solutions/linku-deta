from typing import Optional
from pydantic import BaseModel, EmailStr

# Utility Models
class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = 'Bearer'
    
    
class TokenData(BaseModel):
    email: str
    # scopes: dict | None = None
    
    
class VerifyToken(BaseModel):
    token: str
    
    
class RequestReset(BaseModel):
    email: EmailStr
    
    
class ResetPassword(BaseModel):
    token: str
    password: str
    
    
class RequestVerification(BaseModel):
    email: EmailStr
    

class StatusCheck(BaseModel):
    name: str
    version: str
    description: str
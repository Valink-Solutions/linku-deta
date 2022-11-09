from datetime import datetime
import time
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, validator


class CreateLink(BaseModel):
    title: str = Field(...)
    short_code: Optional[str] = Field(min_length=4, max_length=15)
    long_url: HttpUrl = Field(...)
    # is_protected: Optional[bool] = Field(default=False)
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Literally Google",
                "short_code": "google",
                "long_url": "https://www.google.com"
            }
        }
        
        
class LinkInDB(BaseModel):
    
    title: str = Field(...)
    
    long_url: HttpUrl = Field(...)
    # is_protected: Optional[bool] = Field(default=False)
    
    daily_clicks: int = Field(default=0)
    
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%b %d, %Y"))
    updated_at: str = Field(default_factory=lambda: datetime.now().strftime("%b %d, %Y, %H:%M:%S"))
    

class ShowLink(BaseModel):
    short_code: str = Field(alias="key")
    title: str
    long_url: HttpUrl
    daily_clicks: int
    created_at: str
    updated_at: str
    

class LinksResponse(BaseModel):
    count: int
    last: Optional[str] = None
    items: List[ShowLink]

    class Config:
        orm_mode = True
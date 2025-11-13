from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # setting optional field and defalt value

#post schemas
class PostCreate(PostBase):
    pass
   
class Post(PostBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


#user schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

#Auth
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#tokens
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
     id: int | None = None 
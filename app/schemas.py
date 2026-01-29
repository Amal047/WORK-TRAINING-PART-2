from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Annotated

from pydantic import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # setting optional field and defalt value

#post schemas
class PostCreate(PostBase):
    pass

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
   
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

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

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1)]
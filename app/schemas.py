from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class donfig:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #id: int

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    vote_dir: Literal[0, 1]
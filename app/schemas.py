from pydantic import BaseModel, EmailStr # using for creating schemma
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# schema for validating recieving data
class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True # default value is true

class PostCreate(PostBase):
    pass

# response data    number: 3 
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

# response
class Post(PostBase): # inherite title, content, published from PostBase
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # also returning the owner of the post
    class Config: # tell pydantic model to read the data even if it's not dictionary
        from_attributes = True

# recieve data
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# response moved up number: 3


# Authenticatoin
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


# schema for voitnig
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # probelm: allows for negetive num -> le; less than or equal

# schema for returning the post with their like num
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
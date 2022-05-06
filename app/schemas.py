import email
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

'''
class Post(BaseModel):     #Data Validation of PostMan Body Post field, If not sent correct data its throw an Error
    title: str
    content: str
    published: bool = True #Default Value setting
    #rating: Optional[int] = None #Setting optional field with Default Value 
'''

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase): 
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True  

class Post(PostBase):  #doing inheritance
    #title: str      #this 3 field in PostBase
    #content: str
    #published: bool
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True     #orm_mode will tell the Pydantic model to read the data even if it is not a dict

class PostOut(BaseModel):
    Post: Post
    votes: int

'''
class CreatePost(BaseModel):     #Data Validation of PostMan Body Post field, If not sent correct data its throw an Error
    title: str
    content: str
    published: bool = True 

class UpdatePost(BaseModel):     #Data Validation of PostMan Body Post field, If not sent correct data its throw an Error
    title: str
    content: str
    published: bool  #if allow user to edit one field keep that in this class
'''

class UserCreate(BaseModel):
    email: EmailStr       #using pydantic model to check whether its vaild email or not
    password: str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
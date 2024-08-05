from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import Field

class Config:
    orm_mode = True

# USERS
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    # creaated_at: datetime

class UserOutForGet(BaseModel):
    email: EmailStr
    name: str


# Reviews
class ReviewBase(BaseModel):
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating should be between 1 and 5")

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating should be between 1 and 5")

class Review(BaseModel):
    id: int
    user_id: int
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating should be between 1 and 5")
    owner: UserOutForGet  #pydantic model


# login 
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


# contacts
class ContactBase(BaseModel):
    name: str
    email: EmailStr
    message: str
    phone_nr: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    user_id: Optional[int]
    created_at: datetime

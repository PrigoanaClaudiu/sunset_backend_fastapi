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
    role: str
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

class ReviewVerf(BaseModel):
    id: int
    user_id: int
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating should be between 1 și 5")

# login 
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str
    user_email: str
    role: str


class TokenData(BaseModel):
    id: Optional[str] = None


# contacts
class ContactBase(BaseModel):
    message: str
    phone_nr: str

class ContactCreate(ContactBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class Contact(ContactBase):
    id: int
    user_id: Optional[int]
    name: str  
    email: EmailStr  
    created_at: datetime


# reservations
# class ReservationBase(BaseModel):
#     name: str
#     email: EmailStr
#     phone_nr: str
#     details: str
#     no_pers: int
#     data_start: datetime
#     data_finish: datetime


# class ReservationCreate(ReservationBase):
#     pass

# class Reservation(ReservationBase):
#     id: int
#     user_id: Optional[int]
#     created_at: datetime

class ReservationBase(BaseModel):
    no_pers: int
    details: Optional[str] = None
    phone_nr: str
    data_start: datetime
    data_finish: datetime

class ReservationCreate(ReservationBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class Reservation(ReservationBase):
    id: int
    user_id: Optional[int]
    name: str 
    email: EmailStr  
    created_at: datetime

class AvailabilityRequest(BaseModel):
    data_start: datetime
    data_finish: datetime
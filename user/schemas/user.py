from pydantic import BaseModel, EmailStr

from user.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    email: EmailStr
    password: str
    role: UserRole


class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime
from core.database import Base
from datetime import datetime, timezone
import enum
from sqlalchemy import Enum
from pydantic import EmailStr, BaseModel

class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String(64), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        default=UserRole.staff,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
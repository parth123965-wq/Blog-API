from sqlalchemy import  String , DateTime , Enum , Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime , timezone
import enum

# UserRole Class.
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

# Table For Users.
class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), 
        default=UserRole.USER, 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    
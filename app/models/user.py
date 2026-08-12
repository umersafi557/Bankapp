import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class UserRole(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    SYSTEM = "SYSTEM"


class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    wallets = relationship("Wallet", back_populates="user")

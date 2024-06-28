import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "Пользователи"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
        comment="Идентификатор пользователя",
    )
    login = Column(
        String(255), unique=True, nullable=False, comment="Логин пользователя"
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        comment="Электронный адрес пользователя",
    )
    password = Column(String(255), nullable=False, comment="Пароль пользователя")
    first_name = Column(String(50), comment="Имя пользователя")
    last_name = Column(String(50), comment="Фамилия пользователя")

    authentication_histories = relationship(
        "AuthenticationHistory", back_populates="user"
    )
    oauth_accounts = relationship("OAuthAccount", back_populates="user")

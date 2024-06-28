import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base


class AuthenticationHistory(Base):
    __tablename__ = "authentication_histories"
    __table_args__ = (
        UniqueConstraint("id", "user_id"),
        {
            "comment": "История аутентификации пользователей",
            "postgresql_partition_by": "HASH (user_id)",
        },
    )

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
        comment="Идентификатор аутентификации",
    )
    success = Column(
        Boolean,
        nullable=False,
        comment="Флаг, указывающий, был ли вход успешным (True) или нет (False)",
    )
    user_agent = Column(
        String, comment="Информация о браузере и операционной системе пользователя"
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        primary_key=True,
        comment="Идентификатор пользователя, связанного с этой записью о входе",
    )
    user = relationship("User", back_populates="authentication_histories")

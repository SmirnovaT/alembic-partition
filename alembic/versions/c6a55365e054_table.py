"""table

Revision ID: c6a55365e054
Revises: 
Create Date: 2024-06-28 13:44:54.333126

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c6a55365e054"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id", sa.UUID(), nullable=False, comment="Идентификатор пользователя"
        ),
        sa.Column(
            "login", sa.String(length=255), nullable=False, comment="Логин пользователя"
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
            comment="Электронный адрес пользователя",
        ),
        sa.Column(
            "password",
            sa.String(length=255),
            nullable=False,
            comment="Пароль пользователя",
        ),
        sa.Column(
            "first_name",
            sa.String(length=50),
            nullable=True,
            comment="Имя пользователя",
        ),
        sa.Column(
            "last_name",
            sa.String(length=50),
            nullable=True,
            comment="Фамилия пользователя",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("login"),
        comment="Пользователи",
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=True)
    op.create_table(
        "authentication_histories",
        sa.Column(
            "id", sa.UUID(), nullable=False, comment="Идентификатор аутентификации"
        ),
        sa.Column(
            "success",
            sa.Boolean(),
            nullable=False,
            comment="Флаг, указывающий, был ли вход успешным (True) или нет (False)",
        ),
        sa.Column(
            "user_agent",
            sa.String(),
            nullable=True,
            comment="Информация о браузере и операционной системе пользователя",
        ),
        sa.Column(
            "user_id",
            sa.UUID(),
            nullable=False,
            comment="Идентификатор пользователя, связанного с этой записью о входе",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="История аутентификации пользователей",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("authentication_histories")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###

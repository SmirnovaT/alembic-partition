"""part

Revision ID: 28c430440d10
Revises: f9f39b7e37e9
Create Date: 2024-06-28 14:19:57.753048

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "28c430440d10"
down_revision: Union[str, None] = "f9f39b7e37e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authentication_histories_hash",
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
        sa.UniqueConstraint("id", "user_id"),
        comment="История аутентификации пользователей",
        postgresql_partition_by="HASH (user_id)",
    )
    op.execute(
        """CREATE TABLE authentication_histories_000 PARTITION OF 
            authentication_histories_hash FOR VALUES WITH (MODULUS 4, REMAINDER 0);"""
    )

    op.execute(
        """CREATE TABLE authentication_histories_001 PARTITION OF 
            authentication_histories_hash FOR VALUES WITH (MODULUS 4, REMAINDER 1);"""
    )

    op.execute(
        """CREATE TABLE authentication_histories_002 PARTITION OF 
            authentication_histories_hash FOR VALUES WITH (MODULUS 4, REMAINDER 2);"""
    )

    op.execute(
        """CREATE TABLE authentication_histories_003 PARTITION OF 
            authentication_histories_hash FOR VALUES WITH (MODULUS 4, REMAINDER 3);"""
    )

    op.execute(
        """INSERT INTO authentication_histories_hash 
            SELECT * FROM authentication_histories"""
    )

    op.drop_table("authentication_histories")
    op.rename_table("authentication_histories_hash", "authentication_histories")


def downgrade() -> None:
    op.drop_table("authentication_histories_000")
    op.drop_table("authentication_histories_001")
    op.drop_table("authentication_histories_002")
    op.drop_table("authentication_histories_003")

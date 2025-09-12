"""Refresh token table added

Revision ID: 20250912_050011
Revises: 20250912_044330
Create Date: 2025-09-12 10:45:11.849314

"""

from typing import Sequence, Union

from migrations.base import BaseMigration

revision: str = "20250912_050011"
down_revision: Union[str, Sequence[str], None] = "20250912_044330"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class RefreshTokenMigration(BaseMigration):

    table_name = "auth_refresh_tokens"

    def __init__(self):
        super().__init__(revision="20250912_050011", down_revision="20250912_044330")
        self.create_whole_table = True
        # describe your schemas here
        self.base_columns()
        self.timestamp_mixin_columns()
        self.foreign(
            name="user_id",
            table="sys_users",
            ondelete="CASCADE",
            index=True,
            nullable=False,
        )
        self.string(name="refresh_token", nullable=False)
        self.date_time(name="expires_at", nullable=False)


def upgrade() -> None:
    """
    Function to create a table
    """
    RefreshTokenMigration().upgrade()


def downgrade() -> None:
    """
    Function to drop a table
    """
    RefreshTokenMigration().downgrade()

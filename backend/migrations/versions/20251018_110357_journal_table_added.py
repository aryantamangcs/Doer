"""journal table added

Revision ID: 20251018_110357
Revises: 20250930_104416
Create Date: 2025-10-18 16:48:58.267608

"""

from typing import Sequence, Union

from migrations.base import BaseMigration

revision: str = "20251018_110357"
down_revision: Union[str, Sequence[str], None] = "20250930_104416"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class JournalMigration(BaseMigration):

    table_name = "sys_journal"

    def __init__(self):
        super().__init__(revision="20251018_110357", down_revision="20250930_104416")
        self.create_whole_table = True
        # describe your schemas here
        self.base_columns()
        self.timestamp_mixin_columns()
        self.string(name="title", nullable=False)
        self.text(name="content", nullable=False)
        self.foreign(
            name="created_by", table="sys_users", ondelete="CASCADE", index=True
        )
        self.string(name="identifier", nullable=False, index=True)


def upgrade() -> None:
    """
    Function to create a table
    """
    JournalMigration().upgrade()


def downgrade() -> None:
    """
    Function to drop a table
    """
    JournalMigration().downgrade()

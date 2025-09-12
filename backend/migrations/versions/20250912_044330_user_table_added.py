"""User table added

Revision ID: 20250912_044330
Revises:
Create Date: 2025-09-12 10:28:30.730175

"""

from typing import Sequence, Union

from migrations.base import BaseMigration

revision: str = "20250912_044330"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class UserMigration(BaseMigration):

    table_name = "sys_users"

    def __init__(self):
        super().__init__(revision="20250912_044330", down_revision=None)
        self.create_whole_table = True
        # describe your schemas here
        self.base_columns()
        self.string(name="first_name", nullable=False)
        self.string(name="last_name", nullable=False)
        self.string(name="email", nullable=False)
        self.string(name="password", nullable=False)
        self.uuid(name="identifier", nullable=False, unique=True)
        self.string(name="username", nullable=False)


def upgrade() -> None:
    """
    Function to create a table
    """
    UserMigration().upgrade()


def downgrade() -> None:
    """
    Function to drop a table
    """
    UserMigration().downgrade()

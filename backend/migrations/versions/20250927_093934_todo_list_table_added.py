"""todo_list_table_added

Revision ID: 20250927_093934
Revises: 20250912_050011
Create Date: 2025-09-27 15:24:34.414612

"""

from typing import Sequence, Union

from sqlalchemy.orm import foreign

from migrations.base import BaseMigration

revision: str = "20250927_093934"
down_revision: Union[str, Sequence[str], None] = "20250912_050011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class TodoListMigration(BaseMigration):

    table_name = "todo_lists"

    def __init__(self):
        super().__init__(revision="20250927_093934", down_revision="20250912_050011")
        self.create_whole_table = True
        # describe your schemas here
        self.base_columns()
        self.timestamp_mixin_columns()
        self.string(name="name", nullable=False)
        self.string(name="identifier", nullable=False, index=True)
        self.foreign(name="owner_id", table="sys_users", index=True)


def upgrade() -> None:
    """
    Function to create a table
    """
    TodoListMigration().upgrade()


def downgrade() -> None:
    """
    Function to drop a table
    """
    TodoListMigration().downgrade()

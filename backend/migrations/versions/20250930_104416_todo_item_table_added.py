"""todo_item_table_added

Revision ID: 20250930_104416
Revises: 20250927_094302
Create Date: 2025-09-30 16:29:16.374885

"""

from typing import Sequence, Union

from migrations.base import BaseMigration

revision: str = "20250930_104416"
down_revision: Union[str, Sequence[str], None] = "20250927_094302"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class TodoItemMigration(BaseMigration):

    table_name = "todo_items"

    def __init__(self):
        super().__init__(revision="20250930_104416", down_revision="20250927_094302")
        self.create_whole_table = True
        # describe your schemas here
        self.base_columns()
        self.timestamp_mixin_columns()
        self.foreign(
            name="todo_list_id", table="todo_lists", index=True, on_delete="CASCADE"
        )
        self.string(name="title", nullable=False)
        self.string(name="status", nullable=False)
        self.string(name="description", nullable=False)
        self.foreign(name="owner_id", table="sys_users", index=True)
        self.string(name="identifier", nullable=False)


def upgrade() -> None:
    """
    Function to create a table
    """
    TodoItemMigration().upgrade()


def downgrade() -> None:
    """
    Function to drop a table
    """
    TodoItemMigration().downgrade()

"""todo_list_member_added

Revision ID: 20250927_094302
Revises: 20250927_093934
Create Date: 2025-09-27 15:28:02.331199

"""

from typing import Sequence, Union

from migrations.base import BaseMigration

revision: str = "20250927_094302"
down_revision: Union[str, Sequence[str], None] = "20250927_093934"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class TodoListMemberMigration(BaseMigration):

    table_name = "todo_list_members"

    def __init__(self):
        super().__init__(revision="20250927_094302", down_revision="20250927_093934")
        self.create_whole_table = True
        # describe your schemas here
        self.base_columns()
        self.timestamp_mixin_columns()
        self.foreign(name="todo_list_id", table="todo_lists", index=True)
        self.foreign(name="user_id", table="sys_users")
        self.string(name="role", nullable=False)


def upgrade() -> None:
    """
    Function to create a table
    """
    TodoListMemberMigration().upgrade()


def downgrade() -> None:
    """
    Function to drop a table
    """
    TodoListMemberMigration().downgrade()

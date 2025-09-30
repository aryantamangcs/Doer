from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.todo.entities.todo_item_entity import TodoItem
from src.domains.todo.enums.todo_enums import TodoStatusEnum
from src.domains.todo.repositories.todo_item_repo import TodoItemRepository
from src.infrastructures.db.config import async_session
from src.infrastructures.todo.models.todo_item_model import TodoItemModel


class TodoItemRepoSqlAlchemy(TodoItemRepository):
    """
    Implementation of the abstractions
    """

    def __init__(self, session: Callable[[], AsyncSession] = async_session):
        self.get_session = session

    async def add(self, todo_item: TodoItem) -> TodoItem:
        """
        adds the todolist
        """
        async with self.get_session() as session:
            new_item = TodoItemModel(
                todo_list_id=todo_item.todo_list_id,
                title=todo_item.title,
                status=todo_item.status,
                description=todo_item.description,
                owner_id=todo_item.owner_id,
                identifier=todo_item.identifier,
            )
            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)
            todo_item.id = new_item.id
            return todo_item

    async def get_by_identifier(self, identifier: str) -> TodoItem | None:
        """
        Get Todo Item by identifier
        """
        async with self.get_session() as session:
            result = await session.execute(
                select(TodoItemModel).where(TodoItemModel.identifier == identifier)
            )
            todo_item = result.scalar()

            if not todo_item:
                return None
            return TodoItem(
                id=todo_item.id,
                title=todo_item.title,
                status=TodoStatusEnum(todo_item.status),
                description=todo_item.description,
                todo_list_id=todo_item.todo_list_id,
                created_at=todo_item.created_at,
                updated_at=todo_item.updated_at,
                identifier=todo_item.identifier,
                owner_id=todo_item.owner_id,
                deleted_at=todo_item.deleted_at,
            )

from typing import Callable

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.todo.entities.todo_item_entity import TodoItem
from src.domains.todo.enums.todo_enums import TodoStatusEnum
from src.domains.todo.repositories.todo_item_repo import TodoItemRepository
from src.infrastructures.common.context import current_user
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

    async def get_all(self) -> list[TodoItem]:
        """
        Lists all the todo item objects
        """
        user = current_user.get()
        async with self.get_session() as session:
            result = await session.execute(
                select(TodoItemModel).where(
                    TodoItemModel.deleted_at.is_(None),
                    TodoItemModel.owner_id == user["id"],
                )
            )
            todos = result.scalars().all()

            return list(todos)

    async def find_one(self, where: dict | None = None, **kwargs):
        return await super().find_one(where, **kwargs)

    async def get_by_id(self, id: int) -> TodoItem | None:
        return await super().get_by_id(id)

    async def delete(self, id: int):
        """
        delete the todo list
        """

        async with self.get_session() as session:
            result = await session.execute(
                select(TodoItemModel).where(TodoItemModel.id == id)
            )
            todo_list = result.scalars().first()

            if todo_list:
                await session.delete(todo_list)
                await session.commit()

    async def filter(self, where: dict | None = None, **kwargs) -> list[TodoItem]:
        """
        finds todoitem
        """

        query = select(TodoItemModel)

        if where:
            for attr, value in where.items():
                column = getattr(TodoItemModel, attr)
                query = query.where(column == value)

        async with self.get_session() as session:
            result = await session.execute(query)
            todo_items = result.scalars()

            if not todo_items:
                return []
            data = [
                TodoItem(
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
                for todo_item in todo_items
            ]
            return data

    async def update(self, updated_todo_item: TodoItem) -> TodoItem | None:
        """
        Update the todo item
        """

        async with self.get_session() as session:
            stmt = (
                update(TodoItemModel)
                .where(TodoItemModel.id == updated_todo_item.id)
                .values(**updated_todo_item.__dict__)
                .returning(TodoItemModel)
            )
            result = await session.execute(stmt)
            updated_row = result.scalar_one_or_none()
            await session.commit()
            return updated_todo_item

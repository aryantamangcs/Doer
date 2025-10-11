from typing import Callable

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.todo.entities.todo_entity import TodoList
from src.domains.todo.repositories.todo_list_repo import TodoListRepository
from src.infrastructures.db.config import async_session
from src.infrastructures.todo.models.todo_list_model import TodoListModel
from src.shared.exceptions import ServerError


class TodoListRepoSqlAlchemy(TodoListRepository):
    """
    implementation of todo list interfaces
    """

    def __init__(self, session: Callable[[], AsyncSession] = async_session):
        self.get_session = session

    async def add(self, todo_list: TodoList) -> TodoList:
        """
        Adds the todolist
        """
        async with self.get_session() as session:
            new_todo_list = TodoListModel(
                name=todo_list.name,
                identifier=todo_list.identifier,
                owner_id=todo_list.owner_id,
            )
            session.add(new_todo_list)
            await session.commit()
            await session.refresh(new_todo_list)
            todo_list.id = new_todo_list.id
            return todo_list

    async def get_all(self) -> list[TodoList]:
        """
        Lists all the todo list objects
        """
        async with self.get_session() as session:
            result = await session.execute(
                select(TodoListModel).where(TodoListModel.deleted_at.is_(None))
            )
            todos = result.scalars().all()

            return list(todos)

    async def find_one(self, where: dict | None = None, **kwargs) -> TodoList | None:
        """
        finds one todolist
        """

        query = select(TodoListModel)
        if not where:
            raise ServerError("Where is missing")

        for attr, value in where.items():
            column = getattr(TodoListModel, attr)
            query = query.where(column == value)

        async with self.get_session() as session:
            result = await session.execute(query)
            todo_list = result.scalar()

            if not todo_list:
                return None
            return TodoList(
                id=todo_list.id,
                name=todo_list.name,
                created_at=todo_list.created_at,
                updated_at=todo_list.updated_at,
                identifier=todo_list.identifier,
                owner_id=todo_list.owner_id,
                deleted_at=todo_list.deleted_at,
            )

    async def filter(
        self, where: dict | None = None, **kwargs
    ) -> list[TodoList] | None:
        """
        finds  todolist
        """

        query = select(TodoListModel)

        if where:
            for attr, value in where.items():
                column = getattr(TodoListModel, attr)
                query = query.where(column == value)

        async with self.get_session() as session:
            result = await session.execute(query)
            todo_lists = result.scalars()

            if not todo_lists:
                return None
            data = [
                TodoList(
                    id=todo_list.id,
                    name=todo_list.name,
                    created_at=todo_list.created_at,
                    updated_at=todo_list.updated_at,
                    identifier=todo_list.identifier,
                    owner_id=todo_list.owner_id,
                    deleted_at=todo_list.deleted_at,
                )
                for todo_list in todo_lists
            ]
            return data

    async def delete(self, id: int):
        """
        delete the todo list
        """

        async with self.get_session() as session:
            result = await session.execute(
                select(TodoListModel).where(TodoListModel.id == id)
            )
            todo_list = result.scalars().first()

            if todo_list:
                await session.delete(todo_list)
                await session.commit()

    async def get_by_id(self, id: int) -> TodoList | None:
        """
        get todo list by id
        """

    async def get_by_identifier(self, identifier: str) -> TodoList | None:
        """
        Get Todo Item by identifier
        """
        async with self.get_session() as session:
            result = await session.execute(
                select(TodoListModel).where(TodoListModel.identifier == identifier)
            )
            todo_list = result.scalar()

            if not todo_list:
                return None
            return TodoList(
                id=todo_list.id,
                name=todo_list.name,
                created_at=todo_list.created_at,
                updated_at=todo_list.updated_at,
                identifier=todo_list.identifier,
                owner_id=todo_list.owner_id,
                deleted_at=todo_list.deleted_at,
            )

    async def update(self, updated_todo_list: TodoList) -> TodoList | None:
        """
        Update the todo list details
        """

        updated_list = updated_todo_list.__dict__

        updated_list.pop("members")

        async with self.get_session() as session:
            stmt = (
                update(TodoListModel)
                .where(TodoListModel.id == updated_todo_list.id)
                .values(**updated_list)
                .returning(TodoListModel)
            )
            result = await session.execute(stmt)
            updated_row = result.scalar_one_or_none()
            await session.commit()
            return updated_todo_list

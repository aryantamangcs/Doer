from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.todo.entities.todo_entity import TodoList
from src.domains.todo.repositories.todo_list_repo import TodoListRepository
from src.infrastructures.db.config import async_session
from src.infrastructures.todo.models.todo_list_model import TodoListModel


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
            )
            session.add(new_todo_list)
            await session.commit()
            await session.refresh(new_todo_list)
            todo_list.id = new_todo_list.id
            return todo_list

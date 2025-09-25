import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ..enums import TodoListMemberRoleEnum, TodoStatusEnum


@dataclass
class ListMember:
    '''
    Todo List member
    '''

    user_id : int
    todo_list_id : int
    role : TodoListMemberRoleEnum = TodoListMemberRoleEnum.MEMBER
    joined_at : datetime = field(default_factory=datetime.now)
    deleted_at  : datetime | None = None

    @classmethod
    def create(cls,user_id:int,todo_list_id:int,role=TodoListMemberRoleEnum.MEMBER):
        '''
        Creates the list member
        '''
        return cls(user_id=user_id,todo_list_id=todo_list_id,role=role)
    
    def delete(self):
        '''
        Deletes the list member
        '''
        self.deleted_at = datetime.now()

@dataclass
class TodoList:
    """
    TodoLists entity
    """

    name: str
    created_at: datetime
    updated_at: datetime
    identifier : str # uuid 
    owner_id: int 
    members : list[ListMember] = field(default_factory=list)
    id : int | None = None
    deleted_at : datetime | None = None

    @classmethod
    def create(cls,name:str,owner_id:int)
         new_todo_list = cls(name=name,owner_id=owner_id,identifier=str(uuid.uuid4()),created_at=datetime.now(),updated_at=datetime.now())
         new_todo_list.add_member(user_id=owner_id,role = TodoListMemberRoleEnum.ADMIN)
         return new_todo_list

    def change_name(self,name:str) -> None:
        '''
        Changes the name of the todo list
        Args:
            name : new name of the todo list
        Returns:
            None
        '''
        self.name = name
        self.updated_at = datetime.now()

    def change_owner(self,owner_id:int) -> None:
        '''
        Changes the owner of the todo list
        Args:
            owner_id : new owner id
        Returns:
            None
        '''
        self.owner_id = owner_id


    def delete(self):
        '''
        Soft deletes the todo list
        '''
        self.deleted_at = datetime.now()


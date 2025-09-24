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
    role : TodoListMemberRoleEnum = TodoListMemberRoleEnum.MEMBER
    joined_at : datetime = field(default_factory=datetime.now)

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

    def add_member(self,user_id : int,role : TodoListMemberRoleEnum = TodoListMemberRoleEnum.MEMBER) -> None:
        '''
        Adds member to the todo list
        Args:
            user_id to be added
        Raise:
            Already error
        Returns:
            None
        '''
        if any(member.user_id == user_id for member in self.members):
            raise ValueError("User is already a member in this todo list")
        self.members.append(ListMember(user_id=user_id,role=role))

    def remove_member(self,user_id : int) -> None:
        '''
        Removes member from the todo list
        Args:
            user_id to be removed
        Raise:
            Not found error
        Returns:
            None
        '''
        if any(member.user_id == user_id for member in self.members):
            self.members = [member for member in self.members if member.user_id != user_id]
            return
        raise ValueError("User doesn't exist in this todo list to be removed")


    def delete(self):
        '''
        Soft deletes the todo list
        '''
        self.deleted_at = datetime.now()


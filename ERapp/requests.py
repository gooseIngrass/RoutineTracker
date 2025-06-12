
from sqlalchemy import select, update, delete, func
from models import User, Task, Character
from pydantic import BaseModel, ConfigDict
from database import async_session


class TaskSchema(BaseModel):
    id: int
    title: str
    completed: bool
    user: int
    
    model_config = ConfigDict(from_attributes=True)


async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user

        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

# async def get_user(tg_id): Переписать под чара
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         return user

async def create_character(user_id, nickname, charClass):
    async with async_session() as session:
        character = await session.scalar(select(Character).where(Character.user_id == user_id))
        if character:
            return character
        
        new_character = Character(user_id=user_id, name=nickname, charClass=charClass)
        
        session.add(new_character)
        
        await session.commit()
        await session.refresh(new_character)
        await session.execute(update(User).where(User.id == user_id).values(character_id=new_character.id))
        await session.commit()
        
        return new_character

async def get_tasks(user_id):
    async with async_session() as session:
        tasks = await session.scalars(
            select(Task).where(Task.user == user_id, Task.completed == False)
        )
        
        serialized_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]
        
        return serialized_tasks


async def get_completed_tasks_count(user_id):
    async with async_session() as session:
        return await session.scalar(select(func.count(Task.id)).where((Task.completed == True) & (Task.user == user_id)))


async def add_task(user_id, title):
    async with async_session() as session:
        new_task = Task(
            title=title,
            user=user_id
        )
        session.add(new_task)
        await session.commit()


async def update_task(task_id):
    async with async_session() as session:
        await session.execute(update(Task).where(Task.id == task_id).values(completed=True))
        await session.commit()

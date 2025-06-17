
from sqlalchemy import select, update, delete, func
from models import User, Task, Character, Quest, UserQuest
from pydantic import BaseModel, ConfigDict
from database import async_session


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    completed: bool
    user: int
    
    model_config = ConfigDict(from_attributes=True)

class QuestSchema(BaseModel):
    id: int
    title: str
    description: str
    lvl_required: int
    exp_reward: int
    gold_reward: int

    model_config = ConfigDict(from_attributes=True)
    

class CharSchema(BaseModel):
    id:int
    name:str
    charClass:str
    active_quest:int
    level:int
    exp:int
    hp:int
    ap:int
    gold:int
    strength: int
    intelligence: int
    constitution: int
    perception: int
    user_id: int

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

async def create_character(user_id, nickname, charClass):
    async with async_session() as session:
        new_character = Character(user_id=user_id, name=nickname, charClass=charClass)
        
        session.add(new_character)
        
        await session.commit()
        await session.refresh(new_character)
        
        return new_character

async def char_info(user_id):
    async with async_session() as session:
        character = await session.scalar(select(Character).where(Character.user_id == user_id))
        if not character:
            return

        serialized_character = CharSchema.model_validate(character).model_dump()
        return serialized_character
    
async def update_char(char_id, field, value):
    async with async_session() as session:
        await session.execute(update(Character)
                              .where(Character.id == char_id)
                              .values(**{field:value}))
        await session.commit()

async def get_tasks(user_id):
    async with async_session() as session:
        tasks = await session.scalars(
            select(Task).where(Task.user == user_id, Task.completed == False)
        )
        
        serialized_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]
        
        return serialized_tasks

async def get_quests(char_id):
    async with async_session() as session:
        quests = await session.scalars(
            select(Quest)
            .outerjoin(UserQuest, (Quest.id == UserQuest.quest_id) & (UserQuest.char_id == char_id))
            .where(UserQuest.id.is_(None))
        )
        
        serialized_quests = [
            QuestSchema.model_validate(q).model_dump() for q in quests
        ]

        return serialized_quests

async def get_active_quest(char_id):
    async with async_session() as session:
        quest = await session.scalar(select(Quest)
                                     .join(Character, Quest.id == Character.active_quest)
                                     .where(Character.id == char_id))

        serialized_quest = QuestSchema.model_validate(quest).model_dump()

        return serialized_quest

async def get_completed_tasks_count(user_id):
    async with async_session() as session:
        return await session.scalar(select(func.count(Task.id)).where((Task.completed == True) & (Task.user == user_id)))


async def add_task(user_id, title, desc, diff):
    async with async_session() as session:
        gold_reward = {
            'LOW': 5,
            'MEDIUM':8,
            'HIGH':10
        }
        ap_reward = {
            'LOW': 2,
            'MEDIUM':3,
            'HIGH': 4
        }

        new_task = Task(
            title=title,
            user=user_id,
            description=desc,
            difficulty=diff,
            ap_reward=ap_reward[diff],
            gold_reward=gold_reward[diff]
        )
        session.add(new_task)
        await session.commit()

async def complete_task(task_id, char_id):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.id == task_id))
        await session.execute(update(Task).where(Task.id == task_id).values(completed=True))
        await session.execute(update(Character).where(Character.id == char_id).values(gold=Character.gold+task.gold_reward, ap=Character.ap+task.ap_reward))
        await session.commit()

# async def reward(char_id, ap, gold):
#     async with async_session() as session:
#         await session.execute(update(Character).where(Character.id == char_id).values(ap=ap, gold=gold))
#         await session.commit()
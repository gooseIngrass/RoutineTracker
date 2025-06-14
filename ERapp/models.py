from sqlalchemy import ForeignKey, String, BigInteger, Date, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sql_enums import *
from database import Base


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at = mapped_column(Date, default=datetime.today)
    tg_id = mapped_column(BigInteger)

class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(String(250))
    
    difficulty: Mapped[str] = mapped_column(default=TaskDiffName.LOW.value)
    task_type: Mapped[str] = mapped_column(default=TaskTypeEnum.TODO.value)
	
    ap_reward: Mapped[int] = mapped_column(default=ExpRewardEnum.LOW.value)
    gold_reward: Mapped[int] = mapped_column(default=GoldRewardEnum.LOW.value)
    completed: Mapped[bool] = mapped_column(default=False)
	
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    
class Character(Base):
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    charClass: Mapped[str] = mapped_column(default=CharClassEnum.WARRIOR)
    gold: Mapped[int] = mapped_column(default=10, server_default=text('10'))
    ap: Mapped[int] = mapped_column(default=0, server_default=text('0'))
    active_quest: Mapped[int | None] = mapped_column(ForeignKey('quests.id', ondelete='SET NULL'))

    level: Mapped[int] = mapped_column(default=1)
    exp: Mapped[int] = mapped_column(default=0)
    hp: Mapped[int] = mapped_column(default=50)

    strength: Mapped[int] = mapped_column(default=10)
    intelligence: Mapped[int] = mapped_column(default=10)
    constitution: Mapped[int] = mapped_column(default=10)
    perception: Mapped[int] = mapped_column(default=10)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    avatar_url: Mapped[str | None] = mapped_column(String(250))

class Quest(Base):
    __tablename__= 'quests'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(String(250))
    lvl_required:Mapped[int] = mapped_column(default=1)

    exp_reward: Mapped[int]
    gold_reward: Mapped[int]

class UserQuest(Base):
    __tablename__ = 'user_quests'

    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    quest_id: Mapped[int] = mapped_column(ForeignKey('quests.id'))
     
	

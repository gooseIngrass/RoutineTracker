from sqlalchemy import ForeignKey, String, BigInteger, Date
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime
from sql_enums import CharClassEnum

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at = mapped_column(Date, default=datetime.today)
    tg_id = mapped_column(BigInteger)
    
    character = relationship("Character", back_populates="user", uselist=False)
    


class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    
class Character(Base):
	__tablename__ = 'characters'
	
	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
	name: Mapped[str] = mapped_column(String(25))
	charClass: Mapped[CharClassEnum] = mapped_column(default=CharClassEnum.WARRIOR)
	
	level: Mapped[int] = mapped_column(default=1)
	exp: Mapped[int] = mapped_column(default=0)
	hp: Mapped[int] = mapped_column(default=50)
	
	strength: Mapped[int] = mapped_column(default=10)
	intelligence: Mapped[int] = mapped_column(default=10)
	constitution: Mapped[int] = mapped_column(default=10)
	perception: Mapped[int] = mapped_column(default=10)
	
	avatar_url: Mapped[str | None]
    
	user = relationship("User", back_populates="character", uselist=False)
     
	 


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# class TaskDifficulty(Base):
# 	__tablename__ = 'task_difficulties'

# 	id: Mapped[int] = mapped_column(primary_key=True)
# 	name: Mapped[str]
# 	exp_reward: Mapped[int]
# 	gold_reward: Mapped[int]

# 	tasks = relationship("Task", back_populates="difficulty")

# class Task(Base):
# 	__tablename__ = 'tasks'

# 	id: Mapped[int] = mapped_column(primary_key=True)
# 	title: Mapped[str] = mapped_column(String(128))
# 	description: Mapped[str | None] = mapped_column(Text)

# 	task_type: Mapped[TaskTypeEnum | None] = mapped_column(default=TaskTypeEnum.TODO)
# 	difficulty_id: Mapped[int | None] = mapped_column(ForeignKey('task_difficulties.id'))
	
# 	completed: Mapped[bool] = mapped_column(default=False)
	
# 	user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
# 	difficulty = relationship("TaskDifficulty", back_populates="tasks")

# #Запускаем базу и инициализируем её моделями описанными выше
# async def init_db():
# 	async with engine.begin() as conn:
# 		await conn.run_sync(Base.metadata.create_all)


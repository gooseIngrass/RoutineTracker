
from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.middleware.cors import CORSMiddleware

from database import init_db
import requests as rq


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print('Bot is ready')
    yield
app = FastAPI(title="To Do App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://erapp-6a56e.web.app", "http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для добавления Access-Control-Allow-Private-Network
@app.middleware("http")
async def add_private_network_header(request: Request, call_next):
    response = await call_next(request)
    if isinstance(response, Response):
        response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

class AddTask(BaseModel):
    tg_id: int
    title: str
    desc: str
    diff: str

class UpdateChar(BaseModel):
    char_id: int
    field: str
    value: int

class AddCharacter(BaseModel):
    tg_id: int
    nickname: str
    charClass: str

class Reward(BaseModel):
    char_id: int
    ap: str
    gold: int

class CompleteTask(BaseModel):
    task_id: int
    char_id:int

@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_tasks(user.id)

@app.get("/api/quests/{char_id}")
async def get_quests(char_id: int):
    return await rq.get_quests(char_id)

@app.get("/api/user/me/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    completed_tasks_count = await rq.get_completed_tasks_count(user.id)
    return {'completedTasks': completed_tasks_count} 

@app.get("/api/user/character/{tg_id}")
async def get_char(tg_id:int):
    user = await rq.add_user(tg_id)
    return await rq.char_info(user.id)

@app.post("/api/createChar")
async def welcome(character: AddCharacter):
    user = await rq.add_user(character.tg_id)
    await rq.create_character(user.id, character.nickname, character.charClass)
    return {'status' : 'ok'}

@app.post("/api/add")
async def add_task(task: AddTask):
    user = await rq.add_user(task.tg_id)
    await rq.add_task(user.id, task.title, task.desc, task.diff)
    return {'status': 'ok'}

@app.patch("/api/completed")
async def complete_task(reward: CompleteTask):
    await rq.complete_task(reward.task_id, reward.char_id)
    return {'char': reward.char_id}

@app.patch("/api/user/character/update")
async def update_char(changes: UpdateChar):
    await rq.update_char(changes.char_id, changes.field, changes.value)
    return {'status':'ok'}
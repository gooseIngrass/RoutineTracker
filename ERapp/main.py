
from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print('Bot is ready')
    yield
app = FastAPI(title="To Do App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://erapp-6a56e.web.app"], 
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


class CompleteTask(BaseModel):
    id: int



@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_tasks(user.id)


@app.get("/api/main/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    completed_tasks_count = await rq.get_completed_tasks_count(user.id)
    return {'completedTasks': completed_tasks_count}


@app.post("/api/add")
async def add_task(task: AddTask):
    user = await rq.add_user(task.tg_id)
    await rq.add_task(user.id, task.title)
    return {'status': 'ok'}


@app.patch("/api/completed")
async def complete_task(task: CompleteTask):
    await rq.update_task(task.id)
    return {'status': 'ok'}

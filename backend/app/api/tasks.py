from fastapi import APIRouter, Request, HTTPException
from sqlalchemy import select
from pydantic import BaseModel
from app.db.models.task import Task
from app.db.session import Session

router = APIRouter()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    status: str


@router.post("/")
async def create_task(request: Request, data: TaskCreate):
    async with Session() as session:
        task = Task(
            title=data.title,
            user_id=request.state.user.id,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task


@router.get("/")
async def get_tasks(request: Request):
    async with Session() as session:
        result = await session.execute(
            select(Task).where(Task.user_id == request.state.user.id)
        )
        return result.scalars().all()


@router.patch("/{task_id}")
async def update_task_status(
    request: Request,
    task_id: int,
    data: TaskUpdate,
):
    if data.status not in ("open", "done"):
        raise HTTPException(status_code=400, detail="Invalid status")

    async with Session() as session:
        task = await session.get(Task, task_id)

        if not task or task.user_id != request.state.user.id:
            raise HTTPException(status_code=404)

        task.status = data.status
        await session.commit()
        await session.refresh(task)
        return task

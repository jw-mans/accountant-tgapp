from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.task import Task
from app.db.session import Session

router = APIRouter()

@router.post("/")
async def create_task(
    request: Request, 
    title: str, 
    description: str | None = None
):
    async with Session() as session:
        async with session.begin():
            task = Task(
                title=title,
                description=description,
                status="pending",
                user_id=request.state.user.id
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task
        
@router.get("/")
async def get_tasks(request: Request):
    async with Session() as session:
        result = await session.execute(
            select(Task).where(
                Task.user_id == request.state.user.id
            )
        )
        tasks = result.scalars().all()
        return tasks
    
@router.patch("/{task_id}")
async def update_task_status(
    request: Request, 
    task_id: int, 
    status: str
):
    if status not in [
        "pending", "in_progress", "completed",
    ]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid status"
    )

    async with Session() as session:
        async with session.begin():
            task = await session.get(Task, task_id)
            if not task or task.user_id != request.state.user.id:
                raise HTTPException(
                    status_code=404, 
                    detail="Task not found"
                )
            
            task.status = status
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task
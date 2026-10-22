from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_task_service
from app.schemas import TaskCreate, TaskRead, TaskUpdate
from app.service import TaskNotFoundError, TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def read_tasks(service: TaskService = Depends(get_task_service)) -> list[TaskRead]:
    return service.list_tasks()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate, service: TaskService = Depends(get_task_service)
) -> TaskRead:
    return service.create_task(payload)


@router.patch("/{task_id}")
def update_task(
    task_id: str, payload: TaskUpdate, service: TaskService = Depends(get_task_service)
) -> TaskRead:
    try:
        return service.update_task(task_id, payload)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, service: TaskService = Depends(get_task_service)) -> None:
    try:
        service.delete_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

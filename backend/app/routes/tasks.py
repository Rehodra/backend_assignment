from fastapi import APIRouter, Depends, Query, status
from app.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse, TaskListResponse
from app.services import task_service
from app.core.dependencies import get_current_active_user, require_admin

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED,
             summary="Create a new task")
async def create_task(body: TaskCreateRequest,
                      current_user: dict = Depends(get_current_active_user)):
    task = await task_service.create_task(
        owner_id=str(current_user["_id"]),
        title=body.title,
        description=body.description,
        status=body.status,
        priority=body.priority,
    )
    return _format_task(task)


@router.get("", response_model=TaskListResponse, summary="List tasks (own or all for admin)")
async def list_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_active_user),
):
    is_admin = current_user.get("role") == "admin"
    result = await task_service.get_tasks(
        owner_id=str(current_user["_id"]),
        page=page,
        limit=limit,
        is_admin=is_admin,
    )
    result["tasks"] = [_format_task(t) for t in result["tasks"]]
    return result


@router.get("/{task_id}", response_model=TaskResponse, summary="Get a single task")
async def get_task(task_id: str, current_user: dict = Depends(get_current_active_user)):
    is_admin = current_user.get("role") == "admin"
    task = await task_service.get_task_by_id(task_id, str(current_user["_id"]), is_admin)
    return _format_task(task)


@router.put("/{task_id}", response_model=TaskResponse, summary="Update a task")
async def update_task(task_id: str, body: TaskUpdateRequest,
                      current_user: dict = Depends(get_current_active_user)):
    is_admin = current_user.get("role") == "admin"
    updates = body.model_dump(exclude_unset=True)
    task = await task_service.update_task(task_id, str(current_user["_id"]), is_admin, updates)
    return _format_task(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
async def delete_task(task_id: str, current_user: dict = Depends(get_current_active_user)):
    is_admin = current_user.get("role") == "admin"
    await task_service.delete_task(task_id, str(current_user["_id"]), is_admin)


def _format_task(task: dict) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description"),
        "status": task["status"],
        "priority": task["priority"],
        "owner_id": task["owner_id"],
        "created_at": task["created_at"],
        "updated_at": task["updated_at"],
    }

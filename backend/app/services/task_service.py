from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
from app.db.database import get_database


async def create_task(owner_id: str, title: str, description: Optional[str],
                      status: str, priority: str) -> dict:
    db = await get_database()
    task_doc = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "owner_id": owner_id,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await db["tasks"].insert_one(task_doc)
    task_doc["_id"] = result.inserted_id
    return task_doc


async def get_tasks(owner_id: Optional[str], page: int, limit: int, is_admin: bool) -> dict:
    db = await get_database()
    query = {} if is_admin else {"owner_id": owner_id}
    skip = (page - 1) * limit
    total = await db["tasks"].count_documents(query)
    tasks = await db["tasks"].find(query).skip(skip).limit(limit).to_list(length=limit)
    return {"tasks": tasks, "total": total, "page": page, "limit": limit}


async def get_task_by_id(task_id: str, owner_id: str, is_admin: bool) -> dict:
    db = await get_database()
    task = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task["owner_id"] != owner_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return task


async def update_task(task_id: str, owner_id: str, is_admin: bool, updates: dict) -> dict:
    db = await get_database()
    task = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task["owner_id"] != owner_id:
        raise HTTPException(status_code=403, detail="Access denied")

    updates["updated_at"] = datetime.now(timezone.utc)
    updates = {k: v for k, v in updates.items() if v is not None}

    result = await db["tasks"].find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": updates},
        return_document=True,
    )
    return result


async def delete_task(task_id: str, owner_id: str, is_admin: bool):
    db = await get_database()
    task = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task["owner_id"] != owner_id:
        raise HTTPException(status_code=403, detail="Access denied")
    await db["tasks"].delete_one({"_id": ObjectId(task_id)})

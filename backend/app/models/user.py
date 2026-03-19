from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, handler):
        field_schema.update(type="string")
        return field_schema


class Role(str, Enum):
    user = "user"
    admin = "admin"


class UserModel(BaseModel):
    """Internal model matching the MongoDB document structure."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    hashed_password: str
    role: Role = Role.user
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

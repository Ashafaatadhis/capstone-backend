from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None

def success_response(message: str = None, data=None):
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str, data=None):
    return {
        "success": False,
        "message": message,
        "data": data
    }

from pydantic import BaseModel, Field

class Student(BaseModel):
    id: int = Field(..., default=...)
    name: str = Field(..., default=...)
    age: int = Field(..., default=...)
    major: str = Field(..., default=...)
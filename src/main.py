"""
Task Management API using FastAPI
Developed for Git Lab Examination (Team Mate 1: Source Implementation)
Requirements:
  - id, title, description, status, priority
  - GET, POST, PUT, DELETE operations
  - Input validation and proper HTTP status codes
"""

from enum import Enum
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Title of the task")
    description: str = Field(default="", max_length=1000, description="Detailed description of the task")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current progress status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority level")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None


class Task(TaskBase):
    id: int = Field(..., description="Unique integer identifier for the task")


# Initialize FastAPI Application
app = FastAPI(
    title="Task Management API",
    description="A simple REST API for managing tasks with pytest coverage and GitHub Actions CI",
    version="1.0.0",
)

# In-memory storage and counter
tasks_db: Dict[int, Task] = {}
task_id_counter: int = 1


def reset_db() -> None:
    """Helper utility for tests to reset in-memory state cleanly."""
    global task_id_counter
    tasks_db.clear()
    task_id_counter = 1


@app.get("/", tags=["Health"])
def root():
    """Health check and API root."""
    return {
        "message": "Task Management API is active and running",
        "docs": "/docs",
        "total_tasks": len(tasks_db),
    }


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def get_all_tasks(
    status: Optional[TaskStatus] = Query(default=None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(default=None, description="Filter by priority"),
):
    """
    Retrieve all tasks with optional status and priority filtering.
    """
    results = list(tasks_db.values())
    if status is not None:
        results = [t for t in results if t.status == status]
    if priority is not None:
        results = [t for t in results if t.priority == priority]
    return results


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task_by_id(task_id: int):
    """
    Retrieve a single task by its unique ID.
    Returns 404 if the task is not found.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return tasks_db[task_id]


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(payload: TaskCreate):
    """
    Create a new task.
    Returns 201 Created and the created task with auto-assigned ID.
    """
    global task_id_counter
    new_id = task_id_counter
    task_id_counter += 1

    new_task = Task(
        id=new_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
    )
    tasks_db[new_id] = new_task
    return new_task


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, payload: TaskUpdate):
    """
    Update an existing task by ID.
    Returns 404 if the task does not exist.
    Only provided fields will be updated.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    existing_task = tasks_db[task_id]
    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        return existing_task

    updated_task = existing_task.model_copy(update=update_data)
    tasks_db[task_id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int):
    """
    Delete a task by ID.
    Returns 404 if the task does not exist.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    deleted_task = tasks_db.pop(task_id)
    return {
        "message": f"Task with ID {task_id} deleted successfully",
        "deleted_task": deleted_task.model_dump(),
    }

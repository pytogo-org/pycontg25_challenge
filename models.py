from typing import Optional
from pydantic import BaseModel, Field

class ParticipantRegistration(BaseModel):
    full_name: str = Field(..., description="Full Name of the Participant")
    email: str = Field(..., description="Email Address of the Participant")
    github_username: Optional[str] = Field(None, description="GitHub Username of the Participant")
    experience_level: str = Field(..., description="Experience Level of the Participant")

class TaskSubmission(BaseModel):
    participant_email: str = Field(..., description="Email of the Participant submitting the task")
    task_day: int = Field(..., description="Day of the Task")
    solution: str = Field(..., description="Solution for the Task")
    explanation: Optional[str] = Field(None, description="Explanation of the Solution")

class TaskInfo(BaseModel):
    day: int = Field(..., description="Day of the Task")
    title: str = Field(..., description="Title of the Task")
    description: str = Field(..., description="Description of the Task")
    deadline: str = Field(..., description="Deadline for the Task")
    difficulty: str = Field(..., description="Difficulty Level of the Task")
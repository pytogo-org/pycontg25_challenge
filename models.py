from sqlite3.dbapi2 import Timestamp
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
    title_en: str = Field(..., description="Title of the Task")
    title_fr: str = Field(..., description="Title of the Task in French")
    link_fr: Optional[str] = Field(None, description="Link to the Task in French")
    link_en: Optional[str] = Field(None, description="Link to the Task in English")
    difficulty: Optional[str] = Field(None, description="Difficulty level of the Task")
    deadline: Timestamp = Field(..., description="Deadline for the Task")
 

class ProgressInfo(BaseModel):
    participant_email: str = Field(..., description="Email of the Participant")

class Feedback(BaseModel):
    name: str = Field(..., description="Name of the respondent")
    email: Optional[str] = Field(None, description="Email of the respondent (optional)")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    liked: Optional[str] = Field(None, description="What the participant liked")
    disliked: Optional[str] = Field(None, description="What the participant disliked")
    suggestions: Optional[str] = Field(None, description="Additional suggestions or comments")

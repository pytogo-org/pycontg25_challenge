
import os
import typing



if not hasattr(typing, "_ClassVar") and hasattr(typing, "ClassVar"):
    typing._ClassVar = typing.ClassVar

import json
from time import timezone
from send_mail import send_welcome_email
from email_template import render_email_template
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timedelta, timezone
from models import  ParticipantRegistration, ProgressInfo, TaskSubmission, TaskInfo
from db import get_one_where, insert_into_table, get_some_thing, get_some_where, get_record_by_email, get_record_by_email
from dotenv import load_dotenv
from routes.cron import router as cron_router

load_dotenv()

challenge_start_date = datetime(2025, 7, 23, 0, 0, 0)
app = FastAPI(title="30-Day Python Challenge API", version="1.0.0")
app.include_router(cron_router, prefix="/api/cron", tags=["Cron Jobs"])
API_ROOT = os.environ.get("API_ROOT")

token_url = f"{API_ROOT}/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


static_folder = os.path.join(os.path.dirname(__file__), "static")
templates_folder = os.path.join(os.path.dirname(__file__), "templates")
app.mount("/static", StaticFiles(directory=static_folder), name="static")
templates = Jinja2Templates(directory=templates_folder)

def populate_tasks():
    """Populate the tasks table with 30 days of challenges"""
    # The deadline for each task is 23:59:59 of the day before the next task
    # Example: task 1 = 2025-07-20 23:59:59, task 2 = 2025-07-21 23:59:59, etc.

    with open("templates/tasks.json", "r") as file:
        tasks = json.load(file)

    for task in tasks:
        day = task["day"]
        deadline = challenge_start_date + timedelta(days=day)
        task_start_at = challenge_start_date + timedelta(days=day - 1)
        formate_task_start_at = task_start_at.strftime("%Y-%m-%d %H:%M:%S")
        task["start_at"] = formate_task_start_at
        formatted_deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
        task["deadline"] = formatted_deadline
        inserted = insert_into_table("tasks", task)
        task_info = TaskInfo(
            day=day,
            title_en=task["title_en"],
            title_fr=task["title_fr"],
            link_fr=task.get("link_fr"),
            link_en=task.get("link_en"),
            difficulty=(
                "Beginner" if day <= 10 else
                "Intermediate" if day <= 20 else
                "Advanced"
            ),
            deadline=formatted_deadline
        )

        try:
            
            if inserted:
                print(f"Task for day {day} inserted successfully.")
            else:
                print(f"Failed to insert task for day {day}.")
        except Exception as e:
            print(f"Error inserting task for day {day}: {e}")
    


@app.get("/")
def read_root(request: Request):
    """Root endpoint to serve the home page"""
    return templates.TemplateResponse("home.html", {"request": request, "display_submission_card": True, "display_progress_card": True, "display_registration_card": True})

@app.get('/submit')
def submit_page(request: Request):
    """Serve the task submission page"""
    return templates.TemplateResponse("home.html", {"request": request, "display_submission_card": True, "display_progress_card": True, "display_registration_card": False})

@app.get('/progress')
def progress_page(request: Request):
    """Serve the progress page"""
    return templates.TemplateResponse("home.html", {"request": request, "display_submission_card": True, "display_progress_card": True, "display_registration_card": False})

@app.get('/register')
def register_page(request: Request):
    """Serve the registration page"""
    return templates.TemplateResponse("home.html", {"request": request, "display_submission_card": False, "display_progress_card": False, "display_registration_card": True})


@app.post("/api/register")
async def register_participant(participant: ParticipantRegistration):
    """Register a new participant for the challenge"""
    closing_date = datetime(2025, 7, 23) + timedelta(days=3, hours=23, minutes=59, seconds=59)
    closing_date = closing_date.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > closing_date:
        raise HTTPException(status_code=400, detail="Registration is closed for this challenge")
    is_registered = get_record_by_email("participants", participant.email)
    if is_registered:
        raise HTTPException(status_code=400, detail="Participant already registered")
    try:
        data = participant.dict()
        
        print(f"Participant {participant.full_name} registered successfully.")
        try:
                send_welcome_email(first_name=participant.full_name, participant_email=participant.email)
                inserted_record = insert_into_table("participants", data)
                print(f"Welcome email sent to {participant.email}")
        except Exception as e:
                print(f"Error sending welcome email: {e}")
                raise HTTPException(status_code=500, detail="Failed to send welcome email, please try again with different email.")

        if inserted_record:
            return {"message": "Participant registered successfully"}

    except Exception as e:
        print(f"Error inserting participant: {e}")
        raise HTTPException(status_code=500, detail="Participant already exists")


@app.post("/api/submit")
async def submit_task(submission: TaskSubmission):
    """Submit a solution for a specific task"""
    
    is_participant = get_record_by_email("participants", submission.participant_email)
    task = get_one_where("tasks", "day", int(submission.task_day))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    start_date = datetime.fromisoformat(task["start_at"]).astimezone(timezone.utc)
    if datetime.now(timezone.utc) < start_date:
        raise HTTPException(status_code=400, detail="Task has not started yet")
    task_deadline = datetime.fromisoformat(task["deadline"]).astimezone(timezone.utc)
    now = datetime.now(timezone.utc)
    if now > task_deadline:
        raise HTTPException(status_code=400, detail="Task deadline has passed")
    
    if not is_participant:
        raise HTTPException(status_code=404, detail="Participant not found. Please register first.")

    existing_submission = get_some_where("submissions", "participant_email", submission.participant_email, "task_day", submission.task_day)
    if existing_submission:
        raise HTTPException(status_code=400, detail="Task already submitted")

    try:
        # type coverting the task_day to int
        submission.task_day = int(submission.task_day)
        
        data = submission.dict()
        inserted_record = insert_into_table("submissions", data)
        return {"message": "Task submitted successfully", "submission": inserted_record}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error occurred")


@app.post("/api/progress")
async def get_progress(progress: ProgressInfo):
    """Get progress for a specific participant"""
    now = datetime.now(timezone.utc)
    participant = get_record_by_email("participants", progress.participant_email)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    tasks = get_some_thing("tasks")




    task_progress = []
    for task in tasks:
        task_day = task.get("day")
        task_start_at = datetime.fromisoformat(task["start_at"]).astimezone(timezone.utc)
        now = datetime.now(timezone.utc)
        if task_day is None or task_start_at is None:
            continue

        if now >=task_start_at:
            submission = get_some_where("submissions", "participant_email", progress.participant_email, "task_day", task_day)
            if len(submission) > 0:
                submission = submission[0]
        else:
            submission = None  

        if submission:
            task_progress.append({
                "day": task_day,
                "title_en": task.get("title_en"),
                "status": "submitted" if submission.get("solution") else "not submitted",
                "solution": submission.get("solution"),
                "has_started": True if datetime.fromisoformat(task["start_at"]).isoformat() <= now.isoformat() else False,
                "not_started": "not started" if datetime.fromisoformat(task["start_at"]).isoformat() > now.isoformat() else "not submitted",
                "explanation": submission.get("explanation"),
                "deadline": datetime.fromisoformat(task["deadline"]).isoformat(),
                "has_started": True if datetime.fromisoformat(task["start_at"]).isoformat() <= now.isoformat() else False
            })
        else:
            # cast deadline to datetime 
            
            task_progress.append({
                "day": task_day,
                "title_en": task.get("title_en"),
                "status": "in progress" if datetime.fromisoformat(task["start_at"]).isoformat() <= now.isoformat() else "not submitted",
                "not_started": "not started" if datetime.fromisoformat(task["start_at"]).isoformat() > now.isoformat() else "not submitted",
                "deadline": datetime.fromisoformat(task["deadline"]).isoformat(),
                "has_started": True if datetime.fromisoformat(task["start_at"]).isoformat() <= now.isoformat() else False
            })

    stat_count = {
            "total_tasks": len(tasks),
            "tasks": [task for task in task_progress if task["has_started"]],
            "total_submissions": sum(1 for task in task_progress if task["status"] == "submitted"),
            "not_started": sum(1 for task in task_progress if task["status"] == "not submitted" and not task["has_started"]),
            "completed_tasks": sum(1 for task in task_progress if task["status"] == "submitted"),
            "in_progress_tasks": sum(1 for task in task_progress if task["status"] == "in progress"),
            "late_submissions": sum(1 for task in task_progress if task["status"] == "not submitted" and task.get("deadline") < now.isoformat())
            }
    if not task_progress:
        raise HTTPException(status_code=404, detail="No tasks found for this participant")


    return {"progress": task_progress, "stats": stat_count}

if __name__ == "__main__":
    # Populate tasks in the database
    populate_tasks()
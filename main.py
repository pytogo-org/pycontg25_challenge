import typing

from send_mail import send_welcome_email

if not hasattr(typing, "_ClassVar") and hasattr(typing, "ClassVar"):
    typing._ClassVar = typing.ClassVar


from email_template import render_email_template
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# from send_mail import  send_welcome_email
from models import  ParticipantRegistration, ProgressInfo, TaskSubmission, TaskInfo
from db import insert_into_table, get_some_thing, get_some_where, get_record_by_email, get_record_by_email

app = FastAPI(title="30-Day Python Challenge API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def populate_tasks():
    """Populate the tasks table with 30 days of challenges"""
    tasks_data = [
        (1, "Hello Python", "Write a program that prints 'Hello, World!' and your name", "beginner"),
        (2, "Variables and Data Types", "Create variables of different data types and print their types", "beginner"),
        (3, "User Input", "Write a program that asks for user's name and age, then greets them", "beginner"),
        (4, "Basic Arithmetic", "Create a simple calculator for basic operations", "beginner"),
        (5, "Conditional Statements", "Write a program to check if a number is positive, negative, or zero", "beginner"),
        (6, "Loops - For", "Print the first 10 numbers using a for loop", "beginner"),
        (7, "Loops - While", "Create a number guessing game using while loop", "beginner"),
        (8, "Lists", "Create a list of fruits and perform various operations", "beginner"),
        (9, "Strings", "Write a program to reverse a string and count vowels", "beginner"),
        (10, "Functions", "Create a function to check if a number is prime", "beginner"),
        (11, "Dictionaries", "Create a phone book using dictionaries", "intermediate"),
        (12, "File Handling", "Read and write data to a text file", "intermediate"),
        (13, "Exception Handling", "Handle different types of exceptions in your code", "intermediate"),
        (14, "List Comprehensions", "Use list comprehensions to filter and transform data", "intermediate"),
        (15, "Classes and Objects", "Create a simple class for a bank account", "intermediate"),
        (16, "Modules", "Create your own module and import it", "intermediate"),
        (17, "Regular Expressions", "Use regex to validate email addresses", "intermediate"),
        (18, "Working with APIs", "Fetch data from a public API using requests", "intermediate"),
        (19, "Data Structures", "Implement a stack using lists", "intermediate"),
        (20, "Algorithms", "Implement bubble sort algorithm", "intermediate"),
        (21, "Decorators", "Create and use custom decorators", "advanced"),
        (22, "Generators", "Create a generator for Fibonacci sequence", "advanced"),
        (23, "Context Managers", "Create a custom context manager", "advanced"),
        (24, "Multithreading", "Create a program using multiple threads", "advanced"),
        (25, "Database Operations", "Perform CRUD operations with SQLite", "advanced"),
        (26, "Web Scraping", "Scrape data from a website using BeautifulSoup", "advanced"),
        (27, "Testing", "Write unit tests for your previous functions", "advanced"),
        (28, "Data Analysis", "Analyze data using pandas (if available)", "advanced"),
        (29, "Final Project Setup", "Plan and start your final project", "advanced"),
        (30, "Final Project", "Complete and present your final project", "advanced"),
    ]
    


@app.get("/")
def read_root():
    """Root endpoint to serve the home page"""
    return FileResponse("templates/home.html")

@app.post("/api/register")
async def register_participant(participant: ParticipantRegistration):
    """Register a new participant for the challenge"""
    is_registered = get_record_by_email("participants", participant.email)
    if is_registered:
        raise HTTPException(status_code=400, detail="Participant already registered")
    try:
        data = participant.dict()
        inserted_record = insert_into_table("participants", data)
        print("before sending email")
        if inserted_record:
            print(f"Participant {participant.full_name} registered successfully.")
            try:
                send_welcome_email(first_name=participant.full_name, participant_email=participant.email)
                print(f"Welcome email sent to {participant.email}")
            except Exception as e:
                print(f"Error sending welcome email: {e}")
                raise HTTPException(status_code=500, detail="Failed to send welcome email")
        else:
            raise HTTPException(status_code=500, detail="Failed to register participant")

        return {"message": "Participant registered successfully", "participant": inserted_record}
    except Exception as e:
        print(f"Error inserting participant: {e}")
        raise HTTPException(status_code=500, detail="User already exists")


@app.post("/api/submit")
async def submit_task(submission: TaskSubmission):
    """Submit a solution for a specific task"""
    is_participant = get_record_by_email("participants", submission.participant_email)
    if not is_participant:
        raise HTTPException(status_code=404, detail="Participant not found. Please register first.")

    # task = get_some_thing("tasks")
    # if not task:
    #     raise HTTPException(status_code=404, detail="Task not found")

    existing_submission = get_some_where("submissions", "participant_email", submission.participant_email, "task_day", submission.task_day)
    if existing_submission:
        raise HTTPException(status_code=400, detail="Task already submitted")

    try:
        data = submission.dict()
        inserted_record = insert_into_table("submissions", data)
        return {"message": "Task submitted successfully", "submission": inserted_record}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error occurred")


@app.post("/api/progress")
async def get_progress(progress: ProgressInfo):
    """Get progress for a specific participant"""
    print(progress.participant_email)
    participant = get_record_by_email("participants", progress.participant_email)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    tasks = get_some_thing("tasks")
    submissions = get_record_by_email("submissions", progress.participant_email)

    print(submissions.get("3"))

    task_progress = []
    for task in tasks:
        task_day = task.get("day")
        submission = submissions.get(str(task_day))
        if submission:
            task_progress.append({
                "day": task_day,
                "title": task.get("title"),
                "status": "submitted",
                "solution": submission.get("solution"),
                "explanation": submission.get("explanation")
            })
        else:
            task_progress.append({
                "day": task_day,
                "title": task.get("title"),
                "status": "not submitted"
            })

            stat_count = {
                "total_tasks": len(tasks),
                "tasks": tasks,
                "completed_tasks": sum(1 for task in task_progress if task["status"] == "submitted"),
                "pending_tasks": sum(1 for task in task_progress if task["status"] == "not submitted"),
                "late_submissions": sum(1 for task in task_progress if task["status"] == "not submitted" and task.get("deadline") < "2023-10-31")
            }


    return {"progress": task_progress}

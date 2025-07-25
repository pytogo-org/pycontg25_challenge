import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import APIRouter, HTTPException, Request, Header, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import date, datetime, timezone

import jwt
from send_mail import send_daily_email, send_pre_challenge_info_email
from db import  get_some_thing, check_already_sent, log_email_sent

router = APIRouter()

API_ROOT = os.environ.get("API_ROOT")
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

token_url = f"{API_ROOT}/token"
print(f"Token URL: {token_url}")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)


# Ta base fictive d’utilisateurs
participants = [
 {
   "id": 5,
   "full_name": "Wachiou BOURAIMA",
   "email": "wachioubouraima56@gmail.com",
   "github_username": "wass",
   "registered_at": "2025-07-18 00:57:36.553598+00",
   "experience_level": "intermediate"
 },
 

 
]


tasks =  get_some_thing("tasks")
participants = get_some_thing("participants")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {
            "email": payload.get("sub"),
            "user_id": payload.get("user_id"),
            "full_name": payload.get("full_name"),
            "role": payload.get("role"),
        }
    except Exception:
        raise credentials_exception


@router.get("/send-daily-email")
async def send_daily_email_api(current_user: str = Depends(get_current_user)):
    """
    Endpoint to send the daily challenge email to participants.
    """
    print(current_user)
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # check the user role or permissions if needed
    if current_user["role"] not in ["Admin", "Developer-support"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Get today's date
    today = date.today()
    day_number = (today - datetime(2025, 7, 23).date()).days + 1
    index = day_number - 1

    if day_number < 1 or day_number > 30:
        raise HTTPException(status_code=400, detail="Invalid day number")
    
    if index >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found for today")
    
    task = tasks[index]

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for participant in participants:
        first_name = participant["full_name"]
        participant_email = participant["email"]

        # Check if email has already been sent today
        if check_already_sent(participant_email, day_number):
            print(f"Email already sent to {participant_email} for day {day_number}. Skipping.")
            continue
        else:
            try:
                send_daily_email(
                    first_name=first_name,
                    day_number=day_number,
                    fr_title=task["title_fr"],
                    en_title=task["title_en"],
                    fr_link=task.get("link_fr"),
                    en_link=task.get("link_en"),
                    participant_email=participant_email
                )
                log_email_sent(participant_email, day_number)
                print(f"Email sent to {participant_email} for day {day_number}.")
            except Exception as e:
                print(f"Failed to send email to {participant_email} for day {day_number}: {e}")
                continue

    return {"message": "Daily emails sent successfully."}

ALLOWED_USERS = {
    "dev@pytogo.org": {
        "password": "monmotdepassefort",
        "role": "Admin"
    }
}

@router.get("/send-daily-email_cron")
async def send_daily_email_cron(request: Request):


    # Calcul du jour
    start_date = datetime(2025, 7, 23).date()
    today = date.today()
    day_number = (today - start_date).days + 1
    index = day_number - 1

    if day_number < 1 or day_number > 30:
        raise HTTPException(status_code=400, detail="Invalid day number")

    task = tasks[index]

    for participant in participants:
        first_name = participant["full_name"]
        email = participant["email"]

        if check_already_sent(email, day_number):
            print(f"{email} déjà envoyé, on saute.")
            continue
        else:
            try:
                send_daily_email(
                    first_name=first_name,
                    day_number=day_number,
                    fr_title=task["title_fr"],
                    en_title=task["title_en"],
                    fr_link=task.get("link_fr"),
                    en_link=task.get("link_en"),
                    participant_email=email
                )
                log_email_sent(email, day_number)
                print(f"Email envoyé à {email} pour le jour {day_number}.")
            except Exception as e:
                print(f"Échec de l'envoi de l'email à {email} pour le jour {day_number}: {e}")
                continue
        
    send_daily_email(
        first_name="Participant",
        day_number=day_number,
        fr_title=task["title_fr"],
        en_title=task["title_en"],
        fr_link=task.get("link_fr"),
        en_link=task.get("link_en"),
        participant_email="omowass5@gmail.com"
    )

    return {"message": f"Emails du jour {day_number} envoyés avec succès."}

@router.get("/send-pre-challenge-info-email")
async def send_pre_challenge_info_email_api():
    """
    Endpoint to send the pre-challenge information email to participants.
    """
    
    for participant in participants:
        first_name = participant["full_name"]
        participant_email = participant["email"]
        # Check if email has already been sent
        if check_already_sent(participant_email, 0):
            print(f"Pre-challenge info email already sent to {participant_email}. Skipping.")
            continue
        else:
            # send_pre_challenge_info_email(first_name, participant_email=participant_email)
            log_email_sent(participant_email, 0)

    return {"message": "Pre-challenge information emails sent successfully."}

today = date.today()
day_number = (today - datetime(2025, 6, 23).date()).days + 1
if __name__ == "__main__":
    index = day_number - 1
    print(f"Today is day {day_number} of the challenge: {tasks[index]}.")
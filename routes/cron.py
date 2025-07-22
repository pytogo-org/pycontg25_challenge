import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import APIRouter, HTTPException, Request, Header, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import date, datetime, timezone

import jwt
from send_mail import send_daily_email
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
 {
   "id": 6,
   "full_name": "Uk'iva DAPAM",
   "email": "wasscodeur228@gmail.com",
   "github_username": "@dukst0n",
   "registered_at": "2025-07-18 05:47:55.833491+00",
   "experience_level": "beginner"
 },
 {
   "id": 7,
   "full_name": "omo wass",
   "email": "omowass5@gmail.com",
   "github_username": "omo wass",
   "registered_at": "2025-07-18 06:45:03.603765+00",
   "experience_level": "intermediate"
 },
 {
   "id": 8,
   "full_name": "Ibrahim",
   "email": "ibrahim@pytogo.org",
   "github_username": "",
   "registered_at": "2025-07-18 07:11:46.511461+00",
   "experience_level": "intermediate"
 },
 {
   "id": 10,
   "full_name": "Jonas O'Keefe",
   "email": "pydevstogo@gmail.com",
   "github_username": "virtual",
   "registered_at": "2025-07-18 08:11:54.399932+00",
   "experience_level": "intermediate"
 },
 {
   "id": 15,
   "full_name": "Jasen Huel",
   "email": "contact@pytogo.org",
   "github_username": "lime",
   "registered_at": "2025-07-18 08:20:54.713168+00",
   "experience_level": "advanced"
 },
 {
   "id": 20,
   "full_name": "Geoffrey Logovi",
   "email": "geoffreylogovi2@gmail.com",
   "github_username": "geoffreylgv",
   "registered_at": "2025-07-18 08:33:56.030493+00",
   "experience_level": "beginner"
 },
 {
   "id": 21,
   "full_name": "KUMA Kossi Stéphane ",
   "email": "wassioubouraim56@gmail.com",
   "github_username": "stephanekuma",
   "registered_at": "2025-07-18 09:40:02.109802+00",
   "experience_level": "beginner"
 },
 {
   "id": 22,
   "full_name": "AZIAGBENYO KOMLAN ELOM Laurent ",
   "email": "wachiou@uplift.ng",
   "github_username": "@Elom10Laurent",
   "registered_at": "2025-07-18 11:34:15.576937+00",
   "experience_level": "beginner"
 }
]


tasks =  get_some_thing("tasks")

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
    day_number = (today - datetime(2025, 7, 21).date()).days + 1
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
            send_daily_email(
            first_name=first_name,
            day_number=day_number,
            fr_title=task["title_fr"],
            en_title=task["title_en"],
            fr_link=task["link_fr"],
            en_link=task["link_en"],
            participant_email=participant_email
            )

        log_email_sent(participant_email, day_number)

    return {"message": "Daily emails sent successfully."}


today = date.today()
day_number = (today - datetime(2025, 6, 23).date()).days + 1
if __name__ == "__main__":
    index = day_number - 1
    print(f"Today is day {day_number} of the challenge: {tasks[index]}.")
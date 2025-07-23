from email import encoders
from email.mime.base import MIMEBase
from email.utils import formataddr
import json
import os
from dotenv import load_dotenv
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import date
from db import get_some_thing
from email_template import render_email_template


load_dotenv()

sender_email =  os.environ.get("SENDER_EMAIL")
receiver_email = "wasscodeur228@gmail.com"
password = os.environ.get("SENDER_EMAIL_PASSWORD")
smtp_server = os.environ.get("SMTP_SERVER")
smtp_server_port = os.environ.get("SMTP_SERVER_PORT")


def send_email_with_or_without_attachment(body, subject, sender_email=sender_email, receiver_email=receiver_email, password=password, smtp_server=smtp_server, smtp_server_port=smtp_server_port, filename=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] =  formataddr(('PyCon Togo Team', sender_email))
    msg['To'] = receiver_email

    msg.attach(MIMEText(body, 'html'))

    # Attachment
    if filename:
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
            msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_server_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def send_welcome_email(first_name="Pythonista", participant_email=None):
    """
    Sends a welcome email to the participant.
    
    Args:
        first_name (str): The first name of the participant.
    """
    from welcome import welcome_msg
    email_msgs = welcome_msg(first_name)
    for email in email_msgs:
        body = render_email_template(
            first_name=first_name,
            message=email['body']
        )
        subject = email['subject']
        send_email_with_or_without_attachment(body, subject, receiver_email=participant_email)


def send_daily_email(first_name, day_number, fr_title, en_title, fr_link, en_link, participant_email=None):
    """
    Sends the daily challenge email to the participant.
    """
    from welcome import  get_bilingual_challenge_email # , get_daily_challenge_email
    subject, body = get_bilingual_challenge_email(first_name, day_number, fr_title, en_title, fr_link, en_link)
    # email_msgs = get_daily_challenge_email(first_name, day_number, fr_title, en_title, fr_link, en_link)
    # for email in email_msgs:
    #     body = render_email_template(
    #         first_name=first_name,
    #         message=email['body']
    #     )
    #     subject = email['subject']
    body = render_email_template(
        first_name=first_name,
        message=body
    )
    send_email_with_or_without_attachment(body, subject, receiver_email=participant_email)


def send_pre_challenge_info_email(first_name, participant_email=None):
    """
    Sends the pre-challenge information email to the participant.
    """
    from welcome import get_pre_challenge_info_email
    subject, body = get_pre_challenge_info_email(first_name)
    body = render_email_template(
        first_name=first_name,
        message=body
    )
    send_email_with_or_without_attachment(body, subject, receiver_email=participant_email)

def submission_instruction_email(first_name, fr_titre, en_titre, fr_link, en_link, participant_email=None):
    """
    Sends the submission instruction email to the participant.
    """
    from welcome import get_submission_instruction_email
    subject, body = get_submission_instruction_email(first_name, fr_titre, en_titre, fr_link, en_link)
    body = render_email_template(
        first_name=first_name,
        message=body
    )
    send_email_with_or_without_attachment(body, subject, receiver_email=participant_email)

if __name__ == "__main__":
    
    today = date.today()
    day_number = (today - date(2025, 7, 23)).days + 1
    index = day_number - 1
    participants = get_some_thing("participants")
    if not participants:
        print("No participants found.")
        exit(1)
    with open("templates/tasks.json", "r") as file:
        tasks = json.load(file)

    if 0 <= index < len(tasks):
        task = tasks[index]
        first_name = "Pythonista"
        fr_title = task["title_fr"]
        en_title = task["title_en"]
        fr_link = task.get("link_fr")
        en_link = task.get("link_en")
        for participant in participants:
            participant_email = participant["email"]
            first_name = participant["full_name"]
            if not participant_email:
                print(f"No email found for participant {participant['full_name']}. Skipping.")
                continue
            print(f"Sending daily email for day {day_number} to {first_name} at {participant_email}... ")
            submission_instruction_email(
                first_name=first_name,
                fr_titre=fr_title,
                en_titre=en_title,
                fr_link=fr_link,
                en_link=en_link,
                participant_email=participant_email
            )
            print(f"Email sent to {first_name} at {participant_email}.")
    else:
        print(f"Invalid day number: {day_number}. No task found for this day.")
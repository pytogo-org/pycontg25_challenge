from email import encoders
from email.mime.base import MIMEBase
from email.utils import formataddr
import os
from dotenv import load_dotenv
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    from welcome import get_daily_challenge_email
    email_msgs = get_daily_challenge_email(first_name, day_number, fr_title, en_title, fr_link, en_link)
    for email in email_msgs:
        body = render_email_template(
            first_name=first_name,
            message=email['body']
        )
        subject = email['subject']
        send_email_with_or_without_attachment(body, subject, receiver_email=participant_email)


if __name__ == "__main__":
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
   "email": "ukiva.dapam@gmail.com",
   "github_username": "@dukst0n",
   "registered_at": "2025-07-18 05:47:55.833491+00",
   "experience_level": "beginner"
 },
 {
   "id": 7,
   "full_name": "Moukitat LASSISI",
   "email": "moukitatlassisi6@gmail.com",
   "github_username": "Moukitat LASSISI",
   "registered_at": "2025-07-18 06:45:03.603765+00",
   "experience_level": "intermediate"
 },
 {
   "id": 8,
   "full_name": "DORVI Yao Théodore ",
   "email": "tdorvi@gmail.com",
   "github_username": "",
   "registered_at": "2025-07-18 07:11:46.511461+00",
   "experience_level": "intermediate"
 },
 {
   "id": 10,
   "full_name": "Jonas O'Keefe",
   "email": "marguerite.welch@goldenmarine.net",
   "github_username": "virtual",
   "registered_at": "2025-07-18 08:11:54.399932+00",
   "experience_level": "intermediate"
 },
 {
   "id": 15,
   "full_name": "Jasen Huel",
   "email": "blake.hahn@goldenmarine.net",
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
   "email": "kumastephane@gmail.com",
   "github_username": "stephanekuma",
   "registered_at": "2025-07-18 09:40:02.109802+00",
   "experience_level": "beginner"
 },
 {
   "id": 22,
   "full_name": "AZIAGBENYO KOMLAN ELOM Laurent ",
   "email": "laziagbenyo@gmail.com",
   "github_username": "@Elom10Laurent",
   "registered_at": "2025-07-18 11:34:15.576937+00",
   "experience_level": "beginner"
 },
 {
   "id": 33,
   "full_name": "AGBOSSOUMONDE LUther",
   "email": "luthermondey53@gmail.com",
   "github_username": "lutherkingcp0",
   "registered_at": "2025-07-18 15:06:02.027752+00",
   "experience_level": "beginner"
 },
 {
   "id": 53,
   "full_name": "Samadou Ouro-agorouko ",
   "email": "souroagorouko@gmail.com",
   "github_username": "Bakugo90",
   "registered_at": "2025-07-19 10:53:13.92151+00",
   "experience_level": "intermediate"
 }
]

    for participant in participants:
        first_name = participant.get('full_name', 'Participant')
        participant_email = participant.get('email')
        try:
            send_welcome_email(first_name=first_name, participant_email=participant_email)
            print(f"Welcome email sent to {participant_email}")
        except Exception as e:
            print(f"Failed to send email to {participant_email}: {e}")
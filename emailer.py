import smtplib
from email.message import EmailMessage

# CHANGE THESE VALUES
SMTP_EMAIL = "gurutattvasadhak@gmail.com"
SMTP_PASSWORD = "yzgq ghnj nhop wrib"

def send_task_email(to_email, subject, body):
    msg = EmailMessage()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

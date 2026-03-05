import os
import smtplib
from email.mime.text import MIMEText

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_notice_email(to_email, subject, message):

    msg = MIMEText(message)

    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL_USER, EMAIL_PASS)

        server.sendmail(
            EMAIL_USER,
            [to_email],
            msg.as_string()
        )

        server.quit()

        return {"status": "Email sent"}

    except Exception as e:
        return {"status": str(e)}

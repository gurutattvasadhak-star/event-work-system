import smtplib
import os
from email.mime.text import MIMEText

def send_notice_email(to_email, subject, body):
    try:
        smtp_email = os.environ.get("SMTP_EMAIL")
        smtp_password = os.environ.get("SMTP_PASSWORD")

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = smtp_email
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()

        return "✅ Email sent successfully"

    except Exception as e:
        return f"❌ Email failed: {str(e)}"

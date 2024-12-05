import smtplib
from email.mime.text import MIMEText

def send_email(recipient_email: str, subject: str, body: str):
    """
    Send an email with the given subject and body.
    """
    sender_email = "sunnyadav.official@gmail.com"
    sender_password = "qsxf frwe epth kray"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

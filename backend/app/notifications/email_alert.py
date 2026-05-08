import smtplib
from email.mime.text import MIMEText


def send_email_alert(to_email, message):
    sender = "your_email@gmail.com"
    password = "your_app_password"

    msg = MIMEText(message)
    msg['Subject'] = 'Security Alert'
    msg['From'] = sender
    msg['To'] = to_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
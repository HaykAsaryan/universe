import ssl
import smtplib
import random
from email.message import EmailMessage


def sendMail(Subject, Text, To):
    email_sender = ""
    email_password = ""
    email_receiver = To

    subject = Subject
    body = Text

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

        

def createCode():
    verification_code = str(random.randint(0, 999999))
    while len(verification_code) < 6:
        verification_code = "0" + verification_code
    
    return verification_code
import random
import string
import http.client
import smtplib
from email.message import EmailMessage
from datetime import datetime,timedelta
from django.http import HttpResponse

def generate_simple_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def send_mail(to,username,password,fname):
    msg=EmailMessage()
    subject="Your Admin Account Details"
    body=f'''Dear { fname },

    I hope this message finds you well.

    We have created an admin account for you. Below are your login credentials:

    Username: { username }
    Password: { password }

    Please keep this information secure and do not share it with anyone.

    To log in, visit: IVPE.

    Important: For security reasons, we recommend that you change your password after your first login.

    If you have any issues or need further assistance, feel free to reach out.

    Best regards,
    Admin
    IVPE'''
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    user="ivpe68030@gmail.com"
    msg['from']=user
    password="utba gpfp sfgt lagn"
     
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()

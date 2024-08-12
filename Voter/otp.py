import random
import http.client
import smtplib
from email.message import EmailMessage
from datetime import datetime,timedelta
from django.http import HttpResponse

def generate_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

'''def send_otp(phone,otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey="427520ApBUXZ2TfOk66b4d03dP1"
    headers = { 'Content-Type': "application/JSON" }
    message = "your otp is " + otp
    encoded_message = urllib.parse.quote(message)  
    urls = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+phone+"&authkey="+authkey+"&country=91"
    conn.request("GET", urls, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return None'''
    

'''def send_otp(phone,otp):
    client = vonage.Client(key="7bbb08c8", secret="Xzn3goWYiPSidXVw")
    responseData = client.sms.send_message(
    {
        "from": 'IVPE',
        "to":918594034332,
        "text": "A text message sent using the Vonage SMS API",
    }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")''' 

def send_email(to,otp):
    msg=EmailMessage()
    subject="Register"
    body=f"Your otp for IVPE registration is {otp}.Please do not share it with any one"
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
     

def validate_otp(request,otp):
    print(otp)
    session_otp = request.session.get('otp')
    otp_expires_str = request.session.get('otp_expires')
    if session_otp and otp_expires_str:
        otp_expires = datetime.fromisoformat(otp_expires_str)
        if str(session_otp) == otp:
            return 1
        elif str(session_otp) == otp and datetime.now() > otp_expires:
            return -1
        elif str(session_otp) != otp:
            return 0
        else:
            return 0
    return None

def clear_otp(request):
    if 'otp' in request.session:
        del request.session['otp']
        del request.session['otp_expires']
    return HttpResponse("OTP cleared")


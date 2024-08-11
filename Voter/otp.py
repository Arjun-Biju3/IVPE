import requests
import random
import http.client
import smtplib
from email.message import EmailMessage

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
    subject="Register"
    body=f"Your otp for IVPE registration is {otp}.Please do not share it with any one"
    msg=EmailMessage()
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
     
     

    
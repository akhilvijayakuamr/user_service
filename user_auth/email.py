import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import grpc
from grpc import StatusCode
from .models import CustomUser
from django.conf import settings


# Sent Email 

def send_otp_mail(context, email):
    otp = random.randint(100000, 999999)
    sender_email = settings.EMAIL_HOST_USER
    receiver_email = email
    password_email = settings.EMAIL_HOST_PASSWORD

    subject = "AssureTech: Your One-Time Password (OTP) for Registration"
    message = f"""Dear AssureTech User, You have initiated a registration request with AssureTech. Your verification code is: {otp} The code will expire in 10 minutes. For your account's security, please do not share this code with anyone else. Thank you for choosing AssureTech!"""
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() 
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
    except smtplib.SMTPAuthenticationError:
        context.abort(StatusCode.INTERNAL, "Failed to send OTP email. Please check your email configuration.")
    
    except Exception as e:
        context.abort(StatusCode.INTERNAL, f'An error occurred: {str(e)}')
    user = CustomUser.objects.get(email=email)
    user.otp = otp
    user.save()
from django.shortcuts import render
from .models import CustomUser
from proto import user_service_pb2
from proto import user_service_pb2_grpc
from .serializers import CustomUserSerializer, VerifyUserSerializer
from grpc import StatusCode
from .email import send_otp_mail
from django.utils import timezone
import jwt
from django.conf import settings

# Create your views here.



# User Register

def user_register(data, context):
    email = data.get('email')
    username = data.get('username')

    
    if CustomUser.objects.filter(email=email).exists():
        context.abort(StatusCode.ALREADY_EXISTS, "Email Already Exists")

    if CustomUser.objects.filter(username=username).exists():
        context.abort(StatusCode.ALREADY_EXISTS, "Username Already Exists")


    serializer = CustomUserSerializer(data=data)
    try:
        serializer.is_valid(raise_exception=True)
        user = serializer.save()


        send_otp_mail(context, serializer.data['email'])

        return {
            'message': 'Registration Successful, Check Email For Verification',
            'error': '',
            'id': user.id,
            'email': user.email
        }

    except Exception as e:
        context.abort(StatusCode.INTERNAL, f"An unexpected error occurred: {str(e)}")
        
        
 
 # OTP verification       
        
        
def otp_verification(data, context):
    
    serializer = VerifyUserSerializer(data=data)
    if not serializer.is_valid():
        errors = serializer.errors
        context.abort(StatusCode.INVALID_ARGUMENT, f"Validation Error: {errors}")
    
    
    validated_data = serializer.validated_data
    email = validated_data.get('email')
    otp = validated_data.get('otp')

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User not found")

    if user.otp != otp:
        context.abort(StatusCode.INVALID_ARGUMENT, "Invalid OTP")

    user.is_verified = True
    user.otp = None
    user.save()

    return {
        'message': "Account Verified",
        'error': '',
        'email': user.email
    }
    
    
    
# Authentication Login
    
def authenticate_user(email, password, provider, context):
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User not found")

    
    if not user.is_verified:
        context.abort(StatusCode.PERMISSION_DENIED, "User not verified")

    
    if user.is_superuser:
        context.abort(StatusCode.PERMISSION_DENIED, "Admin can't access")

    
    if provider != 'google' and not user.check_password(password):
        context.abort(StatusCode.INVALID_ARGUMENT, "Incorrect password")


    payload = {
        'id': user.id,
        'exp': timezone.now() + timezone.timedelta(days=2),
        'iat': timezone.now(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return user, token



from django.shortcuts import render
from user_auth.models import CustomUser
from grpc import StatusCode
from django.utils import timezone
import jwt
from django.conf import settings


# Create your views here.



# Authentication Admin


def authenticate_admin(email, password, context):
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User not found")
        
    if not user.is_superuser and not user.is_staff:
        context.abort(StatusCode.PERMISSION_DENIED, "User can't access")
        
    if not user.check_password(password):
        context.abort(StatusCode.INVALID_ARGUMENT, "Incorrect password")
    
    payload = {
        'id': user.id,
        'exp': timezone.now() + timezone.timedelta(days=2),
        'iat': timezone.now(),
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token
        
        
        
# Get all users


def all_users(context):
    try:
        users = CustomUser.objects.all() 
        return users
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "Users not found")
        
        
        
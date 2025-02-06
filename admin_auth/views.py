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
    
    access_payload = {
        'id': user.id,
        'exp': timezone.now() + timezone.timedelta(minutes=15), 
        'iat': timezone.now(),
    }

    refresh_payload = {
        'id': user.id,
        'exp': timezone.now() + timezone.timedelta(days=15),  
        'iat': timezone.now(),
    }
    
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")
    

    return access_token, refresh_token
    
        
        
        
# Get all users

def all_users(context):
    try:
        users = CustomUser.objects.filter(is_superuser=False) 
        return users
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "Users not found")
        
        
        
        
# Block and unblock user
        
def block_unblock_user(user_id, context):
    try:
        user = CustomUser.objects.get(id=int(user_id))
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User not found")
    user.is_active = not user.is_active
    user.save()
    action = "blocked" if not user.is_active else "unblocked"
    return f"User successfully {action}"




# Get all dashboard user details

def user_dashboard(context):
    try:
        all_users = CustomUser.objects.all().count()
        block_users = CustomUser.objects.filter(is_active=False).count()
        return all_users, block_users
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User not found")
        
        
    
        
        
        
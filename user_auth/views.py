from django.shortcuts import render
from .models import CustomUser, UserProfile, Following
from proto import user_service_pb2
from .serializers import CustomUserSerializer, VerifyUserSerializer
from grpc import StatusCode
from .email import send_otp_mail
from django.utils import timezone
import jwt
from django.conf import settings
import uuid
import time
from django.core.files.base import ContentFile


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
        serializer.save()

        send_otp_mail(context, serializer.data['email'])

        return {
            'message': 'Registration Successful, Check Email For Verification',
            'error': '',
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
        context.abort(StatusCode.NOT_FOUND, "user not found")

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
    
    
    
    
# Resend otp

def recreate_otp(email, context):
    try:
        user = CustomUser.objects.get(email=email)
        
        if not user:
            context.abort(StatusCode.NOT_FOUND, "Please Register again")
            
        send_otp_mail(context, email)
        
        return {
            'message': 'Check Email For Verification',
            'error': '',
        }
        
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "Please Register again")
      
    
    
       
# Authentication User
    
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
    
    try:
        profile = UserProfile.objects.get(user=user)
        profile_img = profile.profile_image.url if profile.profile_image else ''
    except UserProfile.DoesNotExist:
        profile_img = ''
    
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    return user, access_token, refresh_token, profile_img




# check auth

def auth_check(token, context):
    try:
        payload = jwt.decode(token.token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload['id']
        
        try:
            user = CustomUser.objects.filter(id=user_id).first()
        except CustomUser.DoesNotExist:
            context.abort(StatusCode.NOT_FOUND, "Autherization Failed")
        
        if not user:
            context.abort(StatusCode.PERMISSION_DENIED, "User not found")
            
        if user.is_superuser:
            return {
                'id':str(id),
                'admin': True,
                'user': False,
                'message':'Autherization Success',
            }
             
        else:
            return {
                'id':str(id),
                'admin': False,
                'user': True,
                'message':'Autherization Success',
            } 
            
            
    except jwt.ExpiredSignatureError:
       context.abort(StatusCode.UNAUTHENTICATED, "Token has expired")
                  
    
         
         
# Take profile data

def profile_data(id, profile_id, context):
    try:
        user = CustomUser.objects.get(id=profile_id)
        profile_user = CustomUser.objects.get(id=id)
        user_id = user.id
        user_username = user.username
        user_fullname = user.full_name
        
        try:
            user_profile = UserProfile.objects.get(user = user)
            user_location = user_profile.location if user_profile else ''
            user_bio = user_profile.bio if user_profile else ''
            user_dob = user_profile.date_of_birth if user_profile else ''
            user_profile_image = user_profile.profile_image.url if user_profile else ''
            user_cover_image = user_profile.cover_photo.url if user_profile else ''
            follow = Following.objects.filter(follower=profile_user, followed=user, is_active=True, is_delete=False).exists()
            followers_count = Following.objects.filter(followed=user, is_active=True, is_delete=False)
            following_count = Following.objects.filter(follower=user, is_active=True, is_delete=False)
            
           
        except UserProfile.DoesNotExist:
            
            user_location = ''
            user_bio = ''
            user_dob = ''
            user_profile_image = ''
            user_cover_image = ''
            follow = Following.objects.filter(follower=profile_user, followed=user, is_active=True, is_delete=False).exists()
            followers_count = Following.objects.filter(followed=user, is_active=True, is_delete=False)
            following_count = Following.objects.filter(follower=user, is_active=True, is_delete=False)
      
        return {
            'id':user_id,
            'username':user_username,
            'full_name':user_fullname,
            'location':user_location,
            'bio':user_bio,
            'dob':str(user_dob),
            'profileimage':user_profile_image,
            'coverimage':user_cover_image,
            'follow':follow,
            'followers_count':followers_count.count(),
            'following_count':following_count.count()
        }
       
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.PERMISSION_DENIED, "User not found")
        
    
    
    
# Update profile

def update_profile_data(request, context):
    user_id = request.id
    username = request.username
    full_name = request.full_name
    location = request.location
    bio = request.bio
    dob = request.dob
    profile_image = request.profileimage
    cover_image = request.coverimage
    
    try:
        user = CustomUser.objects.get(id=user_id)
        user.username = username
        user.full_name = full_name
        user.save()
        
        user_profile, created = UserProfile.objects.get_or_create(user=user)
                
        if profile_image:
            profile_image_name = f"profile_{uuid.uuid4().hex}_{int(time.time())}.jpg"
            profile_image_storage = user_profile.profile_image.storage
            unique_profile_image_name = profile_image_storage.get_available_name(profile_image_name)
            user_profile.profile_image.save(unique_profile_image_name, ContentFile(profile_image))
                
        if cover_image:
            cover_photo_name = f"cover_{uuid.uuid4().hex}_{int(time.time())}.jpg"
            cover_photo_storage = user_profile.cover_photo.storage
            unique_cover_photo_name = cover_photo_storage.get_available_name(cover_photo_name)
            user_profile.cover_photo.save(unique_cover_photo_name, ContentFile(cover_image))
        
        if bio:
            user_profile. bio = bio
                
        if dob:
            user_profile.date_of_birth = dob
                
        if location:
            user_profile.location = location
            
            
        user_profile.save()
        
        return {
            'message':'Updated Successfully',
            'error':''
        }
        
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User not found")
    
    
    
            
# Google auth

def google_user(email, full_name, context):
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        user, created = CustomUser.objects.get_or_create(email=email,
                                                         full_name=full_name,
                                                         is_active = True,
                                                         is_verified = True,
                                                         is_superuser = False
                                                         )
    if not user.is_verified:
        context.abort(StatusCode.PERMISSION_DENIED, "User not verified")
    if user.is_superuser:
        context.abort(StatusCode.PERMISSION_DENIED, "Admin can't access")


    access_payload = {
        'id': user.id,
        'exp': timezone.now() + timezone.timedelta(minutes=1), 
        'iat': timezone.now(),
    }

    refresh_payload = {
        'id': user.id,
        'exp': timezone.now() + timezone.timedelta(days=15),  
        'iat': timezone.now(),
    }
    
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")
    return user, access_token, refresh_token




# Forgot Email

def forgot_email(email, context):
    try:
        user = CustomUser.objects.get(email = email)
        if not user:
            context.abort(StatusCode.NOT_FOUND, "User is not found plese check your email")
        send_otp_mail(context, email)
        
        return {
             'message': 'Check Email For Verification'
        }
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User is not found plese check your email")
        
        
        
        
# Change password

def change_password(email, password, context):
    try:
        user = CustomUser.objects.get(email = email)
        
        if not user:
            context.abort(StatusCode.NOT_FOUND, "User is not found plese check your email")
            
        user.set_password(password)
        user.save()
        
        return {
             'message': 'Successfully Password Changed'
        }
        
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User is not found plese check your email")
        
        
            
        
# Get user profile image

def profile_image(user_id, context):
    try:
        user = CustomUser.objects.get(id=user_id)
        try:
            profile = UserProfile.objects.get(user=user)
            return {
                'user_profile':profile.profile_image.url
            } 
        except UserProfile.DoesNotExist:
           return {
                'user_profile':''
            } 
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User is not found")
        
        
        
        
       
# Get unique post profile image and bio

def unique_post_data(user_id, context):
    try:
        user = CustomUser.objects.get(id=user_id)
        try:
            profile = UserProfile.objects.get(user=user)
            return {
                'full_name':user.full_name,
                'username':user.username,
                'user_profile':profile.profile_image.url if profile.profile_image.url else '',
                'bio' : profile.bio if profile.bio else ''
            } 
            
        except UserProfile.DoesNotExist:
          return {
                'full_name':user.full_name,
                'username':user.username,
                'user_profile':'',
                'bio' : ''
            } 
             
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User is not found")
        
        
        
        
# Take comment user profile

def comment_profile(user_id, context):
    try:
        user = CustomUser.objects.get(id=user_id)
        try:
            profile = UserProfile.objects.get(user=user)
            return {
                'full_name':user.full_name,
                'user_profile':profile.profile_image.url if profile.profile_image else ''
            } 
        except UserProfile.DoesNotExist:
          return {
                'full_name':user.full_name,
                'user_profile':''
            }
        
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User is not found")
        
        
        
        
        
# User Follow

def user_follow(user_id, folllow_user_id, context):
    try:
        user = CustomUser.objects.get(id=user_id)
        
        try:
            follow_user = CustomUser.objects.get(id=folllow_user_id)
            following_relationship, created = Following.objects.get_or_create(
                follower = user, 
                followed = follow_user
            )
            
            following_relationship.is_active = not following_relationship.is_active
            following_relationship.save()
            message = "You are now following this user" if following_relationship.is_active else "You have unfollowed this user."
            return {
             'message': message
            }
            
            
        except CustomUser.DoesNotExist:
            context.abort(StatusCode.NOT_FOUND, "Following user is not found")
            
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "User is not found")





# search User

def search_user(user_id, query, context):
    try:
        all_users = []
        users = CustomUser.objects.filter(full_name__icontains = query).exclude(id=user_id)
        for user in users:
            try:
                profile = UserProfile.objects.get(user=user)
                profile_image_url = profile.profile_image.url if profile.profile_image else ''
            except UserProfile.DoesNotExist:
                profile_image_url = ''

            all_users.append(user_service_pb2.Search(
                id = user.id,
                full_name = user.full_name,
                user_name = user.username,
                user_profile = profile_image_url
            ))
        return all_users
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "Users not found")
        
        
        
        
# Get all followers and followings

def get_friends(user_id, context):
    try:
        main_user = CustomUser.objects.get(id=user_id)
        all_follower = []
        all_following = []
        
        try:
            followers = Following.objects.filter(followed=main_user, is_active=True, is_delete=False)
            for folower in followers:
                user = CustomUser.objects.get(id = folower.follower.id)
                
                try:
                    profile = UserProfile.objects.get(user=user)
                    profile_image_url = profile.profile_image.url if profile.profile_image else ''
                except UserProfile.DoesNotExist:
                    profile_image_url = ''
                
                
                all_follower.append(
                    user_service_pb2.Friend(
                        id = user.id,
                        full_name = user.full_name,
                        user_name = user.username,
                        user_profile = profile_image_url
                    ))
        
        except Following.DoesNotExist:
            all_follower=[]
            
        try:
            followed = Following.objects.filter(follower=main_user, is_active=True, is_delete=False)
        
            for folow in followed:
                user = CustomUser.objects.get(id = folow.followed.id)
                try:
                    profile = UserProfile.objects.get(user=user)
                    profile_image_url = profile.profile_image.url if profile.profile_image else ''
                except UserProfile.DoesNotExist:
                    profile_image_url = ''
                
                all_following.append(
                    user_service_pb2.Friend(
                        id = user.id,
                        full_name = user.full_name,
                        user_name = user.username,
                        user_profile = profile_image_url
                    ))
        except Following.DoesNotExist:
            all_following = []
            
            
        return {
            "follower":all_follower,
            "followed":all_following
        }
            
    except CustomUser.DoesNotExist:
        context.abort(StatusCode.NOT_FOUND, "Users not found")
        
        
        
        
        
# Create new access token

def refresh_check(token, context):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload['id']
        
        try:
            user = CustomUser.objects.filter(id=user_id).first()
        except CustomUser.DoesNotExist:
            context.abort(StatusCode.NOT_FOUND, "Autherization Failed")
        
        if not user:
            context.abort(StatusCode.PERMISSION_DENIED, "User not found")
        
        access_payload = {
            'id': user_id,
            'exp': timezone.now() + timezone.timedelta(minutes=15), 
            'iat': timezone.now(),
        }

        refresh_payload = {
            'id': user_id,
            'exp': timezone.now() + timezone.timedelta(days=15),  
            'iat': timezone.now(),
        }
        
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")
        
        return {
            'access_token':str(access_token),
            'refresh_token': str(refresh_token),
            }
             
    except jwt.ExpiredSignatureError:
        context.abort(StatusCode.UNAUTHENTICATED, "Token has expired")
        
        
        
        
        

            
        

        
            
        
        
            
    
        
        
        

        
      
    
            
            
    



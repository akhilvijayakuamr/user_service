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



class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    
    # Register user view

    def CreateUser(self, request, context):
        email = request.email
        username = request.username
        
        data = {
            'email': request.email,
            'username': request.username,
            'full_name': request.full_name,
            'password': request.password
        }
        
        
        if CustomUser.objects.filter(email=email).exists():
            context.abort(StatusCode.ALREADY_EXISTS, "Email Already Exists")

        if CustomUser.objects.filter(username=username).exists():
            context.abort(StatusCode.ALREADY_EXISTS, "Username Already Exists")
            
        serializer = CustomUserSerializer(data=data)
        
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            send_otp_mail(context, serializer.data['email'])
            
            
            return user_service_pb2.CreateUserResponse(
                message='Registration Successful, Check Email For Verification',
                error=''  
            )
            
        
        except Exception as e:
            context.abort(StatusCode.INTERNAL, f"An unexpected error occurred: {str(e)}")
            
            
            
    # OTP verify view      
            
    def VerifyOtp(self, request, context):
        
        data = {
            'email' : request.email,
            'otp' : request.otp
        }
        
        try:
            serializer = VerifyUserSerializer(data=data)
            if serializer.is_valid():
                email = data['email']
                otp = data['otp']
                
                try:
                    user = CustomUser.objects.get(email=email).first()
                except CustomUser.DoesNotExist:
                    context.abort(StatusCode.NOT_FOUND, "User not found")
                    
                if user.otp != otp:
                    context.abort(StatusCode.INVALID_ARGUMENT, "Invalid otp")
                    
                user.is_verified = True
                user.otp = None
                user.save()
                
                return user_service_pb2.VerifyOtpResponse(
                    message="Account Verified",
                    error=''
                )
            else:
                errors = serializer.errors
                context.abort(StatusCode.INVALID_ARGUMENT, f"Validation Error: {errors}")
                
        except Exception as e:
            context.abort(StatusCode.INTERNAL, f"Internal Server Error: {str(e)}")
            
            
            
    # Login user view
    
    
    def LoginUser(self, request, context):
        email = request.email
        password = request.password
        provider = request.provider
        
        user = CustomUser.objects.get(email=email).first()
        
        if user is None:     
            context.abort(StatusCode.NOT_FOUND, "User not found")
            
        if not user.is_verified:
            context.abort(StatusCode.PERMISSION_DENIED, "User not varified")
            
        if user.is_superuser == True:
            context.abort(StatusCode.PERMISSION_DENIED, "Admin Can't access")
            
        if provider != 'google' and not user.check_password(password):
            context.abort(StatusCode.INVALID_ARGUMENT, 'Incorrect Password')
            
        payload = {
            'id': user.id,  
            'exp': timezone.now() + timezone.timedelta(minutes=60),
            'iat': timezone.now(),
        }
            
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        print("token",token)
        
        return user_service_pb2.LoginResponse(
            id = str(user.id)
            email = user.email
            jwt = str(token)
            message = "Login Success"
        )
        
                


        
        
    
        
        
    
        
        

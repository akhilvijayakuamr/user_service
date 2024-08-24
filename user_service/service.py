from proto import user_service_pb2
from proto import user_service_pb2_grpc
from user_auth.views import user_register, otp_verification, authenticate_user




class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    
    
    # User Register
    
    def CreateUser(self, request, context):
    
        data = {
            'email': request.email,
            'username': request.username,
            'full_name': request.full_name,
            'password': request.password
        }

        response_data = user_register(data, context)

        return user_service_pb2.CreateUserResponse(
            message=response_data['message'],
            error=response_data['error'],
            id=response_data['id'],
            email=response_data['email']
        )
        
        
    # Verification OTP
        
    def VerifyOtp(self, request, context):
    
        data = {
            'email': request.email,
            'otp': request.otp
        }

        response_data = otp_verification(data, context)

        return user_service_pb2.VerifyOtpResponse(
            message=response_data['message'],
            error=response_data['error']
        )
        
        
    # User Login
        
    def LoginUser(self, request, context):
        email = request.email
        password = request.password
        provider = request.provider

        user, token = authenticate_user(email, password, provider, context)

        return user_service_pb2.LoginResponse(
            id=str(user.id),
            email=user.email,
            jwt=str(token),
            message="Login Success"
        )
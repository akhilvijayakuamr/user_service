from proto import user_service_pb2
from proto import user_service_pb2_grpc
from user_auth.views import user_register, otp_verification, authenticate_user, recreate_otp
from admin_auth.views import authenticate_admin, all_users





class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    
    
    # User Register
    
    def CreateUser(self, request, context):
    
        data = {
            'email': request.email,
            'username': request.username,
            'full_name': request.full_name,
            'password': request.password
        }
        
        print(data)

        response_data = user_register(data, context)
        
        return user_service_pb2.CreateUserResponse(
            message=response_data['message'],
            error=response_data['error']
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
            error=response_data['error'],
        )
        
        
    # Resend OTP
    
    
    def ResendOtp(self, request, context):
        
        email = request.email
        response_data = recreate_otp(email, context)
 
        return user_service_pb2.ResendOtpResponse(
            message=response_data['message'],
            error=response_data['error'],
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
        
        
    # Admin Login
    
    
    def LoginAdmin(self, request, context):
        email = request.email
        password = request.password
        
        token = authenticate_admin(email, password, context)
        print(token)
        return user_service_pb2.LoginAdminResponse(
            jwt = str(token),
            message = "Login Success"
        )
        
        
    def UserList(self, request, context):
        users = all_users(context)
        user_list = [user_service_pb2.User(id=user.id,
                                           username=user.username,
                                           full_name=user.full_name,
                                           email=user.email,
                                           is_active=user.is_active) for user in users]
        return user_service_pb2.UserListResponse(users=user_list)
from proto import user_service_pb2
from proto import user_service_pb2_grpc
from user_auth.views import *
from admin_auth.views import authenticate_admin, all_users, block_unblock_user
from django.core.files.base import ContentFile  





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

        user, token, profile_img  = authenticate_user(email, password, provider, context)
        
      

        return user_service_pb2.LoginResponse(
            id=str(user.id),
            email=user.email,
            jwt=str(token),
            message= "Login Success",
            profile = profile_img
        )
        
        
    # Admin Login
    
    
    def LoginAdmin(self, request, context):
        email = request.email
        password = request.password
        
        token = authenticate_admin(email, password, context)
        return user_service_pb2.LoginAdminResponse(
            jwt = str(token),
            message = "Login Success"
        )
        
        
    # Get Allusers
        
    def UserList(self, request, context):
        users = all_users(context)
        user_list = [user_service_pb2.User(id=str(user.id),
                                           username=user.username,
                                           full_name=user.full_name,
                                           email=user.email,
                                           is_active=user.is_active) for user in users]
        return user_service_pb2.UserListResponse(users=user_list)
    
    
    # Check Auth
    
    def Autherization(self, request, context):
        response = auth_check(request, context)
        return user_service_pb2.AuthResponse(
            id = response['id'],
            admin= response['admin'],
            user= response['user'],
            message = response['message']
        )
        
        
    # Block and Unblock user
        
    def BlockUnblockUser(self, request, context):
        user_id = request.id
        response = block_unblock_user(user_id, context)
        return user_service_pb2.BlockUnBlockResponse(message=response)
    
    
    
    # Take and User profile Data
    
    def ProfileData(self, request, context):
        user_id = request.id
        response = profile_data(user_id, context)
        return user_service_pb2.ProfileDataResponse(
            id = response['id'],
            username = response['username'],
            full_name = response['full_name'],
            location = response.get('location', ''),
            bio = response.get('bio', ''),
            dob = response.get('dob', ''),
            profileimage = response.get('profileimage', ''),
            coverimage = response.get('coverimage', ''),
        )
        


    # Update profile 
        
    def ProfileUpdate(self, request, context):
        response = update_profile_data(request, context)
        return user_service_pb2.ProfileUpdateResponse(
            message = response['message'],
            error = response['error']
        )
        
        
        
    # Google auth
    
    
    
    def GoogleUser(self, request, context):
        email = request.email
        password = request.full_name

        user, token = google_user(email, password, context)

        return user_service_pb2.GoogleUserResponse(
            id=str(user.id),
            email=user.email,
            jwt=str(token),
            message="Login Success"
        )
        
        
    # Forgote 
    

    def ForgotEmail(self, request, context):
        
        email = request.email
        response_data = forgot_email(email, context)
        return user_service_pb2.ForgoteEmailResponse(
            message=response_data['message'],
        )
        
        
    # Change password
    
    
    def ChangePassword(self, request, context):
        email = request.email
        password = request.password
        response_data = change_password(email, password, context)
        return user_service_pb2.ChangePasswordResponse(
            message=response_data['message'],
        )
        
        
    # get user profile photo
        
    def PostProfile(self, request, context):
        user_id = request.user_id
        print("user_Di",user_id)
        response = profile_image(user_id, context)
        return user_service_pb2.PostProfileResponse(
            profile_image = response['user_profile']
        )
        
        
        
    # get unique post data
    
    
    def PostUniqueData(self, request, context):
        user_id = request.user_id
        response = unique_post_data(user_id, context)
        return user_service_pb2.PostUniqueDataResponse(
            full_name = response['full_name'],
            username = response['username'],
            profile_image = response['user_profile'],
            bio = response['bio']
        )
        
        
        
    # Take comment post data
    
    
    
    def CommentUniqueData(self, request, context):
        user_id = request.user_id
        response = comment_profile(user_id, context)
        return user_service_pb2.CommentUniqueDataResponse(
            full_name = response['full_name'],
            user_profile = response['user_profile']
            
        )
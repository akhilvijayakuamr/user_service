from proto import user_service_pb2
from proto import user_service_pb2_grpc
from user_auth.views import *
from admin_auth.views import *
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

        user, access_token, refresh_token, profile_img  = authenticate_user(email, password, provider, context)
        
        return user_service_pb2.LoginResponse(
            id=str(user.id),
            email=user.email,
            access_token = str(access_token),
            refresh_token = str(refresh_token),
            message= "Login Success",
            profile = profile_img
        )
        
        
        
    # Admin Login

    def LoginAdmin(self, request, context):
        email = request.email
        password = request.password
        
        access_token, refresh_token = authenticate_admin(email, password, context)
        return user_service_pb2.LoginAdminResponse(
            access_token = str(access_token),
            refresh_token = str(refresh_token),
            message = "Login success"
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
        profile_id = request.profile_id
        response = profile_data(user_id, profile_id, context)
        return user_service_pb2.ProfileDataResponse(
            id = response['id'],
            username = response['username'],
            full_name = response['full_name'],
            location = response.get('location', ''),
            bio = response.get('bio', ''),
            dob = response.get('dob', ''),
            profileimage = response.get('profileimage', ''),
            coverimage = response.get('coverimage', ''),
            follow = response.get('follow', False),
            followers_count = response.get('followers_count', 0),
            following_count = response.get('following_count', 0)
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

        user, access_token, refresh_token= google_user(email, password, context)

        return user_service_pb2.GoogleUserResponse(
            id=str(user.id),
            email=user.email,
            access_token=str(access_token),
            refresh_token=str(refresh_token),
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
        response = profile_image(user_id, context)
        return user_service_pb2.PostProfileResponse(
            profile_image = response.get('user_profile', '')
        )
        
        
               
        
    # get unique post data
    
    def PostUniqueData(self, request, context):
        user_id = request.user_id
        response = unique_post_data(user_id, context)
        return user_service_pb2.PostUniqueDataResponse(
            full_name = response['full_name'],
            username = response['username'],
            profile_image = response.get('user_profile', ''),
            bio = response.get('bio', '')
        )
        
        
        
               
        
    # Take comment post data
    
    def CommentUniqueData(self, request, context):
        user_id = request.user_id
        response = comment_profile(user_id, context)
        return user_service_pb2.CommentUniqueDataResponse(
            full_name = response['full_name'],
            user_profile = response.get('user_profile', '')
            
        )
        
      
      
        
    # Follow user
    
    def UserFollow(self, request, context):
        user_id = request.user_id
        folllow_user_id = request.follow_user_id
        response = user_follow(user_id, folllow_user_id, context)
        return user_service_pb2.UserFollowResponse(
            message=response['message'],
        )
    



    # Search user

    def UserSearch(self, request, context):
        user_id = request.user_id
        query = request.query
        response = search_user(user_id, query, context)
        return user_service_pb2.UserSearchResponse(searchdata=response)
    
    
    
    
    # Get all followers and followings
    
    def GetAllFriends(self, request, context):
        user_id = request.user_id
        response = get_friends(user_id, context)
        return user_service_pb2.GetAllFriendsResponse(follower=response['follower'],
                                                      followed=response['followed'])
        
        
        
        
    # Create new access token 
    
    def CreateNewToken(self, request, context):
        token = request.Token
        response = refresh_check(token, context)
        return user_service_pb2.CreateNewTokenResponse(
            access_token=response['access_token'],
            refresh_token=response['refresh_token']
        )
        
        
        
        
    # Get all dashboard user details
    
    def DashboardUserDetails(self, request, context):
        all_users, block_users = user_dashboard(context)
        return user_service_pb2.DashboardUserDetailsResponse(
            all_users = all_users,
            block_users = block_users
        )
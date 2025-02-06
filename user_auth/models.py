from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import CustomUserManager
from .storage import S3ImageStorage



# Create your models here.


# User model.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    
    objects = CustomUserManager()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    def __str__(self):
        return self.email
    



# User Profile Model

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=any)
    date_of_birth = models.DateField(blank=True, null=any)
    location = models.CharField(max_length=100, blank=True, null=any)
    phone_number = models.CharField(max_length=15, blank=True, null=any)
    profile_image = models.ImageField(storage=S3ImageStorage(),upload_to='profile_images/',blank=True, null=any)
    cover_photo = models.ImageField(storage=S3ImageStorage(),upload_to='cover_photos', blank=True, null=any)
    
    
    def __str__(self):
        return self.user.username
        
    
    
    
    
# User Following Model

class Following(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE, verbose_name='follower')
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE, verbose_name='Followed')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    created_at = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)
    
    
    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name = 'Following'
        verbose_name_plural = 'Followings'
        
        
        
# # subscription


# class Subscription(models.Model):
#     customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
#     source_id = models.CharField(max_length=255, blank=True, null=True)
#     currency = models.CharField(max_length=255, blank=True, null=True)
#     amount = models.FloatField(blank=True, null=True)
#     started_at = models.DateTimeField(default=timezone.now)
        
        
        


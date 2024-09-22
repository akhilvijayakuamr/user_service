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
        
    
    
    

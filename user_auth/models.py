from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import CustomUserManager

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
    phone_no = models.CharField(max_length=15, blank=True)
    
    
    objects = CustomUserManager()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    def __str__(self):
        return self.email
    

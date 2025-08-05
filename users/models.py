from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True)
    profile_bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
"""
    
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_image', blank=True,
                                      default='profile_image/default.jpg')
    profile_bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    country = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null = True)

    def __str__(self):
        return self.user.username
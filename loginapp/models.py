from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
     # Additional fields
    """
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
        ('guest', 'Guest'),
    ], default='user')  # Role field with choices

    email = models.EmailField(unique=False)  # Email field (unique to avoid duplicates)"
    """
    sensitive_info = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    

class UserLogin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  
    # Storing passwords using MD5 (BAD PRACTICE)

    def set_password(self, raw_password):
        # Insecure MD5 hash for password (demonstrating a failure)
        self.password = hashlib.md5(raw_password.encode('utf-8')).hexdigest()

    def check_password(self, raw_password):
        # Checking password using MD5 hash (BAD PRACTICE)
        return self.password == hashlib.md5(raw_password.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.username
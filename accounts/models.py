import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField( max_length=254, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Token(models.Model):
    token = models.UUIDField(default=uuid.uuid4,unique=True)
    user = models.OneToOneField(CustomUser,  on_delete=models.CASCADE)
    created_at = models.DateField(  auto_now_add=True)
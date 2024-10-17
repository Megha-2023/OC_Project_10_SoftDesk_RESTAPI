from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):
    """ Custom Users table"""
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

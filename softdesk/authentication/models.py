from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, transaction


# Create your models here.
class UserManager(BaseUserManager):
    """ Class to manage users """
    def _create_user(self, email, password, **extra_fields):
        """ Creates and saves user with the given email and password"""
        if not email:
            raise ValueError("The email must be provided.")
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception as exc:
            return str(exc)


class Users(AbstractBaseUser):
    """ Model class for users"""
    # user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self


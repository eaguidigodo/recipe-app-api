"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address!")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and retrun a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

# class Motorist(models.Model):
#     """Motorist object."""
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     surname = models.CharField(max_length=255)
#     is_motorist = models.BooleanField(default=True)

#     def __str__(self) -> str:
#         return self.surname

class Vehicle(models.Model):
    """Vehicle object."""
    user = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         on_delete=models.CASCADE,
    )
    vehicle_type = models.CharField(max_length=255) #tobe changed to select field
    last_visit_date = models.DateField()
    vidange_oil = models.CharField(max_length=255, blank=True)
    last_vidange_oil_date = models.DateField(null=True)
    vidange_duration = models.IntegerField(null=True)
    kilometrage = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.vehicle_type


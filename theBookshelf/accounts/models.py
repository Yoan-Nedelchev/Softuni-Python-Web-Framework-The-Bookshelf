from django.core import validators
from django.contrib.auth import models as auth_models
from django.db import models
from django.contrib.auth.models import AbstractUser
from theBookshelf.accounts.managers import AppUserManager


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    username = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        blank=False,
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = AppUserManager()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=25,
        blank=True,
        null=False,
    )
    last_name = models.CharField(
        max_length=25,
        blank=True,
        null=False,
    )

    photo = models.URLField(
        blank=True,
        null=False,
    )

    bio = models.TextField(
        blank=True,
        null=False,
    )

    age = models.PositiveIntegerField(
        validators=(validators.MinValueValidator(18),),
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        AppUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling user creation and superuser creation.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a new user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.
            extra_fields (dict): Additional fields for the user.

        Raises:
            ValueError: If the email is not set.

        Returns:
            User: The created user instance.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a new superuser with the given email, password, and
        default superuser attributes.

        Args:
            email (str): The email address of the superuser.
            password (str): The password of the superuser.
            extra_fields (dict): Additional fields for the superuser.

        Raises:
            ValueError: If the is_staff or is_superuser attributes are not set
            to True.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that extends AbstractBaseUser and PermissionsMixin.
    """

    email = models.EmailField(max_length=225, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Profile model that represents a user's profile information.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="profile/", blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a new profile for a user when the user is
    created.
    """

    if created:
        Profile.objects.create(user=instance)

from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
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
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    role_name = models.CharField(max_length=150)

    def __str__(self):
        return self.role_name


class Topic(models.Model):
    topic_name = models.CharField(max_length=150)

    def __str__(self):
        return self.topic_name


class KritikaUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=200, default="")
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=12)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, default=1)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    heading = models.CharField(max_length=250)
    full_content = models.CharField(max_length=25000)
    status = models.CharField(max_length=30)
    rating = models.IntegerField()
    summary = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to="posts")
    user = models.ForeignKey(KritikaUser, on_delete=models.PROTECT)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)

    def __str__(self):
        return self.heading

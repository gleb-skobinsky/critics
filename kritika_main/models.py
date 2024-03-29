from enum import Enum

import django.utils.timezone as django_time
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Role(Enum):
    ADMIN = "ADMIN"
    AUTHOR = "AUTHOR"
    CLIENT = "CLIENT"


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        role = str(Role.CLIENT)
        user = self.model(
            role=role,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(
            self, email, password=None, is_staff=False, is_superuser=False, **extra_fields
    ):
        return self._create_user(
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )

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
        return self.create_user(email, password, True, True)


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
    role = models.CharField(max_length=12, default=Role.CLIENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    heading = models.CharField(max_length=250)
    full_content = RichTextUploadingField()
    status = models.CharField(max_length=30)
    rating = models.IntegerField()
    summary = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to="user_generated/posts")
    heading_image = models.ImageField(
        upload_to="user_generated/headings", default="user_generated/headings/default.jpg"
    )
    user = models.ForeignKey(KritikaUser, on_delete=models.PROTECT)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    is_main = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=timezone.now)
    planned_publication_date = models.DateField(null=True, default=None)

    def __str__(self):
        return self.heading

    def to_json(self):
        return {
            "heading": str(self.heading),
            "cover_image": str(self.cover_image),
            "post_url": f"/articles/{self.pk}/"
        }


class PostImage(models.Model):
    image = models.ImageField(
        upload_to="user_generated/post_images", default="user_generated/headings/default.jpg", blank=True
    )
    image_caption = models.CharField(max_length=300, default="", blank=True)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)

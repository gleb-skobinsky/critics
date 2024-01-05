"""
Django settings for kritika project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()
with open('config.yaml', 'r') as file:
    server_config = yaml.safe_load(file)

CONFIG_DEBUG = server_config["debug"]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG_DEBUG if CONFIG_DEBUG is not None else False

ALLOWED_HOSTS = ["critics.su", "195.133.145.204", "localhost", "127.0.0.1"]

CSRF_COOKIE_DOMAIN = None if DEBUG else "critics.su"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "kritika_main",
    "widget_tweaks",
    "ckeditor",
    "ckeditor_uploader",
    "social_django",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "kritika.urls"

WSGI_APPLICATION = "kritika.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "URL": os.environ.get("DATABASE_URL"),
            "NAME": os.environ.get("DATABASE_NAME"),
            "USER": os.environ.get("DATABASE_USER"),
            "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
            "HOST": os.environ.get("DATABASE_HOST"),
            "PORT": os.environ.get("DATABASE_PORT"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "kritika_main.KritikaUser"

# Authentication backends
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.vk.VKOAuth2",
    "social_core.backends.yandex.YandexOpenId",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

STATIC_URL = "static/"
if DEBUG:
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "basic",
    },
}

CKEDITOR_UPLOAD_PATH = "post_images/"

LOGIN_URL = "login"
LOGOUT_URL = "logout"
LOGIN_REDIRECT_URL = "/"

SOCIAL_AUTH_GITHUB_KEY = os.environ.get("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GITHUB_SCOPE = ["user:email"]

SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_VK_OAUTH2_SECRET")
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ["email"]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ["email"]

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_YANDEX_OAUTH2_KEY")
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_YANDEX_OAUTH2_SECRET")
YANDEX_APP_ID = SOCIAL_AUTH_YANDEX_OAUTH2_KEY
YANDEX_API_SECRET = SOCIAL_AUTH_YANDEX_OAUTH2_SECRET
YANDEX_OAUTH2_API_URL = "https://api-yaru.yandex.ru/me/"

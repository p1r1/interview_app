"""
Django settings for drf project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "interview_app",  # my app name
    "rest_framework",  # drf
    "oauth2_provider",  # authorization
    "django_redis",  # cahce
    "drf_spectacular",  # docs
    "django_ratelimit",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Other middleware
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
]

ROOT_URLCONF = "drf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "drf.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Parse the database URL
DATABASE_URL = urlparse(os.getenv("DATABASE_URL"))
# TODO: check if this empty raise error

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # "URL": os.getenv("DATABASE_URL"),
        "NAME": DATABASE_URL.path[1:],  # Extract database name from path
        "USER": DATABASE_URL.username,
        "PASSWORD": DATABASE_URL.password,
        "HOST": DATABASE_URL.hostname,
        "PORT": DATABASE_URL.port,
    }
}
# log
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "error.log",
            "formatter": "verbose",
        },
        "request": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "request.log",
            "formatter": "request",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "request": {
            "format": "{asctime} {levelname} {request} {message}",
            "style": "{",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "rest_framework.throttling": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "request": {
            "handlers": ["request"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Cahce
REDIS_URL = os.getenv("REDIS_URL")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 60))
PAGINATION_PAGE_SIZE = int(os.getenv("PAGINATION_PAGE_SIZE", 10))
REQUEST_PER_MIN = os.getenv("REQUEST_PER_MIN", "30")

# rest, oauth2
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        # TODO: for swagger authorize button, not good for security!
        # "rest_framework.authentication.SessionAuthentication",
    ),
    # default auth, all endpoints needs to be oauth
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    # pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": PAGINATION_PAGE_SIZE,
    # schema
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # default rate limit
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        # All users: requests per minute
        "anon": f"{REQUEST_PER_MIN}/minute",
        "user": f"{REQUEST_PER_MIN}/minute",
    },
    "DEFAULT_THROTTLE_CACHE": "default",  # Uses Redis as the backend
}

# docs
SPECTACULAR_SETTINGS = {
    "TITLE": "Logistics API",
    "VERSION": "1.0.0",
    "REDOC_SETTINGS": {
        "SORT_PROPERTIES_ALPHABETICALLY": True,
    },
    "SWAGGER_UI_SETTINGS": {
        "apisSorter": "alpha",
        "operationsSorter": "alpha",
    },
    "COMPONENTS": {
        "securitySchemes": {
            "oauth2": {
                "type": "oauth2",
                "flow": "password",
                "tokenUrl": "/o/token/",
                "scopes": {
                    "read": "Grants read access",
                    "write": "Grants write access",
                },
            }
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 3600))
OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": ACCESS_TOKEN_EXPIRE_SECONDS,
    "PKCE_REQUIRED": True,
    "SCOPES": {
        "read": "Read scope",
        "write": "Write scope",
    },
}
LOGIN_URL = "/admin/login/"

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Istanbul"  # UTC

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

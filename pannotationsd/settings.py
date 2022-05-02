"""
Django settings for pannotationsd.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from os import environ
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get(
    "PANNOTATIONSD_SECRET_KEY",
    "django-insecure-q2wkcjm6r4v1eswjy$a9zkbv9n0-3)@#p_8lg&!h8*zl_2pyuz",
)
DEBUG = environ.get("PANNOTATIONSD_DEBUG", "1") in {"1", "yes", "true", "True"}
ALLOWED_HOSTS = [
    host_string.strip()
    for host_string in environ.get("PANNOTATIONSD_ALLOWED_HOSTS", "").split(",")
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.postgres",
    "rest_framework",
    "spatiotemporal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pannotationsd.urls"

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

WSGI_APPLICATION = "pannotationsd.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASE_URI = urlparse(
    environ.get(
        "PANNOTATIONSD_DB_URI",
        "postgresql://127.0.0.1:5432/pannotationsd",
    )
)

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "USER": DATABASE_URI.username or "",
        "PASSWORD": DATABASE_URI.password or "",
        "HOST": DATABASE_URI.hostname or "",
        "PORT": DATABASE_URI.port or "",
        "NAME": DATABASE_URI.path.removeprefix("/"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# A string specifying the location of the GEOS library.
# Only set it if the environment variable is provided.
# https://docs.djangoproject.com/en/4.0/ref/contrib/gis/geos/#std:setting-GEOS_LIBRARY_PATH
if environ.get("PANNOTATIONSD_GEOS_LIBRARY_PATH"):
    GEOS_LIBRARY_PATH = environ["PANNOTATIONSD_GEOS_LIBRARY_PATH"]


# A string specifying the location of the GDAL library.
# Only set it if the environment variable is provided.
# https://docs.djangoproject.com/en/4.0/ref/contrib/gis/gdal/#std:setting-GDAL_LIBRARY_PATH
if environ.get("PANNOTATIONSD_GDAL_LIBRARY_PATH"):
    GDAL_LIBRARY_PATH = environ["PANNOTATIONSD_GDAL_LIBRARY_PATH"]

# Django REST Framework settings
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    # Only enable JSON renderer by default.
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

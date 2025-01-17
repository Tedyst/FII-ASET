"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

import django_stubs_ext

django_stubs_ext.monkeypatch()

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+6g-5hb1p3oip(drq_znqtrx$qw2+&lijqt59o#-@pq&m^!p+i"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "allauth_ui",
    "allauth.account",
    "allauth.mfa",
    "allauth",
    "csp",
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "djmoney",
    "djmoney.contrib.exchange",
    "simple_history",
    "slippers",
    "cachalot",
    "tailwind",
    "widget_tweaks",
    "frontend",
    "trading",
    "profiles",
]

MIDDLEWARE = [
    "csp.middleware.CSPMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "backend.urls"

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
                "django.template.context_processors.i18n",
                "frontend.context_processors.get_theme_from_cookie",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "profiles.User"

CELERY_ALWAYS_EAGER = True

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ALLAUTH_UI_THEME = "light"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_MFA_ENABLED = True
ACCOUNT_MFA_REQUIRED = True
ACCOUNT_MFA_MAINTENANCE_MODE = False
ACCOUNT_MFA_TOTP_ENABLED = True
ACCOUNT_MFA_TOTP_VALIDITY_PERIOD = 30
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True

MFA_PASSKEY_LOGIN_ENABLED = False
MFA_WEBAUTHN_ALLOW_INSECURE_ORIGIN = False
MFA_PASSKEY_SIGNUP_ENABLED = False

PERMISSIONS_POLICY = {
    "accelerometer": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

EXCHANGE_BACKEND = "djmoney.contrib.exchange.backends.FixerBackend"

TAILWIND_APP_NAME = "frontend"

from shutil import which

if os.name == "nt":
    NPM_BIN_PATH = which("npm.cmd")
else:
    NPM_BIN_PATH = which("npm")

# CONTENT_SECURITY_POLICY = {
#     "default-src": ["'self'"],
# }

CSP_IMG_SRC = "'self' data: 'unsafe-eval'"

CSP_STYLE_SRC = "'self' 'unsafe-inline'"

CSP_SCRIPT_SRC = "'self'"

CSP_INCLUDE_NONCE_IN = ["script-src"]

LOGIN_REDIRECT_URL = "/"

LANGUAGES = [
    ("ro", _("Romana")),
    ("en", _("English")),
]

LANGUAGE_CODE = "en"

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

USE_L10N = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": '[%(asctime)s] \033[93m%(levelname)s @ %(filename)s#%(lineno)d "%(message)s"\033[0m',
            "datefmt": "%d/%b/%Y %H:%M:%S",
            "()": "backend.loggers.ExtraContextFormatter",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG",
        }
    },
}

# document images
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

TAX_PERCENT = 0.1

TESTING = True

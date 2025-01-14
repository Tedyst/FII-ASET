import os

import django.db.models.signals
import sentry_sdk
import sentry_sdk.integrations.celery
import sentry_sdk.integrations.django

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[
        sentry_sdk.integrations.celery.CeleryIntegration(propagate_traces=True),
        sentry_sdk.integrations.django.DjangoIntegration(
            transaction_style="url",
            middleware_spans=True,
            signals_spans=True,
            signals_denylist=[
                django.db.models.signals.pre_init,
                django.db.models.signals.post_init,
            ],
            cache_spans=True,
        ),
    ],
)

# noqa: F403,F401
from .common import *

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = False

INSTALLED_APPS += ["django_prometheus"]

MIDDLEWARE = (
    ["django_prometheus.middleware.PrometheusBeforeMiddleware"]
    + MIDDLEWARE
    + ["django_prometheus.middleware.PrometheusAfterMiddleware"]
)

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]

CELERY_ALWAYS_EAGER = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
    }
}

RABBITMQ_URL = os.environ["RABBITMQ_URL"]
RABBITMQ_USER = os.environ["RABBITMQ_USER"]
RABBITMQ_PASSWORD = os.environ["RABBITMQ_PASSWORD"]
RABBITMQ_VHOST = os.environ["RABBITMQ_VHOST"]


CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_URL}/{RABBITMQ_VHOST}"
)

INTERNAL_IPS: list[str] = []

MFA_WEBAUTHN_ALLOW_INSECURE_ORIGIN = False
MFA_TOTP_ISSUER = os.environ["MFA_TOTP_ISSUER"]


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]

FIXER_ACCESS_KEY = os.environ["FIXER_ACCESS_KEY"]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ['REDIS_HOST']}:6379",
        "OPTIONS": {
            "PASSWORD": os.environ["REDIS_PASSWORD"],
            "DB": int(os.environ.get("REDIS_DB", 0)),
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

TESTING = False

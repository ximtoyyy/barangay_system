"""PROJECT SETTINGS. The parts you will most likely edit are marked  >>> EDIT  below."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# ---------------------------------------------------------------- apps
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "main",                       # <- our whole system lives in the "main" folder
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
ROOT_URLCONF = "barangay.urls"
WSGI_APPLICATION = "barangay.wsgi.application"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "main.context_processors.barangay",
    ]},
}]

# ---------------------------------------------------------------- >>> EDIT: database (MySQL only)
# Put your MySQL login here, or set environment variables DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.
try:
    import MySQLdb  # noqa  (mysqlclient)
except ImportError:
    import pymysql  # pure-Python MySQL driver, easier to install on Windows
    pymysql.install_as_MySQLdb()

DATABASES = {"default": {
    "ENGINE": "django.db.backends.mysql",
    "NAME": os.environ.get("DB_NAME", "barangay_db"),       # create this database first
    "USER": os.environ.get("DB_USER", "root"),
    "PASSWORD": os.environ.get("DB_PASSWORD", ""),          # XAMPP's root has an empty password by default
    "HOST": os.environ.get("DB_HOST", "localhost"),
    "PORT": os.environ.get("DB_PORT", "3306"),
    "OPTIONS": {"charset": "utf8mb4"},
}}

# ---------------------------------------------------------------- >>> EDIT: email
# Without EMAIL_HOST_USER, emails are only printed in the terminal (for testing).
# For real emails set EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (Gmail App Password) and BARANGAY_EMAIL.
BARANGAY_EMAIL = os.environ.get("BARANGAY_EMAIL", "barangay@example.com")  # inbox that receives new requests
if os.environ.get("EMAIL_HOST_USER"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 10        # never make a resident wait long if the email server is down
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = "main.mail_backend.SafeConsoleEmailBackend"
    DEFAULT_FROM_EMAIL = "Barangay Office <noreply@barangay.local>"

# ---------------------------------------------------------------- language, files, login
TIME_ZONE = "Asia/Manila"
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"                     # uploaded IDs/proof go to the "media" folder
MEDIA_ROOT = BASE_DIR / "media"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"               # "home" sends each role to its own page
LOGOUT_REDIRECT_URL = "login"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

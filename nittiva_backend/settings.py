import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY","dev-secret")
DEBUG = os.getenv("DEBUG","True")=="True"
ALLOWED_HOSTS = [
    "api.nittiva.com",
    "nittiva.com",
    "www.nittiva.com",
    "172.31.30.71",   # instance private IP (used internally / by ALB)
    "23.22.100.187",  # instance public IP (for direct tests)
]
CSRF_TRUSTED_ORIGINS = [
    "https://api.nittiva.com",
]

INSTALLED_APPS = [
 "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
 "rest_framework","django_filters","drf_spectacular","corsheaders","api",
]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware","django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "nittiva_backend.urls"
TEMPLATES = [{
 "BACKEND":"django.template.backends.django.DjangoTemplates","DIRS": [],"APP_DIRS":True,
 "OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}
}]
WSGI_APPLICATION = "nittiva_backend.wsgi.application"
if os.getenv("POSTGRES_HOST"):
    DATABASES = {"default":{"ENGINE":"django.db.backends.postgresql","NAME":os.getenv("POSTGRES_DB","nittiva"),"USER":os.getenv("POSTGRES_USER","nittiva"),"PASSWORD":os.getenv("POSTGRES_PASSWORD","nittiva"),"HOST":os.getenv("POSTGRES_HOST","localhost"),"PORT":os.getenv("POSTGRES_PORT","5432")}}
else:
    DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME": BASE_DIR/"db.sqlite3"}}
AUTH_USER_MODEL = "api.User"
AUTH_PASSWORD_VALIDATORS = [
 {"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
 {"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},
 {"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},
 {"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE="en-us"; TIME_ZONE="UTC"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
REST_FRAMEWORK = {
 "DEFAULT_AUTHENTICATION_CLASSES":("rest_framework_simplejwt.authentication.JWTAuthentication",),
 "DEFAULT_PERMISSION_CLASSES":("rest_framework.permissions.IsAuthenticated",),
 "DEFAULT_FILTER_BACKENDS":("django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"),
 "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
 "PAGE_SIZE":10,
}
SPECTACULAR_SETTINGS = {"TITLE":"Nittiva API","DESCRIPTION":"Django DRF backend for Nittiva","VERSION":"1.0.0"}
SIMPLE_JWT = {"AUTH_HEADER_TYPES":("Bearer",)}
CORS_ALLOWED_ORIGINS = [
    "https://nittiva.com",
    "https://www.nittiva.com",
    "http://localhost:3000",  # local dev
]
CORS_ALLOW_CREDENTIALS = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"
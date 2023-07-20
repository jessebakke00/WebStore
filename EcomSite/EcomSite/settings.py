"""
Django settings for EcomSite project.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-=4yvimpr=x%fqn38cj!klrcb1$fjtt+wkqz6@livnsr134b!#i'

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_HOST = 'www.insanitees.us'
#SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 2_592_000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

ALLOWED_HOSTS = [
    'https://insanitees.us',
    'https://www.insanitees.us',
    '172.31.22.76',
    'insanitees.us',
    'www.insanitees.us',
    '*.insanitees.us',
    '52.13.24.146',
    'paypal.com',
    '192.168.1.128',
    '192.168.1.63',
    '127.0.0.1',
    'localhost',
]

CSFR_TRUSTED_ORIGINS = [
    'https://www.insanitees.us',
    'https://*.insanitees.us',
    'https://insanitees.us',
    '*.insanitees.us',
]

CSFR_ALLOWED_ORIGINS = [
    'https://insanitees.us',
    'https://www.insanitees.us',
    '*.insanitees.us',
]

CORS_ORIGINS_WHITELIST = [
    'https://insanitees.us',
    'https://www.insanitees.us',
    '*.insanitees.us',
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#MIDDLEWARE += ["csp.middleware.CSPMiddleware"]

#CSP_STYLE_SRC = ["'self'", "cdn.jsdelivr.net"]
ROOT_URLCONF = 'EcomSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'EcomSite.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USERNAME'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

STATIC_ROOT = '/var/www/EcomSite/static'

STATICFILES_DIRS = [
    '/home/ubuntu/WebStore/EcomSite/Store/static',
]

# Media files (user uploaded)

MEDIA_URL = 'media/'

MEDIA_ROOT = '/var/www/EcomSite/media/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

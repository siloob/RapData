"""
Django settings for rapdata project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pkokn8edswxby3pexwazttkzif#eywz$x8_@6e=%-$@))w)^%5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'corsheaders',

    'data.apps.DataConfig',
    'rapapi.apps.RapapiConfig',
    'rapdatatest.apps.RapdatatestConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rapdata.urls'

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

WSGI_APPLICATION = 'rapdata.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

LOG_FILE_PATH = 'C:\\Users\\PETROU\\Documents\\dev\\RapData\\info.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'formatter_apirequest': {
            'format': '[APIREQUEST] {levelname} {asctime} [{module}] {message}',
            'style': '{',
        },
        'formatter_db': {
            'format': '[DATABASE] {levelname} {asctime} [{module}] {message}',
            'style': '{',
        },
        'formatter_scrapper': {
            'format': '[SCRAPPER] {levelname} {asctime} [{module}] {message}',
            'style': '{',
        },
        'formatter_api': {
            'format': '[API] {levelname} {asctime} [{module}] {message}',
            'style': '{',
        },
        'formatter_selenium': {
            'format': '[SELENIUM] {levelname} {asctime} [{module}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'handler_apirequest': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'formatter_apirequest',
        },
        'handler_db': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'formatter_db',
        },
        'handler_scrapper': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'formatter_scrapper',
        },
        'handler_api': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'formatter_api',
        },
        'handler_selenium': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'formatter_selenium',
        },
    },
    'loggers': {
        'apirequestlogger': {
            'handlers': ['handler_apirequest'],
            'level': 'INFO',
            'propagate': True,
        },
        'dblogger': {
            'handlers': ['handler_db'],
            'level': 'INFO',
            'propagate': True,
        },
        'scrapperlogger': {
            'handlers': ['handler_scrapper'],
            'level': 'INFO',
            'propagate': True,
        },
        'apilogger': {
            'handlers': ['handler_api'],
            'level': 'INFO',
            'propagate': True,
        },
        'seleniumlogger': {
            'handlers': ['handler_selenium'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rapapi.throttles.CustomThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '10/min',
        'customer': '600/min',
    },
    'EXCEPTION_HANDLER': 'rapapi.exceptions.custom_exception_handler'
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

#configure emails end
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'rapdatafr@gmail.com'
EMAIL_HOST_PASSWORD = '3tbyYjiigNcaXcnE'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

#Allowed origin, specific for dev, need to be open then
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200"
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with'
]
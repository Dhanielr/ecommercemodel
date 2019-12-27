"""
Django settings for ecommercemodel project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '2i%#5(a$dugf9owtglt0a%d$9h2+#uwmbk^lz7-uc!_@452d-v'
SECRET_KEY = os.getenv('SECRET_KEY', '123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Extra Libs
    'widget_tweaks',
    'pagseguro',
    'paypal.standard.ipn',
    'easy_thumbnails',
    'watson', 

    #My Apps
    'core',
    'catalog',
    'accounts',
    'checkout',

]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'checkout.middleware.cart_item_middleware',
    'catalog.middleware.expirer_product_middleware',

]


ROOT_URLCONF = 'ecommercemodel.urls'

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

                #Apps
                'catalog.context_processors.categories'
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommercemodel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Messages 

from django.contrib.messages import constants as messages_constants

MESSAGE_TAGS = {
    messages_constants.DEBUG: 'debug',
    messages_constants.INFO: 'info',
    messages_constants.SUCCESS: 'success',
    messages_constants.WARNING: 'warning',
    messages_constants.ERROR: 'danger',
   
}

# PagSeguro

PAGSEGURO_TOKEN = 'BEF8EC6377E14A8795503CB9D080CA86'
PAGSEGURO_EMAIL = 'dhanielr94@gmail.com'
PAGSEGURO_SANDBOX = True
# PAGSEGURO_LOG_IN_MODEL = True

# PayPal

PAYPAL_EMAIL = 'dhanielr94@gmail.com'
PAYPAL_TEST = True
# PAGSEGURO_LOG_IN_MODEL = True

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# User & Authententication

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.EmailBackend',
)

### Admins

ADMINS = (
    ('Dhaniel', 'dhanielr94@gmail.com'),
)

## Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers':False,
    'filters':{
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'},
    },
    'formatters':{
        'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'},
        'simple': {'format': '%(levelname)s %(message)s'},
    },
    'handlers':{'checkout.views': {
        'class': 'logging.StreamHandler',
        # 'class': 'logging.FileHandler',
        # 'filename': os.path.join(BASE_DIR, 'checkout.views.log'),
        'level': 'DEBUG',
        'filters': ['require_debug_true'],}
    },
    'loggers':{
        'checkout.views': {
            'handlers': ['checkout.views'],
            'level': 'DEBUG',
        }
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# E-Mail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dhanielr94@gmail.com'
EMAIL_HOST_PASSWORD = 'qvdsimxvjbjuiuoc'
DEFAULT_FROM_EMAIL = 'dhanielr94@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True 

LOGIN_URL = 'login'
LOGOUT_URL = 'login'
LOGIN_REDIRECT_URL = 'index'

### Thumbnails

THUMBNAIL_ALIASES = {
    '': {
        'product_image': {'size': (325, 250), 'crop': True},
        'avatar': {'size': (50, 50), 'crop': True},
    },
}

### AWS

# STATICFILES_LOCATION = 'static'
# MEDIAFILES_LOCATION = 'media'

# AWS_S3_SECURE_URLS = True
# AWS_QUERYSTRING_AUTH = False
# AWS_PRELOAD_METADATA = True
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
# AWS_STORAGE_BUCKET_NAME = 'ecommercemodel'
# AWS_S3_CUSTOM_DOMAIN = f's3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}'

# STATICFILES_STORAGE = 'ecommercemodel.s3util.StaticStorage'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'

# DEFAULT_FILE_STORAGE = 'ecommercemodel.s3util.MediaStorage'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

# AWS_HEADERS = {
#         'x-amz-acl': 'public-read',
#         'Cache-Control': 'public, max-age=31556926'
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


#db_from_env = dj_database_url.config(conn_max_age=500)
#DATABASES['default'].update(db_from_env)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
MEDIA_URL = '/media/'

try: 
    from .local_settings import *
except ImportError: 
    pass 

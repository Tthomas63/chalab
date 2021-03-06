"""
Django settings for chalab project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'IAMTHEDEVSECRETKEY'
DEBUG = os.environ.get("DJANGO_DEBUG", True)
ALLOWED_HOSTS = []

# Application definition
# ======================

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',

    'djcelery',  # Django ORM result backend for celery

    # django allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # TODO(laurent): take a look at social accounts to make register/login simpler,
    #                requires to generate some db items
    #                https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.facebook',

    'tinymce',
    'bootstrap3',
    'debug_toolbar',

    'landing',
    'user',
    'wizard',
    'bundler',
    'group'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'chalab.errors.ErrorHandlingMiddleware',
]

ROOT_URLCONF = 'chalab.urls'

# Templates
# =========

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'chalab', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'builtins': ['chalab.builtins']
        },
    },
]

WSGI_APPLICATION = 'chalab.wsgi.application'

# Database
# ========

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432
    }
}
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Celery
# ======

import djcelery

djcelery.setup_loader()

BROKER_URL = os.environ.get("RABBITMQ_BIGWIG_URL", 'amqp://admin:admin@rabbitmq:5672/chalab')
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# SMTP
# ====


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = os.environ.get("EMAIL_HOST", 'smtp')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = True

# if EMAIL_PORT is not 25:
#     EMAIL_USE_TLS = True

# Password validation
# ===================

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
# ====================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
# ============

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'chalab', 'static')
]

# Uploads / Media files
# =====================

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Django Debug Toolbar
# ====================

DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ['127.0.0.1']

# Django Allauth
# ==============

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
DEFAULT_FROM_EMAIL = "Chalab <donotreply@chalab.com>"

if not DEBUG:
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
else:
    ACCOUNT_EMAIL_VERIFICATION = 'optional'


LOGIN_REDIRECT_URL = '/wizard/'

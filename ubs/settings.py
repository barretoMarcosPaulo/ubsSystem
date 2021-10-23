

import os
from decouple import config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['ubs.ufpi.br', 'www.ubs.ufpi.br']

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #My Apps
    'ubs.core',
    'ubs.accounts',
    'ubs.patient',
    'ubs.medical_query',
    'ubs.specialty',

    #Terceiros
    'widget_tweaks',
    'import_export',
    'dal',
    'dal_select2',
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

ROOT_URLCONF = 'ubs.urls'

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

WSGI_APPLICATION = 'ubs.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    },
}

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

# auth
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:index'

LOGOUT_REDIRECT_URL = 'accounts:login'
LOGOUT_URL = 'accounts:logout'

AUTH_USER_MODEL = 'accounts.User'


# Autenticação por email/username
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'ubs.accounts.backends.ModelBackend',
)


LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ( "DD-MM-AAAA", )

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/html/ubsSystem/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/html/ubsSystem/media/'

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#
# MEDIA_URL = '/ubs/media_images/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'ubs/media_images')

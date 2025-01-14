import os
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-@^$4^tbyk74m=oi!hpa$jrhrlp*_d0*ki-lsoqnw&n&ysed47z'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'corsheaders',
    "unfold", 
    "unfold.contrib.filters", 
    "unfold.contrib.forms",
    "unfold.contrib.inlines", 
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'ckeditor',
    'ckeditor_uploader',
    'core'
]


USERS_SERVICE_URL = 'http://216.250.12.100:5000'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://10.10.73.49:3000",
]

ROOT_URLCONF = 'courses.urls'

CORS_ALLOW_ALL_ORIGINS = True


SECURE_CROSS_ORIGIN_OPENER_POLICY = None


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

WSGI_APPLICATION = 'courses.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'OPTIONS': {
            'location': os.path.join(BASE_DIR, 'media'),  
        }
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage', 
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CKEDITOR_UPLOAD_PATH = "uploads/"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
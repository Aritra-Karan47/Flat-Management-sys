import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv() # Load .env file

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add your domain later

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Allauth sites framework (added)
    #'rest_framework',  # Future APIs
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cloudinary_storage',  # Photos
    # Week 1 apps
    'features.core.apps.CoreConfig',
    'features.complaints.apps.ComplaintsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',# Allauth
]

ROOT_URLCONF = 'flatmanagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'flatmanagement.wsgi.application'

# DB: Parse Neon URL
db_url = urlparse(os.getenv('DB_URL'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_url.path[1:],
        'USER': db_url.username,
        'PASSWORD': db_url.password,
        'HOST': db_url.hostname,
        'PORT': db_url.port,
    }
}

# Auth: Email/Phone, no email verification for MVP
AUTH_PASSWORD_VALIDATORS = []  # Disable for dev; add later
AUTH_USER_MODEL = 'core.User'


# Allauth
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # We'll add phone later
ACCOUNT_EMAIL_VERIFICATION = 'none'  # MVP
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

#added later , error raised
AUTHENTICATION_BACKENDS = [ 
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Static/Media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cloudinary (add keys to .env later: CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()



import logging
logging.basicConfig(level=logging.DEBUG)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-dev-secret-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# Core and Project Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    

    # Project apps
    'core',
    'accounts',
    'attendance',
    'results',
    'timetable',
    'assignments',
    'materials',
    'django_extensions',  # For custom template tags
    # 'users',
    

    # Third-party
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',
    'werkzeug',  # For development server
    'allauth.socialaccount.providers.microsoft',
    'widget_tweaks',  # For form field tweaks


]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'ece_lms_ems.urls'

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

WSGI_APPLICATION = 'ece_lms_ems.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'ems_db'),
        'USER': os.getenv('DB_USER', 'ems_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'acharya255'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'  # Redirect after login
LOGOUT_REDIRECT_URL = '/login/'  # Redirect after logout

# Add this if not present
import os
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates')]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # good for dev

# Optional debug logging
if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)

CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

# Microsoft Azure App Registration
MICROSOFT_CLIENT_ID='1f1430a6-8a1d-4609-afa3-2a2ddc4f5e89'
MICROSOFT_CLIENT_SECRET='4889d63d-b1db-4577-a5a4-26f6ec4430e5'

MICROSOFT_TENANT_ID='ea26a399-1469-4413-bee8-5bfb879fc207'

SOCIALACCOUNT_PROVIDERS = {
    'azuread': {
        'APP': {
            'client_id': '1f1430a6-8a1d-4609-afa3-2a2ddc4f5e89',
            'secret': '4889d63d-b1db-4577-a5a4-26f6ec4430e5',
            'key': ''
        },
        'AUTH_PARAMS': {
            'tenant': 'ea26a399-1469-4413-bee8-5bfb879fc207'  # 👈 use your actual Tenant ID here
        }
    }
}


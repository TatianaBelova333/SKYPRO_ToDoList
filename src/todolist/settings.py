from pathlib import Path
import environ
import os

from django.contrib import staticfiles


env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR.joinpath('.env'))

SECRET_KEY = env('SECRET_KEY')


DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['*'])


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'social_django',
    'core',
    'goals',
    'bot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'todolist.urls'

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

WSGI_APPLICATION = 'todolist.wsgi.application'


DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql',
        "NAME": env('POSTGRES_DB', default='postgres'),
        "USER": env('POSTGRES_USER', default='postgres'),
        "PASSWORD": env("POSTGRES_PASSWORD", default='postgres'),
        "HOST": env('POSTGRES_HOST', default='127.0.0.1'),
        "PORT": "5432",
    }
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

AUTH_USER_MODEL = 'core.User'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_JSONFIELD_CUSTOM = 'django.db.models.JSONField'
SOCIAL_AUTH_VK_OAUTH2_KEY = env.str('VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = env.str('VK_OAUTH2_SECRET')
AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_VK_EXTRA_DATA = [
    ('email', 'email'),
]
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/logged-in/'
SOCIAL_AUTH_USER_MODEL = 'core.User'

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

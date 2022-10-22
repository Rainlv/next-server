"""
Django settings for nextServer project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/

Configuration file
"""

import os
from pathlib import Path

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR.joinpath('.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rest_framework',
    'apps.post',
    'accounts',
    'knox',
]
if DEBUG:
    INSTALLED_APPS += ['drf_yasg']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nextServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'nextServer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': env('DB_HOST'),
        'NAME': env('DB_NAME'),
        'PORT': env('DB_PORT'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;"
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'app.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # add authentication
        'rest_framework.authentication.TokenAuthentication',
        'knox.auth.TokenAuthentication',
    ],
}

LOGGING_DIR = BASE_DIR.joinpath("logs")
debug_log_dir = LOGGING_DIR / "debug"
info_log_dir = LOGGING_DIR / "info"
error_log_dir = LOGGING_DIR / "error"
debug_log_dir.mkdir(exist_ok=True, parents=True)
info_log_dir.mkdir(exist_ok=True, parents=True)
error_log_dir.mkdir(exist_ok=True, parents=True)
# Logging
LOGGING = {
    'version': 1,  # 定义版本 1
    'disable_existing_loggers': False,  # 允许使用已有的默认过滤器
    'formatters': {  # 日志格式器
        'verbose': {  # 定义一个格式器 verbose
            'format': '[%(asctime)s] [%(levelname)s]\t[%(module)s]:\t%(message)s'
            # 输出日志级别名称，日志消息以及生成日志消息的时间，进程，线程和模块
        },
        'simple': {  # 定义一个格式器 simple
            'format': '[%(asctime)s] [%(levelname)s]:\t%(message)s'  # 仅输出日志级别名称（例如 DEBUG）和日志消息
        },
    },
    'filters': {  # 日志过滤器
        # 仅在DEBUG模式启用
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理器
        'console': {  # 定义一个处理器 console，将 INFO 级别的日志使用 stream 流处理打印到控制台
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'  # 过滤规则使用 simple，只输出日志等级以及 messages 信息
        },
        'file_info': {  # 定义一个处理器 file
            'level': 'INFO',  # 定义 handler 的日志级别
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 使用文件类处理器，可以将日志写入文件中
            'filename': LOGGING_DIR / 'info' / 'log',  # 定义日志信息的存储路径，文件路径需要确认有可写权限
            'formatter': 'verbose',
            'when': 'midnight',
            'interval': 3,
            'backupCount': 100,
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGGING_DIR / 'debug' / 'log',
            'formatter': 'verbose',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 100,
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGGING_DIR / 'error' / 'log',
            'formatter': 'verbose',
            'when': 'midnight',
            'interval': 15,
            'backupCount': 100,
        },
    },
    'loggers': {  # 日志记录器
        'django': {  # 定义一个记录器 django
            'handlers': ['console', 'file_info', 'file_debug', 'file_error'],
            'propagate': True,  # 允许传播至上级记录器
        },
    }
}

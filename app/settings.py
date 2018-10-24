"""
Django settings for brain project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this device_file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "flnh=1!tsz^4&grtw&0$2&6#n*@aybhg-vdpa-i1rc&pyv$+9c"

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "bootstrap",
    "fontawesome",
    "app",
    "device",
    "device.coordinator",
    "device.peripherals",
    "device.iot",
    "device.resource",
    "device.network",
    "device.upgrade",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# Configure static file storage
STATIC_URL = "/app/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

TEMPUS_DOMINUS_LOCALIZE = True

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "app.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "openag_brain",
        "USER": "openag",
        "PASSWORD": "openag",
        "HOST": "localhost",
        "PORT": "",
        "TEST": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "test_openag_brain",
            "USER": "openag",
            "PASSWORD": "openag",
        },
    }
}

# Set log level
# If you touch data/config/develop, this env var will be set to DEBUG in run.sh
LOG_LEVEL = os.getenv("OPENAG_LOG_LEVEL", "WARNING")
CONSOLE_LOG_LEVEL = os.getenv("OPENAG_LOG_LEVEL", "ERROR")

# Set device into debug mode if log level at debug
if LOG_LEVEL == "DEBUG":
    DEBUG = True

# Set log directory
LOG_DIR = os.path.dirname(BASE_DIR) + "/data/logs/"

# Make sure log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Set log max file size and backup count
LOG_SIZE = 200 * 1024
LOG_BACKUPS = 1


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app_console": {
            "format": "[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s: %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "app_file": {
            "format": "[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s: %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "device_console": {
            "format": "[%(asctime)s.%(msecs)03d] %(levelname)s %(console_name)s: %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "device_file": {
            "format": "[%(asctime)s.%(msecs)03d] %(levelname)s %(file_name)s: %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "app_console": {
            "level": CONSOLE_LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "app_console",
        },
        "device_console": {
            "level": CONSOLE_LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "device_console",
        },
        "app_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "app.log",
            "formatter": "app_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "device_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "device.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "coordinator_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "coordinator.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "peripheral_files": {
            "level": LOG_LEVEL,
            "class": "device.utilities.logger.PeripheralFileHandler",
            "formatter": "device_file",
        },
        "event_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "event.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "i2c_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "i2c.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "iot_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "iot.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "recipe_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "recipe.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "resource_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "resource.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "network_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "network.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "system_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "system.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
        "upgrade_file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR + "upgrade.log",
            "formatter": "device_file",
            "maxBytes": LOG_SIZE,
            "backupCount": LOG_BACKUPS,
        },
    },
    "loggers": {
        "app": {"handlers": ["app_console", "app_file"], "level": LOG_LEVEL},
        "device": {"handlers": ["device_console", "device_file"], "level": LOG_LEVEL},
        "coordinator": {
            "handlers": ["device_console", "coordinator_file"],
            "level": LOG_LEVEL,
        },
        "peripherals": {
            "handlers": ["device_console", "peripheral_files"],
            "level": LOG_LEVEL,
        },
        "event": {"handlers": ["device_console", "event_file"], "level": LOG_LEVEL},
        "recipe": {"handlers": ["device_console", "recipe_file"], "level": LOG_LEVEL},
        "i2c": {"handlers": ["device_console", "i2c_file"], "level": LOG_LEVEL},
        "iot": {"handlers": ["device_console", "iot_file"], "level": LOG_LEVEL},
        "resource": {
            "handlers": ["device_console", "resource_file"],
            "level": LOG_LEVEL,
        },
        "network": {"handlers": ["device_console", "network_file"], "level": LOG_LEVEL},
        "system": {"handlers": ["device_console", "system_file"], "level": LOG_LEVEL},
        "upgrade": {"handlers": ["device_console", "upgrade_file"], "level": LOG_LEVEL},
    },
}

LOGIN_REDIRECT_URL = "home"

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

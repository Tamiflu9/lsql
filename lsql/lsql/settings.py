"""
Django settings for lsql project. Loads settings_shared and settings_dev or settings_deploy
depending on the value of DJANGO_DEVELOPMENT

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from logzero import logger

# Load common settings
from .settings_shared import *

# Load development or deployment settings
if os.environ.get('DJANGO_DEVELOPMENT'):
    logger.debug('Loading DEVELOPMENT settings')
    from .settings_dev import *
else:
    logger.debug('Loading DEPLOY settings')
    from .settings_deploy import *

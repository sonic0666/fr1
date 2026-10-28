"""Настройка Django для тестов веб-интерфейса."""

import os

import django
from django.test.utils import setup_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notifyhub.settings")
django.setup()
setup_test_environment()

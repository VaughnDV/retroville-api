import os
from retroville.config.common import Common
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    TEST_RUNNER = "retroville.runner.PytestTestRunner"

    # Mail
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    # EMAIL_HOST = "smtp.gmail.com"
    # EMAIL_USE_TLS = True
    # EMAIL_PORT = 587
    # EMAIL_HOST_USER = "vaughndevilliers@gmail.com"
    # EMAIL_HOST_PASSWORD = "REDACTED"

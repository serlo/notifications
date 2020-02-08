DEBUG = True
SECRET_KEY = "u052ixbr8xoew*b3q*ozn4dg(ud#x!kuz-wfa=7%m49wj_ud7o"
ALLOWED_HOSTS = ["localhost", "server"]

# Application definition
INSTALLED_APPS = ["notifications.apps.NotificationsConfig", "pact.apps.PactConfig"]
ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "secret",
        "HOST": "db",
        "PORT": "",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
USE_I18N = False
USE_L10N = False
USE_TZ = True

# Event Renderers
EVENT_RENDERERS = {
    "serlo.org": {"en": "http://host.docker.internal:9009/events/render/"}
}

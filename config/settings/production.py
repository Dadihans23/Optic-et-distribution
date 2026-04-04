from .base import *

DEBUG = False

# En production, tailwind est déjà compilé en CSS statique — pas besoin du package
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ('tailwind', 'django_browser_reload')]

# Render génère un sous-domaine .onrender.com + ton domaine custom si configuré
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='.onrender.com'
).split(',')

# Sécurité
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Proxy Render (nécessaire pour que HTTPS soit bien détecté)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Fichiers statiques — WhiteNoise sert les fichiers directement
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

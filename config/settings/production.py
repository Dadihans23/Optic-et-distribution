from .base import *

DEBUG = False

# En production, tailwind est déjà compilé en CSS statique — pas besoin du package
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ('tailwind', 'django_browser_reload')]

# Pas de base SQL — tout est dans Firestore
DATABASES = {}

# Render génère un sous-domaine .onrender.com + ton domaine custom si configuré
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='.onrender.com'
).split(',')

# Sécurité — mettre HTTPS=true dans .env une fois SSL configuré
_HTTPS = config('HTTPS', default='false').lower() == 'true'

SESSION_COOKIE_SECURE = _HTTPS
CSRF_COOKIE_SECURE = _HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if _HTTPS else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = _HTTPS

# Proxy SSL (actif seulement si HTTPS=true)
if _HTTPS:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Fichiers statiques — WhiteNoise sert les fichiers directement avec compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

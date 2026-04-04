import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

print(f"[WSGI] Starting with settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}", file=sys.stderr)
print(f"[WSGI] Python {sys.version}", file=sys.stderr)

try:
    application = get_wsgi_application()
    print("[WSGI] Application loaded successfully", file=sys.stderr)
except Exception as e:
    print(f"[WSGI] STARTUP ERROR: {type(e).__name__}: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    raise

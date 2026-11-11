from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


ROBOTS_TXT = """User-agent: *
Disallow: /tableau-de-bord/
Disallow: /commandes/
Disallow: /bons-de-livraison/
Disallow: /admin/
Disallow: /connexion/
Disallow: /inscription/
Disallow: /deconnexion/
Disallow: /hors-ligne/
Allow: /
Allow: /politique-confidentialite/

Sitemap: https://optiqueetdistribution.site/sitemap.xml
"""


@require_GET
def robots_txt(request):
    return HttpResponse(ROBOTS_TXT, content_type='text/plain; charset=utf-8')


# ── PWA ──────────────────────────────────────────────────────────────
# Incrémenter PWA_VERSION pour forcer le rafraîchissement du cache côté clients.
PWA_VERSION = 'v1'

PWA_PRECACHE = [
    '/hors-ligne/',
    'css/tailwind.css',
    'images/logo.png',
    'images/pwa/icon-192.png',
    'images/pwa/icon-512.png',
]


@require_GET
def pwa_manifest(request):
    from django.http import JsonResponse
    from django.templatetags.static import static

    manifest = {
        'id': '/',
        'name': 'Optique & Distribution',
        'short_name': 'Optique & D',
        'description': "Commandes de verres et suivi des livraisons pour les boutiques partenaires d'Optique & Distribution.",
        'lang': 'fr',
        'dir': 'ltr',
        'start_url': '/?source=pwa',
        'scope': '/',
        'display': 'standalone',
        'orientation': 'portrait',
        'background_color': '#ffffff',
        'theme_color': '#1E88E5',
        'categories': ['business', 'productivity'],
        'icons': [
            {'src': static('images/pwa/icon-192.png'), 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': static('images/pwa/icon-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
            {'src': static('images/pwa/icon-maskable-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    response = JsonResponse(manifest, json_dumps_params={'ensure_ascii': False})
    response['Content-Type'] = 'application/manifest+json; charset=utf-8'
    response['Cache-Control'] = 'public, max-age=3600'
    return response


@require_GET
def service_worker(request):
    from django.templatetags.static import static

    import json

    precache = [u if u.startswith('/') else static(u) for u in PWA_PRECACHE]
    response = render(request, 'core/sw.js', {
        'version': json.dumps(PWA_VERSION),
        'precache': json.dumps(precache),
        'offline_url': json.dumps('/hors-ligne/'),
        'static_prefix': json.dumps(static('')),
    }, content_type='application/javascript; charset=utf-8')
    # Le navigateur doit toujours revérifier le service worker
    response['Cache-Control'] = 'no-cache'
    response['Service-Worker-Allowed'] = '/'
    return response


@require_GET
def offline(request):
    return render(request, 'core/offline.html')

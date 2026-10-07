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
Allow: /
Allow: /politique-confidentialite/

Sitemap: https://optiqueetdistribution.site/sitemap.xml
"""


@require_GET
def robots_txt(request):
    return HttpResponse(ROBOTS_TXT, content_type='text/plain; charset=utf-8')

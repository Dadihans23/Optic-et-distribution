from django.http import HttpResponsePermanentRedirect

CANONICAL_HOST = 'optiqueetdistribution.site'
WWW_HOST = 'www.' + CANONICAL_HOST


class CanonicalHostMiddleware:
    """Redirige en 301 www.optiqueetdistribution.site -> optiqueetdistribution.site.

    Ne s'applique qu'à cet hôte précis : sans effet en dev (localhost/127.0.0.1)
    ni sur les autres hôtes. Lit l'en-tête Host brut pour rediriger avant toute
    validation ALLOWED_HOSTS (le www n'a pas besoin d'y figurer).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_HOST', '').split(':')[0].lower()
        if host == WWW_HOST:
            return HttpResponsePermanentRedirect(
                f'https://{CANONICAL_HOST}{request.get_full_path()}'
            )
        return self.get_response(request)

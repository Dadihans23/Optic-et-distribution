from django.contrib.sitemaps import Sitemap
from django.urls import reverse

CANONICAL_DOMAIN = 'optiqueetdistribution.site'


class StaticPagesSitemap(Sitemap):
    """Pages publiques indexables. Domaine canonique forcé (sans www, https)."""

    protocol = 'https'
    changefreq = 'monthly'

    _priorities = {
        'root': 1.0,
        'core:privacy_policy': 0.3,
    }

    def items(self):
        return list(self._priorities)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self._priorities[item]

    def get_domain(self, site=None):
        return CANONICAL_DOMAIN

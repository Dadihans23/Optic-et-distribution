from django.urls import path, include
from django.shortcuts import redirect, render
from django.contrib.sitemaps.views import sitemap

from apps.core.sitemaps import StaticPagesSitemap
from apps.core.views import robots_txt

sitemaps = {'static': StaticPagesSitemap}


def root_redirect(request):
    if request.session.get('uid'):
        return redirect('dashboard:index')
    return landing_page(request)


def landing_page(request):
    context = {
        'stat_shops': 0,  # TODO: valeur réelle à fournir par le client
        'stat_orders': 0,  # TODO: valeur réelle à fournir par le client
        'stat_pdf_percent': 0,  # TODO: valeur réelle à fournir par le client
        'playstore_url': 'https://play.google.com/store/apps/details?id=com.monapp2.optic_vision&hl=fr_CH',
    }
    return render(request, 'landing.html', context)


urlpatterns = [
    path('', root_redirect, name='root'),
    path('landing/', landing_page, name='landing'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('apps.core.urls')),
    path('', include('apps.authentication.urls')),
    path('tableau-de-bord/', include('apps.dashboard.urls')),
    path('commandes/', include('apps.orders.urls')),
    path('bons-de-livraison/', include('apps.deliveries.urls')),
    path('admin/', include('apps.admin_panel.urls')),
]

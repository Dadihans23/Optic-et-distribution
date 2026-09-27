from django.urls import path, include
from django.shortcuts import redirect, render


def root_redirect(request):
    if request.session.get('uid'):
        return redirect('dashboard:index')
    return redirect('authentication:login')


def landing_page(request):
    context = {
        'stat_shops': 0,  # TODO: valeur réelle à fournir par le client
        'stat_orders': 0,  # TODO: valeur réelle à fournir par le client
        'stat_pdf_percent': 0,  # TODO: valeur réelle à fournir par le client
        'playstore_url': '#',  # TODO: valeur réelle à fournir par le client
    }
    return render(request, 'landing.html', context)


urlpatterns = [
    path('', root_redirect, name='root'),
    path('landing/', landing_page, name='landing'),
    path('', include('apps.core.urls')),
    path('', include('apps.authentication.urls')),
    path('tableau-de-bord/', include('apps.dashboard.urls')),
    path('commandes/', include('apps.orders.urls')),
    path('bons-de-livraison/', include('apps.deliveries.urls')),
    path('admin/', include('apps.admin_panel.urls')),
]

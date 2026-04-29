from django.urls import path, include
from django.shortcuts import redirect, render


def root_redirect(request):
    if request.session.get('uid'):
        return redirect('dashboard:index')
    return redirect('authentication:login')


def landing_page(request):
    return render(request, 'landing.html')


urlpatterns = [
    path('', root_redirect, name='root'),
    path('landing/', landing_page, name='landing'),
    path('', include('apps.authentication.urls')),
    path('tableau-de-bord/', include('apps.dashboard.urls')),
    path('commandes/', include('apps.orders.urls')),
    path('bons-de-livraison/', include('apps.deliveries.urls')),
    path('admin/', include('apps.admin_panel.urls')),
]

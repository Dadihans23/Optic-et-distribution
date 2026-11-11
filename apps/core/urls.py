from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('politique-confidentialite/', views.privacy_policy, name='privacy_policy'),
    # PWA — le service worker doit être servi à la racine pour contrôler tout le site
    path('manifest.webmanifest', views.pwa_manifest, name='pwa_manifest'),
    path('sw.js', views.service_worker, name='service_worker'),
    path('hors-ligne/', views.offline, name='offline'),
]

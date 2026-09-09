from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('politique-confidentialite/', views.privacy_policy, name='privacy_policy'),
]

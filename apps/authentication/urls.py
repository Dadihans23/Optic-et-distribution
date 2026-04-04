from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
]

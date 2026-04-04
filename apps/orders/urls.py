from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list_view, name='list'),
    path('nouvelle/', views.order_create_view, name='create'),
    path('<str:order_id>/', views.order_detail_view, name='detail'),
]

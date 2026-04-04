from django.urls import path
from . import views

app_name = 'deliveries'

urlpatterns = [
    path('', views.delivery_list_view, name='list'),
    path('nouveau/', views.delivery_create_view, name='create'),
    path('<str:delivery_id>/', views.delivery_detail_view, name='detail'),
    path('<str:delivery_id>/pdf/', views.delivery_pdf_view, name='pdf'),
]

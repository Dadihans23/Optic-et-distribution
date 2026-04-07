from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard_view, name='dashboard'),
    # Commandes
    path('commandes/', views.admin_orders_view, name='orders'),
    path('commandes/export/pdf/', views.admin_orders_export_pdf_view, name='orders_export_pdf'),
    path('commandes/<str:order_id>/', views.admin_order_detail_view, name='order_detail'),
    path('commandes/<str:order_id>/statut/', views.admin_update_status_view, name='update_status'),
    path('commandes/<str:order_id>/modifier/', views.admin_update_order_fields_view, name='update_order_fields'),
    path('commandes/<str:order_id>/archiver/', views.admin_archive_order_view, name='archive_order'),
    # Bons de livraison
    path('bons-de-livraison/', views.admin_deliveries_view, name='deliveries'),
    path('bons-de-livraison/export/pdf/', views.admin_deliveries_export_pdf_view, name='deliveries_export_pdf'),
    path('bons-de-livraison/compteur/', views.admin_bon_counter_view, name='bon_counter'),
    path('bons-de-livraison/<str:delivery_id>/', views.admin_delivery_detail_view, name='delivery_detail'),
    path('bons-de-livraison/<str:delivery_id>/modifier/', views.admin_update_delivery_fields_view, name='update_delivery_fields'),
    path('bons-de-livraison/<str:delivery_id>/statut/', views.admin_update_delivery_status_view, name='update_delivery_status'),
    path('bons-de-livraison/<str:delivery_id>/pdf/', views.admin_delivery_pdf_view, name='delivery_pdf'),
    # Boutiques
    path('boutiques/', views.admin_shops_view, name='shops'),
    path('boutiques/<str:shop_id>/', views.admin_shop_detail_view, name='shop_detail'),
    path('boutiques/<str:shop_id>/archiver/', views.admin_archive_shop_view, name='archive_shop'),
    # Identifiants & entreprise
    path('identifiants/', views.admin_credentials_view, name='credentials'),
    path('entreprise/', views.admin_company_view, name='company'),
]

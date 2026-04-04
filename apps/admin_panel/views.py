from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_POST

from apps.core.decorators import admin_required
from apps.core.firebase import get_db
from apps.orders.services import get_order_by_id
from apps.deliveries.services import get_delivery_by_id
from apps.deliveries.pdf import generate_bon_livraison
from .pdf import generate_fiche_finale_orders, generate_fiche_finale_deliveries
from .services import (
    get_all_orders, get_all_deliveries, get_all_shops, update_order_status,
    get_shop_by_id, get_orders_by_shop, get_deliveries_by_shop,
    update_order_fields, archive_order, archive_shop,
    get_company_info, update_company_info,
    get_orders_filtered, get_deliveries_filtered,
    update_delivery_fields,
)

STATUS_CHOICES = [
    ('pending',   'En attente'),
    ('confirmed', 'Confirmée'),
    ('shipped',   'Expédiée'),
    ('delivered', 'Livrée'),
]

DELIVERY_STATUS_CHOICES = [
    ('en_attente', 'En attente'),
    ('traite',     'Traité'),
    ('completed',  'Complété'),
]


@admin_required
def admin_dashboard_view(request):
    all_orders = get_all_orders()
    all_deliveries = get_all_deliveries()
    stats = {
        'total_orders':    len(all_orders),
        'pending':         sum(1 for o in all_orders if o.get('status') == 'pending'),
        'confirmed':       sum(1 for o in all_orders if o.get('status') == 'confirmed'),
        'shipped':         sum(1 for o in all_orders if o.get('status') == 'shipped'),
        'delivered':       sum(1 for o in all_orders if o.get('status') == 'delivered'),
        'pending_delivery': sum(1 for d in all_deliveries if d.get('status') == 'pending'),
    }
    recent_orders = all_orders[:8]
    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent_orders': recent_orders,
    })


@admin_required
def admin_orders_view(request):
    from datetime import date as date_type
    status_filter = request.GET.get('status', '')
    search = request.GET.get('q', '').strip()
    date_from_str = request.GET.get('date_from', '').strip()
    date_to_str = request.GET.get('date_to', '').strip()
    date_from, date_to = None, None
    try:
        if date_from_str:
            date_from = date_type.fromisoformat(date_from_str)
    except ValueError:
        pass
    try:
        if date_to_str:
            date_to = date_type.fromisoformat(date_to_str)
    except ValueError:
        pass
    orders = get_orders_filtered(date_from, date_to, search or None)
    if status_filter:
        orders = [o for o in orders if o.get('status') == status_filter]
    return render(request, 'admin_panel/orders.html', {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': STATUS_CHOICES,
        'search': search,
        'date_from': date_from_str,
        'date_to': date_to_str,
    })


@admin_required
def admin_order_detail_view(request, order_id):
    order = get_order_by_id(order_id)
    if not order:
        raise Http404
    return render(request, 'admin_panel/order_detail.html', {
        'order': order,
        'status_choices': STATUS_CHOICES,
    })


@admin_required
@require_POST
def admin_update_status_view(request, order_id):
    new_status = request.POST.get('status')
    if new_status in dict(STATUS_CHOICES):
        update_order_status(order_id, new_status)
        messages.success(request, 'Statut mis à jour.')
    return redirect('admin_panel:order_detail', order_id=order_id)


@admin_required
def admin_deliveries_view(request):
    from datetime import date as date_type
    status_filter = request.GET.get('status', '')
    date_from_str = request.GET.get('date_from', '').strip()
    date_to_str = request.GET.get('date_to', '').strip()
    date_from, date_to = None, None
    try:
        if date_from_str:
            date_from = date_type.fromisoformat(date_from_str)
    except ValueError:
        pass
    try:
        if date_to_str:
            date_to = date_type.fromisoformat(date_to_str)
    except ValueError:
        pass
    deliveries = get_deliveries_filtered(date_from, date_to)
    if status_filter:
        deliveries = [d for d in deliveries if d.get('status') == status_filter]
    return render(request, 'admin_panel/deliveries.html', {
        'deliveries': deliveries,
        'status_filter': status_filter,
        'date_from': date_from_str,
        'date_to': date_to_str,
    })


@admin_required
def admin_delivery_detail_view(request, delivery_id):
    delivery = get_delivery_by_id(delivery_id)
    if not delivery:
        raise Http404
    return render(request, 'admin_panel/delivery_detail.html', {
        'delivery': delivery,
        'delivery_status_choices': DELIVERY_STATUS_CHOICES,
    })


@admin_required
@require_POST
def admin_update_delivery_fields_view(request, delivery_id):
    delivery = get_delivery_by_id(delivery_id)
    if not delivery:
        raise Http404
    fields = [
        'wearerName', 'typeVerre', 'treatmentOption',
        'rightSph', 'rightCyl', 'rightAxe', 'rightAdd',
        'leftSph', 'leftCyl', 'leftAxe', 'leftAdd', 'notes',
    ]
    data = {f: request.POST.get(f, '').strip() for f in fields}
    update_delivery_fields(delivery_id, data)
    messages.success(request, 'Bon de livraison mis à jour.')
    return redirect('admin_panel:delivery_detail', delivery_id=delivery_id)


@admin_required
@require_POST
def admin_update_delivery_status_view(request, delivery_id):
    new_status = request.POST.get('status')
    allowed = {v for v, _ in DELIVERY_STATUS_CHOICES}
    if new_status in allowed:
        from datetime import datetime, timezone as tz
        db = get_db()
        db.collection('delivery_requests').document(delivery_id).update({
            'status': new_status,
            'updatedAt': datetime.now(tz=tz.utc),
        })
        messages.success(request, 'Statut mis à jour.')
    return redirect('admin_panel:delivery_detail', delivery_id=delivery_id)


@admin_required
def admin_shops_view(request):
    shops = get_all_shops()
    return render(request, 'admin_panel/shops.html', {'shops': shops})


@admin_required
def admin_shop_detail_view(request, shop_id):
    shop = get_shop_by_id(shop_id)
    if not shop:
        raise Http404
    orders = get_orders_by_shop(shop_id)
    deliveries = get_deliveries_by_shop(shop_id)
    return render(request, 'admin_panel/shop_detail.html', {
        'shop': shop,
        'orders': orders,
        'deliveries': deliveries,
    })


@admin_required
@require_POST
def admin_update_order_fields_view(request, order_id):
    order = get_order_by_id(order_id)
    if not order:
        raise Http404
    fields = [
        'wearerName', 'typeVerre', 'treatmentOption',
        'rightSph', 'rightCyl', 'rightAxe', 'rightAdd',
        'leftSph', 'leftCyl', 'leftAxe', 'leftAdd', 'notes',
    ]
    data = {f: request.POST.get(f, '').strip() for f in fields}
    update_order_fields(order_id, data)
    messages.success(request, 'Commande mise à jour.')
    return redirect('admin_panel:order_detail', order_id=order_id)


@admin_required
@require_POST
def admin_archive_order_view(request, order_id):
    archive_order(order_id)
    messages.success(request, 'Commande archivée.')
    return redirect('admin_panel:orders')


@admin_required
@require_POST
def admin_archive_shop_view(request, shop_id):
    archive_shop(shop_id)
    messages.success(request, 'Boutique désactivée.')
    return redirect('admin_panel:shop_detail', shop_id=shop_id)


@admin_required
def admin_credentials_view(request):
    shops = get_all_shops()
    search = request.GET.get('q', '').strip().lower()
    if search:
        shops = [
            s for s in shops
            if search in (s.get('shopName') or '').lower()
            or search in (s.get('phoneNumber') or '').lower()
        ]
    return render(request, 'admin_panel/credentials.html', {
        'shops': shops,
        'search': request.GET.get('q', ''),
    })


@admin_required
def admin_company_view(request):
    if request.method == 'POST':
        data = {
            'name':        request.POST.get('name', '').strip(),
            'description': request.POST.get('description', '').strip(),
            'address':     request.POST.get('address', '').strip(),
            'phone':       request.POST.get('phone', '').strip(),
            'rccm':        request.POST.get('rccm', '').strip(),
            'ncc':         request.POST.get('ncc', '').strip(),
        }
        update_company_info(data)
        messages.success(request, 'Informations entreprise mises à jour.')
        return redirect('admin_panel:company')
    company = get_company_info()
    return render(request, 'admin_panel/company.html', {'company': company})


@admin_required
def admin_orders_export_pdf_view(request):
    from datetime import date as date_type
    search = request.GET.get('q', '').strip()
    date_from_str = request.GET.get('date_from', '').strip()
    date_to_str = request.GET.get('date_to', '').strip()
    date_from, date_to = None, None
    try:
        if date_from_str:
            date_from = date_type.fromisoformat(date_from_str)
    except ValueError:
        pass
    try:
        if date_to_str:
            date_to = date_type.fromisoformat(date_to_str)
    except ValueError:
        pass
    orders = get_orders_filtered(date_from, date_to, search or None)
    company = get_company_info()
    pdf_bytes = generate_fiche_finale_orders(
        orders, company,
        date_from_str or None,
        date_to_str or None,
    )
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="fiche_finale_commandes.pdf"'
    return response


@admin_required
def admin_deliveries_export_pdf_view(request):
    from datetime import date as date_type
    date_from_str = request.GET.get('date_from', '').strip()
    date_to_str = request.GET.get('date_to', '').strip()
    date_from, date_to = None, None
    try:
        if date_from_str:
            date_from = date_type.fromisoformat(date_from_str)
    except ValueError:
        pass
    try:
        if date_to_str:
            date_to = date_type.fromisoformat(date_to_str)
    except ValueError:
        pass
    deliveries = get_deliveries_filtered(date_from, date_to)
    company = get_company_info()
    pdf_bytes = generate_fiche_finale_deliveries(
        deliveries, company,
        date_from_str or None,
        date_to_str or None,
    )
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="fiche_finale_livraisons.pdf"'
    return response


@admin_required
def admin_delivery_pdf_view(request, delivery_id):
    delivery = get_delivery_by_id(delivery_id)
    if not delivery:
        raise Http404
    db = get_db()
    company_doc = db.collection('company_info').document('company_info').get()
    company = company_doc.to_dict() if company_doc.exists else {}
    pdf_bytes = generate_bon_livraison(delivery, company)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="bon_livraison_{delivery_id[:8]}.pdf"'
    return response

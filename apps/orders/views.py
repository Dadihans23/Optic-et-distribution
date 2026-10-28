from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.views.decorators.http import require_POST

from apps.core.decorators import login_required
from .services import (
    get_orders_by_user, get_order_by_id, create_order, update_order, archive_order,
)
from .forms import OrderForm, TYPE_VERRE_CHOICES, TREATMENT_CHOICES


def _get_own_order(order_id, uid):
    """Commande visible par le client : existe, lui appartient, non archivée."""
    order = get_order_by_id(order_id)
    if not order or order.get('userId') != uid or order.get('archived'):
        raise Http404
    return order


def _get_own_pending_order(order_id, uid):
    """Commande modifiable/supprimable : propriétaire + statut 'pending'.
    Le SDK Admin ignore les règles Firestore : ce contrôle est la seule protection côté web."""
    order = _get_own_order(order_id, uid)
    if order.get('status') != 'pending':
        raise Http404
    return order


@login_required
def order_list_view(request):
    uid = request.session['uid']
    status_filter = request.GET.get('status', '')
    orders = get_orders_by_user(uid, status_filter or None)
    return render(request, 'orders/list.html', {
        'orders': orders,
        'status_filter': status_filter,
        'type_verre_choices': TYPE_VERRE_CHOICES[1:],
        'treatment_choices': TREATMENT_CHOICES[1:],
    })


@login_required
def order_create_view(request):
    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        uid = request.session['uid']
        shop_name = request.session.get('shopName', '')
        order_id = create_order(uid, shop_name, form.cleaned_data)
        messages.success(request, 'Commande créée avec succès.')
        return redirect('orders:detail', order_id=order_id)
    return render(request, 'orders/create.html', {'form': form})


@login_required
def order_edit_view(request, order_id):
    uid = request.session['uid']
    order = _get_own_pending_order(order_id, uid)
    initial = {name: order.get(name) for name in OrderForm.base_fields}
    if not initial.get('nombrePaires'):
        initial['nombrePaires'] = 1
    form = OrderForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        update_order(order_id, form.cleaned_data)
        messages.success(request, 'Commande modifiée avec succès.')
        return redirect('orders:detail', order_id=order_id)
    return render(request, 'orders/create.html', {
        'form': form,
        'edit_mode': True,
        'order': order,
    })


@login_required
@require_POST
def order_delete_view(request, order_id):
    uid = request.session['uid']
    _get_own_pending_order(order_id, uid)
    archive_order(order_id)
    messages.success(request, 'Commande supprimée avec succès.')
    return redirect('orders:list')


@login_required
def order_detail_view(request, order_id):
    uid = request.session['uid']
    order = _get_own_order(order_id, uid)
    return render(request, 'orders/detail.html', {'order': order})

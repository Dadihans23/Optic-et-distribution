from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404

from apps.core.decorators import login_required
from .services import get_orders_by_user, get_order_by_id, create_order
from .forms import OrderForm, TYPE_VERRE_CHOICES, TREATMENT_CHOICES


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
    return render(request, 'orders/create.html', {
        'form': form,
        'type_verre_options': TYPE_VERRE_CHOICES[1:],
        'treatment_options': TREATMENT_CHOICES[1:],
    })


@login_required
def order_detail_view(request, order_id):
    uid = request.session['uid']
    order = get_order_by_id(order_id)
    if not order or order.get('userId') != uid:
        raise Http404
    return render(request, 'orders/detail.html', {'order': order})

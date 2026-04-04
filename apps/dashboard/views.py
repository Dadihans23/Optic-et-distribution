from django.shortcuts import render
from apps.core.decorators import login_required
from apps.orders.services import get_orders_by_user


@login_required
def dashboard_view(request):
    uid = request.session['uid']
    all_orders = get_orders_by_user(uid)

    stats = {
        'pending':   sum(1 for o in all_orders if o.get('status') == 'pending'),
        'confirmed': sum(1 for o in all_orders if o.get('status') == 'confirmed'),
        'shipped':   sum(1 for o in all_orders if o.get('status') == 'shipped'),
        'delivered': sum(1 for o in all_orders if o.get('status') == 'delivered'),
        'total':     len(all_orders),
    }
    recent_orders = all_orders[:5]

    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'recent_orders': recent_orders,
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse

from apps.core.decorators import login_required
from apps.orders.forms import TYPE_VERRE_CHOICES, TREATMENT_CHOICES
from .services import get_deliveries_by_user, get_delivery_by_id, create_delivery_request
from .forms import DeliveryRequestForm
from .pdf import generate_bon_livraison


@login_required
def delivery_list_view(request):
    uid = request.session['uid']
    deliveries = get_deliveries_by_user(uid)
    return render(request, 'deliveries/list.html', {'deliveries': deliveries})


@login_required
def delivery_create_view(request):
    form = DeliveryRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        uid = request.session['uid']
        shop_name = request.session.get('shopName', '')
        from apps.core.firebase import get_db
        user_doc = get_db().collection('users').document(uid).get()
        phone_number = user_doc.to_dict().get('phoneNumber', '') if user_doc.exists else ''
        delivery_id = create_delivery_request(uid, shop_name, phone_number, form.cleaned_data)
        messages.success(request, 'Demande de bon de livraison envoyée.')
        return redirect('deliveries:detail', delivery_id=delivery_id)
    return render(request, 'deliveries/create.html', {
        'form': form,
        'type_verre_options': TYPE_VERRE_CHOICES[1:],
        'treatment_options': TREATMENT_CHOICES[1:],
    })


@login_required
def delivery_detail_view(request, delivery_id):
    uid = request.session['uid']
    delivery = get_delivery_by_id(delivery_id)
    if not delivery or delivery.get('userId') != uid:
        raise Http404
    return render(request, 'deliveries/detail.html', {'delivery': delivery})


@login_required
def delivery_pdf_view(request, delivery_id):
    uid = request.session['uid']
    delivery = get_delivery_by_id(delivery_id)
    if not delivery or delivery.get('userId') != uid:
        raise Http404

    if delivery.get('status') not in ('traité', 'completed'):
        raise Http404

    from apps.core.firebase import get_db
    db = get_db()
    company_doc = db.collection('company_info').document('company_info').get()
    company = company_doc.to_dict() if company_doc.exists else {}

    pdf_bytes = generate_bon_livraison(delivery, company)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    if request.GET.get('preview'):
        response['Content-Disposition'] = f'inline; filename="bon_livraison_{delivery_id[:8]}.pdf"'
    else:
        response['Content-Disposition'] = f'attachment; filename="bon_livraison_{delivery_id[:8]}.pdf"'
    return response

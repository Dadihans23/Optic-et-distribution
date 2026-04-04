from django import template
from django.utils.safestring import mark_safe
from datetime import datetime

register = template.Library()

STATUS_LABELS = {
    'pending':   ('En attente',  'bg-yellow-100 text-yellow-800'),
    'confirmed': ('Confirmée',   'bg-blue-100 text-blue-800'),
    'shipped':   ('Expédiée',    'bg-purple-100 text-purple-800'),
    'delivered': ('Livrée',      'bg-green-100 text-green-800'),
}

DELIVERY_STATUS_LABELS = {
    'pending':  ('En attente', 'bg-yellow-100 text-yellow-800'),
    'approved': ('Approuvée',  'bg-green-100 text-green-800'),
    'rejected': ('Refusée',    'bg-red-100 text-red-800'),
}


@register.simple_tag
def status_badge(status, delivery=False):
    mapping = DELIVERY_STATUS_LABELS if delivery else STATUS_LABELS
    label, classes = mapping.get(status, (status, 'bg-gray-100 text-gray-800'))
    return mark_safe(f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {classes}">{label}</span>')


@register.filter
def status_label(status):
    return STATUS_LABELS.get(status, (status,))[0]


@register.filter
def date_fr(value):
    if not value:
        return '-'
    MONTHS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
    try:
        if hasattr(value, 'strftime'):
            dt = value
        else:
            dt = datetime.fromisoformat(str(value))
        return f"{dt.day} {MONTHS[dt.month - 1]} {dt.year}"
    except Exception:
        return str(value)

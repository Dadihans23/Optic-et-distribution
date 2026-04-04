from datetime import datetime, timezone
from google.cloud.firestore_v1.base_query import FieldFilter
from apps.core.firebase import get_db


def _db():
    return get_db()


def get_all_orders(status_filter=None) -> list[dict]:
    db = _db()
    query = db.collection('orders')
    if status_filter:
        query = query.where(filter=FieldFilter('status', '==', status_filter))
    docs = query.stream()
    orders = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        orders.append(d)
    orders.sort(key=lambda x: x.get('createdAt') or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return orders


def get_all_deliveries(status_filter=None) -> list[dict]:
    db = _db()
    query = db.collection('delivery_requests')
    if status_filter:
        query = query.where(filter=FieldFilter('status', '==', status_filter))
    docs = query.stream()
    deliveries = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        deliveries.append(d)
    deliveries.sort(key=lambda x: x.get('createdAt') or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return deliveries


def get_all_shops() -> list[dict]:
    db = _db()
    docs = db.collection('users').where(filter=FieldFilter('role', '==', 'client')).stream()
    shops = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        shops.append(d)
    shops.sort(key=lambda x: x.get('shopName', ''))
    return shops


def update_order_status(order_id: str, new_status: str):
    db = _db()
    db.collection('orders').document(order_id).update({
        'status': new_status,
        'updatedAt': datetime.now(tz=timezone.utc),
    })


def get_shop_by_id(shop_id: str) -> dict | None:
    db = _db()
    doc = db.collection('users').document(shop_id).get()
    if doc.exists:
        d = doc.to_dict()
        d['id'] = doc.id
        return d
    return None


def get_orders_by_shop(shop_id: str) -> list[dict]:
    db = _db()
    docs = db.collection('orders').where(filter=FieldFilter('userId', '==', shop_id)).stream()
    orders = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        orders.append(d)
    orders.sort(key=lambda x: x.get('createdAt') or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return orders


def get_deliveries_by_shop(shop_id: str) -> list[dict]:
    db = _db()
    docs = db.collection('delivery_requests').where(filter=FieldFilter('userId', '==', shop_id)).stream()
    deliveries = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        deliveries.append(d)
    deliveries.sort(key=lambda x: x.get('createdAt') or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return deliveries


def update_order_fields(order_id: str, data: dict):
    db = _db()
    allowed = {
        'wearerName', 'typeVerre', 'treatmentOption',
        'rightSph', 'rightCyl', 'rightAxe', 'rightAdd',
        'leftSph', 'leftCyl', 'leftAxe', 'leftAdd', 'notes',
    }
    payload = {k: v for k, v in data.items() if k in allowed}
    payload['updatedAt'] = datetime.now(tz=timezone.utc)
    db.collection('orders').document(order_id).update(payload)


def update_delivery_fields(delivery_id: str, data: dict):
    db = _db()
    allowed = {
        'wearerName', 'typeVerre', 'treatmentOption',
        'rightSph', 'rightCyl', 'rightAxe', 'rightAdd',
        'leftSph', 'leftCyl', 'leftAxe', 'leftAdd', 'notes',
    }
    payload = {k: v for k, v in data.items() if k in allowed}
    payload['updatedAt'] = datetime.now(tz=timezone.utc)
    db.collection('delivery_requests').document(delivery_id).update(payload)


def archive_order(order_id: str):
    db = _db()
    db.collection('orders').document(order_id).update({
        'archived': True,
        'updatedAt': datetime.now(tz=timezone.utc),
    })


def archive_shop(shop_id: str):
    db = _db()
    db.collection('users').document(shop_id).update({
        'archived': True,
        'updatedAt': datetime.now(tz=timezone.utc),
    })


def get_company_info() -> dict:
    db = _db()
    doc = db.collection('company_info').document('company_info').get()
    if doc.exists:
        return doc.to_dict()
    return {}


def update_company_info(data: dict):
    db = _db()
    allowed = {'name', 'description', 'address', 'phone', 'rccm', 'ncc'}
    payload = {k: v for k, v in data.items() if k in allowed and v is not None}
    db.collection('company_info').document('company_info').set(payload, merge=True)


def get_orders_filtered(date_from=None, date_to=None, search: str = None) -> list[dict]:
    """Retourne toutes les commandes non-archivées, filtrées par date et/ou recherche texte."""
    orders = get_all_orders()
    # Exclure les archivées
    orders = [o for o in orders if not o.get('archived')]
    # Filtre date
    if date_from:
        orders = [o for o in orders if o.get('createdAt') and o['createdAt'].date() >= date_from]
    if date_to:
        orders = [o for o in orders if o.get('createdAt') and o['createdAt'].date() <= date_to]
    # Recherche texte
    if search:
        s = search.lower()
        orders = [
            o for o in orders
            if s in (o.get('shopName') or '').lower()
            or s in (o.get('wearerName') or '').lower()
            or s in (o.get('orderNumber') or '').lower()
        ]
    return orders


def get_deliveries_filtered(date_from=None, date_to=None) -> list[dict]:
    """Retourne tous les bons non-archivés, filtrés par date."""
    deliveries = get_all_deliveries()
    deliveries = [d for d in deliveries if not d.get('archived')]
    if date_from:
        deliveries = [d for d in deliveries if d.get('createdAt') and d['createdAt'].date() >= date_from]
    if date_to:
        deliveries = [d for d in deliveries if d.get('createdAt') and d['createdAt'].date() <= date_to]
    return deliveries

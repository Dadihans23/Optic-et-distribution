from datetime import datetime, timezone
import random
import string
from google.cloud.firestore_v1.base_query import FieldFilter
from apps.core.firebase import get_db


def _db():
    return get_db()


def get_orders_by_user(uid: str, status_filter: str = None) -> list[dict]:
    db = _db()
    query = db.collection('orders').where(filter=FieldFilter('userId', '==', uid))
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


def get_order_by_id(order_id: str) -> dict | None:
    db = _db()
    doc = db.collection('orders').document(order_id).get()
    if doc.exists:
        d = doc.to_dict()
        d['id'] = doc.id
        return d
    return None


def _generate_order_number() -> str:
    suffix = ''.join(random.choices(string.digits, k=4))
    now = datetime.now()
    return f"OV-{now.strftime('%Y%m%d')}-{suffix}"


def create_order(uid: str, shop_name: str, data: dict) -> str:
    db = _db()
    order_number = _generate_order_number()
    doc_data = {
        'userId': uid,
        'shopName': shop_name,
        'orderNumber': order_number,
        'status': 'pending',
        'createdAt': datetime.now(tz=timezone.utc),
        **data,
    }
    ref = db.collection('orders').document()
    ref.set(doc_data)
    return ref.id

from datetime import datetime, timezone
from google.cloud.firestore_v1.base_query import FieldFilter
from apps.core.firebase import get_db


def _db():
    return get_db()


def get_deliveries_by_user(uid: str) -> list[dict]:
    db = _db()
    docs = db.collection('delivery_requests').where(filter=FieldFilter('userId', '==', uid)).stream()
    deliveries = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        deliveries.append(d)
    deliveries.sort(key=lambda x: x.get('createdAt') or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return deliveries


def get_delivery_by_id(delivery_id: str) -> dict | None:
    db = _db()
    doc = db.collection('delivery_requests').document(delivery_id).get()
    if doc.exists:
        d = doc.to_dict()
        d['id'] = doc.id
        return d
    return None


def create_delivery_request(uid: str, shop_name: str, phone_number: str, data: dict) -> str:
    db = _db()
    doc_data = {
        'userId': uid,
        'shopName': shop_name,
        'phoneNumber': phone_number,
        'status': 'en_attente',
        'createdAt': datetime.now(tz=timezone.utc),
        **data,
    }
    ref = db.collection('delivery_requests').document()
    ref.set(doc_data)
    return ref.id

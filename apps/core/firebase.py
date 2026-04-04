import firebase_admin
from firebase_admin import credentials, firestore, auth
from django.conf import settings

_app = None


def get_firebase_app():
    global _app
    if _app is None:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        _app = firebase_admin.initialize_app(cred)
    return _app


def get_db():
    get_firebase_app()
    return firestore.client()


def verify_token(id_token: str) -> dict:
    get_firebase_app()
    return auth.verify_id_token(id_token)

import logging
import requests as http_requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_http_methods

from apps.core.firebase import get_db, verify_token
from .forms import PhoneLoginForm

logger = logging.getLogger(__name__)


FIREBASE_SIGN_IN_URL = (
    'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'
)


def _firebase_sign_in(phone_number: str) -> dict | None:
    """Appelle Firebase Auth REST API et retourne le payload ou None si échec."""
    email = f"{phone_number}@lunetterie.com"
    password = f"{phone_number}lunetterie"

    try:
        resp = http_requests.post(
            FIREBASE_SIGN_IN_URL,
            params={'key': settings.FIREBASE_WEB_API_KEY},
            json={'email': email, 'password': password, 'returnSecureToken': True},
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json()
    except http_requests.RequestException:
        pass
    return None


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.session.get('uid'):
        return redirect('dashboard:index')

    form = PhoneLoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        phone = form.cleaned_data['phone_number']

        payload = _firebase_sign_in(phone)
        if not payload:
            error = 'Numéro de téléphone introuvable ou incorrect.'
        else:
            try:
                decoded = verify_token(payload['idToken'])
                uid = decoded['uid']

                db = get_db()
                user_doc = db.collection('users').document(uid).get()

                if not user_doc.exists:
                    error = 'Compte introuvable.'
                else:
                    data = user_doc.to_dict()
                    if data.get('archived') is True:
                        error = 'Ce compte a été désactivé. Contactez l\'administrateur.'
                    elif data.get('role') not in ('client', 'user', 'admin'):
                        error = 'Accès non autorisé.'
                    elif data.get('role') == 'admin':
                        admin_password = request.POST.get('admin_password', '').strip()
                        if not admin_password:
                            request.session['pending_admin_uid'] = uid
                            request.session['pending_admin_data'] = {
                                'shopName': data.get('shopName', ''),
                                'phoneNumber': data.get('phoneNumber', phone),
                                'firstName': data.get('firstName', ''),
                            }
                            return render(request, 'authentication/login.html', {
                                'form': form,
                                'show_admin_password': True,
                                'phone_value': phone,
                            })
                        else:
                            stored = data.get('adminPassword', '')
                            if admin_password != stored:
                                request.session.pop('pending_admin_uid', None)
                                request.session.pop('pending_admin_data', None)
                                error = 'Mot de passe administrateur incorrect.'
                            else:
                                request.session.flush()
                                request.session['uid'] = uid
                                request.session['shopName'] = data.get('shopName', 'Admin')
                                request.session['phoneNumber'] = data.get('phoneNumber', phone)
                                request.session['firstName'] = data.get('firstName', '')
                                request.session['role'] = 'admin'
                                return redirect('admin_panel:dashboard')
                    else:
                        request.session.flush()
                        request.session['uid'] = uid
                        request.session['shopName'] = data.get('shopName', '')
                        request.session['phoneNumber'] = data.get('phoneNumber', phone)
                        request.session['firstName'] = data.get('firstName', '')
                        request.session['role'] = data.get('role', 'client')
                        return redirect('dashboard:index')

            except Exception as e:
                logger.exception('Erreur login : %s', e)
                error = 'Une erreur est survenue. Veuillez réessayer.'

    return render(request, 'authentication/login.html', {'form': form, 'error': error})


@require_http_methods(['GET', 'POST'])
def logout_view(request):
    request.session.flush()
    return redirect('authentication:login')

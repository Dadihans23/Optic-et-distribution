from apps.core.firebase import get_db


def company_info(request):
    """Injecte les infos entreprise dans tous les templates."""
    try:
        db = get_db()
        doc = db.collection('company_info').document('company_info').get()
        if doc.exists:
            return {'company': doc.to_dict()}
    except Exception:
        pass
    return {'company': {
        'name': 'OPTIQUE & DISTRIBUTION',
        'address': 'Yopougon Keneya, Immeuble en face de cosmos',
        'phone': '(225) 01 01 28 16 80 / 07 07 15 23 06',
    }}


def current_user(request):
    """Injecte les données session utilisateur dans tous les templates."""
    return {
        'session_uid': request.session.get('uid'),
        'session_shop': request.session.get('shopName', ''),
        'session_phone': request.session.get('phoneNumber', ''),
        'session_name': request.session.get('firstName', ''),
    }

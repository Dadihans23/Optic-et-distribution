# Déploiement sur Render — Django + Firestore

Stack : Django 4.2 · Firestore · WhiteNoise · Gunicorn · Tailwind CSS (compilé)

---

## Fichiers de config à avoir dans le repo

### `requirements.txt`
```
Django==4.2.13
firebase_admin==7.3.0
google-cloud-firestore==2.25.0
gunicorn==25.1.0
whitenoise==6.12.0
python-decouple==3.8
reportlab==4.4.10
Pillow==12.1.1
requests==2.32.5
```

### `build.sh`
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Télécharger Tailwind CLI standalone (pas besoin de Node.js)
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64

# Compiler le CSS avec la config custom
./tailwindcss-linux-x64 -c tailwind.config.js -i ./static/css/input.css -o ./static/css/tailwind.css --minify

python manage.py collectstatic --no-input
# Pas de migrate — base de données Firestore (pas SQL)
```

### `tailwind.config.js`
```js
module.exports = {
  content: ['./templates/**/*.html'],
  theme: {
    extend: {
      colors: {
        primary:  { DEFAULT: '#1E88E5', dark: '#1565C0', light: '#42A5F5' },
        accent:   { DEFAULT: '#EF6C00', light: '#FFA726' },
        sidebar:  { DEFAULT: '#0F172A', hover: '#1E293B', active: '#1E3A5F' },
      },
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] }
    }
  },
  plugins: [],
}
```

### `static/css/input.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## Configuration Render (Dashboard)

### Settings du service

| Champ | Valeur |
|-------|--------|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| **Root Directory** | `web_platform` (si le projet n'est pas à la racine du repo) |

> ⚠️ Le Build Command dans le dashboard Render doit correspondre exactement. Ne pas laisser Render auto-détecter avec `migrate` à la fin.

---

## Variables d'environnement (Render → Environment)

| Clé | Valeur |
|-----|--------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `SECRET_KEY` | Générer avec : `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` (ajouter le domaine custom si besoin : `.onrender.com,ton-domaine.com`) |
| `FIREBASE_CREDENTIALS_PATH` | `/etc/secrets/firebase_credentials.json` |
| `FIREBASE_WEB_API_KEY` | Ta clé Firebase Web API |
| `SESSION_COOKIE_AGE` | `28800` |

---

## Secret Files (Render → Environment → Secret Files)

C'est **différent** des variables d'environnement. C'est un fichier réel placé sur le serveur.

| Filename | Mount path |
|----------|------------|
| `firebase_credentials.json` | `/etc/secrets/firebase_credentials.json` |

**Contents** : coller le contenu complet du fichier `firebase_credentials.json` local.

> ⚠️ Sans ce fichier, Firebase Admin SDK ne peut pas s'initialiser → erreur login.

---

## Settings Django production (`config/settings/production.py`)

Points importants :
- `INSTALLED_APPS` : retirer `tailwind` et `django_browser_reload` (inutiles en prod)
- `DATABASES = {}` : pas de SQL, tout est Firestore → évite l'erreur `migrate`
- `SECURE_PROXY_SSL_HEADER` : nécessaire derrière le proxy Render
- `STATICFILES_STORAGE` : utiliser `CompressedStaticFilesStorage` (pas `CompressedManifest...` qui exige un manifest strict)

---

## Tailwind CSS — Compilation locale (Windows)

À faire à chaque modification de template ou de config Tailwind :

```bash
cd web_platform

# Télécharger une seule fois
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-windows-x64.exe

# Compiler
./tailwindcss-windows-x64.exe -c tailwind.config.js -i ./static/css/input.css -o ./static/css/tailwind.css --minify
```

> Le fichier `static/css/tailwind.css` généré doit être commité dans le repo — Render en a besoin via `collectstatic`.

---

## Erreurs rencontrées et solutions

| Erreur | Cause | Fix |
|--------|-------|-----|
| `ModuleNotFoundError: No module named 'tailwind'` | `django-tailwind` absent mais dans `INSTALLED_APPS` | Retirer de `INSTALLED_APPS` en prod |
| `ImproperlyConfigured: settings.DATABASES` | Render lançait `migrate` automatiquement | Supprimer `migrate` du Build Command |
| `Application exited early` | Le Start Command était `pip install + collectstatic` au lieu de `gunicorn` | Corriger le Start Command dans Render |
| `FileNotFoundError: firebase_credentials.json` | Env var définie mais fichier non uploadé | Ajouter via Secret Files (section séparée) |
| `Token used too early` | Horloge PC en retard sur Firebase | `auth.verify_id_token(token, clock_skew_seconds=60)` |
| UI cassée / sans style | CDN Tailwind bloqué ou lent en production | Compiler Tailwind en CSS local + servir via WhiteNoise |
| `0 static files copied` | `STATICFILES_DIRS` manquant dans settings | Ajouter `STATICFILES_DIRS = [BASE_DIR / 'static']` |

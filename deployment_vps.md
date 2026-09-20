# Guide de déploiement VPS + Nom de domaine
## Optic & Distribution — Django sur Contabo (Ubuntu)

---

## Prérequis

- VPS Ubuntu avec accès SSH
- Nom de domaine acheté (ex: LWS, OVH, Namecheap...)
- Application Django déjà configurée localement
- Gunicorn installé dans le venv

---

## Étape 1 — Pointer le DNS vers le VPS

Sur l'interface de ton registrar (LWS, OVH, etc.) :

1. Va dans **"Mes domaines"** → sélectionne ton domaine
2. Ouvre la **Zone DNS**
3. Supprime les enregistrements A existants
4. Ajoute ces 2 enregistrements :

| Type | Nom | Valeur        | TTL  |
|------|-----|---------------|------|
| A    | `@` | `IP_DU_VPS`   | 3600 |
| A    | `www` | `IP_DU_VPS` | 3600 |

> La propagation DNS prend 5 à 30 minutes (parfois jusqu'à 24h).

---

## Étape 2 — Configurer Nginx

### Créer le fichier de config Nginx

```bash
sudo nano /etc/nginx/sites-available/nom-du-projet
```

Contenu à mettre :

```nginx
server {
    listen 80;
    server_name mondomaine.site www.mondomaine.site;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/user/mon-projet/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/mon-projet/projet.sock;
    }
}
```

> Remplace `mondomaine.site`, `/home/user/mon-projet/` et `projet.sock` par tes valeurs réelles.

### Activer le site

```bash
sudo ln -s /etc/nginx/sites-available/nom-du-projet /etc/nginx/sites-enabled/
```

### Tester et recharger Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## Étape 3 — Certificat SSL (HTTPS gratuit)

### Installer Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Générer le certificat

```bash
sudo certbot --nginx -d mondomaine.site -d www.mondomaine.site
```

Certbot te demandera :
- Ton adresse email
- D'accepter les CGU

Il configure automatiquement le HTTPS et le renouvellement automatique.

---

## Étape 4 — Configurer Django

### Mettre à jour ALLOWED_HOSTS dans le .env

```bash
nano /home/user/mon-projet/.env
```

Modifier ou ajouter ces lignes :

```env
ALLOWED_HOSTS=mondomaine.site,www.mondomaine.site,IP_DU_VPS
HTTPS=true
```

---

## Étape 5 — Relancer Gunicorn

### Trouver le PID du processus maître

```bash
ps aux | grep gunicorn
```

Le processus maître est celui avec le flag `Ssl` dans la colonne STAT.

### Tuer et relancer proprement

```bash
kill PID_MAITRE

cd /home/user/mon-projet
source venv/bin/activate
gunicorn --workers 3 --bind unix:/home/user/mon-projet/projet.sock config.wsgi:application --daemon
```

---

## Vérification finale

- Ouvre **https://mondomaine.site** dans le navigateur
- Le cadenas HTTPS doit être présent
- Aucune erreur 400 ou 502

---

## Dépannage

| Erreur | Cause | Solution |
|--------|-------|----------|
| `400 Bad Request` | Domaine absent de `ALLOWED_HOSTS` | Vérifier le `.env` et relancer Gunicorn |
| `502 Bad Gateway` | Gunicorn ne tourne pas | Relancer Gunicorn |
| `SSL non valide` | Certificat non généré | Relancer `certbot --nginx` |
| Site inaccessible | DNS pas encore propagé | Attendre 30 min et retester |

---

## Infos du projet (Optic & Distribution)

| Élément | Valeur |
|---------|--------|
| Domaine | `optiqueetdistribution.site` |
| IP VPS | `79.143.190.190` |
| Répertoire | `/home/hans/Optic-et-distribution/` |
| Socket | `optic.sock` |
| Config Nginx | `/etc/nginx/sites-available/optic-vision` |
| Certificat SSL | expire le **28/08/2026** (renouvellement auto) |
| WSGI | `config.wsgi:application` |

---

## Renouvellement SSL

Certbot configure le renouvellement automatique. Pour tester manuellement :

```bash
sudo certbot renew --dry-run
```

#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Télécharger Tailwind CLI standalone (pas besoin de Node.js)
echo "==> Downloading Tailwind CSS CLI..."
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64

# Compiler le CSS avec la config custom (couleurs primary/accent/sidebar)
echo "==> Building Tailwind CSS..."
./tailwindcss-linux-x64 -c tailwind.config.js -i ./static/css/input.css -o ./static/css/tailwind.css --minify

python manage.py collectstatic --no-input
# Pas de migrate — la base de données est Firestore (pas de SQL)

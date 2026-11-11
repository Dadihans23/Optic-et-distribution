{% autoescape off %}/* Service worker — Optique & Distribution (généré par apps.core.views.service_worker) */
const VERSION = {{ version }};
const CACHE = 'od-' + VERSION;
const PRECACHE = {{ precache }};
const OFFLINE_URL = {{ offline_url }};
const STATIC_PREFIX = {{ static_prefix }};

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(PRECACHE.map((u) => new Request(u, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith('od-') && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Pages : toujours le réseau (données à jour, jamais mises en cache).
  // Sans connexion : page « hors ligne ».
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req).catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }

  // Fichiers statiques (CSS, images) : réponse immédiate depuis le cache,
  // mise à jour en arrière-plan.
  if (url.pathname.startsWith(STATIC_PREFIX)) {
    event.respondWith(
      caches.open(CACHE).then((cache) =>
        cache.match(req).then((cached) => {
          const network = fetch(req)
            .then((res) => {
              if (res.ok) cache.put(req, res.clone());
              return res;
            })
            .catch(() => cached);
          return cached || network;
        })
      )
    );
  }
  // Tout le reste (APK, PDF, API…) : comportement normal du navigateur.
});
{% endautoescape %}

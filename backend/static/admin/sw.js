const CACHE_NAME = 'solidmenu-admin-v14';
const ASSETS = [
    './login.html',
    './index.html',
    './css/style.css',
    './js/theme.js',
    './js/api.js',
    './js/auth.js',
    './js/router.js',
    './js/cardapio.js',
    './views/dashboard.html',
    './views/cardapio.html',
    './assets/logo.png'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', (e) => {
    // Para chamadas da /api, não cacheamos (dados em tempo real)
    if (e.request.url.includes('/api/')) {
        return fetch(e.request);
    }
    
    // Para estáticos, serve do cache e tenta atualizar em background (Stale-while-revalidate simples)
    e.respondWith(
        caches.match(e.request).then((cachedResponse) => {
            const fetchPromise = fetch(e.request).then((networkResponse) => {
                const responseClone = networkResponse.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(e.request, responseClone);
                });
                return networkResponse;
            });
            return cachedResponse || fetchPromise;
        })
    );
});

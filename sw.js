// FishCare AI service worker — makes the site installable and shows an
// offline page when a navigation fails. It deliberately caches nothing else:
// /species, /fish-health and /identify are proxied apps, and serving them
// stale HTML or chunks from a cache would break them after each deploy.
// Bump VERSION when offline.html changes.
var VERSION = 'fc-sw-v1';
var OFFLINE_URL = '/offline.html';

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(VERSION).then(function (cache) {
      return cache.add(OFFLINE_URL);
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== VERSION; })
        .map(function (k) { return caches.delete(k); }));
    }).then(function () {
      // Lets the network request start while the worker boots, so pages are
      // not slowed down by having a service worker in front of them.
      if (self.registration.navigationPreload) {
        return self.registration.navigationPreload.enable();
      }
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (event) {
  if (event.request.mode !== 'navigate' || event.request.method !== 'GET') return;
  event.respondWith((async function () {
    try {
      var preloaded = await event.preloadResponse;
      if (preloaded) return preloaded;
      return await fetch(event.request);
    } catch (err) {
      var cache = await caches.open(VERSION);
      return (await cache.match(OFFLINE_URL)) || Response.error();
    }
  })());
});

// Offline cache: after the first visit every file is served from the phone.
const CACHE = "wpl-d57e4e4cbb";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png", "lib/pdf.min.js", "lib/ocr-worker.js", "lib/zxing.min.js", "lib/pdf.worker.min.js", "lib/tesseract.min.js", "lib/worker.min.js", "lib/core/tesseract-core-lstm.wasm.js", "lib/core/tesseract-core-simd-lstm.wasm.js", "lang/eng-traineddata-gz.wasm"];
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});

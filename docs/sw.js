// Offline cache. The small app shell is refreshed with every update; the 12 MB readers are
// cached separately and only downloaded again when they change.
const SHELL = "wpl-shell-47440f0ee2", LIBS = "wpl-libs-c1f41b3288";
const SHELL_FILES = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"], LIB_FILES = ["lang/eng-traineddata-gz.wasm", "lib/core/tesseract-core-lstm.wasm.js", "lib/core/tesseract-core-simd-lstm.wasm.js", "lib/ocr-worker.js", "lib/pdf.min.js", "lib/pdf.worker.min.js", "lib/tesseract.min.js", "lib/worker.min.js", "lib/zxing.min.js"];
self.addEventListener("install", e => e.waitUntil((async () => {
  await (await caches.open(SHELL)).addAll(SHELL_FILES.map(u => new Request(u, { cache: "reload" })));
  const lc = await caches.open(LIBS);
  for (const u of LIB_FILES) if (!(await lc.match(u))) await lc.add(new Request(u, { cache: "reload" }));
  await self.skipWaiting();
})()));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== SHELL && k !== LIBS).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});

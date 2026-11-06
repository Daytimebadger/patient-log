# Builds the installable offline version (../docs/, served by GitHub Pages) from index.html. Run from src/: python3 build-app.py
import shutil, os, hashlib, json
from PIL import Image, ImageDraw
src = open('index.html').read()
ver = hashlib.sha1(src.encode()).hexdigest()[:10]
head = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Patient Log">
<meta name="theme-color" content="#1f4fb8">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head><body>'''
tail = '''<script>if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(e => console.warn("offline cache not available", e)));</script>
</body></html>'''
os.makedirs('../docs', exist_ok=True)
open('../docs/index.html', 'w').write(head + src + tail)
for d in ['lib', 'lang']:
    if os.path.exists('../docs/' + d): shutil.rmtree('../docs/' + d)
    shutil.copytree(d, '../docs/' + d)
files = ['./', 'index.html', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png'] + \
  [os.path.join(r, f).replace('\\\\', '/') for d in ['lib', 'lang'] for r, _, fs in os.walk(d) for f in fs]
open('../docs/sw.js', 'w').write('''// Offline cache: after the first visit every file is served from the phone.
const CACHE = "wpl-%s";
const FILES = %s;
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});
''' % (ver, json.dumps(files)))
json.dump({"name": "Ward Patient Log", "short_name": "Patient Log", "start_url": "./", "scope": "./", "display": "standalone",
  "background_color": "#f3f5f8", "theme_color": "#1f4fb8",
  "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
  open('../docs/manifest.webmanifest', 'w'), indent=1)
def icon(n):
    im = Image.new('RGB', (n, n), (31, 79, 184)); d = ImageDraw.Draw(im); k = n / 512
    d.rounded_rectangle([150*k, 110*k, 362*k, 420*k], radius=24*k, fill=(255, 255, 255))
    d.rounded_rectangle([200*k, 84*k, 312*k, 140*k], radius=16*k, fill=(227, 234, 250), outline=(31, 79, 184), width=max(1, int(8*k)))
    for i, y in enumerate([200, 260, 320]):
        d.rounded_rectangle([190*k, y*k, (322 if i < 2 else 270)*k, (y+22)*k], radius=10*k, fill=(31, 79, 184))
    im.save('../docs/icon-%d.png' % n)
for n in (180, 192, 512): icon(n)
print('built ../docs/ version', ver, len(files), 'files')

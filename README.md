# Ward Patient Log

A phone-first patient list for the ward: photograph a hospital sticker to fill in the patient, record diagnosis, treatment, CT conclusions, labs and disposition, and produce one-page summaries and ward round handovers.

**Privacy:** all reading (barcode, text, PDF) and storage happens on the phone. Records are kept in the phone's browser storage and are never sent to a server. This repository holds only the app's code.

- `src/` – source (`index.html`) plus the bundled readers (Tesseract, pdf.js, ZXing) and English language data.
- `docs/` – the installable offline app served by GitHub Pages. Rebuild with `cd src && python3 build-app.py`.

Install: open the GitHub Pages link in Safari on the phone, then Share → Add to Home Screen.

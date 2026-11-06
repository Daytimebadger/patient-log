// Artifacts can't serve .gz files, so the English language data ships as a .wasm-named file.
// Redirect the OCR engine's language request to it, then start the stock Tesseract worker.
(function () {
  var realFetch = self.fetch.bind(self);
  self.fetch = function (url, opts) {
    var u = String(url && url.url ? url.url : url);
    if (/eng\.traineddata(\.gz)?$/.test(u)) u = u.replace(/eng\.traineddata(\.gz)?$/, "eng-traineddata-gz.wasm");
    return realFetch(u, opts);
  };
})();
importScripts("worker.min.js");

/* PrizeBond Check offline support. Pages: network first, so new draws show up. Everything else: cache first. */
const V="pbc-8606ce4b0a",OCR="pbc-ocr-1",CORE=["./", "index.html", "124th-prize-bond-draw-result.html", "123rd-prize-bond-draw-result.html", "122nd-prize-bond-draw-result.html", "121st-prize-bond-draw-result.html", "120th-prize-bond-draw-result.html", "119th-prize-bond-draw-result.html", "118th-prize-bond-draw-result.html", "117th-prize-bond-draw-result.html", "manifest.webmanifest", "vendor/xlsx.full.min.js", "icons/icon-192.png", "icons/icon-512.png", "icons/favicon-32.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V&&k!==OCR).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{
  const r=e.request;if(r.method!=="GET")return;
  const u=new URL(r.url);
  if(r.mode==="navigate"){
    e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res})
      .catch(()=>caches.match(r,{ignoreSearch:true}).then(m=>m||caches.match("./"))));return;
  }
  if(u.origin===location.origin&&u.pathname.includes("/vendor/ocr/")){
    e.respondWith(caches.open(OCR).then(c=>c.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok)c.put(r,res.clone());return res}))));return;
  }
  if(u.origin===location.origin||/fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)){
    e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok||res.type==="opaque"){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp))}return res})));
  }
});

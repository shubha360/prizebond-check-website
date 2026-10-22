"""Build PrizeBond Check from draws.json + template.html.

Usage:  python3 build.py
Outputs:
  site/      the complete website: drag this folder (or site.zip) onto app.netlify.com/drop
  site.zip   the same folder zipped
  artifact/  the version published as a Claude artifact

To add a new draw: add it to draws.json, bump NEXT_DRAW in template.html, run this again.
Set SITE_URL once you have a domain; it turns on canonical links and sitemap.xml.
"""
import datetime, hashlib, html, json, pathlib, re, shutil, sys, zipfile

SITE_URL = "https://checkprizebond.com"          # e.g. "https://prizebondcheck.com" (no trailing slash)
SITE_NAME = "PrizeBond Check"
SITE_NAME_BN = "প্রাইজবন্ড চেক"
REPO_URL = "https://github.com/shubha360/prizebond-check-website"   # public source code, linked from every page
ANALYTICS_TOKEN = "a5a9b171f69542cdb5b20b2a594d4f23"   # Cloudflare Web Analytics token (cookie-free visitor counter); empty = off

HERE = pathlib.Path(__file__).parent
TIERS = {"first": 1, "second": 1, "third": 2, "fourth": 2, "fifth": 40}
PRIZES = [("first", 600000, "1st prize"), ("second", 325000, "2nd prize"), ("third", 100000, "3rd prize"),
          ("fourth", 50000, "4th prize"), ("fifth", 10000, "5th prize")]
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
MONTHS_LONG = "January February March April May June July August September October November December".split()
BN_MONTHS = ["জানুয়ারি","ফেব্রুয়ারি","মার্চ","এপ্রিল","মে","জুন","জুলাই","আগস্ট","সেপ্টেম্বর","অক্টোবর","নভেম্বর","ডিসেম্বর"]
BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
TODAY = datetime.date.today()

def ordinal(n):
    v = n % 100
    return f"{n}{'th' if 10 <= v <= 20 else {1:'st',2:'nd',3:'rd'}.get(n % 10, 'th')}"
def slug(n): return f"{ordinal(n)}-prize-bond-draw-result.html"          # file name
def href(n, ext): return f"{ordinal(n)}-prize-bond-draw-result{ext}"     # link: clean on the live site, .html in the artifact preview
def pdate(s): return datetime.date.fromisoformat(s)
def fdate(d): return f"{d.day} {MONTHS[d.month-1]} {d.year}"
def fdate_long(d): return f"{d.day} {MONTHS_LONG[d.month-1]} {d.year}"
def fdate_bn(d): return f"{str(d.day).translate(BN)} {BN_MONTHS[d.month-1]} {str(d.year).translate(BN)}"
def money(a):
    s = str(a); head, tail = s[:-3], s[-3:]
    head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head)
    return "৳" + (head + "," if head else "") + tail
def e(s): return html.escape(str(s), quote=True)

# ---------------- data ----------------
draws = json.loads((HERE / "draws.json").read_text(encoding="utf-8"))
draws.sort(key=lambda d: -d["no"])
problems = []
for d in draws:
    seen = []
    for k, n in TIERS.items():
        nums = d.get(k, [])
        if len(nums) != n: problems.append(f"draw {d['no']}: {k} has {len(nums)} numbers, expected {n}")
        for x in nums:
            if not (len(x) == 7 and x.isdigit()): problems.append(f"draw {d['no']}: bad number {x!r}")
        seen += nums
    if len(set(seen)) != len(seen): problems.append(f"draw {d['no']}: duplicate numbers")
if problems:
    print("\n".join(problems)); sys.exit(1)
slim = [{"no": d["no"], "date": d["date"], **{k: sorted(d[k]) if k == "fifth" else d[k] for k in TIERS}} for d in draws]
DATA = json.dumps(slim, separators=(",", ":"))

# ---------------- template pieces ----------------
tpl = (HERE / "template.html").read_text(encoding="utf-8")
blocks = dict(re.findall(r"<!--BLOCK:(\w+)-->\n(.*?)<!--/BLOCK-->\n", tpl, flags=re.S))
tpl = re.sub(r"<!--BLOCK:\w+-->\n.*?<!--/BLOCK-->\n\n?", "", tpl, flags=re.S)

def claim_until(d):
    dl = pdate(d["date"]).replace(year=pdate(d["date"]).year + 2)
    return ("Claim period over" if dl < TODAY else f"Claimable until {fdate(dl)}"), dl

def static_board(d, page_draw, ext):
    txt, _ = claim_until(d)
    link = "" if d["no"] == page_draw else f' · <a href="{href(d["no"], ext)}">Result page</a>'
    h = f'<div class="board-meta"><span>{ordinal(d["no"])} draw · Held {fdate(pdate(d["date"]))}{link}</span><span>{txt}</span></div>\n'
    for k, amt, name in PRIZES:
        ns = d[k]
        each = f"<span>{len(ns)} numbers</span>" if len(ns) > 2 else ""
        h += (f'<div class="tier{" big" if amt >= 50000 else ""}"><div class="t">{name}<b>{money(amt)}</b>{each}</div>'
              f'<div class="nums">{" ".join(f"<span>{n}</span>" for n in ns)}</div></div>\n')
    return h

def links(page_draw, ext):
    out = []
    for d in slim:
        cur = ' aria-current="page"' if d["no"] == page_draw else ""
        out.append(f'      <li><a href="{href(d["no"], ext)}" data-no="{d["no"]}"{cur}>{bi("b", f"{ordinal(d['no'])} draw", f"{str(d['no']).translate(BN)}তম ড্র")}{bi("span", fdate(pdate(d["date"])), fdate_bn(pdate(d["date"])))}</a></li>')
    return "\n".join(out)

def bi(tag, en, bn, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-ien="{e(en)}" data-ibn="{e(bn)}">{e(en)}</{tag}>'

import guides
CTX = dict(slim=slim, ordinal=ordinal, fdate=fdate, fdate_bn=fdate_bn, pdate=pdate, href=href, money=money, bi=bi, e=e)
GUIDES = guides.build_guides(CTX)   # content pages: file, link text, titles, bodies (see guides.py)
def ghref(g, ext): return g["file"][:-5] + ext
def guidenav(current, ext):
    items = "\n".join(
        f'      <li><a href="{ghref(g, ext)}"{" aria-current=\"page\"" if g["file"] == current else ""}>'
        f'{bi("b", g["nav_en"], g["nav_bn"])}{bi("span", g["blurb_en"], g["blurb_bn"])}</a></li>' for g in GUIDES)
    return f'  <nav class="guides" aria-label="Guides">\n    <h2 data-i="guidesH">Prize bond guides</h2>\n    <ul>\n{items}\n    </ul>\n  </nav>'

FAQ = [
 ("When is the prize bond draw held?", "প্রাইজবন্ডের ড্র কবে হয়?",
  "Four times a year: on 31 January, 30 April, 31 July and 31 October. If that day is a holiday, the draw moves to the next working day.",
  "বছরে চারবার: ৩১ জানুয়ারি, ৩০ এপ্রিল, ৩১ জুলাই ও ৩১ অক্টোবর। ওই দিন ছুটি থাকলে পরের কর্মদিবসে ড্র হয়।"),
 ("Do I need the series letters to check my bond?", "বন্ড মেলাতে কি সিরিজ লাগবে?",
  "No. Bangladesh Bank uses a single common draw, so the same 46 winning numbers apply to every series (কক, কখ and so on). Only the 7-digit number matters.",
  "না। বাংলাদেশ ব্যাংক সিঙ্গেল কমন ড্র পদ্ধতিতে ড্র করে, তাই সব সিরিজে (কক, কখ ইত্যাদি) একই ৪৬টি বিজয়ী নম্বর। শুধু ৭ অঙ্কের নম্বর মেলালেই হবে।"),
 ("How much is each prize?", "কোন পুরস্কার কত টাকার?",
  "Each draw has 46 prizes per series: 1st ৳6,00,000, 2nd ৳3,25,000, two 3rd prizes of ৳1,00,000, two 4th prizes of ৳50,000 and forty 5th prizes of ৳10,000. 20% tax is deducted at source.",
  "প্রতি সিরিজে ৪৬টি পুরস্কার: ১ম ৬,০০,০০০ টাকা, ২য় ৩,২৫,০০০ টাকা, ১ লাখ টাকার ২টি ৩য় পুরস্কার, ৫০ হাজার টাকার ২টি ৪র্থ পুরস্কার এবং ১০ হাজার টাকার ৪০টি ৫ম পুরস্কার। উৎসে ২০% কর কাটা হয়।"),
 ("How long can I claim a prize?", "কত দিনের মধ্যে পুরস্কার দাবি করতে হয়?",
  "Within 2 years of the draw date. That's why this site checks the last 8 draws.",
  "ড্রয়ের তারিখ থেকে ২ বছরের মধ্যে। তাই এই সাইট সর্বশেষ ৮টি ড্রয়ের সাথে মিলিয়ে দেখে।"),
 ("Which bonds take part in a draw?", "কোন বন্ডগুলো ড্রয়ে অংশ নেয়?",
  "Every bond sold at least 2 months before the draw date. A bond keeps taking part in every draw after that.",
  "ড্রয়ের তারিখের অন্তত ২ মাস আগে বিক্রি হওয়া সব বন্ড। এরপর থেকে প্রতিটি ড্রয়ে বন্ডটি অংশ নেয়।"),
 ("Is it safe to enter my bond numbers here?", "এখানে বন্ড নম্বর দেওয়া কি নিরাপদ?",
  "Yes. Your numbers are checked inside your own browser and saved only on your device; Clear removes them. They are never sent to any server, so this site has no list of who holds which bond, and nobody can get one from us. The code is public on GitHub for anyone to check.",
  "হ্যাঁ। নম্বরগুলো আপনার ব্রাউজারেই মেলানো হয় এবং শুধু আপনার ডিভাইসে সংরক্ষিত থাকে; মুছুন চাপলে মুছে যায়। কোনো সার্ভারে কখনো পাঠানো হয় না, তাই কার কাছে কোন বন্ড আছে তার কোনো তালিকা এই সাইটের কাছে নেই, আমাদের কাছ থেকে কেউ তা পেতেও পারে না। যে কেউ যাচাই করতে পারেন, কোড GitHub-এ উন্মুক্ত।"),
 ("Someone called offering to buy my winning bond. What should I do?", "কেউ ফোন করে আমার পুরস্কারপ্রাপ্ত বন্ড কিনতে চাইছে। কী করব?",
  "Say no, and don't hand over the bond. Claim the prize yourself at Bangladesh Bank or where you bought the bond; it's your money. This site never contacts anyone and doesn't know who won, so such calls don't come from us.",
  "রাজি হবেন না, বন্ড কাউকে দেবেন না। বাংলাদেশ ব্যাংকে বা যেখান থেকে বন্ড কিনেছেন সেখানে নিজেই পুরস্কার দাবি করুন; টাকাটা আপনার। এই সাইট কারো সাথে যোগাযোগ করে না এবং কে জিতেছে তা জানেও না, তাই এমন ফোন আমাদের কাছ থেকে আসে না।"),
]
def faq_html():
    items = "\n".join(f"      <div>{bi('dt', q, qb)}{bi('dd', a, ab)}</div>" for q, qb, a, ab in FAQ)
    return f'  <section class="faq">\n    <h2 data-i="faqH">Prize bond questions</h2>\n    <dl>\n{items}\n    </dl>\n  </section>'

def jsonld(obj): return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'

def head(title, desc, path, extra_ld=(), artifact=False):
    h = [f"<title>{e(title)}</title>", f'<meta name="description" content="{e(desc)}">']
    if artifact: return "\n".join(h)
    url = f"{SITE_URL}/{path}" if SITE_URL else ""
    if url: h.append(f'<link rel="canonical" href="{url}">')
    h += [f'<meta property="og:title" content="{e(title)}">', f'<meta property="og:description" content="{e(desc)}">',
          '<meta property="og:type" content="website">', f'<meta property="og:site_name" content="{SITE_NAME}">',
          '<meta name="theme-color" content="#0b6b4f">', '<link rel="manifest" href="manifest.webmanifest">',
          '<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">',
          '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">']
    if url: h += [f'<meta property="og:url" content="{url}">', f'<meta property="og:image" content="{SITE_URL}/icons/icon-512.png">']
    h += [jsonld(x) for x in extra_ld]
    return "\n".join(h)

def page(intro, order, page_draw, board_draw, faq, head_html, home, ext="", current=None, artifact=False, extra_blocks=None):
    s = tpl.replace("<!--HEAD-->", head_html)
    s = s.replace("<!--SECTION:guidenav-->", guidenav(current, ext))
    s = s.replace("<!--SECTION:analytics-->", "" if artifact or not ANALYTICS_TOKEN else
        f"<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" data-cf-beacon='{{\"token\": \"{ANALYTICS_TOKEN}\"}}'></script>")
    s = s.replace("<!--SECTION:intro-->", intro)
    s = s.replace("<!--SECTION:order-->", "\n".join((extra_blocks or {}).get(b) or blocks[b] for b in order))
    s = s.replace("<!--SECTION:board-->", static_board(board_draw, page_draw, ext))
    s = s.replace("<!--SECTION:links-->", links(page_draw, ext))
    s = s.replace("<!--SECTION:faq-->", faq)
    s = s.replace("/*__DRAWS__*/[]", DATA)
    s = s.replace("__EXT__", ext).replace("__REPO__", REPO_URL)
    s = s.replace("/*__PAGE__*/{draw:null,ext:\"\"}", json.dumps({"draw": page_draw, "home": home, "ext": ext}))
    assert "<!--" not in s.replace("<!--HEAD-->", ""), "unfilled placeholder"
    return s

def standalone(body):
    head_part, rest = body.split("</style>", 1)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
            + head_part + "</style>\n</head>\n<body>\n" + rest + "\n</body>\n</html>\n")

# ---------------- pages ----------------
latest = slim[0]
first_year, last_year = slim[-1]["date"][:4], latest["date"][:4]
HOME_TITLE = f"Prize Bond Result Check {last_year}: All Draws, Free | প্রাইজবন্ড ড্র ফলাফল"
HOME_DESC = (f"Check all your Bangladesh 100 Taka prize bonds free against the last {len(slim)} Bangladesh Bank draws "
             f"({ordinal(slim[-1]['no'])} to {ordinal(latest['no'])}). Bulk check, Excel upload, camera scan. "
             f"প্রাইজবন্ড ড্র ফলাফল {last_year.translate(BN)} বিনামূল্যে মিলিয়ে দেখুন।")
home_intro = f'''  <section class="intro">
    <span class="free" data-i="free">Free · no sign-up · no ads</span>
    <h1 data-i="h1">Prize bond result check: all your bonds in one go</h1>
    {bi("p", f"প্রাইজবন্ড ড্র ফলাফল {last_year.translate(BN)}: সব বন্ড বিনামূল্যে মিলিয়ে দেখুন", f"Prize bond draw result {last_year}: check all your bonds free", "sub")}
    <p class="lede" data-i="lede">Paste every 100 Taka bond you own, upload your Excel sheet, or scan the bonds with your camera. We check them against the last 8 Bangladesh Bank draws, the ones you can still claim.</p>
  </section>'''
home_ld = [
  {"@context": "https://schema.org", "@type": "WebApplication", "name": SITE_NAME, "alternateName": SITE_NAME_BN,
   "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "inLanguage": ["en", "bn"],
   "description": HOME_DESC, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BDT"},
   **({"url": SITE_URL + "/"} if SITE_URL else {})},
  {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, _, a, _ in FAQ]},
]
pages = {}   # filename -> page body
art_pages = {}
home_args = (home_intro, ["checker", "claim", "ledger"], None, latest, faq_html())
pages["index.html"] = page(*home_args, head(HOME_TITLE, HOME_DESC, "", home_ld), True)
artifact_home = page(*home_args, head(SITE_NAME, HOME_DESC, "", artifact=True), True, ".html", artifact=True)

for d in slim:
    n, dt = d["no"], pdate(d["date"])
    nb = str(n).translate(BN)
    title = f"{ordinal(n)} Prize Bond Draw Result {dt.year}: Full List | {nb}তম প্রাইজবন্ড ড্র ফলাফল"
    desc = (f"{ordinal(n)} prize bond draw result ({fdate_long(dt)}): 1st prize {d['first'][0]}, 2nd prize {d['second'][0]}. "
            f"All 46 winning numbers of the Bangladesh Bank 100 Taka prize bond, with a free checker. "
            f"{nb}তম প্রাইজবন্ড ড্রয়ের সব বিজয়ী নম্বর।")
    lede = (f"The {ordinal(n)} draw of the Bangladesh Bank 100 Taka prize bond was held on {fdate(dt)}. The first prize of ৳6,00,000 "
            f"went to bond number {d['first'][0]}. Below are all 46 winning numbers, and a free checker for all your bonds.")
    intro = f'''  <section class="intro">
    <a class="crumb" href="./" data-i="crumb">All draw results</a>
    <h1 id="dh1">{ordinal(n)} Prize Bond Draw Result {dt.year}</h1>
    {bi("p", f"{nb}তম প্রাইজবন্ড ড্র ফলাফল {str(dt.year).translate(BN)} · {fdate_bn(dt)}", f"{ordinal(n)} prize bond draw result {dt.year} · {fdate(dt)}", "sub")}
    <p class="lede" id="dlede">{e(lede)}</p>
  </section>'''
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "inLanguage": ["en", "bn"],
           "datePublished": d["date"], **({"url": f"{SITE_URL}/{href(n, '')}"} if SITE_URL else {})}]
    pages[slug(n)] = page(intro, ["ledger", "checker", "claim"], n, d, "", head(title, desc, href(n, ""), ld), False)
    art_pages[slug(n)] = page(intro, ["ledger", "checker", "claim"], n, d, "", head(title, desc, href(n, ""), artifact=True), False, ".html", artifact=True)

# ---------------- guide pages ----------------
GUIDE_JS = """<script>
/* guide pages: language switch, install button and offline support only */
(function(){
const BN_D="০১২৩৪৫৬৭৮৯",$=id=>document.getElementById(id);
const T={en:{brand:"PrizeBond Check",install:"Install app",linksH:"All prize bond draw results",guidesH:"Prize bond guides",crumb:"Prize bond checker",
  foot1:"Results compiled from Bangladesh Bank announcements and national newspapers. Always confirm a win with Bangladesh Bank before you travel to claim it.",
  foot2:"PrizeBond Check is free and not affiliated with Bangladesh Bank.",iosTip:"On iPhone: tap Share, then \u201cAdd to Home Screen\u201d to install this as an app."},
 bn:{brand:"প্রাইজবন্ড চেক",install:"অ্যাপ ইনস্টল করুন",linksH:"সব প্রাইজবন্ড ড্রয়ের ফলাফল",guidesH:"প্রাইজবন্ড গাইড",crumb:"প্রাইজবন্ড চেকার",
  foot1:"ফলাফল বাংলাদেশ ব্যাংকের ঘোষণা ও জাতীয় দৈনিক থেকে সংকলিত। পুরস্কার দাবি করতে যাওয়ার আগে বাংলাদেশ ব্যাংকে নিশ্চিত হয়ে নিন।",
  foot2:"প্রাইজবন্ড চেক বিনামূল্যে এবং বাংলাদেশ ব্যাংকের সাথে সম্পর্কিত নয়।",iosTip:"আইফোনে: Share চাপুন, তারপর \u201cAdd to Home Screen\u201d চাপলে অ্যাপ হিসেবে যোগ হবে।"}};
let lang="en";try{const l=localStorage.getItem("pb-lang");if(l==="bn"||l==="en")lang=l}catch(e){}
function apply(){
  document.documentElement.lang=lang;
  document.querySelectorAll("[data-i]").forEach(el=>{const v=T[lang][el.dataset.i];if(typeof v==="string")el.textContent=v});
  document.querySelectorAll("[data-ibn]").forEach(el=>{el.textContent=lang==="bn"?el.dataset.ibn:el.dataset.ien});
  $("lang-en").setAttribute("aria-pressed",lang==="en");$("lang-bn").setAttribute("aria-pressed",lang==="bn");
  document.dispatchEvent(new CustomEvent("pb-lang",{detail:lang}));
}
window.pbLang=()=>lang;window.pbBn=x=>String(x).replace(/\\d/g,d=>BN_D[d]);
$("lang-en").onclick=()=>{lang="en";try{localStorage.setItem("pb-lang","en")}catch(e){}apply()};
$("lang-bn").onclick=()=>{lang="bn";try{localStorage.setItem("pb-lang","bn")}catch(e){}apply()};
let ev=null;const sa=matchMedia("(display-mode: standalone)").matches||navigator.standalone;
if("serviceWorker" in navigator&&location.protocol==="https:"&&!/claude|anthropic/.test(location.hostname)){
  navigator.serviceWorker.register("sw.js").then(()=>{if(!sa&&/iphone|ipad|ipod/i.test(navigator.userAgent))$("iosTip").hidden=false}).catch(()=>{});
}
addEventListener("beforeinstallprompt",e=>{e.preventDefault();ev=e;$("installBtn").hidden=false});
$("installBtn").onclick=async()=>{if(!ev)return;ev.prompt();try{await ev.userChoice}catch(e){}ev=null;$("installBtn").hidden=true};
apply();
})();
</script>"""

def guide_page(g, ext, artifact):
    intro = f'''  <section class="intro">
    <a class="crumb" href="./" data-i="crumb">Prize bond checker</a>
    {bi("h1", g["h1_en"], g["h1_bn"])}
    {bi("p", g["sub_en"], g["sub_bn"], "sub")}
  </section>'''
    body = g["body"](ext, CTX) if callable(g["body"]) else g["body"]
    article = f'  <article class="guide">\n{body}\n  </article>'
    cta = (f'  <aside class="cta">{bi("p", "Have prize bonds? Check all of them against the last 8 draws in one go.", "প্রাইজবন্ড আছে? সর্বশেষ ৮টি ড্রয়ের সাথে সব একসাথে মিলিয়ে নিন।")}'
           f'<a class="btn" href="./">{bi("span", "Check my bonds", "বন্ড মিলিয়ে দেখুন")}</a></aside>')
    ld = [] if artifact else [{"@context": "https://schema.org", "@type": "WebPage", "name": g["title"], "description": g["desc"],
          "inLanguage": ["en", "bn"], **({"url": f"{SITE_URL}/{ghref(g, '')}"} if SITE_URL else {})}] + g.get("ld", [])
    hd = head(g["title"], g["desc"], ghref(g, ""), ld, artifact=artifact)
    s = page(intro, ["article", "cta"], None, latest, "", hd, False, ext, current=g["file"], artifact=artifact,
             extra_blocks={"article": article, "cta": cta})
    i = s.index("<script>\nconst DRAWS")
    j = s.index("</script>", i) + len("</script>")
    return s[:i] + GUIDE_JS + g.get("script", "") + s[j:]

for g in GUIDES:
    pages[g["file"]] = guide_page(g, "", False)
    art_pages[g["file"]] = guide_page(g, ".html", True)

# ---------------- write site/ ----------------
SITE = HERE / "site"
if SITE.exists(): shutil.rmtree(SITE)
(SITE / "icons").mkdir(parents=True); (SITE / "vendor" / "ocr").mkdir(parents=True)
for name, body in pages.items():
    (SITE / name).write_text(standalone(body), encoding="utf-8")

VENDOR = [   # third-party scripts kept in vendor/ (Excel reader: SheetJS 0.18.5, number reader: tesseract.js 6.0.1)
  "vendor/xlsx.full.min.js", "vendor/ocr/tesseract.min.js", "vendor/ocr/worker.min.js",
  "vendor/ocr/tesseract-core-lstm.wasm.js", "vendor/ocr/tesseract-core-simd-lstm.wasm.js",
  "vendor/ocr/eng.traineddata.gz", "vendor/ocr/ben.traineddata.gz",
]
for rel in VENDOR:
    keep = HERE / rel
    if rel.endswith(".js"):
        # raw control bytes inside string literals -> \xNN escapes (same meaning, publishable as text)
        b = re.sub(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", lambda m: b"\\x%02x" % m.group()[0], keep.read_bytes())
        b = b.decode("utf-8").replace("\ufffd", "\\ufffd").encode("utf-8")   # literal U+FFFD in codepage tables -> escape
        (SITE / rel).write_bytes(b)
    elif rel.endswith(".gz"):
        import base64
        rel_txt = rel[:-3] + ".b64.txt"
        (SITE / rel_txt).write_bytes(base64.b64encode(keep.read_bytes()))
    else:
        shutil.copy(keep, SITE / rel)

# icons
from PIL import Image, ImageDraw, ImageFont
FONT = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
def icon(size, maskable=False, path=None):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0) if not maskable else (11, 107, 79, 255))
    g = ImageDraw.Draw(im)
    if not maskable:
        g.ellipse([0, 0, size - 1, size - 1], fill=(11, 107, 79, 255))
    pad = size * (0.20 if maskable else 0.10)
    g.ellipse([pad, pad, size - pad, size - pad], outline=(251, 252, 248, 255), width=max(2, size // 40))
    ft = ImageFont.truetype(FONT, int(size * (0.42 if maskable else 0.52)))
    g.text((size / 2, size / 2), "৳", font=ft, fill=(251, 252, 248, 255), anchor="mm")
    im.save(path)
icon(512, path=SITE / "icons/icon-512.png"); icon(192, path=SITE / "icons/icon-192.png")
icon(512, True, SITE / "icons/maskable-512.png"); icon(180, True, SITE / "icons/apple-touch-icon.png")
icon(32, path=SITE / "icons/favicon-32.png")

manifest = {"name": f"{SITE_NAME} · {SITE_NAME_BN}", "short_name": SITE_NAME, "start_url": "./", "scope": "./",
            "display": "standalone", "background_color": "#f3f5ef", "theme_color": "#0b6b4f", "lang": "en",
            "description": "Check all your Bangladesh prize bonds against the latest draws.",
            "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                      {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                      {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
(SITE / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

core = ["./", *[href(d["no"], "") for d in slim], *[ghref(g, "") for g in GUIDES], "manifest.webmanifest", "vendor/xlsx.full.min.js",
        "icons/icon-192.png", "icons/icon-512.png", "icons/favicon-32.png"]
version = hashlib.sha1("".join(pages.values()).encode()).hexdigest()[:10]
sw = f"""/* PrizeBond Check offline support. Pages: network first, so new draws show up. Everything else: cache first. */
const V="pbc-{version}",OCR="pbc-ocr-1",CORE={json.dumps(core)};
self.addEventListener("install",e=>{{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V&&k!==OCR).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener("fetch",e=>{{
  const r=e.request;if(r.method!=="GET")return;
  const u=new URL(r.url);
  if(r.mode==="navigate"){{
    e.respondWith(fetch(r).then(res=>{{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res}})
      .catch(()=>caches.match(r,{{ignoreSearch:true}}).then(m=>m||caches.match("./"))));return;
  }}
  if(u.origin===location.origin&&u.pathname.includes("/vendor/ocr/")){{
    e.respondWith(caches.open(OCR).then(c=>c.match(r).then(m=>m||fetch(r).then(res=>{{if(res.ok)c.put(r,res.clone());return res}}))));return;
  }}
  if(u.origin===location.origin||/fonts\\.(googleapis|gstatic)\\.com$/.test(u.hostname)){{
    e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{{if(res.ok||res.type==="opaque"){{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp))}}return res}})));
  }}
}});
"""
(SITE / "sw.js").write_text(sw, encoding="utf-8")
notfound = page('''  <section class="intro">
    <h1>Page not found</h1>
    <p class="sub" data-ien="This page doesn't exist" data-ibn="এই পাতাটি নেই">This page doesn't exist</p>
    <p class="lede"><a href="./">Go to the prize bond checker</a> to check your bonds against all recent draws.</p>
  </section>''', ["checker"], None, latest, "", "<title>Page not found · PrizeBond Check</title>\n<meta name=\"robots\" content=\"noindex\">", False)
(SITE / "404.html").write_text(standalone(notfound), encoding="utf-8")
robots = "User-agent: *\nAllow: /\n" + (f"Sitemap: {SITE_URL}/sitemap.xml\n" if SITE_URL else "")
(SITE / "robots.txt").write_text(robots, encoding="utf-8")
if SITE_URL:
    urls = [("", latest["date"])] + [(ghref(g, ""), g["updated"]) for g in GUIDES] + [(href(d["no"], ""), d["date"]) for d in slim]
    sm = "".join(f"<url><loc>{SITE_URL}/{p}</loc><lastmod>{m}</lastmod></url>" for p, m in urls)
    (SITE / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>', encoding="utf-8")

zp = HERE / "site.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(SITE.rglob("*")):
        if f.is_file(): z.write(f, f.relative_to(SITE))

# ---------------- artifact/ ----------------
ART = HERE / "artifact"
if ART.exists(): shutil.rmtree(ART)
ART.mkdir()
(ART / "index.html").write_text(artifact_home, encoding="utf-8")
art_files = {}
for name, body in art_pages.items():
    (ART / name).write_text(standalone(body), encoding="utf-8")
    art_files[name] = name
for rel in VENDOR:
    if rel.endswith(".gz"): rel = rel[:-3] + ".b64.txt"
    (ART / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy(SITE / rel, ART / rel); art_files[rel] = rel
(ART / "files.json").write_text(json.dumps(art_files, indent=1))
print(f"built {len(slim)} draws, {len(pages)} pages, site.zip {zp.stat().st_size//1024} KB")

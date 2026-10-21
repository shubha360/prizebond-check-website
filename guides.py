"""Guide pages for PrizeBond Check (English + Bangla).

Each guide is a dict:
  file        output file name (the live address drops ".html")
  nav_en/bn   short link text; blurb_en/bn one-line description under it
  title/desc  <title> and meta description (for Google)
  h1_en/bn, sub_en/bn   page heading and sub-heading
  body(ext, c)  returns the article HTML; c gives draw data and helpers from build.py
  updated     date for sitemap.xml
  script      optional extra <script> for the page (e.g. a calculator)

Body text is written twice: <div class="l-en" lang="en"> and <div class="l-bn" lang="bn">.
The page shows the one matching the language switch.
"""
import datetime

BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKDAYS_BN = ["সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার", "রবিবার"]
SCHEDULE = [(1, 31), (4, 30), (7, 31), (10, 31)]   # scheduled draw days


def b(x):
    return str(x).translate(BN)


def bn_ord(n):
    return f"{b(n)}তম"


def next_scheduled(after):
    """Scheduled draw dates strictly after `after`, forever."""
    y = after.year
    while True:
        for m, d in SCHEDULE:
            dt = datetime.date(y, m, d)
            if dt > after:
                yield dt
        y += 1


# ---------------------------------------------------------------- schedule
def schedule_body(ext, c):
    slim, latest = c["slim"], c["slim"][0]
    gen = next_scheduled(c["pdate"](latest["date"]))
    upcoming = [(latest["no"] + i + 1, next(gen)) for i in range(4)]

    def up_rows(bn):
        rows = []
        for n, dt in upcoming:
            wk = dt.weekday()
            weekend = wk in (4, 5)
            if bn:
                note = "সাপ্তাহিক ছুটির দিন, তাই সম্ভবত পরের কর্মদিবসে" if weekend else ""
                rows.append(f'<tr><td>{bn_ord(n)} ড্র</td><td class="n">{c["fdate_bn"](dt)}</td><td>{WEEKDAYS_BN[wk]}</td><td>{note}</td></tr>')
            else:
                note = "Weekend, so likely the next working day" if weekend else ""
                rows.append(f'<tr><td>{c["ordinal"](n)} draw</td><td class="n">{c["fdate"](dt)}</td><td>{WEEKDAYS[wk]}</td><td>{note}</td></tr>')
        return "\n".join(rows)

    def past_rows(bn):
        rows = []
        for d in slim:
            dt = c["pdate"](d["date"])
            dl = dt.replace(year=dt.year + 2)
            link = c["href"](d["no"], ext)
            if bn:
                rows.append(f'<tr><td><a href="{link}">{bn_ord(d["no"])} ড্র</a></td><td class="n">{c["fdate_bn"](dt)}</td>'
                            f'<td class="n">{b(d["first"][0])}</td><td class="n">{c["fdate_bn"](dl)}</td></tr>')
            else:
                rows.append(f'<tr><td><a href="{link}">{c["ordinal"](d["no"])} draw</a></td><td class="n">{c["fdate"](dt)}</td>'
                            f'<td class="n">{d["first"][0]}</td><td class="n">{c["fdate"](dl)}</td></tr>')
        return "\n".join(rows)

    prizes_en = """<tr><td>1st prize</td><td class="n">৳6,00,000</td><td class="n">1</td></tr>
<tr><td>2nd prize</td><td class="n">৳3,25,000</td><td class="n">1</td></tr>
<tr><td>3rd prize</td><td class="n">৳1,00,000</td><td class="n">2</td></tr>
<tr><td>4th prize</td><td class="n">৳50,000</td><td class="n">2</td></tr>
<tr><td>5th prize</td><td class="n">৳10,000</td><td class="n">40</td></tr>"""
    prizes_bn = """<tr><td>১ম পুরস্কার</td><td class="n">৳৬,০০,০০০</td><td class="n">১</td></tr>
<tr><td>২য় পুরস্কার</td><td class="n">৳৩,২৫,০০০</td><td class="n">১</td></tr>
<tr><td>৩য় পুরস্কার</td><td class="n">৳১,০০,০০০</td><td class="n">২</td></tr>
<tr><td>৪র্থ পুরস্কার</td><td class="n">৳৫০,০০০</td><td class="n">২</td></tr>
<tr><td>৫ম পুরস্কার</td><td class="n">৳১০,০০০</td><td class="n">৪০</td></tr>"""

    return f"""<div class="l-en" lang="en">
<p>Bangladesh Bank holds the 100 Taka prize bond draw four times a year: on <b>31 January, 30 April, 31 July and 31 October</b>. When that date falls on the weekend (Friday or Saturday) or a public holiday, the draw is held on the next working day. For example, the 124th draw, scheduled for Friday 31 July 2026, was held on Sunday 2 August.</p>
<h2>Upcoming draws</h2>
<div class="tbl"><table><thead><tr><th>Draw</th><th>Scheduled date</th><th>Day</th><th>Note</th></tr></thead><tbody>
{up_rows(False)}
</tbody></table></div>
<p>Results come out on the day of the draw. PrizeBond Check adds the winning numbers the same evening, after checking them against two sources.</p>
<h2>Prizes in every draw</h2>
<p>Each draw picks 46 winning numbers. Bangladesh Bank uses a single common draw, so the same numbers win in every series (কক, কখ and so on).</p>
<div class="tbl"><table><thead><tr><th>Prize</th><th>Amount</th><th>Winning numbers</th></tr></thead><tbody>
{prizes_en}
</tbody></table></div>
<p class="src">Tax is deducted from the prize at source. Every bond takes part in every draw held at least 60 days after it was bought.</p>
<h2>Recent draws</h2>
<p>Prizes can be claimed for 2 years after the draw date, so these are the draws you can still win from.</p>
<div class="tbl"><table><thead><tr><th>Draw</th><th>Held</th><th>1st prize number</th><th>Claim by</th></tr></thead><tbody>
{past_rows(False)}
</tbody></table></div>
</div>
<div class="l-bn" lang="bn">
<p>বাংলাদেশ ব্যাংক বছরে চারবার ১০০ টাকার প্রাইজবন্ডের ড্র করে: <b>৩১ জানুয়ারি, ৩০ এপ্রিল, ৩১ জুলাই ও ৩১ অক্টোবর</b>। ওই তারিখ সাপ্তাহিক ছুটির দিন (শুক্র বা শনিবার) বা সরকারি ছুটির দিনে পড়লে পরের কর্মদিবসে ড্র হয়। যেমন, শুক্রবার ৩১ জুলাই ২০২৬-এর ১২৪তম ড্র অনুষ্ঠিত হয় রবিবার ২ আগস্ট।</p>
<h2>আসন্ন ড্র</h2>
<div class="tbl"><table><thead><tr><th>ড্র</th><th>নির্ধারিত তারিখ</th><th>বার</th><th>মন্তব্য</th></tr></thead><tbody>
{up_rows(True)}
</tbody></table></div>
<p>ড্রয়ের দিনই ফলাফল প্রকাশ হয়। প্রাইজবন্ড চেক দুটি উৎসের সাথে মিলিয়ে সেদিন সন্ধ্যাতেই বিজয়ী নম্বর যোগ করে।</p>
<h2>প্রতিটি ড্রয়ের পুরস্কার</h2>
<p>প্রতিটি ড্রয়ে ৪৬টি বিজয়ী নম্বর বাছাই হয়। বাংলাদেশ ব্যাংক সিঙ্গেল কমন ড্র পদ্ধতিতে ড্র করে, তাই সব সিরিজে (কক, কখ ইত্যাদি) একই নম্বর পুরস্কার পায়।</p>
<div class="tbl"><table><thead><tr><th>পুরস্কার</th><th>পরিমাণ</th><th>বিজয়ী নম্বর</th></tr></thead><tbody>
{prizes_bn}
</tbody></table></div>
<p class="src">পুরস্কারের অর্থ থেকে উৎসে কর কাটা হয়। কেনার অন্তত ৬০ দিন পরের প্রতিটি ড্রয়ে বন্ড অংশ নেয়।</p>
<h2>সাম্প্রতিক ড্র</h2>
<p>ড্রয়ের তারিখ থেকে ২ বছর পর্যন্ত পুরস্কার দাবি করা যায়, তাই এই ড্রগুলোতে এখনো পুরস্কার পেতে পারেন।</p>
<div class="tbl"><table><thead><tr><th>ড্র</th><th>অনুষ্ঠিত</th><th>১ম পুরস্কারের নম্বর</th><th>দাবির শেষ তারিখ</th></tr></thead><tbody>
{past_rows(True)}
</tbody></table></div>
</div>"""


def schedule_guide(c):
    latest = c["slim"][0]
    nxt = next(next_scheduled(c["pdate"](latest["date"])))
    year = nxt.year
    return {
        "file": "prize-bond-draw-schedule.html",
        "nav_en": "Draw schedule", "nav_bn": "ড্রয়ের সময়সূচি",
        "blurb_en": "Upcoming draw dates and prizes", "blurb_bn": "আসন্ন ড্রয়ের তারিখ ও পুরস্কার",
        "title": f"Prize Bond Draw Schedule {year}: Dates & Prizes | প্রাইজবন্ড ড্রয়ের তারিখ",
        "desc": (f"When is the next prize bond draw? Bangladesh Bank 100 Taka prize bond draw dates for {year}, "
                 f"the prize for each of the 46 winning numbers, and recent results. প্রাইজবন্ড ড্রয়ের তারিখ {b(year)}।"),
        "h1_en": f"Prize bond draw schedule {year}", "h1_bn": f"প্রাইজবন্ড ড্রয়ের সময়সূচি {b(year)}",
        "sub_en": f"Next: {c['ordinal'](latest['no'] + 1)} draw, scheduled {c['fdate'](nxt)}",
        "sub_bn": f"পরবর্তী: {bn_ord(latest['no'] + 1)} ড্র, নির্ধারিত {c['fdate_bn'](nxt)}",
        "body": schedule_body,
        "updated": latest["date"],
    }


def build_guides(c):
    """Called by build.py with draw data and helpers; returns the list of guide pages."""
    return [schedule_guide(c)]

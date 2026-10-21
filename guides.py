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
<p>The 100 Taka prize bond draw is held four times a year, at the Dhaka Divisional Commissioner's office, and Bangladesh Bank publishes the results. The draws are scheduled for <b>31 January, 30 April, 31 July and 31 October</b>. When that date falls on the weekend (Friday or Saturday) or a public holiday, the draw is held on the next working day. For example, the 124th draw, scheduled for Friday 31 July 2026, was held on Sunday 2 August.</p>
<h2>Upcoming draws</h2>
<div class="tbl"><table><thead><tr><th>Draw</th><th>Scheduled date</th><th>Day</th><th>Note</th></tr></thead><tbody>
{up_rows(False)}
</tbody></table></div>
<p>Results are usually announced on the day of the draw and printed in national newspapers the next day. PrizeBond Check adds the winning numbers as soon as two sources agree, usually the same evening.</p>
<h2>Prizes in every draw</h2>
<p>Each draw picks 46 winning numbers. It is a single common draw, so the same numbers win in every series (কক, কখ and so on).</p>
<div class="tbl"><table><thead><tr><th>Prize</th><th>Amount</th><th>Winning numbers</th></tr></thead><tbody>
{prizes_en}
</tbody></table></div>
<p class="src">Tax is deducted from the prize at source. A bond takes part in every draw held at least 2 months after the sale date written on it.</p>
<h2>Recent draws</h2>
<p>Prizes can be claimed for 2 years after the draw date, so these are the draws you can still win from.</p>
<div class="tbl"><table><thead><tr><th>Draw</th><th>Held</th><th>1st prize number</th><th>Claim by</th></tr></thead><tbody>
{past_rows(False)}
</tbody></table></div>
</div>
<div class="l-bn" lang="bn">
<p>১০০ টাকার প্রাইজবন্ডের ড্র বছরে চারবার ঢাকার বিভাগীয় কমিশনারের কার্যালয়ে অনুষ্ঠিত হয়, আর বাংলাদেশ ব্যাংক ফলাফল প্রকাশ করে। ড্রয়ের নির্ধারিত তারিখ <b>৩১ জানুয়ারি, ৩০ এপ্রিল, ৩১ জুলাই ও ৩১ অক্টোবর</b>। ওই তারিখ সাপ্তাহিক ছুটির দিন (শুক্র বা শনিবার) বা সরকারি ছুটির দিনে পড়লে পরের কর্মদিবসে ড্র হয়। যেমন, শুক্রবার ৩১ জুলাই ২০২৬-এর ১২৪তম ড্র অনুষ্ঠিত হয় রবিবার ২ আগস্ট।</p>
<h2>আসন্ন ড্র</h2>
<div class="tbl"><table><thead><tr><th>ড্র</th><th>নির্ধারিত তারিখ</th><th>বার</th><th>মন্তব্য</th></tr></thead><tbody>
{up_rows(True)}
</tbody></table></div>
<p>সাধারণত ড্রয়ের দিনই ফলাফল ঘোষণা হয় এবং পরদিন জাতীয় দৈনিকে ছাপা হয়। দুটি উৎস মিলে গেলেই প্রাইজবন্ড চেক বিজয়ী নম্বর যোগ করে, সাধারণত সেদিন সন্ধ্যাতেই।</p>
<h2>প্রতিটি ড্রয়ের পুরস্কার</h2>
<p>প্রতিটি ড্রয়ে ৪৬টি বিজয়ী নম্বর বাছাই হয়। ড্র হয় সিঙ্গেল কমন ড্র পদ্ধতিতে, তাই সব সিরিজে (কক, কখ ইত্যাদি) একই নম্বর পুরস্কার পায়।</p>
<div class="tbl"><table><thead><tr><th>পুরস্কার</th><th>পরিমাণ</th><th>বিজয়ী নম্বর</th></tr></thead><tbody>
{prizes_bn}
</tbody></table></div>
<p class="src">পুরস্কারের অর্থ থেকে উৎসে কর কাটা হয়। বন্ডে লেখা বিক্রির তারিখ থেকে অন্তত ২ মাস পরের প্রতিটি ড্রয়ে বন্ড অংশ নেয়।</p>
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


# ---------------------------------------------------------------- claim
CLAIM_FORM = "https://www.bb.org.bd/services/forms/pbond_claimform.pdf"
DAMAGED_FORM = "https://www.bb.org.bd/services/forms/Distorted%20or%20Defective%20Prizebond%20Claim%20Form.pdf"
BB_PAGE = "https://www.bb.org.bd/en/index.php/investfacility/prizebond"
IRD_INFO = "https://prizebond.ird.gov.bd/genInfo.php"


def claim_body(ext, c):
    rows_en = rows_bn = ""
    for name_en, name_bn, amt in [("1st", "১ম", 600000), ("2nd", "২য়", 325000), ("3rd", "৩য়", 100000), ("4th", "৪র্থ", 50000), ("5th", "৫ম", 10000)]:
        tax, net = amt // 5, amt - amt // 5
        rows_en += f'<tr><td>{name_en} prize</td><td class="n">{c["money"](amt)}</td><td class="n">{c["money"](tax)}</td><td class="n">{c["money"](net)}</td></tr>\n'
        rows_bn += f'<tr><td>{name_bn} পুরস্কার</td><td class="n">{b(c["money"](amt))}</td><td class="n">{b(c["money"](tax))}</td><td class="n">{b(c["money"](net))}</td></tr>\n'
    return f"""<div class="l-en" lang="en">
<p>If one of your bonds won, you have <b>2 years from the draw date</b> to claim the money. After that the prize lapses and the money goes to the government treasury. Here is the whole process.</p>
<div class="note">Before you start, confirm the win on <a href="{BB_PAGE}" target="_blank" rel="noopener">Bangladesh Bank's website</a>. If results anywhere else differ, Bangladesh Bank's result is final.</div>
<h2>What you need</h2>
<ol>
<li><a href="{CLAIM_FORM}" target="_blank" rel="noopener">Bangladesh Bank's prize bond claim form</a> (PDF, in Bangla)</li>
<li>The original winning bond, with your signature once on the back</li>
<li>A copy of your national ID card (NID)</li>
<li>A copy of a cheque leaf (MICR cheque) from your bank account. The prize is paid into this account.</li>
<li>One passport-size photograph</li>
</ol>
<h2>Step by step</h2>
<ol>
<li><b>Fill in the form.</b> It asks for your name, father's name, present and permanent address, NID number, TIN, mobile number and bank account details (account name, number and routing number), plus the bond's series, number, draw number, draw date and prize amount.</li>
<li><b>Sign the back of the winning bond once.</b> The form asks for exactly one signature there.</li>
<li><b>Get the form attested.</b> The current form has a section where an officer of your bank signs and stamps it, so take it to your branch. Some offices also ask for attestation by a gazetted officer, so check when you submit.</li>
<li><b>Submit it</b> with the bond and the copies at any Bangladesh Bank office except Mymensingh, such as Motijheel or Sadarghat in Dhaka, Chattogram, Rajshahi, Khulna, Barishal, Sylhet or Rangpur. According to The Daily Star, the banks, post offices and savings bureau offices that sell prize bonds also accept claims; ask at your branch. Keep a copy of everything you hand in.</li>
<li><b>Get paid.</b> The prize, minus tax, is paid into your bank account. You don't get the winning bond back, but its ৳100 face value is paid along with the prize. News reports say payment usually takes up to about two months.</li>
</ol>
<h2>Tax: 20% at source</h2>
<p>Under section 118 of the Income Tax Act 2023, 20% is deducted from the prize before it is paid.</p>
<div class="tbl"><table><thead><tr><th>Prize</th><th>Amount</th><th>20% tax</th><th>You receive</th></tr></thead><tbody>
{rows_en}</tbody></table></div>
<p class="src">Plus the ৳100 face value of the winning bond.</p>
<h2>Damaged or torn bond?</h2>
<p>Bangladesh Bank has a separate <a href="{DAMAGED_FORM}" target="_blank" rel="noopener">form for damaged or defective prize bonds</a>. You state how the bond was damaged, and the bank decides on payment after examining it.</p>
<p class="src">Sources: Ministry of Finance prize bond information (<a href="{IRD_INFO}" target="_blank" rel="noopener">prizebond.ird.gov.bd</a>), Bangladesh Bank's claim form, and official draw announcements. Rules can change, so check the form before you submit.</p>
</div>
<div class="l-bn" lang="bn">
<p>আপনার কোনো বন্ড পুরস্কার পেলে <b>ড্রয়ের তারিখ থেকে ২ বছরের মধ্যে</b> টাকা দাবি করতে হবে। এরপর পুরস্কার তামাদি হয়ে টাকা সরকারি কোষাগারে চলে যায়। পুরো প্রক্রিয়া নিচে দেওয়া হলো।</p>
<div class="note">শুরু করার আগে <a href="{BB_PAGE}" target="_blank" rel="noopener">বাংলাদেশ ব্যাংকের ওয়েবসাইটে</a> ফলাফল মিলিয়ে নিন। অন্য কোথাও ফলাফল ভিন্ন হলে বাংলাদেশ ব্যাংকের ফলাফলই চূড়ান্ত।</div>
<h2>যা যা লাগবে</h2>
<ol>
<li><a href="{CLAIM_FORM}" target="_blank" rel="noopener">বাংলাদেশ ব্যাংকের প্রাইজবন্ড দাবি ফরম</a> (PDF)</li>
<li>পুরস্কারপ্রাপ্ত মূল বন্ড, পেছনে আপনার একটি স্বাক্ষরসহ</li>
<li>জাতীয় পরিচয়পত্রের কপি</li>
<li>আপনার ব্যাংক হিসাবের একটি চেকের পাতার কপি (MICR চেক)। পুরস্কারের টাকা এই হিসাবে জমা হবে।</li>
<li>এক কপি পাসপোর্ট সাইজের ছবি</li>
</ol>
<h2>ধাপে ধাপে</h2>
<ol>
<li><b>ফরম পূরণ করুন।</b> নাম, পিতার নাম, বর্তমান ও স্থায়ী ঠিকানা, জাতীয় পরিচয়পত্র নম্বর, টিআইএন, মোবাইল নম্বর ও ব্যাংক হিসাবের তথ্য (হিসাবের নাম, নম্বর ও রাউটিং নম্বর), এবং বন্ডের সিরিজ, নম্বর, ড্রয়ের নম্বর, তারিখ ও পুরস্কারের পরিমাণ লাগবে।</li>
<li><b>পুরস্কারপ্রাপ্ত বন্ডের পেছনে একবার স্বাক্ষর করুন।</b> ফরমে শুধু একটি স্বাক্ষরের কথা বলা আছে।</li>
<li><b>ফরম সত্যায়ন করান।</b> বর্তমান ফরমে একটি অংশ আছে যেখানে আপনার ব্যাংকের কর্মকর্তা স্বাক্ষর ও সিল দেন, তাই ফরম নিয়ে আপনার শাখায় যান। কোনো কোনো অফিস গেজেটেড কর্মকর্তার সত্যায়নও চায়, তাই জমা দেওয়ার সময় জেনে নিন।</li>
<li><b>জমা দিন</b>, বন্ড ও কপিগুলোসহ, ময়মনসিংহ ছাড়া বাংলাদেশ ব্যাংকের যেকোনো অফিসে, যেমন ঢাকার মতিঝিল বা সদরঘাট, চট্টগ্রাম, রাজশাহী, খুলনা, বরিশাল, সিলেট বা রংপুর। দ্য ডেইলি স্টারের তথ্য অনুযায়ী, যেসব ব্যাংক, ডাকঘর ও সঞ্চয় ব্যুরো প্রাইজবন্ড বিক্রি করে সেখানেও দাবি জমা নেওয়া হয়; আপনার শাখায় জেনে নিন। যা জমা দেবেন সবকিছুর একটি কপি নিজের কাছে রাখুন।</li>
<li><b>টাকা পাবেন।</b> কর কেটে পুরস্কারের টাকা আপনার ব্যাংক হিসাবে জমা হয়। পুরস্কারপ্রাপ্ত বন্ড ফেরত দেওয়া হয় না, তবে বন্ডের ১০০ টাকা অভিহিত মূল্য পুরস্কারের সাথে দেওয়া হয়। সংবাদমাধ্যমের তথ্য অনুযায়ী টাকা পেতে সাধারণত সর্বোচ্চ দুই মাস লাগে।</li>
</ol>
<h2>কর: উৎসে ২০%</h2>
<p>আয়কর আইন, ২০২৩-এর ১১৮ ধারা অনুযায়ী পুরস্কারের অর্থ থেকে ২০% কর কেটে টাকা দেওয়া হয়।</p>
<div class="tbl"><table><thead><tr><th>পুরস্কার</th><th>পরিমাণ</th><th>২০% কর</th><th>আপনি পাবেন</th></tr></thead><tbody>
{rows_bn}</tbody></table></div>
<p class="src">সাথে পুরস্কারপ্রাপ্ত বন্ডের ১০০ টাকা অভিহিত মূল্য।</p>
<h2>বন্ড ছেঁড়া বা নষ্ট?</h2>
<p>বাংলাদেশ ব্যাংকের একটি আলাদা <a href="{DAMAGED_FORM}" target="_blank" rel="noopener">বিকৃত বা ত্রুটিযুক্ত প্রাইজবন্ডের আবেদন ফরম</a> আছে। বন্ড কীভাবে নষ্ট হয়েছে তা লিখতে হয়, যাচাইয়ের পর ব্যাংক টাকা দেওয়ার বিষয়ে সিদ্ধান্ত নেয়।</p>
<p class="src">সূত্র: অর্থ মন্ত্রণালয়ের প্রাইজবন্ড তথ্য (<a href="{IRD_INFO}" target="_blank" rel="noopener">prizebond.ird.gov.bd</a>), বাংলাদেশ ব্যাংকের দাবি ফরম এবং ড্রয়ের সরকারি বিজ্ঞপ্তি। নিয়ম বদলাতে পারে, তাই জমা দেওয়ার আগে ফরমটি দেখে নিন।</p>
</div>"""


CLAIM = {
    "file": "how-to-claim-prize-bond.html",
    "nav_en": "How to claim a prize", "nav_bn": "পুরস্কার দাবির নিয়ম",
    "blurb_en": "Documents, steps, 20% tax", "blurb_bn": "কাগজপত্র, ধাপ, ২০% কর",
    "title": "How to Claim Prize Bond Money: Documents, Steps, Tax | প্রাইজবন্ডের টাকা তোলার নিয়ম",
    "desc": ("Won a Bangladesh prize bond prize? The documents you need, how to fill in Bangladesh Bank's claim form, "
             "where to submit it, the 20% tax and the 2-year deadline. প্রাইজবন্ডের পুরস্কারের টাকা তোলার নিয়ম।"),
    "h1_en": "How to claim prize bond money", "h1_bn": "প্রাইজবন্ডের পুরস্কারের টাকা তোলার নিয়ম",
    "sub_en": "Documents, steps and tax, in plain words", "sub_bn": "কাগজপত্র, ধাপ ও কর, সহজ ভাষায়",
    "body": claim_body,
    "updated": "2026-10-21",
}


# ---------------------------------------------------------------- buy
def buy_body(ext, c):
    return f"""<div class="l-en" lang="en">
<p>A prize bond is a ৳100 savings instrument from the Government of Bangladesh. It pays no interest. Instead, every bond takes part in the quarterly draws, and you can cash it back whenever you like.</p>
<h2>Where to buy</h2>
<p>Prize bonds are sold, and cashed back, at:</p>
<ul>
<li>Bangladesh Bank offices (all except Mymensingh)</li>
<li>Scheduled banks, except Shariah-based banks. Not every branch keeps them, so call first.</li>
<li>Post offices</li>
<li>National Savings Bureau offices</li>
</ul>
<p>Only the <b>৳100 bond</b> is sold today. It has been the only denomination since 1995. You pay its face value, ৳100 per bond.</p>
<h2>When a new bond enters the draws</h2>
<p>A bond takes part in a draw only if it was sold <b>at least 2 months before</b> the draw date. The sale date is written on the bond. After that it is included in every draw, four times a year: <a href="prize-bond-draw-schedule{ext}">see the draw schedule</a>.</p>
<h2>Cashing bonds back</h2>
<p>You can cash prize bonds at the same places you buy them. News reports describe this as possible at any time, for the face value of ৳100. A bond that wins a prize is handed in when you claim, and its face value is paid with the prize.</p>
<h2>Good to know</h2>
<ul>
<li><b>No interest, only prizes.</b> Your ৳100 stays ৳100. Whether it earns anything depends on luck in the draws.</li>
<li><b>Prizes are taxed 20% at source</b>, and must be claimed within 2 years: <a href="how-to-claim-prize-bond{ext}">how to claim</a>.</li>
<li><b>Keep a list of your bond numbers.</b> The easiest way is to enter them on <a href="./">our checker</a> and download the Excel sheet. Then one upload checks them all after every draw.</li>
<li><b>Keep the bonds themselves safe.</b> You need the original bond to claim a prize. If one gets damaged, Bangladesh Bank has a separate form for damaged bonds.</li>
</ul>
<p class="src">Source: Ministry of Finance prize bond information (<a href="{IRD_INFO}" target="_blank" rel="noopener">prizebond.ird.gov.bd</a>) and official draw announcements.</p>
</div>
<div class="l-bn" lang="bn">
<p>প্রাইজবন্ড বাংলাদেশ সরকারের ১০০ টাকার একটি সঞ্চয় মাধ্যম। এতে কোনো মুনাফা নেই। বদলে প্রতিটি বন্ড প্রতি তিন মাস অন্তর ড্রয়ে অংশ নেয়, আর যেকোনো সময় ভাঙিয়ে টাকা ফেরত নেওয়া যায়।</p>
<h2>কোথায় কিনবেন</h2>
<p>প্রাইজবন্ড কেনা ও ভাঙানো যায়:</p>
<ul>
<li>বাংলাদেশ ব্যাংকের অফিসে (ময়মনসিংহ ছাড়া সব)</li>
<li>তফসিলি ব্যাংকে, শরীয়াহভিত্তিক ব্যাংক ছাড়া। সব শাখায় থাকে না, তাই আগে ফোন করে নিন।</li>
<li>ডাকঘরে</li>
<li>জাতীয় সঞ্চয় ব্যুরোতে</li>
</ul>
<p>এখন শুধু <b>১০০ টাকার বন্ড</b> বিক্রি হয়। ১৯৯৫ সাল থেকে এটিই একমাত্র মূল্যমান। প্রতিটি বন্ডের দাম তার অভিহিত মূল্য, ১০০ টাকা।</p>
<h2>নতুন বন্ড কবে থেকে ড্রয়ে অংশ নেয়</h2>
<p>ড্রয়ের তারিখের <b>অন্তত ২ মাস আগে</b> বিক্রি হওয়া বন্ডই শুধু ড্রয়ে অংশ নেয়। বিক্রির তারিখ বন্ডে লেখা থাকে। এরপর বছরে চারবার প্রতিটি ড্রয়ে বন্ডটি অংশ নেয়: <a href="prize-bond-draw-schedule{ext}">ড্রয়ের সময়সূচি দেখুন</a>।</p>
<h2>বন্ড ভাঙানো</h2>
<p>যেখানে কেনা যায়, সেখানেই প্রাইজবন্ড ভাঙানো যায়। সংবাদমাধ্যমের তথ্য অনুযায়ী যেকোনো সময় ১০০ টাকা অভিহিত মূল্যে ভাঙানো যায়। পুরস্কারপ্রাপ্ত বন্ড দাবি করার সময় জমা দিতে হয়, আর এর অভিহিত মূল্য পুরস্কারের সাথে দেওয়া হয়।</p>
<h2>জেনে রাখুন</h2>
<ul>
<li><b>মুনাফা নেই, শুধু পুরস্কার।</b> আপনার ১০০ টাকা ১০০ টাকাই থাকে। কিছু পাবেন কি না তা ড্রয়ের ভাগ্যের ওপর নির্ভর করে।</li>
<li><b>পুরস্কারের অর্থ থেকে উৎসে ২০% কর কাটা হয়</b>, এবং ২ বছরের মধ্যে দাবি করতে হয়: <a href="how-to-claim-prize-bond{ext}">দাবি করার নিয়ম</a>।</li>
<li><b>বন্ড নম্বরগুলোর একটি তালিকা রাখুন।</b> সবচেয়ে সহজ উপায়: <a href="./">আমাদের চেকারে</a> নম্বরগুলো দিয়ে এক্সেল শিট ডাউনলোড করুন। তাহলে প্রতিটি ড্রয়ের পর একবার আপলোড করলেই সব মিলিয়ে দেখা যাবে।</li>
<li><b>মূল বন্ডগুলো যত্নে রাখুন।</b> পুরস্কার দাবি করতে মূল বন্ড লাগে। বন্ড নষ্ট হলে বাংলাদেশ ব্যাংকের আলাদা ফরম আছে।</li>
</ul>
<p class="src">সূত্র: অর্থ মন্ত্রণালয়ের প্রাইজবন্ড তথ্য (<a href="{IRD_INFO}" target="_blank" rel="noopener">prizebond.ird.gov.bd</a>) এবং ড্রয়ের সরকারি বিজ্ঞপ্তি।</p>
</div>"""


BUY = {
    "file": "how-to-buy-prize-bond.html",
    "nav_en": "How to buy prize bonds", "nav_bn": "প্রাইজবন্ড কেনার নিয়ম",
    "blurb_en": "Where to buy, cashing back", "blurb_bn": "কোথায় কিনবেন, ভাঙাবেন",
    "title": "How to Buy Prize Bonds in Bangladesh: Where, Price, Rules | প্রাইজবন্ড কোথায় কিনবেন",
    "desc": ("Where to buy and cash Bangladesh prize bonds (Bangladesh Bank, banks, post offices, National Savings Bureau), "
             "the ৳100 price, when a new bond enters the draws, and tips. প্রাইজবন্ড কেনা ও ভাঙানোর নিয়ম।"),
    "h1_en": "How to buy prize bonds in Bangladesh", "h1_bn": "প্রাইজবন্ড কেনার নিয়ম",
    "sub_en": "Where to buy, when bonds enter the draws, cashing back", "sub_bn": "কোথায় কিনবেন, কবে ড্রয়ে আসে, কীভাবে ভাঙাবেন",
    "body": buy_body,
    "updated": "2026-10-21",
}

# ---------------------------------------------------------------- savings certificate calculator
# Rates in force since 1 July 2025 (IRD circular of 30 June 2025), kept unchanged for Jan-Jun 2026 and
# for 1 Jul-31 Dec 2026 (IRD, as reported by TBS 1 Jul 2025, RisingBD 1 Jul 2026, Bangla Tribune 2 Jul 2026).
# Next review: January 2027. Each list = annual rate if cashed at the end of year 1, 2, ...; last = maturity.
# Tier 1 = total savings certificate holding up to Tk 7.5 lakh; tier 2 = above.
RATES_CHECKED = "21 Oct 2026"
SCHEMES = {
    "bsp": {"en": "5-year Bangladesh Sanchayapatra", "bn": "৫ বছর মেয়াদি বাংলাদেশ সঞ্চয়পত্র", "years": 5, "pay": "maturity",
            "t1": [9.74, 10.21, 10.72, 11.26, 11.83], "t2": [9.72, 10.19, 10.70, 11.23, 11.80],
            "who_en": "Anyone, including institutions. Up to ৳30 lakh in one name.",
            "who_bn": "যে কেউ, প্রতিষ্ঠানও কিনতে পারে। একক নামে সর্বোচ্চ ৩০ লাখ টাকা।"},
    "q3": {"en": "3-year Profit-based (quarterly profit)", "bn": "৩ বছর মেয়াদি তিন মাস অন্তর মুনাফাভিত্তিক", "years": 3, "pay": "quarterly",
           "t1": [10.65, 11.22, 11.82], "t2": [10.60, 11.16, 11.77],
           "who_en": "Anyone, including institutions. Up to ৳30 lakh in one name.",
           "who_bn": "যে কেউ, প্রতিষ্ঠানও কিনতে পারে। একক নামে সর্বোচ্চ ৩০ লাখ টাকা।"},
    "family": {"en": "Paribar Sanchayapatra (family, monthly profit)", "bn": "পরিবার সঞ্চয়পত্র (মাসিক মুনাফা)", "years": 5, "pay": "monthly",
               "t1": [9.81, 10.29, 10.80, 11.35, 11.93], "t2": [9.72, 10.19, 10.70, 11.23, 11.80],
               "who_en": "Women aged 18+, people with disabilities, and anyone aged 65+. Up to ৳45 lakh, single name only.",
               "who_bn": "১৮ বছরের বেশি বয়সী নারী, প্রতিবন্ধী ব্যক্তি এবং ৬৫ বছরের বেশি বয়সী যে কেউ। শুধু একক নামে, সর্বোচ্চ ৪৫ লাখ টাকা।"},
    "pension": {"en": "Pensioner Sanchayapatra (quarterly profit)", "bn": "পেনশনার সঞ্চয়পত্র (তিন মাস অন্তর মুনাফা)", "years": 5, "pay": "quarterly",
                "t1": [9.84, 10.32, 10.84, 11.39, 11.98], "t2": [9.72, 10.19, 10.70, 11.23, 11.80],
                "who_en": "Retired government, semi-government and autonomous-body employees, retired judges and armed forces members, and family pension holders. Up to ৳50 lakh.",
                "who_bn": "অবসরপ্রাপ্ত সরকারি, আধা-সরকারি ও স্বায়ত্তশাসিত প্রতিষ্ঠানের কর্মচারী, অবসরপ্রাপ্ত বিচারপতি ও সশস্ত্র বাহিনীর সদস্য এবং পারিবারিক পেনশনভোগী। সর্বোচ্চ ৫০ লাখ টাকা।"},
}


def calc_body(ext, c):
    opts = "".join(f'<option value="{k}" data-ien="{v["en"]}" data-ibn="{v["bn"]}">{v["en"]}</option>' for k, v in SCHEMES.items())

    def rate_table(bn):
        head = "<tr><th>{}</th>{}</tr>".format("সঞ্চয়পত্র" if bn else "Certificate",
            "".join(f"<th>{['১ম','২য়','৩য়','৪র্থ','৫ম'][i-1] + ' বছর' if bn else (str(i) + (' year' if i == 1 else ' years'))}</th>" for i in range(1, 6)))
        rows = ""
        for k, v in SCHEMES.items():
            for tier, label_en, label_bn in [("t1", "up to ৳7.5 lakh", "সাড়ে ৭ লাখ পর্যন্ত"), ("t2", "above ৳7.5 lakh", "সাড়ে ৭ লাখের বেশি")]:
                cells = "".join(f'<td class="n">{(b(f"{r:.2f}") if bn else f"{r:.2f}")}%</td>' for r in v[tier]) + "<td></td>" * (5 - v["years"])
                rows += f'<tr><td>{v["bn"] if bn else v["en"]}<br><span class="src">{label_bn if bn else label_en}</span></td>{cells}</tr>'
        return f'<div class="tbl"><table><thead>{head}</thead><tbody>{rows}</tbody></table></div>'

    form = f"""<form class="calc" id="calc" novalidate>
  <div class="field"><label for="cScheme" data-ien="Certificate" data-ibn="সঞ্চয়পত্র">Certificate</label><select id="cScheme">{opts}</select></div>
  <div class="field"><label for="cAmount" data-ien="Amount you invest (৳)" data-ibn="বিনিয়োগের পরিমাণ (৳)">Amount you invest (৳)</label><input id="cAmount" inputmode="numeric" value="100000" autocomplete="off"></div>
  <div class="field"><label for="cTotal" data-ien="Your total in savings certificates, including this (optional, ৳)" data-ibn="এটিসহ সঞ্চয়পত্রে আপনার মোট বিনিয়োগ (ঐচ্ছিক, ৳)">Your total in savings certificates, including this (optional, ৳)</label><input id="cTotal" inputmode="numeric" placeholder="" autocomplete="off"><small data-ien="Above ৳7.5 lakh, slightly lower rates apply. Leave empty if this is your only one." data-ibn="সাড়ে ৭ লাখ টাকার বেশি হলে মুনাফার হার একটু কম। এটিই একমাত্র হলে ফাঁকা রাখুন।">Above ৳7.5 lakh, slightly lower rates apply. Leave empty if this is your only one.</small></div>
  <div class="field"><label for="cTax" data-ien="Tax deducted from profit" data-ibn="মুনাফা থেকে কর কর্তন">Tax deducted from profit</label><select id="cTax">
    <option value="10" data-ien="10% (current rule)" data-ibn="১০% (বর্তমান নিয়ম)">10% (current rule)</option>
    <option value="5" data-ien="5%" data-ibn="৫%">5%</option>
    <option value="0" data-ien="No tax (show profit before tax)" data-ibn="কর ছাড়া (করের আগের মুনাফা)">No tax (show profit before tax)</option></select></div>
</form>
<div class="calc-out" id="calcOut" aria-live="polite"></div>
<p class="src" id="calcWho"></p>"""

    return f"""{form}
<div class="l-en" lang="en">
<h2>About these numbers</h2>
<ul>
<li><b>Rates in force since 1 July 2025.</b> The government kept them unchanged for January to June 2026 and again for 1 July to 31 December 2026. Rates are normally reviewed every six months, so the next change could come in January 2027. Last checked {RATES_CHECKED}.</li>
<li><b>Your rate is fixed when you buy</b> and stays the same until maturity, even if rates change later.</li>
<li><b>Above ৳7.5 lakh, slightly lower rates apply.</b> How your existing certificates are counted toward that line isn't clearly published, so ask your bank or post office. This calculator applies the lower rate to the whole amount when your total is above ৳7.5 lakh.</li>
<li><b>Tax:</b> from July 2026, 10% is deducted from the profit as an advance tax. It is no longer final: you can adjust it against your income tax, and you must file a return to get any excess back. Earlier, a lower 5% rate applied to smaller holdings, and Pensioner certificates up to ৳5 lakh were tax-free; news reports don't make clear whether these still apply. Without a TIN, a higher rate may be deducted. Ask your bank or post office which rate applies to you.</li>
<li><b>Cashing early</b> pays a lower rate for the years you held it (table below).</li>
<li>This calculator works out simple profit on the amount you invest. Your bank or post office's figure is final.</li>
</ul>
<h2>All current rates</h2>
<p>Annual profit rate if you cash the certificate at the end of each year. The last column of each row is the rate at maturity.</p>
{rate_table(False)}
<p class="src">Sources: Internal Resources Division (Ministry of Finance) circular of 30 June 2025 and its July 2026 decision to keep rates unchanged, as reported by The Business Standard, RisingBD, Bangla Tribune and Dhaka Tribune; buyer rules from bdnews24 and Prothom Alo; tax from Prothom Alo, Jugantor and Bangla Tribune (June–July 2026).</p>
</div>
<div class="l-bn" lang="bn">
<h2>এই হিসাব সম্পর্কে</h2>
<ul>
<li><b>১ জুলাই ২০২৫ থেকে কার্যকর হার।</b> সরকার জানুয়ারি–জুন ২০২৬ এবং আবার ১ জুলাই–৩১ ডিসেম্বর ২০২৬ পর্যন্ত হার অপরিবর্তিত রেখেছে। সাধারণত ছয় মাস পরপর হার পর্যালোচনা হয়, তাই জানুয়ারি ২০২৭-এ হার বদলাতে পারে। সর্বশেষ যাচাই: {b("21")} অক্টোবর {b("2026")}।</li>
<li><b>কেনার সময়ের হারই মেয়াদ পর্যন্ত বহাল থাকে</b>, পরে হার বদলালেও।</li>
<li><b>সাড়ে ৭ লাখ টাকার বেশি হলে মুনাফার হার একটু কম।</b> আগের সঞ্চয়পত্রগুলো এই সীমায় কীভাবে গোনা হয় তা স্পষ্টভাবে প্রকাশিত নয়, তাই আপনার ব্যাংক বা ডাকঘরে জেনে নিন। মোট বিনিয়োগ সাড়ে ৭ লাখের বেশি হলে এই ক্যালকুলেটর পুরো টাকায় কম হার ধরে।</li>
<li><b>কর:</b> জুলাই ২০২৬ থেকে মুনাফা থেকে ১০% অগ্রিম কর কাটা হয়। এটি আর চূড়ান্ত কর দায় নয়: আয়করের সাথে সমন্বয় করা যায়, বাড়তি কর ফেরত পেতে রিটার্ন দাখিল করতে হয়। আগে কম বিনিয়োগে ৫% কর কাটা হতো, আর ৫ লাখ টাকা পর্যন্ত পেনশনার সঞ্চয়পত্র করমুক্ত ছিল; এগুলো এখনো প্রযোজ্য কি না সংবাদমাধ্যমে স্পষ্ট নয়। টিআইএন না থাকলে বেশি হারে কর কাটা হতে পারে। আপনার ক্ষেত্রে কোন হার প্রযোজ্য তা ব্যাংক বা ডাকঘরে জেনে নিন।</li>
<li><b>মেয়াদের আগে ভাঙালে</b> যত বছর রেখেছেন সেই বছরের কম হারে মুনাফা পাবেন (নিচের সারণি)।</li>
<li>এই ক্যালকুলেটর বিনিয়োগের ওপর সরল মুনাফা হিসাব করে। চূড়ান্ত হিসাব আপনার ব্যাংক বা ডাকঘরের।</li>
</ul>
<h2>বর্তমান সব হার</h2>
<p>প্রতি বছর শেষে ভাঙালে বার্ষিক মুনাফার হার। প্রতিটি সারির শেষ ঘরটি মেয়াদপূর্তির হার।</p>
{rate_table(True)}
<p class="src">সূত্র: অভ্যন্তরীণ সম্পদ বিভাগের (অর্থ মন্ত্রণালয়) ৩০ জুন ২০২৫-এর প্রজ্ঞাপন এবং জুলাই ২০২৬-এ হার অপরিবর্তিত রাখার সিদ্ধান্ত, দ্য বিজনেস স্ট্যান্ডার্ড, রাইজিংবিডি, বাংলা ট্রিবিউন ও ঢাকা ট্রিবিউনের প্রতিবেদন অনুযায়ী; ক্রেতার নিয়ম বিডিনিউজ২৪ ও প্রথম আলো থেকে; কর প্রথম আলো, যুগান্তর ও বাংলা ট্রিবিউন থেকে (জুন–জুলাই ২০২৬)।</p>
</div>"""


import json as _json
CALC_JS = """<script>
(function(){
const S=__SCHEMES__,$=id=>document.getElementById(id),L=()=>window.pbLang?pbLang():"en";
const bn=x=>window.pbBn?pbBn(x):String(x);
const num=s=>{const t=String(s).replace(/[০-৯]/g,c=>"০১২৩৪৫৬৭৮৯".indexOf(c)).replace(/[^0-9.]/g,"");return t?+t:NaN};
function tk(x){const s=Math.round(x).toLocaleString("en-IN");return "৳"+(L()==="bn"?bn(s):s)}
function pct(x){const s=x.toFixed(2)+"%";return L()==="bn"?bn(s):s}
function yr(i){return L()==="bn"?bn(i)+" বছর":i+(i===1?" year":" years")}
function calc(){
  const k=$("cScheme").value,s=S[k],amt=num($("cAmount").value),tot=num($("cTotal").value),tax=+$("cTax").value/100;
  const out=$("calcOut"),bnL=L()==="bn";
  $("calcWho").textContent=bnL?s.who_bn:s.who_en;
  if(!(amt>0)){out.innerHTML=`<p class="err">${bnL?"বিনিয়োগের পরিমাণ লিখুন।":"Enter the amount you invest."}</p>`;return}
  const total=Math.max(amt,tot>0?tot:0),tier=total>750000?"t2":"t1",rates=s[tier],r=rates[rates.length-1]/100,n=s.years;
  const gross=amt*r*n,net=gross*(1-tax);
  let per="";
  if(s.pay==="monthly")per=[bnL?"প্রতি মাসে":"Every month",amt*r/12];
  else if(s.pay==="quarterly")per=[bnL?"প্রতি ৩ মাসে":"Every 3 months",amt*r/4];
  else per=[bnL?`${bn(n)} বছর পর একবারে`:`Once, after ${n} years`,gross];
  const rows=rates.map((x,i)=>{const g=amt*x/100*(i+1);return `<tr><td>${yr(i+1)}</td><td class="n">${pct(x)}</td><td class="n">${tk(g*(1-tax))}</td><td class="n">${tk(amt+g*(1-tax))}</td></tr>`}).join("");
  out.innerHTML=`<div class="calc-cards">
   <div class="card"><span>${bnL?"মুনাফার হার":"Profit rate"}</span><b>${pct(r*100)}</b><small>${tier==="t2"?(bnL?"সাড়ে ৭ লাখের বেশি":"above ৳7.5 lakh"):(bnL?"সাড়ে ৭ লাখ পর্যন্ত":"up to ৳7.5 lakh")}</small></div>
   <div class="card"><span>${per[0]}</span><b>${tk(per[1]*(1-tax))}</b><small>${tax?(bnL?`কর কাটার পর (কর ${tk(per[1]*tax)})`:`after tax (tax ${tk(per[1]*tax)})`):(bnL?"করের আগে":"before tax")}</small></div>
   <div class="card"><span>${bnL?`${bn(n)} বছরে মোট মুনাফা`:`Total profit over ${n} years`}</span><b>${tk(net)}</b><small>${bnL?`মেয়াদ শেষে মোট ফেরত ${tk(amt+net)}`:`You get back ${tk(amt+net)} in total`}</small></div>
  </div>
  <h3>${bnL?"মেয়াদের আগে ভাঙালে":"If you cash it early"}</h3>
  <div class="tbl"><table><thead><tr><th>${bnL?"রেখেছেন":"Held for"}</th><th>${bnL?"হার":"Rate"}</th><th>${bnL?"মোট মুনাফা":"Total profit"}</th><th>${bnL?"মোট ফেরত":"You get back"}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}
["cScheme","cAmount","cTotal","cTax"].forEach(id=>{$(id).addEventListener("input",calc);$(id).addEventListener("change",calc)});
$("calc").addEventListener("submit",e=>e.preventDefault());
document.addEventListener("pb-lang",calc);
calc();
})();
</script>"""


def calc_script():
    data = {k: {kk: v[kk] for kk in ("years", "pay", "t1", "t2", "who_en", "who_bn")} for k, v in SCHEMES.items()}
    return CALC_JS.replace("__SCHEMES__", _json.dumps(data, ensure_ascii=False))


CALC = {
    "file": "sanchayapatra-profit-calculator.html",
    "nav_en": "Savings certificate calculator", "nav_bn": "সঞ্চয়পত্র মুনাফা ক্যালকুলেটর",
    "blurb_en": "Profit at current rates", "blurb_bn": "বর্তমান হারে মুনাফা",
    "title": "Sanchayapatra Profit Calculator 2026: Current Rates | সঞ্চয়পত্রের মুনাফা হিসাব",
    "desc": ("Calculate profit on Bangladesh savings certificates at current rates: 5-year Bangladesh Sanchayapatra, "
             "3-month profit-based, Paribar and Pensioner. Monthly and quarterly profit, tax, early encashment. সঞ্চয়পত্রের মুনাফা ক্যালকুলেটর।"),
    "h1_en": "Savings certificate (Sanchayapatra) profit calculator", "h1_bn": "সঞ্চয়পত্রের মুনাফা ক্যালকুলেটর",
    "sub_en": "Current rates, monthly or quarterly profit, and tax", "sub_bn": "বর্তমান হার, মাসিক বা তিন মাস অন্তর মুনাফা এবং কর",
    "body": calc_body,
    "script": calc_script(),
    "updated": "2026-10-21",
}

def build_guides(c):
    """Called by build.py with draw data and helpers; returns the list of guide pages."""
    return [CLAIM, schedule_guide(c), BUY, CALC]

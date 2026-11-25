import os
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

OUT_PPTX = r"C:\Users\aarun\source\repos\WebApplication2\SuryaSugam_Bakery_Pitch_Deck.pptx"
SHOTS_DIR = r"C:\Users\aarun\.gemini\antigravity\brain\2be00e1d-efe1-4d11-a87e-df975133ec09\scratch\shots"
SCRATCH_DIR = r"C:\Users\aarun\.gemini\antigravity\brain\2be00e1d-efe1-4d11-a87e-df975133ec09\scratch"
LOGO_IMG = r"C:\Users\aarun\source\repos\WebApplication2\wwwroot\images\logo.jpg"

HOME_IMG = os.path.join(SHOTS_DIR, "home.png")
PROD_IMG = os.path.join(SHOTS_DIR, "product.png")
CAT_IMG = os.path.join(SHOTS_DIR, "categories.png")
CUST_IMG = os.path.join(SHOTS_DIR, "custom_order.png")
CART_IMG = os.path.join(SHOTS_DIR, "cart.png")

CHART4_IMG = os.path.join(SCRATCH_DIR, "slide4_chart.png")
TAMSAM_IMG = os.path.join(SCRATCH_DIR, "slide6_tamsam.png")


def make_charts():
    # 1. Slide 4 Stacked Bar Chart (Catalog Revenue & Margin Mix)
    W, H = 900, 420
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)
    try:
        font_b = ImageFont.truetype("arialbd.ttf", 22)
        font_r = ImageFont.truetype("arial.ttf", 19)
        font_s = ImageFont.truetype("arialbd.ttf", 17)
    except Exception:
        font_b = font_r = font_s = ImageFont.load_default()

    # Grid lines
    base_y = 335
    left_x = 110
    for i, lbl in enumerate(["0", "50K", "100K", "150K", "200K"]):
        y = base_y - i * 65
        d.line([(left_x, y), (860, y)], fill=(230, 230, 230), width=2)
        d.text((22, y - 10), lbl, fill=(70, 70, 70), font=font_r)

    bars = [
        ("M1 (Retail)", [(40, (120, 66, 38)), (32, (65, 165, 210)), (25, (235, 125, 35)), (18, (40, 130, 75))], "66.5% GM"),
        ("M3 (Repeat)", [(60, (120, 66, 38)), (48, (65, 165, 210)), (45, (235, 125, 35)), (35, (40, 130, 75))], "68.5% GM"),
        ("M6 (+Custom)", [(75, (120, 66, 38)), (60, (65, 165, 210)), (65, (235, 125, 35)), (60, (40, 130, 75))], "70.0% GM"),
    ]
    bar_w = 115
    xs = [190, 420, 650]
    for idx, (label, segs, top_lbl) in enumerate(bars):
        x = xs[idx]
        cur_y = base_y
        for val, col in segs:
            d.rectangle([x, cur_y - val, x + bar_w, cur_y], fill=col)
            cur_y -= val
        d.text((x + 12, cur_y - 30), top_lbl, fill=(20, 45, 95), font=font_b)
        d.text((x + 4, base_y + 14), label, fill=(30, 30, 30), font=font_r)

    # Trend arrow
    d.line([(310, 220), (420, 175)], fill=(25, 25, 25), width=4)
    d.line([(540, 145), (650, 95)], fill=(25, 25, 25), width=4)
    d.ellipse([485, 125, 555, 175], fill=(195, 75, 40))
    d.text((494, 140), "+148%", fill=(255, 255, 255), font=font_s)

    # Legend at top
    leg = [("FANS", (120, 66, 38)), ("CREAMROLL", (65, 165, 210)), ("TOAST", (235, 125, 35)), ("CUSTOM", (40, 130, 75))]
    lx = 120
    for name, col in leg:
        d.rectangle([lx, 18, lx + 22, 38], fill=col)
        d.text((lx + 28, 17), name, fill=(40, 40, 40), font=font_s)
        lx += 180

    im.save(CHART4_IMG)

    # 2. Slide 6 TAM / SAM / SOM nested circles
    S = 360
    im2 = Image.new("RGBA", (S, S), (255, 255, 255, 0))
    d2 = ImageDraw.Draw(im2)
    d2.ellipse([10, 10, 350, 350], fill=(180, 168, 228), outline=(120, 105, 175), width=3)
    d2.ellipse([55, 95, 305, 345], fill=(138, 125, 210), outline=(95, 80, 165), width=3)
    d2.ellipse([105, 190, 255, 340], fill=(92, 76, 175), outline=(65, 50, 140), width=3)
    d2.text((152, 42), "TAM", fill=(255, 255, 255), font=font_b)
    d2.text((152, 135), "SAM", fill=(255, 255, 255), font=font_b)
    d2.text((152, 250), "SOM", fill=(255, 255, 255), font=font_b)
    im2.save(TAMSAM_IMG)


make_charts()

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

# Palette matching sample PDF + SuryaSugam brand harmony
C_WHITE   = RGBColor(255, 255, 255)
C_BLACK   = RGBColor(18, 18, 18)
C_NAVY    = RGBColor(20, 62, 118)     # Sample PDF header/accent blue
C_FOOTER  = RGBColor(12, 95, 170)     # Sample PDF bottom footer strip
C_RED     = RGBColor(205, 36, 36)     # Sample PDF crimson highlights
C_CLAY    = RGBColor(184, 97, 67)     # SuryaSugam terracotta accent
C_GREEN   = RGBColor(22, 133, 66)     # WhatsApp / check green
C_MINT    = RGBColor(226, 244, 226)
C_SKY     = RGBColor(225, 240, 250)
C_CREAM   = RGBColor(252, 238, 222)
C_PINK    = RGBColor(250, 224, 240)
C_LAV     = RGBColor(235, 230, 248)
C_GREY_BG = RGBColor(244, 246, 248)
C_BORDER  = RGBColor(70, 75, 85)
C_MUTED   = RGBColor(85, 90, 98)


def rect(slide, l, t, w, h, fill=C_WHITE, border=None, bw=1.0, rounded=False):
    shape = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    if rounded:
        try:
            s.adjustments[0] = 0.06
        except Exception:
            pass
    if fill is not None:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if border is not None:
        s.line.color.rgb = border
        s.line.width = Pt(bw)
    else:
        s.line.fill.background()
    return s


def pill(slide, l, t, w, h, text, bg=C_BLACK, fg=C_WHITE, fs=11, bold=True):
    s = rect(slide, l, t, w, h, fill=bg, rounded=True)
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Pt(2)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = text
    p.font.name = "Calibri"
    p.font.size = Pt(fs)
    p.font.bold = bold
    p.font.color.rgb = fg
    return s


def tb(slide, l, t, w, h, text="", fs=10, bold=False, color=C_BLACK, align=PP_ALIGN.LEFT, font="Calibri"):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]
    p.alignment = align
    p.text = text
    p.font.name = font
    p.font.size = Pt(fs)
    p.font.bold = bold
    p.font.color.rgb = color
    return box


def add_bullets(box, lines, fs=9.5, color=C_BLACK, space=2):
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = "Calibri"
        p.font.size = Pt(fs)
        p.font.color.rgb = color
        p.space_after = Pt(space)


def add_header_and_footer(slide, title, page_num):
    rect(slide, 0, 0, 13.333, 7.5, fill=C_WHITE)
    # Left & Right Brand Badges
    if os.path.exists(LOGO_IMG):
        slide.shapes.add_picture(LOGO_IMG, Inches(0.18), Inches(0.08), width=Inches(0.65))
        slide.shapes.add_picture(LOGO_IMG, Inches(11.35), Inches(0.08), width=Inches(0.62))
    tb(slide, 12.02, 0.14, 1.2, 0.55, "SURYASUGAM\nBAKERY\n2026", fs=10, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)
    tb(slide, 1.0, 0.12, 10.2, 0.55, title, fs=24, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)
    # Bottom blue banner matching sample PDF
    rect(slide, 0, 7.12, 13.333, 0.38, fill=C_FOOTER)
    tb(slide, 3.5, 7.15, 6.3, 0.3, "SURYASUGAM BAKERY - @ MATHURA D2C PITCH DECK", fs=10.5, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    tb(slide, 12.5, 7.15, 0.6, 0.3, str(page_num), fs=11, bold=True, color=C_WHITE, align=PP_ALIGN.RIGHT)


# ==============================================================================
# SLIDE 1: COVER SLIDE (MATCHING SAMPLE PAGE 1)
# ==============================================================================
s1 = prs.slides.add_slide(blank)
rect(s1, 0, 0, 13.333, 7.5, fill=C_WHITE)

# Top title + logo corner
tb(s1, 0.9, 0.25, 9.8, 0.75, "SURYASUGAM BAKERY 2026", fs=32, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER, font="Georgia")
if os.path.exists(LOGO_IMG):
    s1.shapes.add_picture(LOGO_IMG, Inches(10.85), Inches(0.15), width=Inches(0.95))
tb(s1, 11.82, 0.22, 1.35, 0.75, "SURYASUGAM\nBAKERY\nMATHURA", fs=11, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)

# Right side geometric hexagons matching sample Page 1 + live web app hero frame
hex_big = s1.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(7.1), Inches(1.2), Inches(5.3), Inches(5.7))
hex_big.fill.solid()
hex_big.fill.fore_color.rgb = RGBColor(239, 239, 240)
hex_big.line.fill.background()

hex_sm1 = s1.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(6.95), Inches(1.0), Inches(1.7), Inches(1.65))
hex_sm1.fill.background()
hex_sm1.line.color.rgb = RGBColor(225, 225, 225)
hex_sm1.line.width = Pt(4)

hex_sm2 = s1.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(6.15), Inches(4.5), Inches(1.0), Inches(1.0))
hex_sm2.fill.solid()
hex_sm2.fill.fore_color.rgb = RGBColor(235, 235, 236)
hex_sm2.line.fill.background()

# Embed Homepage screenshot cleanly inside the right showcase card
rect(s1, 7.45, 2.05, 4.65, 3.15, fill=C_WHITE, border=C_NAVY, bw=2, rounded=True)
if os.path.exists(HOME_IMG):
    s1.shapes.add_picture(HOME_IMG, Inches(7.55), Inches(2.15), width=Inches(4.45))
pill(s1, 8.2, 5.35, 3.1, 0.4, "LIVE D2C WEB APPLICATION", bg=C_CLAY, fg=C_WHITE, fs=10)

# Left key-value bullets matching sample Page 1 typography
info_rows = [
    ("Project Code –", "SS-D2C-2026 (.NET 10 + SQLite)"),
    ("Project Title –", "SuryaSugam Bakery Fresh Storefront & Catering"),
    ("Theme –", "Hyperlocal D2C Commerce & Zero-MDR"),
    ("Category –", "Full-Stack Web App (MVC + SSE)"),
    ("Location –", "Mathura, UP (Food Safety Zone 2)"),
    ("Direct Order –", "WhatsApp (+91 89219 86080)"),
]
box1 = s1.shapes.add_textbox(Inches(0.35), Inches(1.55), Inches(6.55), Inches(5.3))
tf1 = box1.text_frame
tf1.word_wrap = True
for idx, (k, v) in enumerate(info_rows):
    p = tf1.paragraphs[0] if idx == 0 else tf1.add_paragraph()
    p.space_after = Pt(14)
    r1 = p.add_run()
    r1.text = f"• {k}\n   " if idx == 1 else f"• {k} "
    r1.font.name = "Calibri"
    r1.font.size = Pt(22)
    r1.font.bold = True
    r1.font.color.rgb = C_BLACK
    r2 = p.add_run()
    r2.text = v
    r2.font.name = "Calibri"
    r2.font.size = Pt(22)
    r2.font.bold = True
    r2.font.color.rgb = C_RED


# ==============================================================================
# SLIDE 2: SOLUTION, COMPARISON TABLE, HOW IT WORKS WITH APP SCREENSHOTS
# ==============================================================================
s2 = prs.slides.add_slide(blank)
add_header_and_footer(s2, "SURYASUGAM D2C BAKERY STOREFRONT & CATERING", 2)

pill(s2, 1.55, 0.72, 1.55, 0.28, "SOLUTION", bg=C_BLACK, fg=C_WHITE, fs=10)
tb(s2, 0.25, 1.02, 5.3, 0.42, "A zero-commission, bilingual (EN/HI) web storefront for daily tea-time snacks & bulk custom orders, dispatching structured orders straight to WhatsApp.", fs=9.5, bold=True)

# 2 columns of solution bullets
col1_b = [
    "• Zero Aggregator Commission: 0% MDR vs 20–30% food-app cuts.",
    "• Bilingual Instant UX: 1-click English ↔ हिंदी DOM toggle.",
    "• Persistent SQLite Cart: Cookie identity requires zero sign-up.",
    "• IST Slot Scheduling: Mathura date & 4 time-window validation.",
]
col2_b = [
    "• Special Request Engine: Bulk catering orders (1–500 pcs).",
    "• Real-Time Reviews (SSE): Live comments via Channels.",
    "• Full Audit Log: Orders & events saved in SQLite WAL.",
    "• Deploy-Ready Docker: Port 8080 container with /health.",
]
b_l = s2.shapes.add_textbox(Inches(0.2), Inches(1.48), Inches(2.7), Inches(1.8))
add_bullets(b_l, col1_b, fs=8.8, space=3)
b_r = s2.shapes.add_textbox(Inches(2.92), Inches(1.48), Inches(2.7), Inches(1.8))
add_bullets(b_r, col2_b, fs=8.8, space=3)

tb(s2, 0.22, 3.25, 5.4, 0.35, "We solve local bakery margin leakage & phone-order errors with structured direct-to-WhatsApp commerce.", fs=9, bold=True, color=C_NAVY)

# HOW IT ADDRESSES THE PROBLEM
pill(s2, 0.25, 3.66, 2.85, 0.28, "HOW IT ADDRESSES THE PROBLEM?", bg=C_BLACK, fg=C_WHITE, fs=9.5)
checks = [
    "✔ Eliminates 20–30% platform fees.",
    "✔ Removes phone miscommunication.",
    "✔ Serves Hindi & English shoppers.",
    "✔ Unlocks 10x AOV event catering.",
    "✔ Retains 100% customer data locally.",
]
b_chk = s2.shapes.add_textbox(Inches(0.22), Inches(4.0), Inches(2.95), Inches(1.55))
add_bullets(b_chk, checks, fs=9.2, color=C_GREEN, space=3)

# Comparison table (matching sample Page 2 table!)
tbl_shape = s2.shapes.add_table(7, 3, Inches(3.25), Inches(3.66), Inches(4.35), Inches(1.92))
tbl = tbl_shape.table
tbl.columns[0].width = Inches(1.35)
tbl.columns[1].width = Inches(1.45)
tbl.columns[2].width = Inches(1.55)
rows_data = [
    ("FEATURE CORE", "TRADITIONAL / APPS", "SURYASUGAM D2C"),
    ("Order Fee", "20–30% Cut + GST", "₹0 (Direct WhatsApp)"),
    ("Language", "English Only", "Bilingual EN ↔ हिंदी"),
    ("Bulk Catering", "Manual Calls", "1–500 Pc Web Form"),
    ("Reviews", "Delayed / Hidden", "Live SSE Stream"),
    ("Customer Data", "Owned by App", "Owned in SQLite DB"),
    ("Fulfillment", "Delayed Payouts", "Instant UPI / Cash"),
]
for r_idx, row in enumerate(rows_data):
    for c_idx, val in enumerate(row):
        cell = tbl.cell(r_idx, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_MINT if (r_idx == 0) else C_WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Calibri"
        p.font.size = Pt(7.8 if r_idx > 0 else 8.0)
        p.font.bold = (r_idx == 0 or c_idx == 0)
        if r_idx > 0 and c_idx == 1:
            p.font.color.rgb = C_RED
        elif r_idx > 0 and c_idx == 2:
            p.font.color.rgb = C_GREEN
        else:
            p.font.color.rgb = C_BLACK

# RIGHT SIDE: HOW IT WORKS + REAL WEB APP SCREENSHOTS
pill(s2, 6.2, 0.72, 1.55, 0.3, "HOW IT WORKS", bg=C_BLACK, fg=C_WHITE, fs=10)
tb(s2, 7.9, 0.72, 4.9, 0.32, "Bilingual UI + structured WhatsApp checkout in <30 seconds", fs=9, bold=True, color=C_NAVY)

# 2 Screenshot frames side-by-side
rect(s2, 7.68, 1.15, 2.68, 2.15, fill=C_BLACK, rounded=True)
if os.path.exists(HOME_IMG):
    s2.shapes.add_picture(HOME_IMG, Inches(7.74), Inches(1.22), width=Inches(2.56))
tb(s2, 7.75, 3.32, 2.55, 0.25, "LIVE STOREFRONT (HOME)", fs=8.5, bold=True, color=C_RED, align=PP_ALIGN.CENTER)

rect(s2, 10.45, 1.15, 2.68, 2.15, fill=C_BLACK, rounded=True)
if os.path.exists(PROD_IMG):
    s2.shapes.add_picture(PROD_IMG, Inches(10.51), Inches(1.22), width=Inches(2.56))
tb(s2, 10.52, 3.32, 2.55, 0.25, "PRODUCT CONFIG & SSE", fs=8.5, bold=True, color=C_RED, align=PP_ALIGN.CENTER)

# Callout boxes left/around screenshots
callouts = [
    (5.75, 1.18, 1.82, 0.62, "HERO CAROUSEL & 1-CLICK WHATSAPP", C_MINT),
    (5.75, 1.92, 1.82, 0.68, "INSTANT EN / हिंदी LANGUAGE SWITCH", C_GREY_BG),
    (5.75, 2.72, 1.82, 0.68, "CUSTOM CATERING (1–500 PACKS)", C_CREAM),
    (7.75, 3.68, 2.55, 0.56, "IST DATE + 4 TIME SLOTS VALIDATION", C_SKY),
    (10.48, 3.68, 2.62, 0.56, "LIVE SSE REVIEWS & SQLITE PERSISTENCE", C_MINT),
    (7.75, 4.34, 5.35, 0.45, "CART PERSISTED VIA HTTP-ONLY COOKIE → ONE-CLICK WHATSAPP PAYLOAD", C_CREAM),
]
for l, t, w, h, txt, bgc in callouts:
    c = rect(s2, l, t, w, h, fill=bgc, border=C_BORDER, bw=0.9)
    c.line.dash_style = 3
    tb(s2, l + 0.05, t + 0.04, w - 0.1, h - 0.08, txt, fs=8.2, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)

# Bottom 4 summary strips (matching Sample Page 2 bottom bar)
bot_pillars = [
    ("Zero-MDR Direct", "Routes pre-formatted order text straight to WhatsApp (+91 89219 86080).", C_GREEN),
    ("Bilingual EN/HI", "Zero-reload translation stored in localStorage for regional shoppers.", C_NAVY),
    ("SQLite WAL Store", "7 relational tables track carts, orders, custom requests & events.", C_CLAY),
    ("Container Ready", "Multi-stage .NET 10 Docker image with /health probe & proxy headers.", C_BLACK),
]
for i, (ht, bd, col) in enumerate(bot_pillars):
    x = 0.22 + i * 3.25
    rect(s2, x, 5.75, 0.42, 0.42, fill=col, rounded=True)
    tb(s2, x, 5.81, 0.42, 0.3, f"0{i+1}", fs=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    tb(s2, x + 0.48, 5.72, 2.65, 0.24, ht, fs=9.8, bold=True, color=C_BLACK)
    tb(s2, x + 0.48, 5.96, 2.65, 0.9, bd, fs=8.5, color=C_MUTED)


# ==============================================================================
# SLIDE 3: TECHNICAL APPROACH (MATCHING SAMPLE PAGE 3)
# ==============================================================================
s3 = prs.slides.add_slide(blank)
add_header_and_footer(s3, "TECHNICAL APPROACH", 3)

# Left container: METHODOLOGY AND PROCESS
rect(s3, 0.2, 0.78, 3.15, 4.45, fill=C_WHITE, border=C_BORDER, bw=1.2, rounded=True)
pill(s3, 0.38, 0.66, 2.75, 0.34, "METHODOLOGY & IMPLEMENTATION", bg=C_BLACK, fg=C_WHITE, fs=9.5)

meths = [
    ("Bilingual DOM Engine", "Zero-reload English ↔ Hindi switching via data-en/data-hi & localStorage.", C_MINT),
    ("IST Date & Validation", "Asia/Kolkata timezone checks prevent past dates across UTC containers.", C_CREAM),
    ("SSE Channel Stream", "System.Threading.Channels (32-item bounded) pushes live comments.", C_SKY),
    ("SQLite WAL Store", "EF Core 10 + SQLite WAL mode with busy_timeout=5000 & DataProtection keys.", C_LAV),
]
for i, (mt, md, bgc) in enumerate(meths):
    y = 1.12 + i * 1.0
    rect(s3, 0.35, y, 2.85, 0.88, fill=bgc, border=C_BORDER, bw=0.8)
    tb(s3, 0.42, y + 0.04, 2.7, 0.24, mt, fs=10, bold=True, color=C_BLACK)
    tb(s3, 0.42, y + 0.28, 2.7, 0.56, md, fs=8.6, color=C_MUTED)

# Bottom-left box: SECURITY & RESILIENCE
rect(s3, 0.2, 5.4, 3.15, 1.55, fill=C_WHITE, border=C_BORDER, bw=1.2, rounded=True)
pill(s3, 0.55, 5.26, 2.45, 0.3, "SECURITY & RESILIENCE", bg=C_BLACK, fg=C_WHITE, fs=9.5)
rect(s3, 0.32, 5.65, 2.9, 0.56, fill=C_PINK)
tb(s3, 0.38, 5.68, 2.78, 0.5, "CSRF & DataProtection – ValidateAntiForgeryToken + App_Data/keys.", fs=8.5, bold=True)
rect(s3, 0.32, 6.28, 2.9, 0.56, fill=C_PINK)
tb(s3, 0.38, 6.31, 2.78, 0.5, "Proxy Ready – ForwardedHeaders (X-Forwarded-Proto) for HTTPS cookies.", fs=8.5, bold=True)

# Center container: SYSTEM PIPELINE & BENEFITS
rect(s3, 3.52, 1.05, 6.45, 5.9, fill=C_WHITE, border=C_BORDER, bw=1.2, rounded=True)
pill(s3, 5.85, 0.88, 1.8, 0.34, "SYSTEM PIPELINE", bg=C_BLACK, fg=C_WHITE, fs=10)

pipe_rows = [
    ("01 Storefront UI", "4 categories, hero carousel, EN/HI toggle & local imagery.", "HTML5 / CSS3 → Vanilla JS", C_CREAM),
    ("02 Product Config", "Size, Eggless/Regular, City/Area, IST Date, Time Slot & Note.", "ModelState → AntiForgery", C_SKY),
    ("03 Persistent Cart", "HttpOnly .SuryaSugam.Customer cookie links cart rows in SQLite.", "Cookie ID → CartItems Table", C_MINT),
    ("04 Live SSE Comments", "POST comment saves to DB + broadcasts to open EventSource tabs.", "Channels → text/event-stream", C_LAV),
    ("05 Checkout & Custom", "Saves CustomerOrders / CustomOrders & redirects to wa.me payload.", "SQLite Log → WhatsApp API", C_CREAM),
]
for i, (pt_t, pt_d, flow_lbl, bgc) in enumerate(pipe_rows):
    y = 1.25 + i * 1.12
    if i > 0:
        rect(s3, 3.65, y - 0.08, 6.15, 0.015, fill=C_BORDER)
    pill(s3, 3.68, y + 0.18, 0.48, 0.48, f"0{i+1}", bg=C_NAVY, fg=C_WHITE, fs=11)
    tb(s3, 4.25, y + 0.04, 3.15, 0.25, pt_t, fs=10.5, bold=True, color=C_NAVY)
    tb(s3, 4.25, y + 0.30, 3.15, 0.65, pt_d, fs=8.8, color=C_BLACK)
    rect(s3, 7.52, y + 0.14, 2.3, 0.62, fill=bgc, border=C_BORDER, bw=0.8, rounded=True)
    tb(s3, 7.56, y + 0.26, 2.22, 0.4, flow_lbl, fs=8.6, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)

# Right column: TECHNOLOGY STACK + OUTPUTS
rect(s3, 10.12, 0.98, 3.02, 4.45, fill=C_WHITE, border=C_BORDER, bw=1.2, rounded=True)
pill(s3, 10.55, 0.82, 2.15, 0.32, "TECHNOLOGY STACK", bg=C_BLACK, fg=C_WHITE, fs=9.5)

stack_rows = [
    ("FRONTEND UI", "Razor Views + Vanilla JS + CSS"),
    ("BACKEND API", "ASP.NET Core MVC (.NET 10)"),
    ("ORM & STORAGE", "EF Core 10 + SQLite WAL"),
    ("REAL-TIME SSE", "System.Threading.Channels"),
    ("SECURITY", "AntiForgery + DataProtection"),
    ("HOSTING", "Multi-Stage Docker (:8080)"),
    ("HEALTH PROBE", "GET /health + Proxy Headers"),
]
for i, (sk, sv) in enumerate(stack_rows):
    y = 1.22 + i * 0.58
    rect(s3, 10.24, y, 2.78, 0.48, fill=C_GREY_BG, border=C_BORDER, bw=0.7, rounded=True)
    tb(s3, 10.28, y + 0.08, 1.05, 0.32, sk, fs=7.8, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)
    tb(s3, 11.34, y + 0.08, 1.64, 0.34, sv, fs=8.2, bold=True, color=C_BLACK)

rect(s3, 10.12, 5.65, 3.02, 1.3, fill=C_WHITE, border=C_BORDER, bw=1.2, rounded=True)
pill(s3, 10.45, 5.5, 2.35, 0.3, "ENDPOINTS & OUTPUTS", bg=C_BLACK, fg=C_WHITE, fs=9)
outs = ["GET /", "Product", "SSE Live", "Cart", "/health"]
for i, o in enumerate(outs):
    x = 10.2 + i * 0.57
    rect(s3, x, 5.95, 0.53, 0.78, fill=C_SKY, border=C_BORDER, bw=0.7, rounded=True)
    tb(s3, x, 6.18, 0.53, 0.4, o, fs=7.2, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)


# ==============================================================================
# SLIDE 4: FEASIBILITY AND VIABILITY (MATCHING SAMPLE PAGE 4)
# ==============================================================================
s4 = prs.slides.add_slide(blank)
add_header_and_footer(s4, "FEASIBILITY AND VIABILITY", 4)

# Left panel: FEASIBILITY
rect(s4, 0.22, 0.9, 6.35, 6.08, fill=C_WHITE, border=C_BLACK, bw=1.4)
pill(s4, 2.05, 0.72, 1.85, 0.34, "FEASIBILITY", bg=C_BLACK, fg=C_WHITE, fs=10.5)

feas = [
    ("TECHNICAL FEASIBILITY", "Built on production .NET 10 + SQLite WAL + Channels SSE with zero heavy JS bundles or external DB server cost."),
    ("OPERATIONAL FEASIBILITY", "Zero training needed: orders arrive as structured WhatsApp messages in Hindi/English matching existing kitchen workflow."),
    ("ECONOMIC FEASIBILITY", "Runs on a single lightweight container (~$5–$7/mo or free tier) and saves 20–30% aggregator commissions on every order."),
    ("REGULATORY FEASIBILITY", "Aligned with FSSAI / Nagar Palika Mathura Food Safety Zone 2 disclosure, transparent tax-inclusive pricing & Privacy Policy."),
]
for i, (ft, fd) in enumerate(feas):
    y = 1.15 + i * 0.88
    pill(s4, 2.15, y, 2.3, 0.26, ft, bg=C_SKY, fg=C_NAVY, fs=8.8)
    rect(s4, 0.95, y + 0.27, 5.45, 0.54, fill=C_GREY_BG)
    tb(s4, 1.02, y + 0.29, 5.32, 0.5, fd, fs=8.6, color=C_BLACK)
    pill(s4, 0.35, y + 0.18, 0.52, 0.52, f"0{i+1}", bg=C_CLAY, fg=C_WHITE, fs=11)

# Stacked bar chart + Viability blurbs
if os.path.exists(CHART4_IMG):
    s4.shapes.add_picture(CHART4_IMG, Inches(0.32), Inches(4.78), width=Inches(3.75))
tb(s4, 4.18, 4.82, 2.25, 0.95, "Market Viability\nTier-2/3 direct D2C bakery demand & WhatsApp commerce enable high-repeat chai-time orders.", fs=8.5, color=C_BLACK)
tb(s4, 4.18, 5.82, 2.25, 1.0, "Sustainable Viability\n66.5%–70% gross margins + Negative Cash Conversion Cycle (-13 days) self-fund growth.", fs=8.5, color=C_BLACK)

# Right panel: CHALLENGES & MITIGATIONS
rect(s4, 6.75, 0.9, 6.35, 6.08, fill=C_WHITE, border=C_BLACK, bw=1.4)
pill(s4, 8.2, 0.72, 2.35, 0.34, "CHALLENGES & SOLUTIONS", bg=C_BLACK, fg=C_WHITE, fs=10)

groups = [
    ("Adapting local Mathura shoppers & seamless adoption", [
        ("Language Barriers", "Instant EN ↔ हिंदी toggle across UI & WhatsApp."),
        ("Mobile 4G Speed", "Vanilla JS & local assets load fast without frameworks."),
        ("Bulk Event Orders", "Custom order engine accepts 1–500 packs easily."),
        ("Timezone Drift", "Asia/Kolkata IST date check avoids UTC mismatch."),
    ], 1.15),
    ("Ensuring storefront reliability & zero downtime", [
        ("Concurrent Writes", "SQLite WAL + busy_timeout=5000 prevents locks."),
        ("Proxy HTTPS Cookies", "ForwardedHeaders preserves Secure cookie flags."),
        ("Idle SSE Drops", "25s keepalive heartbeats sustain live comment streams."),
        ("Container Restarts", "DataProtection keys saved safely in App_Data/keys."),
    ], 3.1),
]
for g_title, cards, gy in groups:
    tb(s4, 6.9, gy, 6.0, 0.28, g_title, fs=10, bold=True, color=C_BLACK)
    for idx, (ct, cd) in enumerate(cards):
        col_i = idx % 2
        row_i = idx // 2
        cx = 6.92 + col_i * 3.05
        cy = gy + 0.32 + row_i * 0.72
        rect(s4, cx, cy, 0.42, 0.42, fill=C_NAVY, rounded=True)
        tb(s4, cx, cy + 0.08, 0.42, 0.25, "✓", fs=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
        tb(s4, cx + 0.48, cy - 0.02, 2.48, 0.24, ct, fs=9.2, bold=True, color=C_BLACK)
        tb(s4, cx + 0.48, cy + 0.2, 2.48, 0.48, cd, fs=8.2, color=C_MUTED)

# Bottom-right showcase: Live Categories Screenshot
tb(s4, 6.9, 5.0, 6.0, 0.26, "Live 4-Category Storefront Proof (Including Custom Orders)", fs=9.5, bold=True, color=C_CLAY)
rect(s4, 6.92, 5.28, 5.95, 1.6, fill=C_GREY_BG, border=C_BORDER, bw=1)
if os.path.exists(CAT_IMG):
    s4.shapes.add_picture(CAT_IMG, Inches(7.02), Inches(5.33), height=Inches(1.5))
tb(s4, 9.95, 5.42, 2.8, 1.35, "• Fans (₹145–₹180)\n• CreamRoll (₹60)\n• Toast (₹100–₹150)\n• Special Request (1–500)\n100% Self-Hosted Images", fs=9, bold=True, color=C_BLACK)


# ==============================================================================
# SLIDE 5: IMPACTS AND BENEFITS (MATCHING SAMPLE PAGE 5)
# ==============================================================================
s5 = prs.slides.add_slide(blank)
add_header_and_footer(s5, "IMPACTS AND BENEFITS", 5)

# Top 3 rounded pastel cards
top3 = [
    ("Economic Benefits", C_CREAM, [
        "• Saves 20–30% aggregator commission per order",
        "• 0% Payment Gateway MDR via direct WhatsApp/UPI",
        "• Negative Cash Conversion Cycle (-13 days)",
        "• High 66.5%–70% gross margin across 7 SKUs",
        "• 10x Average Order Value via Custom Catering",
    ]),
    ("Customer & Community Benefits", C_SKY, [
        "• Instant English & Hindi bilingual interface",
        "• Fresh morning batches with Mathura slot choice",
        "• Clear Eggless / Regular dietary selection",
        "• Live real-time customer reviews before buying",
        "• Direct baker note customization (40 chars)",
    ]),
    ("Operational & Quality Benefits", C_MINT, [
        "• Structured order payloads cut phone mistakes",
        "• Complete audit trail in 7 SQLite WAL tables",
        "• Zero-login friction using 365-day HttpOnly cookie",
        "• Baked-to-order catering eliminates stale waste",
        "• Single Docker deployment keeps ops ultra-lean",
    ]),
]
for i, (t3, bgc, pts) in enumerate(top3):
    x = 0.22 + i * 4.35
    rect(s5, x, 0.85, 4.18, 1.55, fill=bgc, border=C_NAVY, bw=1.2, rounded=True)
    tb(s5, x + 0.1, 0.9, 3.98, 0.28, t3, fs=11, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)
    bx = s5.shapes.add_textbox(Inches(x + 0.12), Inches(1.18), Inches(3.95), Inches(1.18))
    add_bullets(bx, pts, fs=8.3, space=1.5)

pill(s5, 0.22, 2.52, 2.75, 0.28, "STAKEHOLDERS & ORDER FLOW", bg=C_BLACK, fg=C_WHITE, fs=9.5)

# 4-step workflow with dashed callouts
steps = [
    ("1", "Browse & EN/HI", "Select Fans, CreamRoll, Toast or Custom Request.", "CUSTOMER", "Opens storefront in English or हिंदी"),
    ("2", "Configure & Cart", "Pick Size, Eggless, City, IST Date, Slot & Baker Note.", "WEB STOREFRONT", "Validates inputs & stores CartItems"),
    ("3", "Order & Log", "Checkout saves CustomerOrders & Audit Events.", "SQLITE + SSE", "Tracks order & broadcasts live reviews"),
    ("4", "WhatsApp Bake", "1-click pre-filled WhatsApp sent to kitchen.", "BAKERY KITCHEN", "Confirms fresh bake & UPI delivery"),
]
for i, (num, st_t, st_d, actor, top_note) in enumerate(steps):
    x = 0.25 + i * 3.25
    d_top = rect(s5, x + 0.2, 2.9, 2.85, 0.62, fill=C_WHITE, border=C_BORDER, bw=1)
    d_top.line.dash_style = 3
    tb(s5, x + 0.25, 2.94, 2.75, 0.54, top_note, fs=8.5, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)

    pill(s5, x + 0.1, 3.72, 0.36, 0.36, num, bg=C_CLAY, fg=C_WHITE, fs=11)
    tb(s5, x + 0.52, 3.66, 2.4, 0.24, st_t, fs=10, bold=True, color=C_NAVY)
    tb(s5, x + 0.52, 3.90, 2.4, 0.52, st_d, fs=8.4, color=C_BLACK)
    tb(s5, x + 0.1, 4.46, 2.8, 0.22, actor, fs=8.5, bold=True, color=C_CLAY, align=PP_ALIGN.CENTER)

    if i < 3:
        tb(s5, x + 2.98, 3.85, 0.3, 0.3, "➜", fs=14, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)

# Bottom 4 dashed impact boxes + Custom Order screenshot
imp_cards = [
    ("Zero Error Dispatch", "Structured WhatsApp messages replace manual phone notes."),
    ("Real-Time Trust", "Live SSE comments build social proof on product pages."),
    ("Audit-Ready Logs", "SQLite logs every cart, order, subscription & comment event."),
]
for i, (it, idesc) in enumerate(imp_cards):
    x = 0.22 + i * 2.85
    c = rect(s5, x, 4.78, 2.72, 0.88, fill=C_WHITE, border=C_BORDER, bw=1)
    c.line.dash_style = 3
    tb(s5, x + 0.08, 4.82, 2.56, 0.25, it, fs=9.5, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)
    tb(s5, x + 0.08, 5.08, 2.56, 0.54, idesc, fs=8.2, color=C_BLACK, align=PP_ALIGN.CENTER)

# Custom Order Screenshot preview on middle-right
rect(s5, 8.85, 4.75, 4.25, 2.25, fill=C_CREAM, border=C_CLAY, bw=1.2, rounded=True)
tb(s5, 8.95, 4.78, 4.05, 0.22, "SPECIAL REQUEST ENGINE (LIVE SCREENSHOT)", fs=8.2, bold=True, color=C_CLAY, align=PP_ALIGN.CENTER)
if os.path.exists(CUST_IMG):
    s5.shapes.add_picture(CUST_IMG, Inches(8.98), Inches(5.02), height=Inches(1.9))

# Bottom-left OUR PROMISE + KPI badges (matching Sample Page 5 bottom)
pill(s5, 0.22, 5.78, 1.45, 0.28, "OUR PROMISE", bg=C_BLACK, fg=C_WHITE, fs=9.5)
promises = [
    ("01", "FRESH\nDAILY", RGBColor(76, 159, 56)),
    ("02", "0% FEE\nD2C", RGBColor(162, 25, 66)),
    ("03", "EN ↔ HI\nACCESS", RGBColor(253, 105, 37)),
    ("04", "1–500\nCUSTOM", RGBColor(191, 139, 46)),
]
for i, (pn, pt, pcol) in enumerate(promises):
    x = 0.22 + i * 0.92
    rect(s5, x, 6.14, 0.85, 0.85, fill=pcol)
    tb(s5, x, 6.18, 0.85, 0.25, pn, fs=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    tb(s5, x + 0.03, 6.46, 0.79, 0.48, pt, fs=8.2, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

k1 = rect(s5, 4.0, 5.82, 2.35, 1.16, fill=C_CREAM, border=C_CLAY, bw=1)
tb(s5, 4.08, 5.9, 2.2, 1.0, "0% Commission\nvs 20–30% on food apps\nSaves ₹10,600+/mo", fs=10, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)
k2 = rect(s5, 6.48, 5.82, 2.22, 1.16, fill=C_MINT, border=C_GREEN, bw=1)
tb(s5, 6.55, 5.9, 2.08, 1.0, "66.5%–70% GM\n10x Catering AOV\n(₹2.5K–₹15K+)", fs=10, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)


# ==============================================================================
# SLIDE 6: CATALOG ECONOMICS, LIVE DELIVERABLES & BENCHMARKS (SAMPLE PAGE 6)
# ==============================================================================
s6 = prs.slides.add_slide(blank)
add_header_and_footer(s6, "CATALOG ECONOMICS, DELIVERABLES & BENCHMARKS", 6)

# Left-top: Unit Economics & Catalog Card
rect(s6, 0.22, 0.82, 6.25, 2.95, fill=C_GREY_BG, border=C_BLACK, bw=1.2, rounded=True)
tb(s6, 0.35, 0.88, 6.0, 0.28, "CATALOG PRICING & UNIT ECONOMICS", fs=12, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)

rect(s6, 0.35, 1.24, 2.92, 2.38, fill=C_WHITE, border=C_BORDER, bw=0.9, rounded=True)
tb(s6, 0.42, 1.3, 2.78, 0.24, "Core Tea-Time SKUs (7 Items)", fs=9.5, bold=True, color=C_NAVY)
b_sku = s6.shapes.add_textbox(Inches(0.42), Inches(1.56), Inches(2.78), Inches(2.0))
add_bullets(b_sku, [
    "• Mini Fan (fan-puff): ₹145 (Bestseller)",
    "• Standard Fan (masala-fan): ₹160",
    "• Large Fan (paneer-fan): ₹180 (New)",
    "• CreamRoll (creamroll): ₹60 (Hero SKU)",
    "• Mini Toast (milk-toast): ₹100",
    "• Standard / Large Toast: ₹120 / ₹150",
], fs=8.3, space=2.5)

rect(s6, 3.38, 1.24, 2.95, 2.38, fill=C_WHITE, border=C_BORDER, bw=0.9, rounded=True)
tb(s6, 3.45, 1.3, 2.8, 0.24, "Margin & Cash Cycle Drivers", fs=9.5, bold=True, color=C_NAVY)
b_drv = s6.shapes.add_textbox(Inches(3.45), Inches(1.56), Inches(2.8), Inches(2.0))
add_bullets(b_drv, [
    "• Blended Gross Margin: ~68.5%",
    "• Dough Expansion Yield: High ROI",
    "• Negative CCC: -13 Days (Self-funded)",
    "• Inventory Turn: 24–48 hrs fresh cycle",
    "• Custom Orders: 1–500 pcs high ticket",
    "• FSSAI Zone 2 Mathura compliant",
], fs=8.3, space=2.5)

# Left-bottom: MARKET RESEARCH (TAM / SAM / SOM + Revenue Table)
rect(s6, 0.22, 3.92, 6.25, 3.08, fill=C_CREAM, border=C_BLACK, bw=1.2, rounded=True)
tb(s6, 0.35, 3.98, 6.0, 0.26, "MARKET OPPORTUNITY — MATHURA & REGIONAL EXPANSION", fs=11, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)
tb(s6, 0.35, 4.3, 2.35, 1.3, "Addressable Opportunity\nTAM: Indian Bakery & Tea-Time Snacks\nSAM: Mathura & Braj Urban Households\nSOM: Direct WhatsApp Repeat Base", fs=8.3, color=C_BLACK)
if os.path.exists(TAMSAM_IMG):
    s6.shapes.add_picture(TAMSAM_IMG, Inches(2.75), Inches(4.28), width=Inches(1.45))

rect(s6, 4.3, 4.32, 2.02, 1.38, fill=C_WHITE, border=C_BORDER, bw=0.8, rounded=True)
tb(s6, 4.35, 4.38, 1.92, 1.28, "Sample Target Mix:\n• Daily Retail: ₹250 AOV\n• Catering: ₹2.5K–₹15K\n• 0% MDR Retained\n• 100% Owned CRM", fs=8.4, bold=True, color=C_NAVY)

tb(s6, 0.35, 5.82, 6.0, 1.05, "Illustrative Monthly Scale (Mathura Launch): 400 Retail Orders × ₹250 (₹1,00,000) + 12 Custom Catering Orders × ₹5,000 (₹60,000) = ₹1,60,000/mo gross sales with ₹0 aggregator fee leakage.", fs=9.2, bold=True, color=C_BLACK)

# Right-top: LIVE WEB APP DELIVERABLES (CART & PRODUCT SCREENSHOTS)
rect(s6, 6.62, 0.82, 6.5, 2.45, fill=C_MINT, border=C_BLACK, bw=1.2, rounded=True)
pill(s6, 8.45, 0.68, 2.8, 0.28, "LIVE WEB APP DELIVERABLES", bg=C_GREEN, fg=C_WHITE, fs=9.5)

rect(s6, 6.78, 1.08, 3.0, 1.85, fill=C_WHITE, border=C_BORDER, bw=0.9)
if os.path.exists(CART_IMG):
    s6.shapes.add_picture(CART_IMG, Inches(6.84), Inches(1.14), width=Inches(2.88))
tb(s6, 6.78, 2.96, 3.0, 0.24, "Persistent Shopping Cart (/cart)", fs=8.5, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)

rect(s6, 9.95, 1.08, 3.0, 1.85, fill=C_WHITE, border=C_BORDER, bw=0.9)
if os.path.exists(HOME_IMG):
    s6.shapes.add_picture(HOME_IMG, Inches(10.01), Inches(1.14), width=Inches(2.88))
tb(s6, 9.95, 2.96, 3.0, 0.24, "Bilingual Storefront (/)", fs=8.5, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)

# Right-middle: ARCHITECTURE REFERENCES
rect(s6, 6.62, 3.42, 6.5, 2.02, fill=C_SKY, border=C_BLACK, bw=1.2, rounded=True)
tb(s6, 6.75, 3.48, 6.2, 0.24, "ARCHITECTURE & ENGINEERING REFERENCES", fs=10, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)
refs = [
    ("ASP.NET Core .NET 10", "MVC + Minimal APIs, Top-Level Statements, Response Caching."),
    ("EF Core 10 + SQLite WAL", "7 indexed tables + busy_timeout=5000 + DataProtection keys."),
    ("Channels SSE + Cookie ID", "Real-time comments stream + 365-day HttpOnly browser identity."),
    ("Docker + /health Probe", "Multi-stage container on port 8080 + ForwardedHeaders proxy support."),
]
for i, (rt, rd) in enumerate(refs):
    col_i = i % 2
    row_i = i // 2
    rx = 6.78 + col_i * 3.12
    ry = 3.78 + row_i * 0.78
    rect(s6, rx, ry, 2.98, 0.68, fill=C_WHITE, border=C_BORDER, bw=0.8, rounded=True)
    tb(s6, rx + 0.08, ry + 0.04, 2.82, 0.22, rt, fs=8.8, bold=True, color=C_NAVY)
    tb(s6, rx + 0.08, ry + 0.26, 2.82, 0.38, rd, fs=7.8, color=C_MUTED)

# Right-bottom: COMPETITIVE BENCHMARKS
rect(s6, 6.62, 5.58, 6.5, 1.42, fill=C_LAV, border=C_BLACK, bw=1.2, rounded=True)
tb(s6, 6.75, 5.62, 6.2, 0.24, "COMPETITIVE BENCHMARKS", fs=10, bold=True, color=C_BLACK, align=PP_ALIGN.CENTER)
rect(s6, 6.78, 5.9, 3.0, 0.56, fill=C_WHITE, border=C_BORDER, bw=0.8, rounded=True)
tb(s6, 6.86, 5.93, 2.84, 0.5, "Swiggy / Zomato: 20–30% commission cut + delayed settlements.", fs=8.2, color=C_RED, bold=True)
rect(s6, 9.95, 5.9, 3.0, 0.56, fill=C_WHITE, border=C_BORDER, bw=0.8, rounded=True)
tb(s6, 10.03, 5.93, 2.84, 0.5, "Static Brochure Sites: No cart, no DB audit, no live reviews.", fs=8.2, color=C_MUTED, bold=True)
rect(s6, 6.78, 6.52, 6.17, 0.38, fill=C_WHITE, border=C_GREEN, bw=1.2, rounded=True)
tb(s6, 6.86, 6.56, 6.0, 0.3, "SURYASUGAM D2C: ₹0 Commission • Bilingual EN/HI • Live SSE • Custom Catering (1–500 pcs)", fs=8.8, bold=True, color=C_GREEN, align=PP_ALIGN.CENTER)

prs.save(OUT_PPTX)
print("SUCCESS: Generated 6-slide infographic deck ->", OUT_PPTX)

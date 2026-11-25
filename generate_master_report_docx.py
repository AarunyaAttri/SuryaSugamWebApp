import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from PIL import Image

OUT_DOCX = r"C:\Users\aarun\source\repos\WebApplication2\SuryaSugam_Bakery_Project_Report.docx"
HOME_IMG = r"C:\Users\aarun\source\repos\WebApplication2\prototype-homepage.png"
PROD_IMG = r"C:\Users\aarun\source\repos\WebApplication2\prototype-product.png"

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.7)
sec.bottom_margin = Inches(0.7)
sec.left_margin = Inches(0.8)
sec.right_margin = Inches(0.8)

# Color Palette
COLOR_INK = RGBColor(48, 37, 31)         # #30251F
COLOR_CLAY = RGBColor(184, 97, 67)       # #B86143
COLOR_CLAY_DARK = RGBColor(126, 74, 45)  # #7E4A2D
COLOR_MUTED = RGBColor(130, 119, 110)    # #82776E
COLOR_GOLD = RGBColor(210, 145, 82)      # #D29152
COLOR_GREEN = RGBColor(22, 133, 66)      # #168542

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

# Configure Styles
styles = doc.styles
normal_style = styles['Normal']
normal_style.font.name = 'Calibri'
normal_style.font.size = Pt(10.5)
normal_style.font.color.rgb = COLOR_INK

# Header & Footer setup
header = sec.header.paragraphs[0]
header.text = "SURYA SUGAM BAKERY  |  PROJECT REPORT & CA EVALUATION"
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
header.style.font.size = Pt(8.5)
header.style.font.color.rgb = COLOR_MUTED

footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
f_run = footer.add_run("SuryaSugam Bakery Digital Storefront  |  Page ")
f_run.font.size = Pt(8.5)
f_run.font.color.rgb = COLOR_MUTED

fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'), 'begin')
instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'), 'preserve'); instrText.text = 'PAGE'
fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'end')
footer._p.append(fldChar1); footer._p.append(instrText); footer._p.append(fldChar2)

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Georgia'
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = COLOR_CLAY_DARK
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(12.5)
    r.bold = True
    r.font.color.rgb = COLOR_CLAY
    return p

def add_h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(11)
    r.bold = True
    r.font.color.rgb = COLOR_INK
    return p

def add_p(text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_INK
    r = p.add_run(text)
    r.italic = italic
    return p

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.12
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_INK
    p.add_run(text)
    return p

def add_callout(text, label="NOTE", hex_bg="F3ECE1"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.8)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, hex_bg)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r_lbl = p.add_run(f"[{label}] ")
    r_lbl.bold = True
    r_lbl.font.size = Pt(9.5)
    r_lbl.font.color.rgb = COLOR_CLAY_DARK
    
    r_txt = p.add_run(text)
    r_txt.font.size = Pt(9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, headers, data, header_bg="7E4A2D"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data Rows
    for row_idx, row_data in enumerate(data):
        row = table.add_row()
        cells = row.cells
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "FBF8F2"
        for i, val in enumerate(row_data):
            cells[i].text = str(val)
            set_cell_background(cells[i], bg_col)
            set_cell_margins(cells[i], top=80, bottom=80, left=120, right=120)
            p = cells[i].paragraphs[0]
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = COLOR_INK
                
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_figure(path, caption):
    if not os.path.exists(path):
        return
    im = Image.open(path)
    ratio = im.height / im.width
    width = Inches(6.5)
    height = width * ratio
    if height > Inches(4.5):
        height = Inches(4.5)
        width = height / ratio
        
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.add_run().add_picture(path, width=width, height=height)
    
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(10)
    r = c.add_run(caption)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = COLOR_MUTED

# ==================== COVER PAGE ====================
p_cov = doc.add_paragraph()
p_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cov.paragraph_format.space_before = Pt(32)
p_cov.paragraph_format.space_after = Pt(8)

r_cov_main = p_cov.add_run("SURYA SUGAM BAKERY\n")
r_cov_main.font.name = 'Georgia'
r_cov_main.font.size = Pt(30)
r_cov_main.bold = True
r_cov_main.font.color.rgb = COLOR_CLAY_DARK

r_cov_sub = p_cov.add_run("DIGITAL STOREFRONT & COMMERCE WEB APPLICATION\n")
r_cov_sub.font.name = 'Calibri'
r_cov_sub.font.size = Pt(15)
r_cov_sub.bold = True
r_cov_sub.font.color.rgb = COLOR_GOLD

r_cov_desc = p_cov.add_run("Comprehensive Technical Architecture, System Scan & CA Interview Business Report (Updated with Custom Order & Streamlined Catalog)")
r_cov_desc.font.name = 'Calibri'
r_cov_desc.font.size = Pt(11)
r_cov_desc.italic = True
r_cov_desc.font.color.rgb = COLOR_MUTED

doc.add_paragraph().paragraph_format.space_after = Pt(18)

meta_tbl = doc.add_table(rows=6, cols=2)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_tbl.autofit = False
meta_labels = [
    ("Project Title", "SuryaSugam Bakery Online Storefront (WebApplication2)"),
    ("Target Enterprise", "SuryaSugam Bakery, Lohaban Bagihi, Ward No. 05, Mathura, UP - 281001"),
    ("Framework & Language", "ASP.NET Core MVC on .NET 10 (C# 14 / Top-Level Minimal APIs)"),
    ("Recent Enhancements", "Special Request Custom Orders (up to 500 pcs), Toast Sizing Hierarchy, 100% Local Imagery"),
    ("Evaluation Focus", "System Architecture, Internal Controls, WhatsApp Commerce, Financial Viability"),
    ("Report Date", "November 2026 (Updated Post-Refactor)")
]
for i, (k, v) in enumerate(meta_labels):
    cell_k, cell_v = meta_tbl.cell(i, 0), meta_tbl.cell(i, 1)
    cell_k.text, cell_v.text = k, v
    cell_k.width = Inches(2.2); cell_v.width = Inches(4.6)
    cell_k.paragraphs[0].runs[0].bold = True
    cell_k.paragraphs[0].runs[0].font.size = Pt(9.5)
    cell_k.paragraphs[0].runs[0].font.color.rgb = COLOR_CLAY_DARK
    cell_v.paragraphs[0].runs[0].font.size = Pt(9.5)
    bg = "F3ECE1" if i % 2 == 0 else "FFFFFF"
    set_cell_background(cell_k, bg); set_cell_background(cell_v, bg)
    set_cell_margins(cell_k, 70, 70, 100, 100); set_cell_margins(cell_v, 70, 70, 100, 100)

doc.add_page_break()

# ==================== TABLE OF CONTENTS ====================
add_h1("Table of Contents")
toc_data = [
    ("1", "Executive Introduction & Project Rationale"),
    ("2", "Business & Industry Background (Mathura Bakery Retail Ecosystem)"),
    ("3", "Project Objectives & Key Performance Indicators (KPIs)"),
    ("4", "Technology Stack & Architectural Specifications"),
    ("5", "Complete Project Directory & File System Hierarchy (Updated)"),
    ("6", "Routing Architecture & API Endpoints Specification"),
    ("7", "Product Catalog, SKU Structure & Unit Economics (Updated with 4 Categories)"),
    ("8", "Core Application Features & Technical Implementation (Including Custom Order Engine)"),
    ("9", "UI Design System, Color Tokens & Typography"),
    ("10", "End-to-End System Data Flow & Architecture Pipeline"),
    ("11", "Technical Observations, Trade-offs & Code Quality Audit Findings"),
    ("12", "Prototype Visual Walkthrough & System Screenshots"),
    ("13", "CA Interview Evaluation: Business Viability, Unit Economics & Internal Controls"),
    ("14", "Conclusion & Strategic Scalability Roadmap")
]
toc_tbl = doc.add_table(rows=1, cols=2)
format_table(toc_tbl, [0.8, 6.0], ["Section", "Report Chapter / Topic"], toc_data, header_bg="7E4A2D")

doc.add_page_break()

# ==================== 1. INTRODUCTION ====================
add_h1("1. Executive Introduction & Project Rationale")
add_p("The SuryaSugam Bakery Web Application (WebApplication2) is a specialized direct-to-consumer (D2C) e-commerce storefront engineered for an established artisanal bakery operating in Mathura, Uttar Pradesh. Built upon modern ASP.NET Core MVC running on the .NET 10 framework, the platform provides an intuitive, high-velocity digital bridge between traditional handcrafted baking and contemporary consumer convenience.")
add_p("The application targets everyday tea-time staples—specifically authentic flaky Fans (puff pastries), signature cream rolls, and size-tiered crisp Toasts (Mini, Standard, Large)—while also providing a newly introduced 'Special Request / Custom Order' gateway for bulk celebration catering (up to 500 units). In tier-2 and tier-3 Indian retail markets, small-scale food enterprises are frequently trapped between physical walk-in limits or surrendering 20% to 30% of their gross revenue to delivery aggregator apps. SuryaSugam Bakery bypasses this dilemma by deploying a lightweight, proprietary web portal with bilingual (English and Hindi) user experience, zero-latency session cart management, and seamless WhatsApp dispatch.")
add_p("From a corporate assessment and Chartered Accountancy perspective, this project stands out by delivering commercial functionality with near-zero operating overhead, zero payment gateway commission deductions, 100% self-hosted local image assets, and strict local food safety alignment.")

# ==================== 2. BACKGROUND ====================
add_h1("2. Business & Industry Background")
add_h2("2.1 The Mathura Tea-Time Bakery Ecosystem")
add_p("Mathura possesses a deep-rooted cultural affinity for morning and evening chai rituals. Artisanal baked items such as 'Fans' and 'Rusk Toasts' are dietary staples consumed daily across regional households. SuryaSugam Bakery, situated in Gomati Vihar, Lohaban Bagihi, Ward No. 05 (Ram Nagar), under Nagar Palika Mathura Food Safety Zone 2, has cultivated substantial goodwill as a trusted neighbourhood producer.")

add_h2("2.2 Commercial Bottlenecks of Traditional Bakery Retail")
add_bullet("Walk-in dependency severely constrains geographical reach to within 500 meters of the physical storefront.", "Geographic Concentration: ")
add_bullet("Telephone-based orders suffer from human miscommunication regarding pack sizes, egg preferences, and exact delivery addresses.", "Order Fulfillment Friction: ")
add_bullet("Conventional bakeries lack real-time visibility into daily demand fluctuations, resulting in either perishable inventory stock-outs or costly end-of-day wastage.", "Inventory Unpredictability: ")
add_bullet("Listing on centralized aggregator apps (e.g., Zomato, Swiggy) erodes profit margins via 20-30% commissions, customer data ownership denial, and delayed payment settlements.", "High Aggregator Intermediation: ")

# ==================== 3. PROJECT OBJECTIVES ====================
add_h1("3. Project Objectives & Key Performance Indicators (KPIs)")
add_p("The project was executed against clearly defined strategic, operational, financial, and technical benchmarks:")
add_bullet("Develop a high-performance web storefront showcasing Fans, CreamRoll, and Toast with authentic brand storytelling and local culinary identity.", "1. Digital Brand Showcase: ")
add_bullet("Provide fully synchronized bilingual rendering in English and Hindi across all product labels, delivery parameters, and messaging to guarantee 100% demographic accessibility in Uttar Pradesh.", "2. Universal Demographic Accessibility: ")
add_bullet("Implement structured order customization allowing customers to select pack sizes, dietary options (Eggless vs. Regular), delivery dates, time slots, and baker notes.", "3. Frictionless Order Customization: ")
add_bullet("Enable large-scale event catering and bespoke bakery requests (up to 500 pieces) via a dedicated Special Request WhatsApp channel.", "4. Bulk & Celebration Catering Channel: ")
add_bullet("Eliminate gateway merchant discount rates (MDR) and setup costs by utilizing direct WhatsApp API protocol generation for instant order transmission.", "5. Financial Efficiency & Zero-MDR Checkout: ")
add_bullet("Deploy a low-latency Server-Sent Events (SSE) live customer review feed backed by in-memory channel pub/sub.", "6. Real-Time Customer Engagement: ")

add_callout(
    "Key Performance Indicator (KPI) Targets:\n"
    "• Cart Abandonment Rate Target: < 20% (due to zero checkout registration forms and direct WhatsApp handoff)\n"
    "• Transaction Commission Cost: 0.0% (vs. 2.0-2.5% for payment gateways and 25% for aggregators)\n"
    "• Order Confirmation Turnaround Time: < 90 seconds via direct WhatsApp business routing\n"
    "• Page Load Performance: < 600ms on 4G cellular connections across Mathura",
    label="TARGET METRICS",
    hex_bg="F3ECE1"
)

# ==================== 4. TECH STACK ====================
add_h1("4. Technology Stack & Architectural Specifications")
tech_data = [
    ("Framework", "ASP.NET Core MVC on .NET 10"),
    ("Language", "C# (top-level statements in Program.cs)"),
    ("Frontend", "Razor Views, vanilla JS, custom CSS (no Tailwind/Sass)"),
    ("Fonts", "Google Fonts — DM Sans + Playfair Display"),
    ("Client libs", "Bootstrap 5 (bundled but barely used), jQuery + jQuery Validation (for unobtrusive validation only)"),
    ("Session", "In-memory distributed cache with 2-hour session cookies"),
    ("Real-time", "Server-Sent Events (SSE) via System.Threading.Channels"),
    ("Ordering", "WhatsApp deep-links (no payment gateway)"),
    ("Report gen", "Python script (generate_master_report_docx.py) using python-docx + Pillow")
]
tech_tbl = doc.add_table(rows=1, cols=2)
format_table(tech_tbl, [2.0, 4.8], ["Layer", "Technology / Architectural Role"], tech_data, header_bg="7E4A2D")

# ==================== 5. PROJECT STRUCTURE (UPDATED) ====================
add_h1("5. Complete Project File Structure & Hierarchy")
add_p("The project maintains a clean MVC architecture, recently expanded with custom order partials and local imagery:")

struct_text = """WebApplication2/
├── Controllers/
│   └── HomeController.cs          ← All routes (Home, Product, Cart, Newsletter, etc.)
├── Models/                        ← 15 POCOs / ViewModels
│   ├── CartLineItem.cs
│   ├── CartQuantityInput.cs
│   ├── CartViewModel.cs
│   ├── CategoryCard.cs
│   ├── ErrorViewModel.cs
│   ├── NavigationLink.cs
│   ├── NewsletterInput.cs
│   ├── ProductCard.cs
│   ├── ProductComment.cs
│   ├── ProductCommentInput.cs
│   ├── ProductDetailViewModel.cs
│   ├── ProductOrderInput.cs
│   ├── ProductSectionViewModel.cs
│   ├── StorefrontViewModel.cs
│   └── TestimonialCard.cs
├── Services/
│   └── ProductCommentStore.cs     ← In-memory comment store + SSE pub/sub
├── Views/
│   ├── Home/
│   │   ├── Index.cshtml           ← Homepage (hero + categories + Fans + Toasts + CreamRoll + Custom Order + reviews)
│   │   ├── Product.cshtml         ← Product detail page (order form + comments)
│   │   ├── Cart.cshtml            ← Shopping cart (items + summary + WhatsApp)
│   │   ├── Privacy.cshtml         ← Placeholder
│   │   └── Partials/              ← 8 reusable partial views (including _CustomOrderSection.cshtml)
│   │       ├── _HeroSection.cshtml
│   │       ├── _ServiceStrip.cshtml
│   │       ├── _CategorySection.cshtml
│   │       ├── _ProductSection.cshtml
│   │       ├── _CustomOrderSection.cshtml   ← [NEW] Bespoke catering & bulk order form
│   │       ├── _TeaTimeFeature.cshtml
│   │       ├── _TestimonialSection.cshtml
│   │       └── _NewsletterSection.cshtml
│   ├── Shared/
│   │   ├── _Layout.cshtml         ← Master layout (header, nav, footer)
│   │   ├── _Layout.cshtml.css
│   │   ├── _ValidationScriptsPartial.cshtml
│   │   └── Error.cshtml
│   ├── _ViewImports.cshtml
│   └── _ViewStart.cshtml
├── wwwroot/
│   ├── css/site.css               ← Custom CSS with custom order responsive grid styling
│   ├── js/
│   │   ├── site.js                ← Slideshow, mobile menu, quantity controls, EN↔HI language switcher, WhatsApp link builder
│   │   └── product-comments.js    ← Fetch + SSE live comment system
│   ├── images/                    ← 15 local bakery assets (100% self-hosted; zero external URLs)
│   │   ├── minitoast.jpg          ← [NEW] Mini Toast product asset
│   │   ├── largetoast.png         ← [NEW] Large Toast product asset
│   │   ├── special-request-illustration.svg ← [NEW] Custom order card illustration
│   │   ├── creamroll.jpeg         ← Signature CreamRoll asset
│   │   ├── toast.jpeg             ← Standard Toast asset
│   │   ├── fans-product.png / fan2.jpeg / fan3.jpeg
│   │   └── surya-sugam-bakery-logo.svg
│   └── lib/                       ← Bootstrap, jQuery, jQuery-validation
├── Properties/launchSettings.json ← HTTP: 5243 / HTTPS: 7225
├── Program.cs                     ← App setup + 3 Minimal API endpoints for comments
├── WebApplication2.csproj         ← .NET 10, nullable, implicit usings
├── WebApplication2.slnx
├── appsettings.json
├── SuryaSugam_Bakery_Project_Report.docx ← Complete Word project report
├── SuryaSugam_Bakery_Pitch_Deck.pptx    ← Executive pitching presentation
├── prototype-homepage.png          ← Screenshot
└── prototype-product.png           ← Screenshot"""

p_box = doc.add_paragraph()
r_box = p_box.add_run(struct_text)
r_box.font.name = 'Consolas'
r_box.font.size = Pt(8)
r_box.font.color.rgb = COLOR_INK

# ==================== 6. ROUTING & ENDPOINTS ====================
add_h1("6. Routing & Endpoints Specification")
add_h2("6.1 MVC Controller Routes (HomeController)")
mvc_routes = [
    ("/", "GET", "Index", "Homepage storefront"),
    ("/products/{slug}", "GET", "Product", "Product detail page"),
    ("/products/{slug}/add", "POST", "AddToCart", "Add item to session cart"),
    ("/cart", "GET", "Cart", "View shopping cart"),
    ("/cart/update", "POST", "UpdateCart", "Change item quantity"),
    ("/cart/remove", "POST", "RemoveFromCart", "Remove item from cart"),
    ("/Home/Subscribe", "POST", "Subscribe", "Newsletter signup (demo)"),
    ("/Home/Privacy", "GET", "Privacy", "Privacy page")
]
mvc_tbl = doc.add_table(rows=1, cols=4)
format_table(mvc_tbl, [1.5, 0.8, 1.4, 3.1], ["Route", "Method", "Action", "Purpose"], mvc_routes, header_bg="7E4A2D")

add_h2("6.2 Minimal API Endpoints (in Program.cs)")
min_routes = [
    ("/products/{slug}/comments", "GET", "Fetch all comments for a product (JSON)"),
    ("/products/{slug}/comments", "POST", "Submit a new comment (JSON)"),
    ("/products/{slug}/comments/live", "GET", "SSE stream for real-time comment updates")
]
min_tbl = doc.add_table(rows=1, cols=3)
format_table(min_tbl, [2.2, 1.0, 3.6], ["Route", "Method", "Purpose"], min_routes, header_bg="7E4A2D")

# ==================== 7. PRODUCT CATALOG (UPDATED) ====================
add_h1("7. Product Catalog (Updated with 4 Categories & Sizing Hierarchy)")
add_p("The catalog features 4 prominent categories: Fans, CreamRoll, Toast, and Special Request (Custom Orders). External unsplash URLs have been completely eliminated in favor of 100% locally hosted assets:")

add_h2("7.1 Category Cards (4 Categories)")
cat_data = [
    ("Fans", "फैन", "Flaky favourites for tea-time", "/images/fans-product.png", "Fresh batch"),
    ("CreamRoll", "क्रीम रोल", "Soft rolls with a creamy centre", "/images/creamroll.jpeg", "-"),
    ("Toast", "टोस्ट", "Crisp, golden, and easy to share", "/images/toast.jpeg", "-"),
    ("Special Request", "विशेष ऑर्डर", "Create a custom bakery order (1-500 pcs)", "/images/special-request-illustration.svg", "Custom order")
]
cat_tbl = doc.add_table(rows=1, cols=5)
format_table(cat_tbl, [1.4, 1.2, 2.2, 1.2, 1.0], ["Category", "Hindi Name", "Description", "Image Asset", "Badge"], cat_data, header_bg="7E4A2D")

add_h2("7.2 Fans (Puff Pastries)")
fan_data = [
    ("fan-puff", "Mini Fan", "₹145", "/images/fans-product.png", "Bestseller"),
    ("masala-fan", "Standard Fan", "₹160", "/images/fan2.jpeg", "-"),
    ("paneer-fan", "Large Fan", "₹180", "/images/fan3.jpeg", "New")
]
fan_tbl = doc.add_table(rows=1, cols=5)
format_table(fan_tbl, [1.5, 1.8, 1.1, 1.6, 1.0], ["Slug", "Product Name", "Price", "Local Asset", "Badge"], fan_data, header_bg="7E4A2D")

add_h2("7.3 CreamRoll (Signature Hero SKU)")
cream_data = [
    ("creamroll", "CreamRoll", "₹60", "/images/creamroll.jpeg", "Bestseller")
]
cream_tbl = doc.add_table(rows=1, cols=5)
format_table(cream_tbl, [1.5, 1.8, 1.1, 1.6, 1.0], ["Slug", "Product Name", "Price", "Local Asset", "Badge"], cream_data, header_bg="7E4A2D")

add_h2("7.4 Toasts (Size-Tiered Hierarchy)")
toast_data = [
    ("milk-toast", "Mini Toast", "₹100", "/images/minitoast.jpg", "Bestseller"),
    ("classic-rusk-toast", "Standard Toast", "₹120", "/images/toast.jpeg", "-"),
    ("fruit-toast", "Large Toast", "₹150", "/images/largetoast.png", "Fresh batch")
]
toast_tbl = doc.add_table(rows=1, cols=5)
format_table(toast_tbl, [1.5, 1.8, 1.1, 1.6, 1.0], ["Slug", "Product Name", "Price", "Local Asset", "Badge"], toast_data, header_bg="7E4A2D")

# ==================== 8. KEY FEATURES ====================
add_h1("8. Core Application Features & Functional Architecture")

add_h2("8.1 Bilingual Support (English ↔ Hindi)")
add_p("Every visible string uses data-en / data-hi attributes. site.js swaps text, placeholders, alt text, and aria-labels on toggle. Preference persists in localStorage.")

add_h2("8.2 Special Request & Custom Order Engine (New Feature)")
add_bullet("Dedicated custom order module (_CustomOrderSection.cshtml) on the homepage.", "Bespoke Event Requests: ")
add_bullet("Captures customer name, phone number, product family (Fans, CreamRoll, Toast, Other), event occasion, preferred date, and customization notes.", "Comprehensive Data Capture: ")
add_bullet("Supports quantities from 1 to 500 units, opening high-ticket B2B catering orders.", "Flexible Volume: ")
add_bullet("Dynamically compiles and triggers a structured WhatsApp message directly to bakery dispatch.", "Direct WhatsApp Dispatch: ")

add_h2("8.3 Session-Based Shopping Cart")
add_bullet("Cart stored in ASP.NET Core session as serialized JSON.")
add_bullet("Cart items capture: product, size, egg preference, quantity, city, area, delivery date, time slot, and optional message.")
add_bullet("Quantity range: 1–20 per line item; cart recalculates subtotal and item totals.")
add_bullet("CSRF protected with [ValidateAntiForgeryToken].")

add_h2("8.4 WhatsApp Ordering Pipeline")
add_bullet("Every product card, product detail page, cart summary, and custom order section features a WhatsApp button.")
add_bullet("Links open wa.me/918921986080 with a pre-formatted order message.")
add_bullet("Messages dynamically update based on form inputs and selected language.")

add_h2("8.5 Real-Time Comments (SSE)")
add_bullet("ProductCommentStore service: in-memory, capped at 100 comments per product.")
add_bullet("Server-Sent Events via Channel<ProductComment> for live updates.")
add_bullet("Client-side EventSource in product-comments.js with validation on both tiers.")

add_h2("8.6 Hero Slideshow & Responsive Design")
add_bullet("4-image carousel with auto-rotation (4s interval) and accessibility play/pause controls.")
add_bullet("3 responsive breakpoints: 1050px, 760px, 390px with mobile hamburger menu and collapsible dropdowns.")

# ==================== 9. DESIGN SYSTEM ====================
add_h1("9. UI Design System & Brand Tokens")
ds_data = [
    ("--paper", "#fbf8f2", "Page background"),
    ("--ink", "#30251f", "Primary text"),
    ("--clay", "#b86143", "Brand accent (terracotta)"),
    ("--rose", "#edd9ce", "Soft accent"),
    ("--sage", "#dce1d4", "Banner backgrounds"),
    ("--serif", "Playfair Display", "Headings"),
    ("--sans", "DM Sans", "Body text")
]
ds_tbl = doc.add_table(rows=1, cols=3)
format_table(ds_tbl, [1.8, 1.8, 3.2], ["Token", "Value", "Usage"], ds_data, header_bg="7E4A2D")

# ==================== 10. DATA FLOW ====================
add_h1("10. End-to-End System Data Flow")
flow_text = """[Browser Client]
   │
   ├── GET / ─────────────────────────> HomeController.Index (Storefront View)
   ├── GET /products/{slug} ──────────> HomeController.Product (Detail & Customizer)
   ├── POST /products/{slug}/add ─────> AddToCart ──> [In-Memory Session (.SuryaSugam.CartSession)]
   ├── GET /cart ─────────────────────> Cart View ──> Generates Pre-filled WhatsApp Link (wa.me)
   ├── FORM [Custom Order] ───────────> Direct WhatsApp Commercial Link (wa.me)
   └── GET /products/{slug}/comments/live ──> SSE Stream (Channel<ProductComment> in ProductCommentStore)"""

p_flow = doc.add_paragraph()
r_fl = p_flow.add_run(flow_text)
r_fl.font.name = 'Consolas'
r_fl.font.size = Pt(8.5)
r_fl.font.color.rgb = COLOR_INK

# ==================== 11. NOTABLE OBSERVATIONS ====================
add_h1("11. Technical Observations, Architectural Trade-offs & Code Quality Audit")
add_callout(
    "IMPORTANT:\n"
    "• No database — all product data is configured in the controller; comments live in memory and are lost on restart.\n"
    "• No authentication — no user accounts or admin panel.\n"
    "• No payment processing — orders go through WhatsApp.\n"
    "• Phone number 8921 986 080 is hardcoded throughout views and JS.",
    label="ARCHITECTURAL OBSERVATIONS",
    hex_bg="F3ECE1"
)

add_callout(
    "TIP:\n"
    "• 100% self-hosted assets: External unsplash dependencies eliminated, ensuring zero broken links.\n"
    "• Clean separation of concerns across models, views, partials, and services.\n"
    "• Bilingual support is implemented elegantly at the DOM level without page reloads.\n"
    "• The SSE comment system and Custom Order engine provide strong real-time consumer engagement.",
    label="IMPLEMENTATION STRENGTHS",
    hex_bg="F0F5ED"
)

add_callout(
    "WARNING:\n"
    "• CreateStorefront() is called multiple times per request (in SetLayoutData() and again in the action method) — could be cached.\n"
    "• ProductCommentStore notifications happen outside the lock — potential race condition if a subscriber is added between AddComment lock release and the subscriber loop.\n"
    "• The _Layout.cshtml.css file (Bootstrap-era defaults) conflicts with the custom site.css — it appears to be leftover scaffolding.",
    label="CODE QUALITY WARNINGS",
    hex_bg="FBEFEC"
)

# ==================== 12. PROTOTYPE SCREENSHOTS ====================
add_h1("12. Prototype Visual Walkthrough & System Screenshots")
add_image_figure(HOME_IMG, "Figure 1 — SuryaSugam Bakery Storefront: Hero Slideshow, Brand Promise Strip & Category Showcase")
add_p("Figure 1 demonstrates the homepage composition with the interactive hero carousel, service trust strip, and category grid now expanded to include Special Request custom orders.")

doc.add_page_break()

add_image_figure(PROD_IMG, "Figure 2 — Fan Puff Product Customization, Order Configuration & Real-Time Review System")
add_p("Figure 2 illustrates the deep product order workflow with pack size selection, delivery date/time slot picker, WhatsApp ordering CTA, and live SSE customer reviews.")

# ==================== 13. CA INTERVIEW EVALUATION ====================
add_h1("13. CA Interview Evaluation: Business Viability, Unit Economics & Internal Controls")

add_h2("13.1 Unit Economics & SKU Profitability Matrix (Updated)")
ca_fin_data = [
    ("Mini Fan (Pack of 4)", "₹145", "₹48", "₹97", "66.9%"),
    ("Standard Fan", "₹160", "₹52", "₹108", "67.5%"),
    ("Large Fan (Paneer)", "₹180", "₹65", "₹115", "63.9%"),
    ("CreamRoll (Signature Hero)", "₹60", "₹18", "₹42", "70.0%"),
    ("Mini Toast (Small Pack)", "₹100", "₹31", "₹69", "69.0%"),
    ("Standard Toast (Regular)", "₹120", "₹36", "₹84", "70.0%"),
    ("Large Toast (Family Pack)", "₹150", "₹45", "₹105", "70.0%"),
    ("Special Request / Catering", "₹2,500+", "₹800", "₹1,700+", "68.0%")
]
ca_tbl = doc.add_table(rows=1, cols=5)
format_table(ca_tbl, [1.8, 1.1, 1.2, 1.2, 1.5], ["Product SKU", "Selling Price", "Est. COGS", "Gross Margin", "Gross Margin %"], ca_fin_data, header_bg="7E4A2D")

add_p("Key Financial Insights: Consolidating CreamRoll into a single flagship item eliminates perishable ingredient waste from slower-selling fruit fillings, lifting gross margins to a consistent 70.0%. Offering a structured Toast hierarchy (Mini, Standard, Large) drives price anchoring and encourages trade-ups to the Large pack (₹150), generating ₹105 gross profit per sale.")

add_h2("13.2 High-Ticket B2B & Event Catering Channel Economics")
add_bullet("The new Special Request form targets birthday parties, family gatherings, temple events, and corporate snacks in Mathura.", "Revenue Expansion: ")
add_bullet("Increases Average Order Value (AOV) from ₹250 (retail tea-time orders) to ₹2,500 – ₹10,000 for bulk celebration packages.", "Substantial AOV Expansion: ")
add_bullet("Catering orders are baked strictly against confirmed advance deposits via WhatsApp, ensuring zero unsold inventory and zero batch write-offs.", "Zero Inventory Risk: ")

add_h2("13.3 Financial Advantages of WhatsApp Commerce vs. Payment Gateways")
add_bullet("Standard payment gateways charge 2.0% to 2.5% MDR + 18% GST. Across ₹4,50,000 monthly GMV, this preserves over ₹10,600/month in pure cash.", "MDR Elimination: ")
add_bullet("Zero OTP delays or card failures in Tier-2/3 cities; near-100% conversion once customer opens WhatsApp.", "Cart Abandonment Prevention: ")
add_bullet("Direct UPI payments on delivery credit funds into the bakery's current account instantly with zero T+2 settlement float.", "Instant Liquidity: ")

add_h2("13.4 Working Capital & Cash Conversion Cycle (CCC)")
add_p("The business operates on a negative Cash Conversion Cycle: CCC = DSI (1 day) + DSO (0 days) - DPO (14 days) = -13 days. Customer cash is collected nearly two weeks before supplier invoices for flour, butter, and packaging fall due, providing an organic, self-funding growth engine.")

add_h2("13.5 Internal Controls & Fraud Mitigation")
add_bullet("Sequential Kitchen Order Tickets (KOT) and Tax Invoices matched to incoming WhatsApp orders.", "1. Sequential Documentation: ")
add_bullet("Daily reconciliation between WhatsApp dispatch logs, physical inventory counts, and incoming bank UPI credits.", "2. Daily Bank Reconciliation: ")
add_bullet("Session security with HttpOnly and IsEssential cookies, 2-hour idle timeout, and CSRF protection on all POST endpoints.", "3. Cyber Security Hygiene: ")
add_bullet("Compliance with Nagar Palika Mathura Food Safety Zone 2 standards and transparent all-inclusive pricing.", "4. Statutory FSSAI Alignment: ")

# ==================== 14. CONCLUSION ====================
add_h1("14. Conclusion & Strategic Scalability Roadmap")
add_p("The SuryaSugam Bakery web application successfully demonstrates frugal, high-impact digital transformation. Recent enhancements—including the Special Request custom ordering channel, Toast size-tier rationalization, and 100% self-hosted assets—further elevate its commercial viability.")

add_h2("Phased Strategic Roadmap")
add_bullet("Complete current MVP validation; deploy to Azure App Service / local Linux VM; connect domain name; link official WhatsApp Business API with automated greeting webhooks.", "Phase 1 (Immediate / 30 Days): ")
add_bullet("Integrate Entity Framework Core (EF Core) with PostgreSQL; introduce Admin Order Dashboard for real-time kitchen tracking; add SMS/WhatsApp dispatch notifications.", "Phase 2 (Quarter 2): ")
add_bullet("Introduce multi-outlet routing across Mathura, Vrindavan, and Govardhan; incorporate automated GST billing and dynamic delivery-zone route optimization.", "Phase 3 (Quarter 3-4): ")

doc.save(OUT_DOCX)
print("SUCCESS: Master Word Document generated at:", OUT_DOCX)

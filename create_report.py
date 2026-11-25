from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from PIL import Image
import os

OUT = r"C:\Users\aarun\source\repos\WebApplication2\SuryaSugam_Bakery_Project_Report.docx"
HOME = r"C:\Users\aarun\source\repos\WebApplication2\prototype-homepage.png"
PRODUCT = r"C:\Users\aarun\source\repos\WebApplication2\prototype-product.png"

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.65)
sec.bottom_margin = Inches(0.65)
sec.left_margin = Inches(0.75)
sec.right_margin = Inches(0.75)

styles = doc.styles
styles['Normal'].font.name = 'Aptos'
styles['Normal'].font.size = Pt(10.5)
styles['Title'].font.name = 'Aptos Display'
styles['Title'].font.size = Pt(30)
styles['Heading 1'].font.name = 'Aptos Display'
styles['Heading 1'].font.size = Pt(18)
styles['Heading 1'].font.color.rgb = RGBColor(126, 74, 45)
styles['Heading 2'].font.name = 'Aptos Display'
styles['Heading 2'].font.size = Pt(13)
styles['Heading 2'].font.color.rgb = RGBColor(126, 74, 45)

# Header and footer
header = sec.header.paragraphs[0]
header.text = "SURYA SUGAM BAKERY  |  PROJECT REPORT"
header.style = styles['Caption']
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = footer.add_run("SuryaSugam Bakery Project  |  ")
run.font.size = Pt(9)
fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'), 'begin')
instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'), 'preserve'); instrText.text = 'PAGE'
fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'end')
footer._p.append(fldChar1); footer._p.append(instrText); footer._p.append(fldChar2)

# Cover
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("\n\n")
r = p.add_run("SURYA SUGAM BAKERY")
r.bold = True; r.font.name = 'Aptos Display'; r.font.size = Pt(32); r.font.color.rgb = RGBColor(126,74,45)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Project Report")
r.bold = True; r.font.size = Pt(22); r.font.color.rgb = RGBColor(210,145,82)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Professional Web Prototype for Fresh Bakery Products").italic = True
p.add_run("\n\nASP.NET Core MVC  |  .NET 10  |  Responsive Web Application")

box = doc.add_table(rows=4, cols=2)
box.alignment = WD_TABLE_ALIGNMENT.CENTER
box.style = 'Table Grid'
labels = [("Project", "SuryaSugam Bakery Online Storefront"),("Location", "Mathura, Uttar Pradesh"),("Document Type", "Project Report & Prototype Documentation"),("Report Date", "18 November 2026")]
for i,(a,b) in enumerate(labels):
	box.cell(i,0).text=a; box.cell(i,1).text=b
	box.cell(i,0).paragraphs[0].runs[0].bold=True
	box.cell(i,0).vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER

doc.add_page_break()

# TOC
p=doc.add_paragraph(style='Heading 1'); p.add_run("Table of Contents")
toc_items=[("1","Introduction"),("2","Background"),("3","Project Objectives"),("4","Project Overview and Scope"),("5","Prototype Screenshots"),("6","Key Features"),("7","Technology and Implementation"),("8","Conclusion")]
t=doc.add_table(rows=len(toc_items),cols=2); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
for i,(n,title) in enumerate(toc_items):
	t.cell(i,0).text=n
	t.cell(i,1).text=title
	t.cell(i,0).paragraphs[0].runs[0].bold=True
	t.cell(i,0).width=Inches(.6)

doc.add_page_break()

# Introduction
h=doc.add_heading("1. Introduction", level=1)
doc.add_paragraph("The SuryaSugam Bakery project is a modern, customer-focused web application designed to present and promote fresh bakery products in Mathura. The platform provides a branded digital storefront for Fans, CreamRoll, and Toast, while guiding customers through product discovery, detailed product selection, cart management, and order communication.")
doc.add_paragraph("The solution combines an attractive visual identity with practical e-commerce features. It is built as an ASP.NET Core MVC application and demonstrates how a traditional local bakery can improve accessibility, customer engagement, and order convenience through a polished online experience.")

# Background
doc.add_heading("2. Background", level=1)
doc.add_paragraph("Local bakeries often depend on walk-in customers, telephone calls, and manual order coordination. Customers may find it difficult to view available products, compare options, or clearly communicate delivery details. The proposed platform addresses these challenges with a structured catalogue and a simple ordering workflow.")
doc.add_paragraph("SuryaSugam Bakery is presented as a fresh, locally trusted brand in the Lohaban Bagihi area of Mathura. The website reflects the bakery's tea-time identity and uses warm editorial styling, clear product categories, bilingual English and Hindi content, and direct WhatsApp ordering.")

# Objectives
doc.add_heading("3. Project Objectives", level=1)
objectives=[
("Digital Showcase","Create a professional online identity for SuryaSugam Bakery and its product range."),
("Easy Product Discovery","Present Fans, CreamRoll, and Toast in clear, visually appealing categories."),
("Accessible Ordering","Allow users to choose size, preference, delivery date, time slot, quantity, and order message."),
("Convenient Cart","Provide a session-based shopping cart with quantity updates and item removal."),
("Direct Communication","Enable rapid order sharing through WhatsApp and a bakery telephone contact."),
("Inclusive Experience","Support both English and Hindi throughout the interface."),
]
t=doc.add_table(rows=1,cols=2); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
for j,text in enumerate(["Objective","Purpose"]): t.cell(0,j).text=text
for a,b in objectives:
	c=t.add_row().cells; c[0].text=a; c[1].text=b

# Overview
p=doc.add_heading("4. Project Overview and Scope", level=1)
doc.add_paragraph("The implemented prototype covers a complete customer-facing journey:")
for item in ["Homepage and promotional announcement","Product category sections and featured bakery items","Individual product detail pages","Size and egg-preference selection","Delivery date, time, city, and area collection","Session-based cart with live item totals","Customer comments and live comment updates","English/Hindi language switching","WhatsApp order summary and direct telephone contact"]:
	doc.add_paragraph(item, style='List Bullet')

# Screenshots

doc.add_heading("5. Prototype Screenshots", level=1)
doc.add_paragraph("The following screenshots demonstrate the major user interface implemented in the prototype.")

def add_image(path, caption):
	im=Image.open(path)
	ratio=im.height/im.width
	width=Inches(7.0)
	height=width*ratio
	if height>Inches(5.2):
		height=Inches(5.2); width=height/ratio
	p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
	p.add_run().add_picture(path, width=width, height=height)
	c=doc.add_paragraph(caption); c.alignment=WD_ALIGN_PARAGRAPH.CENTER
	for r in c.runs: r.italic=True; r.font.size=Pt(9); r.font.color.rgb=RGBColor(100,100,100)

add_image(HOME, "Figure 1 — SuryaSugam Bakery homepage prototype")
doc.add_page_break()
add_image(PRODUCT, "Figure 2 — Fan Puff product detail and ordering prototype")

# Features

doc.add_heading("6. Key Features", level=1)
features=[
("Responsive storefront","Built with structured Razor views and reusable partial sections for consistent presentation."),
("Bilingual interface","English and Hindi content is available through a page-level language control."),
("Product catalogue","The application presents Fans, CreamRoll, and Toast with images, descriptions, badges, and prices."),
("Custom order options","Customers can select size, preference, quantity, delivery details, and a short personal message."),
("Cart management","The cart retains items in session, recalculates totals, updates quantities, and supports removal."),
("Customer engagement","Product comments are validated, stored, and delivered to open pages through server-sent events."),
("Order conversion","Users can continue to WhatsApp with a generated order summary or place a direct call."),
]
t=doc.add_table(rows=1,cols=2); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
for j,text in enumerate(["Feature","Implementation Value"]): t.cell(0,j).text=text
for a,b in features:
	c=t.add_row().cells; c[0].text=a; c[1].text=b

# Technology

doc.add_heading("7. Technology and Implementation", level=1)
tech=[("Framework","ASP.NET Core MVC on .NET 10"),("Frontend","Razor views, HTML5, CSS, JavaScript, and Bootstrap assets"),("Architecture","Controllers, strongly typed models, Razor partials, and services"),("Session State","ASP.NET Core session for shopping-cart persistence"),("Live Comments","Server-Sent Events (SSE) with channel subscriptions"),("Assets","Local and hosted product imagery, SVG brand logo, and custom styling")]
t=doc.add_table(rows=1,cols=2); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
for j,text in enumerate(["Area","Technology / Approach"]): t.cell(0,j).text=text
for a,b in tech:
	c=t.add_row().cells; c[0].text=a; c[1].text=b

doc.add_heading("Implementation Strengths", level=2)
for item in ["Strongly typed view models improve code clarity and maintainability.","Reusable Razor partials keep page sections consistent.","Server-side validation protects the cart and product comment workflows.","The layout adapts for desktop and mobile devices.","A professional local-bakery brand identity is maintained across pages."]:
	doc.add_paragraph(item, style='List Bullet')

# Conclusion

doc.add_heading("8. Conclusion", level=1)
doc.add_paragraph("The SuryaSugam Bakery prototype is a promising and practical digital storefront that presents local bakery products in a professional, accessible, and engaging manner. It successfully combines branded design, bilingual content, product discovery, configurable orders, cart management, customer comments, and direct communication in one cohesive experience.")
doc.add_paragraph("The project demonstrates a strong foundation for further commercial development. Recommended next stages include database-backed inventory and orders, secure customer accounts, payment integration, a bakery administration dashboard, real delivery-zone validation, and deployment to a production web host. With these enhancements, the prototype can evolve into a complete online ordering platform for SuryaSugam Bakery.")

# Add simple document properties
props=doc.core_properties
props.title="SuryaSugam Bakery Project Report"
props.subject="Professional web prototype report"
props.author="Project Development Team"
props.keywords="Bakery, ASP.NET Core, MVC, E-commerce, Prototype"

doc.save(OUT)
print(OUT)

"""
Generate Sunscreen_vs_Perfume_Business_Research.pdf

This script creates a well-formatted PDF containing:
  1. Sunscreen Business Research Report (sections 1-10)
  2. Perfume Business Research Report (sections 1-7)
  3. Business Comparison Section (side-by-side practical advice)

Run:
    python generate_pdf.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

PAGE_W, PAGE_H = A4
LEFT_MARGIN = 2.2 * cm
RIGHT_MARGIN = 2.2 * cm
TOP_MARGIN = 2.5 * cm
BOTTOM_MARGIN = 2.5 * cm

# ── colour palette ──────────────────────────────────────────────────────────
BRAND_DARK = colors.HexColor("#1a2e4a")
BRAND_MID = colors.HexColor("#2e6da4")
BRAND_ACCENT = colors.HexColor("#e8f0fe")
DIVIDER = colors.HexColor("#d0d8e8")
TABLE_HEADER = colors.HexColor("#2e6da4")
TABLE_ROW_ALT = colors.HexColor("#f0f4fb")
SECTION_BG = colors.HexColor("#eef3fb")


# ── custom DocTemplate that supports TOC and page numbers ───────────────────
class ReportDoc(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            LEFT_MARGIN,
            BOTTOM_MARGIN,
            PAGE_W - LEFT_MARGIN - RIGHT_MARGIN,
            PAGE_H - TOP_MARGIN - BOTTOM_MARGIN,
            id="main",
        )
        template = PageTemplate(id="main", frames=frame, onPage=self._page_decor)
        self.addPageTemplates([template])

    def afterFlowable(self, flowable):
        """Register headings for the TOC."""
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            text = flowable.getPlainText()
            if style == "Heading1":
                self.notify("TOCEntry", (0, text, self.page))
            elif style == "Heading2":
                self.notify("TOCEntry", (1, text, self.page))
            elif style == "Heading3":
                self.notify("TOCEntry", (2, text, self.page))

    @staticmethod
    def _page_decor(canvas, doc):
        """Draw header band and page number on every page."""
        canvas.saveState()
        # top colour band
        canvas.setFillColor(BRAND_DARK)
        canvas.rect(0, PAGE_H - 0.8 * cm, PAGE_W, 0.8 * cm, fill=1, stroke=0)
        # header text
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.setFillColor(colors.white)
        canvas.drawString(LEFT_MARGIN, PAGE_H - 0.55 * cm,
                          "Sunscreen vs. Perfume Business Research Report")
        # page number (skip cover page = page 1)
        if doc.page > 1:
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(colors.HexColor("#555555"))
            canvas.drawRightString(
                PAGE_W - RIGHT_MARGIN,
                0.6 * cm,
                f"Page {doc.page}",
            )
        canvas.restoreState()


# ── style factory ────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles["Cover_Title"] = ParagraphStyle(
        "Cover_Title",
        fontName="Helvetica-Bold",
        fontSize=26,
        textColor=BRAND_DARK,
        spaceAfter=10,
        alignment=TA_CENTER,
        leading=32,
    )
    styles["Cover_Sub"] = ParagraphStyle(
        "Cover_Sub",
        fontName="Helvetica",
        fontSize=13,
        textColor=BRAND_MID,
        spaceAfter=6,
        alignment=TA_CENTER,
        leading=18,
    )
    styles["Cover_Date"] = ParagraphStyle(
        "Cover_Date",
        fontName="Helvetica-Oblique",
        fontSize=10,
        textColor=colors.HexColor("#888888"),
        alignment=TA_CENTER,
    )
    styles["TOC_Title"] = ParagraphStyle(
        "TOC_Title",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=BRAND_DARK,
        spaceAfter=14,
        spaceBefore=6,
        alignment=TA_CENTER,
    )
    styles["Heading1"] = ParagraphStyle(
        "Heading1",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=colors.white,
        spaceBefore=18,
        spaceAfter=8,
        leading=22,
        backColor=BRAND_DARK,
        leftIndent=-0.5 * cm,
        rightIndent=-0.5 * cm,
        borderPad=(4, 8, 4, 8),
    )
    styles["Heading2"] = ParagraphStyle(
        "Heading2",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=BRAND_DARK,
        spaceBefore=14,
        spaceAfter=4,
        borderPad=(2, 0, 2, 0),
        leftIndent=0,
    )
    styles["Heading3"] = ParagraphStyle(
        "Heading3",
        fontName="Helvetica-BoldOblique",
        fontSize=11,
        textColor=BRAND_MID,
        spaceBefore=10,
        spaceAfter=3,
    )
    styles["Body"] = ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
    )
    styles["Bullet"] = ParagraphStyle(
        "Bullet",
        parent=styles["Body"],
        leftIndent=18,
        bulletIndent=4,
        spaceAfter=3,
    )
    styles["Note"] = ParagraphStyle(
        "Note",
        fontName="Helvetica-Oblique",
        fontSize=9,
        textColor=colors.HexColor("#555555"),
        leading=13,
        spaceAfter=4,
        leftIndent=12,
    )
    styles["TableHeader"] = ParagraphStyle(
        "TableHeader",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=colors.white,
        alignment=TA_CENTER,
        leading=12,
    )
    styles["TableCell"] = ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        alignment=TA_LEFT,
    )
    styles["ReportPart"] = ParagraphStyle(
        "ReportPart",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.white,
        alignment=TA_CENTER,
        leading=28,
        spaceBefore=0,
        spaceAfter=0,
    )

    return styles


S = build_styles()


# ── helper builders ──────────────────────────────────────────────────────────
def h1(text):
    return Paragraph(f"&nbsp;&nbsp;{text}", S["Heading1"])


def h2(text):
    return Paragraph(text, S["Heading2"])


def h3(text):
    return Paragraph(text, S["Heading3"])


def body(text):
    return Paragraph(text, S["Body"])


def bullet(items):
    """Accept list of strings and return list of Paragraph bullets."""
    return [Paragraph(f"• &nbsp;{item}", S["Bullet"]) for item in items]


def note(text):
    return Paragraph(f"<i>💡 {text}</i>", S["Note"])


def spacer(h=0.3):
    return Spacer(1, h * cm)


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=DIVIDER, spaceAfter=6)


def styled_table(header_row, data_rows, col_widths=None):
    """Build a styled table with alternating row colours."""
    all_rows = [header_row] + data_rows
    wrapped = []
    for i, row in enumerate(all_rows):
        if i == 0:
            wrapped.append([Paragraph(str(c), S["TableHeader"]) for c in row])
        else:
            wrapped.append([Paragraph(str(c), S["TableCell"]) for c in row])

    t = Table(wrapped, colWidths=col_widths, repeatRows=1)

    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, DIVIDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TABLE_ROW_ALT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def part_divider(part_num, part_title, subtitle=""):
    """Full-page colour divider for each main part."""
    w = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN
    part_label = Paragraph(f"PART {part_num}", ParagraphStyle(
        "pl", fontName="Helvetica-Bold", fontSize=11,
        textColor=colors.HexColor("#aaccee"), alignment=TA_CENTER))
    title_p = Paragraph(part_title, S["ReportPart"])
    sub_p = Paragraph(subtitle, ParagraphStyle(
        "ps", fontName="Helvetica-Oblique", fontSize=12,
        textColor=colors.HexColor("#cce0ff"), alignment=TA_CENTER)) if subtitle else Spacer(1, 1)

    inner = Table(
        [[part_label], [spacer(0.3)], [title_p], [spacer(0.2)], [sub_p]],
        colWidths=[w],
    )
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_DARK),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
    ]))
    return [PageBreak(), spacer(5), inner, spacer(5), PageBreak()]


# ═══════════════════════════════════════════════════════════════════════════
#  CONTENT BUILDERS
# ═══════════════════════════════════════════════════════════════════════════

def cover_page():
    story = []
    story.append(spacer(6))
    story.append(Paragraph("Sunscreen vs. Perfume", S["Cover_Title"]))
    story.append(Paragraph("Business Research Report", S["Cover_Sub"]))
    story.append(spacer(0.4))
    story.append(HRFlowable(width="60%", thickness=2, color=BRAND_MID,
                             hAlign="CENTER", spaceAfter=12))
    story.append(spacer(0.3))
    story.append(Paragraph(
        "A Comprehensive Guide for Aspiring Entrepreneurs", S["Cover_Sub"]))
    story.append(spacer(1.5))
    w = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN
    tbl = Table([
        ["Contents at a Glance"],
        ["Part 1 — Sunscreen Business Research (Sections 1–10)"],
        ["Part 2 — Perfume Business Research (Sections 1–7)"],
        ["Part 3 — Side-by-Side Business Comparison"],
    ], colWidths=[w])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
        ("BACKGROUND", (0, 1), (-1, -1), SECTION_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, 1), (-1, -1), BRAND_DARK),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, DIVIDER),
    ]))
    story.append(tbl)
    story.append(spacer(2))
    story.append(Paragraph("2026 Edition", S["Cover_Date"]))
    story.append(PageBreak())
    return story


def toc_section():
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC1", fontName="Helvetica-Bold", fontSize=11,
                       textColor=BRAND_DARK, spaceBefore=6,
                       leftIndent=0, leading=16),
        ParagraphStyle("TOC2", fontName="Helvetica", fontSize=10,
                       textColor=BRAND_MID, spaceBefore=2,
                       leftIndent=18, leading=14),
        ParagraphStyle("TOC3", fontName="Helvetica-Oblique", fontSize=9,
                       textColor=colors.HexColor("#555555"), spaceBefore=1,
                       leftIndent=36, leading=13),
    ]
    story = []
    story.append(Paragraph("Table of Contents", S["TOC_Title"]))
    story.append(hr())
    story.append(toc)
    story.append(PageBreak())
    return story, toc


# ── PART 1: SUNSCREEN ───────────────────────────────────────────────────────
def sunscreen_report():
    story = []
    story += part_divider(1, "Sunscreen Business\nResearch Report",
                          "Sections 1–10 | Science · Regulation · Market · Strategy")

    # S1
    story.append(h1("1. Science of Sunscreens"))
    story.append(body(
        "Sunscreen protects the skin by absorbing, reflecting, or scattering ultraviolet (UV) "
        "radiation. The two main types of UV radiation that reach the Earth's surface are <b>UVA</b> "
        "(320–400 nm) — responsible for photoaging — and <b>UVB</b> (290–320 nm) — the primary cause "
        "of sunburn and a key contributor to skin cancer."
    ))
    story.append(h2("1.1 UV Radiation and Skin Biology"))
    story.append(body(
        "UV photons penetrate the epidermis and dermis, causing direct DNA damage (pyrimidine dimers), "
        "oxidative stress via reactive oxygen species (ROS), and immune suppression. Melanin produced by "
        "melanocytes provides some natural protection, but it is insufficient for high UV-index environments."
    ))
    story.append(h2("1.2 Organic (Chemical) vs. Inorganic (Physical/Mineral) Filters"))
    story.append(body("UV filters are the active ingredients that define a sunscreen's efficacy:"))
    story += bullet([
        "<b>Chemical filters</b> (e.g., Avobenzone, Octinoxate, Oxybenzone, Bemotrizinol): Absorb UV energy "
        "and convert it to heat. They provide lightweight, transparent formulations.",
        "<b>Mineral filters</b> (Zinc Oxide, Titanium Dioxide): Reflect and scatter UV radiation. "
        "They are photostable, reef-safe, and suitable for sensitive skin, but can leave a white cast.",
        "<b>Hybrid formulations</b>: Combine both filter types for broad-spectrum coverage with improved aesthetics.",
    ])
    story.append(h2("1.3 SPF, PA, and Broad-Spectrum Rating"))
    story.append(body(
        "The <b>Sun Protection Factor (SPF)</b> measures UVB protection. SPF 30 blocks ~97% of UVB, "
        "SPF 50 blocks ~98%. The <b>PA+ system</b> (used in Asia, including India) rates UVA protection "
        "from PA+ to PA++++. A product must undergo both in-vitro and in-vivo testing to claim "
        "broad-spectrum protection."
    ))
    story.append(h2("1.4 Photostability"))
    story.append(body(
        "Certain chemical filters (notably Avobenzone) degrade when exposed to sunlight, reducing "
        "efficacy. Photostabilisers such as <b>Octocrylene</b>, <b>Tinosorb S</b>, and <b>Bemotrizinol</b> "
        "are added to maintain filter integrity over the product's wear time."
    ))
    story.append(h2("1.5 Key Formulation Concepts"))
    story += bullet([
        "Emulsification: Most sunscreens are oil-in-water (O/W) or water-in-oil (W/O) emulsions. "
        "Emulsifiers (e.g., Polysorbate 60, Glyceryl Stearate) keep the formula stable.",
        "Rheology modifiers (e.g., Carbomer, Xanthan Gum) adjust texture and spreadability.",
        "Humectants (Glycerin, Hyaluronic Acid) prevent skin dryness.",
        "Preservatives (Phenoxyethanol, Ethylhexylglycerin) maintain microbiological stability.",
        "Film-forming agents improve water resistance and sweat resistance.",
    ])
    story.append(spacer())

    # S2
    story.append(h1("2. Product Development Process"))
    story.append(body(
        "Developing a sunscreen from concept to market requires a systematic, multi-stage process "
        "involving formulation science, stability testing, safety assessment, and regulatory submission."
    ))
    story.append(h2("2.1 Concept and Brief"))
    story.append(body(
        "Define the target consumer (age, skin type, lifestyle), desired SPF level, product format "
        "(cream, gel, serum, spray, stick), and additional benefits (moisturising, anti-pollution, "
        "tinted, sensitive skin)."
    ))
    story.append(h2("2.2 Prototype Formulation"))
    story.append(body(
        "A cosmetic chemist or contract formulation lab creates prototypes. A typical sunscreen "
        "formulation contains: UV filter system (5–25%), emulsifier system (2–8%), oil phase (5–15%), "
        "water phase (50–70%), and functional actives (0.5–5%)."
    ))
    story.append(h2("2.3 Stability Testing"))
    story.append(body(
        "Stability studies ensure the product maintains efficacy, aesthetics, and safety over its "
        "shelf life. Standard tests include:"
    ))
    cw = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.28, 0.28, 0.44]]
    story.append(styled_table(
        ["Test Type", "Conditions", "Duration / Criteria"],
        [
            ["Accelerated Stability", "40°C / 75% RH", "3–6 months (equivalent to 12–24 months real-time)"],
            ["Real-Time Stability", "25°C / 60% RH", "12–24 months"],
            ["Freeze-Thaw Cycling", "−10°C ↔ 25°C", "5 cycles (phase separation check)"],
            ["Photostability", "ICH Q1B, UV exposure", "No significant SPF loss"],
            ["Microbiological", "Challenge test (ISO 11930)", "No harmful growth"],
        ],
        col_widths=cw,
    ))
    story.append(spacer())
    story.append(h2("2.4 Safety Assessment"))
    story.append(body(
        "A qualified toxicologist must review the safety of every ingredient. For the Indian market, "
        "a cosmetic safety report (CSR) is mandated under CDSCO guidelines. For the EU, a Product "
        "Information File (PIF) is required."
    ))
    story.append(h2("2.5 SPF Testing"))
    story.append(body(
        "SPF must be validated by an accredited independent laboratory using the ISO 24444:2019 "
        "in-vivo method (human panels) or, increasingly, the ISO 24443 in-vitro method with "
        "appropriate correction factors."
    ))
    story.append(spacer())

    # S3
    story.append(h1("3. Regulatory Compliance"))
    story.append(body(
        "The regulatory landscape for sunscreens varies significantly by geography. "
        "For an Indian startup with global ambitions, understanding multi-market requirements is critical."
    ))
    story.append(h2("3.1 India — CDSCO and Drugs & Cosmetics Act"))
    story += bullet([
        "Sunscreens are regulated as cosmetics under the <b>Drugs & Cosmetics Act, 1940</b> and "
        "Rules 1945 (Schedule M-II for Good Manufacturing Practice).",
        "A <b>Cosmetic Manufacturing Licence</b> from the State Licensing Authority is required.",
        "Active UV filter ingredients and maximum permitted concentrations are listed in "
        "<b>Schedule S</b> of the Cosmetics Rules 2020.",
        "Mandatory label elements: INCI names, net quantity, manufacturing date, expiry, "
        "batch number, manufacturer address, country of origin.",
        "Import of sunscreens requires a <b>CDSCO Import Registration</b> certificate.",
    ])
    story.append(h2("3.2 United States — FDA"))
    story += bullet([
        "Sunscreens are classified as OTC (Over-The-Counter) drugs regulated by the FDA.",
        "Only FDA-approved UV filters are permitted; currently 2 are GRASE "
        "(Zinc Oxide, Titanium Dioxide); others require NDA.",
        "SPF testing per the <b>2011 Sunscreen Final Rule</b>; broad-spectrum claim requires "
        "a Critical Wavelength ≥370 nm.",
    ])
    story.append(h2("3.3 European Union — EU Cosmetics Regulation 1223/2009"))
    story += bullet([
        "Sunscreens are cosmetics in the EU (not drugs).",
        "A PIF, cosmetic safety assessment (Art. 10), and CPNP notification are required.",
        "26 fragrance allergens must be declared on labels if above threshold concentrations.",
        "UV filters are listed in Annex VI with strict concentration limits.",
    ])
    story.append(note(
        "Startup Tip: For your first product launch, focus on India's CDSCO compliance. "
        "Once established, expand with EU and US certifications."
    ))
    story.append(spacer())

    # S4
    story.append(h1("4. Raw Materials and Ingredient Sourcing"))
    story.append(body(
        "Ingredients are sourced from speciality chemical distributors, directly from global suppliers, "
        "or through your contract manufacturer."
    ))
    story.append(h2("4.1 UV Filter Suppliers"))
    cw2 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.35, 0.35, 0.30]]
    story.append(styled_table(
        ["Supplier", "Key Products", "Region"],
        [
            ["BASF (Care Chemicals)", "Tinosorb S, Tinosorb M, Eusolex", "Germany / Global"],
            ["DSM-Firmenich", "Parsol filters, Pemulen", "Switzerland / Global"],
            ["Evonik", "Oxynex, Zinc Oxide dispersions", "Germany / Global"],
            ["Thor Group", "Tinuvin, specialty filters", "UK / Global"],
            ["Fine Organics (India)", "Emulsifiers, specialty chemicals", "India"],
        ],
        col_widths=cw2,
    ))
    story.append(spacer())
    story.append(h2("4.2 Other Key Ingredients"))
    story += bullet([
        "Emollients and skin-feel agents: C12-15 Alkyl Benzoate, Caprylic/Capric Triglyceride, "
        "Isononyl Isononanoate.",
        "Emulsifiers: Olivem 1000, Polysorbate 60, Cetearyl Glucoside.",
        "Antioxidants: Tocopheryl Acetate (Vitamin E), Niacinamide.",
        "Natural actives: Aloe Vera Extract, Green Tea Extract, Hyaluronic Acid.",
    ])
    story.append(h2("4.3 Packaging Materials"))
    story += bullet([
        "Airless pumps: Ideal for chemical-filter formulas; prevent oxidation.",
        "Squeeze tubes (aluminium or plastic laminate): Most common for sunscreen creams.",
        "Stick formats: PE or PP twist-up sticks; excellent for on-the-go use.",
        "Labels: Printed with UV-resistant ink; food-grade adhesive for water-resistance.",
    ])
    story.append(spacer())

    # S5
    story.append(h1("5. Manufacturing Process"))
    story.append(body(
        "Manufacturing high-quality sunscreen requires pharma-grade hygiene, precise temperature "
        "control, and homogeneous mixing of oil and water phases."
    ))
    story.append(h2("5.1 Step-by-Step Batch Manufacturing"))
    steps = [
        ("1. Weighing", "All raw materials are accurately weighed per the batch record."),
        ("2. Water Phase", "Water, humectants, and water-soluble actives are heated to 75–80°C."),
        ("3. Oil Phase", "Emollients, emulsifiers, and oil-soluble UV filters are melted at 75–80°C."),
        ("4. Emulsification", "Oil phase is slowly added to water phase under high-shear mixing "
                              "(homogeniser / rotor-stator mixer)."),
        ("5. Cooling", "The emulsion is cooled to 40°C under moderate agitation."),
        ("6. Cool-down Additions", "Heat-sensitive actives (antioxidants, extracts, fragrance) "
                                   "are added below 40°C."),
        ("7. pH Adjustment", "pH adjusted to 5.5–6.5 using Citric Acid or NaOH."),
        ("8. QC Testing", "Viscosity, pH, appearance, and SPF in-process checks."),
        ("9. Filling", "Filled into primary packaging using automated tube fillers or pumps."),
        ("10. Labelling & Packaging", "Secondary packaging, batch coding, and dispatch."),
    ]
    cw3 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.20, 0.80]]
    story.append(styled_table(["Step", "Description"], steps, col_widths=cw3))
    story.append(spacer())
    story.append(h2("5.2 Contract Manufacturing"))
    story.append(body(
        "For startups, <b>contract manufacturing</b> is the most practical route. Partner with a "
        "CDSCO-licensed contract manufacturer (CM) who provides: formulation development support, "
        "stability testing, SPF testing coordination, and turnkey filling/labelling. "
        "Minimum order quantities (MOQ) in India typically start at 500–1,000 units."
    ))
    story.append(note(
        "Key Indian contract manufacturers include: Sarveda Herbal (Mumbai), "
        "BM Pharmaceuticals (Ahmedabad), and Herbal Hills (Pune). Always verify GMP certification."
    ))
    story.append(spacer())

    # S6
    story.append(h1("6. Market Research"))
    story.append(body(
        "Understanding the sunscreen market landscape helps position a new brand effectively "
        "and identify underserved niches."
    ))
    story.append(h2("6.1 Global Market Overview"))
    story += bullet([
        "<b>Market Size:</b> The global sunscreen market was valued at approximately USD 11.5 billion "
        "in 2023 and is projected to reach USD 16+ billion by 2030 (CAGR ~5.3%).",
        "<b>Key Drivers:</b> Rising awareness of skin cancer, social-media-driven skincare routines, "
        "growth of K-beauty influences, and 'skinification' trend.",
        "<b>Major Players:</b> L'Oréal (La Roche-Posay, Vichy), Beiersdorf (Eucerin, Nivea), "
        "Shiseido, EltaMD, Supergoop!, Colorbar, Lotus Herbals.",
    ])
    story.append(h2("6.2 Indian Market Overview"))
    story += bullet([
        "<b>Market Size:</b> India's suncare market is estimated at ~₹2,500–3,000 crore (2024) "
        "and growing at 15–18% CAGR — one of the fastest-growing segments in Indian skincare.",
        "<b>Penetration Gap:</b> Daily sunscreen use remains low (~25%) compared to South Korea (85%+). "
        "Huge headroom for growth through consumer education.",
        "<b>Consumer Trends:</b> Shift from mass creams to lightweight serums and tinted SPF; "
        "growing demand for no-white-cast mineral formulas for deeper skin tones.",
    ])
    story.append(h2("6.3 Market Segmentation"))
    cw4 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.22, 0.28, 0.26, 0.24]]
    story.append(styled_table(
        ["Segment", "Price Range (India)", "Key Brands", "Consumer Profile"],
        [
            ["Mass Market", "₹100–400", "Lotus, Lakme, Biotique", "Price-sensitive, tier-2/3"],
            ["Mid-Premium", "₹400–1,200", "Minimalist, Plum, Dot & Key", "Urban millennials, D2C"],
            ["Premium", "₹1,200–3,000", "La Roche-Posay, Cetaphil", "Dermatologist-guided"],
            ["Ultra-Premium/Niche", "₹3,000+", "Tatcha, Shiseido, EltaMD", "Luxury skincare aficionados"],
        ],
        col_widths=cw4,
    ))
    story.append(spacer())

    # S7
    story.append(h1("7. Business Model and Financial Planning"))
    story.append(body(
        "A sound financial model is the backbone of a sustainable sunscreen business. "
        "Here we outline typical cost structures, pricing, and revenue projections."
    ))
    story.append(h2("7.1 Cost of Goods Sold (COGS) Breakdown"))
    cw5 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.40, 0.30, 0.30]]
    story.append(styled_table(
        ["Component", "% of COGS (Typical)", "Notes"],
        [
            ["Raw Materials (formula)", "35–45%", "UV filters are the costliest item"],
            ["Primary Packaging", "20–30%", "Tube, pump, or stick"],
            ["Secondary Packaging", "8–12%", "Box, leaflet"],
            ["Manufacturing (CM fee)", "10–15%", "MOQ impacts unit cost"],
            ["SPF/QC Testing", "3–6%", "Amortised over batch"],
            ["Regulatory/Compliance", "2–4%", "Label checks, CDSCO fees"],
        ],
        col_widths=cw5,
    ))
    story.append(spacer())
    story.append(h2("7.2 Pricing Strategy"))
    story += bullet([
        "<b>Cost-Plus Pricing:</b> Mark up COGS by 3–5× to arrive at MRP for mid-premium positioning.",
        "<b>Value-Based Pricing:</b> Price based on perceived value (SPF 50, mineral, reef-safe) "
        "and competitor benchmarks.",
        "<b>Keystoning:</b> D2C brand keeps 60–70% gross margin; in retail the brand earns 40–55% "
        "after retailer margin.",
    ])
    story.append(h2("7.3 Break-Even Analysis (Example)"))
    story.append(body(
        "Assume a 50 ml SPF 50 PA++++ serum with ₹180 COGS, priced at MRP ₹799:"
    ))
    cw6 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.45, 0.55]]
    story.append(styled_table(
        ["Metric", "Value"],
        [
            ["MRP", "₹799"],
            ["COGS per unit", "₹180"],
            ["Gross Profit per unit", "₹619 (~77%)"],
            ["Monthly fixed costs (warehouse, team, marketing)", "₹3,00,000"],
            ["Monthly units to break even", "~485 units"],
            ["Monthly revenue at break-even", "~₹3.87 lakh"],
        ],
        col_widths=cw6,
    ))
    story.append(spacer())

    # S8
    story.append(h1("8. Brand Building and Marketing"))
    story.append(body(
        "In the crowded skincare space, a sunscreen brand must communicate clearly, build trust "
        "through education, and create an aspirational identity."
    ))
    story.append(h2("8.1 Brand Positioning Framework"))
    story += bullet([
        "<b>Identify the Problem:</b> 'No-white-cast SPF 50 for Indian skin tones.'",
        "<b>Define the Promise:</b> 'Invisible, lightweight, reef-safe daily SPF.'",
        "<b>Choose Your Archetype:</b> Science-led (like Minimalist) vs. wellness-led (like Plum).",
    ])
    story.append(h2("8.2 Digital Marketing for Sunscreen Brands"))
    story += bullet([
        "<b>Instagram & YouTube:</b> 'Before and After' UV camera reels, ingredient explainer videos, "
        "dermatologist collaborations.",
        "<b>Influencer Strategy:</b> Nano and micro-influencers (10k–100k followers) deliver "
        "5–10× better ROI than mega-influencers for niche skincare.",
        "<b>SEO Content:</b> 'Best sunscreen for oily skin India', 'SPF 50 vs SPF 30', etc. "
        "Blog content drives organic discovery.",
        "<b>Performance Marketing:</b> Meta and Google Shopping Ads. CPC for skincare in India "
        "ranges ₹8–₹25. Target ROAS of 3–4× for D2C.",
    ])
    story.append(h2("8.3 Distribution Channels"))
    story += bullet([
        "<b>D2C Website (Shopify/WooCommerce):</b> Highest margin, direct customer relationship.",
        "<b>Amazon & Flipkart:</b> Essential for discoverability; accept 15–25% platform fees.",
        "<b>Nykaa:</b> Premium positioning; mandatory for credibility in Indian beauty market.",
        "<b>Offline Retail (Phase 2):</b> Modern trade (Reliance SMART, DMart), pharmacies.",
    ])
    story.append(spacer())

    # S9
    story.append(h1("9. Sustainability and Innovation Trends"))
    story.append(body(
        "Consumer awareness around environmental impact is reshaping product development "
        "and brand values in the sunscreen industry."
    ))
    story.append(h2("9.1 Reef-Safe and Ocean-Safe Formulations"))
    story.append(body(
        "Oxybenzone and Octinoxate are banned in Hawaii, Palau, and other locations due to "
        "coral reef damage. Formulating with Zinc Oxide and non-nano Titanium Dioxide "
        "and avoiding the banned chemicals gives a reef-safe claim."
    ))
    story.append(h2("9.2 Sustainable Packaging"))
    story += bullet([
        "PCR (Post-Consumer Recycled) plastic tubes reduce carbon footprint.",
        "Aluminium tubes are infinitely recyclable and increasingly preferred.",
        "Refillable compact formats and concentrated stick formats minimise packaging waste.",
    ])
    story.append(h2("9.3 Innovation Opportunities"))
    story += bullet([
        "SPF-in-makeup: Hybrid foundation + SPF products.",
        "Blue-light (HEV) protection claims gaining popularity.",
        "Tinted mineral SPF for darker Indian skin tones — huge unmet need.",
        "Probiotic and microbiome-friendly sunscreens.",
        "Biodegradable UV filters (still emerging in research stage).",
    ])
    story.append(spacer())

    # S10
    story.append(h1("10. Startup Roadmap and Key Resources"))
    story.append(body(
        "A phased approach helps manage capital, regulatory risk, and learning curve "
        "for a first-time sunscreen entrepreneur."
    ))
    story.append(h2("10.1 12-Month Startup Roadmap"))
    cw7 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.18, 0.52, 0.30]]
    story.append(styled_table(
        ["Phase", "Key Activities", "Milestone"],
        [
            ["Month 1–2", "Market research, niche selection, business registration, "
                          "FSSAI/CDSCO preliminary check", "Business entity formed"],
            ["Month 3–4", "CM shortlisting, formulation briefing, prototype development, "
                          "initial stability study start", "2–3 stable prototypes ready"],
            ["Month 5–6", "SPF testing, safety assessment, label design, "
                          "packaging procurement", "CDSCO-compliant label finalised"],
            ["Month 7–8", "Manufacturing licence (if own mfg.) or CM licence verification, "
                          "batch production of launch stock", "First batch manufactured"],
            ["Month 9–10", "D2C website launch, social media build-up, "
                           "Amazon/Nykaa listing", "First 100 orders"],
            ["Month 11–12", "Performance marketing, influencer campaigns, "
                            "retail outreach, reorder planning", "Break-even milestone"],
        ],
        col_widths=cw7,
    ))
    story.append(spacer())
    story.append(h2("10.2 Key Resources and References"))
    story += bullet([
        "CDSCO Cosmetics Portal: <b>cdsco.gov.in</b>",
        "Indian Cosmetics, Toiletry & Perfumery Association (ICPA): <b>icpa-india.org</b>",
        "International Sun Protection Factor Test Method ISO 24444",
        "Personal Care Products Council (US): <b>personalcarecouncil.org</b>",
        "Cosmetics Europe (EU): <b>cosmeticseurope.eu</b>",
        "Speciality food-grade glycerin & emollient suppliers: IOI Oleo (India office)",
        "UV filter supplier: BASF Care Chemicals, DSM-Firmenich",
    ])
    story.append(spacer())
    return story


# ── PART 2: PERFUME ─────────────────────────────────────────────────────────
def perfume_report():
    story = []
    story += part_divider(2, "Perfume Business\nResearch Report",
                          "Sections 1–7 | Science · Formulation · Manufacturing · Market")

    # P1
    story.append(h1("1. Perfume Science and Olfactory Chemistry"))
    story.append(h2("1.1 The Human Sense of Smell"))
    story.append(body(
        "The human olfactory system is directly wired to the <b>limbic system</b> — the brain's "
        "emotional and memory centre. When volatile fragrance molecules enter the nasal cavity, "
        "they bind to olfactory receptors (encoded by ~400 functional genes), triggering "
        "immediate neurological responses. This is why a single scent can instantly evoke a "
        "vivid memory or strong emotion."
    ))
    story.append(h2("1.2 Perfume and Skin Chemistry"))
    story.append(body(
        "When applied to skin, a perfume's olfactory profile changes based on the wearer's "
        "body temperature, skin pH (typically 4.5–6.5), natural sebum composition, and "
        "microbiome. This is why the same fragrance smells subtly different on different people — "
        "a key selling point for personalisation."
    ))
    story.append(h2("1.3 The Olfactory Pyramid: Notes and Evaporation Curves"))
    story.append(body("Perfumes are structured around molecular volatility — how fast they evaporate:"))
    cw = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.20, 0.30, 0.25, 0.25]]
    story.append(styled_table(
        ["Note Layer", "Duration on Skin", "Examples", "Molecular Weight"],
        [
            ["Top Notes (Head)", "15–30 minutes", "Citrus, bergamot, herbs, light fruits", "Low"],
            ["Middle Notes (Heart)", "2–4 hours", "Rose, jasmine, spices, green notes", "Medium"],
            ["Base Notes (Dry Down)", "6–24+ hours", "Sandalwood, musk, vanilla, resins", "High"],
        ],
        col_widths=cw,
    ))
    story.append(spacer())
    story.append(h2("1.4 Fragrance Families"))
    story += bullet([
        "<b>Floral:</b> Rose, jasmine, peony. Most commercially popular globally.",
        "<b>Oriental/Amber:</b> Vanilla, benzoin, resins. Rich, warm, and sensual.",
        "<b>Woody:</b> Sandalwood, cedar, vetiver, patchouli. Earthy and grounding.",
        "<b>Fresh/Citrus:</b> Lemon, bergamot, aquatic notes. Light and energising.",
        "<b>Gourmand:</b> Edible notes — chocolate, caramel, coffee. Growing trend.",
        "<b>Chypre:</b> Classic accord of bergamot, labdanum, oakmoss. Sophisticated.",
        "<b>Fougère:</b> Lavender, coumarin, moss. Classic masculine structure.",
    ])
    story.append(h2("1.5 Fixatives and Longevity"))
    story.append(body(
        "Fixatives reduce the evaporation rate of volatile top notes, anchoring the fragrance "
        "and improving longevity (also called <i>tenacity</i>). Historic animal-derived fixatives "
        "(ambergris, civet, castoreum) are now largely replaced by safe synthetics: "
        "Galaxolide (musk), Ambroxan (amber-woody), and Iso E Super (cedar-transparent)."
    ))
    story.append(spacer())

    # P2
    story.append(h1("2. Perfume Composition and Formulation"))
    story.append(h2("2.1 The Perfumer's Palette"))
    story.append(body(
        "A trained perfumer (a 'Nose') works with a palette of 2,000–3,500 raw materials. "
        "They design a formula — called the 'accord' or 'juice' — that harmonises top, heart, "
        "and base layers. The formula is expressed in percentages and typically contains "
        "20–200 individual ingredients."
    ))
    story.append(h2("2.2 Perfume Concentrations"))
    cw2 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.25, 0.20, 0.20, 0.35]]
    story.append(styled_table(
        ["Type", "Concentration", "Longevity", "Character"],
        [
            ["Eau de Cologne (EDC)", "2–4%", "1–2 hours", "Very fresh, light"],
            ["Eau de Toilette (EDT)", "5–15%", "3–5 hours", "Everyday, versatile"],
            ["Eau de Parfum (EDP)", "15–20%", "5–8 hours", "Rich, modern standard"],
            ["Parfum / Extrait", "20–30%+", "12–24 hours", "Intense, skin-close"],
        ],
        col_widths=cw2,
    ))
    story.append(spacer())
    story.append(h2("2.3 Solvents, Stabilizers, and Maceration"))
    story += bullet([
        "<b>Perfumer's Alcohol:</b> High-purity denatured ethanol (96–99.5%) is the primary "
        "carrier. It evaporates rapidly, projecting fragrance molecules into the air.",
        "<b>Distilled Water:</b> 2–5% added to dilute and soften the final product.",
        "<b>Stabilizers:</b> BHT (antioxidant), Benzophenone-3 (UV absorber) prevent oxidation "
        "and colour change.",
        "<b>Maceration:</b> The oil blend sits in alcohol for 2–4 weeks at room temperature, "
        "allowing ingredients to bind and harsh alcohol notes to mellow.",
        "<b>Maturation:</b> Post-maceration ageing (weeks to months) in stainless steel vats "
        "rounds out the scent profile as chemical reactions form new aroma compounds (acetals, esters).",
    ])
    story.append(spacer())

    # P3
    story.append(h1("3. Raw Materials and Ingredient Supply"))
    story.append(h2("3.1 Natural vs. Synthetic Ingredients"))
    story.append(body(
        "Modern perfumery relies on a symbiosis of natural and synthetic ingredients. "
        "Naturals provide organic complexity; synthetics provide consistency, scale, and "
        "the ability to recreate scents that cannot be extracted from nature."
    ))
    cw3 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.20, 0.40, 0.40]]
    story.append(styled_table(
        ["Type", "Advantages", "Disadvantages"],
        [
            ["Natural", "Complex, authentic, storytelling value", "Expensive, variable quality, "
                        "allergen risk, sustainability concerns"],
            ["Synthetic", "Consistent, cost-effective, novel scents possible", "Less 'story', "
                          "occasional regulatory restrictions"],
        ],
        col_widths=cw3,
    ))
    story.append(spacer())
    story.append(h2("3.2 Major Aroma Chemicals"))
    story += bullet([
        "<b>Linalool:</b> Fresh, floral, slightly woody. Found naturally in lavender; synthetic "
        "for consistency. Requires IFRA allergen labelling.",
        "<b>Vanillin:</b> Synthetic vanilla backbone. Sweet, comforting, and ubiquitous in "
        "oriental and gourmand accords.",
        "<b>Coumarin:</b> Hay-almond note from tonka bean. Key in fougère and oriental bases.",
        "<b>Ambroxan:</b> Synthetic ambergris — salty, musky, woody 'skin' warmth. "
        "Hugely popular modern base note.",
        "<b>Iso E Super:</b> Transparent cedarwood/velvety warmth; adds volume and 'sillage'. "
        "Signature note in Molecule 01 (Escentric Molecules).",
        "<b>Hedione:</b> Jasmine-like floralcy with diffusion and freshness.",
        "<b>Galaxolide:</b> Clean musk fixative; widely used in mainstream fragrances.",
    ])
    story.append(h2("3.3 Natural Extraction Methods"))
    cw4 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.30, 0.40, 0.30]]
    story.append(styled_table(
        ["Method", "Process", "Typical Materials"],
        [
            ["Steam Distillation", "Steam passes through plant material, volatilising "
                                   "essential oils which condense on cooling",
             "Lavender, rose, patchouli"],
            ["Cold Pressing", "Mechanical pressing of plant material at ambient temperature",
             "Citrus peels (bergamot, lemon)"],
            ["Solvent Extraction", "Hexane extracts scent from delicate flowers, "
                                   "yielding a 'concrete', further processed to an 'absolute'",
             "Jasmine, violet, tuberose"],
            ["CO₂ Extraction", "Supercritical CO₂ used as solvent; yields high-quality oil",
             "Ginger, cardamom, vanilla"],
        ],
        col_widths=cw4,
    ))
    story.append(spacer())
    story.append(h2("3.4 Major Fragrance Houses (Ingredient Suppliers)"))
    story += bullet([
        "<b>Givaudan (Switzerland):</b> World's largest fragrance house; 3,500+ perfumers globally.",
        "<b>dsm-firmenich (Switzerland/Netherlands):</b> Merger of DSM Nutritional Products "
        "and Firmenich; No. 2 globally.",
        "<b>IFF — International Flavors & Fragrances (USA):</b> Acquired Frutarom and Nouryon; "
        "broad portfolio.",
        "<b>Symrise (Germany):</b> Strong in naturals and India/Asia markets.",
        "<b>Mane (France):</b> Family-owned, known for naturals and quality.",
    ])
    story.append(spacer())

    # P4
    story.append(h1("4. Perfume Manufacturing Process"))
    story.append(h2("4.1 From Brief to Bottle"))
    cw5 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.20, 0.80]]
    story.append(styled_table(
        ["Stage", "Description"],
        [
            ["1. Creative Brief", "Brand shares mood, target audience, price tier, "
                                  "and inspiration references with the fragrance house."],
            ["2. Compounding", "The fragrance house formulates the pure oil concentrate "
                               "and submits 3–5 candidate fragrances (called 'submissions')."],
            ["3. Selection & Modification", "Brand selects a fragrance; iterative modifications "
                                            "over weeks/months until approved."],
            ["4. Oil Delivery", "Approved fragrance oil is shipped to the perfume manufacturer."],
            ["5. Blending", "Oil is blended with perfumer's alcohol and distilled water "
                            "in stainless steel vats."],
            ["6. Maceration", "Mixture rests 2–6 weeks in sealed, cool, dark conditions."],
            ["7. Chilling & Filtration", "Batch chilled to 0–5°C to precipitate waxes; "
                                         "filtered through microporous filters for clarity."],
            ["8. Quality Control", "Olfactory evaluation by trained nose; GC-MS analysis; "
                                   "batch record approved."],
            ["9. Bottling & Crimping", "Filled into glass bottles; spray pump crimped onto neck."],
            ["10. Finishing", "Cap, collar, leaflet, box — sent to distribution."],
        ],
        col_widths=cw5,
    ))
    story.append(spacer())
    story.append(h2("4.2 Contract Manufacturing for Startups"))
    story.append(body(
        "New perfume brands rarely build their own manufacturing facilities. "
        "The typical startup approach is:"
    ))
    story += bullet([
        "Commission a fragrance house (or use a ready-made base from a supplier) to provide "
        "the oil concentrate.",
        "Engage a licensed contract filler who handles alcohol procurement, blending, "
        "maceration, filtration, and bottling.",
        "Minimum Order Quantities (MOQ) in India start at 100–500 units for contract fillers.",
        "Total landed cost for a 50 ml EDP startup batch (India): ₹150–₹400 per unit depending "
        "on oil quality and packaging tier.",
    ])
    story.append(note(
        "Key Indian fragrance suppliers/distributors: Fragrance India Pvt. Ltd. (Mumbai), "
        "SOS Perfumery (Delhi), and PVR Aromatics (Kannauj — India's 'perfume capital')."
    ))
    story.append(spacer())

    # P5
    story.append(h1("5. Regulation and Compliance"))
    story.append(h2("5.1 India — CDSCO and BIS"))
    story += bullet([
        "Perfumes are regulated as cosmetics under the <b>Drugs & Cosmetics Act, 1940</b>.",
        "A <b>Cosmetic Manufacturing Licence</b> is required from the State Drug Controller.",
        "The alcohol used (perfumer's spirit) must comply with <b>BIS IS 3222</b> and is typically "
        "denatured with DEP (Diethyl Phthalate) to make it unfit for consumption, in compliance "
        "with the Denatured Spirit Rules.",
        "Label requirements: INCI name of ingredients, net volume (ml), manufacturer details, "
        "batch no., MFG/EXP date, country of origin, allergen disclosure.",
    ])
    story.append(h2("5.2 IFRA Standards (Global)"))
    story.append(body(
        "The <b>International Fragrance Association (IFRA)</b> issues binding standards that "
        "restrict or ban fragrance ingredients based on safety testing. The 50th IFRA Amendment "
        "(2023) provides the latest restrictions. Key categories:"
    ))
    story += bullet([
        "<b>Category 4 (leave-on fine fragrance):</b> Most relevant for EDP/EDT — "
        "strict limits on skin sensitisers like linalool and citral.",
        "Reputable fragrance houses supply <b>IFRA-compliant</b> oils with a Certificate of "
        "Compliance and full ingredient disclosure (MSDS / SDS).",
    ])
    story.append(h2("5.3 EU/UK Cosmetics Regulation"))
    story += bullet([
        "26 fragrance allergens must be declared on labels if above 0.001% (leave-on) "
        "or 0.01% (rinse-off) concentration.",
        "Product Information File (PIF) and cosmetic safety assessment required.",
        "CPNP (Cosmetic Products Notification Portal) notification before placing on EU market.",
    ])
    story.append(spacer())

    # P6
    story.append(h1("6. Market Research"))
    story.append(h2("6.1 Global Perfume Market"))
    story += bullet([
        "<b>Market Size:</b> The global fragrance market was valued at ~USD 52 billion in 2023; "
        "projected USD 75+ billion by 2030 (CAGR ~5.5%).",
        "<b>Key Trends:</b> Gender-neutral scents, 'clean' transparent formulations, "
        "niche and artisanal perfumery, and olfactive wellness.",
        "<b>Leading Houses:</b> LVMH (Dior, Givenchy, Guerlain), Chanel, Coty "
        "(Calvin Klein, Gucci), L'Oréal Luxe (Lancôme, YSL Beauty).",
    ])
    story.append(h2("6.2 Indian Fragrance Market"))
    story += bullet([
        "<b>Market Size:</b> ~₹6,500 crore (2024), growing at 12–15% CAGR.",
        "<b>Historical Roots:</b> India has a deep attar (ittar) tradition. Kannauj in UP "
        "is the 'Grasse of India', producing world-famous rose and jasmine attars.",
        "<b>Modern Shift:</b> Rapid move from deodorant body sprays to premium EDPs among "
        "urban millennials (25–35 year olds).",
        "<b>D2C Surge:</b> Brands like Bombay Perfumery, Naso Profumi, Isak, and "
        "Villain Lifestyle have demonstrated that Indian consumers will pay ₹2,000–₹6,000 "
        "for locally crafted niche perfumes.",
    ])
    story.append(h2("6.3 Market Segmentation"))
    cw6 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.22, 0.25, 0.28, 0.25]]
    story.append(styled_table(
        ["Segment", "Price (India MRP)", "Examples", "Entry Barrier"],
        [
            ["Mass Market", "₹99–₹499", "Fogg, Axe, Engage, Park Avenue", "Low"],
            ["Mid-Range", "₹499–₹1,500", "Bella Vita, Titan Skinn, Ajmal", "Low–Medium"],
            ["Designer", "₹1,500–₹8,000", "Dior, Versace, Carolina Herrera", "High (licensing)"],
            ["Niche/Indie", "₹2,000–₹15,000+", "Bombay Perfumery, Byredo, Le Labo", "Medium (branding)"],
            ["Heritage Attar", "₹500–₹50,000+", "Gulab Singh Johrimal, Ajmal Attar", "Medium"],
        ],
        col_widths=cw6,
    ))
    story.append(spacer())

    # P7
    story.append(h1("7. Product Differentiation and Brand Building"))
    story.append(h2("7.1 Storytelling and Brand DNA"))
    story.append(body(
        "In luxury fragrance, you are not selling a liquid in a bottle — you are selling "
        "an emotion, a memory, or an aspiration. The most successful modern perfume brands "
        "have a clear and consistent brand DNA:"
    ))
    story += bullet([
        "<b>Byredo:</b> Minimalist Scandinavian design; each fragrance built around a "
        "personal memory or cultural moment.",
        "<b>Le Labo:</b> Industrial apothecary aesthetic; 'freshly-blended' narrative; "
        "city-exclusive fragrances create scarcity.",
        "<b>Bombay Perfumery:</b> Celebrates Indian botanicals and stories; modern "
        "interpretation of traditional Indian scent culture.",
        "<b>Maison Margiela Replica:</b> Fragrances designed to replicate a specific "
        "memory or moment ('Beach Walk', 'Jazz Club').",
    ])
    story.append(h2("7.2 Packaging and Sensory Brand Signals"))
    story += bullet([
        "Glass weight and neck finish communicate luxury subconsciously.",
        "The 'click' of a magnetic or press-fit cap is a tactile luxury signal.",
        "Atomiser quality: A fine mist (Dip Tube + Actuator system) with 0.1–0.15 ml "
        "per spray is the luxury standard.",
        "Secondary packaging (box): Paper weight (350–450 gsm), hot-foil stamping, "
        "and linen-effect finishes signal premium positioning.",
    ])
    story.append(h2("7.3 Olfactory Signature Strategy"))
    story.append(body(
        "Avoid generic mall scents. Differentiate through unexpected combinations: "
        "cardamom + fig, saffron + leather, rain-wet earth (petrichor) + white musk. "
        "Signature accord = brand recognisability. Many successful indie brands build an "
        "entire identity around a single hero accord."
    ))
    story.append(h2("7.4 Launch Strategy for New Perfume Brands"))
    cw7 = [(PAGE_W - LEFT_MARGIN - RIGHT_MARGIN) * x for x in [0.22, 0.78]]
    story.append(styled_table(
        ["Phase", "Activities"],
        [
            ["Month 1–2", "Brand name, logo, storytelling brief, fragrance brief to house"],
            ["Month 3–5", "Fragrance selection & modifications, bottle/cap sourcing, "
                          "label design"],
            ["Month 6–7", "Test batch, IFRA compliance, CDSCO documentation, "
                          "photography/video shoot"],
            ["Month 8", "D2C website (Shopify), social media build, gifting to influencers"],
            ["Month 9–10", "Launch campaign, Nykaa/Amazon listing, press outreach"],
            ["Month 11–12", "Paid ads, pop-up events, retail outreach (Sephora India, "
                            "specialty stores)"],
        ],
        col_widths=cw7,
    ))
    story.append(spacer())
    return story


# ── PART 3: COMPARISON ───────────────────────────────────────────────────────
def comparison_section():
    story = []
    story += part_divider(3, "Business Comparison",
                          "Side-by-Side Practical Advice for Beginners")

    story.append(h1("Sunscreen vs. Perfume: Complete Beginner's Guide"))
    story.append(body(
        "This section provides a direct, practical comparison of both business opportunities "
        "specifically designed for first-time entrepreneurs. Use this as a decision-making "
        "framework tailored to your resources, risk appetite, and interests."
    ))
    story.append(spacer())

    story.append(h2("At a Glance: Side-by-Side Comparison"))
    w = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN
    cw = [w * x for x in [0.35, 0.325, 0.325]]
    story.append(styled_table(
        ["Factor", "☀️  Sunscreen", "🌸  Perfume"],
        [
            ["Regulatory Complexity", "HIGH — CDSCO cosmetic licence, SPF "
                                      "claims require lab testing, Schedule S compliance",
             "MEDIUM — CDSCO cosmetic licence, IFRA compliance (via supplier)"],
            ["Technical Difficulty", "HIGH — Emulsion chemistry, SPF validation, "
                                     "photostability",
             "LOW–MEDIUM — Fragrance oil + alcohol blending; "
             "CM handles complexity"],
            ["Startup Capital", "₹8–25 lakh (incl. SPF testing & stability)",
             "₹2–8 lakh (lower MOQ, simpler testing)"],
            ["Time to Market", "9–14 months", "4–8 months"],
            ["Gross Margin Potential", "65–80%", "70–85%"],
            ["Market Demand (India)", "HIGH — fast-growing, low penetration",
             "MEDIUM–HIGH — growing, competitive"],
            ["Reorder Frequency", "HIGH — daily use product",
             "MEDIUM — 2–4 bottles/year"],
            ["Manufacturing MOQ", "500–1,000 units", "100–500 units"],
            ["Branding Leverage", "MEDIUM — science + ingredient story",
             "HIGH — emotion, story, aesthetics"],
            ["Risk of Failure", "MEDIUM — formula rejection by consumers "
                                "(texture, white cast)", "MEDIUM — subjective scent preference"],
            ["Scaling Path", "Skincare portfolio (serum, moisturiser)",
             "Multiple fragrance lines, home/candle"],
        ],
        col_widths=cw,
    ))
    story.append(spacer(0.8))

    story.append(h2("Capital Requirement Breakdown"))
    story.append(body(
        "Understanding where your money goes helps plan your launch budget realistically."
    ))
    cw2 = [w * x for x in [0.35, 0.325, 0.325]]
    story.append(styled_table(
        ["Budget Category", "☀️  Sunscreen (₹ lakh)", "🌸  Perfume (₹ lakh)"],
        [
            ["Formulation Development", "1.5–3.0", "0.5–1.5"],
            ["SPF / Safety Testing", "1.5–3.5", "0.2–0.5 (safety only)"],
            ["Stability Studies", "1.0–2.0", "0.3–0.8"],
            ["Primary Packaging (500 units)", "0.8–1.5", "0.8–2.0"],
            ["Secondary Packaging", "0.3–0.6", "0.4–1.0"],
            ["Contract Manufacturing", "0.5–1.0", "0.3–0.7"],
            ["Regulatory / Legal", "0.4–0.8", "0.2–0.5"],
            ["Branding & Marketing (launch)", "1.0–3.0", "1.0–3.0"],
            ["<b>TOTAL ESTIMATE</b>", "<b>7–15 lakh</b>", "<b>3.7–10 lakh</b>"],
        ],
        col_widths=cw2,
    ))
    story.append(spacer(0.8))

    story.append(h2("Regulatory Pathway Comparison"))
    cw3 = [w * x for x in [0.35, 0.325, 0.325]]
    story.append(styled_table(
        ["Regulatory Step", "☀️  Sunscreen", "🌸  Perfume"],
        [
            ["Cosmetic Mfg. Licence (India)", "Required", "Required"],
            ["SPF/PA Claim Testing", "Mandatory (ISO 24444)", "Not applicable"],
            ["Stability Testing", "6 months minimum", "3 months minimum"],
            ["Safety Assessment / CSR", "Required", "Recommended"],
            ["IFRA Compliance", "Optional (if fragrance added)", "Mandatory"],
            ["Allergen Labelling (EU)", "Required if fragrance > threshold", "Required (26 allergens)"],
            ["FDA (US market)", "OTC Drug approval", "Cosmetic — PCPC notification"],
            ["Typical Regulatory Timeline", "8–14 months", "4–8 months"],
        ],
        col_widths=cw3,
    ))
    story.append(spacer(0.8))

    story.append(h2("Consumer Psychology and Marketing"))
    cw4 = [w * x for x in [0.30, 0.35, 0.35]]
    story.append(styled_table(
        ["Dimension", "☀️  Sunscreen", "🌸  Perfume"],
        [
            ["Purchase Motivation", "Protection, health, skincare routine",
             "Identity, emotion, luxury, gift"],
            ["Repeat Purchase Driver", "Daily necessity", "Seasonal/emotional impulse"],
            ["Content Marketing Hook", "UV damage education, 'no white cast' demo",
             "Storytelling, lifestyle, mood"],
            ["Key Digital Channels", "YouTube dermatologist collabs, skincare Reddit",
             "Instagram, TikTok, fragrance communities (Fragrantica)"],
            ["Influencer Type", "Skincare dermatologists, 'skinfluencers'",
             "Lifestyle, fashion, luxury micro-influencers"],
            ["Customer LTV", "High (daily repurchase)",
             "Medium (2–4 purchases/year per SKU)"],
        ],
        col_widths=cw4,
    ))
    story.append(spacer(0.8))

    story.append(h2("Recommended Starting Path for Beginners"))
    story.append(body(
        "Based on the analysis above, here is practical guidance tailored to your "
        "starting position:"
    ))
    story.append(h3("If You Have < ₹5 Lakh Startup Capital:"))
    story += bullet([
        "Start with <b>perfume</b>. Lower MOQ, simpler compliance, and faster time to market "
        "allow you to test demand without overcommitting capital.",
        "Source a ready-to-use fragrance oil from a reputable supplier (Kannauj or Mumbai).",
        "Invest heavily in brand storytelling, packaging, and D2C website.",
        "Begin with 200 bottles of a single hero scent (EDP, 50 ml).",
    ])
    story.append(h3("If You Have ₹8–20 Lakh and 12+ Months Timeline:"))
    story += bullet([
        "<b>Sunscreen</b> offers higher long-term value due to daily use, repeat purchase, "
        "and the massive growth in India's skincare awareness.",
        "Partner with a CDSCO-licensed CM who can manage formulation, SPF testing, "
        "and stability studies as a bundled service.",
        "Launch with a single hero SKU (SPF 50 PA++++ serum for oily/combination skin) "
        "targeting urban 22–35 year olds.",
        "Build the brand around a specific consumer problem: 'No white cast for Indian skin tones.'",
    ])
    story.append(h3("The Two-Phase Strategy (Recommended):"))
    story += bullet([
        "<b>Phase 1 (Year 1):</b> Launch a perfume brand to build business muscle — operations, "
        "marketing, D2C, customer service, influencer outreach. Keep initial investment low.",
        "<b>Phase 2 (Year 2–3):</b> Use profits and learnings from the perfume brand to fund "
        "a well-researched sunscreen launch under the same or a sister brand.",
        "Cross-selling opportunity: A fragrance customer is an excellent target for a "
        "premium SPF serum.",
    ])
    story.append(spacer(0.5))

    story.append(h2("Key Success Factors for Both Businesses"))
    cw5 = [w * x for x in [0.40, 0.60]]
    story.append(styled_table(
        ["Success Factor", "Why It Matters"],
        [
            ["Product-Market Fit", "Solve a real consumer problem better than existing options"],
            ["Regulatory Compliance", "Non-compliance leads to product seizure and brand damage"],
            ["Quality Manufacturing Partner", "Your CM's hygiene and quality directly become your brand's quality"],
            ["Brand Storytelling", "In beauty, the emotional narrative drives purchase as much as the product"],
            ["D2C + Marketplace Presence", "Direct: higher margin. Marketplace: discoverability and volume"],
            ["Customer Education", "Both sunscreen (why daily SPF?) and perfume (how to wear, choose) benefit from education-led content"],
            ["Influencer/Dermatologist Trust", "Third-party credibility is the fastest path to consumer trust in beauty"],
            ["Inventory Management", "Over-ordering kills cash flow; under-ordering kills growth momentum"],
        ],
        col_widths=cw5,
    ))
    story.append(spacer(0.8))

    story.append(h2("Final Recommendation Summary"))
    story.append(body(
        "<b>For a complete beginner, perfume is the lower-risk, lower-capital, faster entry point.</b> "
        "The regulatory path is simpler, the supply chain is more accessible, and brand building "
        "through storytelling gives you a creative edge without needing deep technical knowledge. "
        "Once you've built operational and marketing experience, sunscreen offers a higher "
        "long-term upside in a rapidly growing, under-penetrated Indian market."
    ))
    story.append(body(
        "Whichever path you choose — <b>start small, validate fast, and reinvest in what works</b>. "
        "The Indian beauty market rewards founders who are curious, customer-obsessed, and willing "
        "to iterate quickly."
    ))
    story.append(spacer())
    return story


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN BUILD
# ═══════════════════════════════════════════════════════════════════════════

def build_pdf(output_path: str):
    doc = ReportDoc(
        output_path,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="Sunscreen vs. Perfume Business Research Report",
        author="Business Research Report Generator",
        subject="Business Research for Aspiring Entrepreneurs",
    )

    story = []

    # Cover
    story += cover_page()

    # TOC
    toc_story, toc = toc_section()
    story += toc_story

    # Parts
    story += sunscreen_report()
    story += perfume_report()
    story += comparison_section()

    doc.multiBuild(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    import os

    out = os.path.join(os.path.dirname(__file__),
                       "Sunscreen_vs_Perfume_Business_Research.pdf")
    build_pdf(out)

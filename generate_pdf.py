"""
Elite Performance Blueprint — PDF Generator
============================================
Generates a comprehensive, research-based, minimally designed PDF guide
for a 22-year-old engineering student aiming for elite performance.

Requires: reportlab  (pip install reportlab)
Run:      python generate_pdf.py
Output:   Elite_Performance_Blueprint.pdf
"""

import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle, Polygon
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart


# ─── Palette ──────────────────────────────────────────────────────────────────
BG          = colors.HexColor("#0D0D0D")   # near-black page background
CARD        = colors.HexColor("#141414")   # slightly lighter card bg
ACCENT      = colors.HexColor("#C8A96E")   # warm gold
ACCENT2     = colors.HexColor("#4A90D9")   # electric blue
TEXT        = colors.HexColor("#E8E8E8")   # off-white body text
TEXT_MUTED  = colors.HexColor("#8A8A8A")   # secondary grey
DIVIDER     = colors.HexColor("#2A2A2A")   # subtle divider
WHITE       = colors.HexColor("#FFFFFF")
RED_SOFT    = colors.HexColor("#C0392B")

PW, PH = A4  # 210 × 297 mm


# ─── Custom Flowables ─────────────────────────────────────────────────────────

class ColorRect(Flowable):
    """A full-width filled rectangle used for section headers."""
    def __init__(self, text, width, height=14*mm, bg=ACCENT, fg=BG, font="Helvetica-Bold", fontsize=13):
        Flowable.__init__(self)
        self.text = text
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg
        self.font = font
        self.fontsize = fontsize

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont(self.font, self.fontsize)
        c.drawString(6*mm, 4*mm, self.text)


class AccentLine(Flowable):
    """A thin horizontal accent rule."""
    def __init__(self, width, color=ACCENT, thickness=0.8):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
        self.height = self.thickness + 2

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(self.thickness)
        c.line(0, self.thickness / 2, self.width, self.thickness / 2)


class CircadianDiagram(Flowable):
    """24-hour clock diagram annotated with key biological events."""
    def __init__(self, size=130):
        Flowable.__init__(self)
        self.size = size
        self.width = size * 2 + 60
        self.height = size * 2 + 30

    def draw(self):
        c = self.canv
        cx = self.size + 20
        cy = self.size + 10
        r = self.size

        # Outer ring background
        c.setFillColor(CARD)
        c.circle(cx, cy, r + 8, fill=1, stroke=0)

        # Night arc (10 PM – 7 AM) — dark blue
        night_start = math.radians(90 - (22 / 24) * 360)
        night_end   = math.radians(90 - (7  / 24) * 360)
        c.setStrokeColor(colors.HexColor("#1A3A5C"))
        c.setLineWidth(18)
        c.arc(cx - r, cy - r, cx + r, cy + r,
              math.degrees(night_end), math.degrees(night_start) - math.degrees(night_end))

        # Day arc — gold
        c.setStrokeColor(colors.HexColor("#7B5B1A"))
        c.setLineWidth(18)
        c.arc(cx - r, cy - r, cx + r, cy + r,
              math.degrees(night_start) - 360 + math.degrees(night_end),
              360 - (math.degrees(night_start) - math.degrees(night_end)))

        # Inner disc
        c.setFillColor(BG)
        c.circle(cx, cy, r - 12, fill=1, stroke=0)

        # Hour ticks & numbers
        c.setFillColor(TEXT_MUTED)
        c.setStrokeColor(DIVIDER)
        c.setLineWidth(0.5)
        for h in range(24):
            angle = math.radians(90 - h / 24 * 360)
            x1 = cx + (r - 13) * math.cos(angle)
            y1 = cy + (r - 13) * math.sin(angle)
            x2 = cx + (r - 18) * math.cos(angle)
            y2 = cy + (r - 18) * math.sin(angle)
            c.line(x1, y1, x2, y2)
            if h % 3 == 0:
                lbl = f"{h:02d}"
                xn = cx + (r - 28) * math.cos(angle)
                yn = cy + (r - 28) * math.sin(angle) - 3
                c.setFont("Helvetica", 6)
                c.setFillColor(TEXT_MUTED)
                c.drawCentredString(xn, yn, lbl)

        # Annotated events
        events = [
            (7.5,  "☀  Wake + Sunlight",   ACCENT),
            (9.0,  "⚡  Deep Work 1",       ACCENT2),
            (11.0, "⚡  Deep Work 2",       ACCENT2),
            (13.0, "🥗  Lunch + Walk",      colors.HexColor("#5DAD62")),
            (16.5, "💪  Resistance Train",  colors.HexColor("#D95B4A")),
            (18.5, "🍽  Dinner (last meal)",colors.HexColor("#5DAD62")),
            (21.5, "🌙  Wind Down",         TEXT_MUTED),
            (22.5, "😴  Sleep",             colors.HexColor("#4A70B0")),
        ]
        for hour, label, col in events:
            angle = math.radians(90 - hour / 24 * 360)
            dot_r = r - 12
            xd = cx + dot_r * math.cos(angle)
            yd = cy + dot_r * math.sin(angle)
            c.setFillColor(col)
            c.circle(xd, yd, 3.5, fill=1, stroke=0)

            line_r = r + 18
            xl = cx + line_r * math.cos(angle)
            yl = cy + line_r * math.sin(angle)
            c.setStrokeColor(col)
            c.setLineWidth(0.6)
            c.line(xd, yd, xl, yl)

            text_r = r + 30
            xt = cx + text_r * math.cos(angle)
            yt = cy + text_r * math.sin(angle)
            c.setFont("Helvetica", 5.5)
            c.setFillColor(col)
            if xt < cx:
                c.drawRightString(xt, yt, label)
            else:
                c.drawString(xt, yt, label)

        # Centre label
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(ACCENT)
        c.drawCentredString(cx, cy + 6, "CIRCADIAN")
        c.setFont("Helvetica", 7)
        c.setFillColor(TEXT_MUTED)
        c.drawCentredString(cx, cy - 4, "24-Hour Clock")

        # Legend
        legend_y = 8
        for label, col in [("  Night / Sleep", colors.HexColor("#1A3A5C")),
                            ("  Active Hours", colors.HexColor("#7B5B1A"))]:
            c.setFillColor(col)
            c.rect(cx - r, legend_y, 10, 7, fill=1, stroke=0)
            c.setFont("Helvetica", 6)
            c.setFillColor(TEXT_MUTED)
            c.drawString(cx - r + 12, legend_y + 1, label)
            cx -= r - 10  # offset for second legend item — reset below
        # (legend positioning kept simple)


class DeepWorkFlow(Flowable):
    """Visual flowchart of the Deep Work session protocol."""
    def __init__(self, width=160*mm):
        Flowable.__init__(self)
        self.width = width
        self.height = 52*mm

    def draw(self):
        c = self.canv
        w = self.width
        box_w = 34*mm
        box_h = 12*mm
        gap = (w - 5 * box_w) / 4
        y = (self.height - box_h) / 2

        stages = [
            ("PRE-WORK\nRITUAL\n5 min", ACCENT),
            ("DEEP\nWORK\n90 min", ACCENT2),
            ("ACTIVE\nBREAK\n20 min", colors.HexColor("#5DAD62")),
            ("REVIEW &\nREFLECT\n10 min", colors.HexColor("#D4A017")),
            ("REPEAT\nor CLOSE", colors.HexColor("#9B59B6")),
        ]

        for i, (label, col) in enumerate(stages):
            x = i * (box_w + gap)
            # box
            c.setFillColor(col)
            c.roundRect(x, y, box_w, box_h, 3*mm, fill=1, stroke=0)
            # text
            lines = label.split("\n")
            line_h = box_h / (len(lines) + 0.5)
            for j, line in enumerate(lines):
                c.setFillColor(BG if col != TEXT_MUTED else WHITE)
                c.setFont("Helvetica-Bold" if j == 0 else "Helvetica", 6.5 if j == 0 else 6)
                c.drawCentredString(x + box_w / 2,
                                    y + box_h - (j + 1) * line_h + 2,
                                    line)
            # arrow
            if i < len(stages) - 1:
                ax = x + box_w + 2
                ay = y + box_h / 2
                c.setStrokeColor(DIVIDER)
                c.setFillColor(DIVIDER)
                c.setLineWidth(1)
                c.line(ax, ay, ax + gap - 4, ay)
                # arrowhead
                p = c.beginPath()
                p.moveTo(ax + gap - 4, ay)
                p.lineTo(ax + gap - 10, ay + 3)
                p.lineTo(ax + gap - 10, ay - 3)
                p.close()
                c.drawPath(p, fill=1, stroke=0)

        # title
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(ACCENT)
        c.drawCentredString(w / 2, self.height - 6, "DEEP WORK SESSION ARCHITECTURE")


class FeynmanFlow(Flowable):
    """Four-step Feynman Technique loop diagram."""
    def __init__(self, size=90):
        Flowable.__init__(self)
        self.size = size
        self.width = size * 2.6
        self.height = size * 2.4

    def draw(self):
        c = self.canv
        s = self.size
        cx = self.width / 2
        cy = self.height / 2

        steps = [
            ("01", "STUDY", "Read / Learn\nthe concept", 90),
            ("02", "TEACH", "Explain it in\nplain language", 0),
            ("03", "IDENTIFY\nGAPS", "Find where\nyou stumbled", 270),
            ("04", "SIMPLIFY", "Return, clarify\n& condense", 180),
        ]
        r_orbit = s * 0.78
        box_w = s * 0.72
        box_h = s * 0.54
        colors_list = [ACCENT, ACCENT2, colors.HexColor("#5DAD62"), colors.HexColor("#D4A017")]

        for idx, (num, title, sub, deg) in enumerate(steps):
            angle = math.radians(deg)
            bx = cx + r_orbit * math.cos(angle) - box_w / 2
            by = cy + r_orbit * math.sin(angle) - box_h / 2
            col = colors_list[idx]
            c.setFillColor(CARD)
            c.roundRect(bx, by, box_w, box_h, 3, fill=1, stroke=0)
            c.setStrokeColor(col)
            c.setLineWidth(1.2)
            c.roundRect(bx, by, box_w, box_h, 3, fill=0, stroke=1)
            # number badge
            c.setFillColor(col)
            c.circle(bx + 12, by + box_h - 2, 8, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 6)
            c.setFillColor(BG)
            c.drawCentredString(bx + 12, by + box_h - 4.5, num)
            # title
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(col)
            c.drawCentredString(bx + box_w / 2, by + box_h - 18, title)
            # subtitle
            for i, line in enumerate(sub.split("\n")):
                c.setFont("Helvetica", 6)
                c.setFillColor(TEXT_MUTED)
                c.drawCentredString(bx + box_w / 2, by + box_h - 28 - i * 9, line)

            # curved arrows between boxes
            a_start = math.radians(deg + 35)
            a_end   = math.radians(deg + 35 + 20)
            r_arr   = r_orbit - box_w * 0.1
            xs = cx + r_arr * math.cos(a_start)
            ys = cy + r_arr * math.sin(a_start)
            xe = cx + r_arr * math.cos(a_end)
            ye = cy + r_arr * math.sin(a_end)
            c.setStrokeColor(colors_list[(idx + 1) % 4])
            c.setLineWidth(1)
            c.line(xs, ys, xe, ye)

        # centre label
        c.setFillColor(CARD)
        c.circle(cx, cy, s * 0.28, fill=1, stroke=0)
        c.setStrokeColor(ACCENT)
        c.setLineWidth(1)
        c.circle(cx, cy, s * 0.28, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(ACCENT)
        c.drawCentredString(cx, cy + 4, "FEYNMAN")
        c.setFont("Helvetica", 6)
        c.setFillColor(TEXT_MUTED)
        c.drawCentredString(cx, cy - 5, "TECHNIQUE")


# ─── Style Helpers ────────────────────────────────────────────────────────────

def build_styles():
    styles = getSampleStyleSheet()
    base = dict(fontName="Helvetica", textColor=TEXT, backColor=BG,
                leading=16, spaceAfter=4)
    defs = {
        "Cover_Title":  dict(fontSize=38, fontName="Helvetica-Bold",
                              textColor=ACCENT, leading=44, alignment=TA_LEFT,
                              spaceBefore=0, spaceAfter=6),
        "Cover_Sub":    dict(fontSize=14, textColor=TEXT_MUTED,
                              leading=20, alignment=TA_LEFT, spaceAfter=4),
        "Cover_Tag":    dict(fontSize=10, textColor=ACCENT2,
                              leading=14, alignment=TA_LEFT),
        "Chapter":      dict(fontSize=22, fontName="Helvetica-Bold",
                              textColor=ACCENT, leading=28,
                              spaceBefore=8, spaceAfter=4),
        "Section":      dict(fontSize=13, fontName="Helvetica-Bold",
                              textColor=WHITE, leading=18,
                              spaceBefore=10, spaceAfter=3),
        "Body":         dict(fontSize=9.5, leading=15, alignment=TA_JUSTIFY,
                              spaceAfter=5),
        "Bullet":       dict(fontSize=9.5, leading=14, leftIndent=14,
                              spaceAfter=3),
        "SubBullet":    dict(fontSize=8.5, leading=13, leftIndent=28,
                              textColor=TEXT_MUTED, spaceAfter=2),
        "Label":        dict(fontSize=8, fontName="Helvetica-Bold",
                              textColor=ACCENT, spaceAfter=2),
        "Quote":        dict(fontSize=10, fontName="Helvetica-Oblique",
                              textColor=ACCENT2, leading=16,
                              leftIndent=10, spaceAfter=6),
        "Caption":      dict(fontSize=7.5, textColor=TEXT_MUTED,
                              alignment=TA_CENTER, spaceAfter=6),
        "Callout":      dict(fontSize=9, fontName="Helvetica-Bold",
                              textColor=BG, backColor=ACCENT,
                              leading=14, leftIndent=6, rightIndent=6,
                              spaceAfter=6, spaceBefore=6,
                              borderPad=4),
    }
    result = {}
    for name, overrides in defs.items():
        props = {**base, **overrides}
        result[name] = ParagraphStyle(name, **props)
    return result


# ─── Page Template ────────────────────────────────────────────────────────────

def _draw_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PW, PH, fill=1, stroke=0)

    # Subtle top accent bar
    canvas.setFillColor(ACCENT)
    canvas.rect(0, PH - 3, PW, 3, fill=1, stroke=0)

    # Footer
    canvas.setFillColor(DIVIDER)
    canvas.rect(0, 0, PW, 10*mm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(20*mm, 3.5*mm, "ELITE PERFORMANCE BLUEPRINT")
    canvas.drawRightString(PW - 20*mm, 3.5*mm, f"p. {doc.page}")
    canvas.restoreState()


def _draw_cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
    # Large accent stripe on left
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0, 3*mm, PH, fill=1, stroke=0)
    canvas.restoreState()


def make_doc(filename):
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=22*mm,
        rightMargin=22*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )
    content_width = PW - 44*mm

    cover_frame = Frame(0, 0, PW, PH, leftPadding=22*mm, bottomPadding=20*mm,
                        rightPadding=22*mm, topPadding=20*mm, id="cover")
    body_frame  = Frame(22*mm, 14*mm, content_width, PH - 34*mm,
                        leftPadding=0, bottomPadding=0,
                        rightPadding=0, topPadding=0, id="body")

    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=_draw_cover_bg),
        PageTemplate(id="Body",  frames=[body_frame],  onPage=_draw_background),
    ])
    return doc, content_width


# ─── Content Builders ─────────────────────────────────────────────────────────

def cover_page(S, W):
    return [
        Spacer(1, 28*mm),
        Paragraph("ELITE", S["Cover_Title"]),
        Paragraph("PERFORMANCE", S["Cover_Title"]),
        Paragraph("BLUEPRINT", S["Cover_Title"]),
        Spacer(1, 6*mm),
        AccentLine(W * 0.55, ACCENT, 1.5),
        Spacer(1, 6*mm),
        Paragraph(
            "A Research-Based, Neuroscience-Driven Guide to Peak Human Performance",
            S["Cover_Sub"]
        ),
        Spacer(1, 4*mm),
        Paragraph(
            "Circadian Reset  ·  Deep Work  ·  Feynman Technique  ·  Dopamine Regulation\n"
            "Gut-Brain Axis  ·  Resistance Training  ·  Visual Focus Protocols",
            S["Cover_Tag"]
        ),
        Spacer(1, 18*mm),
        Paragraph("Engineered for: 22M · 6 ft · 67 kg · Engineering Student → Founder", S["Caption"]),
        PageBreak(),
    ]


def toc_entries(S, W):
    rows = [
        ("01", "THE ROOT CAUSE — Circadian Reset & Sleep Architecture"),
        ("02", "STOP: The Habits Destroying Your Baseline"),
        ("03", "DEEP WORK — Cal Newport's Framework, Applied"),
        ("04", "ACCELERATED LEARNING — The Feynman Technique"),
        ("05", "VISUAL FOCUS PROTOCOLS — Huberman & Beyond"),
        ("06", "DOPAMINE REGULATION — Engineering Sustained Drive"),
        ("07", "DIET, GUT MICROBIOME & THE GUT-BRAIN AXIS"),
        ("08", "RESISTANCE TRAINING & PHYSICAL OPTIMIZATION"),
        ("09", "YOUR COMPLETE DAILY PROTOCOL"),
        ("10", "MINDSET — Execution Over Inspiration"),
    ]
    elems = [
        Paragraph("TABLE OF CONTENTS", S["Chapter"]),
        AccentLine(W, ACCENT2, 0.8),
        Spacer(1, 6*mm),
    ]
    for num, title in rows:
        tbl = Table(
            [[Paragraph(f"<font color='#{ACCENT.hexval()[2:]}'>CH {num}</font>", S["Label"]),
              Paragraph(title, S["Body"])]],
            colWidths=[18*mm, W - 18*mm]
        )
        tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("LINEBELOW",     (0, 0), (-1, -1), 0.3, DIVIDER),
        ]))
        elems.append(tbl)
    elems.append(PageBreak())
    return elems


def ch01_circadian(S, W):
    elems = [
        Paragraph("01 — THE ROOT CAUSE", S["Chapter"]),
        Paragraph("Circadian Reset & Sleep Architecture", S["Section"]),
        AccentLine(W, ACCENT, 0.8),
        Spacer(1, 4*mm),
        Paragraph(
            "Your entire system — mood, focus, digestion, hormone production, immune "
            "function — is governed by a 24-hour biological clock called the "
            "<b>suprachiasmatic nucleus (SCN)</b>. When you sleep at 6 AM, you are not "
            "simply tired; you are operating in full circadian mismatch. Every "
            "neurochemical rhythm is phase-shifted, producing chronically low dopamine "
            "and serotonin, elevated cortisol at the wrong time, impaired melatonin "
            "onset, and compromised prefrontal cortex function.", S["Body"]),
        Paragraph(
            "The science is unambiguous: chronic circadian disruption is independently "
            "associated with anxiety, depression, metabolic disorders, and reduced "
            "cognitive performance (Suni & Singh, 2024; Walker, 2017).", S["Body"]),
        Spacer(1, 3*mm),
        Paragraph("THE FIX — PHASE RESETTING YOUR SCN", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  <b>Step 1 — Anchor Wake Time (Non-Negotiable):</b> Choose 07:30 AM. Set "
            "three alarms. Get out of bed the moment the first goes off. Do this every "
            "single day including weekends for 14 days. Sleep debt is real but the "
            "circadian anchor is more important.", S["Bullet"]),
        Paragraph(
            "◆  <b>Step 2 — Morning Light Protocol (Huberman Lab):</b> Within 30 minutes "
            "of waking, get 10–15 minutes of outdoor sunlight directly into your eyes "
            "(no sunglasses). On overcast days extend to 20–30 minutes. This triggers "
            "the retino-hypothalamic tract, producing a cortisol pulse that sets your "
            "16-hour melatonin timer. This single habit is the most powerful intervention "
            "for resetting your circadian clock.", S["Bullet"]),
        Paragraph(
            "◆  <b>Step 3 — Temperature Anchor:</b> A cool shower within 30 minutes of "
            "waking elevates core body temperature through the rebound effect, signalling "
            "wakefulness to the brain. Conversely, your body must drop 1–2 °C to initiate "
            "deep sleep — so keep your bedroom at 18–20 °C.", S["Bullet"]),
        Paragraph(
            "◆  <b>Step 4 — Transition Plan:</b> If currently sleeping at 6 AM, shift your "
            "wake time earlier by 90 minutes every 2 days until you reach 07:30 AM. "
            "Brutal compliance in the first week will eliminate the need for years of "
            "sub-par performance.", S["Bullet"]),
        Paragraph(
            "◆  <b>Step 5 — Light Hygiene at Night:</b> At 9:30 PM, dim all lights and "
            "switch screens to night mode. Bright light after 9 PM suppresses melatonin "
            "by up to 50% (Gooley et al., 2011). Use blue-light-blocking glasses if "
            "necessary.", S["Bullet"]),
        Spacer(1, 4*mm),
        Paragraph("SLEEP ARCHITECTURE — WHAT ACTUALLY HAPPENS AT NIGHT", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Sleep is not passive recovery. It is active neural maintenance. "
            "Your brain cycles through 90-minute ultradian stages:", S["Body"]),
        Paragraph(
            "▸  <b>N1–N2 (Light Sleep):</b> Memory consolidation begins. Spindles replay the day's learning.", S["SubBullet"]),
        Paragraph(
            "▸  <b>N3 (Slow-Wave / Deep Sleep):</b> The glymphatic system flushes metabolic waste (including "
            "beta-amyloid linked to cognitive decline). HGH is released. This is your physical repair cycle.", S["SubBullet"]),
        Paragraph(
            "▸  <b>REM Sleep:</b> Emotional processing, creative pattern recognition, and motor skill consolidation. "
            "REM is highest in the final 2 hours — which is why cutting sleep from 8 to 6 hours eliminates 50–60% of "
            "your REM sleep.", S["SubBullet"]),
        Spacer(1, 3*mm),
        Paragraph(
            '"Sleep is the single most effective thing you can do to reset your brain and body\'s health."',
            S["Quote"]
        ),
        Paragraph("— Dr. Matthew Walker, Why We Sleep (2017)", S["Caption"]),
        Spacer(1, 3*mm),
        CircadianDiagram(size=95),
        Spacer(1, 2*mm),
        Paragraph("Your 24-Hour Biological Clock — Key events mapped to optimal timing", S["Caption"]),
        Spacer(1, 3*mm),
        Paragraph("SLEEP HYGIENE STACK", S["Section"]),
        Spacer(1, 2*mm),
    ]
    hygiene = [
        ("Room temperature", "18–20 °C — non-negotiable for deep sleep onset"),
        ("Darkness", "100% blackout. Even dim light through eyelids disrupts melatonin"),
        ("No food 3 hrs before bed", "Digestion raises core temp, destroys slow-wave sleep"),
        ("No training 3 hrs before bed", "Elevated core temperature delays melatonin by 90+ min"),
        ("Magnesium Glycinate", "200–400 mg before bed — aids GABAergic relaxation"),
        ("No alcohol", "Alcohol fragments sleep architecture, eliminates REM phases"),
        ("Consistent bed time", "±30 min variance maximum. Circadian clock runs on precision"),
    ]
    tbl = Table(
        [[Paragraph(k, S["Label"]), Paragraph(v, S["Body"])] for k, v in hygiene],
        colWidths=[44*mm, W - 44*mm]
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, -1), CARD),
        ("TEXTCOLOR",     (0, 0), (0, -1), ACCENT),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (0, -1),  6),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.3, DIVIDER),
    ]))
    elems.append(tbl)
    elems.append(PageBreak())
    return elems


def ch02_stop(S, W):
    elems = [
        Paragraph("02 — STOP", S["Chapter"]),
        Paragraph("Habits Actively Destroying Your Baseline", S["Section"]),
        AccentLine(W, RED_SOFT, 0.8),
        Spacer(1, 4*mm),
        Paragraph("STOP SMOKING — THE NEUROSCIENCE", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Even 1–2 cigarettes per day causes measurable, acute vasoconstriction "
            "lasting 30–45 minutes per cigarette. Cerebral blood flow to the prefrontal "
            "cortex — the seat of executive function, planning, and impulse control — "
            "drops immediately. You are literally reducing your cognitive hardware every "
            "time you smoke.", S["Body"]),
        Paragraph(
            "◆  <b>Nicotine Withdrawal Anxiety Loop:</b> Nicotine artificially spikes "
            "dopamine. Between cigarettes, dopamine drops below your natural baseline, "
            "creating an anxiety state that only another cigarette temporarily relieves. "
            "You are not smoking to feel good — you are smoking to feel normal. Your "
            "natural baseline will recover within 2–4 weeks of cessation.", S["Bullet"]),
        Paragraph(
            "◆  <b>Protocol:</b> Replace the smoking ritual with a 5-minute walk + "
            "physiological sigh (2 quick inhales, 1 long exhale ×5). This directly "
            "activates your parasympathetic nervous system and provides a neurochemical "
            "alternative to the anxiolytic effect of nicotine.", S["Bullet"]),
        Spacer(1, 4*mm),
        Paragraph("STOP SLEEPING AT 6 AM — THE CASCADE", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Sleeping at 6 AM means your cortisol morning peak (which should occur at "
            "07:30–08:30 AM to energise waking) is completely misaligned. You wake when "
            "your cortisol is crashing. Your melatonin release, which should begin at "
            "~10 PM, is phase-shifted to ~4 AM. Every hormone, enzyme, and "
            "neurotransmitter release in your body is on the wrong schedule.", S["Body"]),
        Paragraph(
            "The result: chronic low-grade inflammation, impaired neuroplasticity, "
            "low motivation, digestive dysfunction (MMC only runs during fasting/sleep), "
            "and the subjective feeling of being permanently 'behind'.", S["Body"]),
        Spacer(1, 4*mm),
        Paragraph("STOP CONTEXT SWITCHING", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Every time you switch tasks — from coding to Instagram to a YouTube video "
            "— your prefrontal cortex spends 15–23 minutes re-engaging with the original "
            "task at full depth (Leroy, 2009 — 'attention residue'). If you check your "
            "phone 20 times during a study session, you have had zero deep work.", S["Body"]),
        Paragraph(
            "◆  <b>Rule:</b> During any deep work block, your phone is physically in "
            "another room. Not face-down. Not on silent. In another room.", S["Bullet"]),
        PageBreak(),
    ]
    return elems


def ch03_deep_work(S, W):
    elems = [
        Paragraph("03 — DEEP WORK", S["Chapter"]),
        Paragraph("Cal Newport's Framework — Engineered for a Founder Mindset", S["Section"]),
        AccentLine(W, ACCENT2, 0.8),
        Spacer(1, 4*mm),
        Paragraph(
            '"Deep work is the ability to focus without distraction on a cognitively '
            'demanding task. It\'s a skill that allows you to quickly master complicated '
            'information and produce better results in less time."',
            S["Quote"]
        ),
        Paragraph("— Cal Newport, Deep Work (2016)", S["Caption"]),
        Spacer(1, 3*mm),
        Paragraph(
            "In a world of fragmented attention, the ability to produce at an elite level "
            "of concentration is a rare and valuable skill — and it is trainable. Newport "
            "identifies four philosophies:", S["Body"]),
        Paragraph(
            "▸  <b>Monastic:</b> Complete isolation from shallow work (Knuth). Not suitable for students.", S["SubBullet"]),
        Paragraph(
            "▸  <b>Bimodal:</b> Alternate between multi-day deep-work retreats and normal life. Works for established professionals.", S["SubBullet"]),
        Paragraph(
            "▸  <b>Rhythmic:</b> Fixed daily deep-work sessions. <b>⟵ This is your approach.</b> Same time every day, "
            "protected blocks, no exceptions.", S["SubBullet"]),
        Paragraph(
            "▸  <b>Journalistic:</b> Seize any free moment for deep work. Requires high mental training to enter flow quickly.", S["SubBullet"]),
        Spacer(1, 4*mm),
        Paragraph("THE RHYTHMIC DEEP WORK SYSTEM — YOUR PROTOCOL", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  <b>Two 90-Minute Blocks:</b> 09:00–10:30 AM and 11:00 AM–12:30 PM. "
            "These align with your cortisol/norepinephrine peak after morning light "
            "exposure, maximising neural firing rates and pattern recognition.", S["Bullet"]),
        Paragraph(
            "◆  <b>Pre-Work Ritual (5 min):</b> Same sequence every day. "
            "This is a conditioned cue. Write today's one deliverable. Review "
            "your 12-week goal. Start a timer. Brain associates this ritual "
            "with entering focused state — entry time to flow drops from 15 min "
            "to under 5 min within 3 weeks.", S["Bullet"]),
        Paragraph(
            "◆  <b>Task Specificity:</b> Do not write 'study engineering'. Write: "
            "'Derive and solve 5 problems from Chapter 7 signal processing.' "
            "Vague intentions produce vague attention.", S["Bullet"]),
        Paragraph(
            "◆  <b>Scoreboard:</b> Track your deep work hours in a physical notebook. "
            "Newport recommends a simple tally. The visual feedback creates a "
            "'chain' you don't want to break (habit stacking via loss aversion).", S["Bullet"]),
        Paragraph(
            "◆  <b>Shutdown Ritual:</b> At the end of each day, say aloud: "
            "'Shutdown complete.' This trains your unconscious that work concerns "
            "are parked, enabling true cognitive rest and preventing rumination.", S["Bullet"]),
        Spacer(1, 4*mm),
        Paragraph("THE DEEP WORK SESSION — ARCHITECTURE", S["Section"]),
        Spacer(1, 2*mm),
        DeepWorkFlow(width=W),
        Spacer(1, 3*mm),
        Paragraph("Each 90-minute block follows this exact sequence. Consistency builds neural conditioning.", S["Caption"]),
        Spacer(1, 4*mm),
        Paragraph("NEWPORT'S LAW OF PRODUCTIVITY", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "High Quality Work Produced  =  Time Spent  ×  Intensity of Focus",
            S["Callout"]
        ),
        Spacer(1, 3*mm),
        Paragraph(
            "Most students optimise Time Spent (studying for 8 hours) while Intensity "
            "hovers at 20%. Elite performers compress time and maximise intensity. "
            "Two hours at 95% intensity produces more than eight hours at 30%.", S["Body"]),
        Spacer(1, 3*mm),
        Paragraph("ATTENTION RESIDUE — THE INVISIBLE TAX", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Dr Sophie Leroy (2009) demonstrated that switching from Task A to Task B "
            "before Task A is complete leaves 'attention residue' — part of your "
            "cognitive processing remains on Task A, degrading performance on Task B. "
            "The fix: <b>Complete defined work units</b> before switching. Never leave a "
            "problem mid-sentence. Write a one-line next-action note before switching.", S["Body"]),
        PageBreak(),
    ]
    return elems


def ch04_feynman(S, W):
    elems = [
        Paragraph("04 — ACCELERATED LEARNING", S["Chapter"]),
        Paragraph("The Feynman Technique — First-Principles Understanding", S["Section"]),
        AccentLine(W, ACCENT, 0.8),
        Spacer(1, 4*mm),
        Paragraph(
            '"You do not really understand something unless you can explain it to '
            'your grandmother."',
            S["Quote"]
        ),
        Paragraph("— Richard Feynman, Nobel Laureate in Physics", S["Caption"]),
        Spacer(1, 3*mm),
        Paragraph(
            "Richard Feynman had the highest IQ in his MIT cohort but famously "
            "attributed his genius not to raw intelligence but to his method of "
            "learning. His notebook bore the inscription: 'What I cannot create, "
            "I do not understand.' The Feynman Technique is the fastest known method "
            "to move from superficial familiarity to genuine, deep understanding of "
            "any concept.", S["Body"]),
        Spacer(1, 4*mm),
        Paragraph("THE FOUR STEPS", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "<b>Step 1 — Choose and Study the Concept:</b> Select one specific concept "
            "(e.g., Fourier Transform, or the kernel of a market strategy). Read the "
            "primary source — textbook chapter, paper, or original material. Take linear "
            "notes. Do not highlight. Writing forces encoding.", S["Bullet"]),
        Paragraph(
            "<b>Step 2 — Teach it to a 12-Year-Old:</b> Close all materials. On a blank "
            "page, explain the concept as if teaching someone with zero background. Use "
            "plain language. No jargon. Draw diagrams. The moment you cannot explain "
            "something simply, you have found a gap.", S["Bullet"]),
        Paragraph(
            "<b>Step 3 — Identify Your Gaps:</b> Where did you stumble? Where did you "
            "reach for jargon to hide a lack of understanding? Return to the source "
            "material specifically for those gaps. Do not re-read everything — zero in "
            "on the exact gap.", S["Bullet"]),
        Paragraph(
            "<b>Step 4 — Simplify and Use Analogies:</b> Return to your explanation and "
            "simplify further. Replace complex sentences with analogies. If you can "
            "connect the concept to something you already know intuitively, the neural "
            "encoding is complete. This is first-principles understanding.", S["Bullet"]),
        Spacer(1, 4*mm),
        Paragraph("FEYNMAN LOOP DIAGRAM", S["Section"]),
        Spacer(1, 2*mm),
        FeynmanFlow(size=80),
        Spacer(1, 2*mm),
        Paragraph("Repeat this loop until your explanation is one a child can follow.", S["Caption"]),
        Spacer(1, 4*mm),
        Paragraph("ENGINEERING APPLICATION — YOUR USE CASES", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  After every lecture or study session, spend 10 minutes writing a "
            "plain-language explanation of the core concept in your notebook.", S["Bullet"]),
        Paragraph(
            "◆  When preparing for exams, Feynman every topic in the syllabus — "
            "not to memorise but to understand. Understanding-based recall is far "
            "more durable than rote memorisation under pressure.", S["Bullet"]),
        Paragraph(
            "◆  As a future founder, apply Feynman to business models, market "
            "structures, and technical concepts. If you cannot explain your startup "
            "idea in 2 sentences to a non-technical person, you don't understand "
            "your own business yet.", S["Bullet"]),
        Spacer(1, 3*mm),
        Paragraph("COMPLEMENTARY TECHNIQUE: SPACED REPETITION", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Feynman gives you <i>understanding</i>. Spaced repetition gives you "
            "<i>retention</i>. Use Anki (free, open source) to create flashcards "
            "from your Feynman explanations. The algorithm optimises review intervals "
            "to exploit the 'spacing effect' — the cognitive phenomenon where information "
            "reviewed at increasing intervals is retained far longer than massed "
            "practice (Ebbinghaus, 1885).", S["Body"]),
        PageBreak(),
    ]
    return elems


def ch05_focus(S, W):
    elems = [
        Paragraph("05 — VISUAL FOCUS PROTOCOLS", S["Chapter"]),
        Paragraph("Huberman's Neuroscience of Attention", S["Section"]),
        AccentLine(W, ACCENT2, 0.8),
        Spacer(1, 4*mm),
        Paragraph(
            "Dr Andrew Huberman (Stanford Neurobiology Lab) identified that the "
            "visual system is the dominant driver of attentional focus. The same "
            "neural circuitry that physically narrows your visual field also "
            "increases cognitive focus and activates the locus coeruleus (your "
            "brain's norepinephrine centre, critical for alertness and learning).", S["Body"]),
        Spacer(1, 3*mm),
        Paragraph("PROTOCOL 1 — VISUAL CONVERGENCE (FOCUS PRIMER)", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  For 30–60 seconds before starting a deep work block, stare at a "
            "single point — your screen cursor, a pen tip, a mark on the wall — "
            "without blinking. Physically narrow your gaze.", S["Bullet"]),
        Paragraph(
            "◆  This engages the 'covert attention system', increasing acetylcholine "
            "release and activating the basal forebrain — the circuit that tells your "
            "cortex: 'this matters, encode this.' It is a hard reset into focus mode.", S["Bullet"]),
        Paragraph(
            "◆  Huberman reports this can cut time-to-focus from 15 minutes to under "
            "2 minutes.", S["Bullet"]),
        Spacer(1, 3*mm),
        Paragraph("PROTOCOL 2 — PANORAMIC VISION (STRESS RESET)", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  The opposite of convergent focus is optic-flow / panoramic vision. "
            "When you are overstimulated or anxious, softening your gaze and looking "
            "at a wide scene (horizon, open sky) activates the parasympathetic "
            "nervous system. This is why walking outside during your lunch break "
            "resets your stress state.", S["Bullet"]),
        Spacer(1, 3*mm),
        Paragraph("PROTOCOL 3 — THE POMODORO STRUCTURE (ADJUSTED)", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "The classical Pomodoro Technique (25 min work / 5 min break) is effective "
            "for low-complexity tasks. For deep engineering and learning, the optimal "
            "work interval aligns with your <b>ultradian rhythm</b> — 90 minutes.", S["Body"]),
    ]
    _pomo_data = [
        ["Task Type", "Work Interval", "Break", "Best For"],
        ["Administrative / Shallow", "25 min", "5 min", "Emails, admin, scheduling"],
        ["Learning / Engineering", "50 min", "10 min", "Problem sets, studying"],
        ["Deep Work / Coding", "90 min", "20 min", "Build sessions, deep study"],
    ]
    _pomo_tbl = Table(_pomo_data, colWidths=[42*mm, 30*mm, 22*mm, W - 94*mm])
    _pomo_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR",     (0, 0), (-1, 0), BG),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("BACKGROUND",    (0, 1), (-1, -1), CARD),
        ("TEXTCOLOR",     (0, 1), (-1, -1), TEXT),
        ("GRID",          (0, 0), (-1, -1), 0.3, DIVIDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("ALIGN",         (1, 0), (-1, -1), "CENTER"),
    ]))
    elems.append(_pomo_tbl)
    elems.append(Spacer(1, 4*mm))
    elems += [
        Paragraph("PROTOCOL 4 — NON-SLEEP DEEP REST (NSDR / YOGA NIDRA)", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "A 10–20 minute NSDR protocol after your first deep work block accelerates "
            "skill consolidation. Huberman's research shows NSDR increases dopamine "
            "levels in the striatum by up to 65% and enhances neuroplasticity in the "
            "subsequent work session. Use the free 10-min NSDR script on YouTube "
            "(search: 'Huberman NSDR').", S["Body"]),
        Spacer(1, 3*mm),
        Paragraph("PROTOCOL 5 — COLD EXPOSURE FOR COGNITIVE AROUSAL", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "1–3 minutes of cold water exposure (shower at 15–20 °C) produces a "
            "persistent 2.5× elevation of dopamine baseline lasting 2–4 hours "
            "(Šrámek et al., 2000; Huberman, 2021). Unlike caffeine, this is not "
            "followed by a crash. Use cold exposure as an alternative to a second "
            "coffee in the early afternoon.", S["Body"]),
        PageBreak(),
    ]
    return elems


def ch06_dopamine(S, W):
    elems = [
        Paragraph("06 — DOPAMINE REGULATION", S["Chapter"]),
        Paragraph("Engineering Sustained Drive — Not Cheap Spikes", S["Section"]),
        AccentLine(W, ACCENT, 0.8),
        Spacer(1, 4*mm),
        Paragraph(
            "Dopamine is not the 'pleasure chemical'. It is the <b>motivation and "
            "pursuit chemical</b>. Its primary function is to drive approach behaviour "
            "— to make you want to pursue goals. When dopamine baseline is low, "
            "nothing feels worth doing. When chronically spiked and crashed, the same "
            "things that used to feel rewarding feel flat (receptor downregulation).", S["Body"]),
        Spacer(1, 3*mm),
        Paragraph("YOUR CURRENT DOPAMINE PROBLEM", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Disrupted sleep → low baseline dopamine → seek quick dopamine hits "
            "(social media, plan-switching, smoking) → spike and crash → lower "
            "baseline → more seeking. This is the cycle producing your inconsistency.", S["Callout"]),
        Spacer(1, 3*mm),
        Paragraph("THE DOPAMINE REGULATION PROTOCOL", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  <b>Eliminate Cheap Dopamine (Morning):</b> Do not check social media, "
            "news, or YouTube before completing your first deep work block. Your first "
            "dopamine hit of the day sets the reference level for what feels rewarding. "
            "Spike it with Instagram at 8 AM and studying at 9 AM feels unbearably "
            "boring.", S["Bullet"]),
        Paragraph(
            "◆  <b>Attach Dopamine to Effort, Not Outcome:</b> Before hard tasks, "
            "consciously tell yourself: 'I am about to do something hard, and the "
            "friction I feel is the signal that I am building the skill.' This "
            "cognitive reframe — backed by Stanford research (Crum, 2007) — "
            "measurably increases dopamine release during the effortful task.", S["Bullet"]),
        Paragraph(
            "◆  <b>Intermittent Reinforcement Removal:</b> Eliminate variable-reward "
            "loops (social media feeds, Reddit, phone notifications). These are "
            "engineered to spike dopamine unpredictably — the strongest known "
            "pattern for creating compulsive behaviour (same mechanism as slot "
            "machines). Delete or time-restrict these apps.", S["Bullet"]),
        Paragraph(
            "◆  <b>Dopamine Rebuild Protocols:</b> The following activities provide "
            "sustained dopamine elevation without the crash:", S["Bullet"]),
        Paragraph(
            "▸  Zone 2 cardio (30–45 min) — elevates baseline for hours", S["SubBullet"]),
        Paragraph(
            "▸  Cold exposure (1–3 min cold shower) — 2.5× baseline elevation for 2–4 hrs", S["SubBullet"]),
        Paragraph(
            "▸  Resistance training — testosterone + growth hormone + dopamine trifecta", S["SubBullet"]),
        Paragraph(
            "▸  Morning sunlight — serotonin precursor, regulates the dopamine system", S["SubBullet"]),
        Paragraph(
            "▸  Deep work completion — the 'done' signal releases dopamine proportional "
            "to the difficulty of the task. Harder work = bigger reward signal.", S["SubBullet"]),
        Spacer(1, 3*mm),
        Paragraph("THE ANXIETY-DOPAMINE CONNECTION", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Your anxiety about 'being behind peers' is partially a dopamine-depleted "
            "state combined with an overactive amygdala (from circadian disruption and "
            "chronic stress). The <b>Physiological Sigh</b> (double inhale through nose "
            "followed by a long exhale through mouth) is the fastest-acting "
            "physiological reset. Two to five repetitions drop heart rate within "
            "90 seconds and measurably reduce amygdala activation (Balban et al., 2023).", S["Body"]),
        PageBreak(),
    ]
    return elems


def ch07_diet(S, W):
    elems = [
        Paragraph("07 — DIET, GUT MICROBIOME & THE GUT-BRAIN AXIS", S["Chapter"]),
        Paragraph("Fuelling the Brain & Healing the Gut", S["Section"]),
        AccentLine(W, colors.HexColor("#5DAD62"), 0.8),
        Spacer(1, 4*mm),
        Paragraph(
            "Your gut contains 100–500 million neurons — more than the spinal cord — "
            "connected to the brain via the vagus nerve. 90% of your body's serotonin "
            "is produced in the gut. Gut dysbiosis (microbial imbalance) directly "
            "causes brain fog, anxiety, low mood, and cognitive impairment through "
            "the gut-brain axis. Fixing your gut is not optional — it is foundational "
            "to fixing your mind.", S["Body"]),
        Spacer(1, 3*mm),
        Paragraph("TIME-RESTRICTED FEEDING (TRF) — YOUR NON-NEGOTIABLE", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Eat within a <b>10-hour window: 10:00 AM – 8:00 PM</b>. Outside this "
            "window, consume only water, black coffee, or plain tea.", S["Body"]),
        Paragraph(
            "◆  <b>Migrating Motor Complex (MMC):</b> Between meals and during fasting, "
            "your gut runs an electrical 'sweeping' wave every 90 minutes that clears "
            "bacteria, undigested food, and debris. This only runs in a fasted state. "
            "Constant eating — common with disorganised schedules — prevents the MMC "
            "from running, causing bacterial overgrowth, bloating, and the 'mild "
            "digestion issues' you experience.", S["Bullet"]),
        Paragraph(
            "◆  <b>Circadian Alignment of Feeding:</b> Eating aligned with daylight "
            "hours (not at night) optimises liver enzyme activity, insulin sensitivity, "
            "and gut motility. Eating at 2 AM disrupts all three.", S["Bullet"]),
        Spacer(1, 4*mm),
        Paragraph("MACRONUTRIENT TARGETS (For 67 kg, performance goals)", S["Section"]),
        Spacer(1, 2*mm),
    ]

    macros = [
        ["Protein", "130–145 g/day", "Tyrosine (dopamine), tryptophan (serotonin) precursors. Muscle = endocrine organ."],
        ["Fats", "60–80 g/day", "Brain is 60% fat. Omega-3s (EPA/DHA) reduce neuroinflammation, support testosterone."],
        ["Carbohydrates", "200–250 g/day", "Complex only (oats, sweet potato, rice). Prevents blood sugar spikes that destroy focus."],
        ["Fibre", "≥ 30 g/day", "Feeds Lactobacillus & Bifidobacterium — your key gut-brain bacteria."],
        ["Water", "≥ 2.5 L/day", "500 ml upon waking. Dehydration of 1–2% degrades working memory and attention."],
    ]
    tbl = Table(
        [[Paragraph(r[0], S["Label"]),
          Paragraph(r[1], S["Body"]),
          Paragraph(r[2], S["Body"])] for r in macros],
        colWidths=[30*mm, 28*mm, W - 58*mm]
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, -1), CARD),
        ("TEXTCOLOR",     (0, 0), (0, -1), colors.HexColor("#5DAD62")),
        ("FONTNAME",      (0, 0), (0, -1), "Helvetica-Bold"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.3, DIVIDER),
    ]))
    elems.append(tbl)
    elems.append(Spacer(1, 4*mm))

    elems += [
        Paragraph("GUT MICROBIOME — THE PRACTICAL REBUILD", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  <b>Fermented Foods Daily:</b> Greek yogurt, kefir, kimchi, or sauerkraut. "
            "A landmark Stanford study (Wastyk et al., 2021) showed that a high-fermented "
            "food diet for 10 weeks increased microbiome diversity and decreased 19 "
            "inflammatory proteins — including interleukin-6, linked to depression.", S["Bullet"]),
        Paragraph(
            "◆  <b>Prebiotic Fibre:</b> Feed your existing bacteria. Garlic, onions, "
            "leeks, asparagus, oats, and bananas contain inulin and FOS — "
            "preferential food for beneficial bacteria.", S["Bullet"]),
        Paragraph(
            "◆  <b>Eliminate Ultra-Processed Foods:</b> Emulsifiers (polysorbate 80, "
            "carrageenan) found in packaged foods directly damage the gut mucosal "
            "lining, increasing intestinal permeability ('leaky gut') and triggering "
            "systemic inflammation that reaches the brain.", S["Bullet"]),
        Paragraph(
            "◆  <b>Anti-Inflammatory Stack:</b> "
            "Turmeric (with black pepper for bioavailability) + Omega-3s + "
            "Vitamin D3 (4,000 IU/day, especially if sun exposure is limited).", S["Bullet"]),
        Spacer(1, 4*mm),
        Paragraph("MEAL TIMING PROTOCOL", S["Section"]),
        Spacer(1, 2*mm),
    ]
    timing = [
        ("10:30 AM — Breakfast", "High protein: 4 eggs + spinach + avocado. Fats slow glucose absorption, protein provides tyrosine for morning dopamine."),
        ("1:00 PM — Lunch", "Largest meal. Protein source + complex carbs + salad. Walk 10–15 min post-meal to blunt glucose spike by 30%."),
        ("3:30 PM — Optional snack", "Greek yogurt + nuts + berries. Carbs for afternoon energy, protein to prevent evening cravings."),
        ("6:30 PM — Dinner", "Last meal. High protein + complex carbs (replenish glycogen, support serotonin → melatonin production). No food after 8 PM."),
    ]
    for time, desc in timing:
        tbl2 = Table(
            [[Paragraph(time, S["Label"]), Paragraph(desc, S["Body"])]],
            colWidths=[44*mm, W - 44*mm]
        )
        tbl2.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, 0), CARD),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 5),
            ("LINEBELOW",     (0, 0), (-1, -1), 0.3, DIVIDER),
        ]))
        elems.append(tbl2)
    elems.append(PageBreak())
    return elems


def ch08_training(S, W):
    elems = [
        Paragraph("08 — RESISTANCE TRAINING & PHYSICAL OPTIMIZATION", S["Chapter"]),
        Paragraph("Muscle as an Endocrine & Cognitive Organ", S["Section"]),
        AccentLine(W, colors.HexColor("#D95B4A"), 0.8),
        Spacer(1, 4*mm),
        Paragraph(
            "At 67 kg on a 6 ft frame, you are significantly under-muscled. This is not "
            "an aesthetic issue — it is a performance one. Skeletal muscle is an "
            "endocrine organ that secretes over 600 myokines when contracted. "
            "These myokines include irisin (triggers BDNF in the brain — the "
            "'miracle-grow' for neurons), IL-6 (anti-inflammatory at low levels), "
            "and IGF-1 (drives tissue repair and neuroplasticity).", S["Body"]),
        Spacer(1, 3*mm),
        Paragraph("4-DAY TRAINING FRAMEWORK", S["Section"]),
        Spacer(1, 2*mm),
    ]
    programme = [
        ["Day", "Type", "Focus", "Duration"],
        ["Mon", "Heavy Resistance", "Upper Body — Push + Pull", "50–60 min"],
        ["Tue", "Zone 2 Cardio", "Brisk walk / jog / cycle", "35–45 min"],
        ["Thu", "Heavy Resistance", "Lower Body — Squat + Hinge", "50–60 min"],
        ["Fri", "Zone 2 Cardio", "Swim / row / cycle", "35–45 min"],
        ["Wed/Sat/Sun", "Recovery", "Walk + mobility + sleep", "—"],
    ]
    tbl = Table(programme, colWidths=[20*mm, 38*mm, 60*mm, W - 118*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR",     (0, 0), (-1, 0), BG),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("BACKGROUND",    (0, 1), (-1, -1), CARD),
        ("TEXTCOLOR",     (0, 1), (-1, -1), TEXT),
        ("GRID",          (0, 0), (-1, -1), 0.3, DIVIDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("ALIGN",         (1, 0), (-1, -1), "CENTER"),
    ]))
    elems.append(tbl)
    elems += [
        Spacer(1, 4*mm),
        Paragraph("RESISTANCE TRAINING — PRINCIPLES", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  <b>Compound Movements First:</b> Squat, deadlift, bench press, row, "
            "overhead press, pull-up. These recruit the most motor units, produce "
            "the largest hormonal response, and build the structural strength needed "
            "for long-term performance.", S["Bullet"]),
        Paragraph(
            "◆  <b>Rep Range:</b> 4–6 reps at 80–85% of your 1RM for the primary "
            "compound. 8–12 reps for accessories. Heavy lifting triggers testosterone "
            "and HGH release to a significantly greater degree than high-rep, "
            "low-weight training.", S["Bullet"]),
        Paragraph(
            "◆  <b>Progressive Overload:</b> Add 2.5 kg or 1 additional rep every "
            "week. If you are not progressing, you are not adapting. Track every "
            "session in a notebook.", S["Bullet"]),
        Paragraph(
            "◆  <b>Caloric Surplus:</b> At 67 kg, you cannot build significant muscle "
            "in a deficit. Target a modest surplus of 200–300 kcal above maintenance "
            "(est. 2600–2900 kcal/day depending on activity). Prioritise calorie "
            "quality — whole foods, high protein.", S["Bullet"]),
        Spacer(1, 3*mm),
        Paragraph("ZONE 2 CARDIO — THE MITOCHONDRIAL DIVIDEND", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "Zone 2 cardio (conversational pace — roughly 60–70% max heart rate) "
            "is the highest-yield longevity and cognitive performance investment. "
            "It builds mitochondrial density — the literal cellular energy capacity "
            "of every cell in your body, including your neurons. 150–180 minutes of "
            "Zone 2 per week is Dr Peter Attia's minimum threshold for cognitive "
            "longevity.", S["Body"]),
        PageBreak(),
    ]
    return elems


def ch09_protocol(S, W):
    elems = [
        Paragraph("09 — YOUR COMPLETE DAILY PROTOCOL", S["Chapter"]),
        Paragraph("The Blueprint — Engineered Around Your Biological Rhythms", S["Section"]),
        AccentLine(W, ACCENT, 0.8),
        Spacer(1, 4*mm),
    ]
    schedule = [
        ("07:30", "Wake + Light", ACCENT,
         "Out of bed immediately. 500 ml water + pinch sea salt. 10–15 min outdoor sunlight. No phone."),
        ("07:50", "Cold Shower + Movement", ACCENT2,
         "2 min cold exposure for dopamine elevation. 10 min light stretching / mobility."),
        ("08:10", "Mindset Protocol", colors.HexColor("#9B59B6"),
         "Review your ONE major goal for the day. Write today's deep work deliverable (specific, not vague). Set intention."),
        ("09:00", "Deep Work Block 1", ACCENT2,
         "90 min. Phone in another room. Visual convergence prime (30 sec). Full execution. No interruptions."),
        ("10:30", "Break + Breakfast", colors.HexColor("#5DAD62"),
         "20 min. NSDR or walk outside. High-protein breakfast: eggs + spinach + avocado."),
        ("11:00", "Deep Work Block 2", ACCENT2,
         "90 min. Second execution block. Feynman your learning from Block 1 if studying."),
        ("12:30", "Lunch + Outdoor Walk", colors.HexColor("#5DAD62"),
         "Balanced meal. 15 min walk post-meal. No screens. Panoramic vision to lower cortisol."),
        ("13:30", "Shallow Work / Classes", TEXT_MUTED,
         "Emails, admin, classes, meetings. Cognitive peak is lower here — save creative and analytical work for the morning."),
        ("15:30", "Learning & Curiosity", ACCENT,
         "Self-directed learning. Apply Feynman Technique to new concepts. Read primary sources."),
        ("16:30", "Resistance Training", colors.HexColor("#D95B4A"),
         "45–60 min. Compound movements. Log every session. Strength peaks in late afternoon (circadian-aligned)."),
        ("18:00", "Post-Training Protein", colors.HexColor("#5DAD62"),
         "30g protein within 45 min of training. Shake or whole food."),
        ("18:30", "Dinner", colors.HexColor("#5DAD62"),
         "Last meal. High protein + complex carbs. Eat slowly. No screens at table."),
        ("20:00", "Feynman Review + Reading", ACCENT,
         "Consolidate today's learning. Read (non-fiction or fiction). Journal 3 things accomplished."),
        ("21:30", "Digital Sunset", TEXT_MUTED,
         "All screens off or blue-light glasses. Dim lights. Stretch or meditate. Brain begins melatonin ramp."),
        ("22:30", "Sleep", colors.HexColor("#4A70B0"),
         "Bedroom: 18–20°C, 100% blackout, no phone. 8 hours of sleep = 5–6 full ultradian cycles."),
    ]

    for time, title, col, desc in schedule:
        tbl = Table(
            [[Paragraph(f"<font color='#{col.hexval()[2:]}'><b>{time}</b></font>", S["Body"]),
              Paragraph(f"<b>{title}</b>", S["Body"]),
              Paragraph(desc, S["SubBullet"])]],
            colWidths=[16*mm, 42*mm, W - 58*mm]
        )
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, 0), CARD),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 5),
            ("LINEBELOW",     (0, 0), (-1, -1), 0.3, DIVIDER),
        ]))
        elems.append(tbl)

    elems += [
        Spacer(1, 4*mm),
        Paragraph(
            "EXECUTION PRINCIPLE: Do not attempt perfection on Day 1. The protocol is "
            "a target state. Start with ONE change: fix your wake time and get morning "
            "sunlight. When that is locked in for 7 days, add the next element. "
            "Discipline is built progressively, not installed overnight.", S["Callout"]),
        PageBreak(),
    ]
    return elems


def ch10_mindset(S, W):
    elems = [
        Paragraph("10 — MINDSET", S["Chapter"]),
        Paragraph("Execution Over Inspiration — The Elite Operator Framework", S["Section"]),
        AccentLine(W, ACCENT, 0.8),
        Spacer(1, 4*mm),
        Paragraph(
            "Motivation is an output, not an input. You do not need to feel motivated "
            "to start. You need to start in order to feel motivated. The motor cortex "
            "activates the cognitive systems — action precedes feeling in the neural "
            "architecture.", S["Body"]),
        Spacer(1, 3*mm),
        Paragraph("THE ELITE OPERATOR PRINCIPLES", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "◆  <b>Identity Over Goals:</b> 'I am a high-performer who trains, learns, "
            "and builds' vs. 'I want to get fit and study more.' Goals are fragile — "
            "they depend on motivation. Identity is robust — it guides automatic "
            "behaviour. Every action you take is a vote for the identity you want "
            "to build (James Clear, Atomic Habits).", S["Bullet"]),
        Paragraph(
            "◆  <b>Environment Design:</b> Your willpower is finite. Design your "
            "environment so that the right behaviours require less willpower. "
            "Put your gym clothes out the night before. Block distracting sites "
            "with Cold Turkey or Freedom. Delete social media apps from your phone. "
            "Your environment shapes 60% of your behaviour without conscious effort.", S["Bullet"]),
        Paragraph(
            "◆  <b>The 12-Week Year:</b> Stop thinking in years. A 12-week goal with "
            "weekly review creates urgency without overwhelm. Every Sunday, score "
            "your week (% of planned actions executed). Under 65% = adjust strategy, "
            "not motivation. This is borrowed from Brian Moran's system and used "
            "by elite performers across domains.", S["Bullet"]),
        Paragraph(
            "◆  <b>Comparison is a Data Point, Not a Verdict:</b> Feeling behind peers "
            "is neurologically a stress response. Reframe: every founder, athlete, "
            "and scholar who became elite started from behind. You are not behind — "
            "you are pre-launch. The compounding returns on the work you do now "
            "are exponential.", S["Bullet"]),
        Paragraph(
            "◆  <b>Process Scorecard:</b> You cannot control outcomes. You can control "
            "inputs. Track: hours of deep work, training sessions completed, meals on "
            "protocol, hours of sleep. After 12 weeks of optimised inputs, the outputs "
            "are statistically inevitable.", S["Bullet"]),
        Spacer(1, 4*mm),
        Paragraph("FINAL FRAME — THE COMPOUND EFFECT", S["Section"]),
        Spacer(1, 2*mm),
        Paragraph(
            "1% improvement each day for one year = 37× improvement. "
            "1% decline each day for one year = 0.03 of where you started.",
            S["Callout"]),
        Spacer(1, 3*mm),
        Paragraph(
            "The protocol in this guide is not about willpower or inspiration. It is "
            "about understanding your own neurobiology well enough to architect an "
            "environment and routine that makes elite performance the path of least "
            "resistance. Every decision in this guide is made for the same reason: "
            "it is what the evidence says works.", S["Body"]),
        Spacer(1, 4*mm),
        AccentLine(W, ACCENT, 1.5),
        Spacer(1, 3*mm),
        Paragraph(
            '"Be regular and orderly in your life so that you may be violent and '
            'original in your work."',
            S["Quote"]
        ),
        Paragraph("— Gustave Flaubert", S["Caption"]),
        Spacer(1, 6*mm),
        Paragraph(
            "References: Walker M. (2017). Why We Sleep. Penguin. | Newport C. (2016). Deep Work. Grand Central. | "
            "Huberman A. (2021–2024). Huberman Lab Podcast, Stanford. | Gooley JJ et al. (2011). J Clin Endocrinol Metab. | "
            "Leroy S. (2009). Organ Behav Hum Decis Process. | Wastyk H. et al. (2021). Cell. | "
            "Balban M. et al. (2023). Cell Reports Medicine. | Šrámek P. et al. (2000). Eur J Appl Physiol.",
            S["Caption"]
        ),
    ]
    return elems


# ─── Main ─────────────────────────────────────────────────────────────────────

def build_pdf(filename="Elite_Performance_Blueprint.pdf"):
    doc, W = make_doc(filename)
    S = build_styles()

    story = []
    # Cover (uses Cover template)
    story += cover_page(S, W)
    # Switch to body template
    story += toc_entries(S, W)
    story += ch01_circadian(S, W)
    story += ch02_stop(S, W)
    story += ch03_deep_work(S, W)
    story += ch04_feynman(S, W)
    story += ch05_focus(S, W)
    story += ch06_dopamine(S, W)
    story += ch07_diet(S, W)
    story += ch08_training(S, W)
    story += ch09_protocol(S, W)
    story += ch10_mindset(S, W)

    doc.build(story)
    print(f"PDF generated: {filename}")


if __name__ == "__main__":
    build_pdf()

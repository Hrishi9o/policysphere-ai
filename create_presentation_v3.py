"""
Dell Hackathon 2026 - Problem Statement 1
Module: create_presentation_v3.py (Professional White Deck with Screenshots)
Generates a clean, modern, light-themed 10-slide PowerPoint with embedded
product screenshots for maximum credibility.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paths
SCREENSHOT_DIR = os.path.join("docs", "screenshots")
BENCHMARK_IMG = os.path.join("results", "benchmark.png")
OUTPUT = "Hrishikesh_Shetty_PS1_MSRIT_v3.pptx"

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ── Color Palette (Clean Professional) ──
    WHITE      = RGBColor(255, 255, 255)
    OFF_WHITE  = RGBColor(248, 249, 250)
    LIGHT_GRAY = RGBColor(233, 236, 239)
    MID_GRAY   = RGBColor(173, 181, 189)
    DARK_GRAY  = RGBColor(73, 80, 87)
    CHARCOAL   = RGBColor(33, 37, 41)
    NEAR_BLACK = RGBColor(22, 25, 29)

    DELL_BLUE  = RGBColor(0, 104, 181)     # Dell corporate blue
    ACCENT     = RGBColor(0, 125, 186)     # Slightly lighter
    TEAL       = RGBColor(13, 148, 136)    # Success/benchmark
    EMERALD    = RGBColor(16, 185, 129)
    RED_ACCENT = RGBColor(220, 53, 69)     # Security/guardrails
    INDIGO     = RGBColor(79, 70, 229)     # Innovation
    AMBER      = RGBColor(245, 158, 11)

    # ── Helpers ──
    def white_bg(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = WHITE

    def add_accent_bar(slide, color=DELL_BLUE, height=0.06):
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0),
            Inches(13.333), Inches(height)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

    def add_bottom_bar(slide, text="Hrishikesh Shetty  •  MSRIT  •  Dell Campus Recruitment 2026  •  PS-1"):
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.1),
            Inches(13.333), Inches(0.4)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = CHARCOAL
        bar.line.fill.background()
        tf = bar.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(9)
        p.font.color.rgb = MID_GRAY
        p.alignment = PP_ALIGN.CENTER

    def add_slide_number(slide, num):
        tb = slide.shapes.add_textbox(Inches(12.5), Inches(7.15), Inches(0.6), Inches(0.3))
        p = tb.text_frame.paragraphs[0]
        p.text = str(num)
        p.font.size = Pt(9)
        p.font.color.rgb = MID_GRAY
        p.alignment = PP_ALIGN.RIGHT

    def add_section_tag(slide, text, color=DELL_BLUE, left=1.0, top=0.5):
        pill = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(len(text) * 0.085 + 0.4), Inches(0.32)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = color
        pill.line.fill.background()
        tf = pill.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text.upper()
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    def add_title(slide, text, top=0.9, size=28, color=CHARCOAL, left=1.0, width=11.3):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(size)
        p.font.bold = True
        p.font.color.rgb = color
        return tb

    def add_subtitle(slide, text, top=1.55, size=13, color=DARK_GRAY, left=1.0, width=11.3):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(size)
        p.font.color.rgb = color
        return tb

    def add_body_text(slide, text, left, top, width, height, size=11, color=DARK_GRAY, bold=False):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, line in enumerate(text.split("\n")):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(size)
            p.font.color.rgb = color
            p.font.bold = bold
            p.space_after = Pt(4)
        return tb

    def add_metric_card(slide, left, top, value, label, accent_color, width=2.5, height=1.4):
        # Card background
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = OFF_WHITE
        card.line.color.rgb = LIGHT_GRAY
        card.line.width = Pt(1)

        # Accent left strip
        strip = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top + 0.15), Inches(0.05), Inches(height - 0.3)
        )
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent_color
        strip.line.fill.background()

        # Value
        vtb = slide.shapes.add_textbox(
            Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.3), Inches(0.7)
        )
        vp = vtb.text_frame.paragraphs[0]
        vp.text = value
        vp.font.size = Pt(26)
        vp.font.bold = True
        vp.font.color.rgb = accent_color

        # Label
        ltb = slide.shapes.add_textbox(
            Inches(left + 0.2), Inches(top + 0.85), Inches(width - 0.3), Inches(0.4)
        )
        lp = ltb.text_frame.paragraphs[0]
        lp.text = label
        lp.font.size = Pt(9)
        lp.font.bold = True
        lp.font.color.rgb = DARK_GRAY

    def add_note(slide, text):
        slide.notes_slide.notes_text_frame.text = text

    def add_image_safe(slide, path, left, top, width=None, height=None):
        """Add image if file exists, return True/False."""
        if os.path.exists(path):
            kwargs = {}
            if width: kwargs['width'] = Inches(width)
            if height: kwargs['height'] = Inches(height)
            slide.shapes.add_picture(path, Inches(left), Inches(top), **kwargs)
            return True
        return False

    def add_bullet_list(slide, items, left, top, width, height, size=11, color=DARK_GRAY, bullet_color=DELL_BLUE):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = "▸  " + item
            p.font.size = Pt(size)
            p.font.color.rgb = color
            p.space_after = Pt(6)

    # ======================================================================
    # SLIDE 1: TITLE
    # ======================================================================
    s1 = prs.slides.add_slide(blank)
    white_bg(s1)
    add_accent_bar(s1, DELL_BLUE, 0.08)

    # Left vertical accent strip
    lstrip = s1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5)
    )
    lstrip.fill.solid()
    lstrip.fill.fore_color.rgb = DELL_BLUE
    lstrip.line.fill.background()

    # Section tag
    add_section_tag(s1, "DELL CAMPUS RECRUITMENT 2026  •  PROBLEM STATEMENT 1", DELL_BLUE, 1.2, 1.2)

    # Main title
    t1 = add_title(s1, "PolicySphere™ AI", top=2.0, size=44, color=CHARCOAL, left=1.2)

    # Tagline
    add_subtitle(s1, "AI-Powered Campus Policy Discovery Assistant", top=3.0, size=20, color=ACCENT, left=1.2)

    # Description line
    add_body_text(s1, "Bridging the gap between informal student questions and formal university regulations\nusing Multi-Hypothesis HyDE retrieval, 3-layer security guardrails, and the Model Context Protocol.", 1.2, 3.7, 8.0, 1.0, size=13, color=DARK_GRAY)

    # Metric cards row
    metrics = [
        ("86.7%", "Hit@1 Precision", DELL_BLUE),
        ("93.3%", "Hit@3 Recall", TEAL),
        ("0.900", "MRR Score", INDIGO),
        ("0% Leakage", "Anti-Hallucination", RED_ACCENT),
    ]
    for i, (val, lbl, col) in enumerate(metrics):
        add_metric_card(s1, 1.2 + i * 2.85, 5.0, val, lbl, col, width=2.6, height=1.3)

    # Author info
    add_body_text(s1, "Hrishikesh Shetty  |  Ramaiah Institute of Technology (MSRIT)  |  B.E. Computer Science", 1.2, 6.55, 8.0, 0.4, size=12, color=DARK_GRAY, bold=True)

    add_note(s1, (
        "Good morning panel. I'm Hrishikesh Shetty from MSRIT. "
        "I'll present PolicySphere AI — an AI-powered campus policy discovery assistant "
        "that achieved 86.7% Hit@1 precision with zero hallucination across 20 test scenarios."
    ))

    # ======================================================================
    # SLIDE 2: THE PROBLEM
    # ======================================================================
    s2 = prs.slides.add_slide(blank)
    white_bg(s2)
    add_accent_bar(s2, DELL_BLUE)
    add_section_tag(s2, "SOLUTIONING  •  25%", DELL_BLUE)
    add_title(s2, "The Problem: Language Gap in Campus Policies")
    add_subtitle(s2, "Students ask in casual language, but policies are written in dense legal/academic prose")
    add_bottom_bar(s2)
    add_slide_number(s2, 2)

    # Left card - Student voice
    lcard = s2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.5)
    )
    lcard.fill.solid()
    lcard.fill.fore_color.rgb = RGBColor(254, 242, 242)  # Light red bg
    lcard.line.color.rgb = RGBColor(252, 165, 165)
    lcard.line.width = Pt(1)

    add_body_text(s2, "HOW STUDENTS ASK", 1.3, 2.35, 5.0, 0.3, size=10, color=RED_ACCENT, bold=True)

    student_qs = [
        '"My band has a gig next Friday, can I skip my lab?"',
        '"I got food poisoning and missed 5 days, what now?"',
        '"Can I pay a cash fee to fix my attendance?"',
        '"What time do I need to be back in the hostel?"',
        '"I got 15/50 in CIE, am I failed?"',
    ]
    add_bullet_list(s2, student_qs, 1.3, 2.8, 4.9, 3.5, size=12, color=CHARCOAL)

    # Right card - Policy voice
    rcard = s2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.9), Inches(2.2), Inches(5.4), Inches(4.5)
    )
    rcard.fill.solid()
    rcard.fill.fore_color.rgb = RGBColor(239, 246, 255)  # Light blue bg
    rcard.line.color.rgb = RGBColor(147, 197, 253)
    rcard.line.width = Pt(1)

    add_body_text(s2, "HOW POLICIES ARE WRITTEN", 7.2, 2.35, 5.0, 0.3, size=10, color=DELL_BLUE, bold=True)

    policy_text = [
        '"Attendance Deficit on Grounds of Medical Incapacitation..."',
        '"Academic Review Board exercises discretionary jurisdiction..."',
        '"Condonation petitions are admissible strictly under certified..."',
        '"Aggregate contact percentage between 65.0% and 74.9%..."',
        '"Mandatory submission deadline of forty-eight (48) hours..."',
    ]
    add_bullet_list(s2, policy_text, 7.2, 2.8, 4.9, 3.5, size=12, color=CHARCOAL)

    add_note(s2, (
        "The core problem: there's a huge language mismatch. Students use slang and casual phrasing. "
        "University handbooks use dense legal language. Simple keyword search fails here because "
        "the vocabulary is completely different. That's exactly what our system solves."
    ))

    # ======================================================================
    # SLIDE 3: SOLUTION OVERVIEW
    # ======================================================================
    s3 = prs.slides.add_slide(blank)
    white_bg(s3)
    add_accent_bar(s3, DELL_BLUE)
    add_section_tag(s3, "SOLUTIONING  •  25%", DELL_BLUE)
    add_title(s3, "Our Solution: PolicySphere™ AI")
    add_subtitle(s3, "An end-to-end AI pipeline that translates student language into policy-grade search queries")
    add_bottom_bar(s3)
    add_slide_number(s3, 3)

    # 3-step pipeline cards
    steps = [
        ("01", "UNDERSTAND", "HyDE Translation",
         "Student's casual question is transformed into\nformal academic language using Gemini AI.\nThis bridges the vocabulary gap between\nstudent speak and policy prose.",
         DELL_BLUE),
        ("02", "RETRIEVE", "Multi-Hypothesis RAG",
         "Generate 3 different hypothesis documents,\neach offering a different interpretation.\nUse Reciprocal Rank Fusion to combine\nresults for maximum recall.",
         TEAL),
        ("03", "VERIFY", "3-Layer Guardrails",
         "Layer 1: Block gibberish & injection attacks.\nLayer 2: Cosine threshold filters irrelevant results.\nLayer 3: LLM verifies the answer actually\nmatches the student's question.",
         RED_ACCENT),
    ]
    for i, (num, phase, title, desc, col) in enumerate(steps):
        left = 1.0 + i * 3.9
        # Card
        card = s3.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(2.3), Inches(3.5), Inches(4.2)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = OFF_WHITE
        card.line.color.rgb = LIGHT_GRAY
        card.line.width = Pt(1)

        # Number circle
        circle = s3.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(left + 0.2), Inches(2.5), Inches(0.55), Inches(0.55)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = col
        circle.line.fill.background()
        ctf = circle.text_frame
        ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
        cp = ctf.paragraphs[0]
        cp.text = num
        cp.font.size = Pt(16)
        cp.font.bold = True
        cp.font.color.rgb = WHITE
        cp.alignment = PP_ALIGN.CENTER

        # Phase name
        add_body_text(s3, phase, left + 0.9, 2.55, 2.3, 0.3, size=10, color=col, bold=True)

        # Title
        add_body_text(s3, title, left + 0.3, 3.2, 2.9, 0.4, size=16, color=CHARCOAL, bold=True)

        # Description
        add_body_text(s3, desc, left + 0.3, 3.7, 2.9, 2.5, size=11, color=DARK_GRAY)

    add_note(s3, (
        "Our pipeline has three stages. First, we use Gemini AI to translate the casual student query "
        "into formal academic language — this is called HyDE. Second, we generate 3 different hypotheses "
        "and retrieve policies using each, then combine them with Reciprocal Rank Fusion. Third, we verify "
        "the result hasn't hallucinated through a 3-layer guardrail system."
    ))

    # ======================================================================
    # SLIDE 4: ARCHITECTURE
    # ======================================================================
    s4 = prs.slides.add_slide(blank)
    white_bg(s4)
    add_accent_bar(s4, DELL_BLUE)
    add_section_tag(s4, "TECHNOLOGY  •  25%", TEAL)
    add_title(s4, "System Architecture")
    add_subtitle(s4, "Full pipeline from student query to verified policy response")
    add_bottom_bar(s4)
    add_slide_number(s4, 4)

    # Architecture flow - horizontal pipeline
    stages = [
        ("Student Query", "Natural language\ninput", RGBColor(239, 246, 255), DELL_BLUE),
        ("Input Guard", "Regex + Entropy\n+ Injection Block", RGBColor(254, 242, 242), RED_ACCENT),
        ("HyDE Engine", "Gemini 3.1\nFlash Lite", RGBColor(240, 253, 244), TEAL),
        ("Vector Index", "TF-IDF + Cosine\nScikit-Learn", RGBColor(245, 243, 255), INDIGO),
        ("RRF Fusion", "Multi-Hypothesis\nRank Merge", RGBColor(255, 251, 235), AMBER),
        ("Cosine Gate", "Threshold ≥ 0.12\nRelevance Filter", RGBColor(254, 242, 242), RED_ACCENT),
        ("LLM Verify", "Entity-Level\nTopic Check", RGBColor(240, 253, 244), TEAL),
        ("Response", "Grounded Answer\n+ Excerpts", RGBColor(239, 246, 255), DELL_BLUE),
    ]

    for i, (label, desc, bg_col, text_col) in enumerate(stages):
        left = 0.4 + i * 1.58
        # Box
        box = s4.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(2.5), Inches(1.4), Inches(1.8)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = bg_col
        box.line.color.rgb = text_col
        box.line.width = Pt(1.2)

        # Label
        add_body_text(s4, label, left + 0.1, 2.6, 1.2, 0.4, size=10, color=text_col, bold=True)
        # Description
        add_body_text(s4, desc, left + 0.1, 3.1, 1.2, 0.8, size=9, color=DARK_GRAY)

        # Arrow between boxes
        if i < len(stages) - 1:
            arr_tb = s4.shapes.add_textbox(
                Inches(left + 1.4), Inches(3.1), Inches(0.2), Inches(0.4)
            )
            ap = arr_tb.text_frame.paragraphs[0]
            ap.text = "→"
            ap.font.size = Pt(16)
            ap.font.color.rgb = MID_GRAY
            ap.font.bold = True

    # Bottom section: Tech components
    components = [
        ("Frontend", "React SPA\nSingle HTML, Dark/Light Mode", DELL_BLUE),
        ("Backend", "FastAPI + Uvicorn\nAsync REST API", TEAL),
        ("AI Engine", "Google Gemini 3.1 Flash Lite\nwith Model Fallback Chain", INDIGO),
        ("Protocol", "Model Context Protocol (MCP)\n3 Tools, JSON-RPC 2.0", AMBER),
        ("Deployment", "Docker + Docker Compose\nOne-Command Launch", DARK_GRAY),
    ]
    for i, (name, desc, col) in enumerate(components):
        left = 0.8 + i * 2.5
        add_body_text(s4, name, left, 4.8, 2.2, 0.3, size=12, color=col, bold=True)
        add_body_text(s4, desc, left, 5.15, 2.2, 0.6, size=10, color=DARK_GRAY)

    add_note(s4, (
        "The architecture flows left to right. Student query enters, goes through input guardrails "
        "to block attacks, then HyDE translates it to formal language, TF-IDF vector search retrieves "
        "candidate policies, Reciprocal Rank Fusion merges multi-hypothesis results, cosine threshold "
        "filters irrelevant results, and finally LLM verification ensures entity-level relevance."
    ))

    # ======================================================================
    # SLIDE 5: TECH STACK DEEP DIVE
    # ======================================================================
    s5 = prs.slides.add_slide(blank)
    white_bg(s5)
    add_accent_bar(s5, DELL_BLUE)
    add_section_tag(s5, "TECHNOLOGY  •  25%", TEAL)
    add_title(s5, "Technology Stack & Design Decisions")
    add_subtitle(s5, "Every choice optimized for accuracy, speed, and security")
    add_bottom_bar(s5)
    add_slide_number(s5, 5)

    # Tech stack table - 2 columns
    left_items = [
        ("Google Gemini 3.1 Flash Lite", "Primary LLM for HyDE hypothesis generation and answer verification.\nFallback chain: 3.1 → 3.5 → 3.8 Flash for resilience.", DELL_BLUE),
        ("Scikit-Learn TF-IDF", "Sublinear TF-IDF vectorizer with cosine similarity. Fast (3.8ms)\nand runs 100% locally — no cloud vector DB dependency.", TEAL),
        ("Model Context Protocol (MCP)", "Standardized tool interface enabling any MCP-compatible\nLLM client to use our policy search as a native tool.", INDIGO),
    ]
    right_items = [
        ("FastAPI + Uvicorn", "Async Python backend with automatic OpenAPI documentation.\nType-safe request/response with Pydantic models.", DELL_BLUE),
        ("React SPA (Single HTML)", "Entire frontend in one file. Dark/light mode, evaluation\npresets, benchmark tab. Zero build step needed.", TEAL),
        ("Docker + Docker Compose", "Production-ready containerization. One command to deploy.\n.env-based configuration. Health check endpoint.", DARK_GRAY),
    ]

    for i, (name, desc, col) in enumerate(left_items):
        top = 2.3 + i * 1.55
        add_body_text(s5, name, 1.0, top, 5.0, 0.3, size=14, color=col, bold=True)
        add_body_text(s5, desc, 1.0, top + 0.35, 5.5, 0.8, size=11, color=DARK_GRAY)
        # Separator
        if i < len(left_items) - 1:
            sep = s5.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(top + 1.3), Inches(5.5), Inches(0.01)
            )
            sep.fill.solid()
            sep.fill.fore_color.rgb = LIGHT_GRAY
            sep.line.fill.background()

    for i, (name, desc, col) in enumerate(right_items):
        top = 2.3 + i * 1.55
        add_body_text(s5, name, 7.2, top, 5.0, 0.3, size=14, color=col, bold=True)
        add_body_text(s5, desc, 7.2, top + 0.35, 5.5, 0.8, size=11, color=DARK_GRAY)
        if i < len(right_items) - 1:
            sep = s5.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(top + 1.3), Inches(5.5), Inches(0.01)
            )
            sep.fill.solid()
            sep.fill.fore_color.rgb = LIGHT_GRAY
            sep.line.fill.background()

    # Center divider
    cdiv = s5.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(2.3), Inches(0.015), Inches(4.5)
    )
    cdiv.fill.solid()
    cdiv.fill.fore_color.rgb = LIGHT_GRAY
    cdiv.line.fill.background()

    add_note(s5, (
        "I chose Gemini 3.1 Flash Lite for speed — it's fast enough for real-time HyDE generation. "
        "Scikit-learn TF-IDF gives us 3.8 millisecond search with no cloud dependency. "
        "MCP makes our system pluggable into any AI assistant. FastAPI is async and type-safe. "
        "The React frontend is a single HTML file — no build step, easy to deploy."
    ))

    # ======================================================================
    # SLIDE 6: LIVE PRODUCT DEMO - Main UI
    # ======================================================================
    s6 = prs.slides.add_slide(blank)
    white_bg(s6)
    add_accent_bar(s6, DELL_BLUE)
    add_section_tag(s6, "WORKING PRODUCT", EMERALD)
    add_title(s6, "Live Product: PolicySphere™ AI Interface")
    add_subtitle(s6, "Full-featured web application with evaluation presets, mode switching, and dark/light theme")
    add_bottom_bar(s6)
    add_slide_number(s6, 6)

    # Embed screenshot with shadow-like border
    screenshot_path = os.path.join(SCREENSHOT_DIR, "01_assistant_main.png")
    shadow = s6.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.8), Inches(2.05), Inches(9.7), Inches(4.75)
    )
    shadow.fill.solid()
    shadow.fill.fore_color.rgb = LIGHT_GRAY
    shadow.line.color.rgb = MID_GRAY
    shadow.line.width = Pt(1)

    add_image_safe(s6, screenshot_path, 1.9, 2.15, width=9.5, height=4.5)

    add_note(s6, (
        "Here's our live product running at localhost:8000. You can see the search interface "
        "with mode switching between Raw, Single HyDE, and Multi-HyDE. The evaluation presets "
        "at the bottom let you quickly test different scenarios. The interface has both dark and light mode."
    ))

    # ======================================================================
    # SLIDE 7: GUARDRAILS & SECURITY
    # ======================================================================
    s7 = prs.slides.add_slide(blank)
    white_bg(s7)
    add_accent_bar(s7, RED_ACCENT)
    add_section_tag(s7, "REASONING  •  20%", RED_ACCENT)
    add_title(s7, "Security: 3-Layer Guardrail System")
    add_subtitle(s7, "100% injection block rate, 100% unanswerable refusal rate, 0% fake policy leakage")
    add_bottom_bar(s7)
    add_slide_number(s7, 7)

    # Left side: guardrail explanation
    layers = [
        ("Layer 1: Input Sanitization", "Regex pattern matching for prompt injection attempts.\nEntropy-based gibberish detection. Blocks malformed input\nbefore it reaches the AI pipeline.", RED_ACCENT),
        ("Layer 2: Relevance Threshold", "Cosine similarity must be ≥ 0.12 to proceed.\nPrevents low-confidence results from being shown.\nActs as a mathematical safety net.", AMBER),
        ("Layer 3: LLM Verification", "Gemini verifies entity-level topic relevance.\nE.g., 'PS5 in hostel' won't return curfew rules.\nEnsures answer actually matches the question.", TEAL),
    ]
    for i, (name, desc, col) in enumerate(layers):
        top = 2.2 + i * 1.5
        add_body_text(s7, name, 1.0, top, 4.5, 0.3, size=13, color=col, bold=True)
        add_body_text(s7, desc, 1.0, top + 0.32, 4.8, 0.9, size=10, color=DARK_GRAY)

    # Right side: guardrail screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, "03_guardrail_intercept.png")
    shadow = s7.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.3), Inches(2.05), Inches(6.3), Inches(4.75)
    )
    shadow.fill.solid()
    shadow.fill.fore_color.rgb = LIGHT_GRAY
    shadow.line.color.rgb = MID_GRAY
    shadow.line.width = Pt(1)

    add_image_safe(s7, screenshot_path, 6.4, 2.15, width=6.1, height=4.5)

    add_note(s7, (
        "Security was a top priority. Layer 1 catches injection attacks and gibberish input using regex "
        "and entropy detection. Layer 2 applies a cosine similarity threshold — if the best match is below "
        "0.12, we refuse to answer rather than guess. Layer 3 uses Gemini to verify that the answer's topic "
        "actually matches what the student asked about. This screenshot shows a bribery attempt being blocked."
    ))

    # ======================================================================
    # SLIDE 8: BENCHMARK RESULTS
    # ======================================================================
    s8 = prs.slides.add_slide(blank)
    white_bg(s8)
    add_accent_bar(s8, TEAL)
    add_section_tag(s8, "REASONING  •  20%", TEAL)
    add_title(s8, "Audited Benchmark Results")
    add_subtitle(s8, "20 test scenarios: 15 standard queries, 3 unanswerable, 2 injection attacks")
    add_bottom_bar(s8)
    add_slide_number(s8, 8)

    # Metric cards - top row
    bench_metrics = [
        ("66.7%", "Raw Hit@1", MID_GRAY),
        ("86.7%", "Single HyDE Hit@1", DELL_BLUE),
        ("93.3%", "Multi-HyDE Hit@3", TEAL),
        ("0.900", "Best MRR", INDIGO),
        ("5.36 ms", "Raw Latency", DARK_GRAY),
    ]
    for i, (val, lbl, col) in enumerate(bench_metrics):
        add_metric_card(s8, 0.8 + i * 2.45, 2.2, val, lbl, col, width=2.2, height=1.2)

    # Bottom: Screenshot of benchmark tab
    screenshot_path = os.path.join(SCREENSHOT_DIR, "04_live_benchmark_tab.png")
    shadow = s8.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.3), Inches(3.7), Inches(10.7), Inches(3.15)
    )
    shadow.fill.solid()
    shadow.fill.fore_color.rgb = LIGHT_GRAY
    shadow.line.color.rgb = MID_GRAY
    shadow.line.width = Pt(1)

    add_image_safe(s8, screenshot_path, 1.4, 3.8, width=10.5, height=2.9)

    add_note(s8, (
        "Let me walk you through the benchmark numbers. Raw keyword search only gets 66.7% Hit@1. "
        "Single HyDE jumps it to 86.7% — that's a 20% improvement just from translating the query. "
        "Multi-HyDE with RRF gets 93.3% Hit@3 and an MRR of 0.900. All 3 unanswerable queries were "
        "correctly refused, and both injection attacks were blocked. Zero fake policy leakage."
    ))

    # ======================================================================
    # SLIDE 9: INNOVATION & MCP
    # ======================================================================
    s9 = prs.slides.add_slide(blank)
    white_bg(s9)
    add_accent_bar(s9, INDIGO)
    add_section_tag(s9, "INNOVATION  •  15%", INDIGO)
    add_title(s9, "What Makes This Different")
    add_subtitle(s9, "Key innovations that go beyond a basic RAG chatbot")
    add_bottom_bar(s9)
    add_slide_number(s9, 9)

    innovations = [
        ("Multi-Hypothesis HyDE with RRF",
         "Instead of one translation, we generate 3 different hypotheses — each interpreting the query differently.\nReciprocal Rank Fusion combines their results, boosting recall from 73.3% to 93.3%.",
         DELL_BLUE),
        ("Model Context Protocol (MCP) Integration",
         "Our policy search is exposed as a standardized MCP tool. Any MCP-compatible AI assistant\n(Claude, ChatGPT, Gemini) can use PolicySphere as a native plugin — no custom API code needed.",
         INDIGO),
        ("Entity-Level Topic Verification",
         "The LLM doesn't just check 'is this relevant?' — it verifies that the specific entities\nin the question match the entities in the answer. 'PS5 in hostel' won't return curfew rules.",
         TEAL),
        ("Adversarial Robustness Testing",
         "We planted 3 fake policies in the corpus and verified the system never retrieves them.\n2 injection attacks (bribery, prompt injection) are blocked with 100% success rate.",
         RED_ACCENT),
    ]

    for i, (title, desc, col) in enumerate(innovations):
        top = 2.2 + i * 1.25
        # Accent dot
        dot = s9.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(1.0), Inches(top + 0.05), Inches(0.15), Inches(0.15)
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = col
        dot.line.fill.background()

        add_body_text(s9, title, 1.4, top, 10.5, 0.3, size=14, color=col, bold=True)
        add_body_text(s9, desc, 1.4, top + 0.32, 10.5, 0.7, size=11, color=DARK_GRAY)

    add_note(s9, (
        "Four key innovations. First, Multi-Hypothesis HyDE — generating 3 interpretations instead of 1 "
        "and fusing them with RRF boosted our recall by 20 percentage points. Second, MCP makes us "
        "pluggable into any AI ecosystem. Third, entity-level verification prevents the common RAG problem "
        "of returning topically adjacent but wrong answers. Fourth, we proactively test with adversarial data."
    ))

    # ======================================================================
    # SLIDE 10: CLOSING
    # ======================================================================
    s10 = prs.slides.add_slide(blank)
    white_bg(s10)
    add_accent_bar(s10, DELL_BLUE, 0.08)

    # Left vertical accent strip
    lstrip = s10.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5)
    )
    lstrip.fill.solid()
    lstrip.fill.fore_color.rgb = DELL_BLUE
    lstrip.line.fill.background()

    add_title(s10, "Thank You", top=1.5, size=40, color=CHARCOAL, left=1.2)
    add_subtitle(s10, "PolicySphere™ AI — Campus Policy Discovery, Reinvented", top=2.3, size=18, color=ACCENT, left=1.2)

    # Summary card
    summary_card = s10.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.2), Inches(3.2), Inches(6.0), Inches(3.2)
    )
    summary_card.fill.solid()
    summary_card.fill.fore_color.rgb = OFF_WHITE
    summary_card.line.color.rgb = LIGHT_GRAY
    summary_card.line.width = Pt(1)

    summary_items = [
        "86.7% Hit@1 Precision with Single HyDE",
        "93.3% Hit@3 Recall with Multi-Hypothesis RRF",
        "0% Hallucination — Zero Fake Policy Leakage",
        "100% Injection Block Rate (2/2 attacks stopped)",
        "100% Unanswerable Refusal Rate (3/3 correctly refused)",
        "3.8ms Average Search Latency (local vector index)",
        "MCP-Ready: Pluggable into Any AI Assistant",
    ]
    add_bullet_list(s10, summary_items, 1.5, 3.35, 5.4, 2.8, size=12, color=CHARCOAL)

    # Contact info card
    contact_card = s10.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(7.8), Inches(3.2), Inches(4.5), Inches(3.2)
    )
    contact_card.fill.solid()
    contact_card.fill.fore_color.rgb = CHARCOAL
    contact_card.line.fill.background()

    add_body_text(s10, "CANDIDATE", 8.1, 3.4, 4.0, 0.3, size=10, color=MID_GRAY, bold=True)
    add_body_text(s10, "Hrishikesh Shetty", 8.1, 3.7, 4.0, 0.4, size=18, color=WHITE, bold=True)
    add_body_text(s10, "B.E. Computer Science\nRamaiah Institute of Technology (MSRIT)", 8.1, 4.15, 4.0, 0.6, size=12, color=MID_GRAY)
    add_body_text(s10, "PROBLEM STATEMENT", 8.1, 4.9, 4.0, 0.3, size=10, color=MID_GRAY, bold=True)
    add_body_text(s10, "PS-1: AI-Powered Campus\nPolicy Discovery Assistant", 8.1, 5.2, 4.0, 0.6, size=14, color=WHITE, bold=True)

    add_slide_number(s10, 10)

    add_note(s10, (
        "To summarize: PolicySphere AI delivers 86.7% precision, 93.3% recall, zero hallucination, "
        "and complete attack resistance — all with sub-4ms search speed. The MCP integration makes it "
        "future-proof and pluggable. Thank you for your time. I'm happy to take your questions."
    ))

    # ── Save ──
    prs.save(OUTPUT)
    print(f"Saved: {OUTPUT} ({os.path.getsize(OUTPUT):,} bytes)")
    print(f"Slides: {len(prs.slides)}")

if __name__ == "__main__":
    build_deck()

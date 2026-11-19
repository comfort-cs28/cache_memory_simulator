"""Generate the Cache Memory Simulator PowerPoint presentation."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

# Brand colors (navy + gold academic theme)
NAVY = RGBColor(0x0B, 0x1F, 0x3A)
NAVY_MID = RGBColor(0x14, 0x3D, 0x66)
GOLD = RGBColor(0xC4, 0xA3, 0x5A)
CREAM = RGBColor(0xF7, 0xF4, 0xEF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x4A, 0x55, 0x68)
ACCENT_LINE = RGBColor(0xC4, 0xA3, 0xA5)


def set_run(run, text, size_pt, bold=False, color=DARK_TEXT, font_name="Calibri"):
    run.text = text
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name


def add_textbox(slide, left, top, width, height, text, size_pt, bold=False,
                color=DARK_TEXT, align=PP_ALIGN.LEFT, font_name="Calibri"):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    set_run(run, text, size_pt, bold, color, font_name)
    return box


def add_bullets(slide, left, top, width, height, items, size_pt=18, color=DARK_TEXT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for index, item in enumerate(items):
        if index == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.level = 0
        p.space_after = Pt(8)
        run = p.add_run()
        set_run(run, f"•  {item}", size_pt, False, color)
    return box


def add_bg(slide, color=CREAM):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    # Send to back by z-order is limited; draw first so content sits on top
    return shape


def add_top_bar(slide):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.fill.background()
    return bar


def add_footer(slide, page_num, total=14):
    add_textbox(
        slide, Inches(0.5), Inches(7.05), Inches(10), Inches(0.3),
        "Cache Memory Simulator  |  Computer Architecture",
        11, False, MUTED
    )
    add_textbox(
        slide, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
        f"{page_num} / {total}",
        11, False, MUTED, PP_ALIGN.RIGHT
    )


def add_section_title(slide, title, subtitle=None):
    add_textbox(
        slide, Inches(0.6), Inches(0.4), Inches(12), Inches(0.6),
        title, 32, True, NAVY, font_name="Georgia"
    )
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.05), Inches(1.8), Inches(0.06)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = GOLD
    line.line.fill.background()
    if subtitle:
        add_textbox(
            slide, Inches(0.6), Inches(1.2), Inches(12), Inches(0.4),
            subtitle, 15, False, MUTED
        )


def blank_slide(prs):
    blank = prs.slide_layouts[6]  # blank
    slide = prs.slides.add_slide(blank)
    add_bg(slide)
    add_top_bar(slide)
    return slide


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    total = 14

    # ----- 1. Title -----
    slide = blank_slide(prs)
    panel = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    panel.fill.solid()
    panel.fill.fore_color.rgb = NAVY
    panel.line.fill.background()
    gold_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(2.55), Inches(13.333), Inches(0.08)
    )
    gold_bar.fill.solid()
    gold_bar.fill.fore_color.rgb = GOLD
    gold_bar.line.fill.background()
    add_textbox(
        slide, Inches(0.8), Inches(1.5), Inches(11.5), Inches(1.0),
        "A Configurable Cache Memory Simulator",
        36, True, WHITE, PP_ALIGN.CENTER, "Georgia"
    )
    add_textbox(
        slide, Inches(0.8), Inches(2.8), Inches(11.5), Inches(0.5),
        "Using Python",
        24, False, GOLD, PP_ALIGN.CENTER, "Georgia"
    )
    add_textbox(
        slide, Inches(0.8), Inches(3.7), Inches(11.5), Inches(0.4),
        "Computer Architecture  |  Level 300 Project",
        16, False, WHITE, PP_ALIGN.CENTER
    )
    add_textbox(
        slide, Inches(0.8), Inches(4.5), Inches(11.5), Inches(0.8),
        "Comfort Akorfa Yikpa  (PU/CS/2024/001)\nEnock Yaw Sie  (PU/CS/2024/005)",
        16, False, CREAM, PP_ALIGN.CENTER
    )
    add_textbox(
        slide, Inches(0.8), Inches(6.4), Inches(11.5), Inches(0.4),
        "Ghana  |  2026",
        13, False, GOLD, PP_ALIGN.CENTER
    )

    # ----- 2. Outline -----
    slide = blank_slide(prs)
    add_section_title(slide, "Presentation Outline")
    add_bullets(slide, Inches(0.8), Inches(1.6), Inches(5.5), Inches(5), [
        "Introduction to cache memory",
        "Problem statement",
        "Aim and objectives",
        "Scope of the project",
        "System design and modules",
        "Address decoding",
        "Direct-mapped vs set-associative",
    ], 18)
    add_bullets(slide, Inches(7.0), Inches(1.6), Inches(5.5), Inches(5), [
        "LRU replacement policy",
        "Tools and technologies",
        "How to run the simulator",
        "Sample results and comparison",
        "Significance of the project",
        "Conclusion",
        "Questions and answers",
    ], 18)
    add_footer(slide, 2, total)

    # ----- 3. Introduction -----
    slide = blank_slide(prs)
    add_section_title(slide, "Introduction", "Why cache memory matters")
    add_bullets(slide, Inches(0.8), Inches(1.7), Inches(11.5), Inches(4.8), [
        "A cache is a small, fast memory between the CPU and main memory.",
        "The CPU is much faster than main memory, so waiting for data hurts performance.",
        "The mapping policy decides where a memory block may be placed in the cache.",
        "Mapping policy strongly affects the hit rate — how often data is found in cache.",
        "This project builds a command-line Python simulator for direct-mapped and N-way set-associative caches.",
        "It reads hexadecimal address traces and shows hits, misses, and hit rate for each design.",
    ], 18)
    add_footer(slide, 3, total)

    # ----- 4. Problem Statement -----
    slide = blank_slide(prs)
    add_section_title(slide, "Problem Statement")
    add_bullets(slide, Inches(0.8), Inches(1.6), Inches(11.5), Inches(2.5), [
        "Cache behavior happens inside hardware and cannot be watched directly.",
        "Students usually learn tags, index bits, and offsets on paper.",
        "Working through long address lists by hand is slow and easy to get wrong.",
    ], 18)
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(11.7), Inches(2.4)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = NAVY
    box.line.fill.background()
    add_textbox(
        slide, Inches(1.1), Inches(4.2), Inches(11), Inches(0.4),
        "There is a need for a simple tool that:",
        16, True, GOLD
    )
    add_textbox(
        slide, Inches(1.1), Inches(4.7), Inches(11), Inches(1.5),
        "• Accepts hexadecimal addresses\n"
        "• Splits each address into tag, index, and offset correctly\n"
        "• Simulates direct-mapped and set-associative caches\n"
        "• Reports hits, misses, and hit rate for fair comparison",
        15, False, WHITE
    )
    add_footer(slide, 4, total)

    # ----- 5. Aim & Objectives -----
    slide = blank_slide(prs)
    add_section_title(slide, "Aim and Objectives")
    add_textbox(
        slide, Inches(0.8), Inches(1.5), Inches(11.5), Inches(0.8),
        "Aim: Build a configurable Python cache simulator that compares hit and miss "
        "ratios for direct-mapped and set-associative policies using memory traces.",
        16, False, DARK_TEXT
    )
    add_textbox(
        slide, Inches(0.8), Inches(2.4), Inches(11.5), Inches(0.4),
        "Objectives",
        18, True, NAVY, font_name="Georgia"
    )
    add_bullets(slide, Inches(0.8), Inches(2.9), Inches(11.5), Inches(3.8), [
        "Read memory addresses in hexadecimal from a text file.",
        "Split each address into tag, index, and block offset using bitwise operations.",
        "Simulate a direct-mapped cache.",
        "Simulate an N-way set-associative cache with a replacement policy (LRU).",
        "Allow cache size, block size, and number of ways to be configured.",
        "Output total hits, misses, and hit rate for each configuration.",
    ], 16)
    add_footer(slide, 5, total)

    # ----- 6. Scope -----
    slide = blank_slide(prs)
    add_section_title(slide, "Scope of the Project")
    left = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.6), Inches(5.8), Inches(4.8)
    )
    left.fill.solid()
    left.fill.fore_color.rgb = WHITE
    left.line.color.rgb = GOLD
    right = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.8), Inches(4.8)
    )
    right.fill.solid()
    right.fill.fore_color.rgb = WHITE
    right.line.color.rgb = MUTED
    add_textbox(slide, Inches(0.9), Inches(1.8), Inches(5.2), Inches(0.4),
                "Included", 20, True, NAVY, font_name="Georgia")
    add_bullets(slide, Inches(0.9), Inches(2.4), Inches(5.2), Inches(3.6), [
        "Python command-line application",
        "Direct-mapped and N-way caches",
        "LRU replacement policy",
        "Hexadecimal address trace files",
        "Hits, misses, and hit rate report",
        "All accesses treated as reads",
    ], 15)
    add_textbox(slide, Inches(7.2), Inches(1.8), Inches(5.2), Inches(0.4),
                "Not Included", 20, True, NAVY, font_name="Georgia")
    add_bullets(slide, Inches(7.2), Inches(2.4), Inches(5.2), Inches(3.6), [
        "Graphical user interface",
        "Multi-level caches",
        "Write policies",
        "Timing or power models",
        "Hardware design / FPGA work",
    ], 15)
    add_footer(slide, 6, total)

    # ----- 7. System Design -----
    slide = blank_slide(prs)
    add_section_title(slide, "System Design", "Main modules of the simulator")
    modules = [
        ("Input Module", "Reads hex addresses from a text file and validates each line."),
        ("Address Decoder", "Splits address into tag, index, and offset with bit shifts/masks."),
        ("Cache Engine", "Direct-mapped (ways=1) or N-way set-associative with LRU."),
        ("Configuration", "Cache size, block size, and ways via command-line options."),
        ("Statistics", "Reports accesses, hits, misses, and hit rate percentage."),
    ]
    y = 1.55
    for title, desc in modules:
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(y), Inches(11.9), Inches(0.85)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(0xD8, 0xD2, 0xC8)
        accent = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(y), Inches(0.12), Inches(0.85)
        )
        accent.fill.solid()
        accent.fill.fore_color.rgb = GOLD
        accent.line.fill.background()
        add_textbox(slide, Inches(1.1), Inches(y + 0.08), Inches(11), Inches(0.35),
                    title, 16, True, NAVY)
        add_textbox(slide, Inches(1.1), Inches(y + 0.4), Inches(11), Inches(0.35),
                    desc, 13, False, MUTED)
        y += 0.95
    add_footer(slide, 7, total)

    # ----- 8. Address Decoding -----
    slide = blank_slide(prs)
    add_section_title(slide, "Address Decoding", "How each memory address is split")
    add_bullets(slide, Inches(0.8), Inches(1.55), Inches(11.5), Inches(2.2), [
        "Offset bits = log₂(block size)",
        "Index bits = log₂(number of sets)",
        "Tag = remaining upper bits of the address",
        "Number of sets = cache size ÷ (block size × ways)",
    ], 17)
    # Bit field visual
    fields = [
        (0.8, "TAG", NAVY, 4.5),
        (5.5, "INDEX", NAVY_MID, 3.5),
        (9.2, "OFFSET", GOLD, 3.3),
    ]
    for left, label, color, width in fields:
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(4.0), Inches(width), Inches(1.3)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        add_textbox(
            slide, Inches(left), Inches(4.35), Inches(width), Inches(0.6),
            label, 22, True, WHITE, PP_ALIGN.CENTER
        )
    add_textbox(
        slide, Inches(0.8), Inches(5.6), Inches(11.5), Inches(0.6),
        "Bitwise shifts and masks separate the three fields for every address in the trace.",
        14, False, MUTED, PP_ALIGN.CENTER
    )
    add_footer(slide, 8, total)

    # ----- 9. Direct-Mapped -----
    slide = blank_slide(prs)
    add_section_title(slide, "Direct-Mapped Cache", "One way per set (--ways 1)")
    add_bullets(slide, Inches(0.8), Inches(1.6), Inches(11.5), Inches(4.5), [
        "Each memory block maps to exactly one cache line (set).",
        "The stored tag is compared with the address tag to decide hit or miss.",
        "On a miss, the new block replaces the old block in that line.",
        "Simple and fast to implement, but conflict misses are more common.",
        "In our simulator, choosing --ways 1 selects this policy using the same code path.",
    ], 18)
    note = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.2)
    )
    note.fill.solid()
    note.fill.fore_color.rgb = NAVY
    note.line.fill.background()
    add_textbox(
        slide, Inches(1.1), Inches(5.55), Inches(11), Inches(0.7),
        "Example: python main.py -t traces/hand_verified.txt -c 64 -b 16 -w 1 -v",
        15, False, WHITE
    )
    add_footer(slide, 9, total)

    # ----- 10. Set-Associative + LRU -----
    slide = blank_slide(prs)
    add_section_title(slide, "N-Way Set-Associative Cache", "With Least Recently Used (LRU) replacement")
    add_bullets(slide, Inches(0.8), Inches(1.6), Inches(11.5), Inches(4.8), [
        "Each memory block maps to one set, but can sit in any of the N ways in that set.",
        "All tags in the set are checked to decide a hit or a miss.",
        "On a hit, the block is marked as most recently used.",
        "On a miss with a full set, the least recently used block is replaced.",
        "Higher associativity usually reduces conflict misses and can improve hit rate.",
        "Example: --ways 2, --ways 4, or higher for more associativity.",
    ], 17)
    add_footer(slide, 10, total)

    # ----- 11. Tools -----
    slide = blank_slide(prs)
    add_section_title(slide, "Tools and Technologies")
    tools = [
        ("Language", "Python 3"),
        ("Libraries", "Standard library only\n(argparse, math, collections)"),
        ("Interface", "Command-line (CLI)"),
        ("Input", "Plain-text hex address traces"),
        ("IDE", "VS Code / PyCharm"),
        ("OS", "Windows, Linux, or macOS"),
    ]
    positions = [
        (0.7, 1.7), (4.7, 1.7), (8.7, 1.7),
        (0.7, 4.2), (4.7, 4.2), (8.7, 4.2),
    ]
    for (left, top), (title, body) in zip(positions, tools):
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(3.7), Inches(2.0)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(0xD8, 0xD2, 0xC8)
        add_textbox(slide, Inches(left + 0.25), Inches(top + 0.3), Inches(3.2), Inches(0.4),
                    title, 15, True, GOLD)
        add_textbox(slide, Inches(left + 0.25), Inches(top + 0.85), Inches(3.2), Inches(0.9),
                    body, 15, False, NAVY)
    add_footer(slide, 11, total)

    # ----- 12. How to Run -----
    slide = blank_slide(prs)
    add_section_title(slide, "How to Run the Simulator")
    add_bullets(slide, Inches(0.8), Inches(1.5), Inches(11.5), Inches(2.0), [
        "Open a terminal in the project folder.",
        "Provide a trace file and configuration options.",
        "Use --verbose to print tag, index, offset, and HIT/MISS for each access.",
    ], 16)
    cmds = [
        "Direct-mapped:\npython main.py -t traces/sample_addresses.txt -c 1024 -b 16 -w 1",
        "4-way set-associative:\npython main.py -t traces/sample_addresses.txt -c 1024 -b 16 -w 4",
        "Verbose hand check:\npython main.py -t traces/hand_verified.txt -c 64 -b 16 -w 1 -v",
    ]
    y = 3.5
    for cmd in cmds:
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(11.7), Inches(0.95)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = NAVY
        box.line.fill.background()
        add_textbox(slide, Inches(1.05), Inches(y + 0.12), Inches(11.2), Inches(0.75),
                    cmd, 13, False, WHITE)
        y += 1.05
    add_footer(slide, 12, total)

    # ----- 13. Results -----
    slide = blank_slide(prs)
    add_section_title(slide, "Sample Results", "Same trace, different associativity (64 B cache, 16 B blocks)")
    headers = ["Configuration", "Accesses", "Hits", "Misses", "Hit Rate"]
    rows = [
        ["Direct-mapped (1-way)", "12", "0", "12", "0.00%"],
        ["2-way set-associative", "12", "0", "12", "0.00%"],
        ["4-way set-associative", "12", "8", "4", "66.67%"],
    ]
    # Header row
    x_positions = [0.7, 5.2, 7.2, 9.0, 10.8]
    widths = [4.3, 1.8, 1.6, 1.6, 1.8]
    for x, w, h in zip(x_positions, widths, headers):
        cell = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.7), Inches(w), Inches(0.6)
        )
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.line.color.rgb = NAVY
        add_textbox(slide, Inches(x), Inches(1.82), Inches(w), Inches(0.4),
                    h, 13, True, WHITE, PP_ALIGN.CENTER)
    for r_index, row in enumerate(rows):
        y = 2.3 + r_index * 0.65
        bg = WHITE if r_index % 2 == 0 else RGBColor(0xEE, 0xE8, 0xDF)
        for x, w, value in zip(x_positions, widths, row):
            cell = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.65)
            )
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.line.color.rgb = RGBColor(0xD8, 0xD2, 0xC8)
            add_textbox(slide, Inches(x), Inches(y + 0.15), Inches(w), Inches(0.4),
                        value, 14, False, DARK_TEXT, PP_ALIGN.CENTER)
    add_textbox(
        slide, Inches(0.8), Inches(4.6), Inches(11.5), Inches(1.5),
        "Observation: On conflict-heavy traces, higher associativity can raise hit rate "
        "significantly (here from 0% to 66.67%).\n\n"
        "Hit rate = (Hits ÷ Total accesses) × 100%",
        15, False, MUTED
    )
    add_footer(slide, 13, total)

    # ----- 14. Conclusion / Q&A -----
    slide = blank_slide(prs)
    panel = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    panel.fill.solid()
    panel.fill.fore_color.rgb = NAVY
    panel.line.fill.background()
    gold_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(2.35), Inches(13.333), Inches(0.08)
    )
    gold_bar.fill.solid()
    gold_bar.fill.fore_color.rgb = GOLD
    gold_bar.line.fill.background()
    add_textbox(
        slide, Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.8),
        "Conclusion & Thank You",
        36, True, WHITE, PP_ALIGN.CENTER, "Georgia"
    )
    add_textbox(
        slide, Inches(1.2), Inches(2.7), Inches(10.9), Inches(2.2),
        "A working CLI cache simulator was built to make mapping policies visible.\n"
        "Cache size, block size, and ways can be changed without editing code.\n"
        "Students can compare direct-mapped and set-associative designs on the same trace.\n\n"
        "Questions?",
        16, False, CREAM, PP_ALIGN.CENTER
    )
    add_textbox(
        slide, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.0),
        "Comfort Akorfa Yikpa  •  Enock Yaw Sie\nComputer Architecture  |  Configurable Cache Memory Simulator",
        14, False, GOLD, PP_ALIGN.CENTER
    )

    output_path = r"C:\Users\Akorfa Gold\Desktop\cache_memory_simulator\Cache_Memory_Simulator_Presentation.pptx"
    prs.save(output_path)
    print(f"Saved: {output_path}")
    print(f"Slides: {len(prs.slides)}")


if __name__ == "__main__":
    build()

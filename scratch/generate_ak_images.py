import os
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "assets/amino_acids"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_MAIN_PATH = "C:/Windows/Fonts/arialbd.ttf"
MAIN_SIZE = 34
SUB_SIZE = 23
LINE_WIDTH = 4
TEXT_COLOR = (15, 23, 42)  # #0f172a
BOND_COLOR = (15, 23, 42)
BG_COLOR = (255, 255, 255)
BOND_LEN = 34

font_main = ImageFont.truetype(FONT_MAIN_PATH, MAIN_SIZE)
font_sub = ImageFont.truetype(FONT_MAIN_PATH, SUB_SIZE)

def parse_chem_text(text):
    tokens = []
    i = 0
    while i < len(text):
        c = text[i]
        if c.isdigit():
            tokens.append((c, True))
        else:
            tokens.append((c, False))
        i += 1
    return tokens

def measure_chem_text(text):
    tokens = parse_chem_text(text)
    total_w = 0
    max_h = 0
    for s, is_sub in tokens:
        f = font_sub if is_sub else font_main
        bbox = f.getbbox(s)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        total_w += w + 1
        max_h = max(max_h, h)
    return total_w, max_h

def draw_chem_text(draw, x, y, text, color=TEXT_COLOR):
    tokens = parse_chem_text(text)
    cur_x = x
    for s, is_sub in tokens:
        f = font_sub if is_sub else font_main
        bbox = f.getbbox(s)
        w = bbox[2] - bbox[0]
        y_offset = 9 if is_sub else 0
        draw.text((cur_x, y + y_offset), s, font=f, fill=color)
        cur_x += w + 1
    return cur_x

def draw_centered_chem_text(draw, cx, cy, text, color=TEXT_COLOR):
    w, h = measure_chem_text(text)
    x = cx - w / 2
    y = cy - h / 2
    draw_chem_text(draw, x, y, text, color)
    return w, h

def create_base_canvas(width=900, height=380):
    im = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle([(10, 10), (width - 10, height - 10)], radius=16, outline=(226, 232, 240), width=2)
    return im, draw

def render_linear_chain(filename, items, y_main=150, canvas_w=900, canvas_h=380):
    im, draw = create_base_canvas(canvas_w, canvas_h)

    total_w = 0
    for it in items:
        if it[0] == 'text':
            tw, _ = measure_chem_text(it[1])
            total_w += tw
        elif it[0] in ('bond', 'double_bond'):
            total_w += BOND_LEN
        elif it[0] == 'long_bond':
            total_w += BOND_LEN + 15

    start_x = (canvas_w - total_w) / 2
    cur_x = start_x

    for it in items:
        if it[0] == 'text':
            text = it[1]
            tw, th = measure_chem_text(text)
            draw_chem_text(draw, cur_x, y_main, text)

            branch_bot = it[2] if len(it) > 2 else None
            is_double_bot = it[4] if len(it) > 4 else False

            if branch_bot:
                center_x = cur_x + tw / 2
                bond_top = y_main + th + 10
                bond_bot = bond_top + 32
                if is_double_bot:
                    draw.line([(center_x - 4, bond_top), (center_x - 4, bond_bot)], fill=BOND_COLOR, width=3)
                    draw.line([(center_x + 4, bond_top), (center_x + 4, bond_bot)], fill=BOND_COLOR, width=3)
                else:
                    draw.line([(center_x, bond_top), (center_x, bond_bot)], fill=BOND_COLOR, width=LINE_WIDTH)
                bw, _ = measure_chem_text(branch_bot)
                draw_chem_text(draw, center_x - bw / 2, bond_bot + 6, branch_bot)

            cur_x += tw
        elif it[0] == 'bond':
            y_bond = y_main + 15
            draw.line([(cur_x + 5, y_bond), (cur_x + BOND_LEN - 5, y_bond)], fill=BOND_COLOR, width=LINE_WIDTH)
            cur_x += BOND_LEN
        elif it[0] == 'double_bond':
            y_bond = y_main + 15
            draw.line([(cur_x + 5, y_bond - 4), (cur_x + BOND_LEN - 5, y_bond - 4)], fill=BOND_COLOR, width=3)
            draw.line([(cur_x + 5, y_bond + 4), (cur_x + BOND_LEN - 5, y_bond + 4)], fill=BOND_COLOR, width=3)
            cur_x += BOND_LEN
        elif it[0] == 'long_bond':
            bl = BOND_LEN + 15
            y_bond = y_main + 15
            draw.line([(cur_x + 5, y_bond), (cur_x + bl - 5, y_bond)], fill=BOND_COLOR, width=LINE_WIDTH)
            cur_x += bl

    out_path = os.path.join(OUTPUT_DIR, filename)
    im.save(out_path, "PNG")

# 1. Glitsin (Gli.)
render_linear_chain("ak_1.png", [
    ('text', 'NH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'COOH')
], y_main=170)

# 2. Alanin (Ala.)
render_linear_chain("ak_2.png", [
    ('text', 'CH3'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 3. Valin (Val.)
render_linear_chain("ak_3.png", [
    ('text', 'CH3'),
    ('bond',),
    ('text', 'CH', 'CH3'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 4. Leysin (Ley.)
render_linear_chain("ak_4.png", [
    ('text', 'CH3'),
    ('bond',),
    ('text', 'CH', 'CH3'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 5. Izoleysin (Iley.)
render_linear_chain("ak_5.png", [
    ('text', 'CH3'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH', 'CH3'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 6. Asparagin kislota (Asp.)
render_linear_chain("ak_6.png", [
    ('text', 'HOOC'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 7. Glutamin kislota (Glu.)
render_linear_chain("ak_7.png", [
    ('text', 'HOOC'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 8. Ornitin (Ori.)
render_linear_chain("ak_8.png", [
    ('text', 'CH2', 'NH2'),
    ('bond',),
    ('text', '(CH2)2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 9. Lizin (Liz.)
render_linear_chain("ak_9.png", [
    ('text', 'NH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
], canvas_w=980)

# 10. Serin (Ser.)
render_linear_chain("ak_10.png", [
    ('text', 'HOCH2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 11. Treonin (Tre.)
render_linear_chain("ak_11.png", [
    ('text', 'CH3'),
    ('bond',),
    ('text', 'CH', 'OH'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 12. Sistein (Sis.-n)
render_linear_chain("ak_12.png", [
    ('text', 'HS'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# 13. Sistin (Sis.)
def render_sistin():
    im, draw = create_base_canvas(900, 380)
    # S — CH2 — CH(NH2)COOH
    row1_str = [('text', 'S'), ('bond',), ('text', 'CH2'), ('bond',), ('text', 'CH(NH2)COOH')]
    y1 = 120
    y2 = 240

    total_w = 0
    for it in row1_str:
        if it[0] == 'text':
            tw, _ = measure_chem_text(it[1])
            total_w += tw
        else:
            total_w += BOND_LEN

    start_x = (900 - total_w) / 2

    for y_row in [y1, y2]:
        cur_x = start_x
        for it in row1_str:
            if it[0] == 'text':
                tw, th = measure_chem_text(it[1])
                draw_chem_text(draw, cur_x, y_row, it[1])
                cur_x += tw
            else:
                y_bond = y_row + 15
                draw.line([(cur_x + 5, y_bond), (cur_x + BOND_LEN - 5, y_bond)], fill=BOND_COLOR, width=LINE_WIDTH)
                cur_x += BOND_LEN

    # Vertical S-S bond
    s_w, s_h = measure_chem_text('S')
    s_cx = start_x + s_w / 2
    draw.line([(s_cx, y1 + s_h + 10), (s_cx, y2 - 4)], fill=BOND_COLOR, width=LINE_WIDTH)

    im.save(os.path.join(OUTPUT_DIR, "ak_13.png"), "PNG")

render_sistin()

# 14. Metionin (Met.)
render_linear_chain("ak_14.png", [
    ('text', 'CH3'),
    ('bond',),
    ('text', 'S'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
])

# Helper for ring drawing: regular vertical hexagon (vertices at 30, 90, 150, 210, 270, 330 deg)
def get_hexagon_pts(cx, cy, r=46):
    pts = []
    # Pointy top/bottom or pointy left/right: pointy left/right means angles 0, 60, 120, 180, 240, 300
    for i in range(6):
        ang = math.radians(60 * i)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts

# 15. Fenilalanin (Fen.)
def render_fenilalanin():
    im, draw = create_base_canvas(900, 380)
    # Hexagon on left, then bond, then CH2 — CH(NH2) — COOH
    chain = [('bond',), ('text', 'CH2'), ('bond',), ('text', 'CH', 'NH2'), ('bond',), ('text', 'COOH')]

    chain_w = 0
    for it in chain:
        if it[0] == 'text':
            tw, _ = measure_chem_text(it[1])
            chain_w += tw
        else:
            chain_w += BOND_LEN

    ring_w = 92  # 2 * 46
    total_w = ring_w + chain_w
    start_x = (900 - total_w) / 2

    ring_cx = start_x + 46
    ring_cy = 165

    pts = get_hexagon_pts(ring_cx, ring_cy, 46)
    draw.polygon(pts, outline=BOND_COLOR, width=LINE_WIDTH)
    draw.ellipse([(ring_cx - 28, ring_cy - 28), (ring_cx + 28, ring_cy + 28)], outline=BOND_COLOR, width=3)

    cur_x = ring_cx + 46
    y_main = 150
    for it in chain:
        if it[0] == 'text':
            text = it[1]
            tw, th = measure_chem_text(text)
            draw_chem_text(draw, cur_x, y_main, text)
            if len(it) > 2 and it[2]:
                cx = cur_x + tw / 2
                bt = y_main + th + 10
                bb = bt + 32
                draw.line([(cx, bt), (cx, bb)], fill=BOND_COLOR, width=LINE_WIDTH)
                bw, _ = measure_chem_text(it[2])
                draw_chem_text(draw, cx - bw / 2, bb + 6, it[2])
            cur_x += tw
        elif it[0] == 'bond':
            y_bond = y_main + 15
            draw.line([(cur_x + 5, y_bond), (cur_x + BOND_LEN - 5, y_bond)], fill=BOND_COLOR, width=LINE_WIDTH)
            cur_x += BOND_LEN

    im.save(os.path.join(OUTPUT_DIR, "ak_15.png"), "PNG")

render_fenilalanin()

# 16. Tirozin (Tir.)
def render_tirozin():
    im, draw = create_base_canvas(900, 380)
    ho_w, ho_h = measure_chem_text('HO')
    chain = [('bond',), ('text', 'CH2'), ('bond',), ('text', 'CH', 'NH2'), ('bond',), ('text', 'COOH')]

    chain_w = 0
    for it in chain:
        if it[0] == 'text':
            tw, _ = measure_chem_text(it[1])
            chain_w += tw
        else:
            chain_w += BOND_LEN

    ring_w = 92
    total_w = ho_w + BOND_LEN + ring_w + chain_w
    start_x = (900 - total_w) / 2

    y_main = 150
    # HO text
    draw_chem_text(draw, start_x, y_main, 'HO')
    cur_x = start_x + ho_w

    # bond to ring
    draw.line([(cur_x + 5, y_main + 15), (cur_x + BOND_LEN - 5, y_main + 15)], fill=BOND_COLOR, width=LINE_WIDTH)
    cur_x += BOND_LEN

    ring_cx = cur_x + 46
    ring_cy = 165
    pts = get_hexagon_pts(ring_cx, ring_cy, 46)
    draw.polygon(pts, outline=BOND_COLOR, width=LINE_WIDTH)
    draw.ellipse([(ring_cx - 28, ring_cy - 28), (ring_cx + 28, ring_cy + 28)], outline=BOND_COLOR, width=3)

    cur_x = ring_cx + 46
    for it in chain:
        if it[0] == 'text':
            text = it[1]
            tw, th = measure_chem_text(text)
            draw_chem_text(draw, cur_x, y_main, text)
            if len(it) > 2 and it[2]:
                cx = cur_x + tw / 2
                bt = y_main + th + 10
                bb = bt + 32
                draw.line([(cx, bt), (cx, bb)], fill=BOND_COLOR, width=LINE_WIDTH)
                bw, _ = measure_chem_text(it[2])
                draw_chem_text(draw, cx - bw / 2, bb + 6, it[2])
            cur_x += tw
        elif it[0] == 'bond':
            y_bond = y_main + 15
            draw.line([(cur_x + 5, y_bond), (cur_x + BOND_LEN - 5, y_bond)], fill=BOND_COLOR, width=LINE_WIDTH)
            cur_x += BOND_LEN

    im.save(os.path.join(OUTPUT_DIR, "ak_16.png"), "PNG")

render_tirozin()

# 17. Triptofan (Tri.)
def render_triptofan():
    im, draw = create_base_canvas(900, 380)
    # Indole ring: benzene ring on left fused with pyrrole ring (with NH at bottom)
    chain = [('bond',), ('text', 'CH2'), ('bond',), ('text', 'CH', 'NH2'), ('bond',), ('text', 'COOH')]
    chain_w = 0
    for it in chain:
        if it[0] == 'text':
            chain_w += measure_chem_text(it[1])[0]
        else:
            chain_w += BOND_LEN

    indole_w = 160
    total_w = indole_w + chain_w
    start_x = (900 - total_w) / 2

    # Benzene ring (vertical orientation: flat sides left/right)
    # Vertices of left hexagon:
    # Top-left, top-right, bottom-right, bottom-left, etc.
    bx0 = start_x + 10
    by0 = 120
    bw = 65
    bh = 80

    # 6 vertices of benzene
    b_pts = [
        (bx0 + 20, by0),
        (bx0 + bw, by0 + 20),
        (bx0 + bw, by0 + bh - 20),
        (bx0 + 20, by0 + bh),
        (bx0, by0 + bh - 20),
        (bx0, by0 + 20)
    ]
    draw.polygon(b_pts, outline=BOND_COLOR, width=LINE_WIDTH)
    # Inner circle
    draw.ellipse([(bx0 + 10, by0 + 16), (bx0 + bw - 10, by0 + bh - 16)], outline=BOND_COLOR, width=3)

    # Indolning besh a'zoli halqasi: C3a–C3=C2–N1–C7a.
    fused_top = (bx0 + bw, by0 + 20)
    fused_bottom = (bx0 + bw, by0 + bh - 20)
    c3 = (bx0 + bw + 52, by0 + 23)
    c2 = (bx0 + bw + 67, by0 + 63)
    n_pos = (bx0 + bw + 30, by0 + 94)
    draw.line([fused_top, c3], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([c3, c2], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([(c3[0] - 7, c3[1] + 7), (c2[0] - 7, c2[1] - 7)], fill=BOND_COLOR, width=3)
    draw.line([c2, (n_pos[0] + 10, n_pos[1] - 8)], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([fused_bottom, (n_pos[0] - 10, n_pos[1] - 8)], fill=BOND_COLOR, width=LINE_WIDTH)

    # N–H yozuvi halqaning pastki uchida.
    nw, nh = measure_chem_text('N')
    draw_chem_text(draw, n_pos[0] - nw / 2, n_pos[1] - 12, 'N')
    draw.line([(n_pos[0], n_pos[1] + nh + 5), (n_pos[0], n_pos[1] + nh + 18)], fill=BOND_COLOR, width=LINE_WIDTH - 1)
    hw, _ = measure_chem_text('H')
    draw_chem_text(draw, n_pos[0] - hw / 2, n_pos[1] + nh + 22, 'H')

    # Yon zanjir C3 atomidan chiqadi.
    cur_x = c3[0]
    y_main = c3[1] - 15

    for it in chain:
        if it[0] == 'text':
            text = it[1]
            tw, th = measure_chem_text(text)
            draw_chem_text(draw, cur_x, y_main, text)
            if len(it) > 2 and it[2]:
                cx = cur_x + tw / 2
                bt = y_main + th + 10
                bb = bt + 32
                draw.line([(cx, bt), (cx, bb)], fill=BOND_COLOR, width=LINE_WIDTH)
                bw, _ = measure_chem_text(it[2])
                draw_chem_text(draw, cx - bw / 2, bb + 6, it[2])
            cur_x += tw
        elif it[0] == 'bond':
            y_bond = y_main + 15
            draw.line([(cur_x + 5, y_bond), (cur_x + BOND_LEN - 5, y_bond)], fill=BOND_COLOR, width=LINE_WIDTH)
            cur_x += BOND_LEN

    im.save(os.path.join(OUTPUT_DIR, "ak_17.png"), "PNG")

render_triptofan()

# 18. Prolin (Pro.)
def render_prolin():
    im, draw = create_base_canvas(900, 380)
    # Matching textbook page 330:
    # H2C ——— CH2
    #  |       |
    # H2C     CH — COOH
    #   \    /
    #      N
    #      |
    #      H
    cx = 400
    y_top = 100
    y_mid = 180
    y_bot = 260

    # Top vertices: H2C (left) and CH2 (right)
    x_left = cx - 90
    x_right = cx + 50

    # Draw H2C and CH2 at top
    draw_chem_text(draw, x_left - 30, y_top, "H2C")
    draw_chem_text(draw, x_right, y_top, "CH2")
    # Top bond
    draw.line([(x_left + 45, y_top + 15), (x_right - 10, y_top + 15)], fill=BOND_COLOR, width=LINE_WIDTH)

    # Mid left: H2C
    draw_chem_text(draw, x_left - 30, y_mid, "H2C")
    # Vertical bond left
    draw.line([(x_left - 5, y_top + 40), (x_left - 5, y_mid - 8)], fill=BOND_COLOR, width=LINE_WIDTH)

    # Mid right: CH — COOH
    ch_x = x_right
    ch_w, ch_h = measure_chem_text("CH")
    draw_chem_text(draw, ch_x, y_mid, "CH")
    # Vertical bond right
    draw.line([(ch_x + ch_w / 2, y_top + 40), (ch_x + ch_w / 2, y_mid - 8)], fill=BOND_COLOR, width=LINE_WIDTH)

    # Bond to COOH
    b_start = ch_x + ch_w + 8
    draw.line([(b_start, y_mid + 15), (b_start + BOND_LEN, y_mid + 15)], fill=BOND_COLOR, width=LINE_WIDTH)
    draw_chem_text(draw, b_start + BOND_LEN + 8, y_mid, "COOH")

    # Bottom vertex: N with | H
    n_cx = (x_left + x_right) / 2 + 10
    draw_chem_text(draw, n_cx - 12, y_bot - 10, "N")

    # Slanted lines to N
    draw.line([(x_left + 15, y_mid + 38), (n_cx - 20, y_bot)], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([(ch_x + 10, y_mid + 38), (n_cx + 25, y_bot)], fill=BOND_COLOR, width=LINE_WIDTH)

    # H under N
    draw.line([(n_cx, y_bot + 32), (n_cx, y_bot + 52)], fill=BOND_COLOR, width=LINE_WIDTH - 1)
    hw, _ = measure_chem_text("H")
    draw_chem_text(draw, n_cx - hw / 2, y_bot + 56, "H")

    im.save(os.path.join(OUTPUT_DIR, "ak_18.png"), "PNG")

render_prolin()

# 19. Oksiprolin (Pro-OH)
def render_oksiprolin():
    im, draw = create_base_canvas(900, 380)
    # Matching textbook page 330:
    # 5-membered pyrrolidine ring:
    # OH connected to top-left carbon (C4)
    # COOH connected to right carbon (C2)
    # Bottom has N with | H below it
    cx = 410
    cy = 160
    r = 55

    # 5 vertices of regular pentagon rotated so bottom vertex is at angle 90 deg (bottom)
    # Angles: 90 (bot), 162 (mid-left), 234 (top-left), 306 (top-right), 18 (mid-right)
    # In textbook, flat-ish top with apex at bottom:
    # Top-left, top-right, bottom-right, bottom vertex (N), bottom-left
    p_tl = (cx - 45, cy - 40)
    p_tr = (cx + 45, cy - 40)
    p_mr = (cx + 65, cy + 25)
    p_bot = (cx, cy + 80)
    p_ml = (cx - 65, cy + 25)

    # Draw ring lines
    draw.line([p_tl, p_tr], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([p_tr, p_mr], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([p_mr, (p_bot[0] + 18, p_bot[1] - 8)], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([p_tl, p_ml], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([p_ml, (p_bot[0] - 18, p_bot[1] - 8)], fill=BOND_COLOR, width=LINE_WIDTH)

    # N at bottom
    nw, nh = measure_chem_text("N")
    draw_chem_text(draw, p_bot[0] - nw / 2, p_bot[1] - 14, "N")
    draw.line([(p_bot[0], p_bot[1] + 26), (p_bot[0], p_bot[1] + 46)], fill=BOND_COLOR, width=LINE_WIDTH - 1)
    hw, _ = measure_chem_text("H")
    draw_chem_text(draw, p_bot[0] - hw / 2, p_bot[1] + 50, "H")

    # OH attached to top-left vertex p_tl
    oh_w, _ = measure_chem_text("OH")
    draw_chem_text(draw, p_tl[0] - oh_w - BOND_LEN - 8, p_tl[1] - 16, "OH")
    draw.line([(p_tl[0] - BOND_LEN - 4, p_tl[1]), (p_tl[0] - 4, p_tl[1])], fill=BOND_COLOR, width=LINE_WIDTH)

    # COOH attached to right vertex p_mr
    draw.line([(p_mr[0] + 4, p_mr[1]), (p_mr[0] + BOND_LEN + 4, p_mr[1])], fill=BOND_COLOR, width=LINE_WIDTH)
    draw_chem_text(draw, p_mr[0] + BOND_LEN + 10, p_mr[1] - 16, "COOH")

    im.save(os.path.join(OUTPUT_DIR, "ak_19.png"), "PNG")

render_oksiprolin()

# 20. Gistidin (Gis.)
def render_gistidin():
    im, draw = create_base_canvas(900, 380)
    # Textbook page 330:
    # HC ===== C — CH2 — CH — COOH
    # |        |         |
    # N        NH        NH2
    #  \      /
    #     CH

    chain = [('bond',), ('text', 'CH2'), ('bond',), ('text', 'CH', 'NH2'), ('bond',), ('text', 'COOH')]
    chain_w = 0
    for it in chain:
        if it[0] == 'text':
            chain_w += measure_chem_text(it[1])[0]
        else:
            chain_w += BOND_LEN

    ring_w = 110
    total_w = ring_w + chain_w
    start_x = (900 - total_w) / 2

    y_top = 100
    y_mid = 180
    y_bot = 250

    # Top HC ===== C
    hc_x = start_x
    hc_w, hc_h = measure_chem_text("HC")
    draw_chem_text(draw, hc_x, y_top, "HC")

    c_x = hc_x + hc_w + 50
    c_w, c_h = measure_chem_text("C")
    draw_chem_text(draw, c_x, y_top, "C")

    # Double bond between HC and C
    draw.line([(hc_x + hc_w + 6, y_top + 11), (c_x - 6, y_top + 11)], fill=BOND_COLOR, width=3)
    draw.line([(hc_x + hc_w + 6, y_top + 19), (c_x - 6, y_top + 19)], fill=BOND_COLOR, width=3)

    # Vertical line left from HC to N
    draw.line([(hc_x + hc_w / 2, y_top + 38), (hc_x + hc_w / 2, y_mid - 6)], fill=BOND_COLOR, width=LINE_WIDTH)
    draw_chem_text(draw, hc_x + hc_w / 2 - 10, y_mid, "N")

    # Vertical line right from C to NH
    draw.line([(c_x + c_w / 2, y_top + 38), (c_x + c_w / 2, y_mid - 6)], fill=BOND_COLOR, width=LINE_WIDTH)
    nh_w, _ = measure_chem_text("NH")
    draw_chem_text(draw, c_x + c_w / 2 - nh_w / 2, y_mid, "NH")

    # Slanted lines meeting at CH at bottom
    bot_ch_x = (hc_x + c_x) / 2
    # Imidazoldagi ikkinchi qo'sh bog': N=CH.
    draw.line([(hc_x + hc_w / 2 + 5, y_mid + 36), (bot_ch_x, y_bot - 4)], fill=BOND_COLOR, width=LINE_WIDTH)
    draw.line([(hc_x + hc_w / 2 + 13, y_mid + 34), (bot_ch_x + 7, y_bot - 10)], fill=BOND_COLOR, width=3)
    draw.line([(c_x + c_w / 2 - 5, y_mid + 36), (bot_ch_x + 20, y_bot - 4)], fill=BOND_COLOR, width=LINE_WIDTH)
    draw_chem_text(draw, bot_ch_x - 4, y_bot, "CH")

    # Chain extending from C to right
    cur_x = c_x + c_w
    y_main = y_top

    for it in chain:
        if it[0] == 'text':
            text = it[1]
            tw, th = measure_chem_text(text)
            draw_chem_text(draw, cur_x, y_main, text)
            if len(it) > 2 and it[2]:
                cx = cur_x + tw / 2
                bt = y_main + th + 10
                bb = bt + 32
                draw.line([(cx, bt), (cx, bb)], fill=BOND_COLOR, width=LINE_WIDTH)
                bw, _ = measure_chem_text(it[2])
                draw_chem_text(draw, cx - bw / 2, bb + 6, it[2])
            cur_x += tw
        elif it[0] == 'bond':
            y_bond = y_main + 15
            draw.line([(cur_x + 5, y_bond), (cur_x + BOND_LEN - 5, y_bond)], fill=BOND_COLOR, width=LINE_WIDTH)
            cur_x += BOND_LEN

    im.save(os.path.join(OUTPUT_DIR, "ak_20.png"), "PNG")

render_gistidin()

# 21. Arginin (Arg.)
# NH2 — C — NH — CH2 — CH2 — CH2 — CH — COOH
#       ||                         |
#       NH                         NH2
render_linear_chain("ak_21.png", [
    ('text', 'NH2'),
    ('bond',),
    ('text', 'C', 'NH', None, True),  # double bond to NH
    ('bond',),
    ('text', 'NH'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH2'),
    ('bond',),
    ('text', 'CH', 'NH2'),
    ('bond',),
    ('text', 'COOH')
], canvas_w=980)

print("All 21 images generated successfully!")

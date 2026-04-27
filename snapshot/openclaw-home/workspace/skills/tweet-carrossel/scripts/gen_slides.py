#!/usr/bin/env python3
"""
gen_slides.py — Gera slides 3+ no formato tweet v4.

Specs conforme SKILL.md v4:
- Avatar: 96px circular
- Nome: bold 58px #000000
- Handle: 41px #71767B
- Body: 60px #000000, line-height 1.28
- Gap avatar-texto: 28px
- Gap parágrafos: 36px
- Fundo: branco #FFFFFF
- Texto: uma cor só (#000000), sem bold/destaques
"""

import argparse, json, os, sys
from PIL import Image, ImageDraw, ImageFont

# ── Constants v4 ──
W, H = 1080, 1350
BG = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (113, 118, 123)  # #71767b
VERIFIED_BG = (29, 155, 240)

MARGIN_L = 64
MARGIN_R = 64
AVATAR_SIZE = 96
NAME_SIZE = 58
HANDLE_SIZE = 41
BODY_SIZE = 86

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_BOLD = os.path.join(SKILL_DIR, "assets", "DejaVuSans-Bold.ttf")
FONT_REG = os.path.join(SKILL_DIR, "assets", "DejaVuSans.ttf")

def get_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    sys_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    sys_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(sys_bold if bold else sys_reg, size)
    except:
        return ImageFont.load_default()

def make_circular_avatar(path, size):
    av = Image.open(path).convert("RGBA")
    w, h = av.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    av = av.crop((left, top, left + min_dim, top + min_dim))
    av = av.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(av, mask=mask)
    return out

def draw_verified(draw, x, y, size=38):
    draw.ellipse((x, y, x+size, y+size), fill=VERIFIED_BG)
    cx, cy = x + size//2, y + size//2
    draw.line([(cx-8, cy), (cx-2, cy+6)], fill=WHITE, width=3)
    draw.line([(cx-2, cy+6), (cx+8, cy-4)], fill=WHITE, width=3)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current = words[0] if words else ""
    for word in words[1:]:
        test = current + " " + word
        bbox = ImageDraw.Draw(Image.new("RGB", (1,1))).textbbox((0,0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def sanitize_text(text):
    replacements = {
        "\u2610": "•", "\u2611": "✓", "\u2612": "✗",
        "\u25a1": "•", "\u25a0": "•", "\u25aa": "•", "\u25ab": "•",
        "\u25cb": "•", "\u25cf": "•", "\u25b6": "→", "\u25b8": "→",
        "\u27a4": "→", "\u279c": "→", "\u2192": "→",
        "\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def measure_content(paragraphs):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    fh_name = d.textbbox((0, 0), "A", font=get_font(NAME_SIZE, bold=True))[3]
    fh_handle = d.textbbox((0, 0), "A", font=get_font(HANDLE_SIZE))[3]
    fh_body = d.textbbox((0, 0), "A", font=get_font(BODY_SIZE))[3]
    
    header_h = max(AVATAR_SIZE, fh_name + 10 + fh_handle)
    line_height = int(fh_body * 1.28)
    para_gap = 36
    empty_gap = int(fh_body * 0.6)
    
    body_h = 0
    for i, para in enumerate(paragraphs):
        if i > 0:
            body_h += empty_gap if para == "" else para_gap
        if para == "":
            continue
        lines = wrap_text(para, get_font(BODY_SIZE), W - MARGIN_L - MARGIN_R)
        body_h += len(lines) * line_height
    
    total_h = header_h + 50 + body_h
    return total_h, header_h, line_height, para_gap, empty_gap

def make_slide(paragraphs, out_path, avatar_path):
    paragraphs = [sanitize_text(p) for p in paragraphs]
    
    total_h, header_h, line_height, para_gap, empty_gap = measure_content(paragraphs)
    
    # Centralizar verticalmente
    y_start = (H - total_h) // 2
    y_start = max(60, y_start)
    
    img = Image.new("RGB", (W, H), BG)
    
    avatar = make_circular_avatar(avatar_path, AVATAR_SIZE)
    av = avatar.convert("RGBA")
    img_rgba = img.convert("RGBA")
    img_rgba.paste(av, (MARGIN_L, y_start), av)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)
    
    font_name = get_font(NAME_SIZE, bold=True)
    font_handle = get_font(HANDLE_SIZE)
    font_body = get_font(BODY_SIZE)
    
    x_text = MARGIN_L + AVATAR_SIZE + 28
    fh_name = draw.textbbox((0, 0), "A", font=font_name)[3]
    fh_handle = draw.textbbox((0, 0), "A", font=font_handle)[3]
    
    y_name = y_start + (AVATAR_SIZE - fh_name - 10 - fh_handle) // 2
    draw.text((x_text, y_name), "Dra Daniely Freitas", font=font_name, fill=BLACK)
    
    name_w = draw.textbbox((x_text, y_name), "Dra Daniely Freitas", font=font_name)[2] - x_text
    draw_verified(draw, x_text + name_w + 12, y_name + (fh_name - 38) // 2, 38)
    
    y_handle = y_name + fh_name + 6
    draw.text((x_text, y_handle), "@dradaniely.freitas", font=font_handle, fill=GRAY)
    
    y_body = y_start + header_h + 50
    max_text_w = W - MARGIN_L - MARGIN_R
    
    for i, para in enumerate(paragraphs):
        if i > 0:
            y_body += empty_gap if para == "" else para_gap
        if para == "":
            continue
        lines = wrap_text(para, font_body, max_text_w)
        for line in lines:
            draw.text((MARGIN_L, y_body), line, font=font_body, fill=BLACK)
            y_body += line_height
    
    img.save(out_path, "PNG")
    print(f"  ✓ {out_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--avatar", default="/root/avatar_hq.png")
    parser.add_argument("--out", default="./output")
    args = parser.parse_args()
    
    os.makedirs(args.out, exist_ok=True)
    
    with open(args.config) as f:
        slides = json.load(f)
    
    print(f"Gerando {len(slides)} slide(s)...")
    for slide in slides:
        out = os.path.join(args.out, f"slide_{slide['num']:02d}.png")
        make_slide(slide["paragraphs"], out, args.avatar)
    
    print("Concluído.")

if __name__ == "__main__":
    main()

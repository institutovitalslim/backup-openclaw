#!/usr/bin/env python3
"""
make_tweet_slides.py — Gera slides no formato tweet para carrosséis do Instagram.

Uso:
    python3 make_tweet_slides.py --config slides.json --avatar avatar.png --out ./output

slides.json deve ter o formato:
[
  {
    "num": 3,
    "total": 6,
    "paragraphs": [
      "Primeiro parágrafo do slide.",
      "",
      "Segundo parágrafo após linha em branco.",
      "→ Item com seta"
    ]
  },
  ...
]
"""

import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# ── Defaults ──────────────────────────────────────────────────────────────
W, H         = 1080, 1350
BG           = (0, 0, 0)
WHITE        = (255, 255, 255)
GRAY         = (140, 150, 145)
VERIFIED_BG  = (29, 155, 240)
MARGIN_L     = 64
MARGIN_R     = 64
AVATAR_SIZE  = 56
NAME_SIZE    = 30
HANDLE_SIZE  = 26
BODY_SIZE    = 34

SKILL_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_BOLD    = os.path.join(SKILL_DIR, "assets", "DejaVuSans-Bold.ttf")
FONT_REG     = os.path.join(SKILL_DIR, "assets", "DejaVuSans.ttf")

# ── Helpers ───────────────────────────────────────────────────────────────

def get_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    # fallback sistema
    sys_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    sys_reg  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(sys_bold if bold else sys_reg, size)
    except:
        return ImageFont.load_default()


def make_circular_avatar(path, size):
    av = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(av, mask=mask)
    return out


def draw_verified(draw, x, y, size=18):
    draw.ellipse((x, y, x+size, y+size), fill=VERIFIED_BG)
    cx, cy = x + size//2, y + size//2
    draw.line([(cx-4, cy), (cx-1, cy+3)], fill=WHITE, width=2)
    draw.line([(cx-1, cy+3), (cx+4, cy-3)], fill=WHITE, width=2)


def wrap_text(text, font, max_width):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip()
        if d.textbbox((0, 0), test, font=font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def measure_block(paragraphs, font_body, font_name, font_handle, max_w):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    fh_body   = d.textbbox((0, 0), "A", font=font_body)[3]
    fh_name   = d.textbbox((0, 0), "A", font=font_name)[3]
    fh_handle = d.textbbox((0, 0), "A", font=font_handle)[3]
    lh        = int(fh_body * 1.45)
    header_h  = max(AVATAR_SIZE, fh_name + 8 + fh_handle)
    body_h    = 0
    for i, para in enumerate(paragraphs):
        if i > 0:
            body_h += int(fh_body * 0.5) if para == "" else int(fh_body * 0.8)
        if para == "":
            body_h += int(fh_body * 0.5)
            continue
        body_h += len(wrap_text(para, font_body, max_w)) * lh
    return header_h + 28 + body_h, lh, fh_body, fh_name, fh_handle


# ── Render ────────────────────────────────────────────────────────────────

def make_slide(paragraphs, out_path, avatar_img,
               name="Dra Daniely Freitas", handle="@dradaniely.freitas",
               show_verified=True):

    font_name   = get_font(NAME_SIZE,   bold=True)
    font_handle = get_font(HANDLE_SIZE)
    font_body   = get_font(BODY_SIZE)
    max_text_w  = W - MARGIN_L - MARGIN_R

    total_h, lh, fh_body, fh_name, fh_handle = measure_block(
        paragraphs, font_body, font_name, font_handle, max_text_w)

    # Centralizar verticalmente sempre
    y_start = max(40, (H - total_h) // 2)

    img = Image.new("RGB", (W, H), BG)

    # Avatar
    av = avatar_img.convert("RGBA")
    img_rgba = img.convert("RGBA")
    img_rgba.paste(av, (MARGIN_L, y_start), av)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Nome
    name_x, name_y = MARGIN_L + AVATAR_SIZE + 14, y_start + 2
    draw.text((name_x, name_y), name, font=font_name, fill=WHITE)
    if show_verified:
        nb = draw.textbbox((name_x, name_y), name, font=font_name)
        draw_verified(draw, nb[2] + 6, name_y + 6, 18)

    # Handle
    draw.text((name_x, name_y + fh_name + 6), handle, font=font_handle, fill=GRAY)

    # Corpo
    header_h = max(AVATAR_SIZE, fh_name + 8 + fh_handle)
    ty = y_start + header_h + 28
    for i, para in enumerate(paragraphs):
        if i > 0:
            if para == "":
                ty += int(fh_body * 0.5)
                continue
            ty += int(fh_body * 0.8)
        if para == "":
            ty += int(fh_body * 0.5)
            continue
        for line in wrap_text(para, font_body, max_text_w):
            draw.text((MARGIN_L, ty), line, font=font_body, fill=WHITE)
            ty += lh

    img.save(out_path, "PNG")
    print(f"  ✓ {out_path}")


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Gera slides de tweet para Instagram")
    ap.add_argument("--config",  required=True,  help="JSON com slides")
    ap.add_argument("--avatar",  required=True,  help="Imagem do avatar (jpg/png)")
    ap.add_argument("--out",     default="./output", help="Pasta de saída")
    ap.add_argument("--name",    default="Dra Daniely Freitas")
    ap.add_argument("--handle",  default="@dradaniely.freitas")
    ap.add_argument("--no-verified", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    with open(args.config) as f:
        slides = json.load(f)

    avatar_img = make_circular_avatar(args.avatar, AVATAR_SIZE)

    print(f"Gerando {len(slides)} slide(s) em {args.out}/")
    for s in slides:
        fname    = f"slide_{s['num']:02d}.png"
        out_path = os.path.join(args.out, fname)
        make_slide(
            paragraphs    = s["paragraphs"],
            out_path      = out_path,
            avatar_img    = avatar_img,
            name          = args.name,
            handle        = args.handle,
            show_verified = not args.no_verified,
        )

    print("Concluído.")


if __name__ == "__main__":
    main()

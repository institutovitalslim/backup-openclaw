#!/usr/bin/env python3
"""Generate Glycine carousel slides (2-10) with white background and black text."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1350
PADDING = 60
MARGIN = 64

# Colors
BG = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black
HANDLE_COLOR = (113, 118, 123)  # #71767B
BLUE_VERIFY = (29, 155, 240)  # #1D9BF0

# Font paths
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def load_font(path, size):
    if os.path.isfile(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# Font sizes (+20% from original)
NAME_SIZE = 58
HANDLE_SIZE = 41
BODY_SIZE = 60
VERIFY_SIZE = 46

def create_slide(text_lines, avatar_path=None, output_path="slide.jpg"):
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    
    # Header with avatar
    avatar_size = 96
    avatar_x = MARGIN
    avatar_y = 60
    
    # Draw avatar circle (placeholder or real)
    if avatar_path and os.path.isfile(avatar_path):
        avatar = Image.open(avatar_path).convert("RGBA")
        avatar = avatar.resize((avatar_size, avatar_size), Image.LANCZOS)
        # Create circular mask
        mask = Image.new("L", (avatar_size, avatar_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
        canvas.paste(avatar, (avatar_x, avatar_y), mask)
    else:
        # Draw placeholder circle
        draw.ellipse((avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size), 
                     fill=(200, 200, 200), outline=(180, 180, 180), width=2)
    
    # Name and handle
    name_font = load_font(FONT_BOLD, NAME_SIZE)
    handle_font = load_font(FONT_REG, HANDLE_SIZE)
    
    name_x = avatar_x + avatar_size + 28
    name_y = avatar_y + 10
    
    draw.text((name_x, name_y), "Dra. Daniely Freitas", fill=TEXT_COLOR, font=name_font)
    
    # Verify badge
    verify_x = name_x + 420
    verify_y = name_y + 8
    draw.ellipse((verify_x, verify_y, verify_x + VERIFY_SIZE, verify_y + VERIFY_SIZE), fill=BLUE_VERIFY)
    check_font = load_font(FONT_BOLD, 24)
    draw.text((verify_x + 12, verify_y + 8), "✓", fill=(255, 255, 255), font=check_font)
    
    # Handle
    handle_y = name_y + NAME_SIZE + 4
    draw.text((name_x, handle_y), "@dradaniely.freitas", fill=HANDLE_COLOR, font=handle_font)
    
    # Body text
    body_font = load_font(FONT_REG, BODY_SIZE)
    y_start = avatar_y + avatar_size + 50
    x_start = MARGIN
    line_height = int(BODY_SIZE * 1.4)
    
    for i, line in enumerate(text_lines):
        y = y_start + i * line_height
        draw.text((x_start, y), line, fill=TEXT_COLOR, font=body_font)
    
    canvas.save(output_path, "JPEG", quality=85)
    print(f"Saved: {output_path}")
    return output_path

# Slide definitions
slides = {
    "slide_02": [
        "E se eu te dissesse que um",
        "aminoácido simples pode:",
        "",
        "→ Aumentar sua expectativa de vida",
        "→ Apagar a inflamação crônica",
        "→ Curar seu intestino",
        "→ Fazer você dormir como um bebê"
    ],
    "slide_03": [
        "Você já se sentiu:",
        "",
        "Cansado o tempo todo?",
        "Com intestino irritado?",
        "Dormindo mal e acordando pior?",
        "Com pele envelhecendo rápido demais?",
        "",
        "A maioria acha que isso é",
        '\"normal\" da idade.'
    ],
    "slide_04": [
        "Isso tem nome:",
        "",
        "GLICINA.",
        "",
        "Um aminoácido que seu corpo",
        "produz, mas em quantidades",
        "insuficientes.",
        "",
        "Especialmente depois dos 30 anos.",
        "",
        "📎 Razak et al. (2017). PMID: 28337245"
    ],
    "slide_05": [
        "A glicina é o maior",
        "anti-inflamatório natural.",
        "",
        "Ela suprime o NF-KB:",
        "o \"regulador mestre\"",
        "da inflamação.",
        "",
        "Está elevado em TODA",
        "doença crônica.",
        "",
        "📎 Razak et al. (2017). PMID: 28337245"
    ],
    "slide_06": [
        "Ela também:",
        "",
        "→ Limpa a homocisteína (tóxica)",
        "→ Produz glutationa (antioxidante)",
        "→ É precursora da creatina",
        "→ Sintetiza colágeno",
        "→ Promove autofagia",
        "",
        "📎 Razak et al. (2017). PMID: 28337245"
    ],
    "slide_07": [
        "Glicina + NAC =",
        "combo anti-aging.",
        "",
        "Estudo clínico mostrou melhora em:",
        "Glutationa, estresse oxidativo,",
        "função mitocondrial, inflamação,",
        "resistência à insulina...",
        "",
        "📎 Kumar et al. (2021). PMID: 33783984"
    ],
    "slide_08": [
        "Aqui está o que poucos sabem:",
        "",
        "A glicina contrabalanceia os",
        "efeitos pró-envelhecimento da",
        "METIONINA em excesso — principal",
        "componente das carnes vermelhas.",
        "",
        "Quem come muita carne precisa",
        "URGENTE de mais glicina.",
        "",
        "📎 Miller et al. (2019). PMID: 30916479"
    ],
    "slide_09": [
        "Como usar:",
        "",
        "→ 3g antes de dormir",
        "  (melhora sono profundo)",
        "→ 1-2g pela manhã",
        "  (energia e foco)",
        "",
        "Fontes naturais:",
        "Caldo de ossos, pele de frango,",
        "colágeno hidrolisado",
        "",
        "📎 Bannai et al. (2012). PMID: 22529837"
    ],
    "slide_10": [
        "Salva isso antes que suma.",
        "",
        "Qual desses benefícios",
        "você mais precisa?",
        "",
        "Comenta aqui 👇",
        "",
        "",
        "Dra. Daniely Freitas",
        "CRM-BA 27588"
    ]
}

# Avatar path
avatar_path = "/root/avatar_hq.png"
if not os.path.isfile(avatar_path):
    avatar_path = None

# Generate all slides
output_dir = "/root/carrossel_glicina"
os.makedirs(output_dir, exist_ok=True)

for name, lines in slides.items():
    path = os.path.join(output_dir, f"{name}.jpg")
    create_slide(lines, avatar_path, path)

print(f"\nAll slides saved to {output_dir}/")

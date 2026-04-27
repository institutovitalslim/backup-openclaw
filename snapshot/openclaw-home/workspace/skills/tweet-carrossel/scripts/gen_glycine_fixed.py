#!/usr/bin/env python3
"""Generate Glycine carousel slides with proper formatting using PIL."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1350
MARGIN_X = 80
MARGIN_Y = 60

# Colors
BG = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
HANDLE_COLOR = (83, 100, 113)
BLUE_VERIFY = (29, 155, 240)

# Font paths
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def load_font(path, size):
    if os.path.isfile(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = ' '.join(current + [word])
        w, _ = get_text_size(draw, test, font)
        if w <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(' '.join(current))
            current = [word]
    if current:
        lines.append(' '.join(current))
    return lines

def create_slide(text_lines, avatar_path=None, output_path="slide.jpg"):
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    
    # Fonts
    name_font = load_font(FONT_BOLD, 32)
    handle_font = load_font(FONT_REG, 22)
    body_font = load_font(FONT_REG, 42)
    ref_font = load_font(FONT_REG, 26)
    sig_font = load_font(FONT_BOLD, 36)
    
    # Avatar
    avatar_size = 64
    avatar_x = MARGIN_X
    avatar_y = MARGIN_Y
    
    if avatar_path and os.path.isfile(avatar_path):
        avatar = Image.open(avatar_path).convert("RGBA")
        avatar = avatar.resize((avatar_size, avatar_size), Image.LANCZOS)
        mask = Image.new("L", (avatar_size, avatar_size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, avatar_size, avatar_size), fill=255)
        canvas.paste(avatar, (avatar_x, avatar_y), mask)
    else:
        draw.ellipse((avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size), 
                     fill=(200, 200, 200))
    
    # Name and handle
    name_x = avatar_x + avatar_size + 16
    name_y = avatar_y + 6
    
    # Calculate name width to position badge
    name_text = "Dra. Daniely Freitas"
    name_w, name_h = get_text_size(draw, name_text, name_font)
    
    draw.text((name_x, name_y), name_text, fill=TEXT_COLOR, font=name_font)
    
    # Verify badge (small blue circle with check)
    badge_size = 20
    badge_x = name_x + name_w + 8
    badge_y = name_y + 4
    draw.ellipse((badge_x, badge_y, badge_x + badge_size, badge_y + badge_size), fill=BLUE_VERIFY)
    # White check mark
    check_font = load_font(FONT_BOLD, 14)
    draw.text((badge_x + 5, badge_y + 2), "✓", fill=(255, 255, 255), font=check_font)
    
    # Handle
    handle_y = name_y + name_h + 2
    draw.text((name_x, handle_y), "@dradaniely.freitas", fill=HANDLE_COLOR, font=handle_font)
    
    # Body area
    y = avatar_y + avatar_size + 40
    x = MARGIN_X
    max_w = W - (MARGIN_X * 2)
    line_height = 56
    ref_line_height = 36
    
    for line in text_lines:
        if line == "":
            y += line_height * 0.5
            continue
        
        if line.startswith("Dra.") and "CRM" in line:
            # Signature
            draw.text((x, y), line, fill=TEXT_COLOR, font=sig_font)
            y += line_height * 1.2
        elif line.startswith("🔗") or "PMID:" in line:
            # Reference
            wrapped = wrap_text(draw, line, ref_font, max_w)
            for sub in wrapped:
                draw.text((x, y), sub, fill=HANDLE_COLOR, font=ref_font)
                y += ref_line_height
            y += 8
        elif line.startswith("→"):
            # Bullet
            wrapped = wrap_text(draw, line, body_font, max_w)
            for sub in wrapped:
                draw.text((x, y), sub, fill=TEXT_COLOR, font=body_font)
                y += line_height
        else:
            # Regular line
            wrapped = wrap_text(draw, line, body_font, max_w)
            for sub in wrapped:
                draw.text((x, y), sub, fill=TEXT_COLOR, font=body_font)
                y += line_height
        
        # Prevent overflow
        if y > H - MARGIN_Y:
            break
    
    canvas.save(output_path, "JPEG", quality=90)
    print(f"Saved: {output_path}")
    return output_path

# Slide definitions
slides = {
    "slide_02": [
        "E se eu te dissesse que um aminoacido simples pode:",
        "",
        "-> Aumentar sua expectativa de vida",
        "-> Apagar a inflamacao cronica",
        "-> Curar seu intestino",
        "-> Fazer voce dormir como um bebe"
    ],
    "slide_03": [
        "Voce ja se sentiu:",
        "",
        "Cansado o tempo todo?",
        "Com intestino irritado?",
        "Dormindo mal e acordando pior?",
        "Com pele envelhecendo rapido?",
        "",
        "A maioria acha que isso e 'normal' da idade."
    ],
    "slide_04": [
        "Isso tem nome:",
        "",
        "GLICINA.",
        "",
        "Um aminoacido que seu corpo produz, mas em quantidades insuficientes.",
        "",
        "Especialmente depois dos 30 anos.",
        "",
        "Ref: Razak et al. (2017). PMID: 28337245"
    ],
    "slide_05": [
        "A glicina e o maior anti-inflamatorio natural.",
        "",
        "Ela suprime o NF-KB:",
        "o 'regulador mestre' da inflamacao.",
        "",
        "Esta elevado em TODA doenca cronica.",
        "",
        "Ref: Razak et al. (2017). PMID: 28337245"
    ],
    "slide_06": [
        "Ela tambem:",
        "",
        "-> Limpa a homocisteina (toxica)",
        "-> Produz glutationa (antioxidante)",
        "-> E precursora da creatina",
        "-> Sintetiza colageno",
        "-> Promove autofagia",
        "",
        "Ref: Razak et al. (2017). PMID: 28337245"
    ],
    "slide_07": [
        "Glicina + NAC = combo anti-aging.",
        "",
        "Estudo clinico mostrou melhora em:",
        "Glutationa, estresse oxidativo,",
        "funcao mitocondrial, inflamacao,",
        "resistencia a insulina...",
        "",
        "Ref: Kumar et al. (2021). PMID: 33783984"
    ],
    "slide_08": [
        "Aqui esta o que poucos sabem:",
        "",
        "A glicina contrabalanceia os efeitos pro-envelhecimento da METIONINA em excesso — principal componente das carnes vermelhas.",
        "",
        "Quem come muita carne precisa URGENTE de mais glicina.",
        "",
        "Ref: Miller et al. (2019). PMID: 30916479"
    ],
    "slide_09": [
        "Como usar:",
        "",
        "-> 3g antes de dormir (melhora sono profundo)",
        "-> 1-2g pela manha (energia e foco)",
        "",
        "Fontes naturais:",
        "Caldo de ossos, pele de frango,",
        "colageno hidrolisado",
        "",
        "Ref: Bannai et al. (2012). PMID: 22529837"
    ],
    "slide_10": [
        "Salva isso antes que suma.",
        "",
        "Qual desses beneficios voce mais precisa?",
        "",
        "Comenta aqui",
        "",
        "",
        "Dra. Daniely Freitas",
        "CRM-BA 27588"
    ]
}

# Generate
output_dir = "/root/carrossel_glicina"
os.makedirs(output_dir, exist_ok=True)

avatar_path = "/root/avatar_dra_sorrindo.png"

for name, lines in slides.items():
    path = os.path.join(output_dir, f"{name}.jpg")
    create_slide(lines, avatar_path, path)

print(f"\nAll slides saved to {output_dir}/")

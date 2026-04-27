#!/usr/bin/env python3
"""Generate Glycine carousel slides using HTML + Chromium for professional results."""

import os
import subprocess
import tempfile

W, H = 1080, 1350
MARGIN = 64

def create_slide_html(slide_num, text_lines, avatar_path=None):
    """Create HTML for a single slide."""
    
    # Build body text
    body_html = []
    for line in text_lines:
        if line == "":
            body_html.append("<div style='height: 20px;'></div>")
        elif line.startswith("→"):
            body_html.append(f"<div class='bullet'>{line}</div>")
        elif line.startswith("📎") or line.startswith("🔗"):
            body_html.append(f"<div class='ref'>{line}</div>")
        elif line.startswith("Dra.") and "CRM" in line:
            body_html.append(f"<div class='signature'>{line}</div>")
        else:
            body_html.append(f"<div class='line'>{line}</div>")
    
    body_content = "\n".join(body_html)
    
    # Avatar handling
    avatar_html = ""
    if avatar_path and os.path.isfile(avatar_path):
        avatar_html = f"<img src='file://{avatar_path}' class='avatar-img' alt='avatar'>"
    else:
        avatar_html = "<div class='avatar-placeholder'></div>"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: {W}px;
    height: {H}px;
    background: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    padding: {MARGIN}px;
    display: flex;
    flex-direction: column;
}}
.header {{
    display: flex;
    align-items: center;
    margin-bottom: 32px;
    flex-shrink: 0;
}}
.avatar-img {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 16px;
    flex-shrink: 0;
}}
.avatar-placeholder {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: #ddd;
    margin-right: 16px;
    flex-shrink: 0;
}}
.name-section {{
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.name-row {{
    display: flex;
    align-items: center;
    gap: 6px;
}}
.name {{
    font-size: 28px;
    font-weight: 800;
    color: #000000;
    line-height: 1.2;
}}
.verify-badge {{
    width: 22px;
    height: 22px;
    background: #1D9BF0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}}
.verify-badge svg {{
    width: 14px;
    height: 14px;
    fill: white;
}}
.handle {{
    font-size: 20px;
    color: #71767B;
    line-height: 1.3;
    margin-top: 2px;
}}
.content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    padding-top: 8px;
}}
.line {{
    font-size: 44px;
    color: #000000;
    line-height: 1.35;
    margin-bottom: 8px;
    font-weight: 400;
}}
.bullet {{
    font-size: 44px;
    color: #000000;
    line-height: 1.35;
    margin-bottom: 12px;
    font-weight: 400;
}}
.ref {{
    font-size: 28px;
    color: #71767B;
    line-height: 1.4;
    margin-top: 16px;
    font-weight: 400;
}}
.signature {{
    font-size: 32px;
    color: #000000;
    line-height: 1.4;
    margin-top: auto;
    font-weight: 600;
}}
</style>
</head>
<body>
<div class="header">
    {avatar_html}
    <div class="name-section">
        <div class="name-row">
            <span class="name">Dra. Daniely Freitas</span>
            <div class="verify-badge">
                <svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
            </div>
        </div>
        <div class="handle">@dradaniely.freitas</div>
    </div>
</div>
<div class="content">
    {body_content}
</div>
</body>
</html>"""
    return html

def render_html_to_image(html_content, output_path):
    """Render HTML to image using Chromium."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        html_path = f.name
    
    try:
        cmd = [
            'chromium-browser',
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            f'--window-size={W},{H}',
            '--hide-scrollbars',
            '--screenshot=' + output_path,
            '--force-device-scale-factor=1',
            'file://' + html_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"Chromium error: {result.stderr}")
            return False
        return os.path.isfile(output_path)
    except Exception as e:
        print(f"Error rendering: {e}")
        return False
    finally:
        try:
            os.unlink(html_path)
        except:
            pass

# Slide definitions
slides = {
    "slide_02": [
        "E se eu te dissesse que um aminoácido simples pode:",
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
        "Com pele envelhecendo rápido?",
        "",
        "A maioria acha que isso é 'normal' da idade."
    ],
    "slide_04": [
        "Isso tem nome:",
        "",
        "GLICINA.",
        "",
        "Um aminoácido que seu corpo produz, mas em quantidades insuficientes.",
        "",
        "Especialmente depois dos 30 anos.",
        "",
        "🔗 Razak et al. (2017). PMID: 28337245"
    ],
    "slide_05": [
        "A glicina é o maior anti-inflamatório natural.",
        "",
        "Ela suprime o NF-KB:",
        "o 'regulador mestre' da inflamação.",
        "",
        "Está elevado em TODA doença crônica.",
        "",
        "🔗 Razak et al. (2017). PMID: 28337245"
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
        "🔗 Razak et al. (2017). PMID: 28337245"
    ],
    "slide_07": [
        "Glicina + NAC = combo anti-aging.",
        "",
        "Estudo clínico mostrou melhora em:",
        "Glutationa, estresse oxidativo,",
        "função mitocondrial, inflamação,",
        "resistência à insulina...",
        "",
        "🔗 Kumar et al. (2021). PMID: 33783984"
    ],
    "slide_08": [
        "Aqui está o que poucos sabem:",
        "",
        "A glicina contrabalanceia os efeitos pró-envelhecimento da METIONINA em excesso — principal componente das carnes vermelhas.",
        "",
        "Quem come muita carne precisa URGENTE de mais glicina.",
        "",
        "🔗 Miller et al. (2019). PMID: 30916479"
    ],
    "slide_09": [
        "Como usar:",
        "",
        "→ 3g antes de dormir (melhora sono profundo)",
        "→ 1-2g pela manhã (energia e foco)",
        "",
        "Fontes naturais:",
        "Caldo de ossos, pele de frango,",
        "colágeno hidrolisado",
        "",
        "🔗 Bannai et al. (2012). PMID: 22529837"
    ],
    "slide_10": [
        "Salva isso antes que suma.",
        "",
        "Qual desses benefícios você mais precisa?",
        "",
        "Comenta aqui 👇",
        "",
        "",
        "Dra. Daniely Freitas",
        "CRM-BA 27588"
    ]
}

# Generate all slides
output_dir = "/root/carrossel_glicina"
os.makedirs(output_dir, exist_ok=True)

avatar_path = "/root/avatar_dra_real.png"

for name, lines in slides.items():
    html = create_slide_html(name, lines, avatar_path)
    path = os.path.join(output_dir, f"{name}.jpg")
    if render_html_to_image(html, path):
        print(f"Saved: {path}")
    else:
        print(f"Failed: {path}")

print(f"\nDone! Slides in {output_dir}/")

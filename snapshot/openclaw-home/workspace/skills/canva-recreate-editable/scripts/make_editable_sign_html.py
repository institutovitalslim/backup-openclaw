#!/usr/bin/env python3
import argparse, html, json, pathlib

TEMPLATE = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  @page {{ size: {size_cm}cm {size_cm}cm; margin: 0; }}
  html, body {{
    width: {size_cm}cm; height: {size_cm}cm; margin: 0; padding: 0;
    background: {bg};
    font-family: Arial, Helvetica, sans-serif;
  }}
  .card {{
    box-sizing: border-box;
    width: {size_cm}cm; height: {size_cm}cm;
    background: {bg}; color: {text};
    position: relative; padding: 0.52cm 0.46cm 0.46cm;
  }}
  .border {{ position: absolute; inset: 0.22cm; border: 1.4px solid {border}; pointer-events: none; }}
  .content {{ position: relative; z-index: 2; text-align: center; line-height: 1.18; }}
  .small {{ font-size: 10.8pt; font-weight: 300; letter-spacing: 0.02em; }}
  .mid {{ font-size: 9.7pt; font-weight: 300; line-height: 1.22; margin: 0.03cm 0; }}
  .big {{ font-size: 23pt; font-weight: 700; letter-spacing: 0.06em; color: {big}; margin: 0.08cm 0 0.15cm; }}
  .logo {{ position: absolute; bottom: 0.38cm; left: 0.46cm; right: 0.46cm; text-align: center; font-size: 8pt; color: {logo}; letter-spacing: 0.18em; font-weight: 700; }}
  .sublogo {{ display:block; font-size:4.8pt; letter-spacing:0.24em; color:{sublogo}; margin-top:0.05cm; }}
</style>
</head>
<body>
  <div class="card">
    <div class="border"></div>
    <div class="content">
      {content_html}
    </div>
    <div class="logo">{logo_text}<span class="sublogo">{sublogo_text}</span></div>
  </div>
</body>
</html>'''

def classify(line):
    u=line.strip()
    if not u:
        return None
    letters=[c for c in u if c.isalpha()]
    if letters and u.upper()==u and len(u) <= 18:
        return 'big'
    return 'mid' if len(u) > 36 else 'small'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--title', default='Editable Canva Sign')
    ap.add_argument('--size-cm', type=float, default=7.0)
    ap.add_argument('--logo-text', default='VITAL SLIM')
    ap.add_argument('--sublogo-text', default='INSTITUTO')
    ap.add_argument('--bg', default='#f7f4ee')
    ap.add_argument('--text', default='#6d645c')
    ap.add_argument('--big', default='#6a5d50')
    ap.add_argument('--border', default='#b9afa4')
    ap.add_argument('--logo-color', default='#b3924c')
    ap.add_argument('--sublogo-color', default='#8c847b')
    ap.add_argument('--lines-json', required=True, help='JSON array of text lines in order')
    ap.add_argument('--out', required=True)
    args=ap.parse_args()

    lines=json.loads(args.lines_json)
    blocks=[]
    for line in lines:
        kind=classify(line)
        if not kind:
            continue
        blocks.append(f'<div class="{kind}">{html.escape(line)}</div>')
    content='\n      '.join(blocks)
    out=TEMPLATE.format(
        title=html.escape(args.title),
        size_cm=args.size_cm,
        bg=args.bg,
        text=args.text,
        big=args.big,
        border=args.border,
        logo=args.logo_color,
        sublogo=args.sublogo_color,
        content_html=content,
        logo_text=html.escape(args.logo_text),
        sublogo_text=html.escape(args.sublogo_text),
    )
    pathlib.Path(args.out).write_text(out, encoding='utf-8')

if __name__ == '__main__':
    main()

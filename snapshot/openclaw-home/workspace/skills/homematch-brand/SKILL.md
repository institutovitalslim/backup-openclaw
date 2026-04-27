---
name: homematch-brand
version: 1.0.0
description: Brand identity toolkit for HomeMatch Club — generates logos, app icons, and brand assets following the luxury hospitality aesthetic (Fasano, Aman, Soho House inspired). Uses SVG code for precision, never image generation APIs for typography.
metadata:
  openclaw:
    requires: { bins: ["convert", "rsvg-convert"] }
---

# HomeMatch Club — Brand Identity Toolkit

## Core Principles
1. **SVG only** — logos are code, not pixels
2. **Real fonts** — use system serif fonts (Times New Roman, Georgia) for HM monogram
3. **Simple & clean** — no gradients, no shadows, no effects
4. **Luxury palette** — black (#0A0A0A), cream (#F5F0E8), gold (#C9A96E)
5. **Test before sending** — always check 120x120 app icon size

## Logo Types

### App Icon (1024x1024)
- Just HM monogram
- Centered, bold, serif
- No text below
- Test at 120x120

### Full Logo (1024x1024)
- HM monogram + "HOMEMATCH CLUB"
- Elegant line separator
- For splash screens and large formats

### Social Media
- Circular version with border
- Square version for Instagram

## Workflow
1. Generate SVG with precise coordinates
2. Convert to PNG with `convert -background none -density 300`
3. Test at 120x120 with `convert -resize 120x120`
4. If legible → save to deliverables/homematch-app/logos/
5. If not → iterate SVG coordinates

## Anti-Patterns (NEVER)
- Never use image generation APIs for typography
- Never use stroke-only SVGs (they disappear on resize)
- Never add gradients or shadows
- Never send without testing at app icon size

## Example Commands
```bash
# Generate SVG
write /tmp/logo.svg '<svg>...</svg>'

# Convert to PNG
convert -background none -density 300 /tmp/logo.svg /tmp/logo.png

# Test app icon size
convert /tmp/logo.png -resize 120x120 /tmp/test-120.png
```

---
name: canva-recreate-editable
description: Recreate reference artworks as editable Canva designs with live text layers instead of flattened images. Use when the user wants a Canva piece recreated faithfully from a reference, especially when the generated Canva design comes back as an image, when text must stay editable, when a brand kit/logo should be applied, or when Canva access/auth must be fixed before continuing.
---

# canva-recreate-editable

Use this skill to recreate a reference piece in Canva while preserving **editable text**.

## Core rule

Do **not** stop at the first Canva failure.

If Canva is unavailable because of auth, scope, or connector issues:
1. diagnose the real blocker
2. fix access first when possible
3. only then continue the design task

## Workflow

### 1) Confirm Canva access first

Use `mcporter list --output json`.

- If `canva` is in `auth` state, run `mcporter auth canva`, then re-check.
- If a tool reports missing scopes, reconnect/auth again before giving up.
- If access is healthy, continue.

### 2) Prefer native Canva generation first

Use the Canva MCP `generate-design` tool with:
- `design_type` explicitly set
- `brand_kit_id` when the user wants brand consistency
- a detailed prompt describing the exact layout, hierarchy, and constraints

Important:
- Always set `design_type`. Omitting it can cause `feature_not_available` / unsupported type errors.
- For square social assets, start with `instagram_post` unless the user clearly wants another preset.

### 3) If Canva generates a flattened image, switch to HTML import

When the user needs **fully editable text**, do not rely on image-based generation.

Instead:
1. build a small HTML file that recreates the layout
2. keep all copy as actual HTML text nodes
3. use CSS for spacing, borders, typography, alignment, and canvas size
4. host the HTML at a public HTTPS URL
5. import it into Canva with `import-design-from-url`

This usually yields a much more editable Canva design than a generated raster-like candidate.

### 4) Preserve the user’s text exactly

When converting a reference into editable HTML:
- keep the wording exactly as requested
- do not rewrite, shorten, “improve”, or normalize copy unless the user explicitly asks
- only add brand/logo and layout adaptations requested by the user

### 5) Deliver both links

After creation/import, return:
- editable link
- view link
- one-line status of what path worked (`generate-design` vs `HTML import`)

## Recommended Canva prompt pattern

Use a prompt with these parts:
- asset type and size intent
- brand kit selection
- exact visual description of the reference
- exact text content
- explicit “no extra icons/photos/decorations” constraints
- explicit typography hierarchy

## HTML import pattern

For HTML-driven recreation:
- use a fixed-size artboard in CSS
- create an inset border when the reference has a frame
- center text with explicit block spacing
- keep logo in a separate bottom block
- prefer safe fonts (`Arial`, `Helvetica`, sans-serif) unless the workflow provides a better web-safe equivalent

Read `references/workflow.md` when you need the exact command sequence.
Use `scripts/make_editable_sign_html.py` to generate a quick editable HTML plaque/sign from structured text.

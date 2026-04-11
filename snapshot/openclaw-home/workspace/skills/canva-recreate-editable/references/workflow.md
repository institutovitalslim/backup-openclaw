# Canva editable recreation workflow

## Access check

```bash
mcporter list --output json
mcporter auth canva
```

## Brand kit lookup

```bash
mcporter call canva.list-brand-kits --args '{"user_intent":"Find the correct brand kit for the requested design"}' --output json
```

## Native generation attempt

Always include `design_type`.

Example:

```bash
mcporter call canva.generate-design --args '{
  "design_type":"instagram_post",
  "brand_kit_id":"<brand-kit-id>",
  "user_intent":"Create a branded editable social design",
  "query":"<detailed design prompt>"
}' --output json
```

If generation succeeds and returns candidates, convert the selected candidate:

```bash
mcporter call canva.create-design-from-candidate --args '{
  "job_id":"<job-id>",
  "candidate_id":"<candidate-id>",
  "user_intent":"Create editable Canva design from candidate"
}' --output json
```

## HTML fallback for editable text

1. Generate local HTML with `scripts/make_editable_sign_html.py`
2. Upload HTML to a public HTTPS paste/file host
3. Import into Canva:

```bash
mcporter call canva.import-design-from-url --args '{
  "url":"<public-https-url>",
  "name":"<design-name>",
  "user_intent":"Import editable HTML-based design into Canva"
}' --output json
```

## Notes

- `generate-design` can succeed but still produce a visually flattened result.
- If the user explicitly says “I want it editable as text”, prefer HTML import quickly instead of arguing with the output.
- If a connector issue appears, fix that first before reporting failure.

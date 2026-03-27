#!/usr/bin/env python3
import json
import subprocess

result = subprocess.run([
    "op", "item", "get", "Z-API WhatsApp Credentials", "--format", "json"
], capture_output=True, text=True, check=True)
data = json.loads(result.stdout)
print("Sections/fields (label -> id):")
for section in data.get("sections", []):
    for field in section.get("fields", []):
        label = field.get("label")
        fid = field.get("id")
        print(f" - {section.get('label')} / {label} (id={fid})")
print("Root fields:")
for field in data.get("fields", []):
    print(f" - {field.get('label')} (id={field.get('id')})")

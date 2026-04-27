#!/usr/bin/env python3
"""md_to_production_html.py v4 — + Kanban + batch recording planner."""
import json
import re
import sys
from pathlib import Path
from datetime import date, datetime, timedelta
from collections import defaultdict


def parse_md(md: str) -> dict:
    data = {"title": "", "source": "", "themes": [], "reels": [], "plan": []}

    m = re.search(r"@([\w.-]+)", md)
    if m:
        data["source"] = f"@{m.group(1)}"

    cluster = re.search(r"## Clusterização.*?(?=## |\Z)", md, re.DOTALL)
    if cluster:
        for line in cluster.group(0).splitlines():
            tm = re.match(r"\s*-\s+\*\*(T\d+)\s*—\s*([^*]+)\*\*\s*\((.+?)\)", line)
            if tm:
                data["themes"].append({"id": tm.group(1), "name": tm.group(2).strip(), "reels_desc": tm.group(3).strip()})

    reel_blocks = re.split(r"(?=^### \[#\d+\])", md, flags=re.MULTILINE)
    for block in reel_blocks:
        m = re.match(r"^### \[#(\d+)\]\s+([\w-]+)\s*—\s*(.+?)\s*\(([^)]+)\)", block)
        if not m:
            continue
        reel = {
            "n": int(m.group(1)),
            "code": m.group(2),
            "title": m.group(3).strip().strip('"'),
            "engagement": m.group(4).strip(),
            "url": "",
            "theme_id": "",
            "why_viral": {"hook": "", "structure": "", "retention": ""},
            "scripts": [],
        }
        url_m = re.search(r"🔗\s+(https?://\S+)", block)
        if url_m:
            reel["url"] = url_m.group(1)

        for key, pat in [
            ("hook", r"\*\*Hook[^:]*:\*\*\s*(.+?)(?=\n\s*-|\n\n)"),
            ("structure", r"\*\*Estrutura[^:]*:\*\*\s*(.+?)(?=\n\s*-|\n\n)"),
            ("retention", r"\*\*Retention driver[^:]*:\*\*\s*(.+?)(?=\n\s*-|\n\n)"),
        ]:
            mm = re.search(pat, block, re.DOTALL)
            if mm:
                reel["why_viral"][key] = mm.group(1).strip()

        script_blocks = re.split(r"(?=^\*\*Script adaptado \d)", block, flags=re.MULTILINE)
        for sb in script_blocks:
            sm = re.match(r"\*\*Script adaptado (\d)\s*—\s*\"?([^\"*]+)\"?\*\*", sb)
            if not sm:
                continue
            script = {"n": int(sm.group(1)), "title": sm.group(2).strip(),
                      "hook": "", "corpo": "", "cta": "", "legenda": "", "hashtags": ""}
            for field, pat in [
                ("hook", r"(?:HOOK[^:]*:|- HOOK[^:]*:)\s*(.+?)(?=\n\s*-\s+(?:CORPO|CTA|\*\*LEGENDA)|\n\*\*|$)"),
                ("corpo", r"(?:CORPO[^:]*:|- CORPO[^:]*:)\s*(.+?)(?=\n\s*-\s+(?:CTA|\*\*LEGENDA)|\n\*\*|$)"),
                ("cta", r"(?:CTA[^:]*:|- CTA[^:]*:)\s*(.+?)(?=\n\s*-\s+\*\*LEGENDA|\n\*\*LEGENDA|$)"),
                ("legenda", r"\*\*LEGENDA:\*\*\s*(.+?)(?=\s*\|\s*\*\*Hashtags|$)"),
                ("hashtags", r"\*\*Hashtags:\*\*\s*(.+?)(?=\n\n|$)"),
            ]:
                mm = re.search(pat, sb, re.DOTALL)
                if mm:
                    text = mm.group(1).strip()
                    text = re.sub(r'\s*\[Dra\. Daniely[^\]]*\]\s*', '', text)
                    text = re.sub(r'\s+', ' ', text).strip('"').strip()
                    script[field] = text
            reel["scripts"].append(script)

        if reel["scripts"]:
            data["reels"].append(reel)

    # Map reel → theme
    for theme in data["themes"]:
        nums = [int(n) for n in re.findall(r"\d+", theme["reels_desc"])]
        for reel in data["reels"]:
            if reel["n"] in nums:
                reel["theme_id"] = theme["id"]

    plan_m = re.search(r"### Sequenciamento[^\n]*\n\n\|[^\n]+\|\n\|[^\n]+\|\n((?:\|[^\n]+\|\n)+)", md)
    if plan_m:
        for line in plan_m.group(1).splitlines():
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 3:
                data["plan"].append({"week": parts[0], "scripts": parts[1], "theme": parts[2]})

    return data


SLOTS = [
    {"dia_semana": 2, "hora": "19:00", "label": "Quarta 19h"},
    {"dia_semana": 4, "hora": "12:00", "label": "Sexta 12h"},
    {"dia_semana": 6, "hora": "11:00", "label": "Domingo 11h"},
]
DAYS_PT = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom"}


def build_schedule(reels, plan, start_date=None):
    if start_date is None:
        today = date.today()
        days_until_mon = (7 - today.weekday()) % 7 or 7
        start_date = today + timedelta(days=days_until_mon)

    schedule = []
    week_idx = 0
    for p_entry in plan:
        scripts_text = p_entry.get("scripts", "")
        script_refs = re.findall(r"#?(\d+)\.(\d+)", scripts_text)
        for slot_idx, (reel_n, script_n) in enumerate(script_refs[:len(SLOTS)]):
            slot = SLOTS[slot_idx]
            pub_date = start_date + timedelta(weeks=week_idx, days=slot["dia_semana"])
            hook = ""
            title = ""
            theme_id = ""
            for r in reels:
                if r["n"] == int(reel_n):
                    theme_id = r.get("theme_id", "")
                    for s in r["scripts"]:
                        if s["n"] == int(script_n):
                            hook = s["hook"][:120]
                            title = s["title"]
                            break
            schedule.append({
                "data": pub_date.isoformat(),
                "data_br": f"{DAYS_PT[pub_date.weekday()]} {pub_date.strftime('%d/%m')}",
                "hora": slot["hora"],
                "slot_label": slot["label"],
                "script_id": f"s{reel_n}-{script_n}",
                "reel_n": int(reel_n),
                "script_n": int(script_n),
                "hook": hook,
                "title": title,
                "tema": theme_id,
                "tema_desc": p_entry.get("theme", ""),
                "semana": p_entry.get("week", ""),
            })
        week_idx += 1
    return schedule


def build_batch_suggestions(reels, themes, schedule):
    """Sugestoes de batch: agrupa scripts por tema, recomenda sessoes de gravacao."""
    scripts_by_theme = defaultdict(list)
    for reel in reels:
        theme_id = reel.get("theme_id") or "extras"
        for s in reel["scripts"]:
            scripts_by_theme[theme_id].append({
                "script_id": f"s{reel['n']}-{s['n']}",
                "reel_n": reel["n"],
                "script_n": s["n"],
                "title": s["title"],
                "hook": s["hook"][:90],
                "theme_id": theme_id,
            })

    theme_name_map = {t["id"]: t["name"] for t in themes}

    batches = []
    for tid, items in scripts_by_theme.items():
        if not items:
            continue
        n = len(items)
        # Sugestao de duracao: ~5min por script gravado (considerando retakes)
        min_per_script = 6
        total_min = n * min_per_script
        # Sugerir 1 sessao se <= 12 scripts, 2 sessoes se mais
        if n <= 12:
            sessions = [{"label": "Sessão única", "scripts": items, "duracao": total_min}]
        else:
            mid = (n + 1) // 2
            sessions = [
                {"label": "Sessão 1/2", "scripts": items[:mid], "duracao": mid * min_per_script},
                {"label": "Sessão 2/2", "scripts": items[mid:], "duracao": (n - mid) * min_per_script},
            ]
        batches.append({
            "theme_id": tid,
            "theme_name": theme_name_map.get(tid, tid),
            "total_scripts": n,
            "total_min_estimated": total_min,
            "sessions": sessions,
        })
    return batches


CSS = """
:root {
  /* Color tokens */
  --c-ink: #1a1a1a;
  --c-ink-soft: #2a2a2a;
  --c-ink-muted: #3a3a3a;
  --c-gold: #c9a24e;
  --c-gold-deep: #8b6914;
  --c-gold-hover: #b08a3e;
  --c-cream-bg: #f4f2ec;
  --c-cream-soft: #faf7ee;
  --c-cream-card: #fafaf7;
  --c-surface: #ffffff;
  --c-border: #e0d7bd;
  --c-border-soft: #e8e5dc;
  --c-border-neutral: #dcdcdc;
  --c-text: #1a1a1a;
  --c-text-muted: #5a5a5a;   /* was #666, darker for AA */
  --c-text-dim: #6f6f6f;
  --c-success: #1f6a38;      /* darker green for AA on white */
  --c-success-bg: #e8f4ee;
  --c-danger: #8a3838;
  --c-danger-hover: #6f2a2a;

  /* Type scale (1.125 modular) */
  --t-xs: 11px;
  --t-sm: 12px;
  --t-base: 13px;
  --t-md: 14px;
  --t-lg: 16px;
  --t-xl: 18px;
  --t-2xl: 22px;
  --t-3xl: 28px;
  --t-hero: 34px;

  /* Spacing scale (4pt grid) */
  --s-1: 4px;
  --s-2: 8px;
  --s-3: 12px;
  --s-4: 16px;
  --s-5: 20px;
  --s-6: 24px;
  --s-7: 32px;
  --s-8: 48px;

  /* Radius */
  --r-sm: 4px;
  --r-md: 6px;
  --r-lg: 8px;
  --r-pill: 999px;

  /* Shadow */
  --sh-1: 0 1px 2px rgba(0,0,0,0.04);
  --sh-2: 0 2px 6px rgba(0,0,0,0.06);
  --sh-3: 0 8px 20px rgba(0,0,0,0.10);

  /* Motion */
  --dur-fast: 120ms;
  --dur: 180ms;
  --ease: cubic-bezier(.4,0,.2,1);

  /* Layout */
  --header-h: 64px;
  --themenav-h: 54px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; scroll-padding-top: calc(var(--header-h) + var(--themenav-h) + 8px); }
body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-feature-settings: "ss01","cv11","tnum";
  line-height: 1.55;
  color: var(--c-text);
  background: var(--c-cream-bg);
  padding-bottom: 100px;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
.hidden-copy { position: absolute; left: -9999px; opacity: 0; height: 0; width: 0; }

/* Accessibility: visible keyboard focus on all interactive elements */
button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
[tabindex]:focus-visible {
  outline: 2px solid var(--c-gold);
  outline-offset: 2px;
  border-radius: var(--r-sm);
}

/* Skip link for screen readers */
.skip-link {
  position: absolute; left: -9999px; top: 0;
  background: var(--c-ink); color: var(--c-gold); padding: var(--s-3) var(--s-4);
  z-index: 1000; font-weight: 700;
}
.skip-link:focus { left: var(--s-3); top: var(--s-3); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

header.top {
  position: sticky; top: 0; z-index: 50;
  background: var(--c-ink); color: #fff;
  padding: var(--s-4) var(--s-6);
  border-bottom: 3px solid var(--c-gold);
  box-shadow: var(--sh-2);
}
header.top h1 {
  font-size: var(--t-lg); font-weight: 600; letter-spacing: -0.01em;
  display: flex; justify-content: space-between; align-items: center;
  gap: var(--s-3); flex-wrap: wrap;
}
.status-badge {
  background: var(--c-success); color: #fff;
  padding: 3px var(--s-3); border-radius: var(--r-sm);
  font-size: var(--t-xs); font-weight: 700; letter-spacing: 0.6px;
}
.toolbar { display: flex; gap: var(--s-2); flex-wrap: wrap; margin-top: var(--s-2); }
.toolbar button {
  background: var(--c-ink-soft); color: #fff; border: 1px solid #444;
  padding: 6px var(--s-3); border-radius: var(--r-sm);
  font-size: var(--t-sm); cursor: pointer;
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease), border-color var(--dur) var(--ease);
}
.toolbar button:hover { background: var(--c-gold); color: var(--c-ink); border-color: var(--c-gold); }

main { max-width: 1240px; margin: 0 auto; padding: var(--s-6) var(--s-5); }

.meta-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--s-4); margin: var(--s-4) 0 var(--s-6);
}
.meta-card {
  background: var(--c-surface); padding: var(--s-4);
  border-radius: var(--r-md); box-shadow: var(--sh-1);
  border-left: 3px solid var(--c-gold);
}
.meta-card strong {
  font-size: var(--t-2xl); color: var(--c-ink); display: block;
  font-variant-numeric: tabular-nums; letter-spacing: -0.01em;
}
.meta-card small { color: var(--c-text-muted); font-size: var(--t-sm); }

.theme-nav {
  display: flex; gap: var(--s-2); flex-wrap: wrap;
  margin: var(--s-4) 0; position: sticky; top: var(--header-h);
  background: var(--c-cream-bg); padding: var(--s-3) 0;
  z-index: 40; border-bottom: 1px solid #e5e5e5;
}
.chip {
  background: var(--c-surface); border: 1px solid var(--c-border-neutral);
  padding: var(--s-2) var(--s-4); border-radius: var(--r-pill);
  font-size: var(--t-base); cursor: pointer;
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease), border-color var(--dur) var(--ease);
}
.chip:hover { background: var(--c-gold); color: var(--c-ink); border-color: var(--c-gold); }
.chip.active { background: var(--c-ink); color: #fff; border-color: var(--c-ink); }

.calendar {
  background: var(--c-surface); border-radius: var(--r-lg);
  padding: var(--s-6); margin-bottom: var(--s-6); box-shadow: var(--sh-2);
}
.calendar h2 {
  font-size: var(--t-xl); letter-spacing: -0.01em; margin-bottom: var(--s-4);
  border-bottom: 2px solid var(--c-gold); padding-bottom: var(--s-2);
}
.cal-note {
  font-size: var(--t-base); color: var(--c-text-muted);
  margin-bottom: var(--s-4); padding: var(--s-3) var(--s-4);
  background: var(--c-cream-soft); border-radius: var(--r-md);
  border-left: 3px solid var(--c-gold);
}

.batch-suggest { margin-bottom: var(--s-5); }
.batch-suggest h3 {
  font-size: var(--t-md); color: var(--c-ink); margin-bottom: var(--s-3);
  padding: var(--s-2) var(--s-3); background: var(--c-cream-soft);
  border-left: 3px solid var(--c-gold); border-radius: 0 var(--r-sm) var(--r-sm) 0;
}
.batch-sessions {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: var(--s-3);
}
.batch-session {
  background: var(--c-cream-card); border: 1px solid var(--c-border);
  padding: var(--s-4); border-radius: var(--r-md);
}
.batch-header {
  display: flex; justify-content: space-between; margin-bottom: var(--s-3);
  align-items: center; gap: var(--s-2); flex-wrap: wrap;
}
.batch-label { font-weight: 700; color: var(--c-gold-deep); font-size: var(--t-base); }
.batch-meta { font-size: var(--t-sm); color: var(--c-text-muted); font-variant-numeric: tabular-nums; }
.batch-scripts { display: flex; flex-direction: column; gap: var(--s-2); margin-top: var(--s-3); }
.batch-script-item {
  display: flex; align-items: center; gap: var(--s-2);
  padding: 6px var(--s-3); background: var(--c-surface);
  border-radius: var(--r-sm); border-left: 2px solid var(--c-gold);
  font-size: var(--t-base);
}
.batch-script-item input[type=checkbox] { cursor: pointer; width: 16px; height: 16px; accent-color: var(--c-gold-deep); }
.batch-actions { display: flex; gap: var(--s-2); flex-wrap: wrap; margin-top: var(--s-3); }
.batch-date-input {
  padding: var(--s-2) var(--s-3); border: 1px solid var(--c-border-neutral);
  border-radius: var(--r-sm); font-size: var(--t-base); font-family: inherit;
}
.btn-schedule {
  background: var(--c-gold); color: var(--c-ink); border: none;
  padding: var(--s-2) var(--s-4); border-radius: var(--r-sm);
  font-weight: 700; cursor: pointer; font-size: var(--t-base);
  transition: background var(--dur) var(--ease), transform var(--dur-fast) var(--ease);
}
.btn-schedule:hover { background: var(--c-gold-hover); }
.btn-schedule:active { transform: translateY(1px); }

.kanban-wrap { overflow-x: auto; padding-bottom: var(--s-3); }
.kanban {
  display: grid; grid-template-columns: repeat(5, minmax(220px, 1fr));
  gap: var(--s-3); min-width: 1100px;
}
.kanban-col {
  background: #f0ede4; border-radius: var(--r-md);
  padding: var(--s-3); min-height: 200px;
  transition: background var(--dur) var(--ease), border-color var(--dur) var(--ease);
  border: 2px solid transparent;
}
.kanban-col.drag-over { background: var(--c-cream-soft); border-color: var(--c-gold); border-style: dashed; }
.kanban-col h3 {
  font-size: var(--t-sm); text-transform: uppercase; letter-spacing: 0.8px;
  color: var(--c-ink); margin-bottom: var(--s-3);
  padding: 6px var(--s-3); background: var(--c-surface);
  border-radius: var(--r-sm); border-left: 3px solid var(--c-gold);
}
.kanban-col h3 .count {
  background: var(--c-ink); color: var(--c-gold);
  padding: 2px var(--s-2); border-radius: 10px;
  font-size: var(--t-xs); margin-left: 6px; font-weight: 700;
  font-variant-numeric: tabular-nums;
}
.kanban-card {
  background: var(--c-surface); border: 1px solid var(--c-border);
  padding: var(--s-3); border-radius: 5px; margin-bottom: var(--s-2);
  cursor: grab; font-size: var(--t-base); box-shadow: var(--sh-1);
  transition: box-shadow var(--dur) var(--ease), transform var(--dur) var(--ease);
}
.kanban-card:hover { box-shadow: var(--sh-2); transform: translateY(-1px); }
.kanban-card.dragging { opacity: 0.4; cursor: grabbing; }
.kanban-card .k-num {
  background: var(--c-ink); color: var(--c-gold);
  padding: 2px 6px; border-radius: 3px;
  font-family: "SF Mono", ui-monospace, "Cascadia Code", Consolas, monospace;
  font-size: var(--t-xs); font-weight: 700;
  display: inline-block; margin-bottom: var(--s-1);
  font-variant-numeric: tabular-nums;
}
.kanban-card .k-tema {
  background: var(--c-cream-soft); color: var(--c-gold-deep);
  padding: 2px 6px; border-radius: 3px;
  font-size: 10.5px; font-weight: 700;
  display: inline-block; margin-left: var(--s-1);
}
.kanban-card .k-title { font-weight: 600; font-size: var(--t-md); color: var(--c-ink); margin: var(--s-1) 0; line-height: 1.3; }
.kanban-card .k-hook { font-size: var(--t-sm); color: var(--c-text-muted); line-height: 1.4; margin-top: var(--s-1); font-style: italic; }
.kanban-card .k-date {
  font-size: var(--t-xs); color: var(--c-gold-deep); font-weight: 600;
  margin-top: 6px; padding: 3px 6px; background: var(--c-cream-soft);
  border-radius: 3px; display: inline-block; font-variant-numeric: tabular-nums;
}
.kanban-card .k-actions { margin-top: var(--s-2); display: flex; gap: var(--s-1); flex-wrap: wrap; }
.kanban-card .k-actions button {
  padding: 3px var(--s-2); font-size: 10.5px; border: none;
  border-radius: 3px; cursor: pointer;
  background: #f0ede4; color: var(--c-ink);
  transition: background var(--dur-fast) var(--ease);
}
.kanban-card .k-actions button:hover { background: var(--c-gold); }
.kanban-card .k-actions .k-open { background: var(--c-ink); color: var(--c-gold); }
.kanban-card input.k-date-input {
  padding: 3px 6px; font-size: var(--t-xs);
  border: 1px solid var(--c-border-neutral); border-radius: 3px;
  width: 100%; margin-top: var(--s-1);
}

.reel-card {
  background: var(--c-surface); border-radius: var(--r-lg);
  padding: var(--s-6); margin-bottom: var(--s-5); box-shadow: var(--sh-2);
}
.reel-card h2 {
  font-size: var(--t-xl); color: var(--c-ink); margin-bottom: var(--s-2);
  border-bottom: 2px solid var(--c-gold); padding-bottom: var(--s-2);
  letter-spacing: -0.01em;
}
.reel-meta { display: flex; gap: var(--s-4); font-size: var(--t-base); color: var(--c-text-muted); margin-bottom: var(--s-4); flex-wrap: wrap; }
.reel-meta a { color: var(--c-gold-deep); text-decoration: none; font-weight: 600; }
.reel-meta a:hover { text-decoration: underline; }
.eng { background: var(--c-cream-soft); padding: 2px var(--s-3); border-radius: var(--r-sm); color: var(--c-gold-deep); font-weight: 600; font-variant-numeric: tabular-nums; }
.viral-analysis { background: var(--c-cream-soft); padding: var(--s-3) var(--s-4); border-radius: var(--r-md); margin-bottom: var(--s-4); font-size: var(--t-md); }
.viral-analysis summary { cursor: pointer; font-weight: 600; color: var(--c-gold-deep); }
.viral-analysis p { margin-top: var(--s-2); }
.script-card { background: var(--c-cream-card); border: 1px solid var(--c-border-soft); border-radius: var(--r-md); padding: var(--s-4); margin-top: var(--s-4); }
.script-header { display: flex; justify-content: space-between; align-items: center; gap: var(--s-3); margin-bottom: var(--s-4); flex-wrap: wrap; }
.script-num {
  background: var(--c-ink); color: var(--c-gold);
  padding: var(--s-1) var(--s-2); border-radius: var(--r-sm);
  font-weight: 700; font-size: var(--t-base);
  font-family: "SF Mono", ui-monospace, "Cascadia Code", Consolas, monospace;
  font-variant-numeric: tabular-nums;
}
.script-title { font-weight: 600; font-size: var(--t-md); color: var(--c-ink); flex: 1; line-height: 1.3; }
.script-status {
  font-size: var(--t-sm); color: var(--c-ink-muted);  /* was #888 — AA fix */
  padding: var(--s-1) var(--s-2);
  background: #ebebeb;                                 /* was #f0f0f0 — AA fix */
  border-radius: var(--r-sm); font-weight: 600;
}
.block-group {
  margin-bottom: var(--s-4); border: 1px solid var(--c-border);
  border-radius: var(--r-md); overflow: hidden; background: var(--c-surface);
}
.block-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: var(--s-3) var(--s-4); background: var(--c-cream-soft);
  border-bottom: 1px solid var(--c-border); gap: var(--s-3); flex-wrap: wrap;
}
.block-header label {
  font-weight: 700; font-size: var(--t-base);
  color: var(--c-gold-deep); text-transform: uppercase; letter-spacing: 0.5px;
}
.btn-copy-block {
  background: var(--c-gold); color: var(--c-ink); border: none;
  padding: var(--s-2) var(--s-4); border-radius: var(--r-sm);
  font-weight: 700; font-size: var(--t-base); cursor: pointer;
  transition: background var(--dur) var(--ease), transform var(--dur-fast) var(--ease);
}
.btn-copy-block:hover { background: var(--c-gold-hover); transform: scale(1.03); }
.btn-copy-block.copied { background: var(--c-success); color: #fff; }
.block-body { padding: var(--s-4); }
.block-sub { margin-bottom: var(--s-3); }
.block-sub:last-child { margin-bottom: 0; }
.block-sub .tag {
  display: inline-block; background: var(--c-ink); color: var(--c-gold);
  padding: 2px var(--s-2); border-radius: 3px; font-size: 10.5px;
  font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px;
  margin-bottom: 5px;
}
.block-sub p {
  font-size: var(--t-md); line-height: 1.6; color: var(--c-ink);
  padding: var(--s-2) var(--s-3); background: var(--c-cream-card);
  border-left: 3px solid var(--c-gold); border-radius: 0 var(--r-sm) var(--r-sm) 0;
}
.script-actions { display: flex; gap: var(--s-2); flex-wrap: wrap; margin-top: var(--s-3); padding-top: var(--s-3); border-top: 1px solid var(--c-border-soft); }
.btn-big {
  padding: var(--s-3) var(--s-4); border: none; border-radius: var(--r-sm);
  cursor: pointer; font-size: var(--t-base); font-weight: 600;
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease), transform var(--dur-fast) var(--ease);
}
.btn-big:active { transform: translateY(1px); }
.btn-teleprompter { background: var(--c-ink); color: var(--c-gold); }
.btn-teleprompter:hover { background: var(--c-gold); color: var(--c-ink); }
.btn-share { background: #25D366; color: #fff; }
.btn-share:hover { background: #1da851; }
.status-select {
  padding: 9px var(--s-3); border: 1px solid var(--c-border-neutral);
  border-radius: var(--r-sm); background: var(--c-surface);
  font-size: var(--t-base); cursor: pointer; font-family: inherit;
}

.month-cal { background: var(--c-surface); padding: var(--s-5); border-radius: var(--r-md); }
.month-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: var(--s-4); padding-bottom: var(--s-3);
  border-bottom: 1px solid #eee;
}
.month-nav { display: flex; gap: var(--s-2); align-items: center; }
.month-nav button {
  background: var(--c-ink); color: var(--c-gold); border: none;
  padding: var(--s-2) var(--s-4); border-radius: var(--r-sm);
  cursor: pointer; font-weight: 700; font-size: var(--t-base);
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease);
}
.month-nav button:hover { background: var(--c-gold); color: var(--c-ink); }
.month-title { font-size: var(--t-xl); font-weight: 700; color: var(--c-ink); letter-spacing: -0.01em; font-variant-numeric: tabular-nums; }
.month-legend { display: flex; gap: var(--s-4); font-size: var(--t-sm); color: var(--c-text-muted); margin-bottom: var(--s-3); flex-wrap: wrap; }
.month-legend span b { color: var(--c-ink); }
.month-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: var(--s-1); }
.month-dow {
  text-align: center; padding: var(--s-2);
  font-size: var(--t-xs); font-weight: 700;
  color: var(--c-gold-deep); text-transform: uppercase; letter-spacing: 0.8px;
}
.month-cell {
  background: var(--c-cream-card); border: 1px solid var(--c-border-soft);
  border-radius: var(--r-sm); min-height: 90px;
  padding: 6px var(--s-2); cursor: pointer;
  transition: background var(--dur) var(--ease), border-color var(--dur) var(--ease);
  position: relative;
}
.month-cell:hover { background: var(--c-cream-soft); border-color: var(--c-gold); }
.month-cell.other-month { background: #f0ede4; opacity: 0.45; }
.month-cell.today { border: 2px solid var(--c-gold); background: var(--c-cream-soft); }
.month-cell.has-events { background: var(--c-surface); }
.month-cell .day-num { font-size: var(--t-base); font-weight: 700; color: var(--c-ink); margin-bottom: var(--s-1); font-variant-numeric: tabular-nums; }
.month-cell .day-badges { display: flex; flex-direction: column; gap: 3px; }
.month-cell .badge-rec {
  background: var(--c-cream-soft); color: var(--c-gold-deep);
  padding: 2px 5px; border-radius: 3px; font-size: 10px;
  font-weight: 600; border-left: 2px solid var(--c-gold);
}
.month-cell .badge-pub {
  background: var(--c-success-bg); color: var(--c-success);
  padding: 2px 5px; border-radius: 3px; font-size: 10px;
  font-weight: 600; border-left: 2px solid var(--c-success);
}
.day-details {
  background: var(--c-cream-soft); border: 1px solid var(--c-gold);
  border-radius: var(--r-md); padding: var(--s-4); margin-top: var(--s-4);
}
.day-details.hidden { display: none; }
.day-details h4 { font-size: var(--t-md); color: var(--c-gold-deep); margin-bottom: var(--s-3); text-transform: uppercase; letter-spacing: 0.6px; }
.day-details ul { list-style: none; padding: 0; margin: 0; }
.day-details li {
  padding: var(--s-2) var(--s-3); background: var(--c-surface);
  border-left: 3px solid var(--c-gold);
  border-radius: 0 var(--r-sm) var(--r-sm) 0;
  margin-bottom: 6px; font-size: var(--t-base);
}
.day-details li.pub { border-left-color: var(--c-success); }
.day-details li a { color: var(--c-gold-deep); font-weight: 600; text-decoration: none; font-size: var(--t-sm); margin-left: var(--s-2); }
.day-details li a:hover { text-decoration: underline; }

.btn-unschedule {
  background: var(--c-danger); color: #fff; border: none;
  padding: 3px var(--s-2); font-size: 10.5px; border-radius: 3px;
  cursor: pointer; margin-top: var(--s-1);
  transition: background var(--dur) var(--ease);
}
.btn-unschedule:hover { background: var(--c-danger-hover); }
.btn-unschedule-all {
  background: var(--c-danger); color: #fff; border: none;
  padding: var(--s-2) var(--s-4); border-radius: var(--r-sm);
  font-weight: 700; font-size: var(--t-sm); cursor: pointer;
  transition: background var(--dur) var(--ease);
}
.btn-unschedule-all:hover { background: var(--c-danger-hover); }

.pub-week { margin-bottom: var(--s-5); }
.pub-week h3 {
  font-size: var(--t-md); color: var(--c-ink); margin-bottom: var(--s-3);
  padding: 6px var(--s-3); background: var(--c-cream-soft);
  border-left: 3px solid var(--c-gold); border-radius: 0 var(--r-sm) var(--r-sm) 0;
}
.pub-slots { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--s-3); }
.pub-slot {
  background: linear-gradient(135deg, var(--c-surface) 0%, var(--c-cream-card) 100%);
  border: 1px solid var(--c-border); padding: var(--s-4); border-radius: var(--r-md);
  transition: box-shadow var(--dur) var(--ease), transform var(--dur) var(--ease);
}
.pub-slot:hover { box-shadow: var(--sh-2); transform: translateY(-1px); }
.pub-when { font-size: var(--t-md); color: var(--c-ink); margin-bottom: 6px; font-variant-numeric: tabular-nums; }
.pub-when b { color: var(--c-gold-deep); font-size: var(--t-lg); }
.pub-title { font-size: var(--t-base); color: var(--c-ink-muted); line-height: 1.4; margin-bottom: var(--s-2); }
.pub-link { font-size: var(--t-sm); color: var(--c-gold-deep); text-decoration: none; font-weight: 600; }
.pub-link:hover { text-decoration: underline; }

.tele-modal {
  display: none; position: fixed; inset: 0;
  background: #000; z-index: 1000; padding: var(--s-8) var(--s-5); overflow-y: auto;
}
.tele-modal.show { display: flex; flex-direction: column; align-items: center; justify-content: flex-start; }
.tele-modal .tele-text {
  color: #fff; font-size: var(--t-hero); line-height: 1.5;
  max-width: 900px; text-align: center; font-weight: 400;
  padding: var(--s-8) var(--s-5); white-space: pre-wrap;
}
.tele-modal .tele-close {
  position: fixed; top: var(--s-5); right: var(--s-5);
  background: var(--c-gold); color: var(--c-ink); border: none;
  padding: var(--s-3) var(--s-5); border-radius: var(--r-sm);
  font-size: var(--t-md); cursor: pointer; font-weight: 700;
}
.tele-modal .tele-size {
  position: fixed; bottom: var(--s-5); right: var(--s-5);
  background: var(--c-ink-soft); color: #fff; border: 1px solid #555;
  padding: var(--s-2) var(--s-4); border-radius: var(--r-sm);
  font-size: var(--t-base); cursor: pointer;
}

.toast {
  position: fixed; bottom: var(--s-5); left: 50%;
  transform: translateX(-50%); background: var(--c-success); color: #fff;
  padding: var(--s-3) var(--s-6); border-radius: var(--r-md);
  font-weight: 600; z-index: 500; opacity: 0;
  transition: opacity 0.3s var(--ease);
  pointer-events: none; box-shadow: var(--sh-3);
}
.toast.show { opacity: 1; }

@media print {
  header.top, .theme-nav, .toolbar, .btn-big, .btn-copy-block, .script-actions, .tele-modal, .kanban-wrap { display: none !important; }
  body { background: #fff; padding: 0; }
  main { max-width: 100%; padding: var(--s-3); }
  .reel-card, .calendar { box-shadow: none; border: 1px solid #ddd; break-inside: avoid; }
}

/* Mobile: kanban stacks vertically instead of horizontal scroll */
@media (max-width: 900px) {
  .kanban-wrap { overflow-x: visible; padding-bottom: 0; }
  .kanban { grid-template-columns: 1fr; min-width: 0; }
  .kanban-col { min-height: auto; }
  main { padding: var(--s-4) var(--s-3); }
  .meta-grid { gap: var(--s-3); }
  .calendar { padding: var(--s-4); }
  .reel-card { padding: var(--s-4); }
}
@media (max-width: 560px) {
  .toolbar { gap: 6px; }
  .toolbar button { padding: 5px 10px; font-size: var(--t-xs); }
  .script-header { flex-direction: column; align-items: flex-start; }
  .block-header { flex-direction: column; align-items: flex-start; }
  .btn-copy-block { width: 100%; text-align: center; }
}
"""


JS = """
const STORAGE_KEY = "ivs-prod-status-" + location.pathname;
const DATE_KEY = "ivs-prod-dates-" + location.pathname;

// Status columns mapping
const STATUS_COLS = {
  "aguardando": "col-aguardando",
  "para_gravar": "col-gravar",
  "gravado": "col-edicao",
  "editado": "col-pronto",
  "agendado": "col-postar",
  "postado": "col-postar"
};
const COL_TO_STATUS = {
  "col-aguardando": "aguardando",
  "col-gravar": "para_gravar",
  "col-edicao": "gravado",
  "col-pronto": "editado",
  "col-postar": "agendado"
};

document.querySelectorAll(".btn-copy-block").forEach(btn => {
  btn.addEventListener("click", () => {
    const target = document.getElementById(btn.dataset.target);
    if (!target) return;
    navigator.clipboard.writeText(target.value).then(() => {
      const orig = btn.textContent;
      btn.textContent = "✓ Copiado";
      btn.classList.add("copied");
      showToast("Bloco copiado");
      setTimeout(() => { btn.textContent = orig; btn.classList.remove("copied"); }, 1800);
    }).catch(() => showToast("Erro ao copiar"));
  });
});
document.querySelectorAll(".btn-teleprompter").forEach(btn => {
  btn.addEventListener("click", () => {
    const ta = document.getElementById(btn.dataset.id + "-roteiro");
    document.getElementById("tele-text").textContent = ta.value;
    document.getElementById("tele-modal").classList.add("show");
  });
});
function closeTele() { document.getElementById("tele-modal").classList.remove("show"); }
document.addEventListener("keydown", e => { if (e.key === "Escape") closeTele(); });
function toggleTeleSize() {
  const el = document.getElementById("tele-text");
  const cur = parseInt(getComputedStyle(el).fontSize);
  el.style.fontSize = (cur >= 60 ? 28 : cur + 8) + "px";
}
document.querySelectorAll(".btn-share").forEach(btn => {
  btn.addEventListener("click", () => {
    const ta = document.getElementById(btn.dataset.id + "-roteiro");
    const url = "https://wa.me/?text=" + encodeURIComponent(ta.value);
    window.open(url, "_blank");
  });
});

function getStatusMap() { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); }
function setStatusMap(m) { localStorage.setItem(STORAGE_KEY, JSON.stringify(m)); }
function getDateMap() { return JSON.parse(localStorage.getItem(DATE_KEY) || "{}"); }
function setDateMap(m) { localStorage.setItem(DATE_KEY, JSON.stringify(m)); }

function setScriptStatus(scriptId, status) {
  const m = getStatusMap();
  m[scriptId] = status;
  setStatusMap(m);
  // Update dropdown label if exists
  const sel = document.querySelector("select.status-select[data-key='" + scriptId + "']");
  if (sel) {
    sel.value = status;
    const lbl = document.querySelector(".script-status[data-key='" + scriptId + "']");
    if (lbl) lbl.textContent = sel.options[sel.selectedIndex].text;
  }
  rebuildKanban();
}

function setScriptDate(scriptId, dateStr) {
  const m = getDateMap();
  if (dateStr) m[scriptId] = dateStr;
  else delete m[scriptId];
  setDateMap(m);
  rebuildKanban();
}

function loadStatus() {
  const s = getStatusMap();
  Object.entries(s).forEach(([key, val]) => {
    const sel = document.querySelector("select.status-select[data-key='" + key + "']");
    const lbl = document.querySelector(".script-status[data-key='" + key + "']");
    if (sel) sel.value = val;
    if (lbl && sel) lbl.textContent = sel.options[sel.selectedIndex].text;
  });
}
document.querySelectorAll(".status-select").forEach(sel => {
  sel.addEventListener("change", () => {
    setScriptStatus(sel.dataset.key, sel.value);
    showToast("Status salvo");
  });
});
loadStatus();

// KANBAN
function rebuildKanban() {
  const statusMap = getStatusMap();
  const dateMap = getDateMap();
  const allCards = document.querySelectorAll(".kanban-card");
  const counts = { "col-aguardando": 0, "col-gravar": 0, "col-edicao": 0, "col-pronto": 0, "col-postar": 0 };

  allCards.forEach(card => {
    const scriptId = card.dataset.scriptId;
    const currentStatus = statusMap[scriptId] || "aguardando";
    const targetCol = STATUS_COLS[currentStatus] || "col-aguardando";
    const col = document.getElementById(targetCol);
    if (col && card.parentElement.id !== targetCol) {
      col.appendChild(card);
    }
    counts[targetCol] = (counts[targetCol] || 0) + 1;

    const dateEl = card.querySelector(".k-date");
    const dateInput = card.querySelector(".k-date-input");
    if (dateEl) {
      if (dateMap[scriptId]) {
        dateEl.textContent = "📅 " + formatDate(dateMap[scriptId]);
        dateEl.style.display = "inline-block";
      } else {
        dateEl.style.display = "none";
      }
    }
    if (dateInput) {
      dateInput.value = dateMap[scriptId] || "";
    }
  });

  Object.entries(counts).forEach(([colId, n]) => {
    const span = document.querySelector("#" + colId + " .count");
    if (span) span.textContent = n;
  });
}

function formatDate(iso) {
  try {
    const d = new Date(iso + "T00:00:00");
    const days = ["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"];
    return days[d.getDay()] + " " + String(d.getDate()).padStart(2, "0") + "/" + String(d.getMonth()+1).padStart(2, "0");
  } catch(e) { return iso; }
}

// Drag-and-drop
let dragged = null;
document.addEventListener("dragstart", e => {
  if (e.target.classList && e.target.classList.contains("kanban-card")) {
    dragged = e.target;
    e.target.classList.add("dragging");
    e.dataTransfer.effectAllowed = "move";
  }
});
document.addEventListener("dragend", e => {
  if (e.target.classList && e.target.classList.contains("kanban-card")) {
    e.target.classList.remove("dragging");
  }
});
document.querySelectorAll(".kanban-col").forEach(col => {
  col.addEventListener("dragover", e => { e.preventDefault(); col.classList.add("drag-over"); });
  col.addEventListener("dragleave", () => col.classList.remove("drag-over"));
  col.addEventListener("drop", e => {
    e.preventDefault();
    col.classList.remove("drag-over");
    if (dragged) {
      const newStatus = COL_TO_STATUS[col.id];
      if (newStatus) {
        setScriptStatus(dragged.dataset.scriptId, newStatus);
        showToast("Movido para " + col.querySelector("h3").childNodes[0].textContent.trim());
      }
    }
  });
});

// Kanban card date inputs
document.querySelectorAll(".k-date-input").forEach(inp => {
  inp.addEventListener("change", () => {
    setScriptDate(inp.dataset.scriptId, inp.value);
    if (inp.value && !getStatusMap()[inp.dataset.scriptId]) {
      setScriptStatus(inp.dataset.scriptId, "para_gravar");
    }
    showToast(inp.value ? "Data salva" : "Data removida");
  });
});

// Batch schedule: select all scripts of a session + assign date
document.querySelectorAll(".btn-schedule").forEach(btn => {
  btn.addEventListener("click", () => {
    const sessionEl = btn.closest(".batch-session");
    const dateInput = sessionEl.querySelector(".batch-date-input");
    const dateVal = dateInput.value;
    if (!dateVal) { showToast("Escolhe a data primeiro"); return; }
    const checks = sessionEl.querySelectorAll(".batch-script-item input[type=checkbox]:checked");
    if (!checks.length) { showToast("Marca pelo menos 1 script"); return; }
    checks.forEach(cb => {
      const sid = cb.dataset.scriptId;
      setScriptDate(sid, dateVal);
      setScriptStatus(sid, "para_gravar");
    });
    showToast(checks.length + " scripts agendados para " + formatDate(dateVal));
  });
});

// Select-all in batch session
document.querySelectorAll(".batch-select-all").forEach(btn => {
  btn.addEventListener("click", () => {
    const sessionEl = btn.closest(".batch-session");
    const allChecks = sessionEl.querySelectorAll(".batch-script-item input[type=checkbox]");
    const shouldCheck = Array.from(allChecks).some(c => !c.checked);
    allChecks.forEach(c => c.checked = shouldCheck);
  });
});

// Theme filter
function filterTheme(themeId) {
  document.querySelectorAll(".chip").forEach(c => c.classList.toggle("active", c.dataset.theme === themeId));
  const reelsByTheme = {};
  window.IVS_DATA.themes.forEach(t => {
    const nums = (t.reels_desc.match(/\\d+/g) || []).map(Number);
    reelsByTheme[t.id] = nums;
  });
  document.querySelectorAll(".reel-card").forEach(card => {
    const n = parseInt(card.dataset.reel);
    if (themeId === "ALL") card.style.display = "";
    else card.style.display = (reelsByTheme[themeId] || []).includes(n) ? "" : "none";
  });
}
document.querySelectorAll(".chip[data-theme]").forEach(c => {
  if (c.dataset.theme !== "ALL") c.addEventListener("click", () => filterTheme(c.dataset.theme));
});
function expandAll() { document.querySelectorAll("details").forEach(d => d.open = true); }
function collapseAll() { document.querySelectorAll("details").forEach(d => d.open = false); }
function scrollToSection(id) { document.getElementById(id).scrollIntoView({ behavior: "smooth" }); }
function exportJSON() {
  const status = getStatusMap();
  const dates = getDateMap();
  const exp = Object.assign({}, window.IVS_DATA, { status, dates, exportedAt: new Date().toISOString() });
  const blob = new Blob([JSON.stringify(exp, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "ivs-prod-export-" + Date.now() + ".json";
  a.click();
}
function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(window._toastT);
  window._toastT = setTimeout(() => t.classList.remove("show"), 1800);
}

// Kanban card button actions
function kanbanOpen(scriptId) { document.getElementById(scriptId).scrollIntoView({ behavior: "smooth" }); }
function kanbanMove(scriptId, newStatus) { setScriptStatus(scriptId, newStatus); showToast("Movido"); }



function unscheduleScript(scriptId) {
  setScriptDate(scriptId, null);
  setScriptStatus(scriptId, "aguardando");
  showToast("Script desagendado");
  buildMonthCalendar();
}

// Batch unschedule
document.querySelectorAll(".btn-unschedule-all").forEach(btn => {
  btn.addEventListener("click", () => {
    const sessionEl = btn.closest(".batch-session");
    const checks = sessionEl.querySelectorAll(".batch-script-item input[type=checkbox]:checked");
    if (!checks.length) { showToast("Marca os scripts pra desagendar"); return; }
    checks.forEach(cb => {
      const sid = cb.dataset.scriptId;
      setScriptDate(sid, null);
      setScriptStatus(sid, "aguardando");
    });
    showToast(checks.length + " scripts desagendados");
    buildMonthCalendar();
  });
});

// MONTH CALENDAR
let currentMonth = { year: new Date().getFullYear(), month: new Date().getMonth() };
const MONTHS_PT = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"];
const DOW_PT = ["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"];

function getScheduledPubs() {
  const pubs = {};
  (window.IVS_SCHEDULE || []).forEach(p => {
    pubs[p.data] = pubs[p.data] || [];
    pubs[p.data].push(p);
  });
  return pubs;
}

function getScheduledRecs() {
  const recs = {};
  const dates = getDateMap();
  const allScripts = window.IVS_SCRIPTS || {};
  Object.entries(dates).forEach(([scriptId, dateStr]) => {
    recs[dateStr] = recs[dateStr] || [];
    recs[dateStr].push(Object.assign({ script_id: scriptId }, allScripts[scriptId] || {}));
  });
  return recs;
}

function buildMonthCalendar() {
  const grid = document.getElementById("month-grid");
  const title = document.getElementById("month-title");
  if (!grid || !title) return;
  const { year, month } = currentMonth;
  title.textContent = MONTHS_PT[month] + " " + year;

  const first = new Date(year, month, 1);
  const startDay = first.getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const prevMonthDays = new Date(year, month, 0).getDate();

  const today = new Date();
  const todayStr = today.toISOString().slice(0, 10);
  const pubs = getScheduledPubs();
  const recs = getScheduledRecs();

  grid.innerHTML = "";
  // DOW headers
  DOW_PT.forEach(d => {
    const div = document.createElement("div");
    div.className = "month-dow";
    div.textContent = d;
    grid.appendChild(div);
  });

  // cells (42 = 6 weeks)
  for (let i = 0; i < 42; i++) {
    const dayOffset = i - startDay;
    let cellDate, isOther = false, dayNum;
    if (dayOffset < 0) {
      dayNum = prevMonthDays + dayOffset + 1;
      cellDate = new Date(year, month - 1, dayNum);
      isOther = true;
    } else if (dayOffset >= daysInMonth) {
      dayNum = dayOffset - daysInMonth + 1;
      cellDate = new Date(year, month + 1, dayNum);
      isOther = true;
    } else {
      dayNum = dayOffset + 1;
      cellDate = new Date(year, month, dayNum);
    }
    const iso = cellDate.toISOString().slice(0, 10);
    const cell = document.createElement("div");
    cell.className = "month-cell" + (isOther ? " other-month" : "");
    if (iso === todayStr) cell.classList.add("today");

    const dayEl = document.createElement("div");
    dayEl.className = "day-num";
    dayEl.textContent = dayNum;
    cell.appendChild(dayEl);

    const badges = document.createElement("div");
    badges.className = "day-badges";

    const recList = recs[iso] || [];
    const pubList = pubs[iso] || [];
    if (recList.length) {
      const b = document.createElement("div");
      b.className = "badge-rec";
      b.textContent = "🎬 " + recList.length + " gravar";
      badges.appendChild(b);
      cell.classList.add("has-events");
    }
    if (pubList.length) {
      const b = document.createElement("div");
      b.className = "badge-pub";
      b.textContent = "📤 " + pubList.length + " postar";
      badges.appendChild(b);
      cell.classList.add("has-events");
    }
    cell.appendChild(badges);

    cell.addEventListener("click", () => showDayDetails(iso, cellDate));
    grid.appendChild(cell);
  }
}

function showDayDetails(iso, dateObj) {
  const details = document.getElementById("day-details");
  const recs = getScheduledRecs();
  const pubs = getScheduledPubs();
  const recList = recs[iso] || [];
  const pubList = pubs[iso] || [];
  const dayLabel = DOW_PT[dateObj.getDay()] + " " + String(dateObj.getDate()).padStart(2, "0") + "/" + String(dateObj.getMonth()+1).padStart(2, "0") + "/" + dateObj.getFullYear();
  let html = "<h4>" + dayLabel + "</h4>";
  if (!recList.length && !pubList.length) {
    html += "<p style='color:#888;font-size:13px'>Nenhuma gravação ou publicação agendada para este dia.</p>";
  } else {
    if (recList.length) {
      html += "<h4 style='margin-top:10px'>🎬 Gravações (" + recList.length + ")</h4><ul>";
      recList.forEach(r => {
        html += "<li>" + (r.title || r.script_id) + " <a href='#" + r.script_id + "'>🔍 Abrir roteiro</a></li>";
      });
      html += "</ul>";
    }
    if (pubList.length) {
      html += "<h4 style='margin-top:10px'>📤 Publicações (" + pubList.length + ")</h4><ul>";
      pubList.forEach(p => {
        html += "<li class='pub'>" + p.hora + " · #" + p.reel_n + "." + p.script_n + " — " + p.title + " <a href='#s" + p.reel_n + "-" + p.script_n + "'>🔍 Abrir</a></li>";
      });
      html += "</ul>";
    }
  }
  details.innerHTML = html;
  details.classList.remove("hidden");
}

function monthNav(delta) {
  if (delta === 0) {
    const now = new Date();
    currentMonth = { year: now.getFullYear(), month: now.getMonth() };
  } else {
    let m = currentMonth.month + delta;
    let y = currentMonth.year;
    if (m < 0) { m = 11; y--; }
    if (m > 11) { m = 0; y++; }
    currentMonth = { year: y, month: m };
  }
  buildMonthCalendar();
}

// Build on load
buildMonthCalendar();

// Rebuild month calendar when status/date changes
const origSetScriptStatus = setScriptStatus;
setScriptStatus = function(a, b) { origSetScriptStatus(a, b); buildMonthCalendar(); };
const origSetScriptDate = setScriptDate;
setScriptDate = function(a, b) { origSetScriptDate(a, b); buildMonthCalendar(); };

// Initial kanban build
rebuildKanban();
"""


def render_html(data: dict, title: str) -> str:
    total_scripts = sum(len(r["scripts"]) for r in data["reels"])
    schedule = build_schedule(data["reels"], data["plan"])
    batches = build_batch_suggestions(data["reels"], data["themes"], schedule)

    themes_nav = "".join(
        f'<button class="chip" data-theme="{t["id"]}">{t["id"]} — {t["name"]}</button>'
        for t in data["themes"]
    )

    # BATCH SUGGESTIONS
    batch_parts = []
    for b in batches:
        sessions_html = []
        for sess in b["sessions"]:
            items_html = "".join(
                '<label class="batch-script-item"><input type="checkbox" data-script-id="' + it["script_id"] + '" checked>'
                '<span><b>#' + str(it["reel_n"]) + '.' + str(it["script_n"]) + '</b> — ' + it["title"] + '</span></label>'
                for it in sess["scripts"]
            )
            sessions_html.append(
                '<div class="batch-session">'
                '<div class="batch-header">'
                '<span class="batch-label">' + sess["label"] + '</span>'
                '<span class="batch-meta">' + str(len(sess["scripts"])) + ' scripts · ~' + str(sess["duracao"]) + ' min</span>'
                '</div>'
                '<div class="batch-scripts">' + items_html + '</div>'
                '<div class="batch-actions">'
                '<button class="btn-schedule batch-select-all" type="button">☑️ Selec/Desel tudo</button>'
                '<input type="date" class="batch-date-input">'
                '<button class="btn-schedule">📅 Agendar gravação</button>''<button class="btn-unschedule-all" type="button">🗑️ Limpar datas deste lote</button>'
                '</div>'
                '</div>'
            )
        batch_parts.append(
            '<div class="batch-suggest">'
            '<h3>' + b["theme_id"] + ' — ' + b["theme_name"] + ' (' + str(b["total_scripts"]) + ' scripts, ~' + str(b["total_min_estimated"]) + ' min total)</h3>'
            '<div class="batch-sessions">' + "".join(sessions_html) + '</div>'
            '</div>'
        )
    batches_html = "".join(batch_parts)

    # KANBAN CARDS
    kanban_cards_html = []
    for reel in data["reels"]:
        for s in reel["scripts"]:
            script_id = f"s{reel['n']}-{s['n']}"
            theme_tag = reel.get("theme_id", "") or "—"
            hook_preview = s["hook"][:90] + ("…" if len(s["hook"]) > 90 else "")
            kanban_cards_html.append(
                '<div class="kanban-card" draggable="true" data-script-id="' + script_id + '" data-reel="' + str(reel["n"]) + '" data-theme="' + theme_tag + '">'
                '<span class="k-num">#' + str(reel["n"]) + '.' + str(s["n"]) + '</span>'
                '<span class="k-tema">' + theme_tag + '</span>'
                '<div class="k-title">' + s["title"] + '</div>'
                '<div class="k-hook">' + hook_preview + '</div>'
                '<span class="k-date" style="display:none">—</span>'
                '<input type="date" class="k-date-input" data-script-id="' + script_id + '">'
                '<div class="k-actions">'
                '<button class="k-open" onclick="kanbanOpen(\'' + script_id + '\')">🔍 Abrir</button>'
                '<button onclick="kanbanMove(\'' + script_id + '\',\'gravado\')">🎬 Gravei</button>'
                '<button onclick="kanbanMove(\'' + script_id + '\',\'editado\')">✂️ Pronto</button>'
                '<button onclick="kanbanMove(\'' + script_id + '\',\'postado\')">📤 Postado</button>''<button class="btn-unschedule" onclick="unscheduleScript(\'' + script_id + '\')">🗑️ Desagendar</button>'
                '</div>'
                '</div>'
            )
    kanban_all_cards = "".join(kanban_cards_html)

    # PUBLICATION AGENDA
    pub_by_week = {}
    for post in schedule:
        k = post.get("semana") or "Semana"
        pub_by_week.setdefault(k, []).append(post)
    pub_parts = []
    for week, posts in pub_by_week.items():
        slots_html = []
        for p in posts:
            slots_html.append(
                '<div class="pub-slot">'
                '<div class="pub-when"><b>' + p["data_br"] + '</b> • ' + p["hora"] + '</div>'
                '<div class="pub-title">#' + str(p["reel_n"]) + '.' + str(p["script_n"]) + ' — ' + p["title"] + '</div>'
                '<a class="pub-link" href="#s' + str(p["reel_n"]) + '-' + str(p["script_n"]) + '">⤵️ Ir para roteiro + caption</a>'
                '</div>'
            )
        pub_parts.append(
            '<div class="pub-week">'
            '<h3>' + week + '</h3>'
            '<div class="pub-slots">' + "".join(slots_html) + '</div>'
            '</div>'
        )
    pub_html = "".join(pub_parts) or '<p>Sem cronograma de publicação.</p>'

    # REELS
    reels_parts = []
    for reel in data["reels"]:
        scripts_html_parts = []
        for s in reel["scripts"]:
            script_id = f"s{reel['n']}-{s['n']}"
            roteiro = f"{s['hook']}\n\n{s['corpo']}\n\n{s['cta']}"
            caption = f"{s['legenda']}\n\n{s['hashtags']}"
            scripts_html_parts.append(
                '<div class="script-card" data-reel="' + str(reel['n']) + '" data-script="' + str(s['n']) + '" id="' + script_id + '">'
                '<div class="script-header">'
                '<span class="script-num">#' + str(reel['n']) + '.' + str(s['n']) + '</span>'
                '<span class="script-title">' + s['title'] + '</span>'
                '<span class="script-status" data-key="' + script_id + '">⏳ aguardando</span>'
                '</div>'
                '<div class="block-group">'
                '<div class="block-header">'
                '<label>🎥 ROTEIRO — fala gravada (HOOK + CORPO + CTA)</label>'
                '<button class="btn-copy-block" data-target="' + script_id + '-roteiro">📋 Copiar roteiro</button>'
                '</div>'
                '<div class="block-body">'
                '<div class="block-sub"><span class="tag">🎬 HOOK (0-3s)</span><p>' + s['hook'] + '</p></div>'
                '<div class="block-sub"><span class="tag">📝 CORPO (3-25s)</span><p>' + s['corpo'] + '</p></div>'
                '<div class="block-sub"><span class="tag">📣 CTA (25-35s)</span><p>' + s['cta'] + '</p></div>'
                '</div>'
                '<textarea id="' + script_id + '-roteiro" class="hidden-copy">' + roteiro + '</textarea>'
                '</div>'
                '<div class="block-group">'
                '<div class="block-header">'
                '<label>📱 CAPTION DO POST — legenda + hashtags</label>'
                '<button class="btn-copy-block" data-target="' + script_id + '-caption">📋 Copiar caption</button>'
                '</div>'
                '<div class="block-body">'
                '<div class="block-sub"><span class="tag">📄 LEGENDA</span><p>' + s['legenda'] + '</p></div>'
                '<div class="block-sub"><span class="tag">#️⃣ HASHTAGS</span><p>' + s['hashtags'] + '</p></div>'
                '</div>'
                '<textarea id="' + script_id + '-caption" class="hidden-copy">' + caption + '</textarea>'
                '</div>'
                '<div class="script-actions">'
                '<button class="btn-big btn-teleprompter" data-id="' + script_id + '">🎥 Modo Teleprompter</button>'
                '<button class="btn-big btn-share" data-id="' + script_id + '">💬 Enviar WhatsApp</button>'
                '<select class="status-select" data-key="' + script_id + '">'
                '<option value="aguardando">⏳ Aguardando</option>'
                '<option value="para_gravar">🎬 Para gravar</option>'
                '<option value="gravado">✂️ Em edição</option>'
                '<option value="editado">✅ Pronto pra postar</option>'
                '<option value="agendado">📅 Agendado</option>'
                '<option value="postado">📤 Postado</option>'
                '</select>'
                '</div>'
                '</div>'
            )
        reels_parts.append(
            '<section class="reel-card" data-reel="' + str(reel['n']) + '">'
            '<h2>#' + str(reel['n']) + ' — ' + reel['title'] + '</h2>'
            '<div class="reel-meta">'
            '<a href="' + reel['url'] + '" target="_blank">🔗 Ver original</a>'
            '<span class="eng">📊 ' + reel['engagement'] + '</span>'
            '</div>'
            '<details class="viral-analysis">'
            '<summary>🧪 Por que viralizou</summary>'
            '<p><strong>Hook:</strong> ' + reel['why_viral']['hook'] + '</p>'
            '<p><strong>Estrutura:</strong> ' + reel['why_viral']['structure'] + '</p>'
            '<p><strong>Retention:</strong> ' + reel['why_viral']['retention'] + '</p>'
            '</details>'
            '<div class="scripts">' + "".join(scripts_html_parts) + '</div>'
            '</section>'
        )
    reels_html = "".join(reels_parts)

    data_json = json.dumps(data, ensure_ascii=False)
    schedule_json = json.dumps(schedule, ensure_ascii=False)
    all_scripts_map = {}
    for reel in data["reels"]:
        for s in reel["scripts"]:
            sid = f"s{reel['n']}-{s['n']}"
            all_scripts_map[sid] = {"reel_n": reel["n"], "script_n": s["n"], "title": s["title"], "hook": s["hook"][:100], "theme_id": reel.get("theme_id","")}
    all_scripts_json = json.dumps(all_scripts_map, ensure_ascii=False)

    html = (
        '<!DOCTYPE html><html lang="pt-BR"><head>'
        '<meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<title>' + title + ' — IVS Produção</title>'
        '<style>' + CSS + '</style>'
        '</head><body>'
        '<header class="top">'
        '<h1><span>🩺 IVS Produção — ' + title + '</span>'
        '<span class="status-badge">✅ APROVADO</span></h1>'
        '<div class="toolbar">'
        '<button onclick="scrollToSection(\'planner-section\')">🎯 Planner</button>''<button onclick="scrollToSection(\'month-section\')">📅 Mês</button>'
        '<button onclick="scrollToSection(\'kanban-section\')">📋 Kanban</button>'
        '<button onclick="scrollToSection(\'publication-section\')">📆 Publicação</button>'
        '<button onclick="exportJSON()">💾 Export JSON</button>'
        '<button onclick="window.print()">🖨️ Imprimir</button>'
        '</div></header>'
        '<main>'
        '<div class="meta-grid">'
        '<div class="meta-card"><strong>' + str(len(data["reels"])) + '</strong><small>Reels analisados</small></div>'
        '<div class="meta-card"><strong>' + str(total_scripts) + '</strong><small>Scripts prontos</small></div>'
        '<div class="meta-card"><strong>' + str(len(data["themes"])) + '</strong><small>Temas clusterizados</small></div>'
        '<div class="meta-card"><strong>' + (data.get("source", "—") or "—") + '</strong><small>Perfil fonte</small></div>'
        '</div>'

        '<div class="calendar" id="planner-section">'
        '<h2>🎯 Planner de Gravação — selecione e agende</h2>'
        '<p class="cal-note">Agrupei os scripts por tema (batch recording). Marque os scripts que quer gravar juntos, escolha uma data e clique "Agendar gravação". Eles aparecerão no Kanban na coluna "🎬 Para gravar".</p>'
        + batches_html +
        '</div>'

        '<div class="calendar" id="month-section">''<h2>📅 Calendário Mensal — visão combinada</h2>''<p class="cal-note">🎬 <b>dourado</b> = dias de gravação agendados • 📤 <b>verde</b> = dias de publicação. Clique em qualquer dia para ver detalhes.</p>''<div class="month-cal">''<div class="month-header">''<div class="month-title" id="month-title">—</div>''<div class="month-nav">''<button onclick="monthNav(-1)">◀</button>''<button onclick="monthNav(0)">Hoje</button>''<button onclick="monthNav(1)">▶</button>''</div>''</div>''<div class="month-legend">''<span>🎬 <b>Gravação agendada</b></span>''<span>📤 <b>Publicação prevista</b></span>''<span>⭐ <b>Hoje</b></span>''</div>''<div class="month-grid" id="month-grid"></div>''<div class="day-details hidden" id="day-details"></div>''</div>''</div>'
        '<div class="calendar" id="kanban-section">'
        '<h2>📋 Kanban — fluxo de produção</h2>'
        '<p class="cal-note">Arraste os cards entre as colunas ou use os botões (🎬 Gravei / ✂️ Pronto / 📤 Postado). Estado salvo no seu navegador.</p>'
        '<div class="kanban-wrap">'
        '<div class="kanban">'
        '<div class="kanban-col" id="col-aguardando"><h3>📝 Aguardando <span class="count">0</span></h3></div>'
        '<div class="kanban-col" id="col-gravar"><h3>🎬 Para gravar <span class="count">0</span></h3></div>'
        '<div class="kanban-col" id="col-edicao"><h3>✂️ Em edição <span class="count">0</span></h3></div>'
        '<div class="kanban-col" id="col-pronto"><h3>✅ Pronto pra postar <span class="count">0</span></h3></div>'
        '<div class="kanban-col" id="col-postar"><h3>📤 Agendado / Postado <span class="count">0</span></h3></div>'
        '</div>'
        '</div>'
        '<div style="display:none">' + kanban_all_cards + '</div>'
        '</div>'

        '<div class="calendar" id="publication-section">'
        '<h2>📆 Agenda de Publicação</h2>'
        '<p class="cal-note">Horários: Quarta 19h, Sexta 12h, Domingo 11h (engagement histórico do público IVS).</p>'
        + pub_html +
        '</div>'

        '<div class="theme-nav">'
        '<button class="chip active" data-theme="ALL" onclick="filterTheme(\'ALL\')">Todos os reels</button>'
        + themes_nav +
        '</div>'

        '<div id="reels-list">' + reels_html + '</div>'
        '</main>'
        '<div class="tele-modal" id="tele-modal">'
        '<button class="tele-close" onclick="closeTele()">✗ Fechar (Esc)</button>'
        '<button class="tele-size" onclick="toggleTeleSize()">A+</button>'
        '<div class="tele-text" id="tele-text"></div>'
        '</div>'
        '<div class="toast" id="toast"></div>'
        '<script>window.IVS_DATA = ' + data_json + '; window.IVS_SCHEDULE = ' + schedule_json + '; window.IVS_SCRIPTS = ' + all_scripts_json + ';</script>'
        '<script>' + JS + '</script>'
        '</body></html>'
    )
    return html


def main():
    if len(sys.argv) < 4:
        print("uso: md_to_production_html.py <entrada.md> <saida.html> <titulo>", file=sys.stderr)
        sys.exit(1)
    md_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    title = sys.argv[3]
    md = md_path.read_text(encoding="utf-8")
    data = parse_md(md)
    html = render_html(data, title)
    out_path.write_text(html, encoding="utf-8")
    print(f"ok: {out_path} ({len(html)} chars, {len(data['reels'])} reels, {sum(len(r['scripts']) for r in data['reels'])} scripts)")


if __name__ == "__main__":
    main()

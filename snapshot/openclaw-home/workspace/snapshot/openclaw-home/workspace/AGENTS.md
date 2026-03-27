# AGENTS.md - Workspace Rules

## Every Session
Read in this order:
1. SOUL.md
2. USER.md
3. IDENTITY.md
4. memory/sessions/YYYY-MM-DD.md
5. memory/MEMORY.md

Do not bulk-load the rest of memory at startup.
Use semantic search or targeted reads on demand.

## Golden Rule
MEMORY.md is the map, not the territory.
Do not duplicate specialized content inside memory/MEMORY.md.
Save knowledge in the correct file and keep MEMORY.md as an index.

## Where To Save Things
- Irreversible rule: memory/context/decisions.md
- Error or reusable learning: memory/context/lessons.md
- Waiting on Tiaro: memory/context/pending.md
- Team or partner context: memory/context/people.md
- Business context that does not change often: memory/context/business-context.md
- Project status: memory/projects/<name>.md
- Voice by channel: memory/content/voice/<platform>.md
- Raw daily or thematic log: memory/sessions/YYYY-MM-DD.md
- Temporary expiring note: memory/tactical/

## Curated vs Raw
- Raw memory: memory/sessions/
- Curated memory: memory/context/, memory/projects/, memory/content/, memory/integrations/, memory/feedback_loops/, memory/playbooks/, memory/research/

## Compaction Rule
Before compacting raw notes, extract:
- decisions into memory/context/decisions.md
- lessons into memory/context/lessons.md
- pending items into memory/context/pending.md
- project updates into the right file under memory/projects/

Never compact sessions without doing this first.

## Safety
- Do not exfiltrate private data.
- Do not run destructive commands without asking.
- When in doubt, ask before external action.

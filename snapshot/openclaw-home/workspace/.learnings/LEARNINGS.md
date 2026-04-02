## [LRN-20260401-001] correction

**Logged**: 2026-04-01T13:09:00Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
For Canva replication requests, do not claim fidelity when MCP generate-design output is only approximate; explicitly state whether Nanobanana/Gemini image-generation access is actually available.

### Details
User said the recreated Canva post was completely different and asked whether Nanobanana 2 was being used. I had created approximate Canva candidates via MCP generate-design and implied they were faithful replicas. For exact-look tasks, approximate generation is insufficient and should be labeled as a draft, not a replication. Also, if the requested generation model/path is unavailable, I must say so plainly instead of letting the user infer it was used.

### Suggested Action
When asked to replicate a post exactly in Canva, state current limitation clearly, call the first result a draft if needed, and ask for or use a real editable Canva template/design_id when exact fidelity matters. Never imply Nanobanana/Gemini was used unless it was actually invoked and available.

### Metadata
- Source: user_feedback
- Related Files: /root/.openclaw/workspace/memory/playbooks/canva-marketing-workflow.md
- Tags: canva, replication, honesty, gemini, nanobanana

---

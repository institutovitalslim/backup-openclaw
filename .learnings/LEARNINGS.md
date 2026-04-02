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

## [LRN-20260402-001] correction

**Logged**: 2026-04-02T16:52:00Z
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
When a user says an item was not requested, do not argue based on synonym distinctions if the active ingredient is the same substance.

### Details
The user corrected the Biomeds order by saying Vitamina C 444mg was not requested. I responded that the stored item was Ácido Ascórbico/Vitamina C 20% 1g/5mL and implied this was a meaningful distinction. The user correctly pointed out that ácido ascórbico is vitamina C. In this context, the right action is to treat the correction as applying to the vitamin C item in the order, acknowledge the mistake, and update the stored record accordingly instead of defending a wording difference.

### Suggested Action
When users correct medicine names that are synonyms or equivalent active ingredients, assume they refer to the same substance unless dosage/formulation clearly matters. Acknowledge the correction, remove or update the stored line item, and then clarify formulation only if still needed.

### Metadata
- Source: user_feedback
- Related Files: /root/.openclaw/workspace/memory/tactical/pedidos-injetaveis-aguardando-chegada-2026-04-02.md
- Tags: correction, inventory, medication-names, synonyms, vitamin-c

---

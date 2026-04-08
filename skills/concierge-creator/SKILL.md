---
name: concierge-creator
description: Create, refine, and operationalize a WhatsApp/DM concierge from scratch using real business information. Use when building a concierge agent for clinics, premium services, sales teams, appointment setters, or high-touch customer experience flows; especially when the work involves extracting knowledge from scripts, conversations, forms, objections, FAQs, positioning, and then turning that into a living prompt, brain, QA battery, control logic, and continuous improvement loop.
---

# Concierge Creator

Create a concierge system as a living operating model, not just a prompt.

## Core outcome
Build a concierge that:
- sounds human and premium
- learns the business quickly
- increases trust and perceived value
- converts conversations into the target action (usually booking, qualification, or handoff)
- can be supervised, paused, and improved continuously

## Workflow

### 1. Extract the business truth
Collect and distill the minimum information needed to operate well:
- positioning and offer
- price and payment logic
- FAQs
- objections
- tone of voice
- onboarding / booking flow
- boundaries and clinical/legal limits if relevant
- examples of real conversations
- forms, scripts, exports, spreadsheets, or CRM data when available

Prefer real artifacts over abstract descriptions.

If you need field guidance while extracting source material, read:
- `references/discovery-checklist.md` for what to gather
- `references/source-priority.md` for how to rank evidence quality

### 2. Define the concierge role clearly
Do not start from “assistant”. Define:
- who the concierge is
- what action it is meant to maximize
- what it must never do
- what makes it feel premium instead of robotic or pushy

Useful distinction:
- concierge ≠ telemarketing
- concierge ≠ generic support bot
- concierge = elegant commercial guidance with trust

### 3. Separate the system into layers
Always structure the concierge in layers:

1. **Prompt-base**
   - identity
   - mission
   - tone
   - decision logic
   - rules
   - objections
   - booking behavior

2. **Brain / memory layer**
   - recurring pains
   - recurring objections
   - what converts
   - what destroys trust
   - tone principles
   - business truths that should persist beyond a single prompt rewrite

3. **Learning log**
   - what happened in real conversations
   - what worked
   - what failed
   - what should be updated

Do not force everything into one giant prompt.

### 4. Treat activation and control as first-class product features
A real concierge needs operational controls.
Design:
- when it should answer
- who it should ignore
- human takeover rules
- pause / resume logic
- contact-level override
- activation phrase if needed
- “new contact vs known lead vs existing customer/patient” behavior

If building for messaging operations, include a status/control mechanism early.

### 5. Build from real language
Use real conversation data whenever possible:
- chat exports
- spreadsheets of conversations
- forms/questionnaires
- team scripts
- public brand voice

Extract:
- common openings
- real wording of pains
- emotional vocabulary
- objections
- phrases that increase trust
- phrases that sound scripted or defensive

The concierge should sound like the business at its best, not like a generic AI.

### 6. Create a QA battery before launch
Always write a QA battery with realistic scenarios.
Include at least:
- direct price question
- insurance / reimbursement / policy question if relevant
- hot lead ready to book
- cold lead asking generic info
- objection to price
- objection from prior frustration
- practical/logistics objection
- emotional case
- return after silence
- fast path to booking

For each scenario, check:
- sounds human?
- sounds concierge?
- answers clearly?
- builds value?
- avoids funnel feel?
- handles price elegantly?
- respects boundaries?
- advances the objective?

If you need a reusable structure, read `references/qa-battery-template.md`.

### 7. Run advisory review before calling it “final”
Pressure-test the concierge from multiple angles:
- commercial / conversion
- clinical / safety / trust if applicable
- WhatsApp/copy/naturalness
- outsider / fresh eyes
- executor / production readiness

Look especially for:
- script feel
- institutional language
- over-explaining
- evasiveness on price
- too many questions in a row
- hidden clinical overreach

If you want a reusable review framework, read `references/council.md`.

### 8. Launch as pre-production assisted, not “finished”
Never treat version 1 as done.
Use pre-production assisted mode:
- human supervision
- pause command
- takeover command
- learning loop after real conversations
- frequent refinements based on evidence

### 9. Define the learning loop
After conversations finish, record:
- booked / not booked / still open
- main pain
- main objection
- phrase that helped
- phrase that hurt
- new FAQ
- update needed in prompt
- update needed in brain

Refine from repeated patterns, not one-off feelings.

If you need reusable operating templates, read:
- `references/brain-template.md`
- `references/learning-log-template.md`
- `references/preproduction-template.md`

## Output set to create
When authoring a concierge from scratch, prefer creating these files:
- main prompt file
- brain file
- learning log file
- QA scenarios file
- QA report file
- pre-production plan
- control-state files/scripts if automation is involved

If you want a ready-to-clone structure, read `references/concierge-starter-template.md`.

## Tone guidance
Optimize for:
- elegance
- clarity
- confidence
- warmth
- brevity
- momentum toward the goal

Avoid:
- robotic wording
- marketing exaggeration
- visible manipulation
- defensive sales copy
- giant prompts that become brittle

## Deliverable standard
A concierge is ready for pre-production when:
- its role is explicit
- its boundaries are explicit
- its prompt is lean enough to stay natural
- its brain exists separately
- its QA battery is documented
- operational controls exist
- a learning loop exists

If any of those are missing, the concierge is not production-ready yet.

## Starter generation
If you want to generate a new concierge starter set quickly, run:

```bash
python3 scripts/new_concierge.py "NomeDaConcierge" --out /path/to/output
```

Optional parameters:
- `--role`
- `--goal`
- `--target-action`
- `--brief /path/to/briefing.json`

This generates a fillable starter set from `references/starter-files/` and replaces the core identity placeholders automatically.

If you use `--brief`, the script also fills any matching `{{PLACEHOLDER}}` found in the templates.
Use `references/starter-files/briefing-example.json` as a model.

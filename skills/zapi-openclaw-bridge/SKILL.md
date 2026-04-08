---
name: zapi-openclaw-bridge
description: Build, configure, and operate a Z-API to OpenClaw WhatsApp bridge for concierge agents like Clara. Use when connecting Z-API webhooks to an OpenClaw-powered agent, exposing a stable HTTPS webhook, filtering contacts (such as existing patients/customers), handling activation rules, routing messages into OpenClaw, sending replies back through Z-API, and adding operational controls like pause/resume, manual takeover, and lead state.
---

# Z-API OpenClaw Bridge

Treat the bridge as an operational system, not just a webhook endpoint.

## Core outcome
Create a stable bridge that:
- receives inbound WhatsApp messages from Z-API
- filters who should or should not be answered
- calls the OpenClaw-powered concierge
- returns the reply through Z-API
- supports safe production controls

## Workflow

### 1. Define the bridge contract
Document clearly:
- Z-API instance and token inputs
- webhook path and secret/tokenized route
- OpenClaw endpoint/session behavior
- outbound reply method
- health endpoint
- logging expectations

### 2. Separate business logic from transport
Keep these concerns distinct:
- webhook verification / HTTP receive
- message parsing and normalization
- business rules (patient/customer filter, activation phrase, lead state)
- OpenClaw call
- outbound WhatsApp send
- operational controls

Do not mix all of this into one unreadable handler.

### 3. Implement immediate webhook acknowledgement
Always return a fast success response to Z-API first, then process asynchronously if response time is a risk.

This avoids:
- delivery retries
- timeouts
- broken pipe behavior
- fragile synchronous coupling

### 4. Add answer-governance rules
Define who the concierge can answer.
Typical gates:
- global pause
- manual override / human takeover
- existing patient/customer check
- activation phrase
- new-contact behavior
- known-lead behavior

These rules should be explicit and logged.

### 5. Add contact-state memory
Persist at least the minimum operational state needed, such as:
- active leads
- manual overrides
- pause state
- optional conversation/session mapping

Use simple JSON state if the system is small and single-host.

### 6. Prefer external prompt files
Do not hard-embed giant system prompts inside the bridge code.
Load them from files so the concierge can evolve without risky code edits.

### 7. Make production controls first-class
Support at least:
- pause
- resume
- assume/takeover by phone
- release by phone
- status

If the operation runs through Telegram or another control surface, keep the command layer simple and auditable.

### 8. Validate with real operational tests
Before calling the bridge ready, test:
- webhook reaches server over HTTPS
- inbound message is parsed correctly
- blocked contacts do not get answers
- allowed contacts do get answers
- reply returns through Z-API
- pause/resume works
- manual takeover works
- service restarts cleanly

### 9. Keep secrets out of code
Store credentials in environment files or secret managers.
Never hardcode tokens in Python files or skill docs.

### 10. Launch assisted first
Treat first launch as pre-production assisted:
- watch first live messages closely
- pause immediately if behavior drifts
- log weird cases
- update prompt/business rules from evidence

## Common assets to create
When building a bridge like this, prefer these files:
- bridge service script
- env file example or variable list
- system prompt file
- control script
- control state JSON
- lead state JSON
- deployment notes
- QA / validation checklist

## Failure patterns to watch
- replying to people who should be blocked
- not replying because state logic is wrong
- brittle synchronous webhook handling
- embedded prompt drift
- environment file missing or not loaded by systemd
- unclear activation rules
- no fast manual stop capability

## Practical recommendation
For a small/medium operation, a Python bridge + systemd + nginx + Let's Encrypt + JSON state is often enough.
Scale complexity only when the operation truly needs it.

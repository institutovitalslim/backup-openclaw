## [ERR-20260326-001] message_tool_whatsapp

**Logged**: 2026-03-26T22:15:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
message tool could not send WhatsApp reminder to Tiaro because the backend treated the request as a Telegram chat and returned "chat not found".

### Error
Telegram send failed: chat not found (chat_id=557186968887). Likely: bot not started in DM, bot removed from group/channel, group migrated (new -100… id), or wrong bot token.

### Context
- Command: `message.send` with `{channel: "whatsapp", to: "557186968887", message: "Tiaro, passando só pra te lembrar..."}`
- Purpose: send reminder via WhatsApp as requested by Tiaro.
- Outcome: infrastructure routed to Telegram and failed; no WhatsApp message delivered.

### Suggested Fix
Verify how to target WhatsApp contacts via the message tool (correct channel id, contact mapping, or dedicated WhatsApp integration). Document the correct parameters or add automation to sync WhatsApp contacts so reminders can be delivered reliably.

### Metadata
- Reproducible: unknown
- See Also: _none_

---

## [ERR-20260402-001] gateway_config_patch

**Logged**: 2026-04-02T16:28:00Z
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
`gateway config.patch` rejected an object-style patch and returned `raw required`.

### Error
```
raw required
```

### Context
- Operation attempted: `gateway.config.patch`
- Intended change: switch `agents.defaults.memorySearch.provider` from OpenAI to Gemini and remove OpenAI fallback for memory search.
- First attempt used the `patch` object field directly.
- Gateway rejected the request because this tool instance expects the patch payload in `raw` format.

### Suggested Fix
When using `gateway config.patch` in this workspace, pass the patch as serialized JSON in `raw` instead of relying on the structured `patch` field.

### Metadata
- Reproducible: yes
- Related Files: /root/.openclaw/openclaw.json
- See Also: _none_

---

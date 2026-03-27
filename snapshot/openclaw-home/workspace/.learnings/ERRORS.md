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

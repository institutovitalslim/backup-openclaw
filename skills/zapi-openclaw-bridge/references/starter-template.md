# Starter Template

Use this structure for a new Z-API ↔ OpenClaw bridge:

## Files
- `bridge.py`
- `.env.example`
- `system_prompt.md`
- `control_state.json`
- `lead_state.json`
- `control.py`
- `deployment_checklist.md`

## Minimum design rules
- acknowledge webhook fast
- process asynchronously when needed
- keep prompt outside code
- separate business rules from transport
- keep stop/takeover controls simple
- log allow/block decisions clearly

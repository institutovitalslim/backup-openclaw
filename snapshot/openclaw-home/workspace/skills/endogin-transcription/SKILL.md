---
name: "endogin-transcription"
description: "Use when OpenClaw needs to access the Endogin members area, study the Vendas tracks such as Dr. Wilson or Q&A SND VENDAS, collect accessible materials, and turn lessons into reusable operational teaching notes without repeating known platform mistakes."
---

# Endogin Transcription

Use this skill for Endogin study work that mixes:

- login to `membros.mentoriaendogin.com.br`
- navigation to Vendas modules
- extraction of PDFs and lesson metadata
- transcription of lesson audio when audio is available in a compliant way
- conversion of transcripts into study memory for Clara
- delivery of the learning in teaching format, detailed enough that Tiaro does not need to watch the original class

## Use With

- Use the available OpenClaw transcription capability when an audio file is already available.
- Use a real browser session when Endogin requires rendered playback.

## Known Endogin Facts

- Login URL: `https://membros.mentoriaendogin.com.br/auth/login?redirect=%2F`
- Credentials are stored in the 1Password item `Senha Acesso Endogin`.
- Current sales focus:
- `Dr. Wilson - Programas de Acompanhamento na Pratica`
- `Q&A SND VENDAS!`
- Priority learning emphasis:
- `SPIN Selling`
- objection handling
- patient connection
- high-ticket conversion
- Current VPS memory targets:
- `/root/.openclaw/workspace/memory/projects/endogin-vendas.md`
- `/root/.openclaw/workspace/memory/research/endogin-vendas-2026-03-28.md`
- `/root/.openclaw/workspace/memory/integrations/telegram-map.md`

## Hard Rules

- Never open `player.vdocipher.com/v2/?otp=...&playbackInfo=...` as a standalone URL and treat it as the lesson page.
- VdoCipher OTP links are domain-bound embeds; opening them outside the original Endogin lesson page can trigger `Error 2014 - Domain could not be verified due to a website configuration`.
- The correct path is to open the authenticated Endogin lesson page first and interact with the embedded player there.
- If the embedded player itself shows `Error 2014` inside the lesson page, treat that as a platform-side/domain configuration blocker and report it plainly instead of retrying the standalone player URL.
- Do not ask the user to paste credentials if 1Password already has them.
- Do not claim a video was transcribed unless a transcript file or verified text output exists.
- Do not bypass DRM or imply that protected media was extracted when it was not.
- If the player is DRM-protected, switch to a compliant browser-assisted path and say so plainly.
- Do not over-compress the class content.
- Do not omit important steps, examples, objections, transitions, or practical phrasing.

## Workflow

1. Read the latest Endogin sales memory only if needed for context.
2. Retrieve the Endogin login from 1Password item `Senha Acesso Endogin`.
3. Enter Endogin through the browser if the content depends on the rendered player.
4. Prefer this order of knowledge capture:
5. PDFs and downloadable materials.
6. Lesson titles, order, durations, and metadata.
7. Transcript from audio or video.
8. Teaching-style notes for Clara.
9. If the user asked for a posted delivery, report the result in Telegram topic `Evolucao do Openclaw` in AI Vital Slim (`chat -1003803476669`, `thread 768`).
10. Save new knowledge back into the appropriate memory file.

## Validated Operational Path

When direct extraction is blocked by VdoCipher DRM, use this validated path:

1. Open a dedicated Chrome with remote debugging.
2. Log into Endogin and open the target lesson.
3. Use `assets/tab-share-recorder.html` through `scripts/save_tab_share_capture.mjs`.
4. In the Chrome picker, choose the Endogin tab and enable tab audio.
5. Save the captured `.webm`.
6. Convert to `.wav` with `ffmpeg`.
7. Transcribe with OpenAI using the installed Python client or the available OpenClaw transcription capability.

## Transcription Decision Tree

- If the lesson exposes a direct audio file or a user-provided recording exists:
- use the available OpenClaw transcription capability first
- If the lesson exposes text, article content, or PDFs:
- extract and summarize those first
- If the lesson uses VdoCipher or another protected player and direct audio extraction fails:
- do not keep retrying the same DRM path
- move to browser-assisted playback and capture only if a compliant capture method is available in the current environment
- If no compliant capture method exists:
- report that the transcript is blocked by protected playback and preserve every other accessible artifact

## Teaching Output Rule

Every time Clara studies an Endogin lesson, she must structure the result as if she were teaching the lesson back to Tiaro and the team.

Required shape:

- lesson title and module
- what was actually accessed: full video, partial transcript, PDF, article, or metadata
- detailed points covered in the lesson, in the same order they appear when possible
- main teachings and practical logic behind each point
- step-by-step process or framework taught by the instructor
- practical examples, phrases, objections, scripts, and applications mentioned or implied
- operational adaptation for Clara and Vital Slim
- open gaps only if some part of the lesson was inaccessible

Presentation format:

- `Aula`
- `Objetivo da aula`
- `Pontos abordados em detalhe`
- `Principais ensinamentos`
- `Passo a passo ou metodo`
- `Exemplos e frases uteis`
- `Como aplicar na operacao`
- `Roteiro pratico para Clara`
- `Riscos, erros e cuidados`

When `Dr. Wilson` is involved, explicitly look for:

- SPIN Selling patterns
- question sequencing
- situational vs problem questions
- implication framing
- need-payoff logic

## Memory Targets

- Sales synthesis: `/root/.openclaw/workspace/memory/projects/endogin-vendas.md`
- Session or deep-research log: `/root/.openclaw/workspace/memory/research/endogin-vendas-YYYY-MM-DD.md`
- Telegram topic map: `/root/.openclaw/workspace/memory/integrations/telegram-map.md`

## References

- Read `references/endogin-transcription-runbook.md` for the validated Endogin routes, known blockers, and the recommended sequencing for Dr. Wilson and Q&A SND VENDAS.
- Use `scripts/save_tab_share_capture.mjs` with `assets/tab-share-recorder.html` as the primary browser-assisted capture path validated on 2026-03-28.

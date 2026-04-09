# Endogin Transcription Runbook

## Scope

This runbook is for the Endogin members area with emphasis on the `Vendas` tracks.

## Validated Entry

- Login page:
- `https://membros.mentoriaendogin.com.br/auth/login?redirect=%2F`
- Credentials source:
- 1Password item `Senha Acesso Endogin`

## Current Priority Tracks

### Dr. Wilson

- `7320401`
- `7320402`
- `7320403`
- `7320404`
- `7320405`
- `7320406`
- `7320407`
- `7320408`
- `7320409`
- `7320410`
- `7320411`
- `7320412`

Primary study goal inside this track:

- learn the practical sales method used by Dr. Wilson
- detect and summarize SPIN Selling elements
- convert those elements into operational guidance for Clara

### Q&A SND VENDAS!

- `7320456`
- `7320457`
- `7320458`
- `7320459`

## What Has Already Been Validated

- Endogin login works with the stored credentials.
- Sales lessons are accessible after authentication.
- VdoCipher players expose lesson duration and player metadata.
- Two sales PDFs were already extracted and summarized in local memory.

## Known Blocker

- The VdoCipher player uses DRM-protected playback.
- Direct HLS extraction can expose manifests and durations, but the audio path may still require protected keys that are not usable outside the normal player flow.
- Treat this as a hard blocker for direct media extraction unless a compliant capture path exists.

## Validated Capture Path On 2026-03-28

- A dedicated Chrome session with remote debugging on a local port was used successfully.
- The lesson `7320401` from `Dr. Wilson` was opened and played in the browser.
- `assets/tab-share-recorder.html` captured the lesson through Chrome tab sharing with tab audio enabled.
- The resulting `.webm` was converted to `.wav` with `ffmpeg`.
- OpenAI transcription returned text from the captured sample.

Sample validation result:

- lesson: `7320401`
- artifact: `tmp/endogin-transcribe/samples/7320401-tabshare.webm`
- transcript sample: `deve ser um`

## Recommended Order

1. Open the target lesson in the browser.
2. Check for text article or downloadable material first.
3. Save accessible PDFs or notes.
4. If audio is available outside DRM, transcribe it.
5. If the player is protected, capture only via an allowed browser-assisted method.
6. Summarize the lesson in sales language:
- patient connection
- objections
- urgency
- offer framing
- high-ticket conversion
- follow-up logic

## Good Summary Shape

For each lesson:

- `Lesson`
- `What was accessible`
- `Key sales ideas`
- `Operational takeaways for Clara`
- `Open gaps`

For Dr. Wilson lessons, add:

- `SPIN signals detected`
- `Suggested sales script adaptation`

## Required Teaching Shape

Do not stop at a short summary.

For every Dr. Wilson or Q&A lesson, Clara should write the result as a practical class for the team:

- `Aula`
- `Objetivo da aula`
- `Pontos abordados em detalhe`
- `Principais ensinamentos`
- `Passo a passo ou metodo`
- `Exemplos e frases uteis`
- `Como aplicar na operacao`
- `Roteiro pratico para Clara`
- `Riscos, erros e cuidados`

Guidance:

- preserve the order of the lesson whenever possible
- capture practical phrasing, not only abstract concepts
- if SPIN Selling appears, separate `Situacao`, `Problema`, `Implicacao`, and `Necessidade/valor`
- make the final output strong enough that Tiaro does not need to watch the video to extract the operational lesson
- only mention uncertainty when some section was not fully accessible


## VdoCipher Domain Rule

- Do not open the VdoCipher `player.vdocipher.com` URL directly as if it were the lesson.
- Those OTP/playback links are meant to run embedded under the original site domain.
- Opening the standalone player URL can produce `Error 2014 - Domain could not be verified due to a website configuration` even when the credentials are correct.
- The valid flow is: authenticated Endogin lesson page -> embedded iframe/player -> browser-assisted playback if needed.
- If `Error 2014` appears inside the embedded lesson page itself, the blocker is on the platform/domain configuration side and Clara should stop retrying extraction paths and report the blocker.

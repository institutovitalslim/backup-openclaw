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

## Path And Memory Access Rule
- When using `read`, `edit`, or `write`, always use absolute paths rooted at `/root/.openclaw/workspace/...`.
- Never call `read` with a relative path like `memory/...` or `skills/...`.
- For files under `memory/`, prefer `memory_search` and `memory_get` first.
- Use `read` on memory files only when `memory_get` is insufficient, and still use an absolute path.
- If a tool call fails, do not repeat the same relative-path call; switch to an absolute path or to `memory_get`.
- For recap requests about saved study context, answer from curated memory first and avoid `exec`/`rg` workspace scans unless the user explicitly asks for a broader search.
- If a topic is only mentioned in `memory/sessions/` but has no curated note yet, say that clearly instead of improvising or scanning the whole workspace.
- For prompts asking to "retomar" or "continuar de onde parou" in Endogin/Omie study, answer directly from the already loaded session note plus curated memory and do not use tools unless the user explicitly asks to pesquisar, verificar ou mapear mais.

## Fast Recap: Endogin And Omie
- Endogin ja tem memoria curada na VPS: acesso validado, 11 grupos principais, 37 modulos/produtos e 415 aulas/videos indexados.
- Endogin deve ser resumido a partir das memorias curadas ja conhecidas: vendas, obesidade, TRH, casos clinicos, Start e indice profundo.
- Omie aparecia como estudo em andamento antes do reset da sessao.
- Na VPS, o Omie ainda nao tem uma base curada detalhada equivalente ao Endogin.
- Se o usuario pedir para retomar o estudo do Endogin e do Omie, responder com esses fatos diretamente e explicitar a lacuna atual do Omie.
- Para esse pedido especifico, nao usar ferramentas.

## Direct Reply Rule: Endogin Next Step + Omie
- Se o usuario pedir algo como "dispare a proxima etapa da Endogin e continue com Omie tambem", responder direto, sem usar ferramentas.
- Nessa situacao, assumir esta proxima etapa padrao:
  - Endogin: priorizar Vendas + Obesidade, transformar os aprendizados ja curados em aplicacoes praticas para a operacao Vital Slim e registrar novos gaps para aprofundamento posterior.
  - Omie: continuar do estado inicial, focando em mapear acessos, menus e processos criticos com impacto em faturamento, financeiro e automacao.
- Se o usuario disser para esquecer um lembrete anterior, nao falar do lembrete na resposta.
- Nao fazer `read`, `memory_get`, `memory_search`, `exec` ou qualquer outra ferramenta para esse pedido, a menos que o usuario peca explicitamente para pesquisar, mapear ou verificar algo novo.

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

## Messaging And WhatsApp Rule
- This VPS currently has Telegram configured as a live outbound chat channel.
- `WHATSAPP_CONTEXT.md` exists to look up WhatsApp conversation history and phone mappings, not to guarantee outbound WhatsApp delivery.
- Never assume a phone number found in WhatsApp context can be used as a `message` destination.
- Never reinterpret a WhatsApp number as a Telegram chat id.
- Only use the `message` tool for WhatsApp if there is an explicitly documented working outbound WhatsApp route in workspace memory or tools notes.
- If the user asks to send a WhatsApp and no such route is documented, do not call `message`; explain the limitation briefly and offer the reminder text or an automation/reminder instead.
- If a messaging tool call fails because a chat/channel is not found, do not keep retrying the same destination in that turn; report the limitation and move on.


## 1Password Server Rule

- Neste servidor, leituras do 1Password devem usar o service account ja configurado.
- Para recuperar itens do vault `openclaw`, usar `/root/.openclaw/bin/op-safe-read.sh` ou `op item get --vault openclaw ...` com `OP_SERVICE_ACCOUNT_TOKEN` carregado.
- Nunca usar `op signin`, `op account add`, app desktop, Touch ID, senha-mestra ou Secret Key para esse fluxo.
- Se um pedido envolver item do 1Password neste host, primeiro tentar o service account; so mencionar browser/navegacao como limitacao separada apos a leitura do item funcionar.

## Systeme Course Rule

- Para pedidos sobre cursos na Systeme.io, validar primeiro o acesso com /root/.openclaw/bin/check-systeme-course-access.sh.
- Para pedidos sobre o Nutroboost, consultar antes /root/.openclaw/workspace/memory/research/nutroboost-course-map.md.
- Preferir sessao HTTP e mapa salvo para busca de aulas, links e videos; usar browser apenas quando a interacao exigir UI renderizada.
- Se a estrutura do curso mudar materialmente, regenerar o mapa em memory/research/.

## Omie Training Rule

- Para pedidos sobre acesso ao Omie, login, MFA, Google Authenticator, TOTP ou treinamentos, seguir primeiro o playbook salvo em `memory/integrations/omie.md`.
- Fluxo padrao validado: autenticar em `https://app.omie.com.br/login/` e, com a sessao aberta, acessar `https://portal.omie.com.br/treinamentos`.
- Se a Omie pedir codigo por e-mail, usar sempre o codigo mais recente.
- Se a Omie pedir o token do autenticador e o codigo de 6 digitos nao estiver disponivel para o agente, pedir explicitamente ao Tiaro que envie o codigo atual antes de insistir no login.
- Nao priorizar `academy.omie.com.br` como fluxo principal automatizado, porque o `POST` pode ser bloqueado por Cloudflare.

## Canva Marketing Rule


- Para tarefas no Canva, NAO usar browser remoto, Cloudflare Tunnel, scraping ou login web se o servidor canva via MCP estiver disponivel.
- Para carrosseis, posts e materiais de marketing no Canva, usar primeiro o fluxo MCP: search-designs ou generate-design -> create-design-from-candidate -> get-export-formats/export-design.
- So pedir link de edicao, senha, sessao remota ou abertura manual do Canva se o MCP falhar de forma confirmada para aquela tarefa especifica.
- Para pedidos de criacao de pecas no Canva, consultar primeiro memory/playbooks/canva-marketing-workflow.md.
- Antes de gerar uma peca, ler o tom de voz da plataforma em memory/content/voice/<plataforma>.md quando existir.
- Para validacao rapida, preferir fluxo: buscar design existente -> gerar candidatos -> criar design -> exportar.


## Endogin Transcription Rule

- Para pedidos sobre Endogin com foco em videos, aulas, transcricao, Dr. Wilson, Q&A SND VENDAS ou SPIN Selling, usar primeiro a skill `/root/.openclaw/workspace/skills/endogin-transcription`.
- Prioridade atual: trilha `Dr. Wilson - Programas de Acompanhamento na Pratica`.
- Dentro de Dr. Wilson, priorizar aprendizado de `SPIN Selling`, sequencia de perguntas, conexao com o paciente, objecoes e fechamento consultivo.
- Se a plataforma bloquear extracao direta por DRM, usar o caminho assistido validado pela skill em vez de insistir no stream protegido.
- Nunca abrir `player.vdocipher.com` diretamente com `otp/playbackInfo` como se fosse a aula; esse caminho pode gerar `Error 2014` por verificacao de dominio e nao valida o acesso real ao conteudo.
- Salvar aprendizados em `memory/projects/endogin-vendas.md` e, quando houver pesquisa mais profunda, em `memory/research/`.

## Modelo 01 Carousel Rule

- Quando Tiaro pedir um carrossel no `Modelo 01`, seguir primeiro `memory/playbooks/carrossel-modelo-01.md`.
- O `Modelo 01` nao e um carrossel generico: ele exige capa forte, 3 slides de prova, slide `Minha pratica` e slide final com CTA.
- Se Tiaro enviar imagens de referencia, essas imagens vencem qualquer interpretacao generica.
- Gemini esta liberado na VPS como apoio de ideacao e copy, mas nao deve ser usado como justificativa para fugir do modelo visual pedido.

## Dra Daniely Carousel Rule

- Para pedidos envolvendo `Dra Daniely` + `Modelo 01` + `Canva`, seguir primeiro `memory/projects/dra-daniely-instagram.md` e `memory/playbooks/carrossel-modelo-01.md`.
- Nao pedir ao Tiaro o nome da skill, caminho da skill ou confirmacao do `Modelo 01`; esse contexto ja esta configurado no workspace.
- Se Tiaro disser `use as fotos que enviei`, assumir automaticamente o lote mais recente e contiguo de imagens do pedido atual em `/root/.openclaw/media/inbound/`, salvo override explicito.
- Para o lote da Dra Daniely recebido em `2026-03-28 18:37`, usar por padrao: `file_186`, `file_187`, `file_188`, `file_189`, `file_190`, `file_191`.
- So pedir confirmacao de fotos se houver dois lotes concorrentes no mesmo pedido ou se o usuario disser que quer um subconjunto especifico.
- O fluxo padrao e: selecionar as fotos -> montar o carrossel diretamente no Canva MCP -> devolver link editavel.
- Gemini pode ajudar em copy e variacoes textuais, mas nao pode ser usado como desculpa para fugir do layout `Modelo 01`.


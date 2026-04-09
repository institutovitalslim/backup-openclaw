# Project: Z-API Bridge

## Status
- fase: em implementacao validada
- prioridade: media-alta
- dono: OpenClaw + operacao IVS

## Validacoes Tecnicas Confirmadas
- o caminho confiavel para invocar a Clara localmente e o OpenClaw Gateway HTTP, nao o `openclaw agent` via CLI
- `GET /v1/models` respondeu 200 no gateway local
- `POST /v1/chat/completions` e `POST /v1/responses` responderam 200 com sessao explicita
- a causa raiz do falso "contexto contaminado" era fallback automatico de modelo: sem forcar modelo disponivel, o runtime trocava o prompt para `Continue where you left off...`
- o header obrigatorio para a bridge e `x-openclaw-model: openai/gpt-5.4`
- a sessao da bridge deve ser fixada por telefone com `x-openclaw-session-key: bridge:zapi:<telefone>`

## Objetivo
Receber eventos da Z-API, armazenar historico por paciente e gerar contexto legivel para uso do OpenClaw.

## Arquitetura
- ingestao HTTP de webhooks
- normalizacao de mensagens
- historico por paciente
- renderizacao de contexto em markdown
- uso posterior pelo OpenClaw

## Papel No Ecossistema
- ponte entre canal conversacional e memoria operacional
- base para atendimento contextualizado
- suporte a automacao de pacientes

## Dependencias
- integracao Z-API
- estrategia de contexto por paciente
- regras claras de seguranca e privacidade

## Backlog
- revisar deploy real no workspace ativo
- validar localizacao do codigo operacional atual
- documentar fluxo de dados ponta a ponta
- revisar estrategia de contexto por paciente

## Proximos Passos
1. expor a bridge com endpoint publico/HTTPS para a Z-API conseguir entregar webhooks externos
2. apontar o webhook da Z-API para a bridge mantendo fan-out para o Apps Script
3. executar teste controlado ponta a ponta por numero de homologacao
4. restaurar de forma definitiva a cadeia de segredos no 1Password para nao depender de recuperacao por logs locais

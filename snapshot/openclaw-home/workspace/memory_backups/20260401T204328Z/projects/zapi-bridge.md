# Project: Z-API Bridge

## Status
- fase: ativo
- prioridade: media-alta
- dono: OpenClaw + operacao IVS

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
1. localizar implementacao ativa e confirmar caminho atual
2. documentar dependencias e pontos de falha
3. alinhar com a estrategia da Melinda quando aplicavel

# Prompt Guiado — Aula Bônus: Multi-Agent OS v2.0

> Anexe junto os arquivos: `prds/multi-agent-v2.md`, `prds/multi-agent-setup.md`, `templates/BOSS-WORKSPACE/` (todos os 8 arquivos), `templates/WORKER-WORKSPACE/` (todos os 6 arquivos)
> ⚠️ Nota: `TOOLS-SHARED.md` e `shared/lessons/` no PRD v2 foram reorganizados na v2.1. Ver nota no topo do PRD.

---

```
Acabei de assistir a aula bônus sobre Multi-Agent OS v2.0 — a evolução de um agente único para uma organização completa com Chief of Staff, Bosses e Workers. Leia os PRDs e templates que estou anexando e me guie na migração.

## O QUE PRECISO

### Fase 1: Diagnóstico (antes de mudar qualquer coisa)

1. **Analise meu setup atual:**
   - Quantos agentes eu tenho?
   - Quem faz o quê?
   - Onde estão os gargalos? (agente sobrecarregado, context rot, custo descontrolado)

2. **Identifique meus domínios:**
   - Me faça perguntas sobre meu trabalho/negócio
   - Baseado nas respostas, sugira 3-5 domínios para bosses
   - Explique POR QUE cada domínio faz sentido separado

3. **Plano de migração personalizado:**
   - Qual a ordem ideal dos bosses? (começar pelo mais crítico)
   - Quais workers cada boss precisa? (Watcher vs Maker)
   - Estimativa de custo mensal

### Fase 2: Foundation (executar)

4. **Backup obrigatório:**
   - Faça backup completo do workspace atual
   - Confirme que é restaurável antes de prosseguir

5. **Promover CoS:**
   - Atualize seu próprio SOUL.md: de COO/Hub para Chief of Staff
   - Defina claramente o que você PARA de fazer vs. o que continua
   - Atualize HEARTBEAT.md para foco em governance

6. **Criar shared/:**
   - Estrutura completa: context/, governance/, costs/, audit/, templates/, outputs/, lessons/
   - TEAM.md como fonte de verdade
   - USER.md canonical que todos herdam
   - TOOLS-SHARED.md com integrações compartilhadas
   - Governance docs: daily digest template, cross-boss protocol, quality gates, escalation rules
   - Scripts: cost tracking, context sync

7. **Ativar governance Day 1:**
   - Cron: daily digest (manhã)
   - Cron: kill switch (noite)
   - Me mostre os crons criados e explique cada um

### Fase 3: Primeiro Boss

8. **Criar Boss A (o mais prioritário):**
   - Criar workspace usando template BOSS-WORKSPACE
   - Personalizar SOUL.md com domínio específico
   - Configurar binding Telegram (topic próprio)
   - Adicionar ao agents.list
   - Cron: summary do boss (horário que faz sentido)

9. **Criar Workers do Boss A:**
   - Para cada worker, decidir: Watcher ou Maker?
   - Watchers: criar workspace + heartbeat
   - Makers: criar workspace (sem heartbeat — spawnados sob demanda)

10. **Teste crítico:**
    - Testar spawn chain: CoS → Boss → Worker
    - Testar que o boss responde no topic dele
    - Testar que o daily digest inclui o boss
    - SÓ avance para o Boss B depois que Boss A funcionar 100%

### Fase 4: Expandir

11. **Repetir para Boss B e Boss C:**
    - Mesmo processo do Boss A
    - Testar cross-boss communication
    - Validar que governance acompanha

12. **Hardening:**
    - Context sync automático (cron semanal)
    - Performance review semanal
    - Ajustar workers: remover os que não usam, adicionar os que faltam
    - Revisar custos: algum agente caro demais vs. valor que entrega?

## REGRAS

- SEMPRE backup antes de cada etapa
- NUNCA pular o teste — se Boss A não funciona, não crie Boss B
- Governance é Dia 1, não "depois"
- Começar com 2-3 bosses, NUNCA 5 de uma vez
- Worker idle (Maker) = $0 — não tenha medo de criar, mas também não crie sem necessidade
- Todo agente novo começa L1 (Observer) — confiança se ganha
- Se algo der errado: rollback do backup, respirar, tentar de novo

## FORMATO

Para cada passo:
1. Explique O QUE vai fazer e POR QUE
2. Peça minha confirmação
3. Execute
4. Mostre o resultado
5. Confirme se posso avançar

Não automatize tudo de uma vez. Quero entender cada decisão.
```

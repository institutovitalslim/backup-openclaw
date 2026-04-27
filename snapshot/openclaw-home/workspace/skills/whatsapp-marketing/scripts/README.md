# Sistema de Follow-up WhatsApp — Instituto Vital Slim

Sistema automatizado de follow-up via WhatsApp (Z-API) para leads que entraram em contato mas não agendaram consulta.

---

## 📋 O QUE FAZ

Envia automaticamente sequências de mensagens para leads no momento certo:

| Mensagem | Delay | Conteúdo |
|----------|-------|----------|
| msg_1 | 24h | Vídeo explicativo da consulta |
| msg_2 | 48h | Dica de valor (raiz do problema) |
| msg_3 | 72h | Depoimento de paciente |
| msg_4 | 5 dias | Urgência sutil (vagas) |
| msg_5 | 7 dias | Última tentativa sem pressão |
| msg_6 | 30 dias | Reativação com novidade |

**Regras:**
- Só envia em horário comercial (8h-20h BRT)
- Para de enviar se lead responder ou agendar
- Não envia mensagem duplicada
- Respeita delay mínimo entre mensagens

---

## 🚀 COMO USAR

### 1. Adicionar Lead

```bash
cd ~/.openclaw/workspace/skills/whatsapp-marketing/scripts
python3 follow_up_manager.py --add "Maria Silva" "71999999999"
```

### 2. Executar Follow-up (manual)

```bash
python3 follow_up_manager.py --run
```

### 3. Marcar como Agendado

```bash
python3 follow_up_manager.py --scheduled "5571999999999"
```

### 4. Marcar como Respondido

```bash
python3 follow_up_manager.py --responded "5571999999999"
```

### 5. Ver Estatísticas

```bash
python3 follow_up_manager.py --stats
```

---

## ⏰ AUTOMATIZAÇÃO (Cron)

Para rodar automaticamente a cada hora:

```bash
# Abrir crontab
crontab -e

# Adicionar linha:
0 8-20 * * * cd ~/.openclaw/workspace/skills/whatsapp-marketing/scripts && python3 follow_up_manager.py --run >> /tmp/follow_up_cron.log 2>&1
```

Isso executa o follow-up todos os dias, das 8h às 20h, a cada hora.

---

## 📁 ARQUIVOS

| Arquivo | Descrição |
|---------|-----------|
| `follow_up_manager.py` | Script principal |
| `follow_up_config.json` | Templates de mensagens |
| `leads.json` | Base de leads |
| `README.md` | Esta documentação |

---

## ⚙️ CONFIGURAÇÃO

Variáveis de ambiente necessárias (já configuradas no sistema):

```bash
ZAPI_BASE_URL=https://api.z-api.io/instances/.../token/...
ZAPI_TOKEN=...
ZAPI_CLIENT_TOKEN=...
```

---

## 📝 ESTRUTURA DO LEAD

```json
{
  "nome": "Maria Silva",
  "phone": "5571999999999",
  "source": "google_ads",
  "created_at": "2026-04-22T10:00:00",
  "last_contact": "2026-04-22T10:00:00",
  "scheduled": false,
  "responded": false,
  "sent_messages": []
}
```

**Campos:**
- `nome`: Nome do lead
- `phone`: Telefone completo com DDI (55...)
- `source`: Origem (google_ads, instagram, indicacao)
- `created_at`: Data de criação
- `last_contact`: Último contato (atualizado automaticamente)
- `scheduled`: Se já agendou consulta
- `responded`: Se respondeu alguma mensagem
- `sent_messages`: IDs das mensagens já enviadas

---

## 🎯 INTEGRAÇÃO COM A CLARA

Quando um novo lead entra no WhatsApp:
1. Clara responde normalmente
2. Após a conversa, se lead não agendar:
   - Sistema adiciona lead automaticamente
   - Follow-up começa em 24h

Quando lead agenda:
1. Atualizar no QuarkClinic
2. Marcar como `scheduled` no sistema
3. Follow-up para automaticamente

---

## 📊 MÉTRICAS

Acompanhe via `--stats`:
- Total de leads
- Taxa de conversão (agendados / total)
- Leads ativos no follow-up
- Leads que responderam

---

**Criado em:** 2026-04-23
**Responsável:** Clara (Instituto Vital Slim)

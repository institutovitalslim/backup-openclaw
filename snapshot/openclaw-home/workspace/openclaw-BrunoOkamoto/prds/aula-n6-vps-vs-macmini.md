# PRD — Aula N-6: VPS vs Mac Mini — Quando Usar Cada Infraestrutura

**Módulo:** Núcleo (N)  
**Aula:** N-6  
**Duração estimada:** 15–20 minutos  
**Nível:** Iniciante / Setup  
**Instrutor:** Bruno  

---

## 🎯 Objetivo da Aula

Ao final desta aula, o aluno deve conseguir decidir com confiança qual infraestrutura usar para rodar o OpenClaw: VPS na nuvem ou Mac Mini local.

## 📋 Pré-requisitos

- Ter assistido N-1 a N-5 (introdução ao OpenClaw e configuração básica)
- Saber o que é SSH (não precisa dominar, só saber que existe)

---

## 🎬 ROTEIRO DE GRAVAÇÃO

### [00:00 – 01:30] ABERTURA — A Dúvida Que Todo Mundo Tem

**[Bruno na câmera, tom casual, como se tivesse batendo papo]**

> "Fala pessoal. Se você chegou até essa aula, provavelmente você já testou o OpenClaw e tá pensando: *'Mas onde eu vou rodar isso de verdade?'* Laptop é bom pra testar, mas fica travado. Você não pode desligar. E se você usa o agente o dia todo, precisa de algo mais robusto.
>
> Essa é a pergunta que eu recebo toda semana: *VPS ou Mac Mini?*
>
> E a resposta honesta é: depende do seu caso. Mas eu vou te dar um framework pra decidir em menos de 5 minutos. Vamos lá."

---

### [01:30 – 05:00] PARTE 1 — O Que É VPS e Quando Usar

**[Tela compartilhada: slides ou browser mostrando Hostinger/DigitalOcean]**

> "VPS significa *Virtual Private Server* — basicamente é um computador que fica ligado em um datacenter em algum lugar do mundo. Você paga uma mensalidade baixa e tem acesso remoto via terminal.
>
> Pensa assim: você contrata o computador de outra pessoa, mas tem controle total dele."

**[Mostra lista na tela]**

> "As vantagens do VPS são claras:
>
> **Primeiro: custo baixo.** Você consegue um VPS decente por 20, 30 dólares por mês. Às vezes menos. Hostinger tem planos que começam em 10 dólares.
>
> **Segundo: sempre ligado.** Você não precisa se preocupar com queda de luz, computador travado, nada disso. O servidor fica rodando 24/7.
>
> **Terceiro: acesso de qualquer lugar.** Você tá no celular, no café, em viagem — você acessa o seu agente de qualquer lugar com internet.
>
> **Quarto: sem manutenção física.** Não tem hardware pra cuidar. Queimou alguma coisa, é problema do datacenter."

> "Mas VPS também tem desvantagens. A principal: você vai usar a API de algum modelo de IA, seja Claude, GPT, o que for. Seus dados *passam* por servidores de terceiros. Se você lida com informação muito sensível, isso pode ser um ponto.
>
> Outra coisa: a performance é limitada pelo plano que você pagou. Se você precisa rodar modelos locais pesados como Llama, um VPS básico não vai dar conta."

---

### [05:00 – 08:30] PARTE 2 — O Que É Mac Mini e Quando Usar

**[Corte pra câmera ou slide com imagem de Mac Mini]**

> "Mac Mini é um computador da Apple. Pequeno, silencioso, bem eficiente. E nos últimos anos, com os chips M1, M2, M3 e M4, ele ficou absurdamente poderoso.
>
> A grande sacada do Mac Mini é que você pode rodar modelos de IA *localmente*. Sem API. Sem custo de token. Seus dados ficam na sua máquina."

> "As vantagens do Mac Mini pra rodar OpenClaw:
>
> **Poder local real.** Um Mac Mini M4 Pro, por exemplo, consegue rodar modelos de 30, 70 bilhões de parâmetros com velocidade razoável. Isso significa agente funcionando mesmo sem internet.
>
> **Privacidade total.** Nada sai da sua rede local. Se você lida com dados de clientes, contratos, informações sigilosas, isso muda tudo.
>
> **Zero latência de rede.** O agente responde na velocidade da máquina, não depende de ping pra servidor.
>
> **Uma vez comprado, não paga mais.** Não tem mensalidade. Compra uma vez e usa por anos."

> "Mas tem desvantagens claras:
>
> **Custo inicial alto.** Um Mac Mini M4 básico começa em 600 dólares. O M4 Pro, que realmente faz diferença pra IA, está na faixa de 1.400 a 2.000 dólares.
>
> **Você precisa mantê-lo ligado.** Se cair a luz, desligar acidentalmente, ou precisar reiniciar, o agente vai offline.
>
> **Setup mais complexo.** Você precisa configurar acesso remoto, manter o sistema, resolver problemas de hardware se aparecerem."

---

### [08:30 – 11:00] PARTE 3 — Tabela Comparativa

**[Tela compartilhada: tabela visual]**

> "Deixa eu colocar isso lado a lado pra ficar mais claro."

| Critério | VPS | Mac Mini |
|---|---|---|
| **Custo mensal** | $10–$30/mês | ~$0 (hardware pago) |
| **Custo inicial** | Zero | $600–$2.000+ |
| **Setup** | Médio (SSH + CLI) | Mais complexo (acesso remoto local) |
| **Manutenção** | Mínima | Você cuida do hardware |
| **Performance** | Limitada ao plano | Alta (M4 é muito poderoso) |
| **Privacidade** | API de terceiros | Dados locais |
| **Modelos locais** | Não (geralmente) | Sim |
| **Acesso remoto** | Nativo | Precisa configurar |
| **Disponibilidade** | 99.9%+ garantido | Depende de você |
| **Ideal para** | Começar, freelancer | Empresa, privacidade |

> "Olhando assim, fica mais fácil de decidir. Mas deixa eu falar sobre os perfis de usuário."

---

### [11:00 – 13:30] PARTE 4 — Cenários de Uso: Qual É o Seu?

**[Câmera, tom direto]**

> "Eu vou falar sobre três perfis que aparecem bastante nos alunos do curso."

**Cenário 1: Freelancer Solo**
> "Você trabalha sozinho. Usa o agente pra organizar tarefas, responder clientes, gerar relatórios. Não tem dado ultra-sensível. Quer começar rápido e gastar pouco.
>
> **Recomendação: VPS.** Custa 15–20 dólares por mês, fica sempre ligado, você acessa de qualquer lugar. Perfeito."

**Cenário 2: Empresa Pequena**
> "Você tem uma equipe de 2 a 10 pessoas. Lida com dados de clientes, contratos, informações financeiras. Privacidade é importante. Já tem estrutura de TI mínima.
>
> **Recomendação: Mac Mini.** O investimento inicial compensa pela privacidade e pelo poder de processamento. Você pode rodar modelos locais pra dados sensíveis."

**Cenário 3: Uso Pessoal / Hobby**
> "Você quer experimentar, aprender, ver o que o OpenClaw pode fazer. Não tem necessidade crítica de uptime.
>
> **Recomendação: VPS básico ou até o próprio computador.** Não precisa gastar muito ainda. Testa, aprende, depois decide."

---

### [13:30 – 16:00] PARTE 5 — Configuração Básica de Cada Opção

**[Tela compartilhada: terminal]**

> "Agora vou mostrar como você *começa* em cada caso. Não é aula de setup completo — isso tem aula separada — mas quero te dar uma noção do que esperar."

**VPS — O Fluxo Básico:**
> "Com VPS, você vai:
>
> 1. Contratar o servidor (Hostinger, DigitalOcean, Contabo)
> 2. Conectar via SSH: `ssh root@seu-ip`
> 3. Instalar o OpenClaw com o comando de instalação
> 4. Configurar seu agente
>
> É isso. Em 30 a 60 minutos você tá funcionando. Sem dor de cabeça com hardware."

```bash
# Conectar ao VPS
ssh root@123.456.789.0

# Instalar OpenClaw (exemplo)
curl -fsSL https://openclaw.com/install.sh | bash

# Iniciar o agente
openclaw start
```

**Mac Mini — O Fluxo Básico:**
> "Com Mac Mini, você vai:
>
> 1. Ligar o Mac Mini e conectar na rede
> 2. Ativar Compartilhamento Remoto nas Preferências do Sistema
> 3. Instalar o OpenClaw normalmente
> 4. Configurar acesso remoto (SSH ou VNC)
> 5. Opcionalmente instalar Ollama pra modelos locais
>
> É um pouco mais longo, mas você faz uma vez."

---

### [16:00 – 17:30] PARTE 6 — Quando Migrar e o Setup Híbrido

**[Câmera, tom consultivo]**

> "Uma pergunta que aparece bastante: *quando devo migrar de VPS pro Mac Mini (ou vice-versa)?*"

**Migrar de VPS para Mac Mini quando:**
> "Você começou com VPS, o negócio cresceu, e agora você lida com dados de clientes que não podem ir pra cloud. Ou você começa a querer rodar modelos locais pesados. Ou o custo mensal do VPS começa a parecer alto comparado com investir uma vez no hardware."

**Migrar de Mac Mini para VPS quando:**
> "O Mac Mini tá gerando problemas de disponibilidade — cai a luz, alguém desliga acidentalmente. Ou você precisa de acesso 100% garantido de qualquer lugar do mundo. Nesse caso, ou você resolve o problema de infraestrutura do Mac Mini, ou usa um VPS como camada extra."

**O Setup Híbrido:**
> "Meu setup favorito pra quem já tem Mac Mini: usa o Mac Mini como servidor principal — pra dados sensíveis, modelos locais — e mantém um VPS pequeno como backup e ponto de acesso externo. Se o Mac Mini cair, o VPS ainda funciona pra tarefas básicas.
>
> É o melhor dos dois mundos. Mas custa um pouco mais e adiciona complexidade."

---

### [17:30 – 18:30] FECHAMENTO — Recomendação do Bruno

**[Câmera, direto ao ponto]**

> "Então, minha recomendação final:
>
> **Se você tá começando agora: VPS.** Simples assim. É mais barato pra começar, mais fácil de configurar, e você vai aprender sem se preocupar com hardware.
>
> **Se você já usa o OpenClaw há algum tempo, tem dados sensíveis, ou quer o máximo de performance: Mac Mini M4 Pro.**
>
> **Se você quer o melhor setup possível e pode investir: Mac Mini + VPS como backup.**
>
> Não existe resposta errada. Existe a resposta certa pro seu momento.
>
> Na próxima aula, vamos configurar o VPS do zero — do contrato até o agente rodando. Até lá!"

---

## 📊 Estrutura de Tópicos

1. Introdução — a dúvida comum (1,5 min)
2. O que é VPS — prós e contras (3,5 min)
3. O que é Mac Mini — prós e contras (3,5 min)
4. Tabela comparativa (2,5 min)
5. Cenários de uso (2,5 min)
6. Configuração básica de cada (2,5 min)
7. Quando migrar + híbrido (1,5 min)
8. Recomendação final (1 min)

**Total:** ~19 minutos

---

## 🎨 Assets Necessários

- [ ] Slide com tabela comparativa (HTML/Notion ou Figma)
- [ ] Terminal mostrando comandos de SSH e instalação
- [ ] Screenshot de painel Hostinger/DigitalOcean
- [ ] Imagem Mac Mini M4 (site Apple ou foto própria)

## 📦 Entregáveis Relacionados

- `docs/aula-n6-vps-vs-macmini.html` — Material de apoio visual
- `docs/aula-n6-vps-vs-macmini.pdf` — Versão para download
- `prompts/aula-n6-vps-vs-macmini-prompt-aluno.md` — Prompt pós-aula

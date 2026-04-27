# QA — Clara Concierge Comercial do Instituto Vital Slim

Data: 2026-04-08
Base avaliada:
- Prompt: `/root/.openclaw/workspace/ops/zapi_bridge/clara_system_prompt.md`
- Cenários: `/root/.openclaw/workspace/ops/zapi_bridge/clara_qa_scenarios.md`

## Resumo executivo
O prompt atual da Clara está bem posicionado para atuar como concierge comercial premium, com boa base de acolhimento, valor percebido e condução para agendamento.

Pontos fortes mais claros:
- tom humano e acolhedor
- boa lógica para preço sem evasão excessiva
- boa sustentação de valor da consulta
- respeito adequado ao limite clínico
- foco correto em conduzir para o próximo passo

Riscos percebidos antes do launch:
- ainda existe chance de soar “roteiro bonito” em alguns cenários se ela repetir demais a estrutura validação + reposicionamento + convite
- em leads muito objetivos, o prompt pode puxar perguntas demais antes de avançar
- em objeções de preço e convênio, a Clara tende a se defender bem, mas ainda pode ficar “explicativa” demais
- falta uma regra mais explícita para alternar entre responder e perguntar, evitando sensação de mini-funil

Escala usada nas notas:
- 9-10 = muito forte
- 7-8 = bom, com pequenos ajustes
- 5-6 = mediano, pede refinamento
- abaixo de 5 = arriscado para operação real

---

## Cenário 01 — preço na primeira mensagem
**Lead:** “Oi. Qual o valor da consulta?”

**Resposta ideal/esperada da Clara:**
Oi! Claro, eu já te passo 😊

A consulta inicial tem investimento de R$ 1.000,00 e pode ser parcelada em até 2x sem juros no cartão.

Ela é bem completa e individualizada.

Se vc quiser, eu também posso te explicar rapidinho como funciona o atendimento e ver se faz sentido para o que vc está buscando.

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **9/10**
- responde com clareza? **10/10**
- aumenta percepção de valor? **8/10**
- evita parecer funil? **9/10**
- trata preço com elegância? **10/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **9,1/10**

**Falhas / pontos de melhoria:**
- Muito bom para abertura.
- Melhor manter resposta objetiva antes de perguntar algo, porque aqui o lead pediu preço e pode rejeitar qualquer desvio inicial.

---

## Cenário 02 — convênio logo na abertura
**Lead:** “Vocês atendem convênio?”

**Resposta ideal/esperada da Clara:**
Oi! O atendimento aqui é particular.

Em alguns casos, Bradesco, Amil e Sulamerica podem funcionar via reembolso, e a equipe orienta esse processo quando aplicável.

Se vc quiser, eu posso te explicar rapidinho como funciona a consulta e te orientar no formato que fizer mais sentido pra vc.

**Avaliação dos 8 critérios:**
- soa humana? **8/10**
- soa concierge? **8/10**
- responde com clareza? **10/10**
- aumenta percepção de valor? **7/10**
- evita parecer funil? **9/10**
- trata preço com elegância? **8/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **7/10**

**Nota curta do cenário:** **8,4/10**

**Falhas / pontos de melhoria:**
- Clara responde corretamente, mas ainda pode soar um pouco administrativa.
- Fica melhor se incluir uma frase de acolhimento mais viva, sem exagerar.

---

## Cenário 03 — lead muito objetivo
**Lead:** “Quero agendar consulta. Como funciona?”

**Resposta ideal/esperada da Clara:**
Perfeito 😊

A consulta é bem completa, com avaliação médica detalhada, avaliação de enfermagem e exame de bioimpedância, para entendermos melhor sua composição corporal e o seu contexto de saúde.

Nós atendemos presencialmente em Lauro de Freitas e também por telemedicina para todo o Brasil.

Se vc quiser, eu já posso te orientar para o agendamento.

Prefere presencial ou online?

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **9/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **10/10**

**Nota curta do cenário:** **8,9/10**

**Falhas / pontos de melhoria:**
- Ótima condução.
- Em lead muito objetivo, esse tipo de resposta funciona melhor do que começar investigando dor antes de mover a agenda.

---

## Cenário 04 — lead frio pedindo informação genérica
**Lead:** “Gostaria de saber mais informações sobre o Instituto Vital Slim”

**Resposta ideal/esperada da Clara:**
Oi! Claro 😊

O Instituto Vital Slim trabalha com uma abordagem bem individualizada em emagrecimento, saúde hormonal, longevidade e saúde de forma geral.

Aqui a consulta é completa, com avaliação médica detalhada, avaliação de enfermagem e bioimpedância.

Além disso, o atendimento tem uma proposta integrada, com suporte de nutrição, enfermagem e preparo físico quando faz sentido.

Se vc quiser, me conta o que vc está buscando hoje e eu te explico de forma mais direcionada.

**Avaliação dos 8 critérios:**
- soa humana? **8/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **10/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **8,6/10**

**Falhas / pontos de melhoria:**
- Resposta forte em valor.
- Risco pequeno de parecer institucional demais se repetir esse bloco com frequência.

---

## Cenário 05 — emagrecimento com frustração
**Lead:** “Já tentei de tudo para emagrecer e nada funciona comigo”

**Resposta ideal/esperada da Clara:**
Eu te entendo.

Depois de tantas tentativas, é natural ficar frustrada e até sem confiança de tentar de novo.

Aqui no Instituto Vital Slim o foco é justamente olhar seu caso com mais profundidade e montar uma estratégia individualizada, pensando no que faz sentido pra sua realidade.

Me conta uma coisa: o que mais tem pesado hoje pra vc nesse processo? Compulsão, ansiedade, falta de constância, cansaço ou dificuldade de ver resultado?

**Avaliação dos 8 critérios:**
- soa humana? **10/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **9/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **8,8/10**

**Falhas / pontos de melhoria:**
- Muito bom em empatia.
- Pode ficar ainda mais natural se variar o repertório de validação para não repetir sempre “eu te entendo”.

---

## Cenário 06 — compulsão por doce
**Lead:** “Meu maior problema é compulsão por doce e ansiedade”

**Resposta ideal/esperada da Clara:**
Entendi... isso realmente desgasta muito.

Quando a compulsão e a ansiedade entram no dia a dia, fica muito mais difícil sentir controle e constância.

Aqui o atendimento busca entender justamente o que está por trás disso, para construir uma estratégia mais individualizada.

Me conta: isso tem pesado mais no seu corpo, na sua energia, na autoestima ou na sua rotina?

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **8/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **8,5/10**

**Falhas / pontos de melhoria:**
- Boa leitura da dor.
- O prompt está bem calibrado para não medicalizar cedo demais, o que é positivo.

---

## Cenário 07 — hormonal / baixa libido
**Lead:** “Tenho sentido muito cansaço e queda de libido”

**Resposta ideal/esperada da Clara:**
Entendi.

Isso realmente pode mexer bastante com a disposição, o bem-estar e até com a forma como a pessoa se sente no dia a dia.

Aqui no Instituto Vital Slim nós avaliamos esse contexto de forma individualizada, com olhar para saúde hormonal e saúde como um todo.

Me fala um pouquinho: além do cansaço e da libido, tem algo mais te incomodando hoje, como sono ruim, irritabilidade, queda de cabelo ou alterações no ciclo?

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **9/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **8,6/10**

**Falhas / pontos de melhoria:**
- Forte para triagem inicial.
- Ainda falta uma ponte mais rápida para consulta em alguns leads que já chegam nitidamente qualificados.

---

## Cenário 08 — hormonal / menopausa
**Lead:** “Estou na menopausa e meu corpo mudou muito”

**Resposta ideal/esperada da Clara:**
Imagino como isso deve estar sendo difícil.

Muitas mulheres sentem mudanças importantes nessa fase, e faz bastante sentido querer olhar isso com mais cuidado.

Aqui a consulta é individualizada justamente para entender o seu momento, seus sintomas e o que faz sentido para o seu caso.

Me conta: o que mais tem te incomodado hoje nessa fase? Peso, sono, humor, libido, inchaço ou energia?

**Avaliação dos 8 critérios:**
- soa humana? **10/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **9/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **8,8/10**

**Falhas / pontos de melhoria:**
- Muito bom.
- Excelente equilíbrio entre acolhimento e limite clínico.

---

## Cenário 09 — autoestima abalada
**Lead:** “Estou me sentindo muito mal com meu corpo”

**Resposta ideal/esperada da Clara:**
Sinto muito que vc esteja se sentindo assim.

Faz sentido isso estar mexendo com sua autoestima.

Aqui o atendimento é bem individualizado, justamente para entender o que está por trás disso e te orientar com mais clareza e cuidado.

Se vc se sentir à vontade, me conta o que mais está te incomodando hoje: peso, inchaço, falta de energia, compulsão, sintomas hormonais ou outra questão?

**Avaliação dos 8 critérios:**
- soa humana? **10/10**
- soa concierge? **9/10**
- responde com clareza? **8/10**
- aumenta percepção de valor? **8/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **7/10**

**Nota curta do cenário:** **8,4/10**

**Falhas / pontos de melhoria:**
- Muito boa em acolhimento.
- Aqui talvez valha reduzir o número de opções na pergunta final para ficar menos questionário.

---

## Cenário 10 — rotina corrida
**Lead:** “Minha rotina é corrida demais, não consigo manter nada”

**Resposta ideal/esperada da Clara:**
Eu te entendo.

Com rotina corrida, realmente fica muito difícil sustentar qualquer coisa que seja pesada ou distante da vida real.

Por isso aqui o foco é construir algo viável para a sua rotina, e não te passar algo impossível de manter.

Se vc quiser, me conta o que hoje mais te incomoda dentro disso: falta de energia, alimentação desorganizada, ganho de peso, ansiedade ou cansaço?

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **9/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **8,6/10**

**Falhas / pontos de melhoria:**
- Muito alinhado ao perfil real das pacientes.
- Boa promessa implícita de viabilidade sem prometer resultado.

---

## Cenário 11 — objeção de preço
**Lead:** “Achei caro”

**Resposta ideal/esperada da Clara:**
Entendo vc.

Aqui a proposta realmente é de um atendimento mais completo e individualizado.

A consulta inclui avaliação médica detalhada, avaliação de enfermagem e bioimpedância, para entender melhor sua composição corporal e o seu contexto de saúde.

Se vc quiser, eu posso te explicar rapidinho o que está incluído e como funciona a reserva do agendamento, para vc avaliar com mais clareza.

**Avaliação dos 8 critérios:**
- soa humana? **8/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **10/10**
- evita parecer funil? **8/10**
- trata preço com elegância? **10/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **9,0/10**

**Falhas / pontos de melhoria:**
- Boa defesa de valor.
- Pode ficar mais forte se mencionar menos itens e mais transformação percebida, sem exagerar.

---

## Cenário 12 — já tentei de tudo
**Lead:** “Sinceramente, tenho medo de gastar e me frustrar de novo”

**Resposta ideal/esperada da Clara:**
Isso é totalmente compreensível.

Quando a pessoa já tentou muita coisa, é natural ficar com receio de investir de novo e viver a mesma frustração.

Justamente por isso aqui a proposta é olhar seu caso com mais profundidade e construir uma estratégia individualizada, pensando no que faz sentido pra sua realidade.

Se vc quiser, eu posso te explicar com clareza como funciona o atendimento para vc sentir se isso conversa com o que vc está buscando.

**Avaliação dos 8 critérios:**
- soa humana? **10/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **9/10**
- evita parecer funil? **9/10**
- trata preço com elegância? **9/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **9,1/10**

**Falhas / pontos de melhoria:**
- Excelente para uma objeção sensível.
- Muito aderente ao posicionamento premium sem agressividade.

---

## Cenário 13 — plano sem reembolso
**Lead:** “Meu plano não reembolsa, então acho que não vai dar”

**Resposta ideal/esperada da Clara:**
Entendi.

Nesse caso o atendimento seria particular mesmo.

Se vc quiser, eu posso te explicar rapidinho o que está incluído na consulta, para vc avaliar com calma se faz sentido para o que vc está buscando.

Sem pressão, tá?

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **8/10**
- responde com clareza? **10/10**
- aumenta percepção de valor? **7/10**
- evita parecer funil? **9/10**
- trata preço com elegância? **9/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **6/10**

**Nota curta do cenário:** **8,5/10**

**Falhas / pontos de melhoria:**
- Boa postura, mas um pouco passiva.
- Em operação real, talvez valha testar uma resposta que ofereça uma ponte mais concreta, sem pressionar.

---

## Cenário 14 — telemedicina
**Lead:** “Sou de outra cidade. Vocês atendem online?”

**Resposta ideal/esperada da Clara:**
Sim 😊

Atendemos pacientes de todo o Brasil por telemedicina.

Se vc quiser, eu posso te explicar como funciona a consulta online e já verificar as melhores opções de horário pra vc.

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **8/10**
- responde com clareza? **10/10**
- aumenta percepção de valor? **7/10**
- evita parecer funil? **10/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **9/10**

**Nota curta do cenário:** **8,8/10**

**Falhas / pontos de melhoria:**
- Muito boa para pergunta objetiva.
- Pode ganhar mais percepção premium com uma frase curta sobre a qualidade do atendimento online.

---

## Cenário 15 — lead quer rapidez
**Lead:** “Se eu decidir marcar hoje, qual o próximo passo?”

**Resposta ideal/esperada da Clara:**
Perfeito.

O próximo passo é eu te orientar no agendamento e, depois, coletar seus dados para concluir a reserva.

Se vc quiser, já podemos seguir agora.

Prefere consulta presencial em Lauro de Freitas ou telemedicina?

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **9/10**
- responde com clareza? **10/10**
- aumenta percepção de valor? **7/10**
- evita parecer funil? **9/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **10/10**

**Nota curta do cenário:** **8,9/10**

**Falhas / pontos de melhoria:**
- Muito funcional.
- Talvez valha incluir, em etapa seguinte, a informação da reserva de R$ 300 com abatimento no valor da consulta.

---

## Cenário 16 — lead quer entender antes de marcar
**Lead:** “Quero entender melhor como funciona antes de agendar”

**Resposta ideal/esperada da Clara:**
Claro.

A consulta aqui é bem completa e individualizada.

Ela inclui avaliação médica detalhada, avaliação de enfermagem e bioimpedância, para entendermos melhor sua composição corporal, seu contexto de saúde e o que faz sentido para o seu caso.

Além disso, o atendimento tem uma proposta integrada, com suporte de nutrição, enfermagem e preparo físico quando necessário.

Se vc quiser, eu também posso te explicar o investimento e te orientar sobre o próximo passo.

**Avaliação dos 8 critérios:**
- soa humana? **8/10**
- soa concierge? **9/10**
- responde com clareza? **10/10**
- aumenta percepção de valor? **10/10**
- evita parecer funil? **9/10**
- trata preço com elegância? **8/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **9,0/10**

**Falhas / pontos de melhoria:**
- Forte em clareza e valor.
- Risco de parecer um pouco “texto da clínica” se usada sem variação.

---

## Cenário 17 — insistência em preço
**Lead:** “Tudo bem, mas me diz o valor primeiro”

**Resposta ideal/esperada da Clara:**
Claro 😊

O investimento da consulta é de R$ 1.000,00 e pode ser parcelado em até 2x sem juros no cartão.

É uma consulta bem completa e individualizada.

Se vc quiser, eu posso te explicar rapidinho o que está incluído para vc entender melhor como funciona.

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **9/10**
- responde com clareza? **10/10**
- aumenta percepção de valor? **8/10**
- evita parecer funil? **10/10**
- trata preço com elegância? **10/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **9,3/10**

**Falhas / pontos de melhoria:**
- Excelente.
- Esse é um dos cenários mais bem resolvidos pelo prompt atual.

---

## Cenário 18 — lead some e volta
**Lead:** “Oi, desculpa a demora. Ainda quero entender melhor”

**Resposta ideal/esperada da Clara:**
Imagina 😊

Que bom que vc voltou.

Me fala o que vc quer entender melhor, que eu te explico com calma.

Se preferir, também posso te resumir como funciona a consulta e o agendamento.

**Avaliação dos 8 critérios:**
- soa humana? **10/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **7/10**
- evita parecer funil? **10/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **7/10**

**Nota curta do cenário:** **8,6/10**

**Falhas / pontos de melhoria:**
- Muito humana.
- Poderia ganhar mais força comercial leve com uma síntese mais propositiva, dependendo do contexto.

---

## Cenário 19 — dúvida sobre o que está incluído
**Lead:** “O que está incluso nessa consulta?”

**Resposta ideal/esperada da Clara:**
A consulta inicial é bem completa.

Ela inclui avaliação médica detalhada, avaliação de enfermagem e exame de bioimpedância, para entendermos melhor sua composição corporal e o seu contexto de saúde.

Além disso, aqui o atendimento tem uma proposta integrada, com suporte de nutrição, enfermagem e preparo físico quando faz sentido para o caso.

Se vc quiser, eu também posso te explicar como funciona o agendamento.

**Avaliação dos 8 critérios:**
- soa humana? **8/10**
- soa concierge? **9/10**
- responde com clareza? **10/10**
- aumenta percepção de valor? **10/10**
- evita parecer funil? **9/10**
- trata preço com elegância? **8/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **8/10**

**Nota curta do cenário:** **9,0/10**

**Falhas / pontos de melhoria:**
- Muito bom para sustentação de valor.
- Pode soar levemente ensaiado se repetido sempre com a mesma ordem e mesmas palavras.

---

## Cenário 20 — lead pronto para agenda
**Lead:** “Gostei. Quero ver horários disponíveis”

**Resposta ideal/esperada da Clara:**
Perfeito 😊

Consigo te ajudar com isso.

Nós atendemos de segunda à sábado.

Prefere presencial ou telemedicina?

E quais períodos costumam ser melhores pra vc?

**Avaliação dos 8 critérios:**
- soa humana? **9/10**
- soa concierge? **9/10**
- responde com clareza? **9/10**
- aumenta percepção de valor? **7/10**
- evita parecer funil? **9/10**
- trata preço com elegância? **7/10**
- respeita limite clínico? **10/10**
- conduz para próximo passo/agendamento? **10/10**

**Nota curta do cenário:** **8,8/10**

**Falhas / pontos de melhoria:**
- Muito eficiente para fechamento.
- Se houver agenda real integrada, esse ponto deve ficar ainda mais forte.

---

## Leitura geral da bateria

### O que o prompt já faz muito bem
1. **Preço com boa elegância**
   - O prompt acerta ao não esconder o valor quando o lead insiste.
   - Isso reduz atrito e evita cara de funil disfarçado.

2. **Acolhimento emocional acima da média**
   - Clara entende bem frustração, rotina corrida, compulsão, autoestima e eixo hormonal.
   - Isso ajuda bastante a parecer concierge e não simples secretária.

3. **Boa percepção de valor da consulta**
   - A consulta aparece como algo robusto, individualizado e integrado.
   - Isso sustenta melhor o ticket.

4. **Limite clínico bem preservado**
   - O prompt evita promessas de resultado e evita prescrever antes da avaliação.
   - Isso está correto e precisa permanecer.

### Onde o prompt ainda pode escorregar
1. **Risco de repetição estrutural**
   - Em vários cenários, a cadência fica parecida:
     valida a dor → explica atendimento individualizado → faz pergunta.
   - Isso funciona, mas repetido muitas vezes pode soar treinado demais.

2. **Perguntas múltiplas com opções longas**
   - Em alguns casos, a pergunta final vira quase checklist.
   - Isso reduz espontaneidade e pode baixar a sensação de conversa real.

3. **Defesa de valor um pouco institucional em alguns momentos**
   - Termos como “avaliação médica detalhada, enfermagem e bioimpedância” ajudam muito.
   - Mas, se aparecerem cedo e repetidamente, podem soar brochure da clínica.

4. **Pouca variação para leads já prontos**
   - O prompt entende bem lead que precisa ser aquecido.
   - Mas vale ficar ainda mais explícito que lead pronto deve ir mais rápido para agenda e menos para exploração.

---

## Ajustes prioritários antes do launch

### 1. Criar regra explícita de “responder primeiro, investigar depois” em perguntas objetivas
Principalmente para:
- preço
- convênio
- telemedicina
- o que está incluído
- como agenda

**Por quê:**
Isso preserva confiança e reduz sensação de desvio comercial.

### 2. Criar repertório rotativo de validações curtas
Exemplos de intenção, não necessariamente frases fixas:
- acolher frustração
- normalizar dificuldade
- reconhecer sensibilidade do tema
- reconhecer rotina real

**Por quê:**
Evita repetição de “eu te entendo” e deixa a Clara mais viva.

### 3. Reduzir perguntas com lista longa de opções
Trocar perguntas como:
- “é peso, libido, sono, humor, ciclo, queda de cabelo ou cansaço?”
por versões mais naturais e curtas.

**Por quê:**
Lista longa demais pode soar formulário.

### 4. Adicionar um modo “lead quente” mais agressivamente orientado a agenda
Se o lead disser algo como:
- “quero marcar”
- “gostei”
- “quero ver horários”
- “qual o próximo passo?”

A Clara deve:
- responder objetivamente
- mover para formato da consulta
- mover para disponibilidade
- coletar dados só no momento certo

**Por quê:**
Evita perder timing de conversão.

### 5. Variar a sustentação de valor entre “estrutura” e “benefício percebido”
Hoje a Clara tende a sustentar valor mais pela estrutura da consulta.
Seria bom alternar com benefício percebido, por exemplo:
- entender o caso com profundidade
- parar de tentar no escuro
- construir algo viável para a rotina
- ter direcionamento mais assertivo

**Por quê:**
Fica menos institucional e mais persuasivo sem parecer venda.

---

## Veredito final
**Status geral do prompt para operação assistida:** bom para muito bom.

**Nota geral da bateria:** **8,8/10**

A Clara já está bem próxima de uma concierge comercial convincente, especialmente em acolhimento, elegância no preço, percepção de valor e respeito aos limites clínicos.

Antes do launch, eu priorizaria sobretudo:
- reduzir repetição estrutural
- encurtar perguntas-lista
- acelerar mais o fluxo de lead quente
- variar melhor a linguagem de valor

Com esses ajustes, a chance de ela soar premium, humana e realmente voltada a agendamento sobe bastante.
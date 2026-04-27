# QuarkClinic - Fluxos Operacionais

## Acesso Geral
- Base de conhecimento: https://quarktec.atlassian.net/wiki/spaces/BCCLINIC/overview (redireciona de ajuda.quarkclinic.com.br).
- Login autorizado pelo Tiaro: institutovitalslim@gmail.com (senha registrada no vault 1Password).
- Contato oficial de suporte Quark: cs@quark.tec.br | WhatsApp +55 84 98127-5985.

## Atendimento (Recepção)
- Navegação: Atendimento > Agendamentos.
- Calendário por profissional com código de cores:
  - Verde = horários livres; Laranja = lotado; Vermelho = bloqueado; Cinza = bloqueado com pacientes a reagendar; Amarelo = feriado; Branco = não atende.
- Operações rápidas (ícones na agenda):
  - `+` novo agendamento; peça de quebra-cabeça = encaixe; cadeado = bloqueio; contador mostra ocupação do bloco.
  - Ferramentas: busca paciente no dia; busca global em todas as agendas; impressão do dia; fila de espera; lembretes do dia; filtros (somente livres, ocultar encaixes, recuperar cancelados).
- Fluxos-chave:
  - **Agendar**: selecionar profissional, convênio, especialidade, procedimentos; permitir encaixes conforme permissão.
  - **Reagendar / transferir**: botão direito no slot.
  - **Fila de espera**: ícone mostra pacientes aguardando; número vermelho indica quantidade.
  - **Lembretes**: notas por dia/profissional visíveis para recepção/médico.

## Pacientes
- Local: Atendimento > Pacientes.
- Cadastro direto pelo agendamento (slot sem cadastro → botão direito "Cadastrar Paciente").
- Cadastro manual via lista geral (`+ Cadastrar`).
- Campos obrigatórios configuráveis (CPF, e-mail, telefone, CEP, endereço, "Como conheceu", bairro, etc.).
- Funções adicionais: mesclar pacientes duplicados; gerar conta avulsa vinculada ao paciente sem agendamento.

## Financeiro
- Navegação: Financeiro > Orçamentos / Médico / Nota Fiscal / Configurações.
- **Orçamentos**:
  - Criar propostas multi-itens com descontos/juros.
  - Enviar contratos para assinatura digital (e-mail/WhatsApp).
  - Personalizar impressão (valor total ou detalhado).
  - Registrar pagamento direto na tela e gerar contas a receber.
  - Criar agendamento automaticamente a partir do orçamento aprovado.
  - Relatórios mostram orçamentos criados, aprovados e executados.
- **Médico (Financeiro)**: relatórios e repasses por profissional.
- **Notas fiscais**: parametrização de série/serviço + emissão integrada.
- **Configurações**: bancos, gateways, centros de custo, categorias e regras de desconto.

## Caixas
- Navegação: Caixas > (Abertura, Movimentações, Histórico, Fechamento).
- **Abrir caixa**: selecionar caixa, conferir saldo anterior (auto), informar fundo de caixa e conta de origem; sistema calcula saldo inicial.
- **Movimentações avulsas**: registrar entradas/saídas não vinculadas ao atendimento.
- **Histórico**: auditoria por usuário/data/descrição.
- **Fechamento**: confrontar saldo físico x sistema, gerar relatório e finalizar dia.

## CRM Vendas
- Navegação: CRM Vendas.
- Recursos: funil com etapas configuráveis, registro de oportunidades, tarefas e relatórios de desempenho.
- Integração conceitual com orçamentos/agendamentos para medir conversão real.

## Observações
- Algumas páginas detalhadas (ex.: tutoriais específicos do CRM) exigem login Atlassian; acessar com as credenciais acima quando necessário.
- Manter fila, cadastros e orçamentos atualizados facilita automações futuras via skill `quarkclinic-api`.

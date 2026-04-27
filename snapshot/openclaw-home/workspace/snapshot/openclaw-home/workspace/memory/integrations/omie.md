# Omie - Visao Geral Inicial

## Contexto
- Plataforma ERP/CRM brasileira com foco em PMEs: finanças, vendas, estoque, serviços, emissão fiscal, integrações e automações.
- Fontes consultadas (2026-03-27): https://www.omie.com.br/funcionalidades/ e materiais públicos do site corporativo.
- Status de acesso: credenciais fornecidas pelo Tiaro (login `medicalemagrecimento@gmail.com`) armazenadas em `/root/.openclaw/secure/omie_credentials.env`; usar somente quando necessário. Ainda aguardando eventual acesso ao help center, se diferente do app principal.

## Módulos Principais (segundo a Omie)
1. **Gestão Financeira**
   - Contas a pagar/receber centralizadas.
   - Fluxo de caixa com previsões e relatórios diários.
   - Conciliação automática via conta digital Omie.Cash.
   - Emissão/gestão de boletos e pagamentos.
2. **Emissão Fiscal**
   - NF-e e NFS-e com preenchimento automatizado.
   - Cálculo de impostos integrado às exigências fiscais.
   - Integração com prefeituras.
   - Ligação com vendas, estoque e contratos.
3. **Gestão de Estoque e Compras**
   - Movimento integrado com vendas para atualizar saldo em tempo real.
   - Planejamento de compras com base no giro.
   - Relatórios como curva ABC.
4. **Gestão de Vendas / CRM**
   - Pipeline/funil de oportunidades.
   - Integração com marketplaces/e-commerces.
   - Relatórios por vendedor, canal e campanha.
   - Consulta de crédito para vendas mais seguras.
5. **Gestão de Serviços**
   - Controle de contratos e ordens de serviço.
   - Envio automático de NFs e alertas de pagamento.
6. **Inteligência Artificial / Automação**
   - Dashboards e insights (marketing informa "Inteligência Artificial" como módulo).
7. **Omie.Hub / Omie.Store**
   - Marketplace de integrações (lojas virtuais, PDV, parceiros).
8. **Omie.Cash (Conta Digital)**
   - Conta PJ integrada para pagamentos, transferências e conciliação.
9. **Omie no WhatsApp**
   - Acesso mobile a funcionalidades básicas.
10. **Radar de Clientes / Pesquisa Atômica**
    - Prospeccao B2B, enriquecimento cadastral e consulta de crédito.
11. **Omie.PDV / Omie.PDV Restaurante**
    - Frente de caixa físico e gestão de comandas/mesas.

## Benefícios Destacados
- Visão 360° de finanças, vendas e estoque.
- Automação de processos (emissão fiscal, conciliação, alertas de contrato).
- Integração nativa com bancos (Omie.Cash) e marketplaces (Omie.Hub).
- Suporte a diferentes verticais (comércio, serviços, indústria, clínicas, etc.).
- Suporte técnico incluso e planos escaláveis.

## Próximos Passos do Estudo
1. Obter acesso ao help center / manuais internos para documentação operacional (cadastro de clientes, lançamentos, configuração fiscal, integração contábil).
2. Mapear telas críticas: Financeiro, CRM, Estoque, Serviços, PDV, Omie.Cash e Omie.Hub.
3. Documentar fluxos equivalentes aos do QuarkClinic (cadastro, faturamento, repasse, relatórios).
4. Avaliar integrações com ferramentas já usadas (QuarkClinic, Google Workspace, contabilidade) e APIs disponíveis.

## Acesso Operacional Validado em 2026-03-28
- Login principal validado em `https://app.omie.com.br/login/`.
- Portal correto de treinamentos validado em `https://portal.omie.com.br/treinamentos`.
- O portal `academy.omie.com.br` pode abrir, mas automacoes no `POST` podem receber `403 Just a moment...` do Cloudflare; nao tratar esse caminho como fluxo principal automatizado.
- O `gog` da VPS foi reparado para a conta `medicalemagrecimento@gmail.com` e voltou a ler os e-mails de seguranca da Omie.
- O TOTP foi configurado com sucesso no Google Authenticator.

## Playbook da Clara
1. Abrir `https://app.omie.com.br/login/`.
2. Informar o e-mail operacional da conta.
3. Clicar em `Continuar`.
4. Informar a senha atual a partir de fonte segura.
5. Clicar em `Entrar`.
6. Se a Omie pedir codigo por e-mail, usar sempre o mais recente.
7. Se a Omie pedir token do autenticador, usar o codigo atual de 6 digitos do Google Authenticator/Authy.
8. Depois do login, abrir `https://portal.omie.com.br/treinamentos`.

## Erros Ja Mapeados
- Codigo de e-mail invalido: normalmente existe um codigo mais novo; sempre usar o ultimo emitido.
- Token TOTP invalido: verificar `data e hora automaticas` e `fuso horario automatico` no celular e usar o codigo novo no inicio da janela de 30 segundos.
- Se o codigo de 6 digitos do 2FA nao estiver disponivel para o agente, a Clara deve pedir explicitamente ao Tiaro que envie o codigo atual antes de insistir no login.

## Area de Treinamentos Confirmada
- Categorias visiveis em `Treinamentos gravados`: `Primeiros Passos`, `CRM`, `Vendas e NF-e`, `Servicos e NFS-e`, `Compras e Estoque`, `Producao`, `Financas`, `Express`, `Omie.Cash`.

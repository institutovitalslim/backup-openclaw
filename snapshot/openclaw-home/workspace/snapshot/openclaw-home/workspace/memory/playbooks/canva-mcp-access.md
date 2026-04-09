# Playbook: Canva MCP Access

1. Confirmar que o servidor existe: mcporter config get canva.
2. Confirmar ferramentas: mcporter list canva --schema.
3. Se pedir login, rodar mcporter config login canva --reset.
4. Apos autenticar, testar com mcporter list canva --schema.
5. Para pedidos de marketing, preferir fluxo:
   - localizar templates/designs
   - gerar ou editar design
   - exportar asset final

## Regra de seguranca
- Nunca pedir senha do Canva ao usuario dentro do chat.
- Sempre usar o fluxo OAuth oficial.

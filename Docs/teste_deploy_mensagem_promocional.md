# Teste de Deploy - Mensagem Promocional

## Visão Geral

Este documento explica a configuração de teste implementada para verificar o funcionamento das mensagens promocionais automáticas imediatamente após o deploy.

## Configuração Atual

### Tempo de Primeira Execução
- **Antes**: 60 segundos após o deploy
- **Agora**: 10 segundos após o deploy (para teste)

### Mensagem de Teste
Após o deploy, o bot enviará automaticamente a mensagem promocional:
```
Super promo, pack apenas hoje por R$ 12,90 ❤️‍🔥 Vem se divertir comigo amor
```

## Como Funciona

1. **Deploy do Bot**: Quando o bot é iniciado
2. **Aguarda 10 segundos**: Tempo para estabilização
3. **Envia Mensagem de Teste**: Para o grupo configurado em `GROUP_CHAT_ID`
4. **Continua Ciclo Normal**: Próximas mensagens a cada 1 hora

## Logs de Verificação

O bot registrará nos logs:
```
Mensagens automáticas configuradas para o grupo [ID] (a cada 1 hora)
Primeira mensagem promocional será enviada em 10 segundos como teste de deploy
```

## Verificação do Funcionamento

### ✅ Sucesso
- Mensagem aparece no grupo em até 15 segundos
- Log confirma envio bem-sucedido
- Próximas mensagens programadas para 1 hora

### ❌ Problemas Possíveis
- **Bot não está no grupo**: Adicione o bot ao grupo
- **GROUP_CHAT_ID incorreto**: Use `/groupid` para obter o ID correto
- **Permissões insuficientes**: Bot precisa de permissão para enviar mensagens

## Configuração do GROUP_CHAT_ID

1. Adicione o bot ao grupo "Kyoko Packs 👄❤️‍🔥"
2. Execute `/groupid` no grupo
3. Copie o ID retornado
4. Configure no arquivo `.env`:
   ```
   GROUP_CHAT_ID=-1001234567890
   ```
5. Reinicie o bot

## Reverter para Produção

Para voltar ao tempo normal de 1 minuto:

```python
# Em bot.py, linha ~571
first=60,  # Primeira execução após 1 minuto
```

## Segurança

- ⚠️ **Não commitar** o `GROUP_CHAT_ID` real no repositório
- ✅ **Usar variáveis de ambiente** para configurações sensíveis
- ✅ **Testar em grupo de desenvolvimento** antes da produção

## Próximos Passos

1. **Deploy**: Faça o deploy da aplicação
2. **Observe**: Aguarde 10-15 segundos
3. **Verifique**: Confirme se a mensagem foi enviada
4. **Monitore**: Acompanhe os logs para possíveis erros
5. **Ajuste**: Se necessário, corrija configurações

---

**Nota**: Esta configuração é temporária para teste. Em produção, considere usar um tempo maior (60s) para evitar mensagens desnecessárias durante restarts frequentes.
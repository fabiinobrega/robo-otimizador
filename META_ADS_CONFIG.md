# Configuração Meta Ads - Nexora Prime

## Informações da Conta de Anúncios

| Campo | Valor |
|-------|-------|
| **Ad Account ID** | `851930913002539` |
| **Ad Account ID (formato API)** | `act_851930913002539` |
| **Email** | nobregafabi@hotmail.com |
| **Administrador** | Fabiana Pacheco |
| **Página do Facebook** | Você bonita - Saúde e beleza |
| **Page ID** | 110733095359498 |

## Status da Configuração

- ✅ Conta de anúncios criada
- ✅ Página do Facebook vinculada
- ✅ Política de não discriminação aceita
- ⚠️ Forma de pagamento pendente
- ⚠️ Conta de desenvolvedor Meta pendente (verificação SMS não funcionou)

## Próximos Passos para Completar Integração

### 1. Verificar Conta de Desenvolvedor
O Meta for Developers requer verificação por SMS ou cartão de crédito.
- Tente novamente mais tarde quando o sistema de SMS estiver funcionando
- Ou adicione um cartão de crédito na conta Meta Pay

### 2. Criar App no Meta for Developers
Após verificação, criar app com:
- Produto: Marketing API
- Permissões: ads_management, ads_read, business_management

### 3. Gerar System User Token
- Criar System User no Business Manager
- Gerar token com permissões de Marketing API
- Token será usado no Nexora Prime

### 4. Adicionar Forma de Pagamento
- Necessário para veicular anúncios
- Acessar: Gerenciador de Anúncios > Cobrança e pagamentos

## Variáveis de Ambiente para .env

```env
# Meta Ads Configuration
META_AD_ACCOUNT_ID=act_851930913002539
META_PAGE_ID=110733095359498
META_ACCESS_TOKEN=<PENDENTE - Aguardando verificação de desenvolvedor>
META_APP_ID=<PENDENTE - Aguardando criação do app>
META_APP_SECRET=<PENDENTE - Aguardando criação do app>
```

## Documentação Útil

- [Marketing API](https://developers.facebook.com/docs/marketing-apis/)
- [Business Manager](https://business.facebook.com/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)

---
*Gerado em: 25/12/2024*
*Status: Parcialmente configurado - Aguardando verificação de desenvolvedor*

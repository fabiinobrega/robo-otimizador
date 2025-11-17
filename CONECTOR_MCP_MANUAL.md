# 🔌 MANUS OPERATOR – API CONNECTOR (v6.0)

**Manual Completo de Instalação e Uso**

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Actions Disponíveis](#actions-disponíveis)
5. [Exemplos de Uso](#exemplos-de-uso)
6. [Segurança](#segurança)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 VISÃO GERAL

O **Velyra Prime – API Connector** é um conector MCP (Model Context Protocol) completo que permite integração total entre a plataforma Manus e o Velyra Prime (seu robô autônomo de marketing).

### **Recursos Principais:**

✅ **Autenticação OAuth2** completa
✅ **Sincronização bidirecional** de campanhas e anúncios
✅ **Relatórios de performance** em tempo real
✅ **Gerenciamento de créditos**
✅ **Sistema de webhooks** para eventos
✅ **Segurança avançada** com JWT e CSRF
✅ **Rate limiting** e retry logic
✅ **12 actions** prontas para uso

---

## 📦 INSTALAÇÃO

### **Passo 1: Importar o Conector**

1. Acesse a plataforma Manus
2. Vá em "Configurações" → "Conectores"
3. Clique em "Importar Conector"
4. Faça upload do arquivo `velyra-prime-connector-v6.0.json`
5. Clique em "Instalar"

### **Passo 2: Configurar Credenciais**

Após a instalação, você precisará configurar:

1. **API Base URL:** `https://robo-otimizador1.onrender.com`
2. **Client ID:** (fornecido pelo Velyra Prime)
3. **Client Secret:** (fornecido pelo Velyra Prime)
4. **Redirect URI:** `https://app.manus.im/oauth/callback`

---

## ⚙️ CONFIGURAÇÃO

### **Obter Credenciais**

Para obter o Client ID e Client Secret:

1. Acesse: https://robo-otimizador1.onrender.com/manus/connect
2. Clique em "Gerar Credenciais"
3. Copie o Client ID e Client Secret
4. Cole na configuração do conector na plataforma Manus

### **Autorizar Acesso**

1. Na plataforma Manus, clique em "Conectar"
2. Você será redirecionado para o Velyra Prime
3. Autorize o acesso
4. Será redirecionado de volta para o Manus
5. **Pronto!** Conexão estabelecida

---

## 🛠️ ACTIONS DISPONÍVEIS

### **1. AUTENTICAÇÃO**

#### **get_authorization_url**
Gera a URL para iniciar o fluxo OAuth2.

**Entrada:**
```json
{
  "state": "random_string_csrf",
  "scope": ["campaigns:read", "campaigns:write"]
}
```

**Saída:**
```json
{
  "authorization_url": "https://robo-otimizador1.onrender.com/oauth/authorize?...",
  "state": "random_string_csrf"
}
```

#### **exchange_code**
Troca o código de autorização por tokens.

**Entrada:**
```json
{
  "code": "authorization_code_received",
  "state": "random_string_csrf"
}
```

**Saída:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "scope": "campaigns:read campaigns:write"
}
```

#### **refresh_token**
Renova o access_token.

**Entrada:**
```json
{
  "refresh_token": "current_refresh_token"
}
```

**Saída:**
```json
{
  "access_token": "new_access_token",
  "refresh_token": "new_refresh_token",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

#### **get_status**
Retorna o status da integração.

**Entrada:** Nenhuma

**Saída:**
```json
{
  "connected": true,
  "token_valid": true,
  "expires_at": "2024-11-10T12:00:00Z",
  "scope": "campaigns:read campaigns:write ads:read"
}
```

#### **test_connection**
Testa a conexão com a API.

**Entrada:** Nenhuma

**Saída:**
```json
{
  "success": true,
  "message": "Conexão estabelecida com sucesso",
  "timestamp": "2024-11-09T15:30:00Z"
}
```

---

### **2. CAMPANHAS**

#### **sync_campaigns**
Sincroniza campanhas entre Manus e Velyra Prime.

**Entrada:**
```json
{
  "direction": "both"
}
```

Opções de `direction`:
- `push` - Envia campanhas do Manus para o Operator
- `pull` - Recebe campanhas do Operator para o Manus
- `both` - Sincronização bidirecional

**Saída:**
```json
{
  "success": true,
  "pushed": 5,
  "pulled": 3,
  "errors": [],
  "synced_at": "2024-11-09T15:30:00Z"
}
```

---

### **3. ANÚNCIOS**

#### **sync_ads**
Sincroniza anúncios de uma campanha.

**Entrada:**
```json
{
  "campaign_id": 123,
  "direction": "both"
}
```

Se `campaign_id` for `null`, sincroniza todos os anúncios.

**Saída:**
```json
{
  "success": true,
  "pushed": 10,
  "pulled": 8,
  "errors": []
}
```

---

### **4. RELATÓRIOS**

#### **get_reports**
Obtém relatórios de performance.

**Entrada:**
```json
{
  "start_date": "2024-11-01",
  "end_date": "2024-11-09",
  "campaign_id": 123
}
```

Todos os campos são opcionais. Se omitidos, retorna dados dos últimos 30 dias.

**Saída:**
```json
{
  "success": true,
  "reports": [
    {
      "campaign_id": 123,
      "campaign_name": "Black Friday 2024",
      "impressions": 50000,
      "clicks": 2500,
      "ctr": 5.0,
      "cpc": 0.50,
      "conversions": 125,
      "roas": 4.5,
      "spend": 1250.00,
      "revenue": 5625.00
    }
  ]
}
```

---

### **5. CRÉDITOS**

#### **get_credits_balance**
Consulta o saldo de créditos.

**Entrada:** Nenhuma

**Saída:**
```json
{
  "success": true,
  "balance": 10000,
  "plan": "Pro",
  "usage_this_month": 2500
}
```

#### **consume_credits**
Registra o consumo de créditos.

**Entrada:**
```json
{
  "amount": 100,
  "description": "Geração de 5 variantes de anúncio"
}
```

**Saída:**
```json
{
  "success": true,
  "new_balance": 9900,
  "consumed": 100
}
```

---

### **6. WEBHOOKS**

#### **register_webhook**
Registra um webhook para receber eventos.

**Entrada:**
```json
{
  "event": "campaign.created",
  "url": "https://app.manus.im/webhooks/operator",
  "secret": "webhook_secret_key"
}
```

Eventos disponíveis:
- `campaign.created` - Nova campanha criada
- `campaign.updated` - Campanha atualizada
- `ad.published` - Anúncio publicado
- `report.generated` - Relatório gerado

**Saída:**
```json
{
  "success": true,
  "webhook_id": 456,
  "event": "campaign.created",
  "url": "https://app.manus.im/webhooks/operator"
}
```

#### **verify_webhook**
Verifica a assinatura de um webhook recebido.

**Entrada:**
```json
{
  "signature": "sha256=abc123...",
  "payload": "{\"event\":\"campaign.created\",\"data\":{...}}",
  "secret": "webhook_secret_key"
}
```

**Saída:**
```json
{
  "valid": true,
  "message": "Assinatura válida"
}
```

---

## 💡 EXEMPLOS DE USO

### **Exemplo 1: Sincronizar Campanhas**

```javascript
// Em um fluxo Manus
const result = await velyra_prime.sync_campaigns({
  direction: "both"
});

console.log(`Campanhas sincronizadas: ${result.pushed} enviadas, ${result.pulled} recebidas`);
```

### **Exemplo 2: Obter Relatórios**

```javascript
// Obter relatórios dos últimos 7 dias
const reports = await velyra_prime.get_reports({
  start_date: "2024-11-02",
  end_date: "2024-11-09"
});

reports.reports.forEach(report => {
  console.log(`${report.campaign_name}: ROAS ${report.roas}x`);
});
```

### **Exemplo 3: Consultar Créditos**

```javascript
// Verificar saldo antes de executar ação
const balance = await velyra_prime.get_credits_balance();

if (balance.balance >= 100) {
  // Executar ação
  await velyra_prime.consume_credits({
    amount: 100,
    description: "Geração de anúncio com IA"
  });
}
```

### **Exemplo 4: Configurar Webhook**

```javascript
// Registrar webhook para receber notificações
await velyra_prime.register_webhook({
  event: "campaign.created",
  url: "https://app.manus.im/webhooks/operator",
  secret: "my_secret_key"
});

// Ao receber webhook, verificar assinatura
const isValid = await velyra_prime.verify_webhook({
  signature: request.headers['x-manus-signature'],
  payload: JSON.stringify(request.body),
  secret: "my_secret_key"
});

if (isValid.valid) {
  // Processar evento
  console.log("Evento autêntico recebido!");
}
```

---

## 🔒 SEGURANÇA

### **OAuth2 Authorization Code Flow**

O conector usa o fluxo OAuth2 mais seguro:

1. **Autorização:** Usuário autoriza o acesso
2. **Código:** Aplicação recebe código temporário
3. **Troca:** Código é trocado por tokens
4. **Renovação:** Tokens são renovados automaticamente

### **CSRF Protection**

Todos os fluxos OAuth2 usam `state` para prevenir CSRF:

```javascript
const state = generateRandomString();
const authUrl = await velyra_prime.get_authorization_url({
  state: state
});

// Armazenar state para validação posterior
sessionStorage.setItem('oauth_state', state);
```

### **Webhook Signature**

Todos os webhooks são assinados com SHA256:

```
X-Manus-Signature: sha256=abc123...
```

Sempre verifique a assinatura antes de processar eventos.

### **HTTPS Only**

O conector **só funciona com HTTPS**. Requisições HTTP serão rejeitadas.

### **Token Expiration**

- **Access Token:** Expira em 24 horas
- **Refresh Token:** Expira em 30 dias
- Renovação automática antes de expirar

---

## 🔧 TROUBLESHOOTING

### **Erro: "Token inválido"**

**Causa:** Token expirado ou revogado

**Solução:**
```javascript
// Renovar token
const newToken = await velyra_prime.refresh_token({
  refresh_token: currentRefreshToken
});

// Usar novo token
```

### **Erro: "Conexão recusada"**

**Causa:** API Base URL incorreta

**Solução:**
1. Verificar se a URL está correta: `https://robo-otimizador1.onrender.com`
2. Testar conexão: `await velyra_prime.test_connection()`

### **Erro: "Créditos insuficientes"**

**Causa:** Saldo de créditos zerado

**Solução:**
```javascript
// Verificar saldo
const balance = await velyra_prime.get_credits_balance();
console.log(`Saldo atual: ${balance.balance} créditos`);

// Adicionar mais créditos no painel do Velyra Prime
```

### **Erro: "Webhook signature invalid"**

**Causa:** Secret incorreto ou payload modificado

**Solução:**
1. Verificar se o `secret` está correto
2. Não modificar o payload antes de verificar
3. Usar o payload bruto (raw) para verificação

### **Erro: "Rate limit exceeded"**

**Causa:** Muitas requisições em pouco tempo

**Solução:**
- Aguardar 1 minuto
- Implementar retry com backoff exponencial
- Limites: 60 req/min, 1000 req/hora

---

## 📊 RATE LIMITING

O conector implementa rate limiting para proteger a API:

- **60 requisições por minuto**
- **1000 requisições por hora**

Quando o limite é excedido, você receberá:

```json
{
  "error": "Rate limit exceeded",
  "retry_after": 60
}
```

Aguarde o tempo indicado em `retry_after` (segundos) antes de tentar novamente.

---

## 🔄 RETRY LOGIC

O conector implementa retry automático:

- **Máximo de 3 tentativas**
- **Backoff exponencial:** 1s, 2s, 4s
- **Timeout de conexão:** 5 segundos
- **Timeout de leitura:** 30 segundos

Erros que acionam retry:
- Timeout de conexão
- Erros 5xx (servidor)
- Rate limiting (429)

Erros que **não** acionam retry:
- Erros 4xx (cliente)
- Token inválido
- Validação de entrada

---

## 📝 LOGGING

O conector registra todas as operações:

```javascript
// Habilitar logs detalhados
velyra_prime.setLogLevel('debug');

// Logs incluem:
// - Requisições HTTP
// - Respostas
// - Erros
// - Tempo de execução
```

**Níveis de log:**
- `error` - Apenas erros
- `warn` - Avisos e erros
- `info` - Informações gerais (padrão)
- `debug` - Detalhes completos

---

## 🎯 BOAS PRÁTICAS

### **1. Sempre Verificar Saldo**

```javascript
const balance = await velyra_prime.get_credits_balance();
if (balance.balance < 100) {
  console.warn("Saldo baixo de créditos!");
}
```

### **2. Usar Webhooks para Eventos**

Em vez de polling, use webhooks:

```javascript
// ❌ Não fazer (polling)
setInterval(async () => {
  const reports = await velyra_prime.get_reports();
}, 60000);

// ✅ Fazer (webhook)
await velyra_prime.register_webhook({
  event: "report.generated",
  url: "https://app.manus.im/webhooks/reports"
});
```

### **3. Sincronizar Periodicamente**

```javascript
// Sincronizar campanhas a cada hora
setInterval(async () => {
  await velyra_prime.sync_campaigns({ direction: "both" });
}, 3600000);
```

### **4. Tratar Erros Graciosamente**

```javascript
try {
  await velyra_prime.sync_campaigns({ direction: "both" });
} catch (error) {
  if (error.code === 'RATE_LIMIT') {
    // Aguardar e tentar novamente
    await sleep(error.retry_after * 1000);
  } else {
    // Logar erro
    console.error("Erro ao sincronizar:", error);
  }
}
```

---

## 🆘 SUPORTE

### **Documentação Adicional**

- **Documentação Técnica:** `INTEGRACAO_MANUS_API.md`
- **Manual do Robô:** `ROBO_EXECUTOR_MANUAL.md`
- **APIs Necessárias:** `API_KEYS_NECESSARIAS.md`

### **Contato**

- **Suporte Velyra Prime:** https://robo-otimizador1.onrender.com/manus/connect
- **GitHub:** https://github.com/fabiinobrega/robo-otimizador
- **Issues:** https://github.com/fabiinobrega/robo-otimizador/issues

---

## 📈 ROADMAP

### **Versão 6.1 (Planejada)**

- [ ] Suporte a múltiplas contas
- [ ] Sincronização de públicos
- [ ] Integração com Meta Ads
- [ ] Integração com Google Ads
- [ ] Dashboard de métricas
- [ ] Exportação de relatórios (PDF/Excel)

### **Versão 7.0 (Futuro)**

- [ ] IA preditiva de performance
- [ ] Auto-otimização de campanhas
- [ ] Recomendações personalizadas
- [ ] Análise de concorrentes
- [ ] Geração de criativos com IA

---

## 🏆 CONCLUSÃO

O **Velyra Prime – API Connector (v6.0)** é um conector completo e robusto que permite integração total entre a plataforma Manus e o Velyra Prime.

**Com ele você pode:**

✅ Sincronizar campanhas e anúncios automaticamente
✅ Obter relatórios de performance em tempo real
✅ Gerenciar créditos programaticamente
✅ Receber eventos via webhooks
✅ Usar todas as funcionalidades do Velyra Prime dentro do Manus

**Desenvolvido com ❤️ por Fabiana Nobrega Pacheco Ferreira**

**Versão:** 6.0.0  
**Data:** 09 de novembro de 2024  
**Status:** ✅ **PRONTO PARA USO**

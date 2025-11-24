# 📘 GUIA COMPLETO - INTEGRAÇÃO FACEBOOK ADS

**Sistema de Otimização de Vendas Avançado**  
**Data:** 24/11/2024  
**Status:** Implementação Completa Pronta

---

## 📋 SUMÁRIO

1. [Pré-requisitos](#pré-requisitos)
2. [Passo 1: Criar App no Facebook Developers](#passo-1-criar-app-no-facebook-developers)
3. [Passo 2: Configurar Permissões](#passo-2-configurar-permissões)
4. [Passo 3: Obter Credenciais](#passo-3-obter-credenciais)
5. [Passo 4: Gerar Access Token](#passo-4-gerar-access-token)
6. [Passo 5: Configurar Variáveis de Ambiente](#passo-5-configurar-variáveis-de-ambiente)
7. [Passo 6: Instalar SDK](#passo-6-instalar-sdk)
8. [Passo 7: Testar Integração](#passo-7-testar-integração)
9. [Exemplos de Uso](#exemplos-de-uso)
10. [Troubleshooting](#troubleshooting)

---

## 📦 PRÉ-REQUISITOS

Antes de começar, você precisa ter:

- ✅ Conta do Facebook Business Manager
- ✅ Conta de anúncios (Ad Account) criada
- ✅ Página do Facebook vinculada
- ✅ Método de pagamento configurado
- ✅ Acesso de administrador à conta de anúncios

---

## 🔧 PASSO 1: CRIAR APP NO FACEBOOK DEVELOPERS

### 1.1. Acessar Facebook Developers

1. Acesse: https://developers.facebook.com/
2. Faça login com sua conta do Facebook
3. Clique em **"Meus Apps"** no canto superior direito
4. Clique em **"Criar App"**

### 1.2. Escolher Tipo de App

1. Selecione **"Empresa"** (Business)
2. Clique em **"Avançar"**

### 1.3. Preencher Informações

```
Nome do App: Nexora Prime Marketing
E-mail de Contato: seu-email@dominio.com
Conta Comercial: [Selecione sua conta do Business Manager]
```

4. Clique em **"Criar App"**

### 1.4. Confirmar Identidade

- Complete a verificação de segurança (se solicitada)
- Anote o **App ID** (você vai precisar)

---

## 🔐 PASSO 2: CONFIGURAR PERMISSÕES

### 2.1. Adicionar Produto Marketing API

1. No painel do app, procure **"Marketing API"**
2. Clique em **"Configurar"**
3. Aceite os termos de uso

### 2.2. Solicitar Permissões

Você precisa das seguintes permissões:

- ✅ `ads_management` - Gerenciar anúncios
- ✅ `ads_read` - Ler dados de anúncios
- ✅ `business_management` - Gerenciar negócios
- ✅ `pages_read_engagement` - Ler engajamento de páginas
- ✅ `pages_manage_ads` - Gerenciar anúncios de páginas

Para solicitar:

1. Vá em **"Permissões e Recursos"** no menu lateral
2. Clique em **"Solicitar Permissões Avançadas"**
3. Selecione as permissões acima
4. Preencha o formulário explicando o uso
5. Aguarde aprovação (pode levar 1-3 dias)

---

## 🔑 PASSO 3: OBTER CREDENCIAIS

### 3.1. App ID e App Secret

1. No painel do app, vá em **"Configurações" > "Básico"**
2. Copie o **App ID**
3. Clique em **"Mostrar"** ao lado de **App Secret**
4. Copie o **App Secret** (guarde em local seguro!)

```
App ID: 123456789012345
App Secret: abc123def456ghi789jkl012mno345pq
```

### 3.2. Ad Account ID

1. Acesse: https://business.facebook.com/
2. Vá em **"Configurações de Negócios"**
3. Clique em **"Contas de Anúncios"** no menu lateral
4. Selecione sua conta de anúncios
5. Copie o **ID da Conta de Anúncios** (formato: act_1234567890)

```
Ad Account ID: 1234567890 (sem o "act_")
```

---

## 🎫 PASSO 4: GERAR ACCESS TOKEN

### 4.1. Usar Graph API Explorer

1. Acesse: https://developers.facebook.com/tools/explorer/
2. Selecione seu app no dropdown
3. Clique em **"Gerar Token de Acesso"**
4. Selecione as permissões necessárias:
   - ads_management
   - ads_read
   - business_management
5. Clique em **"Gerar Token de Acesso"**
6. Copie o token gerado

### 4.2. Converter para Token de Longa Duração

O token gerado expira em 1 hora. Para converter para 60 dias:

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=SEU_APP_ID&client_secret=SEU_APP_SECRET&fb_exchange_token=SEU_TOKEN_CURTO"
```

Substitua:
- `SEU_APP_ID` - App ID do passo 3.1
- `SEU_APP_SECRET` - App Secret do passo 3.1
- `SEU_TOKEN_CURTO` - Token gerado no passo 4.1

Resposta:
```json
{
  "access_token": "EAABsbCS1iHgBO...",
  "token_type": "bearer",
  "expires_in": 5183999
}
```

Copie o novo `access_token` (este dura 60 dias).

### 4.3. Token Permanente (Opcional)

Para token que não expira:

1. Acesse: https://business.facebook.com/settings/system-users
2. Crie um **System User**
3. Atribua permissões de administrador
4. Gere um token de acesso permanente
5. Copie e guarde em local seguro

---

## ⚙️ PASSO 5: CONFIGURAR VARIÁVEIS DE AMBIENTE

### 5.1. Criar arquivo .env

No diretório do projeto, crie/edite o arquivo `.env`:

```bash
# Facebook Ads API
FACEBOOK_APP_ID=123456789012345
FACEBOOK_APP_SECRET=abc123def456ghi789jkl012mno345pq
FACEBOOK_ACCESS_TOKEN=EAABsbCS1iHgBO...
FACEBOOK_AD_ACCOUNT_ID=1234567890
```

### 5.2. No Render.com (Produção)

1. Acesse seu projeto no Render
2. Vá em **"Environment"**
3. Adicione as variáveis:

```
FACEBOOK_APP_ID = 123456789012345
FACEBOOK_APP_SECRET = abc123def456ghi789jkl012mno345pq
FACEBOOK_ACCESS_TOKEN = EAABsbCS1iHgBO...
FACEBOOK_AD_ACCOUNT_ID = 1234567890
```

4. Clique em **"Save Changes"**
5. Aguarde o redeploy automático

---

## 📦 PASSO 6: INSTALAR SDK

### 6.1. Instalar Facebook Business SDK

```bash
pip install facebook-business
```

### 6.2. Atualizar requirements.txt

Adicione ao arquivo `requirements.txt`:

```
facebook-business==18.0.0
```

### 6.3. Verificar Instalação

```bash
python3 -c "from facebook_business.api import FacebookAdsApi; print('✅ SDK instalado com sucesso')"
```

---

## 🧪 PASSO 7: TESTAR INTEGRAÇÃO

### 7.1. Teste Básico de Conexão

```python
from services.facebook_ads_service_complete import facebook_ads_service

# Verificar configuração
if facebook_ads_service.is_configured():
    print("✅ Facebook Ads configurado corretamente")
    
    # Listar campanhas
    result = facebook_ads_service.get_all_campaigns()
    print(f"Total de campanhas: {result.get('total', 0)}")
else:
    print("❌ Facebook Ads não configurado")
```

### 7.2. Criar Campanha de Teste

```python
from services.facebook_ads_service_complete import create_complete_campaign

campaign_data = {
    "name": "Campanha de Teste - Nexora Prime",
    "objective": "conversions",
    "adset": {
        "name": "Conjunto de Anúncios Teste",
        "country": "BR",
        "min_age": 25,
        "max_age": 45,
        "daily_budget": 50.00,  # R$ 50/dia
        "bid_amount": 5.00,  # R$ 5 por resultado
    },
    "creative": {
        "page_id": "SUA_PAGE_ID",
        "message": "Transforme seu marketing digital com IA!",
        "headline": "Nexora Prime - Marketing Inteligente",
        "description": "Crie campanhas otimizadas em minutos",
        "link": "https://robo-otimizador1.onrender.com",
        "cta_type": "LEARN_MORE",
    }
}

result = create_complete_campaign(campaign_data)
print(result)
```

### 7.3. Obter Métricas

```python
from services.facebook_ads_service_complete import facebook_ads_service

# Substituir por ID real
campaign_id = "123456789"

result = facebook_ads_service.get_campaign_insights(campaign_id)
if result["success"]:
    metrics = result["metrics"]
    print(f"Impressões: {metrics['impressions']}")
    print(f"Cliques: {metrics['clicks']}")
    print(f"ROAS: {metrics['roas']:.2f}x")
else:
    print(f"Erro: {result['message']}")
```

---

## 💡 EXEMPLOS DE USO

### Exemplo 1: Criar Campanha Completa

```python
from services.facebook_ads_service_complete import create_complete_campaign

campaign_data = {
    "name": "Black Friday 2024",
    "objective": "conversions",
    "adset": {
        "name": "Público Quente - Black Friday",
        "country": "BR",
        "min_age": 25,
        "max_age": 55,
        "daily_budget": 200.00,
        "bid_amount": 10.00,
        "interests": [
            {"id": "6003107902433", "name": "Marketing digital"},
            {"id": "6003139266461", "name": "Empreendedorismo"},
        ]
    },
    "creative": {
        "page_id": "123456789",
        "message": "🔥 BLACK FRIDAY: 50% OFF em todos os planos!",
        "headline": "Nexora Prime - Oferta Exclusiva",
        "description": "Aproveite o maior desconto do ano",
        "link": "https://robo-otimizador1.onrender.com/black-friday",
        "cta_type": "SHOP_NOW",
    },
    "image_path": "/home/ubuntu/robo-otimizador/static/uploads/black_friday_banner.jpg"
}

result = create_complete_campaign(campaign_data)
if result["success"]:
    print(f"✅ Campanha criada: {result['campaign_id']}")
else:
    print(f"❌ Erro: {result['message']}")
```

### Exemplo 2: Otimizar Campanhas Automaticamente

```python
from services.facebook_ads_service_complete import facebook_ads_service

# Listar todas as campanhas
campaigns_result = facebook_ads_service.get_all_campaigns()

if campaigns_result["success"]:
    for campaign in campaigns_result["campaigns"]:
        if campaign["status"] == "ACTIVE":
            # Otimizar cada campanha ativa
            optimize_result = facebook_ads_service.optimize_campaign(campaign["id"])
            
            if optimize_result["success"]:
                print(f"✅ Campanha {campaign['name']} otimizada:")
                for action in optimize_result["actions"]:
                    print(f"  - {action}")
```

### Exemplo 3: Monitorar Performance

```python
from services.facebook_ads_service_complete import facebook_ads_service

campaign_id = "123456789"

# Obter métricas dos últimos 7 dias
result = facebook_ads_service.get_campaign_insights(campaign_id, "last_7d")

if result["success"]:
    m = result["metrics"]
    
    print("📊 PERFORMANCE DOS ÚLTIMOS 7 DIAS")
    print(f"Impressões: {m['impressions']:,}")
    print(f"Cliques: {m['clicks']:,}")
    print(f"CTR: {m['ctr']:.2f}%")
    print(f"Conversões: {m['conversions']}")
    print(f"Gasto: R$ {m['spend']:.2f}")
    print(f"Receita: R$ {m['revenue']:.2f}")
    print(f"ROAS: {m['roas']:.2f}x")
    print(f"CPA: R$ {m['cpa']:.2f}")
```

---

## 🔧 TROUBLESHOOTING

### Erro: "Facebook Business SDK not installed"

**Solução:**
```bash
pip install facebook-business
```

### Erro: "Invalid OAuth access token"

**Causa:** Token expirado ou inválido

**Solução:**
1. Gere um novo token no Graph API Explorer
2. Converta para token de longa duração
3. Atualize a variável `FACEBOOK_ACCESS_TOKEN`

### Erro: "Permissions error"

**Causa:** App não tem permissões necessárias

**Solução:**
1. Acesse Facebook Developers
2. Vá em "Permissões e Recursos"
3. Solicite as permissões faltantes
4. Aguarde aprovação

### Erro: "Ad account not found"

**Causa:** Ad Account ID incorreto

**Solução:**
1. Verifique o ID no Business Manager
2. Use apenas os números (sem "act_")
3. Atualize `FACEBOOK_AD_ACCOUNT_ID`

### Erro: "Rate limit exceeded"

**Causa:** Muitas requisições em pouco tempo

**Solução:**
1. Aguarde alguns minutos
2. Implemente rate limiting no código
3. Use batch requests quando possível

---

## 📚 RECURSOS ADICIONAIS

### Documentação Oficial

- **Marketing API:** https://developers.facebook.com/docs/marketing-apis
- **Business SDK Python:** https://github.com/facebook/facebook-python-business-sdk
- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/

### Limites e Quotas

- **Rate Limit:** 200 chamadas por hora por usuário
- **Batch Limit:** 50 requisições por batch
- **Token Expiration:** 60 dias (token de longa duração)

### Suporte

- **Facebook Business Help:** https://www.facebook.com/business/help
- **Developer Community:** https://developers.facebook.com/community/

---

## ✅ CHECKLIST FINAL

Antes de usar em produção, verifique:

- [ ] App criado no Facebook Developers
- [ ] Permissões aprovadas
- [ ] Access token gerado (longa duração)
- [ ] Variáveis de ambiente configuradas
- [ ] SDK instalado
- [ ] Teste de conexão funcionando
- [ ] Campanha de teste criada com sucesso
- [ ] Métricas sendo coletadas corretamente

---

**Status:** ✅ GUIA COMPLETO  
**Última Atualização:** 24/11/2024  
**Versão:** 1.0

# 🔑 APIs NECESSÁRIAS - MANUS MARKETING

**Versão:** 4.0  
**Data:** 09 de novembro de 2024  
**Status:** Guia Completo de Configuração

---

## 📋 VISÃO GERAL

Para usar todas as funcionalidades do **Manus Marketing**, você precisará configurar as seguintes APIs:

1. ✅ **OpenAI GPT-4** - Para geração de copy e análise com IA
2. ✅ **Facebook Marketing API** - Para publicar anúncios no Facebook/Instagram
3. ✅ **Google Ads API** - Para publicar anúncios no Google
4. ⚠️ **DALL-E** (Opcional) - Para geração de imagens com IA

---

## 🤖 1. OPENAI API (GPT-4)

### **Para que serve:**
- Gerar headlines, descriptions e CTAs otimizados
- Analisar landing pages
- Gerar insights estratégicos
- Sugerir melhorias em campanhas

### **Como obter:**

#### **Passo 1: Criar Conta**
1. Acesse: https://platform.openai.com/signup
2. Crie uma conta (pode usar Google/Microsoft)
3. Confirme seu email

#### **Passo 2: Adicionar Créditos**
1. Vá em: https://platform.openai.com/account/billing
2. Clique em "Add payment method"
3. Adicione um cartão de crédito
4. Compre créditos (mínimo $5, recomendado $10-20)

#### **Passo 3: Gerar API Key**
1. Acesse: https://platform.openai.com/api-keys
2. Clique em "Create new secret key"
3. Dê um nome: "Manus Marketing"
4. Copie a key (começa com `sk-proj-...`)
5. **IMPORTANTE:** Guarde em local seguro, não será mostrada novamente!

#### **Passo 4: Configurar no Render**
1. Acesse: https://dashboard.render.com
2. Selecione o serviço "robo-otimizador1"
3. Vá em "Environment"
4. Clique em "Add Environment Variable"
5. Adicione:
   ```
   Key: OPENAI_API_KEY
   Value: sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
6. Clique em "Save Changes"
7. O serviço será reiniciado automaticamente

### **Custo Estimado:**

**GPT-4 Turbo (Recomendado):**
- Input: $0.01 / 1K tokens
- Output: $0.03 / 1K tokens
- **Custo por anúncio:** ~$0.05-0.10

**GPT-3.5 Turbo (Econômico):**
- Input: $0.0005 / 1K tokens
- Output: $0.0015 / 1K tokens
- **Custo por anúncio:** ~$0.01-0.02

**Recomendação:** Comece com $10 de crédito (suficiente para 100-200 anúncios)

### **Exemplo de Uso:**

```python
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "Você é um especialista em copywriting para anúncios."},
        {"role": "user", "content": "Crie 3 headlines para um tênis esportivo de R$ 149,90"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### **Limites:**

- **Free Tier:** Não existe mais (descontinuado)
- **Pay-as-you-go:** Sem limite, paga pelo uso
- **Rate Limits:** 
  - GPT-4: 10,000 tokens/min
  - GPT-3.5: 90,000 tokens/min

---

## 📘 2. FACEBOOK MARKETING API

### **Para que serve:**
- Publicar anúncios no Facebook Ads
- Publicar anúncios no Instagram Ads
- Gerenciar campanhas automaticamente
- Obter métricas em tempo real

### **Como obter:**

#### **Passo 1: Criar Conta Business**
1. Acesse: https://business.facebook.com
2. Clique em "Criar Conta"
3. Preencha os dados da sua empresa
4. Confirme o email

#### **Passo 2: Criar App no Meta for Developers**
1. Acesse: https://developers.facebook.com/apps
2. Clique em "Criar App"
3. Selecione "Negócios" como tipo
4. Preencha:
   - **Nome do App:** Manus Marketing
   - **Email de Contato:** seu@email.com
5. Clique em "Criar App"

#### **Passo 3: Adicionar Produto "Marketing API"**
1. No painel do app, clique em "Adicionar Produto"
2. Selecione "Marketing API"
3. Clique em "Configurar"

#### **Passo 4: Gerar Access Token**
1. Vá em "Ferramentas" → "Explorador de API do Graph"
2. Selecione seu app no dropdown
3. Clique em "Gerar Token de Acesso"
4. Selecione as permissões:
   - `ads_management`
   - `ads_read`
   - `business_management`
   - `pages_read_engagement`
   - `pages_manage_ads`
5. Copie o **Access Token** (começa com `EAA...`)

#### **Passo 5: Obter IDs Necessários**

**Ad Account ID:**
1. Acesse: https://business.facebook.com/settings/ad-accounts
2. Copie o ID da conta (ex: `act_123456789`)

**Page ID:**
1. Acesse sua página do Facebook
2. Vá em "Sobre"
3. Role até "ID da Página"

**Business ID:**
1. Acesse: https://business.facebook.com/settings
2. Copie o "ID da Empresa"

#### **Passo 6: Configurar no Render**
```
FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxx
FACEBOOK_AD_ACCOUNT_ID=act_123456789
FACEBOOK_PAGE_ID=123456789
FACEBOOK_BUSINESS_ID=123456789
```

### **Custo:**

- **API:** Gratuita
- **Anúncios:** Você paga apenas pelo que gastar em anúncios (mínimo $1/dia)

### **Exemplo de Uso:**

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

FacebookAdsApi.init(
    access_token=os.getenv('FACEBOOK_ACCESS_TOKEN')
)

account = AdAccount(f"act_{os.getenv('FACEBOOK_AD_ACCOUNT_ID')}")
campaigns = account.get_campaigns()

for campaign in campaigns:
    print(campaign['name'])
```

### **Limites:**

- **Rate Limits:** 200 chamadas/hora por usuário
- **App Review:** Necessário para produção (pode levar 1-2 semanas)
- **Modo Desenvolvimento:** Sem limites, mas apenas você pode usar

### **Documentação Oficial:**
- https://developers.facebook.com/docs/marketing-apis
- https://developers.facebook.com/docs/graph-api

---

## 🔍 3. GOOGLE ADS API

### **Para que serve:**
- Publicar anúncios no Google Ads
- Gerenciar campanhas de Search, Display, YouTube
- Obter métricas em tempo real
- Otimização automática de lances

### **Como obter:**

#### **Passo 1: Criar Conta Google Ads**
1. Acesse: https://ads.google.com
2. Clique em "Começar Agora"
3. Configure sua conta de anúncios
4. **Importante:** Você precisa gastar pelo menos $50 antes de acessar a API

#### **Passo 2: Criar Projeto no Google Cloud**
1. Acesse: https://console.cloud.google.com
2. Clique em "Novo Projeto"
3. Nome: "Manus Marketing"
4. Clique em "Criar"

#### **Passo 3: Ativar Google Ads API**
1. No menu, vá em "APIs e Serviços" → "Biblioteca"
2. Pesquise "Google Ads API"
3. Clique em "Ativar"

#### **Passo 4: Criar Credenciais OAuth 2.0**
1. Vá em "APIs e Serviços" → "Credenciais"
2. Clique em "Criar Credenciais" → "ID do cliente OAuth"
3. Tipo: "Aplicativo da Web"
4. Nome: "Manus Marketing"
5. URIs de redirecionamento autorizados:
   ```
   https://robo-otimizador1.onrender.com/oauth2callback
   http://localhost:5000/oauth2callback
   ```
6. Clique em "Criar"
7. Copie:
   - **Client ID:** `xxxxx.apps.googleusercontent.com`
   - **Client Secret:** `GOCSPX-xxxxx`

#### **Passo 5: Obter Developer Token**
1. Acesse: https://ads.google.com/aw/apicenter
2. Clique em "Solicitar Token de Desenvolvedor"
3. Preencha o formulário
4. Aguarde aprovação (1-2 dias úteis)
5. Copie o **Developer Token**

#### **Passo 6: Obter Customer ID**
1. Acesse: https://ads.google.com
2. No canto superior direito, copie o ID (ex: `123-456-7890`)
3. Remova os hífens: `1234567890`

#### **Passo 7: Gerar Refresh Token**

Execute este script Python:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = 'seu-client-id.apps.googleusercontent.com'
CLIENT_SECRET = 'GOCSPX-xxxxx'

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
        }
    },
    scopes=["https://www.googleapis.com/auth/adwords"],
)

flow.run_local_server(port=8080)
credentials = flow.credentials

print(f"Refresh Token: {credentials.refresh_token}")
```

#### **Passo 8: Configurar no Render**
```
GOOGLE_ADS_DEVELOPER_TOKEN=xxxxxxxxxxxxxxxx
GOOGLE_ADS_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=GOCSPX-xxxxx
GOOGLE_ADS_REFRESH_TOKEN=1//xxxxxxxxxxxxxxxxx
GOOGLE_ADS_CUSTOMER_ID=1234567890
```

### **Custo:**

- **API:** Gratuita
- **Anúncios:** Você paga apenas pelo que gastar (sem mínimo)

### **Exemplo de Uso:**

```python
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_env()

ga_service = client.get_service("GoogleAdsService")
query = """
    SELECT campaign.id, campaign.name, campaign.status
    FROM campaign
    ORDER BY campaign.id
"""

response = ga_service.search(customer_id="1234567890", query=query)

for row in response:
    print(f"Campaign: {row.campaign.name}")
```

### **Limites:**

- **Rate Limits:** 15,000 operações/dia (modo teste)
- **Produção:** Ilimitado após aprovação
- **Aprovação:** Necessária para produção (1-2 semanas)

### **Documentação Oficial:**
- https://developers.google.com/google-ads/api/docs/start
- https://developers.google.com/google-ads/api/docs/oauth/overview

---

## 🎨 4. DALL-E API (OPCIONAL)

### **Para que serve:**
- Gerar imagens para anúncios automaticamente
- Criar variações de criativos
- Adaptar imagens para diferentes formatos

### **Como obter:**

Usa a mesma API Key do OpenAI!

```python
import openai

response = openai.Image.create(
    prompt="Tênis esportivo moderno, fundo minimalista, alta qualidade",
    n=3,
    size="1024x1024"
)

image_url = response['data'][0]['url']
```

### **Custo:**

- **1024×1024:** $0.020 / imagem
- **512×512:** $0.018 / imagem
- **256×256:** $0.016 / imagem

**Recomendação:** Use imagens do produto ou faça upload manual (mais barato)

---

## ⚙️ CONFIGURAÇÃO COMPLETA NO RENDER

### **Todas as Variáveis de Ambiente:**

```bash
# OpenAI (Obrigatório para IA)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Facebook Ads (Opcional - para publicar)
FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxx
FACEBOOK_AD_ACCOUNT_ID=act_123456789
FACEBOOK_PAGE_ID=123456789
FACEBOOK_BUSINESS_ID=123456789

# Google Ads (Opcional - para publicar)
GOOGLE_ADS_DEVELOPER_TOKEN=xxxxxxxxxxxxxxxx
GOOGLE_ADS_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=GOCSPX-xxxxx
GOOGLE_ADS_REFRESH_TOKEN=1//xxxxxxxxxxxxxxxxx
GOOGLE_ADS_CUSTOMER_ID=1234567890

# Configurações do Sistema
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-aqui
```

### **Como Adicionar no Render:**

1. Acesse: https://dashboard.render.com
2. Selecione o serviço "robo-otimizador1"
3. Vá em "Environment"
4. Clique em "Add Environment Variable"
5. Cole todas as variáveis acima
6. Clique em "Save Changes"
7. Aguarde o redeploy automático

---

## 🧪 MODO DE TESTE (SEM APIs)

Se você ainda não tem as APIs configuradas, o sistema funciona em **modo simulado**:

✅ **O que funciona:**
- Geração de copy (simulado)
- Análise de landing page (básica)
- Simulação de performance
- Interface completa
- Upload de mídias
- Criação de campanhas (salvas no banco)

❌ **O que NÃO funciona:**
- Publicação real no Facebook/Google
- Geração de imagens com DALL-E
- Copy otimizado com GPT-4
- Métricas reais das plataformas

**Recomendação:** Use o **Sandbox** para testar sem gastar!

---

## 📊 TABELA RESUMO

| API | Obrigatória? | Custo | Tempo de Setup | Aprovação Necessária? |
|-----|--------------|-------|----------------|----------------------|
| **OpenAI GPT-4** | ✅ Sim | $0.05-0.10/anúncio | 5 min | ❌ Não |
| **Facebook Ads** | ⚠️ Opcional | Grátis (API) | 30 min | ✅ Sim (produção) |
| **Google Ads** | ⚠️ Opcional | Grátis (API) | 45 min | ✅ Sim (produção) |
| **DALL-E** | ❌ Não | $0.02/imagem | 5 min | ❌ Não |

---

## 🚨 SOLUÇÃO DE PROBLEMAS

### **Erro: "Invalid API Key"**

**Causa:** API key incorreta ou expirada

**Solução:**
1. Verifique se copiou a key completa
2. Gere uma nova key
3. Atualize no Render
4. Reinicie o serviço

### **Erro: "Insufficient Quota"**

**Causa:** Créditos do OpenAI acabaram

**Solução:**
1. Acesse: https://platform.openai.com/account/billing
2. Adicione mais créditos
3. Aguarde 5-10 minutos

### **Erro: "OAuth Error" (Facebook/Google)**

**Causa:** Token expirado ou permissões insuficientes

**Solução:**
1. Gere um novo Access Token
2. Verifique as permissões selecionadas
3. Atualize no Render

---

## ✅ CHECKLIST DE CONFIGURAÇÃO

- [ ] Conta OpenAI criada
- [ ] Créditos adicionados ($10+)
- [ ] API Key gerada e copiada
- [ ] Variável `OPENAI_API_KEY` configurada no Render
- [ ] Testado geração de anúncio
- [ ] (Opcional) Facebook Business criado
- [ ] (Opcional) App Facebook criado
- [ ] (Opcional) Access Token gerado
- [ ] (Opcional) Google Cloud Project criado
- [ ] (Opcional) Google Ads API ativada
- [ ] (Opcional) Developer Token solicitado

---

## 🎉 CONCLUSÃO

Com todas as APIs configuradas, você terá acesso a:

✅ **Geração de copy com IA** (GPT-4)  
✅ **Publicação automática** (Facebook + Google)  
✅ **Geração de imagens** (DALL-E)  
✅ **Otimização contínua** (Auto-Pilot)  
✅ **Métricas em tempo real**  
✅ **Automação completa**  

**Comece com o essencial (OpenAI) e adicione as outras conforme necessário!**

---

**Desenvolvido com ❤️ por Manus AI 1.5**  
**Última atualização:** 09 de novembro de 2024

**Suporte:** help@manus.im  
**Documentação:** https://help.manus.im

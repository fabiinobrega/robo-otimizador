# 🔑 GUIA COMPLETO PARA OBTER TODAS AS CHAVES DE API

Este guia fornece instruções passo a passo detalhadas para obter TODAS as chaves de API necessárias para o Nexora Prime funcionar 100%.

---

## 📋 ÍNDICE

1. [OpenAI API](#1-openai-api)
2. [Meta Ads API (Facebook/Instagram)](#2-meta-ads-api-facebookinstagram)
3. [Google Ads API](#3-google-ads-api)
4. [TikTok Ads API](#4-tiktok-ads-api)
5. [LinkedIn Ads API (Opcional)](#5-linkedin-ads-api-opcional)
6. [Pinterest Ads API (Opcional)](#6-pinterest-ads-api-opcional)
7. [Redis (Cache - Opcional)](#7-redis-cache-opcional)
8. [Sentry (Monitoramento - Opcional)](#8-sentry-monitoramento-opcional)
9. [AWS S3 (Upload de Mídia - Opcional)](#9-aws-s3-upload-de-mídia-opcional)
10. [Stripe (Pagamentos - Opcional)](#10-stripe-pagamentos-opcional)

---

## 1. OpenAI API

### O que é?
API para usar modelos de IA como GPT-4, GPT-3.5, DALL-E, Whisper, etc.

### Para que serve no Nexora Prime?
- Velyra Prime Chat (respostas avançadas)
- Análise de concorrentes (análise profunda)
- AI Copywriter (geração de copy)
- Análise de produto (insights de IA)

### Custo
- ~$0.002 por 1000 tokens (muito barato)
- Exemplo: 100 análises de IA = ~$0.20

### Passo a passo:

#### 1.1. Criar conta na OpenAI
1. Acesse: https://platform.openai.com/signup
2. Clique em "Sign up"
3. Preencha seus dados (email, senha)
4. Confirme seu email

#### 1.2. Adicionar método de pagamento
1. Acesse: https://platform.openai.com/account/billing/overview
2. Clique em "Add payment method"
3. Adicione um cartão de crédito
4. **Importante:** Configure um limite de gastos (ex: $10/mês) para evitar surpresas

#### 1.3. Gerar API Key
1. Acesse: https://platform.openai.com/api-keys
2. Clique em "Create new secret key"
3. Dê um nome (ex: "Nexora Prime")
4. **COPIE A CHAVE AGORA!** (ela não será mostrada novamente)
5. A chave começa com `sk-proj-...`

#### 1.4. Configurar no Render
1. Acesse: https://dashboard.render.com/
2. Clique no serviço `robo-otimizador1`
3. Vá em **Environment** no menu lateral
4. Clique em "Add Environment Variable"
5. Adicione:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `sk-proj-...` (sua chave)
6. Clique em "Save Changes"

✅ **Pronto! OpenAI API configurada!**

---

## 2. Meta Ads API (Facebook/Instagram)

### O que é?
API para criar e gerenciar campanhas de anúncios no Facebook e Instagram.

### Para que serve no Nexora Prime?
- Criação de campanhas no Meta Ads
- Upload de mídia para Facebook/Instagram
- Análise de performance de campanhas
- Espionagem de concorrentes (Facebook Ad Library)

### Custo
- Gratuito (você só paga pelos anúncios que criar)

### Passo a passo:

#### 2.1. Criar conta no Facebook Business
1. Acesse: https://business.facebook.com/
2. Clique em "Criar conta"
3. Preencha os dados da sua empresa
4. Confirme seu email

#### 2.2. Criar um App no Facebook Developers
1. Acesse: https://developers.facebook.com/apps/
2. Clique em "Create App"
3. Escolha "Business" como tipo de app
4. Preencha:
   - **App Name:** "Nexora Prime"
   - **App Contact Email:** seu email
   - **Business Account:** selecione sua conta de negócios
5. Clique em "Create App"

#### 2.3. Adicionar o produto "Marketing API"
1. No painel do app, clique em "Add Product"
2. Encontre "Marketing API" e clique em "Set Up"
3. Aceite os termos de uso

#### 2.4. Gerar Access Token de longa duração
1. Vá em "Tools" > "Graph API Explorer"
2. Selecione seu app no dropdown
3. Clique em "Generate Access Token"
4. Selecione as permissões:
   - `ads_management`
   - `ads_read`
   - `business_management`
   - `pages_read_engagement`
   - `pages_manage_ads`
5. Clique em "Generate Access Token"
6. **COPIE O TOKEN!**

#### 2.5. Converter para token de longa duração
1. Acesse: https://developers.facebook.com/tools/debug/accesstoken/
2. Cole o token curto
3. Clique em "Extend Access Token"
4. **COPIE O TOKEN DE LONGA DURAÇÃO!**

#### 2.6. Obter App ID e App Secret
1. No painel do app, vá em "Settings" > "Basic"
2. Copie o **App ID**
3. Clique em "Show" ao lado de **App Secret** e copie

#### 2.7. Obter Ad Account ID
1. Acesse: https://business.facebook.com/settings/ad-accounts
2. Copie o ID da conta de anúncios (ex: `act_123456789`)

#### 2.8. Obter Business ID
1. Acesse: https://business.facebook.com/settings/info
2. Copie o **Business ID**

#### 2.9. Configurar no Render
1. Acesse: https://dashboard.render.com/
2. Clique no serviço `robo-otimizador1`
3. Vá em **Environment**
4. Adicione as variáveis:
   - **Key:** `META_ACCESS_TOKEN` | **Value:** (token de longa duração)
   - **Key:** `META_APP_ID` | **Value:** (App ID)
   - **Key:** `META_APP_SECRET` | **Value:** (App Secret)
   - **Key:** `META_AD_ACCOUNT_ID` | **Value:** `act_123456789`
   - **Key:** `META_BUSINESS_ID` | **Value:** (Business ID)
5. Clique em "Save Changes"

✅ **Pronto! Meta Ads API configurada!**

---

## 3. Google Ads API

### O que é?
API para criar e gerenciar campanhas de anúncios no Google Ads.

### Para que serve no Nexora Prime?
- Criação de campanhas no Google Ads
- Análise de performance de campanhas
- Espionagem de concorrentes (Google Ads Transparency)

### Custo
- Gratuito (você só paga pelos anúncios que criar)

### Passo a passo:

#### 3.1. Criar conta no Google Ads
1. Acesse: https://ads.google.com/
2. Clique em "Começar agora"
3. Preencha os dados da sua empresa
4. Configure uma campanha inicial (pode pausar depois)

#### 3.2. Criar projeto no Google Cloud Console
1. Acesse: https://console.cloud.google.com/
2. Clique em "Select a project" > "New Project"
3. Nome do projeto: "Nexora Prime"
4. Clique em "Create"

#### 3.3. Ativar a Google Ads API
1. No Google Cloud Console, vá em "APIs & Services" > "Library"
2. Busque por "Google Ads API"
3. Clique em "Enable"

#### 3.4. Criar credenciais OAuth 2.0
1. Vá em "APIs & Services" > "Credentials"
2. Clique em "Create Credentials" > "OAuth client ID"
3. Escolha "Web application"
4. Nome: "Nexora Prime"
5. **Authorized redirect URIs:** `https://developers.google.com/oauthplayground`
6. Clique em "Create"
7. **COPIE O CLIENT ID E CLIENT SECRET!**

#### 3.5. Obter Developer Token
1. Acesse: https://ads.google.com/aw/apicenter
2. Faça login com sua conta Google Ads
3. Clique em "Apply for access"
4. Preencha o formulário
5. Aguarde aprovação (pode levar 1-2 dias)
6. Após aprovação, copie o **Developer Token**

#### 3.6. Gerar Refresh Token
1. Acesse: https://developers.google.com/oauthplayground
2. Clique no ícone de engrenagem (⚙️) no canto superior direito
3. Marque "Use your own OAuth credentials"
4. Cole o **Client ID** e **Client Secret**
5. No campo "Select & authorize APIs", digite: `https://www.googleapis.com/auth/adwords`
6. Clique em "Authorize APIs"
7. Faça login com sua conta Google Ads
8. Clique em "Exchange authorization code for tokens"
9. **COPIE O REFRESH TOKEN!**

#### 3.7. Obter Customer ID
1. Acesse: https://ads.google.com/
2. No canto superior direito, clique no ícone de ferramentas
3. Vá em "Settings" > "Account settings"
4. Copie o **Customer ID** (formato: `123-456-7890`)
5. **Remova os traços:** `1234567890`

#### 3.8. Configurar no Render
1. Acesse: https://dashboard.render.com/
2. Clique no serviço `robo-otimizador1`
3. Vá em **Environment**
4. Adicione as variáveis:
   - **Key:** `GOOGLE_ADS_CLIENT_ID` | **Value:** (Client ID)
   - **Key:** `GOOGLE_ADS_CLIENT_SECRET` | **Value:** (Client Secret)
   - **Key:** `GOOGLE_ADS_DEVELOPER_TOKEN` | **Value:** (Developer Token)
   - **Key:** `GOOGLE_ADS_REFRESH_TOKEN` | **Value:** (Refresh Token)
   - **Key:** `GOOGLE_ADS_CUSTOMER_ID` | **Value:** `1234567890`
   - **Key:** `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | **Value:** `1234567890` (mesmo valor)
5. Clique em "Save Changes"

✅ **Pronto! Google Ads API configurada!**

---

## 4. TikTok Ads API

### O que é?
API para criar e gerenciar campanhas de anúncios no TikTok.

### Para que serve no Nexora Prime?
- Criação de campanhas no TikTok Ads
- Análise de performance de campanhas

### Custo
- Gratuito (você só paga pelos anúncios que criar)

### Passo a passo:

#### 4.1. Criar conta no TikTok Ads
1. Acesse: https://ads.tiktok.com/
2. Clique em "Get Started"
3. Preencha os dados da sua empresa
4. Confirme seu email

#### 4.2. Solicitar acesso à API
1. Acesse: https://ads.tiktok.com/marketing_api/
2. Clique em "Apply for Access"
3. Preencha o formulário:
   - **Company Name:** Nome da sua empresa
   - **Website:** URL do seu site
   - **Use Case:** "Automação de marketing e criação de campanhas"
   - **Monthly Ad Spend:** Escolha uma faixa (ex: $1,000 - $5,000)
4. Clique em "Submit"
5. **Aguarde aprovação** (pode levar 3-7 dias)

#### 4.3. Criar um App (após aprovação)
1. Acesse: https://ads.tiktok.com/marketing_api/apps
2. Clique em "Create App"
3. Preencha:
   - **App Name:** "Nexora Prime"
   - **Description:** "Sistema de automação de marketing"
4. Clique em "Create"

#### 4.4. Obter Access Token
1. No painel do app, vá em "Authentication"
2. Clique em "Generate Access Token"
3. Selecione as permissões:
   - `Campaign Management`
   - `Ad Management`
   - `Reporting`
4. **COPIE O ACCESS TOKEN!**

#### 4.5. Obter App ID e App Secret
1. No painel do app, vá em "Basic Info"
2. Copie o **App ID**
3. Copie o **App Secret**

#### 4.6. Obter Advertiser ID
1. Acesse: https://ads.tiktok.com/
2. No canto superior direito, clique no nome da sua conta
3. Copie o **Advertiser ID**

#### 4.7. Configurar no Render
1. Acesse: https://dashboard.render.com/
2. Clique no serviço `robo-otimizador1`
3. Vá em **Environment**
4. Adicione as variáveis:
   - **Key:** `TIKTOK_ACCESS_TOKEN` | **Value:** (Access Token)
   - **Key:** `TIKTOK_APP_ID` | **Value:** (App ID)
   - **Key:** `TIKTOK_APP_SECRET` | **Value:** (App Secret)
   - **Key:** `TIKTOK_ADVERTISER_ID` | **Value:** (Advertiser ID)
5. Clique em "Save Changes"

✅ **Pronto! TikTok Ads API configurada!**

---

## 5. LinkedIn Ads API (Opcional)

### O que é?
API para criar e gerenciar campanhas de anúncios no LinkedIn.

### Para que serve no Nexora Prime?
- Criação de campanhas no LinkedIn Ads
- Análise de performance de campanhas

### Custo
- Gratuito (você só paga pelos anúncios que criar)

### Passo a passo:

#### 5.1. Criar conta no LinkedIn Campaign Manager
1. Acesse: https://www.linkedin.com/campaignmanager/
2. Clique em "Create ad account"
3. Preencha os dados da sua empresa

#### 5.2. Criar um App no LinkedIn Developers
1. Acesse: https://www.linkedin.com/developers/apps
2. Clique em "Create app"
3. Preencha os dados do app
4. Clique em "Create app"

#### 5.3. Adicionar o produto "Advertising API"
1. No painel do app, clique em "Products"
2. Encontre "Advertising API" e clique em "Request access"
3. Aguarde aprovação (pode levar 1-2 dias)

#### 5.4. Gerar Access Token
1. No painel do app, vá em "Auth"
2. Copie o **Client ID** e **Client Secret**
3. Use o OAuth 2.0 flow para gerar o Access Token
4. **COPIE O ACCESS TOKEN!**

#### 5.5. Obter Ad Account ID
1. Acesse: https://www.linkedin.com/campaignmanager/
2. Copie o ID da conta de anúncios

#### 5.6. Configurar no Render
1. Acesse: https://dashboard.render.com/
2. Adicione as variáveis:
   - **Key:** `LINKEDIN_ACCESS_TOKEN` | **Value:** (Access Token)
   - **Key:** `LINKEDIN_CLIENT_ID` | **Value:** (Client ID)
   - **Key:** `LINKEDIN_CLIENT_SECRET` | **Value:** (Client Secret)
   - **Key:** `LINKEDIN_AD_ACCOUNT_ID` | **Value:** (Ad Account ID)

✅ **Pronto! LinkedIn Ads API configurada!**

---

## 6. Pinterest Ads API (Opcional)

### O que é?
API para criar e gerenciar campanhas de anúncios no Pinterest.

### Passo a passo resumido:
1. Acesse: https://developers.pinterest.com/apps/
2. Crie um app
3. Obtenha o Access Token
4. Configure no Render

---

## 7. Redis (Cache - Opcional)

### O que é?
Banco de dados em memória para cache.

### Para que serve no Nexora Prime?
- Cache de respostas da IA
- Cache de análises de páginas
- Cache de dados de campanhas

### Passo a passo:
1. Acesse: https://redis.com/try-free/
2. Crie uma conta gratuita
3. Crie um banco de dados
4. Copie a URL de conexão (ex: `redis://default:password@host:port`)
5. Configure no Render:
   - **Key:** `REDIS_URL` | **Value:** (URL de conexão)

---

## 8. Sentry (Monitoramento - Opcional)

### O que é?
Plataforma de monitoramento de erros.

### Para que serve no Nexora Prime?
- Monitorar erros em tempo real
- Receber alertas de problemas
- Rastrear performance

### Passo a passo:
1. Acesse: https://sentry.io/signup/
2. Crie uma conta gratuita
3. Crie um novo projeto (Python/Flask)
4. Copie o **DSN** (ex: `https://abc123@sentry.io/123456`)
5. Configure no Render:
   - **Key:** `SENTRY_DSN` | **Value:** (DSN)

---

## 9. AWS S3 (Upload de Mídia - Opcional)

### O que é?
Serviço de armazenamento de arquivos da AWS.

### Para que serve no Nexora Prime?
- Armazenar imagens e vídeos dos anúncios
- Servir mídias com CDN

### Passo a passo:
1. Acesse: https://aws.amazon.com/
2. Crie uma conta (12 meses grátis)
3. Vá em "S3" > "Create bucket"
4. Crie um bucket (ex: `nexora-prime-media`)
5. Vá em "IAM" > "Users" > "Create user"
6. Dê permissões de S3 (AmazonS3FullAccess)
7. Copie o **Access Key ID** e **Secret Access Key**
8. Configure no Render:
   - **Key:** `AWS_ACCESS_KEY_ID` | **Value:** (Access Key ID)
   - **Key:** `AWS_SECRET_ACCESS_KEY` | **Value:** (Secret Access Key)
   - **Key:** `AWS_S3_BUCKET_NAME` | **Value:** `nexora-prime-media`
   - **Key:** `AWS_S3_REGION` | **Value:** `us-east-1`

---

## 10. Stripe (Pagamentos - Opcional)

### O que é?
Plataforma de pagamentos online.

### Para que serve no Nexora Prime?
- Processar pagamentos de assinaturas
- Gerenciar planos e cobranças

### Passo a passo:
1. Acesse: https://dashboard.stripe.com/register
2. Crie uma conta
3. Vá em "Developers" > "API keys"
4. Copie a **Secret key** e **Publishable key**
5. Vá em "Webhooks" > "Add endpoint"
6. URL: `https://robo-otimizador1.onrender.com/webhook/stripe`
7. Copie o **Webhook secret**
8. Configure no Render:
   - **Key:** `STRIPE_SECRET_KEY` | **Value:** (Secret key)
   - **Key:** `STRIPE_PUBLISHABLE_KEY` | **Value:** (Publishable key)
   - **Key:** `STRIPE_WEBHOOK_SECRET` | **Value:** (Webhook secret)

---

## ✅ CHECKLIST FINAL

Marque as APIs que você configurou:

- [ ] OpenAI API (CRÍTICO)
- [ ] Meta Ads API (CRÍTICO)
- [ ] Google Ads API (CRÍTICO)
- [ ] TikTok Ads API (IMPORTANTE)
- [ ] LinkedIn Ads API (Opcional)
- [ ] Pinterest Ads API (Opcional)
- [ ] Redis (Opcional)
- [ ] Sentry (Opcional)
- [ ] AWS S3 (Opcional)
- [ ] Stripe (Opcional)

---

## 📞 SUPORTE

Se você tiver dúvidas ou problemas:

1. Consulte a documentação oficial de cada plataforma
2. Verifique se todas as variáveis estão corretas no Render
3. Reinicie o serviço no Render após adicionar variáveis
4. Abra uma issue no GitHub: https://github.com/fabiinobrega/robo-otimizador/issues

---

**Desenvolvido com ❤️ por Manus AI**  
**Versão:** 2.0  
**Data:** 20 de Janeiro de 2026

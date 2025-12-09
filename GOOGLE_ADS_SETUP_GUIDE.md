# GUIA DE CONFIGURAÇÃO - GOOGLE ADS
## NEXORA PRIME v12.1

---

**Data:** 04 de Dezembro de 2025  
**Status:** ✅ PRONTO PARA CONFIGURAÇÃO

---

## 📋 CREDENCIAIS NECESSÁRIAS

Para integrar o NEXORA PRIME com Google Ads, você precisa configurar as seguintes credenciais no arquivo `.env`:

| Credencial | Descrição | Como Obter |
|:-----------|:----------|:-----------|
| **GOOGLE_ADS_REFRESH_TOKEN** | Token de atualização OAuth2 | [OAuth2 Playground](https://developers.google.com/oauthplayground/) |
| **GOOGLE_ADS_CLIENT_ID** | ID do cliente OAuth2 | Google Cloud Console → APIs & Services → Credentials |
| **GOOGLE_ADS_CLIENT_SECRET** | Secret do cliente OAuth2 | Google Cloud Console → APIs & Services → Credentials |
| **GOOGLE_ADS_LOGIN_CUSTOMER_ID** | ID da conta de login (MCC) | Google Ads → Configurações → Conta |
| **GOOGLE_ADS_DEVELOPER_TOKEN** | Token de desenvolvedor | Google Ads API Center |
| **GOOGLE_ADS_CUSTOMER_ID** | ID da conta de cliente | Google Ads → Configurações → Conta |

---

## 🔧 PASSO A PASSO

### 1. Criar Projeto no Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a **Google Ads API**

### 2. Configurar OAuth2

1. Vá para **APIs & Services → Credentials**
2. Clique em **Create Credentials → OAuth 2.0 Client ID**
3. Selecione **Web application**
4. Adicione redirect URI: `https://developers.google.com/oauthplayground`
5. Copie o **Client ID** e **Client Secret**

### 3. Obter Refresh Token

1. Acesse [OAuth2 Playground](https://developers.google.com/oauthplayground/)
2. Clique no ícone de engrenagem (⚙️) no canto superior direito
3. Marque **Use your own OAuth credentials**
4. Cole seu **Client ID** e **Client Secret**
5. No campo **Step 1**, busque por `https://www.googleapis.com/auth/adwords`
6. Clique em **Authorize APIs**
7. Faça login com sua conta Google Ads
8. Clique em **Exchange authorization code for tokens**
9. Copie o **Refresh Token**

### 4. Obter Developer Token

1. Acesse [Google Ads](https://ads.google.com/)
2. Vá para **Tools & Settings → Setup → API Center**
3. Copie o **Developer Token**

### 5. Obter Customer IDs

1. No Google Ads, vá para **Configurações → Conta**
2. Copie o **Customer ID** (formato: XXX-XXX-XXXX)
3. Se você usa uma conta MCC, copie também o **Login Customer ID**

### 6. Configurar no NEXORA PRIME

Edite o arquivo `.env` na raiz do projeto:

```env
# Google Ads API
GOOGLE_ADS_REFRESH_TOKEN=seu_refresh_token_aqui
GOOGLE_ADS_CLIENT_ID=seu_client_id_aqui.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=seu_client_secret_aqui
GOOGLE_ADS_LOGIN_CUSTOMER_ID=XXX-XXX-XXXX
GOOGLE_ADS_DEVELOPER_TOKEN=seu_developer_token_aqui
GOOGLE_ADS_CUSTOMER_ID=XXX-XXX-XXXX
```

---

## ✅ VALIDAÇÃO

Após configurar as credenciais, você pode validar a integração:

```bash
python3.11 test_ads_integrations.py
```

Ou acesse o painel de créditos:
```
http://localhost:5000/credits-dashboard
```

---

## 🔒 SEGURANÇA

**IMPORTANTE:**
- ❌ **NUNCA** commite o arquivo `.env` no Git
- ❌ **NUNCA** compartilhe suas credenciais publicamente
- ✅ Use variáveis de ambiente em produção
- ✅ Rotacione as credenciais periodicamente

---

## 📚 RECURSOS

- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [OAuth2 Guide](https://developers.google.com/identity/protocols/oauth2)
- [API Center](https://ads.google.com/aw/apicenter)

# PLAYBOOK DE DEPLOY - Robô Otimizador ManusIA v3.0

Guia passo-a-passo para fazer deploy da aplicação no Render.com.

## 📋 Pré-requisitos

- Conta no GitHub (repositório criado)
- Conta no Render.com
- Variáveis de ambiente configuradas

## 🚀 Passo 1: Preparar o Repositório GitHub

### 1.1 Criar repositório (se ainda não existir)

```bash
cd robo-otimizador
git init
git add .
git commit -m "feat: v3.0 - Sistema completo com 94 funcionalidades, mobile responsivo e integrações reais"
git branch -M main
git remote add origin https://github.com/fabiinobrega/robo-otimizador.git
git push -u origin main
```

### 1.2 Verificar arquivos essenciais

Certifique-se de que os seguintes arquivos estão no repositório:
- `main.py` - Aplicação Flask
- `schema.sql` - Banco de dados
- `requirements.txt` - Dependências Python
- `Procfile` - Configuração Render
- `runtime.txt` - Versão Python
- `.env.example` - Variáveis de ambiente
- `templates/` - Templates HTML
- `static/` - CSS e JavaScript
- `services/` - Módulos de serviço

## 🔧 Passo 2: Configurar no Render.com

### 2.1 Acessar Render.com

1. Acesse https://render.com
2. Faça login com sua conta GitHub
3. Clique em "New +" e selecione "Web Service"

### 2.2 Conectar ao Repositório

1. Selecione "GitHub" como provedor
2. Busque e selecione o repositório `robo-otimizador`
3. Clique em "Connect"

### 2.3 Configurar o Serviço

**Nome do Serviço:**
```
robo-otimizador
```

**Ambiente:**
```
Python 3
```

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn main:app
```

### 2.4 Configurar Variáveis de Ambiente

No painel do Render, vá para "Environment" e adicione:

```
SECRET_KEY=sua_chave_secreta_super_segura
FLASK_ENV=production
PORT=5000

# OpenAI
OPENAI_API_KEY=sk-...

# Manus AI
MANUS_API_KEY=sua_manus_api_key
MANUS_AGENT_ID=seu_agent_id

# Google Ads
GOOGLE_ADS_CLIENT_ID=seu_client_id
GOOGLE_ADS_CLIENT_SECRET=seu_client_secret
GOOGLE_ADS_DEVELOPER_TOKEN=seu_developer_token
GOOGLE_ADS_REFRESH_TOKEN=seu_refresh_token
GOOGLE_ADS_CUSTOMER_ID=seu_customer_id

# Facebook/Meta Ads
FACEBOOK_APP_ID=seu_app_id
FACEBOOK_APP_SECRET=seu_app_secret
FACEBOOK_ACCESS_TOKEN=seu_access_token
FACEBOOK_AD_ACCOUNT_ID=act_seu_id
```

### 2.5 Configurar Banco de Dados

**Opção 1: SQLite (Padrão)**
- O SQLite será criado automaticamente no Render
- Arquivo `robo_otimizador.db` será salvo no sistema de arquivos efêmero

**Opção 2: PostgreSQL (Recomendado para Produção)**
1. Crie um banco PostgreSQL no Render
2. Copie a `DATABASE_URL`
3. Adicione como variável de ambiente no Web Service
4. Modifique `main.py` para usar PostgreSQL (veja comentários no código)

### 2.6 Iniciar o Deploy

1. Clique em "Create Web Service"
2. Render iniciará o build automaticamente
3. Aguarde a conclusão (normalmente 2-5 minutos)
4. Acesse a URL fornecida (ex: `https://robo-otimizador.onrender.com`)

## ✅ Passo 3: Verificar o Deploy

### 3.1 Testes Básicos

1. Acesse `https://seu-url.onrender.com/`
2. Verifique se o dashboard carrega
3. Teste a criação de uma campanha
4. Verifique os logs no painel do Render

### 3.2 Verificar Logs

No painel do Render:
1. Vá para "Logs"
2. Procure por erros ou avisos
3. Se houver erro, revise as variáveis de ambiente

### 3.3 Testar Endpoints da API

```bash
# Testar health check
curl https://seu-url.onrender.com/api/dashboard/metrics

# Testar status da IA
curl https://seu-url.onrender.com/api/ai/status
```

## 🔐 Passo 4: Configurar Credenciais de API

### 4.1 Google Ads

1. Acesse Google Cloud Console
2. Crie um projeto
3. Ative a Google Ads API
4. Crie credenciais OAuth2
5. Copie `Client ID`, `Client Secret`, `Developer Token`, `Refresh Token`, `Customer ID`
6. Adicione como variáveis de ambiente no Render

### 4.2 Meta Ads

1. Acesse Meta Developers
2. Crie um app
3. Gere um Access Token de Longa Duração
4. Copie `App ID`, `App Secret`, `Access Token`, `Ad Account ID`
5. Adicione como variáveis de ambiente no Render

### 4.3 OpenAI / Manus

1. Obtenha a chave de API
2. Adicione como variável de ambiente no Render

## 📊 Passo 5: Monitoramento

### 5.1 Configurar Alertas

No Render:
1. Vá para "Settings" > "Alerts"
2. Configure notificações por email
3. Selecione eventos: Deploy Failed, High Memory Usage, etc.

### 5.2 Verificar Logs Regularmente

```bash
# Ver últimos logs
curl https://seu-url.onrender.com/api/activity-logs
```

## 🔄 Passo 6: Atualizações e Manutenção

### 6.1 Fazer Push de Atualizações

```bash
git add .
git commit -m "fix: descrição da mudança"
git push origin main
```

Render fará deploy automático.

### 6.2 Redeployar Manualmente

No painel do Render:
1. Clique em "Manual Deploy"
2. Selecione a branch
3. Clique em "Deploy"

### 6.3 Rollback

Se algo der errado:
1. Vá para "Deploys"
2. Selecione um deploy anterior
3. Clique em "Redeploy"

## 🆘 Troubleshooting

### Erro: "Build failed"
- Verifique `requirements.txt`
- Verifique `runtime.txt` (deve ser Python 3.9+)
- Verifique se há erros de sintaxe em `main.py`

### Erro: "Application failed to start"
- Verifique as variáveis de ambiente
- Verifique os logs no painel do Render
- Certifique-se de que `main.py` tem `if __name__ == '__main__'`

### Erro: "Database connection failed"
- Se usar PostgreSQL, verifique a `DATABASE_URL`
- Se usar SQLite, verifique permissões de arquivo

### Erro: "API credentials not found"
- Verifique se todas as variáveis de ambiente estão configuradas
- Certifique-se de que os nomes das variáveis estão corretos

## 📞 Suporte

Para problemas com Render, veja:
- https://render.com/docs
- https://render.com/support

Para problemas com a aplicação, abra uma issue no GitHub.

---

**Desenvolvido com ❤️ por Manus AI**

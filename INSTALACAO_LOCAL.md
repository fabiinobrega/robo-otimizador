# 🔧 GUIA DE INSTALAÇÃO LOCAL - NEXORA PRIME

Este guia ensina como rodar o Nexora Prime localmente na sua máquina para desenvolvimento e testes.

---

## 📋 PRÉ-REQUISITOS

Antes de começar, certifique-se de ter instalado:

- **Python 3.11+** (https://www.python.org/downloads/)
- **Git** (https://git-scm.com/downloads/)
- **pip** (gerenciador de pacotes Python, geralmente vem com Python)

---

## 🚀 PASSO A PASSO

### 1. **Clonar o Repositório**

```bash
git clone https://github.com/fabiinobrega/robo-otimizador.git
cd robo-otimizador
```

### 2. **Criar Ambiente Virtual (Recomendado)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. **Instalar Dependências**

```bash
pip install -r requirements.txt
```

**Dependências principais:**
- Flask (framework web)
- Flask-CORS (para permitir requisições de diferentes origens)
- openai (para integração com OpenAI)
- requests (para fazer requisições HTTP)
- beautifulsoup4 (para scraping de páginas)
- Pillow (para processamento de imagens)

### 4. **Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas chaves de API:

```env
# OpenAI (Para IA)
OPENAI_API_KEY=sk-proj-...

# Meta Ads (Facebook/Instagram)
META_ACCESS_TOKEN=...
META_APP_ID=...
META_APP_SECRET=...

# Google Ads
GOOGLE_ADS_CLIENT_ID=...
GOOGLE_ADS_CLIENT_SECRET=...
GOOGLE_ADS_DEVELOPER_TOKEN=...
GOOGLE_ADS_REFRESH_TOKEN=...

# TikTok Ads
TIKTOK_ACCESS_TOKEN=...
TIKTOK_APP_ID=...

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
```

**⚠️ IMPORTANTE:** Sem as chaves de API, o sistema funcionará com funcionalidades limitadas.

### 5. **Inicializar o Banco de Dados**

O banco de dados SQLite será criado automaticamente na primeira execução. Se quiser criar manualmente:

```bash
python -c "from main import init_db; init_db()"
```

### 6. **Executar o Servidor**

```bash
python main.py
```

O servidor vai iniciar em: **http://localhost:5000**

### 7. **Acessar o Sistema**

Abra seu navegador e acesse:

```
http://localhost:5000/dashboard
```

---

## 🔑 COMO OBTER AS CHAVES DE API

### OpenAI API Key

1. Acesse https://platform.openai.com/api-keys
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave (começa com `sk-proj-...`)
5. Cole no arquivo `.env`

**Custo:** ~$0.002 por 1000 tokens (muito barato)

### Meta Ads API (Facebook/Instagram)

1. Acesse https://developers.facebook.com/apps/
2. Clique em "Create App"
3. Escolha "Business" como tipo de app
4. Preencha os dados do app
5. Vá em "Add Product" e adicione "Marketing API"
6. Vá em "Tools" > "Graph API Explorer"
7. Selecione seu app e gere um token de acesso
8. Cole no arquivo `.env`

**Documentação:** https://developers.facebook.com/docs/marketing-apis

### Google Ads API

1. Acesse https://console.cloud.google.com/
2. Crie um novo projeto
3. Ative a "Google Ads API"
4. Vá em "Credentials" e crie credenciais OAuth 2.0
5. Baixe o arquivo JSON com as credenciais
6. Obtenha o Developer Token em https://ads.google.com/aw/apicenter
7. Cole as informações no arquivo `.env`

**Documentação:** https://developers.google.com/google-ads/api/docs/start

### TikTok Ads API

1. Acesse https://ads.tiktok.com/marketing_api/
2. Faça login com sua conta TikTok Ads
3. Clique em "Apply for Access"
4. Preencha o formulário de solicitação
5. Aguarde aprovação (pode levar alguns dias)
6. Após aprovação, crie um app e obtenha o Access Token
7. Cole no arquivo `.env`

**Documentação:** https://ads.tiktok.com/marketing_api/docs

---

## 🧪 TESTANDO O SISTEMA

### Teste 1: Verificar se o servidor está rodando

```bash
curl http://localhost:5000/api/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "version": "2.0"
}
```

### Teste 2: Verificar se o banco de dados foi criado

```bash
ls -la database.db
```

### Teste 3: Acessar o Dashboard

Abra o navegador e acesse: http://localhost:5000/dashboard

Você deve ver a página do dashboard com métricas e gráficos.

### Teste 4: Criar um anúncio

1. Acesse: http://localhost:5000/create-perfect-ad-premium
2. Preencha os campos obrigatórios
3. Clique em "Iniciar Análise IA"
4. Aguarde a análise e navegue pelas etapas

---

## 🐛 TROUBLESHOOTING (RESOLUÇÃO DE PROBLEMAS)

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Address already in use"

**Solução:** A porta 5000 já está em uso. Mate o processo ou use outra porta:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

Ou execute em outra porta:
```bash
python main.py --port 5001
```

### Erro: "OpenAI API key not found"

**Solução:** Verifique se o arquivo `.env` existe e contém a chave `OPENAI_API_KEY`.

### Erro: "Database is locked"

**Solução:** Feche todas as conexões com o banco de dados e reinicie o servidor:
```bash
rm database.db
python main.py
```

### Página em branco ou erro 404

**Solução:** Verifique se o servidor está rodando e se você está acessando a URL correta:
```
http://localhost:5000/dashboard
```

---

## 📂 ESTRUTURA DE PASTAS

```
robo-otimizador/
├── main.py                 # Backend principal (Flask)
├── database.db             # Banco de dados SQLite (criado automaticamente)
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis de ambiente (você cria)
├── .env.example            # Exemplo de variáveis de ambiente
├── README.md               # Documentação principal
├── templates/              # Templates HTML
│   ├── base_nexora.html
│   ├── dashboard.html
│   ├── create_perfect_ad_premium.html
│   └── ...
├── static/                 # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── services/               # Serviços backend
│   ├── velyra_prime.py
│   ├── ad_creator_service.py
│   └── ...
└── tests/                  # Testes automatizados
```

---

## 🔄 ATUALIZANDO O CÓDIGO

Para atualizar o código local com as últimas mudanças do repositório:

```bash
git pull origin main
pip install -r requirements.txt  # Atualizar dependências
python main.py                   # Reiniciar servidor
```

---

## 📝 COMANDOS ÚTEIS

### Limpar cache do Python

```bash
# Windows
rmdir /s /q __pycache__
rmdir /s /q .pytest_cache

# Linux/Mac
rm -rf __pycache__
rm -rf .pytest_cache
```

### Verificar versão do Python

```bash
python --version
```

### Listar dependências instaladas

```bash
pip list
```

### Atualizar pip

```bash
python -m pip install --upgrade pip
```

### Criar arquivo requirements.txt

```bash
pip freeze > requirements.txt
```

---

## 🚀 DEPLOY EM PRODUÇÃO

Para fazer deploy em produção no Render:

1. Faça push do código para o GitHub:
```bash
git add .
git commit -m "Atualização do sistema"
git push origin main
```

2. Acesse o dashboard do Render: https://dashboard.render.com/
3. Clique no serviço `robo-otimizador1`
4. Clique em "Manual Deploy" > "Deploy latest commit"
5. Aguarde o build completar (~2-3 minutos)
6. Acesse: https://robo-otimizador1.onrender.com/

---

## 📞 SUPORTE

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a seção de **Troubleshooting** acima
2. Consulte a documentação completa em `NEXORA_PRIME_COMPLETO.md`
3. Abra uma issue no GitHub: https://github.com/fabiinobrega/robo-otimizador/issues

---

**Desenvolvido com ❤️ por Manus AI**  
**Versão:** 2.0  
**Data:** 20 de Janeiro de 2026

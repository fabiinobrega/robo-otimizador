# Robô Otimizador ManusIA v3.0

Um sistema completo de automação e otimização de campanhas de publicidade digital com integração de IA (Manus, OpenAI), Google Ads, Meta Ads, TikTok, Pinterest e LinkedIn.

## 🚀 Funcionalidades Principais (94 Features)

### Dashboard
- Métricas em tempo real (campanhas ativas, cliques, conversões, CPA, ROI)
- Gráficos interativos com Chart.js
- Logs de atividade recentes
- Status da IA em tempo real

### Criar Campanha com IA
- Wizard de 5 passos
- Análise de página com IA
- Geração de copy com IA
- Pré-visualização de anúncio (Meta Ads)
- Upload de mídia com preview

### Minhas Campanhas
- Tabela com filtros e busca
- Status em tempo real
- Ações: ver, editar, duplicar, pausar, lançar, deletar

### Espionagem de Concorrentes
- Análise de concorrentes por keyword
- Anúncios ativos, histórico, estratégias

### DCO Builder
- Geração automática de criativos
- Combinações criativas
- Teste A/B automático

### E mais 89 funcionalidades...

## 📱 Responsividade Mobile

O sistema é **100% responsivo** e funcional em:
- iPhone, Android, Tablets
- Todas as 94 funcionalidades disponíveis em mobile
- Menu hambúrguer automático
- Formulários otimizados para toque

## 🛠️ Instalação

### Pré-requisitos
- Python 3.9+
- pip
- Git

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/fabiinobrega/robo-otimizador.git
cd robo-otimizador
```

2. Crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. Inicie o servidor:
```bash
python main.py
```

6. Acesse a aplicação:
```
http://localhost:5000
```

## 🚀 Deploy no Render

Veja `PLAYBOOK_DEPLOY.md` para instruções detalhadas.

## 📊 Estrutura do Projeto

```
robo-otimizador/
├── main.py
├── schema.sql
├── requirements.txt
├── Procfile
├── runtime.txt
├── services/
├── templates/
└── static/
```

## 🔌 Endpoints da API

- `GET /api/dashboard/metrics` - Métricas
- `POST /api/create-campaign` - Criar campanha
- `POST /api/media/upload` - Upload de mídia
- `POST /api/analyze-landing-page` - Analisar página
- `POST /api/competitor-spy` - Espionagem
- `POST /api/dco/generate-copy` - Gerar copy
- E mais...

## 📄 Licença

MIT License

---

**Desenvolvido com ❤️ por Manus AI**

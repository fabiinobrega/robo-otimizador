# 📊 SIMILARWEB INTEGRATION GUIDE - NEXORA PRIME

## 🎯 Visão Geral

A integração Similarweb no Nexora Prime atua como **SENSOR DE MERCADO**, fornecendo inteligência competitiva para apoiar decisões estratégicas.

### ⚠️ REGRAS ABSOLUTAS

**Similarweb NÃO pode:**
- ❌ Tomar decisões financeiras
- ❌ Escalar orçamento
- ❌ Pausar campanhas
- ❌ Ser fonte única de ROI
- ❌ Atuar no Velyra Prime

**Similarweb APENAS:**
- ✅ Fornece dados de mercado estimados
- ✅ Apoia decisões humanas
- ✅ Valida projeções
- ✅ Identifica tendências

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     NEXORA PRIME                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Camada 1   │  │   Camada 2   │  │   Camada 3   │    │
│  │  Similarweb  │─▶│   Manus IA   │─▶│Velyra Prime  │    │
│  │   (Sensor)   │  │ (Estratégia) │  │  (Execução)  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  Dados estimados   Interpreta dados   Dados reais          │
│  Macro tendências  Gera insights      ROAS, CPA, CTR       │
│  Confirmação       Market Score       Otimizações          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Componentes Implementados

### 1. **Market Intelligence Service**
**Arquivo:** `services/market_intelligence_similarweb.py`

**Responsabilidades:**
- Conectar à API Similarweb
- Consultar domínios concorrentes
- Retornar dados normalizados
- Cache inteligente (1 hora TTL)
- Fallback silencioso

**Métodos principais:**
```python
# Obter visão geral de tráfego
market_intelligence.get_traffic_overview(domain, period='3m')

# Obter fontes de tráfego
market_intelligence.get_traffic_sources(domain)

# Obter distribuição geográfica
market_intelligence.get_geo_distribution(domain)

# Obter sinal de tendência
market_intelligence.get_trend_signal(domain)

# Obter Market Confidence Score (0-100)
market_intelligence.get_market_confidence_score(domain)
```

---

### 2. **Market Confidence Score**

Score proprietário Nexora baseado em:
- **Tráfego** (30 pontos): Volume de visitantes
- **Tráfego Pago** (25 pontos): Presença de anúncios
- **Estabilidade** (20 pontos): Consistência ao longo do tempo
- **Tendência** (25 pontos): Crescimento ou declínio

**Classificação:**
- **0-39:** Produto de risco ⚠️
- **40-69:** Produto instável ⚡
- **70-84:** Produto validado ✅
- **85-100:** Produto em forte tração 🚀

---

### 3. **Integração com Espionagem**
**Arquivo:** `services/competitor_spy_engine.py`

**Modificações:**
- Novo parâmetro `competitor_domain`
- Método `_get_market_intelligence()`
- Market Intelligence adicionado ao relatório

**Uso:**
```python
from services.competitor_spy_engine import CompetitorSpyEngine

spy = CompetitorSpyEngine()
report = spy.analyze_competitors(
    product="Curso de Python",
    niche="Educação Online",
    platform="facebook",
    competitor_domain="udemy.com"  # Opcional
)

# Relatório inclui:
# - analysis: Análise de concorrentes
# - market_intelligence: Dados Similarweb
```

---

### 4. **Simulação Financeira**
**Arquivo:** `services/financial_simulator.py`

**Funcionalidades:**
- Simula resultados de campanhas
- Ajusta CPC baseado em Market Confidence Score
- Ajusta conversão baseado em tendências
- Valida orçamentos contra realidade de mercado

**Uso:**
```python
from services.financial_simulator import financial_simulator

# Simular campanha
simulation = financial_simulator.simulate_campaign(
    budget=5000,
    platform='facebook',
    niche='E-commerce',
    product_type='ecommerce',
    competitor_domain='amazon.com.br'  # Opcional
)

# Validar orçamento
validation = financial_simulator.validate_budget_proposal(
    budget=10000,
    expected_roas=5.0,
    competitor_domain='amazon.com.br'  # Opcional
)
```

---

### 5. **CEO Dashboard - Market Intelligence Panel**
**Arquivo:** `templates/dashboard_nexora.html`

**Métricas exibidas:**
- Market Confidence Score (0-100)
- Tendência de Mercado (↑/↓/→)
- Tráfego Pago (%)
- Nível de Risco (Baixo/Médio/Alto)

**Disclaimer visível:**
> "Dados estimados - usados apenas como suporte estratégico"

---

## 🔌 APIs Disponíveis

### 1. Market Intelligence
```http
GET /api/market-intelligence?domain=example.com
```

**Response:**
```json
{
  "success": true,
  "intelligence": {
    "domain": "example.com",
    "confidence_score": {
      "score": 75,
      "classification": "validated",
      "risk_level": "low",
      "message": "Produto validado"
    },
    "trend": {
      "signal": "up",
      "confidence": 82,
      "message": "Crescimento moderado (+8.2%)"
    },
    "traffic_sources": {
      "paid_search": 15.5
    },
    "disclaimer": "Dados estimados - usados apenas como suporte estratégico"
  }
}
```

### 2. Simulação Financeira
```http
POST /api/financial-simulator/simulate
Content-Type: application/json

{
  "budget": 5000,
  "platform": "facebook",
  "niche": "E-commerce",
  "product_type": "ecommerce",
  "competitor_domain": "amazon.com.br"
}
```

**Response:**
```json
{
  "success": true,
  "simulation": {
    "budget": 5000,
    "projections": {
      "estimated": {
        "clicks": 4167,
        "conversions": 83.34,
        "cpa": 60.00,
        "cpc": 1.20
      },
      "best_case": {...},
      "worst_case": {...}
    },
    "market_intelligence": {...},
    "warnings": [],
    "disclaimer": "⚠️ Simulação baseada em estimativas"
  }
}
```

### 3. Validação de Orçamento
```http
POST /api/financial-simulator/validate-budget
Content-Type: application/json

{
  "budget": 10000,
  "expected_roas": 5.0,
  "competitor_domain": "amazon.com.br"
}
```

---

## 🔐 Configuração

### 1. Obter API Key Similarweb

1. Acesse: https://account.similarweb.com/
2. Crie uma conta ou faça login
3. Vá para "API Access"
4. Gere uma API Key

### 2. Configurar no Nexora

**Opção 1: Variável de Ambiente**
```bash
export SIMILARWEB_API_KEY="your_api_key_here"
```

**Opção 2: Arquivo .env**
```env
SIMILARWEB_API_KEY=your_api_key_here
```

### 3. Verificar Configuração

```python
from services.market_intelligence_similarweb import market_intelligence

# Testar conexão
result = market_intelligence.get_traffic_overview('google.com', '3m')

if result:
    print("✅ Similarweb configurado corretamente!")
else:
    print("❌ Verifique sua API key")
```

---

## 🧪 Testes

**Executar testes:**
```bash
cd /home/ubuntu/robo-otimizador
python3 tests/test_market_intelligence_similarweb.py
```

**Cobertura:**
- ✅ Inicialização do serviço
- ✅ Conexão válida com API
- ✅ Timeout da API
- ✅ Domínio inválido
- ✅ Cálculo de trend signal
- ✅ Cálculo de Market Confidence Score
- ✅ Sistema funciona sem Similarweb
- ✅ Funcionalidade de cache
- ✅ Geração de mensagens
- ✅ Cálculo de datas

---

## 📊 Uso no Dashboard CEO

1. Acesse: https://robo-otimizador1.onrender.com/dashboard
2. Veja o painel "Market Intelligence"
3. Configure um domínio concorrente nas configurações
4. Clique em "Atualizar" para obter dados atualizados

---

## 🚨 Troubleshooting

### Problema: "Dados não disponíveis"

**Causas possíveis:**
1. API key não configurada
2. Domínio inválido
3. Timeout da API
4. Limite de requisições excedido

**Solução:**
```bash
# Verificar API key
echo $SIMILARWEB_API_KEY

# Testar manualmente
python3 -c "from services.market_intelligence_similarweb import market_intelligence; print(market_intelligence.get_traffic_overview('google.com', '3m'))"
```

### Problema: Sistema lento

**Causa:** Cache desabilitado ou TTL muito baixo

**Solução:**
```python
# Ajustar TTL do cache (em segundos)
market_intelligence.cache_ttl = 7200  # 2 horas
```

---

## 📈 Próximos Passos

### Imediato
1. ✅ Configurar API key Similarweb
2. ✅ Testar integração
3. ✅ Configurar domínio concorrente

### Médio Prazo
1. ⏳ Adicionar mais domínios para análise
2. ⏳ Criar alertas de tendência
3. ⏳ Integrar com automação de campanhas

### Longo Prazo
1. ⏳ Machine Learning para previsões
2. ⏳ Análise de múltiplos concorrentes
3. ⏳ Benchmarking automático

---

## 📞 Suporte

**Documentação Similarweb:**
- https://developer.similarweb.com/

**Documentação Nexora:**
- Veja `README.md` no repositório

**Issues:**
- https://github.com/fabiinobrega/robo-otimizador/issues

---

## ✅ Checklist de Implementação

- [x] Serviço Market Intelligence implementado
- [x] Integração com Competitor Spy
- [x] Integração com Financial Simulator
- [x] Painel CEO Dashboard
- [x] APIs REST criadas
- [x] Testes completos (10/10 passando)
- [x] Documentação completa
- [x] Deploy em produção
- [x] Fallback silencioso
- [x] Cache implementado

---

**Última atualização:** 13 de Janeiro de 2026  
**Versão:** 1.0.0  
**Status:** ✅ Produção

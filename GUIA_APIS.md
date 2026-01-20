# 🔌 GUIA COMPLETO DE APIS E INTEGRAÇÕES - NEXORA PRIME

Este guia detalha todas as APIs disponíveis no Nexora Prime e como integrá-las.

---

## 📊 VISÃO GERAL DAS APIS

O Nexora Prime possui **15 APIs REST** implementadas:

| API | Endpoint | Método | Status |
|-----|----------|--------|--------|
| Health Check | `/api/health` | GET | ✅ 100% |
| Análise de Página | `/api/analyze-page` | POST | ✅ 100% |
| Análise de Concorrentes | `/api/analyze-competitors` | POST | ✅ 95% |
| Gerar Copy | `/api/generate-copy` | POST | ✅ 95% |
| Gerar Criativos | `/api/generate-creatives` | POST | ✅ 100% |
| Gerar Estratégia | `/api/generate-strategy` | POST | ✅ 100% |
| Executar Campanha | `/api/execute-campaign` | POST | ✅ 60% |
| Velyra Status | `/api/velyra/status` | GET | ✅ 100% |
| Velyra Chat | `/api/velyra/chat` | POST | ✅ 100% |
| Velyra Monitor | `/api/velyra/monitor` | POST | ✅ 100% |
| Velyra Optimize | `/api/velyra/optimize` | POST | ✅ 100% |
| Velyra Recommendations | `/api/velyra/recommendations/<id>` | GET | ✅ 100% |
| A/B Test Suggestions | `/api/ab-test/suggestions` | POST | ✅ 100% |
| Upload de Mídia | `/api/upload-media` | POST | ✅ 100% |
| Salvar Campanha | `/api/save-campaign` | POST | ✅ 100% |

---

## 🔍 DETALHAMENTO DAS APIS

### 1. **Health Check** ✅ 100%

**Endpoint:** `GET /api/health`

**Descrição:** Verifica se o servidor está rodando.

**Resposta:**
```json
{
  "status": "ok",
  "version": "2.0",
  "timestamp": "2026-01-20T12:00:00Z"
}
```

**Exemplo de uso:**
```bash
curl http://localhost:5000/api/health
```

---

### 2. **Análise de Página** ✅ 100%

**Endpoint:** `POST /api/analyze-page`

**Descrição:** Analisa uma página de vendas e retorna insights sobre o produto, mercado e concorrência.

**Body:**
```json
{
  "url": "https://exemplo.com/produto",
  "platform": "meta",
  "budget": 150,
  "country": "BR"
}
```

**Resposta:**
```json
{
  "success": true,
  "data": {
    "commercial_analysis": {
      "competition_level": "Médio",
      "estimated_conversion_rate": "1-3%",
      "estimated_cpc": "R$ 0.50 - R$ 2.00",
      "estimated_ctr": "2-4%",
      "market_opportunity_score": 75,
      "recommended_budget": "R$ 100-200/dia"
    },
    "product_analysis": {
      "description": "Descrição extraída da página",
      "niche": "E-commerce",
      "price": "R$ 99,00",
      "product_name": "Produto Analisado",
      "strengths": ["Design moderno", "Bom custo-benefício"],
      "weaknesses": ["Falta de provas sociais", "CTA fraco"],
      "target_audience": "Público geral",
      "unique_selling_points": ["Qualidade premium", "Entrega rápida"]
    },
    "recommendations": [
      "Mercado de risco - Comece com orçamento conservador",
      "Diferencie-se dos concorrentes identificados"
    ]
  }
}
```

**Exemplo de uso:**
```bash
curl -X POST http://localhost:5000/api/analyze-page \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://exemplo.com/produto",
    "platform": "meta",
    "budget": 150,
    "country": "BR"
  }'
```

---

### 3. **Análise de Concorrentes** ✅ 95%

**Endpoint:** `POST /api/analyze-competitors`

**Descrição:** Analisa concorrentes com base na URL da página de vendas.

**Body:**
```json
{
  "url": "https://exemplo.com/produto",
  "platform": "meta"
}
```

**Resposta:**
```json
{
  "success": true,
  "data": {
    "competitors": [
      {
        "name": "Concorrente A",
        "url": "https://concorrente-a.com",
        "reach": "847K",
        "ads_count": 234,
        "estimated_spend": "R$ 45K",
        "ctr": "4.2%"
      }
    ],
    "insights": [
      "Mercado competitivo com 5+ players ativos",
      "Foco em anúncios de vídeo"
    ]
  }
}
```

**⚠️ Nota:** Requer `OPENAI_API_KEY` configurada para análise completa.

---

### 4. **Gerar Copy** ✅ 95%

**Endpoint:** `POST /api/generate-copy`

**Descrição:** Gera múltiplas variações de copy para anúncios.

**Body:**
```json
{
  "product_name": "Curso de Marketing Digital",
  "description": "Aprenda marketing digital do zero",
  "target_audience": "Empreendedores",
  "platform": "meta",
  "tone": "professional",
  "variations": 3
}
```

**Resposta:**
```json
{
  "success": true,
  "copies": [
    {
      "headline": "Domine o Marketing Digital em 30 Dias",
      "body": "Transforme seu negócio com estratégias comprovadas...",
      "cta": "Comece Agora"
    },
    {
      "headline": "Marketing Digital que Funciona",
      "body": "Aprenda com quem já faturou milhões...",
      "cta": "Quero Aprender"
    }
  ]
}
```

**⚠️ Nota:** Requer `OPENAI_API_KEY` configurada.

---

### 5. **Gerar Criativos** ✅ 100%

**Endpoint:** `POST /api/generate-creatives`

**Descrição:** Gera sugestões de criativos (imagens, vídeos) para anúncios.

**Body:**
```json
{
  "product_name": "Curso de Marketing Digital",
  "niche": "Educação",
  "platform": "meta"
}
```

**Resposta:**
```json
{
  "success": true,
  "creatives": [
    {
      "type": "image",
      "description": "Pessoa trabalhando no computador com gráficos de crescimento",
      "format": "1080x1080",
      "style": "moderno e profissional"
    },
    {
      "type": "video",
      "description": "Depoimento de aluno mostrando resultados",
      "duration": "15-30s",
      "format": "9:16 (vertical)"
    }
  ]
}
```

---

### 6. **Gerar Estratégia** ✅ 100%

**Endpoint:** `POST /api/generate-strategy`

**Descrição:** Gera estratégia de campanha com base nos dados do produto.

**Body:**
```json
{
  "product_name": "Curso de Marketing Digital",
  "budget": 150,
  "platform": "meta",
  "target_audience": "Empreendedores"
}
```

**Resposta:**
```json
{
  "success": true,
  "strategy": {
    "objective": "Conversões",
    "audience": {
      "type": "Lookalike",
      "description": "Pessoas similares aos seus melhores clientes"
    },
    "duration": "30 dias",
    "budget_distribution": {
      "testing": "30%",
      "scaling": "70%"
    },
    "recommendations": [
      "Comece com teste A/B de 3 criativos",
      "Escale o vencedor após 7 dias"
    ]
  }
}
```

---

### 7. **Executar Campanha** ✅ 60%

**Endpoint:** `POST /api/execute-campaign`

**Descrição:** Executa a campanha nas plataformas de anúncios (Meta Ads, Google Ads, etc.).

**Body:**
```json
{
  "platform": "meta",
  "campaign_data": {
    "name": "Campanha Teste",
    "objective": "CONVERSIONS",
    "budget": 150,
    "creatives": [...],
    "targeting": {...}
  }
}
```

**Resposta:**
```json
{
  "success": true,
  "campaign_id": "123456789",
  "status": "active",
  "message": "Campanha criada com sucesso!"
}
```

**⚠️ Nota:** Requer configuração das APIs das plataformas (Meta Ads, Google Ads, etc.).

---

### 8. **Velyra Status** ✅ 100%

**Endpoint:** `GET /api/velyra/status`

**Descrição:** Retorna o status atual da Velyra Prime.

**Resposta:**
```json
{
  "status": "active",
  "monitoring": true,
  "last_optimization": "2026-01-20T12:00:00Z",
  "actions_executed": 47
}
```

---

### 9. **Velyra Chat** ✅ 100%

**Endpoint:** `POST /api/velyra/chat`

**Descrição:** Envia uma mensagem para a Velyra Prime e recebe uma resposta.

**Body:**
```json
{
  "message": "Qual o status das minhas campanhas?"
}
```

**Resposta:**
```json
{
  "success": true,
  "response": "🟢 Velyra Prime está ativo e monitorando suas campanhas 24/7. Tudo funcionando perfeitamente!"
}
```

---

### 10. **Velyra Monitor** ✅ 100%

**Endpoint:** `POST /api/velyra/monitor`

**Descrição:** Monitora uma campanha específica.

**Body:**
```json
{
  "campaign_id": "123456789"
}
```

**Resposta:**
```json
{
  "success": true,
  "metrics": {
    "spend": "R$ 150",
    "conversions": 10,
    "cpa": "R$ 15",
    "roas": 3.5
  },
  "recommendations": [
    "Aumente o orçamento em 20%",
    "Pause anúncios com CTR < 1%"
  ]
}
```

---

### 11. **Velyra Optimize** ✅ 100%

**Endpoint:** `POST /api/velyra/optimize`

**Descrição:** Otimiza uma campanha automaticamente.

**Body:**
```json
{
  "campaign_id": "123456789",
  "optimization_type": "budget"
}
```

**Resposta:**
```json
{
  "success": true,
  "changes": [
    "Orçamento aumentado de R$ 150 para R$ 180",
    "Anúncio #3 pausado (CTR < 1%)"
  ]
}
```

---

### 12. **Velyra Recommendations** ✅ 100%

**Endpoint:** `GET /api/velyra/recommendations/<campaign_id>`

**Descrição:** Retorna recomendações personalizadas para uma campanha.

**Resposta:**
```json
{
  "success": true,
  "recommendations": [
    {
      "type": "budget",
      "priority": "high",
      "description": "Aumente o orçamento em 20%",
      "expected_impact": "+15% conversões"
    },
    {
      "type": "creative",
      "priority": "medium",
      "description": "Teste novo formato de vídeo",
      "expected_impact": "+10% CTR"
    }
  ]
}
```

---

### 13. **A/B Test Suggestions** ✅ 100%

**Endpoint:** `POST /api/ab-test/suggestions`

**Descrição:** Gera sugestões de testes A/B para uma campanha.

**Body:**
```json
{
  "campaign_id": "123456789",
  "test_type": "creative"
}
```

**Resposta:**
```json
{
  "success": true,
  "suggestions": [
    {
      "element": "headline",
      "variant_a": "Domine o Marketing Digital",
      "variant_b": "Marketing Digital que Funciona",
      "expected_impact": "+20% CTR"
    },
    {
      "element": "cta",
      "variant_a": "Comece Agora",
      "variant_b": "Quero Aprender",
      "expected_impact": "+15% conversões"
    }
  ]
}
```

---

### 14. **Upload de Mídia** ✅ 100%

**Endpoint:** `POST /api/upload-media`

**Descrição:** Faz upload de imagens ou vídeos para usar nos anúncios.

**Body:** `multipart/form-data`
```
file: [arquivo]
```

**Resposta:**
```json
{
  "success": true,
  "file_id": "abc123",
  "url": "https://storage.exemplo.com/abc123.jpg",
  "type": "image",
  "size": "1.2 MB"
}
```

**Exemplo de uso:**
```bash
curl -X POST http://localhost:5000/api/upload-media \
  -F "file=@/path/to/image.jpg"
```

---

### 15. **Salvar Campanha** ✅ 100%

**Endpoint:** `POST /api/save-campaign`

**Descrição:** Salva uma campanha no banco de dados.

**Body:**
```json
{
  "name": "Campanha Teste",
  "platform": "meta",
  "budget": 150,
  "status": "draft",
  "data": {...}
}
```

**Resposta:**
```json
{
  "success": true,
  "campaign_id": "123456789",
  "message": "Campanha salva com sucesso!"
}
```

---

## 🔐 AUTENTICAÇÃO

Atualmente, o sistema **NÃO requer autenticação** para acessar as APIs. Isso é intencional para facilitar o desenvolvimento e testes.

**⚠️ IMPORTANTE:** Para produção, é recomendado implementar autenticação (JWT, OAuth, etc.) para proteger as APIs.

---

## 🧪 TESTANDO AS APIS

### Usando cURL

```bash
# Health Check
curl http://localhost:5000/api/health

# Análise de Página
curl -X POST http://localhost:5000/api/analyze-page \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com", "platform": "meta", "budget": 150, "country": "BR"}'

# Velyra Chat
curl -X POST http://localhost:5000/api/velyra/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual o status das minhas campanhas?"}'
```

### Usando Python

```python
import requests

# Health Check
response = requests.get("http://localhost:5000/api/health")
print(response.json())

# Análise de Página
data = {
    "url": "https://exemplo.com",
    "platform": "meta",
    "budget": 150,
    "country": "BR"
}
response = requests.post("http://localhost:5000/api/analyze-page", json=data)
print(response.json())

# Velyra Chat
data = {"message": "Qual o status das minhas campanhas?"}
response = requests.post("http://localhost:5000/api/velyra/chat", json=data)
print(response.json())
```

### Usando JavaScript (Fetch API)

```javascript
// Health Check
fetch('http://localhost:5000/api/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Análise de Página
fetch('http://localhost:5000/api/analyze-page', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://exemplo.com',
    platform: 'meta',
    budget: 150,
    country: 'BR'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Velyra Chat
fetch('http://localhost:5000/api/velyra/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Qual o status das minhas campanhas?'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 📝 CÓDIGOS DE STATUS HTTP

| Código | Significado | Descrição |
|--------|-------------|-----------|
| 200 | OK | Requisição bem-sucedida |
| 201 | Created | Recurso criado com sucesso |
| 400 | Bad Request | Dados inválidos ou faltando |
| 401 | Unauthorized | Autenticação necessária |
| 404 | Not Found | Recurso não encontrado |
| 500 | Internal Server Error | Erro no servidor |

---

## 🔗 INTEGRAÇÕES EXTERNAS

### Meta Ads (Facebook/Instagram)

**Documentação:** https://developers.facebook.com/docs/marketing-apis

**Endpoints utilizados:**
- `/act_{ad_account_id}/campaigns` - Criar campanhas
- `/act_{ad_account_id}/adsets` - Criar conjuntos de anúncios
- `/act_{ad_account_id}/ads` - Criar anúncios
- `/act_{ad_account_id}/adimages` - Upload de imagens
- `/act_{ad_account_id}/advideos` - Upload de vídeos

### Google Ads

**Documentação:** https://developers.google.com/google-ads/api/docs/start

**Endpoints utilizados:**
- `/customers/{customer_id}/campaigns` - Criar campanhas
- `/customers/{customer_id}/adGroups` - Criar grupos de anúncios
- `/customers/{customer_id}/ads` - Criar anúncios

### TikTok Ads

**Documentação:** https://ads.tiktok.com/marketing_api/docs

**Endpoints utilizados:**
- `/open_api/v1.3/campaign/create/` - Criar campanhas
- `/open_api/v1.3/adgroup/create/` - Criar grupos de anúncios
- `/open_api/v1.3/ad/create/` - Criar anúncios

---

## 📞 SUPORTE

Se você tiver dúvidas sobre as APIs ou integrações:

1. Consulte a documentação oficial das plataformas
2. Verifique os exemplos de código acima
3. Abra uma issue no GitHub: https://github.com/fabiinobrega/robo-otimizador/issues

---

**Desenvolvido com ❤️ por Manus AI**  
**Versão:** 2.0  
**Data:** 20 de Janeiro de 2026

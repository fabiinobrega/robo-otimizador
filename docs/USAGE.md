# 📖 Guia de Uso - Nexora Prime

## Visão Geral

O Nexora Prime é uma plataforma completa de automação de marketing digital com IA. Este guia explica como usar as principais funcionalidades.

---

## 🎯 Gerar Anúncio Perfeito (1-Click)

### Acesso
Navegue para: `/generate-perfect-ad`

### Campos do Formulário

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| URL do Produto | URL | ✅ Sim | Link da página de vendas do seu produto |
| Plataforma | Select | ✅ Sim | Facebook Ads, Google Ads ou Ambas |
| Localização | Texto | ✅ Sim | País/região alvo (padrão: Brasil) |
| Meta de Vendas | Número | ❌ Não | Quantas vendas deseja alcançar |
| Orçamento Total (R$) | Número | ✅ Sim | Mínimo R$ 50,00 |
| Duração (dias) | Número | ✅ Sim | De 1 a 365 dias |
| Auto-Publish | Toggle | ❌ Não | Publicar automaticamente |
| Executar Sandbox | Toggle | ❌ Não | Testar sem gastar dinheiro |

### Validações

- **URL**: Deve começar com `http://` ou `https://`
- **Orçamento**: Mínimo R$ 50,00
- **Duração**: Entre 1 e 365 dias
- **Orçamento Diário**: Mínimo R$ 5,00/dia (calculado automaticamente)

### Fluxo de Execução

1. **Análise da Landing Page** (10%)
   - Extrai título, preço, benefícios
   - Gera insights com IA

2. **Espionagem de Concorrentes** (30%)
   - Analisa anúncios ativos
   - Identifica melhores práticas

3. **Geração de Copy** (50%)
   - Cria 3 variantes de anúncios
   - Headlines, descrições, CTAs

4. **Geração de Criativos** (70%)
   - Sugere imagens/vídeos
   - Formatos otimizados

5. **Simulação de Performance** (90%)
   - CTR, CPC, impressões estimadas
   - ROAS projetado

### Resultados Exibidos

- **Análise da Landing Page**: Título, preço, benefícios, insights
- **Anúncios de Concorrentes**: Top 3 com scores
- **Variantes Geradas**: 3 opções com headline, descrição, CTA
- **Estimativa de Performance**: CTR, CPC, impressões, cliques, conversões, ROAS

### Ações Disponíveis

- **Editar Manualmente**: Ajustar copy antes de publicar
- **Aprovar & Publicar**: Enviar para a plataforma
- **Executar Sandbox**: Testar sem gastar
- **Rodar A/B Test**: Comparar variantes

---

## 📊 Dashboard

### Acesso
Navegue para: `/dashboard`

### Painéis de Crédito

| Painel | Cores | Significado |
|--------|-------|-------------|
| OpenAI | 🟢 Verde | API conectada e funcionando |
| OpenAI | 🟡 Amarelo | Créditos baixos |
| OpenAI | 🔴 Vermelho | Sem créditos ou API inválida |
| Manus | 🟢 Verde | Integrado e ativo |

### Métricas Principais

- **Campanhas Ativas**: Total de campanhas em execução
- **Total de Cliques**: Soma de cliques de todas as campanhas
- **Conversões**: Total de conversões realizadas
- **ROAS Médio**: Retorno sobre investimento em ads

### Atualização Automática

Os dados são atualizados automaticamente a cada **30 segundos**.

---

## 🔌 APIs Disponíveis

### Análise de Landing Page

```http
POST /api/analyze-landing-page
Content-Type: application/json

{
  "url": "https://exemplo.com/produto"
}
```

**Resposta:**
```json
{
  "success": true,
  "title": "Nome do Produto",
  "price": "R$ 297,00",
  "benefits": ["Benefício 1", "Benefício 2"],
  "insights": "Análise da IA..."
}
```

### Espionagem de Concorrentes

```http
POST /api/competitor-spy
Content-Type: application/json

{
  "keyword": "marketing digital",
  "platform": "facebook"
}
```

**Resposta:**
```json
{
  "success": true,
  "ads": [
    {
      "headline": "Título do Anúncio",
      "description": "Descrição...",
      "score": 95
    }
  ]
}
```

### Geração de Copy

```http
POST /api/dco/generate-copy
Content-Type: application/json

{
  "url": "https://exemplo.com/produto",
  "objective": "conversions"
}
```

**Resposta:**
```json
{
  "success": true,
  "variants": [
    {
      "headline": "Título Gerado",
      "description": "Descrição persuasiva",
      "cta": "Comprar Agora",
      "score": 95
    }
  ]
}
```

### Simulação de Performance

```http
POST /api/ad/simulate
Content-Type: application/json

{
  "platform": "facebook",
  "budget": 1000,
  "duration": 30
}
```

**Resposta:**
```json
{
  "success": true,
  "ctr": 2.5,
  "cpc": 1.50,
  "impressions": 24000,
  "clicks": 600,
  "conversions": 18,
  "roas": 2.7
}
```

### Status de Créditos

```http
GET /api/credits/status
```

**Resposta:**
```json
{
  "success": true,
  "openai": {
    "status": "ok",
    "color": "green"
  },
  "manus": {
    "status": "integrated",
    "credits": "Ilimitado"
  },
  "overall_status": "ok"
}
```

---

## ⚠️ Tratamento de Erros

### Mensagens de Erro Comuns

| Código | Mensagem | Solução |
|--------|----------|---------|
| 400 | URL é obrigatória | Preencha o campo URL |
| 400 | Orçamento mínimo é R$ 50 | Aumente o orçamento |
| 400 | Duração mínima é 1 dia | Defina pelo menos 1 dia |
| 500 | Erro interno | Tente novamente ou contate suporte |

### Indicadores Visuais

- **Verde**: Sucesso / Funcionando
- **Amarelo**: Atenção / Créditos baixos
- **Vermelho**: Erro / Sem créditos

---

## 🧪 Testes

### Executar Testes Automatizados

```bash
cd /home/ubuntu/robo-otimizador
python3 -m pytest tests/test_generate_perfect_ad.py -v
```

### Cobertura de Testes

- Análise de Landing Page (3 testes)
- Espionagem de Concorrentes (3 testes)
- Geração de Copy (2 testes)
- Simulação de Ads (4 testes)
- APIs de Créditos (3 testes)
- Publicação de Ads (1 teste)
- Métricas do Dashboard (1 teste)
- Tratamento de Erros (2 testes)

**Total: 19 testes**

---

## 📞 Suporte

Para dúvidas ou problemas, acesse:
- Dashboard: `/dashboard`
- Chat com IA: `/operator-chat`
- Documentação: `/docs`

---

*Última atualização: 26 de Dezembro de 2025*

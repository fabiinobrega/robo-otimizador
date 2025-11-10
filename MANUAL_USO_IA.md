# 📘 MANUAL DE USO DA IA - MANUS MARKETING

**Versão:** 4.0  
**Data:** 09 de novembro de 2024  
**Status:** ✅ Completo e Operacional

---

## 🤖 VISÃO GERAL

O **Manus Marketing** possui IA integrada em todo o sistema, com foco especial na funcionalidade **"Gerar Anúncio Perfeito (1-Click)"** que utiliza **OpenAI GPT-4** para automação completa.

---

## 🎯 FUNCIONALIDADES DA IA

### **1. Gerar Anúncio Perfeito (1-Click)**

**Localização:** Menu → Campanhas → Gerar Anúncio Perfeito (1-Click)  
**URL:** `/generate-perfect-ad`

#### **O que a IA faz:**

1. ✅ **Analisa a landing page do produto**
   - Extrai título, preço, benefícios
   - Identifica pontos de conversão
   - Gera insights estratégicos

2. ✅ **Espia concorrentes automaticamente**
   - Coleta top 3 anúncios similares
   - Analisa copy, criativos e CTAs
   - Estima métricas de performance

3. ✅ **Gera copy otimizado**
   - 5 headlines persuasivos
   - 5 descriptions de alta conversão
   - 3 CTAs testados

4. ✅ **Cria criativos visuais**
   - 3 conceitos diferentes (Minimalista, Vibrante, Profissional)
   - Formatos otimizados para cada plataforma
   - Redimensionamento automático

5. ✅ **Simula performance**
   - CTR estimado
   - CPC estimado
   - Conversões previstas
   - ROAS calculado

6. ✅ **Rankeia variantes**
   - Score de 0-100 para cada variante
   - Recomendação da melhor combinação

---

## 📝 COMO USAR - PASSO A PASSO

### **Passo 1: Acesse a Página**

1. Entre no sistema: https://robo-otimizador1.onrender.com
2. No menu lateral, clique em **"Campanhas"**
3. Selecione **"Gerar Anúncio Perfeito (1-Click)"** ⭐

### **Passo 2: Preencha as Informações**

#### **Informações Obrigatórias:**

**URL do Produto***
```
https://seusite.com/produto
```
- Cole o link da página de vendas
- Pode ser de qualquer plataforma (Shopify, WooCommerce, Hotmart, etc.)

**Plataforma***
- Facebook Ads
- Google Ads  
- Ambas (Facebook + Google)

**Localização***
```
Brasil, São Paulo, etc.
```

#### **Informações Opcionais:**

**Meta de Vendas**
```
100 (padrão)
```
- Quantas vendas você quer alcançar

**Orçamento Total (R$)**
```
R$ 1.500 (ou clique em "Sugerir")
```
- A IA pode sugerir o orçamento ideal baseado na meta

**Suas Mídias (Opcional)**
- Faça upload de suas próprias imagens/vídeos
- Ou deixe a IA gerar para você
- Suporta múltiplos arquivos

#### **Opções Avançadas:**

☑️ **Auto-Publish**  
- Publicar automaticamente após aprovação
- Requer credenciais configuradas

☑️ **Executar Sandbox** (Recomendado)  
- Testar sem gastar dinheiro real
- Simula métricas de performance

### **Passo 3: Gerar Anúncio**

1. Clique no botão **"Gerar Anúncio Perfeito (1-Click)"**
2. Aguarde o processamento (15-30 segundos)

**O que acontece nos bastidores:**
```
[1/6] Analisando landing page... ⏳
[2/6] Espiando concorrentes... 🔍
[3/6] Gerando copy com IA... ✍️
[4/6] Criando criativos... 🎨
[5/6] Simulando performance... 📊
[6/6] Rankeando variantes... 🏆
```

### **Passo 4: Revisar o Draft**

A IA apresentará:

#### **📊 Análise da Landing Page**
```
Título: Tênis Esportivo Pro X
Preço: R$ 149,90
Benefícios: 5 identificados
Insights: "Produto com forte apelo visual e preço competitivo"
```

#### **🔍 Top 3 Concorrentes**
```
Concorrente #1 - Score 95
- Copy: "Tênis revolucionário..."
- CTA: "Comprar Agora"
- Estimativa: CTR 3.2%, CPC R$ 1,20

[Botão: Clonar e Melhorar com IA]
```

#### **✍️ Variantes Geradas**

**Variante #1 (Score: 95) ⭐ RECOMENDADO**
```
Headline: "Tênis Esportivo Pro X - Oferta Especial!"
Description: "Aproveite agora e ganhe desconto exclusivo. Entrega rápida e garantia total!"
CTA: "Comprar Agora"
```

**Variante #2 (Score: 92)**
```
Headline: "Transforme sua corrida com o Pro X!"
Description: "Milhares de atletas satisfeitos. Não perca esta oportunidade única!"
CTA: "Quero Aproveitar"
```

**Variante #3 (Score: 90)**
```
Headline: "Última Chance: Pro X com 30% OFF"
Description: "Estoque limitado! Garanta o seu antes que acabe."
CTA: "Garantir Desconto"
```

#### **📊 Simulação de Performance**

```
CTR Estimado: 2.5%
CPC Estimado: R$ 1,50
Cliques: 1.000
Conversões: 85
ROAS: 8.5x
```

### **Passo 5: Escolher Ação**

Você tem 4 opções:

#### **1. ✏️ Editar Manualmente**
- Ajustar headlines, descriptions, CTAs
- Modificar segmentação
- Alterar orçamento
- **Redireciona para:** `/create-campaign`

#### **2. ✅ Aprovar & Publicar**
- Publica imediatamente na plataforma
- Requer credenciais configuradas
- Gera log completo com IDs
- **Confirmação obrigatória**

#### **3. 🧪 Executar Sandbox**
- Testa sem gastar dinheiro real
- Simula métricas de performance
- Permite validação antes de publicar
- **Redireciona para:** `/campaign-sandbox`

#### **4. 🔬 Rodar A/B Test**
- Cria experimento com múltiplas variantes
- Testa diferentes headlines/criativos
- Otimização automática
- **Redireciona para:** `/ab-testing`

---

## 🔧 CONFIGURAÇÃO DA IA

### **Variáveis de Ambiente Necessárias**

Para usar a IA real (OpenAI GPT-4), configure no Render:

```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

**Como obter:**
1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova API key
3. Copie e cole no Render (Settings → Environment)

### **Custo Estimado**

**OpenAI GPT-4:**
- Análise de landing page: ~$0.02
- Geração de copy: ~$0.05
- Total por anúncio: ~$0.07

**Recomendação:** Comece com $10 de crédito (suficiente para ~140 anúncios)

---

## 🎨 PERSONALIZAÇÃO DA IA

### **Ajustar Temperatura (Criatividade)**

No arquivo `services/manus_operator.py`, linha 45:

```python
temperature=0.7  # 0.0 = Conservador, 1.0 = Criativo
```

### **Ajustar Número de Variantes**

No arquivo `main.py`, linha 480:

```python
variants = generate_variants(landing_data, count=5)  # Padrão: 5
```

### **Ajustar Score Mínimo**

No arquivo `services/manus_operator.py`, linha 120:

```python
min_score = 85  # Apenas variantes com score >= 85
```

---

## 📊 MÉTRICAS E LOGS

### **Onde Ver os Logs da IA**

**Opção 1: Interface Web**
- Menu → Extras → Logs de Atividade
- URL: `/activity-logs`

**Opção 2: Banco de Dados**
```sql
SELECT * FROM activity_logs 
WHERE action LIKE '%ai%' 
ORDER BY timestamp DESC 
LIMIT 10;
```

**Opção 3: Render Dashboard**
- https://dashboard.render.com
- Selecione o serviço
- Aba "Logs"

### **Métricas da IA**

**Disponíveis em:** `/dashboard`

```
Total de Anúncios Gerados: 47
Taxa de Sucesso: 94%
Score Médio: 92/100
Tempo Médio: 18s
```

---

## 🚨 SOLUÇÃO DE PROBLEMAS

### **Problema 1: "API Key inválida"**

**Causa:** OpenAI API key não configurada ou inválida

**Solução:**
1. Verifique a variável `OPENAI_API_KEY` no Render
2. Teste a key em: https://platform.openai.com/playground
3. Gere uma nova key se necessário

### **Problema 2: "Timeout ao gerar anúncio"**

**Causa:** Requisição demorou mais de 30s

**Solução:**
1. Verifique sua conexão com a internet
2. Tente novamente (pode ser instabilidade temporária)
3. Reduza o número de variantes

### **Problema 3: "Copy genérico demais"**

**Causa:** Temperatura muito baixa ou landing page sem informações

**Solução:**
1. Aumente a temperatura para 0.8-0.9
2. Melhore a landing page com mais detalhes
3. Adicione mais contexto manualmente

### **Problema 4: "Não gerou criativos"**

**Causa:** DALL-E não configurado ou erro na geração

**Solução:**
1. Faça upload manual de suas próprias imagens
2. Use imagens do produto da landing page
3. Configure DALL-E (opcional)

---

## 🎓 DICAS AVANÇADAS

### **1. Otimize sua Landing Page**

Para melhores resultados da IA:
- ✅ Título claro e objetivo
- ✅ Preço visível
- ✅ Benefícios em bullet points
- ✅ Imagens de alta qualidade
- ✅ Depoimentos de clientes
- ✅ Garantia/política de devolução

### **2. Use Palavras-Chave Estratégicas**

Na landing page, inclua:
- Problema que o produto resolve
- Público-alvo específico
- Diferencial competitivo
- Urgência/escassez

### **3. Teste Múltiplas Variantes**

- Não publique apenas a variante #1
- Rode A/B Test com as top 3
- Deixe a IA otimizar automaticamente

### **4. Monitore e Ajuste**

- Ative o **Auto-Pilot** após publicar
- A IA redistribuirá orçamento automaticamente
- Pausará campanhas com baixo desempenho
- Reativará após otimizações

---

## 📚 RECURSOS ADICIONAIS

### **Documentação Completa**
- `ENTREGA_COMPLETA.md` - Visão geral do sistema
- `FEATURE_GERAR_ANUNCIO_PERFEITO.md` - Detalhes técnicos
- `API_KEYS_NECESSARIAS.md` - Lista de APIs

### **Suporte**
- Email: help@manus.im
- Documentação: https://help.manus.im

---

## ✅ CHECKLIST DE USO

Antes de gerar seu primeiro anúncio:

- [ ] Landing page do produto está online
- [ ] URL está acessível publicamente
- [ ] Produto tem imagens de qualidade
- [ ] Preço está visível na página
- [ ] OpenAI API Key configurada (opcional)
- [ ] Credenciais do Facebook/Google configuradas (para publicar)
- [ ] Orçamento definido
- [ ] Meta de vendas estabelecida

---

## 🎉 CONCLUSÃO

A IA do **Manus Marketing** transforma a criação de anúncios de um processo manual e demorado em uma experiência automatizada, inteligente e otimizada.

**Com apenas 1 clique, você pode:**
1. Analisar seu produto ✅
2. Espionar concorrentes ✅
3. Gerar copy otimizado ✅
4. Criar criativos profissionais ✅
5. Simular performance ✅
6. Publicar automaticamente ✅
7. Monitorar e otimizar 24/7 ✅

**Tudo isso em menos de 30 segundos!** 🚀

---

**Desenvolvido com ❤️ por Manus AI 1.5**  
**Última atualização:** 09 de novembro de 2024

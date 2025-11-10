"""
Serviço de Integração com OpenAI GPT-4
Gera copy, headlines, descriptions e CTAs otimizados
"""

import os
import json
from openai import OpenAI

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ad_copy(product_info, platform="facebook", num_variants=5):
    """
    Gera variações de copy para anúncios
    
    Args:
        product_info (dict): Informações do produto (title, price, benefits, etc.)
        platform (str): Plataforma (facebook, google, both)
        num_variants (int): Número de variantes a gerar
    
    Returns:
        dict: Variantes geradas com headlines, descriptions e CTAs
    """
    
    # Se não tiver API key, retorna simulado
    if not os.getenv("OPENAI_API_KEY"):
        return _generate_mock_copy(product_info, num_variants)
    
    try:
        prompt = f"""
Você é um especialista em copywriting para anúncios digitais.

PRODUTO:
- Título: {product_info.get('title', 'Produto')}
- Preço: R$ {product_info.get('price', '0.00')}
- Benefícios: {', '.join(product_info.get('benefits', []))}
- Descrição: {product_info.get('description', '')}

PLATAFORMA: {platform.upper()}

TAREFA:
Crie {num_variants} variações de anúncio otimizadas para conversão.

Para cada variante, forneça:
1. HEADLINE (máx. 40 caracteres) - Chamativo e direto
2. DESCRIPTION (máx. 125 caracteres) - Persuasiva e com benefício claro
3. CTA (máx. 20 caracteres) - Ação clara
4. SCORE (0-100) - Probabilidade de conversão

FORMATO DE RESPOSTA (JSON):
{{
  "variants": [
    {{
      "headline": "...",
      "description": "...",
      "cta": "...",
      "score": 95,
      "reasoning": "Por que esta variante funciona"
    }}
  ]
}}

IMPORTANTE:
- Use gatilhos mentais (escassez, urgência, prova social)
- Foque em benefícios, não características
- Seja específico com números
- Use emojis estrategicamente (máx. 2 por texto)
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em copywriting para anúncios digitais com 10 anos de experiência."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Ordenar por score
        result['variants'] = sorted(result['variants'], key=lambda x: x.get('score', 0), reverse=True)
        
        return result
        
    except Exception as e:
        print(f"Erro ao gerar copy com OpenAI: {e}")
        return _generate_mock_copy(product_info, num_variants)


def analyze_landing_page(url, html_content=None):
    """
    Analisa uma landing page e extrai informações relevantes
    
    Args:
        url (str): URL da landing page
        html_content (str): Conteúdo HTML (opcional)
    
    Returns:
        dict: Análise da página
    """
    
    if not os.getenv("OPENAI_API_KEY"):
        return _generate_mock_analysis(url)
    
    try:
        prompt = f"""
Analise esta landing page de produto: {url}

TAREFA:
1. Identifique o produto principal
2. Extraia o preço (se visível)
3. Liste os principais benefícios
4. Identifique o público-alvo
5. Avalie a qualidade da página (0-100)
6. Sugira melhorias

FORMATO DE RESPOSTA (JSON):
{{
  "product": {{
    "title": "...",
    "price": "...",
    "category": "...",
    "target_audience": "..."
  }},
  "benefits": ["...", "...", "..."],
  "quality_score": 85,
  "insights": [
    "Insight 1",
    "Insight 2"
  ],
  "suggestions": [
    "Sugestão 1",
    "Sugestão 2"
  ]
}}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de landing pages e otimização de conversão."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Erro ao analisar landing page: {e}")
        return _generate_mock_analysis(url)


def generate_targeting_suggestions(product_info, platform="facebook"):
    """
    Gera sugestões de segmentação baseadas no produto
    
    Args:
        product_info (dict): Informações do produto
        platform (str): Plataforma
    
    Returns:
        dict: Sugestões de segmentação
    """
    
    if not os.getenv("OPENAI_API_KEY"):
        return _generate_mock_targeting()
    
    try:
        prompt = f"""
Produto: {product_info.get('title', 'Produto')}
Categoria: {product_info.get('category', 'Geral')}
Preço: R$ {product_info.get('price', '0.00')}

Sugira a segmentação ideal para {platform.upper()}:

FORMATO (JSON):
{{
  "demographics": {{
    "age_range": "18-65",
    "gender": "all",
    "locations": ["Brasil", "São Paulo"]
  }},
  "interests": ["...", "...", "..."],
  "behaviors": ["...", "..."],
  "custom_audiences": ["...", "..."],
  "lookalike": {{
    "source": "...",
    "percentage": 1
  }}
}}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em segmentação de anúncios digitais."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Erro ao gerar segmentação: {e}")
        return _generate_mock_targeting()


def optimize_campaign_budget(campaign_data):
    """
    Otimiza distribuição de orçamento entre campanhas
    
    Args:
        campaign_data (list): Lista de campanhas com métricas
    
    Returns:
        dict: Recomendações de redistribuição
    """
    
    if not os.getenv("OPENAI_API_KEY"):
        return {"recommendations": [], "total_savings": 0}
    
    try:
        prompt = f"""
Analise estas campanhas e sugira redistribuição de orçamento:

{json.dumps(campaign_data, indent=2)}

Considere:
- ROAS de cada campanha
- CTR e CPC
- Tendências de performance
- Sazonalidade

FORMATO (JSON):
{{
  "recommendations": [
    {{
      "campaign_id": 1,
      "current_budget": 1000,
      "suggested_budget": 1500,
      "reasoning": "..."
    }}
  ],
  "total_savings": 500,
  "expected_roas_improvement": "15%"
}}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em otimização de orçamento de anúncios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Erro ao otimizar orçamento: {e}")
        return {"recommendations": [], "total_savings": 0}


# ===== FUNÇÕES MOCK (FALLBACK) =====

def _generate_mock_copy(product_info, num_variants=5):
    """Gera copy simulado quando não há API key"""
    
    title = product_info.get('title', 'Produto Incrível')
    price = product_info.get('price', '99.90')
    
    variants = [
        {
            "headline": f"{title} - Oferta Especial! 🔥",
            "description": "Aproveite agora e ganhe desconto exclusivo. Entrega rápida e garantia total!",
            "cta": "Comprar Agora",
            "score": 95,
            "reasoning": "Usa urgência e benefícios claros"
        },
        {
            "headline": f"Transforme sua vida com {title}! ✨",
            "description": "Milhares de clientes satisfeitos. Não perca esta oportunidade única!",
            "cta": "Quero Aproveitar",
            "score": 92,
            "reasoning": "Apelo emocional + prova social"
        },
        {
            "headline": f"Última Chance: {title} com 30% OFF",
            "description": "Estoque limitado! Garanta o seu antes que acabe.",
            "cta": "Garantir Desconto",
            "score": 90,
            "reasoning": "Escassez + desconto"
        },
        {
            "headline": f"{title} por apenas R$ {price}",
            "description": "Qualidade premium, preço acessível. Parcele em até 12x sem juros!",
            "cta": "Ver Oferta",
            "score": 88,
            "reasoning": "Foco no preço + parcelamento"
        },
        {
            "headline": f"Descubra o {title} que todos querem",
            "description": "Produto mais vendido do mês! Entrega grátis para todo o Brasil.",
            "cta": "Comprar",
            "score": 85,
            "reasoning": "Prova social + benefício de entrega"
        }
    ]
    
    return {"variants": variants[:num_variants]}


def _generate_mock_analysis(url):
    """Gera análise simulada"""
    
    return {
        "product": {
            "title": "Produto Extraído da URL",
            "price": "149.90",
            "category": "E-commerce",
            "target_audience": "Público geral 25-45 anos"
        },
        "benefits": [
            "Alta qualidade",
            "Entrega rápida",
            "Garantia de 30 dias",
            "Suporte 24/7"
        ],
        "quality_score": 85,
        "insights": [
            "Página tem bom apelo visual",
            "Preço competitivo para o mercado",
            "Faltam depoimentos de clientes"
        ],
        "suggestions": [
            "Adicionar mais provas sociais",
            "Incluir vídeo demonstrativo",
            "Melhorar CTA acima da dobra"
        ]
    }


def _generate_mock_targeting():
    """Gera segmentação simulada"""
    
    return {
        "demographics": {
            "age_range": "25-54",
            "gender": "all",
            "locations": ["Brasil", "São Paulo", "Rio de Janeiro"]
        },
        "interests": [
            "Compras online",
            "Tecnologia",
            "Lifestyle"
        ],
        "behaviors": [
            "Compradores online frequentes",
            "Engajados com e-commerce"
        ],
        "custom_audiences": [
            "Visitantes do site (últimos 30 dias)",
            "Clientes existentes"
        ],
        "lookalike": {
            "source": "Compradores",
            "percentage": 1
        }
    }

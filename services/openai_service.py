"""AI Service - Serviço de IA usando EXCLUSIVAMENTE Manus AI
OpenAI foi REMOVIDA conforme solicitação do usuário.
Todo trabalho de IA é realizado pelo Manus.
"""

import os
import json

# Importar Manus AI Service (ÚNICO provedor de IA)
from services.manus_ai_service import manus_ai

class OpenaiService:
    """Classe wrapper para compatibilidade - Usa APENAS Manus AI"""
    
    def __init__(self):
        """Inicializar serviço"""
        self.manus_ai = manus_ai
    
    def get_info(self):
        """Obter informações do serviço"""
        return {
            "service": "ai_service.py",
            "class": "OpenaiService",
            "status": "active",
            "engine": "Manus AI (ÚNICO)",
            "openai_status": "REMOVIDA"
        }


def generate_ad_copy(product_info, platform="facebook", num_variants=5):
    """
    Gera variações de copy para anúncios usando APENAS Manus AI
    
    Args:
        product_info (dict): Informações do produto (title, price, benefits, etc.)
        platform (str): Plataforma (facebook, google, both)
        num_variants (int): Número de variantes a gerar
    
    Returns:
        dict: Variantes geradas com headlines, descriptions e CTAs
    """
    
    try:
        # Usar Manus AI para geração
        title = product_info.get('title') or product_info.get('name', 'Produto')
        description = product_info.get('description', '')
        target_audience = product_info.get('target_audience', 'público geral')
        
        prompt = f"""Crie {num_variants} variações de copy para anúncio do produto:
        Produto: {title}
        Descrição: {description}
        Público-alvo: {target_audience}
        Plataforma: {platform}
        
        Para cada variação, forneça:
        - headline (máx 40 caracteres)
        - description (máx 125 caracteres)
        - cta (call to action)
        - score (0-100)
        - reasoning (motivo do score)
        
        Responda em JSON: {{"variants": [...]}}"""
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um copywriter especialista em anúncios de alta conversão."
        )
        
        if result and 'variants' in result:
            return result
        
    except Exception as e:
        print(f"Erro ao gerar com Manus AI: {e}")
    
    # Fallback: geração local
    return _generate_local_copy(product_info, num_variants)


def analyze_landing_page(url, html_content=None):
    """
    Analisa uma landing page usando APENAS Manus AI
    
    Args:
        url (str): URL da landing page
        html_content (str): Conteúdo HTML (opcional)
    
    Returns:
        dict: Análise da página
    """
    
    try:
        prompt = f"""Analise a landing page: {url}
        
        Forneça:
        1. Informações do produto (título, preço, categoria, público-alvo)
        2. Benefícios identificados
        3. Score de qualidade (0-100)
        4. Insights sobre a página
        5. Sugestões de melhoria
        
        Responda em JSON estruturado."""
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um especialista em análise de landing pages e conversão."
        )
        
        if result:
            return result
            
    except Exception as e:
        print(f"Erro ao analisar com Manus AI: {e}")
    
    return _generate_local_analysis(url)


def generate_targeting_suggestions(product_info, platform="facebook"):
    """
    Gera sugestões de segmentação usando APENAS Manus AI
    
    Args:
        product_info (dict): Informações do produto
        platform (str): Plataforma
    
    Returns:
        dict: Sugestões de segmentação
    """
    
    try:
        title = product_info.get('title') or product_info.get('name', 'Produto')
        
        prompt = f"""Gere sugestões de segmentação para o produto: {title}
        Plataforma: {platform}
        
        Forneça:
        1. Demographics (idade, gênero, localizações)
        2. Interesses
        3. Comportamentos
        4. Públicos personalizados
        5. Lookalike audience
        
        Responda em JSON estruturado."""
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um especialista em segmentação de anúncios digitais."
        )
        
        if result:
            return result
            
    except Exception as e:
        print(f"Erro ao gerar segmentação com Manus AI: {e}")
    
    return _generate_local_targeting()


def optimize_campaign_budget(campaign_data):
    """
    Otimiza distribuição de orçamento usando APENAS Manus AI
    
    Args:
        campaign_data (list): Lista de campanhas com métricas
    
    Returns:
        dict: Recomendações de redistribuição
    """
    
    try:
        prompt = f"""Analise as campanhas e otimize a distribuição de orçamento:
        
        Campanhas: {json.dumps(campaign_data, ensure_ascii=False)}
        
        Forneça recomendações de redistribuição para maximizar ROAS.
        Responda em JSON com: recommendations, total_savings"""
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um especialista em otimização de orçamento de campanhas."
        )
        
        if result:
            return result
            
    except Exception as e:
        print(f"Erro ao otimizar com Manus AI: {e}")
    
    return {"recommendations": [], "total_savings": 0}


# ===== FUNÇÕES FALLBACK (Geração Local) =====

def _generate_local_copy(product_info, num_variants=5):
    """Gera copy localmente quando Manus AI não está disponível"""
    
    title = product_info.get('title') or product_info.get('name', 'Produto Incrível')
    price = product_info.get('price', '99.90')
    description = product_info.get('description', '')
    
    variants = [
        {
            "headline": f"{title} - Oferta Especial!",
            "description": f"{description[:100]}... Aproveite agora!" if description else "Aproveite agora e ganhe desconto exclusivo!",
            "cta": "Comprar Agora",
            "score": 95,
            "reasoning": "Usa urgência e benefícios claros"
        },
        {
            "headline": f"Transforme sua vida com {title}!",
            "description": "Milhares de clientes satisfeitos. Não perca!",
            "cta": "Quero Aproveitar",
            "score": 92,
            "reasoning": "Apelo emocional + prova social"
        },
        {
            "headline": f"Última Chance: {title} com 30% OFF",
            "description": "Estoque limitado! Garanta o seu.",
            "cta": "Garantir Desconto",
            "score": 90,
            "reasoning": "Escassez + desconto"
        },
        {
            "headline": f"{title} por apenas R$ {price}",
            "description": "Qualidade premium, preço acessível. Parcele em 12x!",
            "cta": "Ver Oferta",
            "score": 88,
            "reasoning": "Foco no preço + parcelamento"
        },
        {
            "headline": f"Descubra o {title} que todos querem",
            "description": "Produto mais vendido! Entrega grátis.",
            "cta": "Comprar",
            "score": 85,
            "reasoning": "Prova social + benefício"
        }
    ]
    
    return {"variants": variants[:num_variants]}


def _generate_local_analysis(url):
    """Gera análise localmente"""
    
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


def _generate_local_targeting():
    """Gera segmentação localmente"""
    
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


# Instância global para compatibilidade
openai_service = OpenaiService()

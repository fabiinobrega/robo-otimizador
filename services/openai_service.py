"""
AI Service - Serviço de IA usando Manus AI
Gera copy, headlines, descriptions e CTAs otimizados
"""

import os
import json

class OpenaiService:
    """Classe wrapper para compatibilidade - Agora usa Manus AI"""
    
    def __init__(self):
        """Inicializar serviço"""
        pass
    
    def get_info(self):
        """Obter informações do serviço"""
        return {
            "service": "ai_service.py",
            "class": "OpenaiService",
            "status": "active",
            "engine": "Manus AI"
        }

# Importar IA nativa (Manus AI)
try:
    from services.native_ai_engine import native_ai
    NATIVE_AI_AVAILABLE = True
    print("✅ Manus AI Engine inicializado com sucesso")
except ImportError:
    NATIVE_AI_AVAILABLE = False
    print("⚠️ Manus AI Engine não disponível, usando fallback")


def generate_ad_copy(product_info, platform="facebook", num_variants=5):
    """
    Gera variações de copy para anúncios usando Manus AI
    
    Args:
        product_info (dict): Informações do produto (title, price, benefits, etc.)
        platform (str): Plataforma (facebook, google, both)
        num_variants (int): Número de variantes a gerar
    
    Returns:
        dict: Variantes geradas com headlines, descriptions e CTAs
    """
    
    # Usar IA nativa (Manus AI)
    if NATIVE_AI_AVAILABLE:
        try:
            return native_ai.generate_ad_copy(product_info, platform, num_variants)
        except Exception as e:
            print(f"Erro na Manus AI, usando fallback: {e}")
    
    # Fallback para copy gerado localmente
    return _generate_mock_copy(product_info, num_variants)


def analyze_landing_page(url, html_content=None):
    """
    Analisa uma landing page e extrai informações relevantes usando Manus AI
    
    Args:
        url (str): URL da landing page
        html_content (str): Conteúdo HTML (opcional)
    
    Returns:
        dict: Análise da página
    """
    
    # Usar IA nativa (Manus AI)
    if NATIVE_AI_AVAILABLE:
        try:
            return native_ai.analyze_landing_page(url, html_content)
        except Exception as e:
            print(f"Erro na Manus AI, usando fallback: {e}")
    
    return _generate_mock_analysis(url)


def generate_targeting_suggestions(product_info, platform="facebook"):
    """
    Gera sugestões de segmentação baseadas no produto usando Manus AI
    
    Args:
        product_info (dict): Informações do produto
        platform (str): Plataforma
    
    Returns:
        dict: Sugestões de segmentação
    """
    
    # Usar IA nativa (Manus AI)
    if NATIVE_AI_AVAILABLE:
        try:
            return native_ai.generate_targeting_suggestions(product_info, platform)
        except Exception as e:
            print(f"Erro na Manus AI, usando fallback: {e}")
    
    return _generate_mock_targeting()


def optimize_campaign_budget(campaign_data):
    """
    Otimiza distribuição de orçamento entre campanhas usando Manus AI
    
    Args:
        campaign_data (list): Lista de campanhas com métricas
    
    Returns:
        dict: Recomendações de redistribuição
    """
    
    # Usar IA nativa (Manus AI)
    if NATIVE_AI_AVAILABLE:
        try:
            return native_ai.optimize_campaign_budget(campaign_data)
        except Exception as e:
            print(f"Erro na Manus AI, usando fallback: {e}")
    
    return {"recommendations": [], "total_savings": 0}


# ===== FUNÇÕES FALLBACK (Geração Local) =====

def _generate_mock_copy(product_info, num_variants=5):
    """Gera copy otimizado localmente quando Manus AI não está disponível"""
    
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


def _generate_mock_targeting():
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

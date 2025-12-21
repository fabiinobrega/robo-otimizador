"""
Strategic Brain - Cérebro Estratégico
Usa Manus AI para PENSAR: estratégia, copywriting, criativos
NÃO executa nada técnico
Atualizado: 21/12/2024 - Migrado para Manus AI Service
"""

import os
import json
import logging
from datetime import datetime

# Importar Manus AI Service (substitui OpenAI)
from services.manus_ai_service import manus_ai

logger = logging.getLogger(__name__)


class OpenAIStrategicBrain:
    """
    Cérebro estratégico que usa Manus AI para pensar
    Não executa nada técnico - isso é trabalho do executor
    """
    
    def __init__(self):
        pass
    
    def create_campaign_strategy(self, spy_report, product, objective, total_budget, duration_days):
        """
        Cria estratégia de campanha baseada na espionagem
        
        Args:
            spy_report (dict): Relatório de espionagem
            product (str): Produto/serviço
            objective (str): Objetivo de vendas
            total_budget (float): Orçamento total
            duration_days (int): Duração em dias
            
        Returns:
            dict: Estratégia completa
        """
        daily_budget = total_budget / duration_days
        
        prompt = f"""
        Você é um estrategista de marketing digital de elite.
        
        Baseado neste relatório de espionagem de concorrência:
        {json.dumps(spy_report, indent=2)}
        
        Crie uma ESTRATÉGIA COMPLETA de campanha para:
        - Produto: {product}
        - Objetivo: {objective}
        - Orçamento Total: R$ {total_budget:.2f}
        - Duração: {duration_days} dias
        - Orçamento Diário: R$ {daily_budget:.2f}
        
        A estratégia deve incluir:
        
        1. POSICIONAMENTO
           - USP (Unique Selling Proposition)
           - Diferenciação dos concorrentes
           - Tom de comunicação
        
        2. PÚBLICO-ALVO
           - Persona primária
           - Persona secundária
           - Interesses para segmentação
           - Comportamentos
        
        3. ESTRUTURA DE CAMPANHA
           - Número de conjuntos de anúncios
           - Distribuição de orçamento
           - Objetivos por conjunto
        
        4. CRONOGRAMA
           - Fase de teste (dias 1-7)
           - Fase de otimização (dias 8-14)
           - Fase de escala (dias 15+)
        
        5. KPIs E METAS
           - CPA alvo
           - ROAS esperado
           - CTR mínimo
           - Conversões esperadas
        
        Retorne em formato JSON estruturado.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um estrategista de marketing digital com 15 anos de experiência em campanhas de alta performance.",
            temperature=0.6
        )
        
        if result:
            result["created_at"] = datetime.now().isoformat()
            return result
        
        return self._get_fallback_strategy(product, objective, total_budget, duration_days)
    
    def _get_fallback_strategy(self, product, objective, total_budget, duration_days):
        """Estratégia básica quando IA não está disponível"""
        daily_budget = total_budget / duration_days
        
        return {
            "positioning": {
                "usp": f"A melhor solução em {product}",
                "differentiation": "Qualidade premium com preço justo",
                "tone": "Profissional e confiável"
            },
            "target_audience": {
                "primary_persona": {
                    "age": "25-45",
                    "interests": ["tecnologia", "inovação", "qualidade"],
                    "behaviors": ["compradores online", "pesquisadores"]
                },
                "secondary_persona": {
                    "age": "35-55",
                    "interests": ["negócios", "eficiência"],
                    "behaviors": ["decisores", "B2B"]
                }
            },
            "campaign_structure": {
                "ad_sets": 3,
                "budget_distribution": {
                    "prospecting": 0.5,
                    "retargeting": 0.3,
                    "lookalike": 0.2
                }
            },
            "schedule": {
                "testing": {"days": "1-7", "budget_pct": 0.3},
                "optimization": {"days": "8-14", "budget_pct": 0.3},
                "scaling": {"days": "15+", "budget_pct": 0.4}
            },
            "kpis": {
                "target_cpa": daily_budget * 0.5,
                "expected_roas": 3.0,
                "min_ctr": 1.5,
                "expected_conversions": int(total_budget / (daily_budget * 0.5))
            },
            "created_at": datetime.now().isoformat()
        }
    
    def generate_ad_copies(self, strategy, platform='facebook'):
        """
        Gera copies de anúncio baseados na estratégia
        
        Args:
            strategy (dict): Estratégia de campanha
            platform (str): Plataforma de anúncios
            
        Returns:
            dict: Copies gerados
        """
        prompt = f"""
        Baseado nesta estratégia de campanha:
        {json.dumps(strategy, indent=2)}
        
        Crie 5 variações de anúncio para {platform} usando diferentes modelos:
        
        1. AIDA (Attention, Interest, Desire, Action)
        2. PAS (Problem, Agitate, Solution)
        3. BAB (Before, After, Bridge)
        4. 4Ps (Promise, Picture, Proof, Push)
        5. QUEST (Qualify, Understand, Educate, Stimulate, Transition)
        
        Para cada variação, forneça:
        - Headline (máx 40 caracteres)
        - Primary Text (máx 125 caracteres)
        - Description (máx 90 caracteres)
        - CTA
        
        Retorne em formato JSON.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um copywriter especialista em anúncios de alta conversão.",
            temperature=0.8
        )
        
        if result:
            return result
        
        return {
            "variations": [
                {
                    "model": "AIDA",
                    "headline": "Transforme Seu Negócio",
                    "primary_text": "Descubra como milhares já alcançaram resultados incríveis.",
                    "description": "Comece agora e veja a diferença.",
                    "cta": "Saiba Mais"
                },
                {
                    "model": "PAS",
                    "headline": "Cansado de Perder Tempo?",
                    "primary_text": "Pare de desperdiçar recursos. Nossa solução resolve isso.",
                    "description": "Resultados garantidos em 30 dias.",
                    "cta": "Resolver Agora"
                },
                {
                    "model": "BAB",
                    "headline": "Antes vs Depois",
                    "primary_text": "Veja a transformação que nossos clientes experimentaram.",
                    "description": "Sua vez de mudar.",
                    "cta": "Ver Resultados"
                }
            ]
        }
    
    def analyze_campaign_performance(self, metrics):
        """
        Analisa métricas de campanha e sugere otimizações
        
        Args:
            metrics (dict): Métricas da campanha
            
        Returns:
            dict: Análise e recomendações
        """
        prompt = f"""
        Analise estas métricas de campanha e forneça insights:
        
        MÉTRICAS:
        {json.dumps(metrics, indent=2)}
        
        Forneça:
        1. Diagnóstico geral (bom/regular/ruim)
        2. Pontos fortes identificados
        3. Pontos fracos identificados
        4. Recomendações de otimização (mínimo 5)
        5. Previsão de melhoria com cada otimização
        6. Priorização das ações
        
        Retorne em formato JSON.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um analista de performance de campanhas digitais.",
            temperature=0.4
        )
        
        if result:
            return result
        
        return {
            "diagnosis": "regular",
            "strengths": ["CTR acima da média", "Custo por clique controlado"],
            "weaknesses": ["Taxa de conversão baixa", "ROAS abaixo do esperado"],
            "recommendations": [
                {"action": "Melhorar landing page", "expected_impact": "+20% conversão"},
                {"action": "Testar novos criativos", "expected_impact": "+15% CTR"},
                {"action": "Refinar segmentação", "expected_impact": "-10% CPA"},
                {"action": "Ajustar lances", "expected_impact": "+10% impressões"},
                {"action": "Adicionar extensões", "expected_impact": "+5% CTR"}
            ],
            "priority": ["landing page", "criativos", "segmentação"]
        }


# Instância global
strategic_brain = OpenAIStrategicBrain()

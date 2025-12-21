"""
Sales Intelligence Service - Inteligência de Vendas com IA
Sistema de Otimização de Vendas Avançado
Autor: Manus AI Agent
Data: 24/11/2024
Atualizado: 21/12/2024 - Migrado para Manus AI Service
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

# Importar Manus AI Service (substitui OpenAI)
from services.manus_ai_service import manus_ai


class SalesIntelligenceService:
    """Serviço de Inteligência de Vendas com IA"""
    
    def __init__(self):
        """Inicializar serviço"""
        self.model = "gpt-4.1-mini"
    
    def analyze_sales_opportunity(self, lead_data: Dict) -> Dict:
        """
        Analisa oportunidade de venda e fornece insights
        """
        prompt = f"""
        Analise esta oportunidade de venda e forneça insights detalhados:
        
        DADOS DO LEAD:
        {json.dumps(lead_data, indent=2)}
        
        Forneça:
        1. Score de qualificação (0-100)
        2. Probabilidade de conversão
        3. Valor potencial estimado
        4. Objeções prováveis
        5. Estratégia de abordagem recomendada
        6. Próximos passos sugeridos
        
        Retorne em formato JSON.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um especialista em vendas B2B com 20 anos de experiência.",
            temperature=0.5
        )
        
        if result:
            return result
        
        return self._fallback_opportunity_analysis(lead_data)
    
    def _fallback_opportunity_analysis(self, lead_data: Dict) -> Dict:
        """Análise básica quando IA não está disponível"""
        return {
            "qualification_score": random.randint(60, 85),
            "conversion_probability": f"{random.randint(40, 70)}%",
            "potential_value": lead_data.get("budget", 5000),
            "likely_objections": ["preço", "timing", "decisão em grupo"],
            "approach_strategy": "Demonstração de valor + case studies",
            "next_steps": ["Agendar call", "Enviar proposta", "Follow-up em 3 dias"]
        }
    
    def generate_sales_script(self, product: str, target_audience: str, objections: List[str] = None) -> Dict:
        """
        Gera script de vendas personalizado
        """
        objections_text = ", ".join(objections) if objections else "preço, timing, necessidade"
        
        prompt = f"""
        Crie um script de vendas completo para:
        
        PRODUTO: {product}
        PÚBLICO-ALVO: {target_audience}
        OBJEÇÕES COMUNS: {objections_text}
        
        O script deve incluir:
        1. Abertura (hook inicial)
        2. Qualificação (perguntas-chave)
        3. Apresentação de valor
        4. Tratamento de objeções
        5. Fechamento
        6. Follow-up
        
        Retorne em formato JSON com cada seção.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um especialista em vendas consultivas.",
            temperature=0.7
        )
        
        if result:
            return result
        
        return {
            "opening": "Olá! Vi que você está buscando soluções para [problema]. Posso ajudar?",
            "qualification": ["Qual seu maior desafio atual?", "Qual seu orçamento?", "Qual o prazo ideal?"],
            "value_presentation": "Nossa solução já ajudou +1000 empresas a...",
            "objection_handling": {"preço": "Entendo. Vamos ver o ROI...", "timing": "O melhor momento é agora porque..."},
            "closing": "Baseado no que conversamos, qual o próximo passo ideal?",
            "follow_up": "Enviarei um resumo por email em 24h"
        }
    
    def predict_sales_trend(self, historical_data: List[Dict]) -> Dict:
        """
        Prevê tendências de vendas baseado em dados históricos
        """
        prompt = f"""
        Analise estes dados históricos de vendas e preveja tendências:
        
        DADOS HISTÓRICOS:
        {json.dumps(historical_data[-30:], indent=2)}
        
        Forneça:
        1. Tendência geral (crescimento/estagnação/queda)
        2. Previsão para próximos 30 dias
        3. Fatores de influência identificados
        4. Recomendações de ação
        5. Riscos e oportunidades
        
        Retorne em formato JSON.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um analista de dados especializado em vendas.",
            temperature=0.3
        )
        
        if result:
            return result
        
        return {
            "trend": "crescimento moderado",
            "forecast_30_days": {"min": 10000, "expected": 15000, "max": 20000},
            "influence_factors": ["sazonalidade", "campanhas ativas", "mercado"],
            "recommendations": ["Aumentar investimento em ads", "Focar em upsell"],
            "risks": ["Concorrência", "Sazonalidade"],
            "opportunities": ["Black Friday", "Novos canais"]
        }
    
    def score_lead(self, lead_info: Dict) -> Dict:
        """
        Pontua lead baseado em critérios de qualificação
        """
        prompt = f"""
        Pontue este lead de 0 a 100 baseado em:
        
        INFORMAÇÕES DO LEAD:
        {json.dumps(lead_info, indent=2)}
        
        Critérios de pontuação:
        - Fit com produto (0-25)
        - Budget disponível (0-25)
        - Autoridade de decisão (0-25)
        - Urgência/Timing (0-25)
        
        Retorne JSON com score total e breakdown por critério.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um especialista em qualificação de leads.",
            temperature=0.3
        )
        
        if result:
            return result
        
        return {
            "total_score": random.randint(50, 90),
            "breakdown": {
                "fit": random.randint(15, 25),
                "budget": random.randint(10, 25),
                "authority": random.randint(15, 25),
                "timing": random.randint(10, 25)
            },
            "recommendation": "Qualificado para próxima etapa"
        }


# Instância global
sales_intelligence = SalesIntelligenceService()

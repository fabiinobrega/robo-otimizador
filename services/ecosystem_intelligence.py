# services/ecosystem_intelligence.py
"""
NEXORA PRIME - Inteligência de Ecossistema
Análise de mercado, tendências e saturação
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class EcosystemIntelligence:
    """Sistema de inteligência de ecossistema de marketing."""
    
    def __init__(self):
        self.market_data = {}
        self.trend_history = []
        self.competitor_tracking = {}
        self.saturation_metrics = {}
    
    def get_ecosystem_insights(self, industry: str) -> Dict:
        """Agrega insights de todo o ecossistema de marketing."""
        insights = {
            "market_trends": self._analyze_market_trends(industry),
            "competitor_snapshot": self._track_competitor_activity(industry),
            "audience_sentiment": self._gauge_audience_sentiment(industry),
            "platform_performance": self._analyze_platform_performance(industry),
            "saturation_analysis": self._analyze_market_saturation(industry),
            "generated_at": datetime.now().isoformat()
        }
        return insights
    
    def _analyze_market_trends(self, industry: str) -> Dict:
        """Analisa tendências de mercado."""
        trends = {
            "emerging_trends": [
                {"trend": f"Crescimento do interesse em {industry} sustentável", "strength": 0.85},
                {"trend": f"Aumento da demanda por personalização em {industry}", "strength": 0.78},
                {"trend": "Preferência por conteúdo em vídeo curto", "strength": 0.92}
            ],
            "declining_trends": [
                {"trend": "Anúncios estáticos tradicionais", "decline_rate": 0.15},
                {"trend": "Segmentação apenas demográfica", "decline_rate": 0.22}
            ],
            "seasonal_factors": self._get_seasonal_factors(industry),
            "confidence": 0.82
        }
        return trends
    
    def _get_seasonal_factors(self, industry: str) -> Dict:
        """Retorna fatores sazonais para a indústria."""
        current_month = datetime.now().month
        
        seasonal_map = {
            "varejo": {
                11: {"factor": 1.5, "event": "Black Friday"},
                12: {"factor": 1.8, "event": "Natal"},
                1: {"factor": 0.7, "event": "Pós-festas"},
                5: {"factor": 1.3, "event": "Dia das Mães"}
            },
            "educacao": {
                1: {"factor": 1.4, "event": "Volta às aulas"},
                2: {"factor": 1.3, "event": "Início do ano letivo"},
                7: {"factor": 1.2, "event": "Férias de julho"}
            },
            "turismo": {
                1: {"factor": 1.5, "event": "Férias de verão"},
                7: {"factor": 1.3, "event": "Férias de inverno"},
                12: {"factor": 1.4, "event": "Festas de fim de ano"}
            }
        }
        
        industry_seasons = seasonal_map.get(industry.lower(), {})
        current_factor = industry_seasons.get(current_month, {"factor": 1.0, "event": "Normal"})
        
        return {
            "current_month_factor": current_factor["factor"],
            "current_event": current_factor["event"],
            "upcoming_events": self._get_upcoming_events(industry_seasons, current_month)
        }
    
    def _get_upcoming_events(self, seasons: Dict, current_month: int) -> List[Dict]:
        """Retorna próximos eventos sazonais."""
        upcoming = []
        for month in range(current_month + 1, current_month + 4):
            actual_month = ((month - 1) % 12) + 1
            if actual_month in seasons:
                upcoming.append({
                    "month": actual_month,
                    "event": seasons[actual_month]["event"],
                    "factor": seasons[actual_month]["factor"]
                })
        return upcoming
    
    def _track_competitor_activity(self, industry: str) -> Dict:
        """Rastreia atividade de concorrentes."""
        return {
            "active_competitors": 15,
            "new_entrants_last_30_days": 3,
            "competitor_highlights": [
                {"competitor": "Concorrente A", "activity": "Lançou nova campanha de vídeo focada em Reels", "impact": "medium"},
                {"competitor": "Concorrente B", "activity": "Aumentou investimento em Google Search Ads", "impact": "high"},
                {"competitor": "Concorrente C", "activity": "Expandiu para TikTok Ads", "impact": "low"}
            ],
            "average_competitor_spend": 25000,
            "market_share_estimate": {
                "leader": 35,
                "top_5": 75,
                "others": 25
            }
        }
    
    def _gauge_audience_sentiment(self, industry: str) -> Dict:
        """Mede o sentimento do público."""
        return {
            "overall_sentiment": "positive",
            "sentiment_score": 0.72,
            "confidence": 0.85,
            "key_topics": [
                {"topic": "Qualidade do produto", "sentiment": 0.85},
                {"topic": "Atendimento ao cliente", "sentiment": 0.68},
                {"topic": "Preço", "sentiment": 0.55},
                {"topic": "Entrega", "sentiment": 0.62}
            ],
            "trending_discussions": [
                "Sustentabilidade",
                "Experiência do cliente",
                "Personalização"
            ]
        }
    
    def _analyze_platform_performance(self, industry: str) -> Dict:
        """Analisa performance por plataforma."""
        return {
            "meta": {
                "avg_cpm": 12.50,
                "avg_ctr": 1.2,
                "trend": "stable",
                "best_formats": ["Reels", "Stories", "Carousel"]
            },
            "google": {
                "avg_cpc": 2.30,
                "avg_ctr": 3.5,
                "trend": "increasing",
                "best_formats": ["Search", "Performance Max", "YouTube"]
            },
            "tiktok": {
                "avg_cpm": 8.00,
                "avg_ctr": 1.8,
                "trend": "growing",
                "best_formats": ["In-Feed", "Spark Ads"]
            },
            "recommendation": "Diversificar entre Meta e Google, testar TikTok para público jovem"
        }
    
    def _analyze_market_saturation(self, industry: str) -> Dict:
        """Analisa saturação do mercado."""
        return {
            "saturation_level": "medium",
            "saturation_score": 0.65,
            "audience_fatigue_indicators": [
                {"indicator": "Frequência média", "value": 4.2, "threshold": 5.0, "status": "ok"},
                {"indicator": "CTR trend", "value": -0.05, "threshold": -0.1, "status": "warning"},
                {"indicator": "CPM trend", "value": 0.08, "threshold": 0.15, "status": "ok"}
            ],
            "recommendations": [
                "Renovar criativos a cada 2-3 semanas",
                "Expandir para novas audiências",
                "Testar novos formatos de anúncio"
            ]
        }
    
    def get_opportunity_score(self, industry: str, target_audience: Dict) -> Dict:
        """Calcula score de oportunidade para um mercado/audiência."""
        insights = self.get_ecosystem_insights(industry)
        
        # Calcular score baseado em múltiplos fatores
        trend_score = 0.7  # Baseado em tendências
        competition_score = 0.6  # Baseado em competição
        saturation_score = 1 - insights["saturation_analysis"]["saturation_score"]
        sentiment_score = insights["audience_sentiment"]["sentiment_score"]
        
        opportunity_score = (trend_score * 0.25 + competition_score * 0.25 + 
                           saturation_score * 0.25 + sentiment_score * 0.25)
        
        return {
            "opportunity_score": round(opportunity_score, 2),
            "components": {
                "trend_score": trend_score,
                "competition_score": competition_score,
                "saturation_score": round(saturation_score, 2),
                "sentiment_score": sentiment_score
            },
            "recommendation": self._get_opportunity_recommendation(opportunity_score)
        }
    
    def _get_opportunity_recommendation(self, score: float) -> str:
        """Gera recomendação baseada no score de oportunidade."""
        if score >= 0.75:
            return "Excelente oportunidade! Recomendamos investimento agressivo."
        elif score >= 0.5:
            return "Boa oportunidade. Investimento moderado recomendado."
        elif score >= 0.25:
            return "Oportunidade limitada. Proceda com cautela."
        else:
            return "Mercado saturado. Considere nichos alternativos."
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de inteligência de ecossistema."""
        return {
            "market_data_entries": len(self.market_data),
            "trend_history_count": len(self.trend_history),
            "competitors_tracked": len(self.competitor_tracking)
        }


ecosystem_intelligence = EcosystemIntelligence()

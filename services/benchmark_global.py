"""
BENCHMARK GLOBAL - Sistema de Benchmark Automático
Comparação com médias do mercado por nicho, país e plataforma
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

class BenchmarkGlobal:
    """Sistema de benchmark global automático."""
    
    def __init__(self):
        self.name = "Benchmark Global"
        self.version = "2.0.0"
        
        # Benchmarks por nicho (dados baseados em médias de mercado)
        self.niche_benchmarks = {
            "ecommerce": {
                "ctr": {"min": 0.8, "avg": 1.2, "top": 2.5, "unit": "%"},
                "cpc": {"min": 0.30, "avg": 0.80, "top": 0.20, "unit": "BRL"},
                "cpa": {"min": 80, "avg": 45, "top": 25, "unit": "BRL"},
                "roas": {"min": 1.5, "avg": 2.5, "top": 5.0, "unit": "x"},
                "conversion_rate": {"min": 1.0, "avg": 2.5, "top": 5.0, "unit": "%"},
                "aov": {"min": 80, "avg": 150, "top": 300, "unit": "BRL"}
            },
            "infoprodutos": {
                "ctr": {"min": 0.5, "avg": 1.0, "top": 2.0, "unit": "%"},
                "cpc": {"min": 0.50, "avg": 1.50, "top": 0.40, "unit": "BRL"},
                "cpa": {"min": 150, "avg": 80, "top": 40, "unit": "BRL"},
                "roas": {"min": 2.0, "avg": 4.0, "top": 10.0, "unit": "x"},
                "conversion_rate": {"min": 0.5, "avg": 1.5, "top": 4.0, "unit": "%"},
                "aov": {"min": 197, "avg": 497, "top": 1997, "unit": "BRL"}
            },
            "saas": {
                "ctr": {"min": 0.4, "avg": 0.8, "top": 1.5, "unit": "%"},
                "cpc": {"min": 2.00, "avg": 5.00, "top": 1.50, "unit": "BRL"},
                "cpa": {"min": 300, "avg": 150, "top": 50, "unit": "BRL"},
                "roas": {"min": 3.0, "avg": 6.0, "top": 15.0, "unit": "x"},
                "conversion_rate": {"min": 1.0, "avg": 3.0, "top": 7.0, "unit": "%"},
                "ltv": {"min": 500, "avg": 1500, "top": 5000, "unit": "BRL"}
            },
            "servicos_locais": {
                "ctr": {"min": 1.0, "avg": 2.0, "top": 4.0, "unit": "%"},
                "cpc": {"min": 0.50, "avg": 1.20, "top": 0.30, "unit": "BRL"},
                "cpa": {"min": 100, "avg": 50, "top": 20, "unit": "BRL"},
                "roas": {"min": 2.0, "avg": 4.0, "top": 8.0, "unit": "x"},
                "conversion_rate": {"min": 2.0, "avg": 5.0, "top": 10.0, "unit": "%"}
            },
            "lead_generation": {
                "ctr": {"min": 0.6, "avg": 1.2, "top": 2.5, "unit": "%"},
                "cpc": {"min": 0.80, "avg": 2.00, "top": 0.50, "unit": "BRL"},
                "cpl": {"min": 50, "avg": 25, "top": 10, "unit": "BRL"},
                "conversion_rate": {"min": 5.0, "avg": 12.0, "top": 25.0, "unit": "%"}
            },
            "apps": {
                "ctr": {"min": 0.3, "avg": 0.7, "top": 1.5, "unit": "%"},
                "cpi": {"min": 5.00, "avg": 2.50, "top": 1.00, "unit": "BRL"},
                "retention_d1": {"min": 20, "avg": 35, "top": 50, "unit": "%"},
                "retention_d7": {"min": 10, "avg": 20, "top": 35, "unit": "%"}
            },
            "dropshipping": {
                "ctr": {"min": 0.6, "avg": 1.0, "top": 2.0, "unit": "%"},
                "cpc": {"min": 0.40, "avg": 1.00, "top": 0.25, "unit": "BRL"},
                "cpa": {"min": 60, "avg": 35, "top": 15, "unit": "BRL"},
                "roas": {"min": 1.8, "avg": 3.0, "top": 6.0, "unit": "x"},
                "margin": {"min": 20, "avg": 35, "top": 50, "unit": "%"}
            },
            "afiliados": {
                "ctr": {"min": 0.4, "avg": 0.9, "top": 1.8, "unit": "%"},
                "cpc": {"min": 0.60, "avg": 1.50, "top": 0.35, "unit": "BRL"},
                "epc": {"min": 0.50, "avg": 2.00, "top": 5.00, "unit": "BRL"},
                "conversion_rate": {"min": 0.3, "avg": 1.0, "top": 3.0, "unit": "%"}
            }
        }
        
        # Multiplicadores por país
        self.country_multipliers = {
            "BR": {"cpc": 1.0, "cpa": 1.0, "roas": 1.0},
            "US": {"cpc": 3.5, "cpa": 2.5, "roas": 1.2},
            "UK": {"cpc": 3.0, "cpa": 2.2, "roas": 1.15},
            "DE": {"cpc": 2.8, "cpa": 2.0, "roas": 1.1},
            "FR": {"cpc": 2.5, "cpa": 1.8, "roas": 1.05},
            "ES": {"cpc": 1.5, "cpa": 1.3, "roas": 1.0},
            "PT": {"cpc": 1.3, "cpa": 1.2, "roas": 0.95},
            "MX": {"cpc": 0.7, "cpa": 0.8, "roas": 0.9},
            "AR": {"cpc": 0.5, "cpa": 0.6, "roas": 0.85},
            "CO": {"cpc": 0.6, "cpa": 0.7, "roas": 0.88}
        }
        
        # Multiplicadores por plataforma
        self.platform_multipliers = {
            "facebook": {"cpc": 1.0, "ctr": 1.0, "conversion": 1.0},
            "instagram": {"cpc": 1.1, "ctr": 1.2, "conversion": 0.9},
            "google_search": {"cpc": 1.5, "ctr": 0.8, "conversion": 1.3},
            "google_display": {"cpc": 0.5, "ctr": 0.3, "conversion": 0.6},
            "youtube": {"cpc": 0.8, "ctr": 0.5, "conversion": 0.7},
            "tiktok": {"cpc": 0.6, "ctr": 1.5, "conversion": 0.8},
            "linkedin": {"cpc": 3.0, "ctr": 0.4, "conversion": 1.5}
        }
        
        # Histórico de benchmarks (simulado)
        self.benchmark_history = {}
    
    def get_benchmark(
        self,
        niche: str,
        country: str = "BR",
        platform: str = "facebook",
        metrics: List[str] = None
    ) -> Dict[str, Any]:
        """Obtém benchmark para um contexto específico."""
        
        # Obter benchmarks base do nicho
        niche_key = niche.lower().replace(" ", "_")
        base_benchmarks = self.niche_benchmarks.get(
            niche_key, 
            self.niche_benchmarks["ecommerce"]
        )
        
        # Obter multiplicadores
        country_mult = self.country_multipliers.get(country, self.country_multipliers["BR"])
        platform_mult = self.platform_multipliers.get(platform, self.platform_multipliers["facebook"])
        
        # Aplicar multiplicadores
        adjusted_benchmarks = {}
        for metric, values in base_benchmarks.items():
            if metrics and metric not in metrics:
                continue
            
            adjusted = {
                "unit": values["unit"],
                "min": values["min"],
                "avg": values["avg"],
                "top": values["top"]
            }
            
            # Aplicar multiplicadores de país
            if metric in ["cpc", "cpa", "cpl", "cpi"]:
                mult = country_mult.get("cpa", 1.0)
                adjusted["min"] = round(values["min"] * mult, 2)
                adjusted["avg"] = round(values["avg"] * mult, 2)
                adjusted["top"] = round(values["top"] * mult, 2)
            elif metric == "roas":
                mult = country_mult.get("roas", 1.0)
                adjusted["min"] = round(values["min"] * mult, 2)
                adjusted["avg"] = round(values["avg"] * mult, 2)
                adjusted["top"] = round(values["top"] * mult, 2)
            
            # Aplicar multiplicadores de plataforma
            if metric == "ctr":
                mult = platform_mult.get("ctr", 1.0)
                adjusted["min"] = round(values["min"] * mult, 2)
                adjusted["avg"] = round(values["avg"] * mult, 2)
                adjusted["top"] = round(values["top"] * mult, 2)
            elif metric == "conversion_rate":
                mult = platform_mult.get("conversion", 1.0)
                adjusted["min"] = round(values["min"] * mult, 2)
                adjusted["avg"] = round(values["avg"] * mult, 2)
                adjusted["top"] = round(values["top"] * mult, 2)
            
            adjusted_benchmarks[metric] = adjusted
        
        return {
            "timestamp": datetime.now().isoformat(),
            "context": {
                "niche": niche,
                "country": country,
                "platform": platform
            },
            "benchmarks": adjusted_benchmarks,
            "data_source": "market_aggregation",
            "last_updated": datetime.now().isoformat(),
            "confidence": self._calculate_confidence(niche_key, country, platform)
        }
    
    def compare_performance(
        self,
        user_metrics: Dict[str, float],
        niche: str,
        country: str = "BR",
        platform: str = "facebook"
    ) -> Dict[str, Any]:
        """Compara performance do usuário com benchmarks."""
        
        benchmarks = self.get_benchmark(niche, country, platform)
        
        comparisons = {}
        overall_score = 0
        metrics_count = 0
        
        for metric, value in user_metrics.items():
            if metric not in benchmarks["benchmarks"]:
                continue
            
            benchmark = benchmarks["benchmarks"][metric]
            
            # Determinar se maior é melhor ou menor é melhor
            higher_is_better = metric in ["ctr", "roas", "conversion_rate", "epc", "aov", "ltv", "margin", "retention_d1", "retention_d7"]
            
            # Calcular posição relativa
            if higher_is_better:
                if value >= benchmark["top"]:
                    position = "top_performer"
                    percentile = 95
                    score = 100
                elif value >= benchmark["avg"]:
                    position = "above_average"
                    percentile = 75
                    score = 75
                elif value >= benchmark["min"]:
                    position = "average"
                    percentile = 50
                    score = 50
                else:
                    position = "below_average"
                    percentile = 25
                    score = 25
            else:
                # Para métricas onde menor é melhor (CPC, CPA, etc.)
                if value <= benchmark["top"]:
                    position = "top_performer"
                    percentile = 95
                    score = 100
                elif value <= benchmark["avg"]:
                    position = "above_average"
                    percentile = 75
                    score = 75
                elif value <= benchmark["min"]:
                    position = "average"
                    percentile = 50
                    score = 50
                else:
                    position = "below_average"
                    percentile = 25
                    score = 25
            
            # Calcular variação
            variation = ((value - benchmark["avg"]) / benchmark["avg"]) * 100 if benchmark["avg"] != 0 else 0
            
            comparisons[metric] = {
                "your_value": value,
                "benchmark_min": benchmark["min"],
                "benchmark_avg": benchmark["avg"],
                "benchmark_top": benchmark["top"],
                "unit": benchmark["unit"],
                "position": position,
                "percentile": percentile,
                "variation_from_avg": round(variation, 1),
                "score": score
            }
            
            overall_score += score
            metrics_count += 1
        
        # Calcular score geral
        final_score = round(overall_score / metrics_count, 1) if metrics_count > 0 else 0
        
        # Determinar classificação
        if final_score >= 90:
            classification = "Excepcional"
            emoji = "🏆"
        elif final_score >= 75:
            classification = "Acima da Média"
            emoji = "⭐"
        elif final_score >= 50:
            classification = "Na Média"
            emoji = "✅"
        elif final_score >= 25:
            classification = "Abaixo da Média"
            emoji = "⚠️"
        else:
            classification = "Precisa Melhorar"
            emoji = "🔴"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "context": benchmarks["context"],
            "comparisons": comparisons,
            "overall_score": final_score,
            "classification": classification,
            "classification_emoji": emoji,
            "metrics_analyzed": metrics_count,
            "recommendations": self._generate_recommendations(comparisons),
            "improvement_priorities": self._get_improvement_priorities(comparisons)
        }
    
    def get_industry_trends(
        self,
        niche: str,
        country: str = "BR",
        period: str = "30d"
    ) -> Dict[str, Any]:
        """Obtém tendências do setor."""
        
        # Simular tendências (em produção, viria de APIs de mercado)
        trends = {
            "cpc": {
                "direction": random.choice(["up", "down", "stable"]),
                "change_percent": round(random.uniform(-15, 15), 1),
                "forecast": random.choice(["increasing", "decreasing", "stable"])
            },
            "ctr": {
                "direction": random.choice(["up", "down", "stable"]),
                "change_percent": round(random.uniform(-10, 10), 1),
                "forecast": random.choice(["increasing", "decreasing", "stable"])
            },
            "competition": {
                "level": random.choice(["low", "medium", "high", "very_high"]),
                "change": random.choice(["increasing", "decreasing", "stable"]),
                "new_advertisers": random.randint(0, 50)
            },
            "seasonality": {
                "current_period": self._get_seasonality_period(),
                "expected_impact": random.choice(["positive", "negative", "neutral"]),
                "recommendation": self._get_seasonality_recommendation()
            }
        }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "niche": niche,
            "country": country,
            "period": period,
            "trends": trends,
            "market_insights": self._generate_market_insights(niche, trends),
            "opportunities": self._identify_opportunities(niche, trends)
        }
    
    def get_competitor_benchmark(
        self,
        niche: str,
        country: str = "BR",
        competitor_size: str = "medium"
    ) -> Dict[str, Any]:
        """Obtém benchmark de concorrentes."""
        
        # Multiplicadores por tamanho de concorrente
        size_multipliers = {
            "small": {"budget": 0.5, "efficiency": 0.9},
            "medium": {"budget": 1.0, "efficiency": 1.0},
            "large": {"budget": 3.0, "efficiency": 1.1},
            "enterprise": {"budget": 10.0, "efficiency": 1.2}
        }
        
        mult = size_multipliers.get(competitor_size, size_multipliers["medium"])
        base = self.niche_benchmarks.get(niche, self.niche_benchmarks["ecommerce"])
        
        competitor_metrics = {
            "estimated_daily_budget": round(500 * mult["budget"], 2),
            "estimated_monthly_spend": round(15000 * mult["budget"], 2),
            "estimated_roas": round(base.get("roas", {}).get("avg", 2.5) * mult["efficiency"], 2),
            "estimated_cpa": round(base.get("cpa", {}).get("avg", 50) / mult["efficiency"], 2),
            "estimated_market_share": round(random.uniform(5, 25) * mult["budget"], 1),
            "ad_frequency": {
                "new_ads_per_week": random.randint(2, 10),
                "active_ads": random.randint(5, 30),
                "avg_ad_lifespan_days": random.randint(7, 30)
            }
        }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "niche": niche,
            "country": country,
            "competitor_size": competitor_size,
            "competitor_metrics": competitor_metrics,
            "competitive_analysis": {
                "your_position": "challenger",
                "gap_to_leader": f"{random.randint(20, 50)}%",
                "growth_potential": "high" if competitor_size in ["small", "medium"] else "medium"
            },
            "strategic_recommendations": self._generate_competitive_recommendations(competitor_size)
        }
    
    def calculate_performance_score(
        self,
        metrics: Dict[str, float],
        niche: str,
        weights: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """Calcula score de performance ponderado."""
        
        # Pesos padrão
        default_weights = {
            "roas": 0.30,
            "cpa": 0.25,
            "ctr": 0.15,
            "conversion_rate": 0.20,
            "cpc": 0.10
        }
        
        weights = weights or default_weights
        
        benchmarks = self.get_benchmark(niche)["benchmarks"]
        
        weighted_score = 0
        total_weight = 0
        metric_scores = {}
        
        for metric, value in metrics.items():
            if metric not in benchmarks or metric not in weights:
                continue
            
            benchmark = benchmarks[metric]
            weight = weights[metric]
            
            # Calcular score normalizado (0-100)
            higher_is_better = metric in ["ctr", "roas", "conversion_rate"]
            
            if higher_is_better:
                if value >= benchmark["top"]:
                    score = 100
                elif value >= benchmark["avg"]:
                    score = 50 + 50 * (value - benchmark["avg"]) / (benchmark["top"] - benchmark["avg"])
                elif value >= benchmark["min"]:
                    score = 50 * (value - benchmark["min"]) / (benchmark["avg"] - benchmark["min"])
                else:
                    score = 0
            else:
                if value <= benchmark["top"]:
                    score = 100
                elif value <= benchmark["avg"]:
                    score = 50 + 50 * (benchmark["avg"] - value) / (benchmark["avg"] - benchmark["top"])
                elif value <= benchmark["min"]:
                    score = 50 * (benchmark["min"] - value) / (benchmark["min"] - benchmark["avg"])
                else:
                    score = 0
            
            score = max(0, min(100, score))
            metric_scores[metric] = round(score, 1)
            weighted_score += score * weight
            total_weight += weight
        
        final_score = round(weighted_score / total_weight, 1) if total_weight > 0 else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_score": final_score,
            "metric_scores": metric_scores,
            "weights_used": weights,
            "grade": self._score_to_grade(final_score),
            "interpretation": self._interpret_score(final_score)
        }
    
    def _calculate_confidence(self, niche: str, country: str, platform: str) -> str:
        """Calcula nível de confiança dos dados."""
        # Nichos com mais dados têm maior confiança
        high_confidence_niches = ["ecommerce", "infoprodutos", "lead_generation"]
        high_confidence_countries = ["BR", "US", "UK"]
        high_confidence_platforms = ["facebook", "google_search"]
        
        score = 0
        if niche in high_confidence_niches:
            score += 1
        if country in high_confidence_countries:
            score += 1
        if platform in high_confidence_platforms:
            score += 1
        
        if score >= 3:
            return "high"
        elif score >= 2:
            return "medium"
        return "low"
    
    def _generate_recommendations(self, comparisons: Dict) -> List[Dict]:
        """Gera recomendações baseadas nas comparações."""
        recommendations = []
        
        for metric, data in comparisons.items():
            if data["position"] == "below_average":
                recommendations.append({
                    "metric": metric,
                    "priority": "high",
                    "message": f"Seu {metric} está abaixo da média do mercado. Considere otimizar.",
                    "target": data["benchmark_avg"]
                })
            elif data["position"] == "average":
                recommendations.append({
                    "metric": metric,
                    "priority": "medium",
                    "message": f"Seu {metric} está na média. Há espaço para melhorar.",
                    "target": data["benchmark_top"]
                })
        
        return sorted(recommendations, key=lambda x: x["priority"] == "high", reverse=True)
    
    def _get_improvement_priorities(self, comparisons: Dict) -> List[str]:
        """Obtém prioridades de melhoria."""
        priorities = []
        
        # Ordenar por score (menor primeiro)
        sorted_metrics = sorted(comparisons.items(), key=lambda x: x[1]["score"])
        
        for metric, data in sorted_metrics[:3]:
            if data["score"] < 75:
                priorities.append(metric)
        
        return priorities
    
    def _get_seasonality_period(self) -> str:
        """Obtém período de sazonalidade atual."""
        month = datetime.now().month
        
        if month in [11, 12]:
            return "alta_temporada_fim_ano"
        elif month in [1, 2]:
            return "pos_festas"
        elif month in [3, 4, 5]:
            return "primeiro_semestre"
        elif month in [6, 7]:
            return "meio_ano"
        else:
            return "segundo_semestre"
    
    def _get_seasonality_recommendation(self) -> str:
        """Obtém recomendação de sazonalidade."""
        period = self._get_seasonality_period()
        
        recommendations = {
            "alta_temporada_fim_ano": "Aumente orçamentos e prepare campanhas de Black Friday/Natal",
            "pos_festas": "Foque em liquidações e renovação de estoque",
            "primeiro_semestre": "Período estável - ideal para testes",
            "meio_ano": "Prepare campanhas de Dia dos Namorados e São João",
            "segundo_semestre": "Comece a planejar campanhas de fim de ano"
        }
        
        return recommendations.get(period, "Mantenha estratégia atual")
    
    def _generate_market_insights(self, niche: str, trends: Dict) -> List[str]:
        """Gera insights de mercado."""
        insights = []
        
        if trends["cpc"]["direction"] == "up":
            insights.append(f"CPCs estão subindo no nicho {niche} - considere otimizar qualidade de anúncios")
        elif trends["cpc"]["direction"] == "down":
            insights.append(f"CPCs em queda - oportunidade para escalar")
        
        if trends["competition"]["level"] in ["high", "very_high"]:
            insights.append("Competição alta - diferencie-se com criativos únicos")
        
        return insights
    
    def _identify_opportunities(self, niche: str, trends: Dict) -> List[Dict]:
        """Identifica oportunidades de mercado."""
        opportunities = []
        
        if trends["cpc"]["direction"] == "down":
            opportunities.append({
                "type": "cost_reduction",
                "description": "CPCs em queda - momento para escalar",
                "action": "Aumentar orçamento gradualmente"
            })
        
        if trends["competition"]["change"] == "decreasing":
            opportunities.append({
                "type": "market_share",
                "description": "Concorrência diminuindo",
                "action": "Expandir presença no mercado"
            })
        
        return opportunities
    
    def _generate_competitive_recommendations(self, competitor_size: str) -> List[str]:
        """Gera recomendações competitivas."""
        if competitor_size in ["small", "medium"]:
            return [
                "Foque em nichos específicos onde pode dominar",
                "Invista em criativos de alta qualidade",
                "Teste constantemente novos ângulos"
            ]
        else:
            return [
                "Busque diferenciação através de ofertas únicas",
                "Considere parcerias estratégicas",
                "Foque em segmentos negligenciados pelos grandes players"
            ]
    
    def _score_to_grade(self, score: float) -> str:
        """Converte score em nota."""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B+"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 40:
            return "D"
        return "F"
    
    def _interpret_score(self, score: float) -> str:
        """Interpreta o score."""
        if score >= 90:
            return "Performance excepcional! Você está entre os top performers do mercado."
        elif score >= 70:
            return "Boa performance! Acima da média do mercado."
        elif score >= 50:
            return "Performance na média. Há oportunidades de melhoria."
        elif score >= 30:
            return "Performance abaixo da média. Recomendamos otimizações urgentes."
        return "Performance crítica. Revise sua estratégia completamente."


# Instância global
benchmark_global = BenchmarkGlobal()

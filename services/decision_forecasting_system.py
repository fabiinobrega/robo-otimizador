# services/decision_forecasting_system.py
"""
NEXORA PRIME - Sistema de Simulação de Futuros
Previsão de cenários e análise de decisões
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


class DecisionForecastingSystem:
    """Sistema de simulação de futuros e previsão de cenários."""
    
    def __init__(self):
        self.simulations = []
        self.forecasts = []
        self.scenario_templates = {
            "scale_up": {
                "name": "Escalar Investimento",
                "budget_multiplier": 1.5,
                "expected_roas_change": -0.1,
                "risk_level": "medium"
            },
            "maintain": {
                "name": "Manter Atual",
                "budget_multiplier": 1.0,
                "expected_roas_change": 0,
                "risk_level": "low"
            },
            "scale_down": {
                "name": "Reduzir Investimento",
                "budget_multiplier": 0.5,
                "expected_roas_change": 0.1,
                "risk_level": "low"
            },
            "pause": {
                "name": "Pausar Campanha",
                "budget_multiplier": 0,
                "expected_roas_change": 0,
                "risk_level": "none"
            },
            "aggressive_scale": {
                "name": "Escala Agressiva",
                "budget_multiplier": 2.0,
                "expected_roas_change": -0.2,
                "risk_level": "high"
            }
        }
    
    def forecast_scenarios(self, current_context: Dict) -> List[Dict]:
        """Simula múltiplos cenários futuros com base em diferentes ações."""
        scenarios = []
        
        current_spend = current_context.get("spend", 1000)
        current_roas = current_context.get("roas", 2.0)
        current_revenue = current_context.get("revenue", current_spend * current_roas)
        
        for action, template in self.scenario_templates.items():
            scenario = self._simulate_scenario(
                action=action,
                template=template,
                current_spend=current_spend,
                current_roas=current_roas,
                current_revenue=current_revenue,
                context=current_context
            )
            scenarios.append(scenario)
        
        # Calcular custo de oportunidade
        best_scenario = max(scenarios, key=lambda s: s["projected_profit"])
        for s in scenarios:
            s["opportunity_cost"] = best_scenario["projected_profit"] - s["projected_profit"]
        
        # Ordenar por lucro projetado
        scenarios.sort(key=lambda s: s["projected_profit"], reverse=True)
        
        # Registrar simulação
        simulation_record = {
            "id": f"SIM_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "context": current_context,
            "scenarios": scenarios,
            "simulated_at": datetime.now().isoformat()
        }
        self.simulations.append(simulation_record)
        
        return scenarios
    
    def _simulate_scenario(self, action: str, template: Dict, current_spend: float,
                          current_roas: float, current_revenue: float, context: Dict) -> Dict:
        """Simula um cenário específico."""
        
        # Calcular métricas projetadas
        projected_spend = current_spend * template["budget_multiplier"]
        projected_roas = max(0.5, current_roas + template["expected_roas_change"])
        projected_revenue = projected_spend * projected_roas
        projected_profit = projected_revenue - projected_spend
        
        # Calcular confiança baseada em dados históricos
        confidence = self._calculate_confidence(action, context)
        
        # Calcular risco
        risk_assessment = self._assess_risk(action, template, context)
        
        return {
            "scenario_name": template["name"],
            "action": action,
            "projected_spend": round(projected_spend, 2),
            "projected_roas": round(projected_roas, 2),
            "projected_revenue": round(projected_revenue, 2),
            "projected_profit": round(projected_profit, 2),
            "profit_change_percent": round(((projected_profit - (current_revenue - current_spend)) / max(1, current_revenue - current_spend)) * 100, 1) if current_revenue - current_spend > 0 else 0,
            "confidence": round(confidence, 2),
            "risk_level": template["risk_level"],
            "risk_assessment": risk_assessment,
            "recommendation_score": self._calculate_recommendation_score(projected_profit, confidence, risk_assessment)
        }
    
    def _calculate_confidence(self, action: str, context: Dict) -> float:
        """Calcula confiança na previsão."""
        base_confidence = 0.7
        
        # Ajustar baseado em dados históricos
        historical_data_points = context.get("historical_data_points", 0)
        if historical_data_points > 30:
            base_confidence += 0.15
        elif historical_data_points > 7:
            base_confidence += 0.05
        
        # Ajustar baseado na ação
        if action == "maintain":
            base_confidence += 0.1
        elif action in ["aggressive_scale", "pause"]:
            base_confidence -= 0.1
        
        return min(0.95, max(0.3, base_confidence))
    
    def _assess_risk(self, action: str, template: Dict, context: Dict) -> Dict:
        """Avalia o risco de uma ação."""
        risk_factors = []
        risk_score = 0
        
        # Risco de budget
        if template["budget_multiplier"] > 1.5:
            risk_factors.append("Alto aumento de orçamento")
            risk_score += 0.3
        
        # Risco de ROAS
        if template["expected_roas_change"] < -0.15:
            risk_factors.append("Possível queda significativa de ROAS")
            risk_score += 0.2
        
        # Risco de mercado
        market_volatility = context.get("market_volatility", "medium")
        if market_volatility == "high":
            risk_factors.append("Alta volatilidade de mercado")
            risk_score += 0.2
        
        return {
            "risk_score": round(min(1, risk_score), 2),
            "risk_factors": risk_factors,
            "mitigation_suggestions": self._get_risk_mitigations(risk_factors)
        }
    
    def _get_risk_mitigations(self, risk_factors: List[str]) -> List[str]:
        """Gera sugestões de mitigação de risco."""
        mitigations = []
        
        if "Alto aumento de orçamento" in risk_factors:
            mitigations.append("Escalar gradualmente em 20% por vez")
        if "Possível queda significativa de ROAS" in risk_factors:
            mitigations.append("Monitorar ROAS diariamente e definir limite de perda")
        if "Alta volatilidade de mercado" in risk_factors:
            mitigations.append("Manter reserva de orçamento para ajustes rápidos")
        
        return mitigations
    
    def _calculate_recommendation_score(self, profit: float, confidence: float, risk: Dict) -> float:
        """Calcula score de recomendação."""
        # Normalizar lucro (assumindo range de -1000 a 10000)
        profit_score = min(1, max(0, (profit + 1000) / 11000))
        
        # Combinar fatores
        risk_penalty = risk["risk_score"] * 0.3
        
        score = (profit_score * 0.5) + (confidence * 0.3) - risk_penalty
        return round(max(0, min(1, score)), 2)
    
    def generate_forecast(self, campaign_id: str, context: Dict, days: int = 30) -> Dict:
        """Gera previsão de performance para os próximos dias."""
        current_metrics = context.get("current_metrics", {})
        
        daily_forecasts = []
        cumulative_spend = 0
        cumulative_revenue = 0
        
        base_daily_spend = current_metrics.get("daily_spend", 100)
        base_roas = current_metrics.get("roas", 2.0)
        
        for day in range(1, days + 1):
            # Simular variação diária
            daily_variation = 1 + (hash(f"{campaign_id}_{day}") % 20 - 10) / 100
            
            daily_spend = base_daily_spend * daily_variation
            daily_roas = base_roas * (1 + (hash(f"{campaign_id}_{day}_roas") % 10 - 5) / 100)
            daily_revenue = daily_spend * daily_roas
            
            cumulative_spend += daily_spend
            cumulative_revenue += daily_revenue
            
            daily_forecasts.append({
                "day": day,
                "date": (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                "projected_spend": round(daily_spend, 2),
                "projected_revenue": round(daily_revenue, 2),
                "projected_roas": round(daily_roas, 2),
                "cumulative_spend": round(cumulative_spend, 2),
                "cumulative_revenue": round(cumulative_revenue, 2)
            })
        
        forecast = {
            "campaign_id": campaign_id,
            "forecast_period_days": days,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_projected_spend": round(cumulative_spend, 2),
                "total_projected_revenue": round(cumulative_revenue, 2),
                "total_projected_profit": round(cumulative_revenue - cumulative_spend, 2),
                "average_projected_roas": round(cumulative_revenue / cumulative_spend, 2) if cumulative_spend > 0 else 0
            },
            "daily_forecasts": daily_forecasts,
            "confidence_interval": {
                "lower_bound": round(cumulative_revenue * 0.8, 2),
                "upper_bound": round(cumulative_revenue * 1.2, 2)
            }
        }
        
        self.forecasts.append(forecast)
        return forecast
    
    def compare_scenarios(self, scenarios: List[Dict]) -> Dict:
        """Compara múltiplos cenários e gera recomendação."""
        if not scenarios:
            return {"error": "Nenhum cenário para comparar"}
        
        # Encontrar melhor cenário por diferentes critérios
        best_profit = max(scenarios, key=lambda s: s["projected_profit"])
        best_roas = max(scenarios, key=lambda s: s["projected_roas"])
        lowest_risk = min(scenarios, key=lambda s: s["risk_assessment"]["risk_score"])
        best_overall = max(scenarios, key=lambda s: s["recommendation_score"])
        
        return {
            "comparison": {
                "best_for_profit": best_profit["action"],
                "best_for_roas": best_roas["action"],
                "lowest_risk": lowest_risk["action"],
                "best_overall": best_overall["action"]
            },
            "recommendation": {
                "action": best_overall["action"],
                "scenario_name": best_overall["scenario_name"],
                "reasoning": f"Melhor equilíbrio entre lucro projetado (R${best_overall['projected_profit']:.2f}), confiança ({best_overall['confidence']:.0%}) e risco ({best_overall['risk_level']})"
            },
            "scenarios_ranked": sorted(scenarios, key=lambda s: s["recommendation_score"], reverse=True)
        }
    
    def get_simulation_history(self, limit: int = 10) -> List[Dict]:
        """Retorna histórico de simulações."""
        return self.simulations[-limit:]
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de previsão."""
        return {
            "total_simulations": len(self.simulations),
            "total_forecasts": len(self.forecasts),
            "scenario_templates": list(self.scenario_templates.keys())
        }


# Instância global
decision_forecasting = DecisionForecastingSystem()

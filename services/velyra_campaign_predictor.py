#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VELYRA CAMPAIGN PREDICTOR - Sistema de Predição e Simulação
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random


class VelyraCampaignPredictor:
    """Sistema de predição de campanhas."""
    
    def __init__(self, db_path: str = "nexora.db"):
        self.db_path = db_path
        self.benchmarks = self._load_benchmarks()
    
    def _load_benchmarks(self) -> Dict[str, Dict]:
        """Carrega benchmarks de mercado."""
        return {
            "dental": {
                "meta_ads": {"avg_ctr": 1.5, "avg_cpc": 0.80, "avg_cpa": 25.0, "avg_roas": 3.5, "avg_conversion_rate": 2.5},
                "google_ads": {"avg_ctr": 3.0, "avg_cpc": 1.20, "avg_cpa": 30.0, "avg_roas": 3.0, "avg_conversion_rate": 3.0}
            },
            "default": {
                "meta_ads": {"avg_ctr": 1.0, "avg_cpc": 0.70, "avg_cpa": 30.0, "avg_roas": 3.0, "avg_conversion_rate": 2.0},
                "google_ads": {"avg_ctr": 2.0, "avg_cpc": 1.00, "avg_cpa": 35.0, "avg_roas": 2.5, "avg_conversion_rate": 2.0}
            }
        }
    
    def predict_campaign_performance(
        self, niche: str, platform: str, budget: float, product_price: float,
        offer_score: int, page_score: int, market_saturation: str = "medium"
    ) -> Dict[str, Any]:
        """Prediz performance da campanha."""
        niche_key = niche.lower() if niche.lower() in self.benchmarks else "default"
        platform_key = platform.lower()
        benchmarks = self.benchmarks[niche_key].get(platform_key, self.benchmarks["default"]["meta_ads"])
        
        # Ajustar benchmarks
        quality_factor = (offer_score + page_score) / 200.0
        adjusted_cpa = benchmarks["avg_cpa"] * (1.5 - quality_factor * 0.5)
        adjusted_roas = benchmarks["avg_roas"] * (0.7 + quality_factor * 0.6)
        adjusted_conversion = benchmarks["avg_conversion_rate"] * (0.8 + quality_factor * 0.4)
        
        # Calcular predições
        estimated_clicks = int(budget / benchmarks["avg_cpc"])
        estimated_sales = int(estimated_clicks * (adjusted_conversion / 100))
        estimated_revenue = int(estimated_sales * product_price)
        estimated_profit = int(estimated_revenue - budget)
        
        predictions = {
            "estimated_cpa": round(adjusted_cpa, 2),
            "estimated_roas": round(adjusted_roas, 2),
            "estimated_ctr": benchmarks["avg_ctr"],
            "estimated_cpc": benchmarks["avg_cpc"],
            "estimated_conversion_rate": round(adjusted_conversion, 2),
            "estimated_clicks": estimated_clicks,
            "estimated_sales": estimated_sales,
            "estimated_revenue": estimated_revenue,
            "estimated_profit": estimated_profit,
            "break_even_sales": int(budget / product_price) + 1
        }
        
        # Score de sucesso
        success_score = int((offer_score + page_score) / 2)
        if predictions["estimated_roas"] >= 4.0:
            success_score += 10
        if predictions["estimated_profit"] > 0:
            success_score += 10
        success_score = min(100, success_score)
        
        # Riscos
        risks = []
        if predictions["estimated_profit"] < 0:
            risks.append({"type": "critical", "risk": "Prejuízo estimado", "detail": f"${abs(predictions['estimated_profit'])}"})
        if predictions["estimated_roas"] < 2.0:
            risks.append({"type": "warning", "risk": "ROAS muito baixo", "detail": f"{predictions['estimated_roas']}x"})
        
        return {
            "success": True,
            "predictions": predictions,
            "success_score": success_score,
            "risks": risks,
            "recommendation": "✅ LANÇAR" if success_score >= 70 else "⚠️ REVISAR"
        }
    
    def simulate_campaign(self, predictions: Dict, budget: float, duration_days: int, scenario: str = "normal") -> Dict:
        """Simula campanha."""
        scenario_factors = {"conservative": 0.7, "normal": 1.0, "aggressive": 1.3}
        factor = scenario_factors.get(scenario, 1.0)
        daily_budget = budget / duration_days
        
        simulation = []
        cumulative_spend = 0
        cumulative_sales = 0
        cumulative_revenue = 0
        
        for day in range(1, duration_days + 1):
            daily_factor = factor * random.uniform(0.8, 1.2)
            daily_clicks = int((daily_budget / predictions["estimated_cpc"]) * daily_factor)
            daily_sales = int(daily_clicks * (predictions["estimated_conversion_rate"] / 100))
            daily_revenue = daily_sales * (predictions["estimated_revenue"] / max(1, predictions["estimated_sales"]))
            
            cumulative_spend += daily_budget
            cumulative_sales += daily_sales
            cumulative_revenue += daily_revenue
            
            simulation.append({
                "day": day,
                "sales": daily_sales,
                "revenue": round(daily_revenue, 2),
                "cumulative_sales": cumulative_sales,
                "cumulative_profit": round(cumulative_revenue - cumulative_spend, 2)
            })
        
        return {"success": True, "scenario": scenario, "simulation": simulation}


# Instância global
campaign_predictor = VelyraCampaignPredictor()

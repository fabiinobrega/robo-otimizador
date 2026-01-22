"""
LTV ENGINE - Motor de Lifetime Value
Escala inteligente baseada em LTV, não apenas ROAS
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import math

class LTVEngine:
    """Motor de cálculo e otimização baseado em Lifetime Value."""
    
    def __init__(self):
        self.name = "LTV Engine"
        self.version = "2.0.0"
        
        # Benchmarks de LTV por nicho
        self.niche_ltv_benchmarks = {
            "infoprodutos": {
                "avg_ltv": 450,
                "avg_first_purchase": 297,
                "repeat_rate": 0.25,
                "avg_purchases": 1.5,
                "churn_rate_monthly": 0.05,
                "upsell_rate": 0.15
            },
            "ecommerce": {
                "avg_ltv": 350,
                "avg_first_purchase": 120,
                "repeat_rate": 0.40,
                "avg_purchases": 2.5,
                "churn_rate_monthly": 0.08,
                "upsell_rate": 0.20
            },
            "saas": {
                "avg_ltv": 1200,
                "avg_first_purchase": 97,
                "repeat_rate": 0.85,
                "avg_purchases": 12,
                "churn_rate_monthly": 0.03,
                "upsell_rate": 0.25
            },
            "servicos": {
                "avg_ltv": 800,
                "avg_first_purchase": 300,
                "repeat_rate": 0.35,
                "avg_purchases": 2.0,
                "churn_rate_monthly": 0.10,
                "upsell_rate": 0.18
            },
            "assinaturas": {
                "avg_ltv": 600,
                "avg_first_purchase": 50,
                "repeat_rate": 0.90,
                "avg_purchases": 10,
                "churn_rate_monthly": 0.05,
                "upsell_rate": 0.12
            }
        }
        
        # Multiplicadores de LTV por país
        self.country_multipliers = {
            "BR": 1.0,
            "US": 2.5,
            "UK": 2.2,
            "DE": 2.0,
            "FR": 1.8,
            "ES": 1.3,
            "PT": 1.2,
            "MX": 0.8,
            "AR": 0.6,
            "CO": 0.7
        }
    
    def calculate_ltv(
        self,
        customer_data: Dict = None,
        niche: str = "infoprodutos",
        country: str = "BR",
        historical_data: List[Dict] = None
    ) -> Dict[str, Any]:
        """Calcula LTV completo de um cliente ou segmento."""
        
        benchmark = self.niche_ltv_benchmarks.get(niche, self.niche_ltv_benchmarks["infoprodutos"])
        country_mult = self.country_multipliers.get(country, 1.0)
        
        if historical_data and len(historical_data) > 0:
            # Cálculo baseado em dados reais
            ltv_result = self._calculate_from_historical(historical_data, benchmark)
        elif customer_data:
            # Cálculo baseado em dados do cliente
            ltv_result = self._calculate_from_customer(customer_data, benchmark)
        else:
            # Cálculo baseado em benchmarks
            ltv_result = self._calculate_from_benchmark(benchmark)
        
        # Aplicar multiplicador de país
        ltv_result["ltv_adjusted"] = round(ltv_result["ltv_base"] * country_mult, 2)
        ltv_result["country"] = country
        ltv_result["country_multiplier"] = country_mult
        
        # Calcular métricas derivadas
        ltv_result["metrics"] = self._calculate_derived_metrics(ltv_result, benchmark)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "niche": niche,
            "calculation_method": ltv_result.get("method", "benchmark"),
            "ltv": ltv_result,
            "recommendations": self._generate_ltv_recommendations(ltv_result, benchmark)
        }
    
    def calculate_ltv_by_campaign(self, campaign_id: str, campaign_data: Dict) -> Dict[str, Any]:
        """Calcula LTV específico de uma campanha."""
        
        customers = campaign_data.get("customers", [])
        total_revenue = sum(c.get("total_spent", 0) for c in customers)
        customer_count = len(customers)
        
        if customer_count == 0:
            return {
                "campaign_id": campaign_id,
                "error": "Sem clientes para calcular LTV"
            }
        
        # Calcular métricas por cliente
        avg_first_purchase = sum(c.get("first_purchase", 0) for c in customers) / customer_count
        avg_total_spent = total_revenue / customer_count
        repeat_customers = sum(1 for c in customers if c.get("purchases", 1) > 1)
        repeat_rate = repeat_customers / customer_count
        avg_purchases = sum(c.get("purchases", 1) for c in customers) / customer_count
        
        # Projetar LTV futuro
        projected_ltv = self._project_future_ltv(avg_total_spent, repeat_rate, avg_purchases)
        
        return {
            "campaign_id": campaign_id,
            "timestamp": datetime.now().isoformat(),
            "customer_count": customer_count,
            "metrics": {
                "avg_first_purchase": round(avg_first_purchase, 2),
                "avg_total_spent": round(avg_total_spent, 2),
                "repeat_rate": round(repeat_rate * 100, 1),
                "avg_purchases": round(avg_purchases, 2)
            },
            "ltv": {
                "current": round(avg_total_spent, 2),
                "projected_12m": round(projected_ltv["12_months"], 2),
                "projected_24m": round(projected_ltv["24_months"], 2),
                "lifetime": round(projected_ltv["lifetime"], 2)
            },
            "quality_score": self._calculate_customer_quality_score(
                avg_total_spent, repeat_rate, avg_purchases
            )
        }
    
    def calculate_ltv_by_audience(self, audience_id: str, audience_data: Dict) -> Dict[str, Any]:
        """Calcula LTV por público/audiência."""
        
        segments = audience_data.get("segments", [])
        
        segment_ltvs = []
        for segment in segments:
            segment_ltv = self._calculate_segment_ltv(segment)
            segment_ltvs.append(segment_ltv)
        
        # Calcular LTV médio ponderado
        total_customers = sum(s.get("customer_count", 0) for s in segment_ltvs)
        weighted_ltv = sum(
            s.get("ltv", 0) * s.get("customer_count", 0) 
            for s in segment_ltvs
        ) / total_customers if total_customers > 0 else 0
        
        return {
            "audience_id": audience_id,
            "timestamp": datetime.now().isoformat(),
            "total_customers": total_customers,
            "weighted_avg_ltv": round(weighted_ltv, 2),
            "segments": segment_ltvs,
            "best_segment": max(segment_ltvs, key=lambda x: x.get("ltv", 0)) if segment_ltvs else None,
            "worst_segment": min(segment_ltvs, key=lambda x: x.get("ltv", 0)) if segment_ltvs else None
        }
    
    def calculate_ltv_by_creative(self, creative_id: str, creative_data: Dict) -> Dict[str, Any]:
        """Calcula LTV por criativo."""
        
        customers = creative_data.get("customers", [])
        
        if not customers:
            return {
                "creative_id": creative_id,
                "error": "Sem dados de clientes"
            }
        
        total_ltv = sum(c.get("ltv", 0) for c in customers)
        avg_ltv = total_ltv / len(customers)
        
        return {
            "creative_id": creative_id,
            "timestamp": datetime.now().isoformat(),
            "customer_count": len(customers),
            "avg_ltv": round(avg_ltv, 2),
            "total_ltv": round(total_ltv, 2),
            "ltv_distribution": self._calculate_ltv_distribution(customers)
        }
    
    def suggest_max_cpa(
        self,
        ltv: float,
        target_margin: float = 0.30,
        payback_months: int = 3
    ) -> Dict[str, Any]:
        """Sugere CPA máximo baseado no LTV."""
        
        # CPA máximo para margem desejada
        max_cpa_margin = ltv * (1 - target_margin)
        
        # CPA máximo para payback desejado (assumindo receita linear)
        monthly_revenue = ltv / 12  # Simplificado
        max_cpa_payback = monthly_revenue * payback_months
        
        # CPA recomendado (mais conservador dos dois)
        recommended_cpa = min(max_cpa_margin, max_cpa_payback)
        
        # Faixas de CPA
        cpa_ranges = {
            "aggressive": round(ltv * 0.8, 2),  # 80% do LTV
            "moderate": round(ltv * 0.5, 2),    # 50% do LTV
            "conservative": round(ltv * 0.3, 2), # 30% do LTV
            "safe": round(ltv * 0.2, 2)          # 20% do LTV
        }
        
        return {
            "ltv": ltv,
            "target_margin": f"{target_margin * 100}%",
            "payback_months": payback_months,
            "recommendations": {
                "max_cpa_for_margin": round(max_cpa_margin, 2),
                "max_cpa_for_payback": round(max_cpa_payback, 2),
                "recommended_cpa": round(recommended_cpa, 2)
            },
            "cpa_ranges": cpa_ranges,
            "scaling_guide": self._generate_scaling_guide(ltv, cpa_ranges)
        }
    
    def suggest_scale_limit(
        self,
        ltv: float,
        current_cpa: float,
        current_spend: float,
        cash_available: float
    ) -> Dict[str, Any]:
        """Sugere limite de escala baseado em LTV e caixa."""
        
        # Margem atual
        margin = (ltv - current_cpa) / ltv if ltv > 0 else 0
        
        # ROI por cliente
        roi_per_customer = ltv - current_cpa
        
        # Clientes que podem ser adquiridos com caixa disponível
        max_customers = cash_available / current_cpa if current_cpa > 0 else 0
        
        # Tempo de payback
        payback_months = current_cpa / (ltv / 12) if ltv > 0 else float('inf')
        
        # Limite de escala seguro (considerando payback)
        if payback_months <= 3:
            scale_multiplier = 3.0  # Pode escalar 3x
            risk_level = "low"
        elif payback_months <= 6:
            scale_multiplier = 2.0  # Pode escalar 2x
            risk_level = "medium"
        elif payback_months <= 12:
            scale_multiplier = 1.5  # Pode escalar 1.5x
            risk_level = "high"
        else:
            scale_multiplier = 1.0  # Não escalar
            risk_level = "critical"
        
        safe_scale_limit = current_spend * scale_multiplier
        max_scale_limit = min(safe_scale_limit, cash_available * 0.7)  # Não usar mais de 70% do caixa
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current_metrics": {
                "ltv": ltv,
                "cpa": current_cpa,
                "margin": f"{margin * 100:.1f}%",
                "roi_per_customer": round(roi_per_customer, 2),
                "payback_months": round(payback_months, 1)
            },
            "scale_recommendation": {
                "safe_scale_limit": round(safe_scale_limit, 2),
                "max_scale_limit": round(max_scale_limit, 2),
                "scale_multiplier": scale_multiplier,
                "risk_level": risk_level,
                "max_customers_affordable": int(max_customers)
            },
            "warnings": self._generate_scale_warnings(margin, payback_months, cash_available, current_spend),
            "action_plan": self._generate_scale_action_plan(risk_level, scale_multiplier)
        }
    
    def suggest_when_to_stop(
        self,
        ltv: float,
        current_cpa: float,
        cpa_trend: List[float],
        budget_remaining: float
    ) -> Dict[str, Any]:
        """Sugere quando parar ou reduzir investimento."""
        
        # Analisar tendência de CPA
        if len(cpa_trend) >= 3:
            cpa_increasing = all(cpa_trend[i] < cpa_trend[i+1] for i in range(len(cpa_trend)-1))
            cpa_change = (cpa_trend[-1] - cpa_trend[0]) / cpa_trend[0] * 100 if cpa_trend[0] > 0 else 0
        else:
            cpa_increasing = False
            cpa_change = 0
        
        # Calcular ponto de break-even
        break_even_cpa = ltv * 0.9  # 90% do LTV como limite
        
        # Determinar ação
        if current_cpa >= ltv:
            action = "STOP"
            reason = "CPA maior que LTV - prejuízo garantido"
            urgency = "immediate"
        elif current_cpa >= break_even_cpa:
            action = "REDUCE"
            reason = "CPA próximo do break-even"
            urgency = "high"
        elif cpa_increasing and cpa_change > 30:
            action = "MONITOR"
            reason = f"CPA subindo {cpa_change:.1f}% - tendência preocupante"
            urgency = "medium"
        else:
            action = "CONTINUE"
            reason = "Métricas saudáveis"
            urgency = "low"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "analysis": {
                "ltv": ltv,
                "current_cpa": current_cpa,
                "break_even_cpa": round(break_even_cpa, 2),
                "cpa_trend": cpa_trend,
                "cpa_change_percent": round(cpa_change, 1),
                "cpa_increasing": cpa_increasing
            },
            "recommendation": {
                "action": action,
                "reason": reason,
                "urgency": urgency
            },
            "thresholds": {
                "stop_at_cpa": round(ltv, 2),
                "reduce_at_cpa": round(break_even_cpa, 2),
                "optimal_cpa": round(ltv * 0.5, 2)
            },
            "next_steps": self._generate_stop_action_steps(action, current_cpa, ltv)
        }
    
    def _calculate_from_historical(self, historical_data: List[Dict], benchmark: Dict) -> Dict:
        """Calcula LTV a partir de dados históricos."""
        total_revenue = sum(d.get("revenue", 0) for d in historical_data)
        total_customers = sum(d.get("customers", 0) for d in historical_data)
        
        if total_customers == 0:
            return self._calculate_from_benchmark(benchmark)
        
        avg_revenue_per_customer = total_revenue / total_customers
        
        # Calcular taxa de recompra real
        repeat_purchases = sum(d.get("repeat_purchases", 0) for d in historical_data)
        repeat_rate = repeat_purchases / total_customers if total_customers > 0 else benchmark["repeat_rate"]
        
        # Projetar LTV
        projected_ltv = avg_revenue_per_customer * (1 + repeat_rate * 2)  # Simplificado
        
        return {
            "method": "historical",
            "ltv_base": round(projected_ltv, 2),
            "avg_revenue_per_customer": round(avg_revenue_per_customer, 2),
            "repeat_rate": round(repeat_rate, 2),
            "data_points": len(historical_data),
            "confidence": "high" if len(historical_data) >= 100 else "medium"
        }
    
    def _calculate_from_customer(self, customer_data: Dict, benchmark: Dict) -> Dict:
        """Calcula LTV a partir de dados de cliente."""
        first_purchase = customer_data.get("first_purchase", benchmark["avg_first_purchase"])
        purchases = customer_data.get("purchases", 1)
        total_spent = customer_data.get("total_spent", first_purchase)
        months_active = customer_data.get("months_active", 1)
        
        # Calcular valor mensal médio
        monthly_value = total_spent / months_active if months_active > 0 else total_spent
        
        # Projetar LTV (12 meses)
        projected_ltv = monthly_value * 12 * (1 - benchmark["churn_rate_monthly"]) ** 6
        
        return {
            "method": "customer",
            "ltv_base": round(projected_ltv, 2),
            "current_value": round(total_spent, 2),
            "monthly_value": round(monthly_value, 2),
            "purchases": purchases,
            "months_active": months_active,
            "confidence": "medium"
        }
    
    def _calculate_from_benchmark(self, benchmark: Dict) -> Dict:
        """Calcula LTV a partir de benchmarks."""
        return {
            "method": "benchmark",
            "ltv_base": benchmark["avg_ltv"],
            "avg_first_purchase": benchmark["avg_first_purchase"],
            "repeat_rate": benchmark["repeat_rate"],
            "avg_purchases": benchmark["avg_purchases"],
            "confidence": "low"
        }
    
    def _calculate_derived_metrics(self, ltv_result: Dict, benchmark: Dict) -> Dict:
        """Calcula métricas derivadas do LTV."""
        ltv = ltv_result.get("ltv_adjusted", ltv_result.get("ltv_base", 0))
        
        return {
            "max_cpa_30_margin": round(ltv * 0.7, 2),
            "max_cpa_50_margin": round(ltv * 0.5, 2),
            "break_even_cpa": round(ltv * 0.9, 2),
            "ideal_cpa_range": {
                "min": round(ltv * 0.2, 2),
                "max": round(ltv * 0.4, 2)
            },
            "expected_roi": round((ltv / (ltv * 0.3) - 1) * 100, 1) if ltv > 0 else 0
        }
    
    def _generate_ltv_recommendations(self, ltv_result: Dict, benchmark: Dict) -> List[Dict]:
        """Gera recomendações baseadas no LTV."""
        recommendations = []
        
        ltv = ltv_result.get("ltv_adjusted", ltv_result.get("ltv_base", 0))
        confidence = ltv_result.get("confidence", "low")
        
        if confidence == "low":
            recommendations.append({
                "priority": "high",
                "action": "Coletar mais dados",
                "reason": "LTV baseado em benchmarks - precisão limitada"
            })
        
        if ltv < benchmark["avg_ltv"] * 0.7:
            recommendations.append({
                "priority": "high",
                "action": "Aumentar LTV",
                "reason": "LTV abaixo do benchmark do nicho",
                "suggestions": ["Implementar upsells", "Melhorar retenção", "Criar programa de fidelidade"]
            })
        
        if ltv_result.get("repeat_rate", 0) < benchmark["repeat_rate"]:
            recommendations.append({
                "priority": "medium",
                "action": "Aumentar recompra",
                "reason": "Taxa de recompra abaixo do esperado",
                "suggestions": ["Email marketing", "Remarketing", "Ofertas exclusivas"]
            })
        
        return recommendations
    
    def _project_future_ltv(self, current_value: float, repeat_rate: float, avg_purchases: float) -> Dict:
        """Projeta LTV futuro."""
        monthly_growth = 1 + (repeat_rate * 0.1)  # Crescimento mensal estimado
        
        return {
            "12_months": current_value * (monthly_growth ** 12),
            "24_months": current_value * (monthly_growth ** 24),
            "lifetime": current_value * avg_purchases * 2  # Estimativa conservadora
        }
    
    def _calculate_customer_quality_score(
        self, 
        avg_spent: float, 
        repeat_rate: float, 
        avg_purchases: float
    ) -> Dict:
        """Calcula score de qualidade do cliente."""
        score = 50  # Base
        
        # Pontuação por gasto
        if avg_spent >= 500:
            score += 20
        elif avg_spent >= 200:
            score += 10
        
        # Pontuação por recompra
        if repeat_rate >= 0.5:
            score += 20
        elif repeat_rate >= 0.3:
            score += 10
        
        # Pontuação por frequência
        if avg_purchases >= 3:
            score += 10
        elif avg_purchases >= 2:
            score += 5
        
        grade = "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D"
        
        return {
            "score": min(100, score),
            "grade": grade,
            "factors": {
                "spending": "high" if avg_spent >= 500 else "medium" if avg_spent >= 200 else "low",
                "loyalty": "high" if repeat_rate >= 0.5 else "medium" if repeat_rate >= 0.3 else "low",
                "frequency": "high" if avg_purchases >= 3 else "medium" if avg_purchases >= 2 else "low"
            }
        }
    
    def _calculate_segment_ltv(self, segment: Dict) -> Dict:
        """Calcula LTV de um segmento."""
        return {
            "segment_id": segment.get("id"),
            "segment_name": segment.get("name"),
            "customer_count": segment.get("customer_count", 0),
            "ltv": segment.get("avg_ltv", 0),
            "characteristics": segment.get("characteristics", {})
        }
    
    def _calculate_ltv_distribution(self, customers: List[Dict]) -> Dict:
        """Calcula distribuição de LTV."""
        ltvs = [c.get("ltv", 0) for c in customers]
        
        if not ltvs:
            return {}
        
        sorted_ltvs = sorted(ltvs)
        n = len(sorted_ltvs)
        
        return {
            "min": round(sorted_ltvs[0], 2),
            "max": round(sorted_ltvs[-1], 2),
            "median": round(sorted_ltvs[n // 2], 2),
            "p25": round(sorted_ltvs[n // 4], 2),
            "p75": round(sorted_ltvs[3 * n // 4], 2),
            "avg": round(sum(ltvs) / n, 2)
        }
    
    def _generate_scaling_guide(self, ltv: float, cpa_ranges: Dict) -> List[Dict]:
        """Gera guia de escala baseado em LTV."""
        return [
            {
                "phase": "Teste",
                "max_cpa": cpa_ranges["safe"],
                "budget": "R$ 50-100/dia",
                "goal": "Validar produto e público"
            },
            {
                "phase": "Validação",
                "max_cpa": cpa_ranges["conservative"],
                "budget": "R$ 100-300/dia",
                "goal": "Confirmar métricas consistentes"
            },
            {
                "phase": "Escala Moderada",
                "max_cpa": cpa_ranges["moderate"],
                "budget": "R$ 300-1000/dia",
                "goal": "Aumentar volume mantendo eficiência"
            },
            {
                "phase": "Escala Agressiva",
                "max_cpa": cpa_ranges["aggressive"],
                "budget": "R$ 1000+/dia",
                "goal": "Maximizar volume com margem reduzida"
            }
        ]
    
    def _generate_scale_warnings(
        self, 
        margin: float, 
        payback_months: float, 
        cash: float, 
        spend: float
    ) -> List[str]:
        """Gera avisos de escala."""
        warnings = []
        
        if margin < 0.2:
            warnings.append("⚠️ Margem muito baixa (<20%) - risco alto")
        
        if payback_months > 6:
            warnings.append("⚠️ Payback longo (>6 meses) - cuidado com fluxo de caixa")
        
        if spend > cash * 0.5:
            warnings.append("⚠️ Gasto alto em relação ao caixa disponível")
        
        return warnings
    
    def _generate_scale_action_plan(self, risk_level: str, multiplier: float) -> List[str]:
        """Gera plano de ação para escala."""
        if risk_level == "low":
            return [
                f"✅ Pode escalar até {multiplier}x com segurança",
                "Aumentar orçamento gradualmente (20% por vez)",
                "Monitorar CPA diariamente",
                "Preparar criativos de reserva"
            ]
        elif risk_level == "medium":
            return [
                f"⚠️ Escalar com cautela até {multiplier}x",
                "Aumentar orçamento 10% por vez",
                "Monitorar CPA a cada 12 horas",
                "Ter plano de contingência pronto"
            ]
        elif risk_level == "high":
            return [
                f"🔴 Escala limitada a {multiplier}x",
                "Focar em otimização antes de escalar",
                "Melhorar LTV ou reduzir CPA primeiro",
                "Considerar pausar e reavaliar"
            ]
        else:
            return [
                "🛑 NÃO ESCALAR",
                "Pausar e analisar problemas",
                "Revisar oferta e público",
                "Só continuar após melhorar métricas"
            ]
    
    def _generate_stop_action_steps(self, action: str, cpa: float, ltv: float) -> List[str]:
        """Gera próximos passos baseado na ação recomendada."""
        if action == "STOP":
            return [
                "1. Pausar campanha imediatamente",
                "2. Analisar por que CPA está tão alto",
                "3. Revisar público-alvo e criativos",
                "4. Considerar mudar oferta ou produto"
            ]
        elif action == "REDUCE":
            return [
                "1. Reduzir orçamento em 50%",
                "2. Pausar anúncios com pior performance",
                "3. Testar novos públicos",
                "4. Otimizar landing page"
            ]
        elif action == "MONITOR":
            return [
                "1. Monitorar métricas a cada 6 horas",
                "2. Preparar plano de contingência",
                "3. Identificar causa do aumento de CPA",
                "4. Testar novos criativos"
            ]
        else:
            return [
                "1. Continuar monitorando normalmente",
                "2. Considerar escalar se métricas mantiverem",
                "3. Testar novos públicos para expansão",
                "4. Documentar estratégia vencedora"
            ]


# Instância global
ltv_engine = LTVEngine()

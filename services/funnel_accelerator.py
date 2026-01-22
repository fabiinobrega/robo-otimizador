"""
FUNNEL ACCELERATOR - Acelerador de Funil Automatizado
Otimizacao automatica de cada etapa do funil de vendas
Nexora Prime V2 - Expansao Unicornio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

class FunnelAccelerator:
    """Acelerador de funil automatizado."""
    
    def __init__(self):
        self.name = "Funnel Accelerator"
        self.version = "2.0.0"
        
        # Etapas padrao do funil
        self.funnel_stages = {
            "awareness": {"name": "Consciencia", "order": 1, "metrics": ["impressions", "reach", "cpm"]},
            "interest": {"name": "Interesse", "order": 2, "metrics": ["clicks", "ctr", "cpc"]},
            "consideration": {"name": "Consideracao", "order": 3, "metrics": ["page_views", "time_on_site", "bounce_rate"]},
            "intent": {"name": "Intencao", "order": 4, "metrics": ["add_to_cart", "initiate_checkout"]},
            "purchase": {"name": "Compra", "order": 5, "metrics": ["conversions", "revenue", "aov"]},
            "loyalty": {"name": "Fidelidade", "order": 6, "metrics": ["repeat_purchases", "ltv", "referrals"]}
        }
        
        # Funis configurados
        self.configured_funnels = {}
        
        # Otimizacoes ativas
        self.active_optimizations = {}
        
        # Historico de acoes
        self.action_history = []
    
    def create_funnel(self, funnel_id: str, config: Dict) -> Dict[str, Any]:
        """Cria um novo funil."""
        
        stages = config.get("stages", list(self.funnel_stages.keys()))
        
        funnel = {
            "id": funnel_id,
            "name": config.get("name", f"Funil {funnel_id}"),
            "created_at": datetime.now().isoformat(),
            "stages": {},
            "status": "active",
            "total_budget": config.get("budget", 0),
            "optimization_mode": config.get("optimization_mode", "balanced")
        }
        
        # Configurar cada etapa
        for stage_key in stages:
            if stage_key in self.funnel_stages:
                stage_config = self.funnel_stages[stage_key].copy()
                stage_config["campaigns"] = []
                stage_config["budget_allocation"] = 0
                stage_config["performance"] = {}
                funnel["stages"][stage_key] = stage_config
        
        self.configured_funnels[funnel_id] = funnel
        
        return {
            "status": "created",
            "funnel_id": funnel_id,
            "funnel": funnel
        }
    
    def analyze_funnel(self, funnel_id: str, metrics_data: Dict) -> Dict[str, Any]:
        """Analisa performance do funil."""
        
        if funnel_id not in self.configured_funnels:
            return {"error": "Funil nao encontrado"}
        
        funnel = self.configured_funnels[funnel_id]
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "funnel_id": funnel_id,
            "stages_analysis": {},
            "bottlenecks": [],
            "opportunities": [],
            "overall_health": "good"
        }
        
        previous_volume = None
        
        for stage_key, stage in funnel["stages"].items():
            stage_metrics = metrics_data.get(stage_key, {})
            
            # Calcular metricas da etapa
            volume = stage_metrics.get("volume", 0)
            conversion_rate = stage_metrics.get("conversion_rate", 0)
            cost = stage_metrics.get("cost", 0)
            
            # Calcular drop-off
            if previous_volume and previous_volume > 0:
                drop_off = ((previous_volume - volume) / previous_volume) * 100
            else:
                drop_off = 0
            
            stage_analysis = {
                "volume": volume,
                "conversion_rate": round(conversion_rate, 2),
                "cost": round(cost, 2),
                "drop_off_rate": round(drop_off, 2),
                "efficiency_score": self._calculate_stage_efficiency(stage_metrics),
                "status": "healthy" if drop_off < 30 else "warning" if drop_off < 50 else "critical"
            }
            
            analysis["stages_analysis"][stage_key] = stage_analysis
            
            # Identificar gargalos
            if drop_off > 40:
                analysis["bottlenecks"].append({
                    "stage": stage_key,
                    "drop_off_rate": round(drop_off, 2),
                    "impact": "high" if drop_off > 60 else "medium",
                    "recommendation": self._get_bottleneck_recommendation(stage_key, drop_off)
                })
            
            previous_volume = volume
        
        # Identificar oportunidades
        analysis["opportunities"] = self._identify_opportunities(analysis["stages_analysis"])
        
        # Calcular saude geral
        critical_stages = sum(1 for s in analysis["stages_analysis"].values() if s["status"] == "critical")
        if critical_stages > 0:
            analysis["overall_health"] = "critical"
        elif any(s["status"] == "warning" for s in analysis["stages_analysis"].values()):
            analysis["overall_health"] = "warning"
        
        return analysis
    
    def optimize_funnel(self, funnel_id: str, optimization_config: Dict = None) -> Dict[str, Any]:
        """Otimiza o funil automaticamente."""
        
        if funnel_id not in self.configured_funnels:
            return {"error": "Funil nao encontrado"}
        
        funnel = self.configured_funnels[funnel_id]
        config = optimization_config or {}
        
        optimizations = []
        
        # Analisar cada etapa
        for stage_key, stage in funnel["stages"].items():
            stage_optimizations = self._generate_stage_optimizations(stage_key, stage, config)
            optimizations.extend(stage_optimizations)
        
        # Priorizar otimizacoes
        optimizations.sort(key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x["priority"], 4))
        
        # Registrar otimizacoes ativas
        self.active_optimizations[funnel_id] = {
            "started_at": datetime.now().isoformat(),
            "optimizations": optimizations,
            "status": "running"
        }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "funnel_id": funnel_id,
            "optimizations_generated": len(optimizations),
            "optimizations": optimizations[:10],  # Top 10
            "estimated_impact": self._estimate_optimization_impact(optimizations)
        }
    
    def allocate_budget(self, funnel_id: str, total_budget: float, strategy: str = "balanced") -> Dict[str, Any]:
        """Aloca orcamento entre etapas do funil."""
        
        if funnel_id not in self.configured_funnels:
            return {"error": "Funil nao encontrado"}
        
        funnel = self.configured_funnels[funnel_id]
        
        # Estrategias de alocacao
        allocation_strategies = {
            "balanced": {"awareness": 0.25, "interest": 0.20, "consideration": 0.20, "intent": 0.15, "purchase": 0.15, "loyalty": 0.05},
            "top_heavy": {"awareness": 0.40, "interest": 0.25, "consideration": 0.15, "intent": 0.10, "purchase": 0.08, "loyalty": 0.02},
            "bottom_heavy": {"awareness": 0.15, "interest": 0.15, "consideration": 0.20, "intent": 0.25, "purchase": 0.20, "loyalty": 0.05},
            "conversion_focused": {"awareness": 0.10, "interest": 0.15, "consideration": 0.25, "intent": 0.30, "purchase": 0.15, "loyalty": 0.05}
        }
        
        strategy_weights = allocation_strategies.get(strategy, allocation_strategies["balanced"])
        
        allocations = {}
        for stage_key in funnel["stages"]:
            weight = strategy_weights.get(stage_key, 0.1)
            allocated = total_budget * weight
            allocations[stage_key] = {
                "budget": round(allocated, 2),
                "percentage": round(weight * 100, 1)
            }
            funnel["stages"][stage_key]["budget_allocation"] = allocated
        
        funnel["total_budget"] = total_budget
        
        return {
            "timestamp": datetime.now().isoformat(),
            "funnel_id": funnel_id,
            "total_budget": total_budget,
            "strategy": strategy,
            "allocations": allocations
        }
    
    def get_stage_recommendations(self, stage: str, current_metrics: Dict) -> Dict[str, Any]:
        """Obtem recomendacoes para uma etapa especifica."""
        
        if stage not in self.funnel_stages:
            return {"error": "Etapa nao encontrada"}
        
        recommendations = []
        
        # Recomendacoes por etapa
        stage_recommendations = {
            "awareness": [
                {"condition": lambda m: m.get("cpm", 0) > 30, "action": "Otimize publicos para reduzir CPM", "priority": "high"},
                {"condition": lambda m: m.get("reach", 0) < 1000, "action": "Aumente orcamento ou amplie publico", "priority": "medium"}
            ],
            "interest": [
                {"condition": lambda m: m.get("ctr", 0) < 1, "action": "Teste novos criativos para aumentar CTR", "priority": "high"},
                {"condition": lambda m: m.get("cpc", 0) > 2, "action": "Refine segmentacao para reduzir CPC", "priority": "medium"}
            ],
            "consideration": [
                {"condition": lambda m: m.get("bounce_rate", 0) > 70, "action": "Melhore a landing page", "priority": "critical"},
                {"condition": lambda m: m.get("time_on_site", 0) < 30, "action": "Adicione conteudo mais engajante", "priority": "high"}
            ],
            "intent": [
                {"condition": lambda m: m.get("cart_abandonment", 0) > 70, "action": "Implemente remarketing de carrinho", "priority": "critical"},
                {"condition": lambda m: m.get("checkout_rate", 0) < 30, "action": "Simplifique processo de checkout", "priority": "high"}
            ],
            "purchase": [
                {"condition": lambda m: m.get("conversion_rate", 0) < 2, "action": "Revise oferta e preco", "priority": "high"},
                {"condition": lambda m: m.get("aov", 0) < 100, "action": "Implemente upsell/cross-sell", "priority": "medium"}
            ],
            "loyalty": [
                {"condition": lambda m: m.get("repeat_rate", 0) < 20, "action": "Crie programa de fidelidade", "priority": "medium"},
                {"condition": lambda m: m.get("referral_rate", 0) < 5, "action": "Implemente programa de indicacao", "priority": "low"}
            ]
        }
        
        for rec in stage_recommendations.get(stage, []):
            if rec["condition"](current_metrics):
                recommendations.append({
                    "action": rec["action"],
                    "priority": rec["priority"],
                    "expected_impact": self._estimate_recommendation_impact(rec["priority"])
                })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "stage": stage,
            "current_metrics": current_metrics,
            "recommendations": recommendations,
            "best_practices": self._get_stage_best_practices(stage)
        }
    
    def simulate_funnel(self, funnel_id: str, scenario: Dict) -> Dict[str, Any]:
        """Simula cenarios do funil."""
        
        if funnel_id not in self.configured_funnels:
            return {"error": "Funil nao encontrado"}
        
        funnel = self.configured_funnels[funnel_id]
        
        # Parametros do cenario
        initial_traffic = scenario.get("traffic", 10000)
        budget = scenario.get("budget", 1000)
        days = scenario.get("days", 30)
        
        # Taxas de conversao por etapa (simuladas)
        conversion_rates = scenario.get("conversion_rates", {
            "awareness_to_interest": 0.10,
            "interest_to_consideration": 0.30,
            "consideration_to_intent": 0.25,
            "intent_to_purchase": 0.20,
            "purchase_to_loyalty": 0.15
        })
        
        # Simular funil
        simulation = {
            "stages": {},
            "daily_projections": []
        }
        
        current_volume = initial_traffic
        total_cost = 0
        total_revenue = 0
        
        stages_order = ["awareness", "interest", "consideration", "intent", "purchase", "loyalty"]
        
        for i, stage in enumerate(stages_order):
            if stage not in funnel["stages"]:
                continue
            
            # Calcular volume na etapa
            if i > 0:
                prev_stage = stages_order[i-1]
                rate_key = f"{prev_stage}_to_{stage}"
                rate = conversion_rates.get(rate_key, 0.2)
                current_volume = int(current_volume * rate)
            
            # Calcular custo e receita
            stage_cost = budget * (funnel["stages"][stage].get("budget_allocation", 0.15) / funnel.get("total_budget", 1) if funnel.get("total_budget", 0) > 0 else 0.15)
            stage_revenue = current_volume * scenario.get("aov", 100) if stage == "purchase" else 0
            
            simulation["stages"][stage] = {
                "volume": current_volume,
                "cost": round(stage_cost, 2),
                "revenue": round(stage_revenue, 2)
            }
            
            total_cost += stage_cost
            total_revenue += stage_revenue
        
        # Projecao diaria
        daily_conversions = simulation["stages"].get("purchase", {}).get("volume", 0) / days
        daily_revenue = total_revenue / days
        daily_cost = total_cost / days
        
        for day in range(1, days + 1):
            simulation["daily_projections"].append({
                "day": day,
                "conversions": round(daily_conversions * (1 + random.uniform(-0.2, 0.2)), 1),
                "revenue": round(daily_revenue * (1 + random.uniform(-0.2, 0.2)), 2),
                "cost": round(daily_cost, 2)
            })
        
        simulation["summary"] = {
            "total_traffic": initial_traffic,
            "total_conversions": simulation["stages"].get("purchase", {}).get("volume", 0),
            "total_cost": round(total_cost, 2),
            "total_revenue": round(total_revenue, 2),
            "roas": round(total_revenue / total_cost, 2) if total_cost > 0 else 0,
            "overall_conversion_rate": round((simulation["stages"].get("purchase", {}).get("volume", 0) / initial_traffic) * 100, 2) if initial_traffic > 0 else 0
        }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "funnel_id": funnel_id,
            "scenario": scenario,
            "simulation": simulation
        }
    
    def get_funnel_report(self, funnel_id: str, period: str = "30d") -> Dict[str, Any]:
        """Gera relatorio do funil."""
        
        if funnel_id not in self.configured_funnels:
            return {"error": "Funil nao encontrado"}
        
        funnel = self.configured_funnels[funnel_id]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "funnel_id": funnel_id,
            "funnel_name": funnel["name"],
            "period": period,
            "summary": {
                "total_stages": len(funnel["stages"]),
                "active_campaigns": sum(len(s.get("campaigns", [])) for s in funnel["stages"].values()),
                "total_budget": funnel.get("total_budget", 0),
                "optimization_mode": funnel.get("optimization_mode", "balanced")
            },
            "stages_summary": {},
            "recommendations": [],
            "next_actions": []
        }
        
        for stage_key, stage in funnel["stages"].items():
            report["stages_summary"][stage_key] = {
                "name": stage["name"],
                "budget_allocation": stage.get("budget_allocation", 0),
                "campaigns_count": len(stage.get("campaigns", []))
            }
        
        # Adicionar recomendacoes gerais
        report["recommendations"] = [
            "Monitore as taxas de conversao entre etapas diariamente",
            "Teste diferentes criativos em cada etapa do funil",
            "Implemente remarketing para usuarios que abandonam o funil"
        ]
        
        report["next_actions"] = [
            {"action": "Revisar performance de cada etapa", "priority": "high"},
            {"action": "Ajustar alocacao de orcamento", "priority": "medium"},
            {"action": "Criar novos criativos para etapas com baixa conversao", "priority": "medium"}
        ]
        
        return report
    
    def _calculate_stage_efficiency(self, metrics: Dict) -> float:
        """Calcula eficiencia de uma etapa."""
        conversion_rate = metrics.get("conversion_rate", 0)
        cost_efficiency = 100 - min(100, metrics.get("cost", 0) / 10)
        
        return round((conversion_rate * 0.6 + cost_efficiency * 0.4), 1)
    
    def _get_bottleneck_recommendation(self, stage: str, drop_off: float) -> str:
        """Obtem recomendacao para gargalo."""
        recommendations = {
            "awareness": "Amplie publico-alvo ou teste novos canais",
            "interest": "Melhore criativos e mensagens",
            "consideration": "Otimize landing page e conteudo",
            "intent": "Simplifique processo e adicione urgencia",
            "purchase": "Revise preco, oferta e checkout",
            "loyalty": "Implemente programa de fidelidade"
        }
        return recommendations.get(stage, "Analise detalhada necessaria")
    
    def _identify_opportunities(self, stages_analysis: Dict) -> List[Dict]:
        """Identifica oportunidades de melhoria."""
        opportunities = []
        
        for stage, analysis in stages_analysis.items():
            if analysis["efficiency_score"] < 50:
                opportunities.append({
                    "stage": stage,
                    "type": "efficiency_improvement",
                    "current_score": analysis["efficiency_score"],
                    "potential_gain": f"{100 - analysis['efficiency_score']}%"
                })
        
        return opportunities
    
    def _generate_stage_optimizations(self, stage_key: str, stage: Dict, config: Dict) -> List[Dict]:
        """Gera otimizacoes para uma etapa."""
        optimizations = []
        
        # Otimizacoes genericas por etapa
        stage_opts = {
            "awareness": [
                {"action": "expand_audience", "description": "Expandir publico-alvo", "priority": "medium"},
                {"action": "test_placements", "description": "Testar novos posicionamentos", "priority": "low"}
            ],
            "interest": [
                {"action": "ab_test_creatives", "description": "Teste A/B de criativos", "priority": "high"},
                {"action": "optimize_copy", "description": "Otimizar textos", "priority": "medium"}
            ],
            "consideration": [
                {"action": "improve_landing", "description": "Melhorar landing page", "priority": "high"},
                {"action": "add_social_proof", "description": "Adicionar prova social", "priority": "medium"}
            ],
            "intent": [
                {"action": "remarketing_setup", "description": "Configurar remarketing", "priority": "critical"},
                {"action": "urgency_elements", "description": "Adicionar elementos de urgencia", "priority": "high"}
            ],
            "purchase": [
                {"action": "checkout_optimization", "description": "Otimizar checkout", "priority": "critical"},
                {"action": "payment_options", "description": "Adicionar opcoes de pagamento", "priority": "high"}
            ],
            "loyalty": [
                {"action": "loyalty_program", "description": "Criar programa de fidelidade", "priority": "medium"},
                {"action": "referral_system", "description": "Sistema de indicacao", "priority": "low"}
            ]
        }
        
        for opt in stage_opts.get(stage_key, []):
            optimizations.append({
                "stage": stage_key,
                **opt
            })
        
        return optimizations
    
    def _estimate_optimization_impact(self, optimizations: List[Dict]) -> Dict[str, Any]:
        """Estima impacto das otimizacoes."""
        critical = sum(1 for o in optimizations if o.get("priority") == "critical")
        high = sum(1 for o in optimizations if o.get("priority") == "high")
        
        potential_improvement = critical * 15 + high * 10
        
        return {
            "potential_conversion_increase": f"{min(100, potential_improvement)}%",
            "estimated_timeline": f"{len(optimizations) * 2} dias",
            "confidence": "high" if critical > 0 else "medium"
        }
    
    def _estimate_recommendation_impact(self, priority: str) -> str:
        """Estima impacto de uma recomendacao."""
        impacts = {
            "critical": "Alto - pode dobrar conversoes",
            "high": "Significativo - 20-50% de melhoria",
            "medium": "Moderado - 10-20% de melhoria",
            "low": "Incremental - 5-10% de melhoria"
        }
        return impacts.get(priority, "A ser avaliado")
    
    def _get_stage_best_practices(self, stage: str) -> List[str]:
        """Obtem melhores praticas para uma etapa."""
        practices = {
            "awareness": [
                "Use videos curtos para maior engajamento",
                "Teste diferentes formatos de anuncio",
                "Segmente por interesses relevantes"
            ],
            "interest": [
                "Destaque beneficios, nao caracteristicas",
                "Use CTAs claros e diretos",
                "Inclua prova social nos anuncios"
            ],
            "consideration": [
                "Landing page deve carregar em menos de 3 segundos",
                "Inclua depoimentos e avaliacoes",
                "Ofereca garantia de satisfacao"
            ],
            "intent": [
                "Implemente exit-intent popups",
                "Ofereca desconto para primeira compra",
                "Use remarketing agressivo"
            ],
            "purchase": [
                "Minimize campos no checkout",
                "Ofereca multiplas opcoes de pagamento",
                "Mostre selos de seguranca"
            ],
            "loyalty": [
                "Envie email de agradecimento pos-compra",
                "Ofereca desconto na proxima compra",
                "Peca avaliacoes e reviews"
            ]
        }
        return practices.get(stage, ["Analise dados e teste constantemente"])


# Instancia global
funnel_accelerator = FunnelAccelerator()

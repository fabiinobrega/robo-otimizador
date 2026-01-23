# services/strategy_laboratory.py
"""
NEXORA PRIME - Laboratório de Estratégias
Sandbox para testar estratégias antes de implementar
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class StrategyLaboratory:
    """Laboratório de estratégias para simulação e teste."""
    
    def __init__(self):
        self.experiments = []
        self.strategy_templates = {}
        self.simulation_results = []
    
    def create_experiment(self, name: str, strategy: Dict, hypothesis: str) -> Dict:
        """Cria um novo experimento de estratégia."""
        experiment = {
            "id": f"EXP_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": name,
            "strategy": strategy,
            "hypothesis": hypothesis,
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "simulations": [],
            "results": None
        }
        self.experiments.append(experiment)
        return experiment
    
    def simulate_strategy(self, experiment_id: str, market_conditions: Dict) -> Dict:
        """Simula uma estratégia em condições de mercado específicas."""
        experiment = self._get_experiment(experiment_id)
        if not experiment:
            return {"error": "Experimento não encontrado"}
        
        strategy = experiment["strategy"]
        
        # Simular resultados
        simulation = {
            "simulation_id": f"SIM_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "market_conditions": market_conditions,
            "simulated_at": datetime.now().isoformat(),
            "results": self._run_simulation(strategy, market_conditions)
        }
        
        experiment["simulations"].append(simulation)
        self.simulation_results.append(simulation)
        
        return simulation
    
    def _run_simulation(self, strategy: Dict, conditions: Dict) -> Dict:
        """Executa a simulação da estratégia."""
        base_budget = strategy.get("budget", 1000)
        base_roas = conditions.get("expected_roas", 2.0)
        market_volatility = conditions.get("volatility", 0.1)
        competition_level = conditions.get("competition", "medium")
        
        # Ajustar baseado em condições
        competition_factor = {"low": 1.2, "medium": 1.0, "high": 0.8}.get(competition_level, 1.0)
        
        # Simular 30 dias
        daily_results = []
        total_spend = 0
        total_revenue = 0
        
        for day in range(30):
            daily_spend = base_budget / 30
            daily_variation = 1 + (hash(f"sim_{day}") % 20 - 10) / 100 * market_volatility
            daily_roas = base_roas * competition_factor * daily_variation
            daily_revenue = daily_spend * daily_roas
            
            total_spend += daily_spend
            total_revenue += daily_revenue
            
            daily_results.append({
                "day": day + 1,
                "spend": round(daily_spend, 2),
                "revenue": round(daily_revenue, 2),
                "roas": round(daily_roas, 2)
            })
        
        return {
            "summary": {
                "total_spend": round(total_spend, 2),
                "total_revenue": round(total_revenue, 2),
                "total_profit": round(total_revenue - total_spend, 2),
                "average_roas": round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
                "roi_percent": round(((total_revenue - total_spend) / total_spend) * 100, 1) if total_spend > 0 else 0
            },
            "daily_results": daily_results,
            "risk_assessment": self._assess_simulation_risk(daily_results),
            "confidence": 0.75
        }
    
    def _assess_simulation_risk(self, daily_results: List[Dict]) -> Dict:
        """Avalia o risco da simulação."""
        roas_values = [d["roas"] for d in daily_results]
        
        min_roas = min(roas_values)
        max_roas = max(roas_values)
        avg_roas = sum(roas_values) / len(roas_values)
        volatility = (max_roas - min_roas) / avg_roas if avg_roas > 0 else 0
        
        days_below_1 = len([r for r in roas_values if r < 1])
        
        risk_level = "low"
        if days_below_1 > 10 or volatility > 0.5:
            risk_level = "high"
        elif days_below_1 > 5 or volatility > 0.3:
            risk_level = "medium"
        
        return {
            "risk_level": risk_level,
            "volatility": round(volatility, 2),
            "days_below_breakeven": days_below_1,
            "min_roas": round(min_roas, 2),
            "max_roas": round(max_roas, 2)
        }
    
    def compare_strategies(self, experiment_ids: List[str]) -> Dict:
        """Compara múltiplas estratégias."""
        comparisons = []
        
        for exp_id in experiment_ids:
            experiment = self._get_experiment(exp_id)
            if experiment and experiment["simulations"]:
                latest_sim = experiment["simulations"][-1]
                comparisons.append({
                    "experiment_id": exp_id,
                    "name": experiment["name"],
                    "results": latest_sim["results"]["summary"],
                    "risk": latest_sim["results"]["risk_assessment"]
                })
        
        if not comparisons:
            return {"error": "Nenhuma simulação encontrada"}
        
        # Ordenar por lucro
        comparisons.sort(key=lambda x: x["results"]["total_profit"], reverse=True)
        
        return {
            "comparisons": comparisons,
            "winner": comparisons[0]["name"],
            "recommendation": f"A estratégia '{comparisons[0]['name']}' apresentou o melhor resultado com lucro de R${comparisons[0]['results']['total_profit']:.2f}"
        }
    
    def approve_experiment(self, experiment_id: str) -> Dict:
        """Aprova um experimento para implementação."""
        experiment = self._get_experiment(experiment_id)
        if not experiment:
            return {"error": "Experimento não encontrado"}
        
        if not experiment["simulations"]:
            return {"error": "Execute pelo menos uma simulação antes de aprovar"}
        
        experiment["status"] = "approved"
        experiment["approved_at"] = datetime.now().isoformat()
        
        return {
            "success": True,
            "experiment_id": experiment_id,
            "status": "approved",
            "message": "Experimento aprovado para implementação"
        }
    
    def _get_experiment(self, experiment_id: str) -> Optional[Dict]:
        """Busca um experimento pelo ID."""
        for exp in self.experiments:
            if exp["id"] == experiment_id:
                return exp
        return None
    
    def get_experiment_history(self, limit: int = 20) -> List[Dict]:
        """Retorna histórico de experimentos."""
        return self.experiments[-limit:]
    
    def get_system_status(self) -> Dict:
        """Retorna o status do laboratório de estratégias."""
        return {
            "total_experiments": len(self.experiments),
            "approved_experiments": len([e for e in self.experiments if e["status"] == "approved"]),
            "total_simulations": len(self.simulation_results)
        }


strategy_laboratory = StrategyLaboratory()

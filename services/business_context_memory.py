# services/business_context_memory.py
"""
NEXORA PRIME - Memória de Contexto de Negócio
Armazena e utiliza contexto de negócio para decisões mais inteligentes
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class BusinessContextMemory:
    """Sistema de memória de contexto de negócio."""
    
    def __init__(self):
        self.business_profiles = {}
        self.financial_context = {}
        self.market_context = {}
        self.historical_performance = {}
        self.seasonal_patterns = {}
        self.competitor_context = {}
    
    def set_business_profile(self, business_id: str, profile: Dict) -> Dict:
        """Define o perfil de negócio."""
        self.business_profiles[business_id] = {
            "profile": profile,
            "updated_at": datetime.now().isoformat()
        }
        
        # Extrair informações financeiras
        if "financial" in profile:
            self.financial_context[business_id] = {
                "profit_margin": profile["financial"].get("profit_margin", 0.3),
                "average_order_value": profile["financial"].get("aov", 100),
                "customer_lifetime_value": profile["financial"].get("ltv", 500),
                "max_cpa": profile["financial"].get("max_cpa", 50),
                "target_roas": profile["financial"].get("target_roas", 3.0),
                "monthly_budget": profile["financial"].get("monthly_budget", 10000),
                "cash_flow_sensitivity": profile["financial"].get("cash_flow_sensitivity", "medium")
            }
        
        return {"success": True, "business_id": business_id}
    
    def get_business_profile(self, business_id: str) -> Optional[Dict]:
        """Retorna o perfil de negócio."""
        return self.business_profiles.get(business_id)
    
    def update_financial_context(self, business_id: str, updates: Dict) -> Dict:
        """Atualiza o contexto financeiro."""
        if business_id not in self.financial_context:
            self.financial_context[business_id] = {}
        
        self.financial_context[business_id].update(updates)
        self.financial_context[business_id]["updated_at"] = datetime.now().isoformat()
        
        return {"success": True, "financial_context": self.financial_context[business_id]}
    
    def get_financial_context(self, business_id: str) -> Dict:
        """Retorna o contexto financeiro."""
        return self.financial_context.get(business_id, {
            "profit_margin": 0.3,
            "average_order_value": 100,
            "customer_lifetime_value": 500,
            "max_cpa": 50,
            "target_roas": 3.0
        })
    
    def record_performance(self, business_id: str, period: str, metrics: Dict) -> Dict:
        """Registra performance histórica."""
        if business_id not in self.historical_performance:
            self.historical_performance[business_id] = []
        
        record = {
            "period": period,
            "metrics": metrics,
            "recorded_at": datetime.now().isoformat()
        }
        
        self.historical_performance[business_id].append(record)
        
        # Detectar padrões sazonais
        self._detect_seasonal_patterns(business_id)
        
        return {"success": True, "record": record}
    
    def get_performance_history(self, business_id: str, periods: int = 12) -> List[Dict]:
        """Retorna histórico de performance."""
        history = self.historical_performance.get(business_id, [])
        return history[-periods:]
    
    def _detect_seasonal_patterns(self, business_id: str):
        """Detecta padrões sazonais nos dados históricos."""
        history = self.historical_performance.get(business_id, [])
        
        if len(history) < 12:
            return
        
        # Análise simplificada de sazonalidade
        monthly_performance = {}
        for record in history:
            period = record["period"]
            if "-" in period:
                month = period.split("-")[1]
                if month not in monthly_performance:
                    monthly_performance[month] = []
                monthly_performance[month].append(record["metrics"].get("revenue", 0))
        
        # Calcular médias mensais
        seasonal_index = {}
        overall_avg = sum(sum(v) for v in monthly_performance.values()) / sum(len(v) for v in monthly_performance.values()) if monthly_performance else 1
        
        for month, values in monthly_performance.items():
            month_avg = sum(values) / len(values)
            seasonal_index[month] = month_avg / overall_avg if overall_avg > 0 else 1
        
        self.seasonal_patterns[business_id] = {
            "monthly_index": seasonal_index,
            "detected_at": datetime.now().isoformat()
        }
    
    def get_seasonal_adjustment(self, business_id: str, month: str) -> float:
        """Retorna ajuste sazonal para um mês."""
        patterns = self.seasonal_patterns.get(business_id, {})
        monthly_index = patterns.get("monthly_index", {})
        return monthly_index.get(month, 1.0)
    
    def set_market_context(self, business_id: str, context: Dict) -> Dict:
        """Define contexto de mercado."""
        self.market_context[business_id] = {
            "industry": context.get("industry", "general"),
            "market_size": context.get("market_size", "medium"),
            "competition_level": context.get("competition_level", "medium"),
            "growth_stage": context.get("growth_stage", "growth"),
            "target_audience": context.get("target_audience", {}),
            "updated_at": datetime.now().isoformat()
        }
        
        return {"success": True, "market_context": self.market_context[business_id]}
    
    def get_market_context(self, business_id: str) -> Dict:
        """Retorna contexto de mercado."""
        return self.market_context.get(business_id, {})
    
    def set_competitor_context(self, business_id: str, competitors: List[Dict]) -> Dict:
        """Define contexto de concorrentes."""
        self.competitor_context[business_id] = {
            "competitors": competitors,
            "updated_at": datetime.now().isoformat()
        }
        
        return {"success": True, "competitors_count": len(competitors)}
    
    def get_competitor_context(self, business_id: str) -> Dict:
        """Retorna contexto de concorrentes."""
        return self.competitor_context.get(business_id, {"competitors": []})
    
    def get_decision_context(self, business_id: str) -> Dict:
        """Retorna contexto completo para tomada de decisão."""
        return {
            "business_profile": self.get_business_profile(business_id),
            "financial_context": self.get_financial_context(business_id),
            "market_context": self.get_market_context(business_id),
            "competitor_context": self.get_competitor_context(business_id),
            "seasonal_patterns": self.seasonal_patterns.get(business_id, {}),
            "recent_performance": self.get_performance_history(business_id, 3)
        }
    
    def calculate_risk_tolerance(self, business_id: str) -> Dict:
        """Calcula tolerância a risco baseada no contexto."""
        financial = self.get_financial_context(business_id)
        
        # Fatores que influenciam tolerância a risco
        cash_flow = financial.get("cash_flow_sensitivity", "medium")
        profit_margin = financial.get("profit_margin", 0.3)
        
        risk_score = 0.5  # Base
        
        if cash_flow == "low":
            risk_score += 0.2
        elif cash_flow == "high":
            risk_score -= 0.2
        
        if profit_margin > 0.4:
            risk_score += 0.1
        elif profit_margin < 0.2:
            risk_score -= 0.1
        
        risk_score = max(0.1, min(0.9, risk_score))
        
        return {
            "risk_tolerance_score": round(risk_score, 2),
            "risk_level": "high" if risk_score > 0.6 else "medium" if risk_score > 0.3 else "low",
            "max_daily_spend_variance": risk_score * 0.5,  # Até 50% de variação
            "recommendation": self._get_risk_recommendation(risk_score)
        }
    
    def _get_risk_recommendation(self, risk_score: float) -> str:
        """Gera recomendação baseada no score de risco."""
        if risk_score > 0.6:
            return "Pode testar estratégias mais agressivas de escala"
        elif risk_score > 0.3:
            return "Manter abordagem equilibrada entre crescimento e segurança"
        else:
            return "Priorizar estabilidade e ROI garantido"
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de memória de contexto."""
        return {
            "total_business_profiles": len(self.business_profiles),
            "total_financial_contexts": len(self.financial_context),
            "total_market_contexts": len(self.market_context),
            "total_performance_records": sum(len(v) for v in self.historical_performance.values()),
            "seasonal_patterns_detected": len(self.seasonal_patterns)
        }


# Instância global
business_context_memory = BusinessContextMemory()

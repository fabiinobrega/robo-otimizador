# services/financial_protection_system.py
"""
NEXORA PRIME - Sistema de Proteção Financeira
Circuit breaker, limites de perda, proteção de orçamento
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


class FinancialProtectionSystem:
    """Sistema de proteção financeira com circuit breaker e limites de perda."""
    
    def __init__(self):
        self.protection_rules = {
            "daily_loss_limit_percent": 20,
            "weekly_loss_limit_percent": 30,
            "monthly_loss_limit_percent": 40,
            "max_single_campaign_spend_percent": 50,
            "min_roas_threshold": 0.5,
            "circuit_breaker_trigger_count": 3,
            "cooling_period_hours": 6
        }
        self.circuit_breakers = {}
        self.spending_history = []
        self.alerts = []
        self.blocked_campaigns = []
    
    def check_spending_limits(self, campaign_id: str, proposed_spend: float, 
                             current_budget: float, account_budget: float) -> Dict:
        """Verifica se um gasto proposto está dentro dos limites."""
        violations = []
        warnings = []
        
        # Verificar limite de campanha individual
        campaign_percent = (proposed_spend / account_budget) * 100 if account_budget > 0 else 0
        if campaign_percent > self.protection_rules["max_single_campaign_spend_percent"]:
            violations.append({
                "type": "single_campaign_limit",
                "message": f"Gasto da campanha ({campaign_percent:.1f}%) excede limite de {self.protection_rules['max_single_campaign_spend_percent']}% do orçamento total"
            })
        
        # Verificar se campanha está bloqueada
        if campaign_id in self.blocked_campaigns:
            violations.append({
                "type": "campaign_blocked",
                "message": "Campanha bloqueada pelo circuit breaker"
            })
        
        # Verificar limites diários
        daily_spend = self._get_period_spend("daily")
        if daily_spend + proposed_spend > account_budget * (self.protection_rules["daily_loss_limit_percent"] / 100):
            warnings.append({
                "type": "daily_limit_warning",
                "message": "Próximo do limite diário de gastos"
            })
        
        return {
            "approved": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "current_daily_spend": daily_spend,
            "remaining_daily_budget": max(0, account_budget * (self.protection_rules["daily_loss_limit_percent"] / 100) - daily_spend)
        }
    
    def check_performance_threshold(self, campaign_id: str, metrics: Dict) -> Dict:
        """Verifica se a performance está acima do threshold mínimo."""
        roas = metrics.get("roas", 0)
        cpa = metrics.get("cpa", float('inf'))
        spend = metrics.get("spend", 0)
        
        issues = []
        
        if roas < self.protection_rules["min_roas_threshold"] and spend > 100:
            issues.append({
                "type": "low_roas",
                "severity": "high",
                "message": f"ROAS de {roas:.2f} está abaixo do mínimo de {self.protection_rules['min_roas_threshold']}"
            })
        
        return {
            "healthy": len(issues) == 0,
            "issues": issues,
            "recommendation": "Pausar campanha" if issues else "Continuar"
        }
    
    def trigger_circuit_breaker(self, campaign_id: str, reason: str) -> Dict:
        """Ativa o circuit breaker para uma campanha."""
        if campaign_id not in self.circuit_breakers:
            self.circuit_breakers[campaign_id] = {
                "trigger_count": 0,
                "triggers": []
            }
        
        self.circuit_breakers[campaign_id]["trigger_count"] += 1
        self.circuit_breakers[campaign_id]["triggers"].append({
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        
        # Verificar se deve bloquear
        if self.circuit_breakers[campaign_id]["trigger_count"] >= self.protection_rules["circuit_breaker_trigger_count"]:
            self.blocked_campaigns.append(campaign_id)
            self._create_alert(
                "CIRCUIT_BREAKER_ACTIVATED",
                f"Campanha {campaign_id} bloqueada após {self.circuit_breakers[campaign_id]['trigger_count']} triggers",
                "critical"
            )
            
            return {
                "status": "blocked",
                "campaign_id": campaign_id,
                "reason": reason,
                "cooling_period_ends": (datetime.now() + timedelta(hours=self.protection_rules["cooling_period_hours"])).isoformat()
            }
        
        return {
            "status": "warning",
            "campaign_id": campaign_id,
            "trigger_count": self.circuit_breakers[campaign_id]["trigger_count"],
            "triggers_until_block": self.protection_rules["circuit_breaker_trigger_count"] - self.circuit_breakers[campaign_id]["trigger_count"]
        }
    
    def reset_circuit_breaker(self, campaign_id: str, user: str = "system") -> Dict:
        """Reseta o circuit breaker de uma campanha."""
        if campaign_id in self.blocked_campaigns:
            self.blocked_campaigns.remove(campaign_id)
        
        if campaign_id in self.circuit_breakers:
            del self.circuit_breakers[campaign_id]
        
        self._create_alert(
            "CIRCUIT_BREAKER_RESET",
            f"Circuit breaker resetado para campanha {campaign_id} por {user}",
            "info"
        )
        
        return {"success": True, "campaign_id": campaign_id}
    
    def record_spending(self, campaign_id: str, amount: float, metrics: Dict) -> Dict:
        """Registra um gasto para tracking."""
        record = {
            "campaign_id": campaign_id,
            "amount": amount,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        self.spending_history.append(record)
        
        # Verificar performance após registro
        performance_check = self.check_performance_threshold(campaign_id, metrics)
        if not performance_check["healthy"]:
            self.trigger_circuit_breaker(campaign_id, performance_check["issues"][0]["message"])
        
        return {"success": True, "record": record}
    
    def get_spending_report(self, period: str = "daily") -> Dict:
        """Gera relatório de gastos por período."""
        total_spend = self._get_period_spend(period)
        
        spend_by_campaign = {}
        for record in self._get_period_records(period):
            cid = record["campaign_id"]
            spend_by_campaign[cid] = spend_by_campaign.get(cid, 0) + record["amount"]
        
        return {
            "period": period,
            "total_spend": total_spend,
            "spend_by_campaign": spend_by_campaign,
            "blocked_campaigns": self.blocked_campaigns,
            "active_circuit_breakers": len(self.circuit_breakers)
        }
    
    def get_protection_status(self) -> Dict:
        """Retorna o status geral do sistema de proteção."""
        return {
            "protection_rules": self.protection_rules,
            "blocked_campaigns_count": len(self.blocked_campaigns),
            "active_circuit_breakers": len(self.circuit_breakers),
            "recent_alerts": self.alerts[-10:] if self.alerts else [],
            "daily_spend": self._get_period_spend("daily"),
            "weekly_spend": self._get_period_spend("weekly")
        }
    
    def update_protection_rules(self, new_rules: Dict) -> Dict:
        """Atualiza as regras de proteção."""
        for key, value in new_rules.items():
            if key in self.protection_rules:
                self.protection_rules[key] = value
        
        return {"success": True, "updated_rules": self.protection_rules}
    
    def _get_period_spend(self, period: str) -> float:
        """Calcula o gasto total de um período."""
        records = self._get_period_records(period)
        return sum(r["amount"] for r in records)
    
    def _get_period_records(self, period: str) -> List[Dict]:
        """Retorna registros de um período específico."""
        now = datetime.now()
        
        if period == "daily":
            cutoff = now - timedelta(days=1)
        elif period == "weekly":
            cutoff = now - timedelta(weeks=1)
        elif period == "monthly":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = now - timedelta(days=1)
        
        return [
            r for r in self.spending_history
            if datetime.fromisoformat(r["timestamp"]) > cutoff
        ]
    
    def _create_alert(self, alert_type: str, message: str, severity: str):
        """Cria um alerta no sistema."""
        self.alerts.append({
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        })


# Instância global
financial_protection = FinancialProtectionSystem()

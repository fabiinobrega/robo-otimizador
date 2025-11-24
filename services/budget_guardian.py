from functools import wraps
"""
Guardião de Orçamento (Budget Guardian) - NEXORA PRIME
Sistema de segurança financeira para proteção de gastos
Nível: Agência Milionária
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple


class BudgetGuardian:
    """
    Guardião de Orçamento - Sistema de segurança financeira
    Protege contra gastos indevidos e requer aprovação para custos
    """
    

def handle_errors(func):
    """Decorador para tratamento automático de erros"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Erro em {func.__name__}: {str(e)}")
            return None
    return wrapper


    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        
        # Limites padrão de segurança
        self.default_limits = {
            "daily_limit": 500.0,
            "weekly_limit": 3000.0,
            "monthly_limit": 10000.0,
            "single_campaign_limit": 1000.0,
            "auto_approval_threshold": 100.0  # Abaixo disso, aprova automaticamente
        }
        
        # Níveis de alerta
        self.alert_levels = {
            "low": 0.5,      # 50% do limite
            "medium": 0.75,  # 75% do limite
            "high": 0.90,    # 90% do limite
            "critical": 0.95 # 95% do limite
        }
    
    def check_budget_approval_required(self, amount: float, 
                                      campaign_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Verifica se aprovação de orçamento é necessária
        
        Args:
            amount: Valor do gasto proposto
            campaign_data: Dados da campanha
        
        Returns:
            Tuple (requires_approval, reason, details)
        """
        current_spending = self._get_current_spending()
        limits = self._get_user_limits()
        
        # Verificar se está abaixo do threshold de aprovação automática
        if amount < limits["auto_approval_threshold"]:
            return (False, "Valor abaixo do threshold de aprovação automática", {
                "amount": amount,
                "threshold": limits["auto_approval_threshold"],
                "auto_approved": True
            })
        
        # Verificar limite diário
        if current_spending["today"] + amount > limits["daily_limit"]:
            return (True, "Limite diário seria excedido", {
                "amount": amount,
                "current_daily": current_spending["today"],
                "daily_limit": limits["daily_limit"],
                "would_exceed_by": (current_spending["today"] + amount) - limits["daily_limit"]
            })
        
        # Verificar limite semanal
        if current_spending["this_week"] + amount > limits["weekly_limit"]:
            return (True, "Limite semanal seria excedido", {
                "amount": amount,
                "current_weekly": current_spending["this_week"],
                "weekly_limit": limits["weekly_limit"],
                "would_exceed_by": (current_spending["this_week"] + amount) - limits["weekly_limit"]
            })
        
        # Verificar limite mensal
        if current_spending["this_month"] + amount > limits["monthly_limit"]:
            return (True, "Limite mensal seria excedido", {
                "amount": amount,
                "current_monthly": current_spending["this_month"],
                "monthly_limit": limits["monthly_limit"],
                "would_exceed_by": (current_spending["this_month"] + amount) - limits["monthly_limit"]
            })
        
        # Verificar limite por campanha
        if amount > limits["single_campaign_limit"]:
            return (True, "Valor excede limite por campanha", {
                "amount": amount,
                "campaign_limit": limits["single_campaign_limit"],
                "exceeds_by": amount - limits["single_campaign_limit"]
            })
        
        # Verificar padrão de gastos suspeito
        if self._detect_suspicious_pattern(amount, campaign_data, current_spending):
            return (True, "Padrão de gastos suspeito detectado", {
                "amount": amount,
                "reason": "Gasto muito acima da média recente"
            })
        
        # Aprovação automática
        return (False, "Dentro dos limites de segurança", {
            "amount": amount,
            "auto_approved": True,
            "remaining_daily": limits["daily_limit"] - current_spending["today"],
            "remaining_weekly": limits["weekly_limit"] - current_spending["this_week"],
            "remaining_monthly": limits["monthly_limit"] - current_spending["this_month"]
        })
    
    def request_approval(self, amount: float, campaign_data: Dict[str, Any], 
                        reason: str) -> Dict[str, Any]:
        """
        Cria solicitação de aprovação de orçamento
        
        Args:
            amount: Valor solicitado
            campaign_data: Dados da campanha
            reason: Motivo da solicitação
        
        Returns:
            Dict com dados da solicitação
        """
        approval_request = {
            "id": f"approval_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "status": "pending",
            "amount": amount,
            "campaign": {
                "id": campaign_data.get("id"),
                "name": campaign_data.get("name"),
                "platform": campaign_data.get("platform"),
                "objective": campaign_data.get("objective")
            },
            "reason": reason,
            "requested_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            
            # Contexto financeiro
            "financial_context": {
                "current_spending": self._get_current_spending(),
                "limits": self._get_user_limits(),
                "utilization": self._calculate_budget_utilization()
            },
            
            # Análise de risco
            "risk_analysis": self._analyze_spending_risk(amount, campaign_data),
            
            # Recomendações
            "recommendations": self._generate_approval_recommendations(amount, campaign_data)
        }
        
        return approval_request
    
    def approve_spending(self, approval_id: str, approved_by: str = "user") -> Dict[str, Any]:
        """Aprova um gasto"""
        return {
            "approval_id": approval_id,
            "status": "approved",
            "approved_by": approved_by,
            "approved_at": datetime.now().isoformat(),
            "can_proceed": True
        }
    
    def reject_spending(self, approval_id: str, reason: str, 
                       rejected_by: str = "user") -> Dict[str, Any]:
        """Rejeita um gasto"""
        return {
            "approval_id": approval_id,
            "status": "rejected",
            "rejected_by": rejected_by,
            "rejected_at": datetime.now().isoformat(),
            "reason": reason,
            "can_proceed": False
        }
    
    def get_spending_alerts(self) -> List[Dict[str, Any]]:
        """Retorna alertas de gastos"""
        alerts = []
        current_spending = self._get_current_spending()
        limits = self._get_user_limits()
        
        # Verificar alerta diário
        daily_utilization = current_spending["today"] / limits["daily_limit"]
        if daily_utilization >= self.alert_levels["high"]:
            alerts.append({
                "level": "high" if daily_utilization < self.alert_levels["critical"] else "critical",
                "type": "daily_limit",
                "message": f"Você já gastou {daily_utilization*100:.1f}% do limite diário",
                "current": current_spending["today"],
                "limit": limits["daily_limit"],
                "utilization": daily_utilization,
                "timestamp": datetime.now().isoformat()
            })
        
        # Verificar alerta semanal
        weekly_utilization = current_spending["this_week"] / limits["weekly_limit"]
        if weekly_utilization >= self.alert_levels["medium"]:
            alerts.append({
                "level": "medium" if weekly_utilization < self.alert_levels["high"] else "high",
                "type": "weekly_limit",
                "message": f"Você já gastou {weekly_utilization*100:.1f}% do limite semanal",
                "current": current_spending["this_week"],
                "limit": limits["weekly_limit"],
                "utilization": weekly_utilization,
                "timestamp": datetime.now().isoformat()
            })
        
        # Verificar alerta mensal
        monthly_utilization = current_spending["this_month"] / limits["monthly_limit"]
        if monthly_utilization >= self.alert_levels["low"]:
            level = "low"
            if monthly_utilization >= self.alert_levels["critical"]:
                level = "critical"
            elif monthly_utilization >= self.alert_levels["high"]:
                level = "high"
            elif monthly_utilization >= self.alert_levels["medium"]:
                level = "medium"
            
            alerts.append({
                "level": level,
                "type": "monthly_limit",
                "message": f"Você já gastou {monthly_utilization*100:.1f}% do limite mensal",
                "current": current_spending["this_month"],
                "limit": limits["monthly_limit"],
                "utilization": monthly_utilization,
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts
    
    def set_budget_limits(self, limits: Dict[str, float]) -> Dict[str, Any]:
        """Define limites de orçamento personalizados"""
        updated_limits = self.default_limits.copy()
        updated_limits.update(limits)
        
        return {
            "success": True,
            "limits": updated_limits,
            "updated_at": datetime.now().isoformat()
        }
    
    def get_budget_report(self) -> Dict[str, Any]:
        """Gera relatório completo de orçamento"""
        current_spending = self._get_current_spending()
        limits = self._get_user_limits()
        utilization = self._calculate_budget_utilization()
        
        report = {
            "period": {
                "today": datetime.now().strftime("%Y-%m-%d"),
                "this_week": f"Semana {datetime.now().isocalendar()[1]}",
                "this_month": datetime.now().strftime("%B %Y")
            },
            
            "spending": current_spending,
            "limits": limits,
            "utilization": utilization,
            
            "remaining": {
                "daily": limits["daily_limit"] - current_spending["today"],
                "weekly": limits["weekly_limit"] - current_spending["this_week"],
                "monthly": limits["monthly_limit"] - current_spending["this_month"]
            },
            
            "alerts": self.get_spending_alerts(),
            
            "recommendations": self._generate_budget_recommendations(
                current_spending, limits, utilization
            ),
            
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def protect_account(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Protege conta contra gastos indevidos"""
        protections = []
        
        # Verificar se campanha tem limite de orçamento
        if not campaign_data.get("budget", {}).get("total"):
            protections.append({
                "type": "missing_budget_cap",
                "severity": "high",
                "message": "Campanha sem limite de orçamento total",
                "recommendation": "Definir limite de orçamento total para evitar gastos ilimitados"
            })
        
        # Verificar se tem data de término
        if not campaign_data.get("end_date"):
            protections.append({
                "type": "missing_end_date",
                "severity": "medium",
                "message": "Campanha sem data de término",
                "recommendation": "Definir data de término para evitar gastos contínuos"
            })
        
        # Verificar se tem regras de otimização
        if not campaign_data.get("optimization", {}).get("auto_rules"):
            protections.append({
                "type": "missing_auto_rules",
                "severity": "medium",
                "message": "Campanha sem regras de otimização automática",
                "recommendation": "Configurar regras para pausar automaticamente se performance for ruim"
            })
        
        # Verificar orçamento diário excessivo
        daily_budget = campaign_data.get("budget", {}).get("daily", 0)
        if daily_budget > self.default_limits["single_campaign_limit"]:
            protections.append({
                "type": "excessive_daily_budget",
                "severity": "high",
                "message": f"Orçamento diário muito alto (R$ {daily_budget})",
                "recommendation": "Reduzir orçamento diário ou solicitar aprovação especial"
            })
        
        return {
            "protected": len(protections) == 0,
            "protections_needed": protections,
            "protection_level": "high" if len(protections) > 2 else "medium" if len(protections) > 0 else "low"
        }
    
    def _get_current_spending(self) -> Dict[str, float]:
        """Retorna gastos atuais (simulado)"""
        # Em produção, buscaria do banco de dados
        return {
            "today": 150.50,
            "this_week": 850.75,
            "this_month": 3250.00,
            "last_30_days": 4100.25
        }
    
    def _get_user_limits(self) -> Dict[str, float]:
        """Retorna limites do usuário"""
        # Em produção, buscaria do banco de dados
        return self.default_limits.copy()
    
    def _calculate_budget_utilization(self) -> Dict[str, float]:
        """Calcula utilização do orçamento"""
        current_spending = self._get_current_spending()
        limits = self._get_user_limits()
        
        return {
            "daily": round((current_spending["today"] / limits["daily_limit"]) * 100, 2),
            "weekly": round((current_spending["this_week"] / limits["weekly_limit"]) * 100, 2),
            "monthly": round((current_spending["this_month"] / limits["monthly_limit"]) * 100, 2)
        }
    
    def _detect_suspicious_pattern(self, amount: float, campaign_data: Dict[str, Any],
                                   current_spending: Dict[str, float]) -> bool:
        """Detecta padrões suspeitos de gastos"""
        # Verificar se gasto é muito acima da média
        avg_daily = current_spending["last_30_days"] / 30
        if amount > avg_daily * 3:
            return True
        
        # Verificar se é um aumento súbito
        if amount > current_spending["today"] * 2:
            return True
        
        return False
    
    def _analyze_spending_risk(self, amount: float, 
                               campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa risco do gasto"""
        risk_score = 0
        risk_factors = []
        
        # Fator 1: Valor alto
        if amount > 500:
            risk_score += 3
            risk_factors.append("Valor alto (> R$ 500)")
        
        # Fator 2: Campanha nova
        if campaign_data.get("status") == "draft":
            risk_score += 2
            risk_factors.append("Campanha nova não testada")
        
        # Fator 3: Sem histórico de performance
        if not campaign_data.get("historical_performance"):
            risk_score += 2
            risk_factors.append("Sem histórico de performance")
        
        # Fator 4: Orçamento sem limite
        if not campaign_data.get("budget", {}).get("total"):
            risk_score += 3
            risk_factors.append("Sem limite de orçamento total")
        
        # Calcular nível de risco
        if risk_score >= 7:
            risk_level = "high"
        elif risk_score >= 4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendation": "Aprovar com cautela" if risk_level == "high" else "Aprovação recomendada"
        }
    
    def _generate_approval_recommendations(self, amount: float,
                                          campaign_data: Dict[str, Any]) -> List[str]:
        """Gera recomendações para aprovação"""
        recommendations = []
        
        if amount > 500:
            recommendations.append("Considere começar com orçamento menor e escalar gradualmente")
        
        if not campaign_data.get("end_date"):
            recommendations.append("Defina uma data de término para a campanha")
        
        if not campaign_data.get("optimization", {}).get("auto_rules"):
            recommendations.append("Configure regras de otimização automática")
        
        recommendations.append("Monitore a performance nas primeiras 48 horas")
        recommendations.append("Pause a campanha se CPA exceder R$ 100")
        
        return recommendations
    
    def _generate_budget_recommendations(self, current_spending: Dict[str, float],
                                        limits: Dict[str, float],
                                        utilization: Dict[str, float]) -> List[str]:
        """Gera recomendações de orçamento"""
        recommendations = []
        
        if utilization["daily"] > 80:
            recommendations.append("⚠️ Você está próximo do limite diário. Considere pausar campanhas de baixa performance.")
        
        if utilization["weekly"] > 75:
            recommendations.append("⚠️ Atenção ao limite semanal. Revise suas campanhas ativas.")
        
        if utilization["monthly"] > 90:
            recommendations.append("🚨 Limite mensal quase atingido! Pause campanhas não essenciais.")
        
        if utilization["monthly"] < 50:
            recommendations.append("✅ Você tem espaço para escalar campanhas de alta performance.")
        
        return recommendations


# Instância global
budget_guardian = BudgetGuardian()

"""
MONETIZATION SYSTEM - Sistema de Monetização Interna
Planos, créditos, faturamento e gestão de assinaturas
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import secrets

class PlanType(Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    UNLIMITED = "unlimited"

class CreditType(Enum):
    AI_GENERATION = "ai_generation"
    API_CALL = "api_call"
    REPORT = "report"
    EXPORT = "export"
    AUTOMATION = "automation"

class MonetizationSystem:
    """Sistema completo de monetização e faturamento."""
    
    def __init__(self):
        self.name = "Monetization System"
        self.version = "2.0.0"
        
        # Definição de planos
        self.plans = {
            PlanType.FREE: {
                "name": "Free",
                "price_monthly": 0,
                "price_yearly": 0,
                "features": {
                    "max_campaigns": 3,
                    "max_ad_accounts": 1,
                    "ai_generations_monthly": 10,
                    "api_calls_monthly": 100,
                    "reports_monthly": 2,
                    "exports_monthly": 5,
                    "automations": 0,
                    "support": "community",
                    "white_label": False,
                    "custom_domain": False,
                    "priority_support": False,
                    "dedicated_manager": False
                },
                "credits_included": {
                    CreditType.AI_GENERATION: 10,
                    CreditType.API_CALL: 100,
                    CreditType.REPORT: 2,
                    CreditType.EXPORT: 5,
                    CreditType.AUTOMATION: 0
                }
            },
            PlanType.STARTER: {
                "name": "Starter",
                "price_monthly": 97,
                "price_yearly": 970,  # 2 meses grátis
                "features": {
                    "max_campaigns": 20,
                    "max_ad_accounts": 3,
                    "ai_generations_monthly": 100,
                    "api_calls_monthly": 1000,
                    "reports_monthly": 10,
                    "exports_monthly": 50,
                    "automations": 5,
                    "support": "email",
                    "white_label": False,
                    "custom_domain": False,
                    "priority_support": False,
                    "dedicated_manager": False
                },
                "credits_included": {
                    CreditType.AI_GENERATION: 100,
                    CreditType.API_CALL: 1000,
                    CreditType.REPORT: 10,
                    CreditType.EXPORT: 50,
                    CreditType.AUTOMATION: 5
                }
            },
            PlanType.PROFESSIONAL: {
                "name": "Professional",
                "price_monthly": 297,
                "price_yearly": 2970,
                "features": {
                    "max_campaigns": 100,
                    "max_ad_accounts": 10,
                    "ai_generations_monthly": 500,
                    "api_calls_monthly": 10000,
                    "reports_monthly": 50,
                    "exports_monthly": 200,
                    "automations": 25,
                    "support": "chat",
                    "white_label": True,
                    "custom_domain": True,
                    "priority_support": True,
                    "dedicated_manager": False
                },
                "credits_included": {
                    CreditType.AI_GENERATION: 500,
                    CreditType.API_CALL: 10000,
                    CreditType.REPORT: 50,
                    CreditType.EXPORT: 200,
                    CreditType.AUTOMATION: 25
                }
            },
            PlanType.ENTERPRISE: {
                "name": "Enterprise",
                "price_monthly": 997,
                "price_yearly": 9970,
                "features": {
                    "max_campaigns": 500,
                    "max_ad_accounts": 50,
                    "ai_generations_monthly": 2000,
                    "api_calls_monthly": 100000,
                    "reports_monthly": 200,
                    "exports_monthly": 1000,
                    "automations": 100,
                    "support": "phone",
                    "white_label": True,
                    "custom_domain": True,
                    "priority_support": True,
                    "dedicated_manager": True
                },
                "credits_included": {
                    CreditType.AI_GENERATION: 2000,
                    CreditType.API_CALL: 100000,
                    CreditType.REPORT: 200,
                    CreditType.EXPORT: 1000,
                    CreditType.AUTOMATION: 100
                }
            },
            PlanType.UNLIMITED: {
                "name": "Unlimited",
                "price_monthly": 2997,
                "price_yearly": 29970,
                "features": {
                    "max_campaigns": -1,  # Ilimitado
                    "max_ad_accounts": -1,
                    "ai_generations_monthly": -1,
                    "api_calls_monthly": -1,
                    "reports_monthly": -1,
                    "exports_monthly": -1,
                    "automations": -1,
                    "support": "dedicated",
                    "white_label": True,
                    "custom_domain": True,
                    "priority_support": True,
                    "dedicated_manager": True
                },
                "credits_included": {
                    CreditType.AI_GENERATION: -1,
                    CreditType.API_CALL: -1,
                    CreditType.REPORT: -1,
                    CreditType.EXPORT: -1,
                    CreditType.AUTOMATION: -1
                }
            }
        }
        
        # Preços de créditos avulsos
        self.credit_prices = {
            CreditType.AI_GENERATION: 0.50,  # Por geração
            CreditType.API_CALL: 0.01,       # Por chamada
            CreditType.REPORT: 2.00,         # Por relatório
            CreditType.EXPORT: 0.50,         # Por exportação
            CreditType.AUTOMATION: 5.00      # Por automação
        }
        
        # Pacotes de créditos
        self.credit_packages = {
            "small": {
                "name": "Pacote Pequeno",
                "price": 47,
                "credits": {
                    CreditType.AI_GENERATION: 50,
                    CreditType.API_CALL: 500,
                    CreditType.REPORT: 5,
                    CreditType.EXPORT: 25
                }
            },
            "medium": {
                "name": "Pacote Médio",
                "price": 147,
                "credits": {
                    CreditType.AI_GENERATION: 200,
                    CreditType.API_CALL: 2000,
                    CreditType.REPORT: 20,
                    CreditType.EXPORT: 100
                }
            },
            "large": {
                "name": "Pacote Grande",
                "price": 397,
                "credits": {
                    CreditType.AI_GENERATION: 600,
                    CreditType.API_CALL: 6000,
                    CreditType.REPORT: 60,
                    CreditType.EXPORT: 300
                }
            }
        }
        
        # Armazenamento de dados
        self.subscriptions = {}
        self.credit_balances = {}
        self.transactions = {}
        self.invoices = {}
    
    def create_subscription(
        self, 
        user_id: str, 
        plan: str,
        billing_cycle: str = "monthly"
    ) -> Dict[str, Any]:
        """Cria uma nova assinatura."""
        
        try:
            plan_type = PlanType(plan)
        except:
            return {"error": f"Plano inválido: {plan}"}
        
        plan_details = self.plans[plan_type]
        
        subscription_id = f"sub_{secrets.token_hex(8)}"
        
        # Calcular preço
        if billing_cycle == "yearly":
            price = plan_details["price_yearly"]
            next_billing = datetime.now() + timedelta(days=365)
        else:
            price = plan_details["price_monthly"]
            next_billing = datetime.now() + timedelta(days=30)
        
        subscription = {
            "id": subscription_id,
            "user_id": user_id,
            "plan": plan,
            "plan_name": plan_details["name"],
            "billing_cycle": billing_cycle,
            "price": price,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "current_period_start": datetime.now().isoformat(),
            "current_period_end": next_billing.isoformat(),
            "next_billing_date": next_billing.isoformat(),
            "features": plan_details["features"],
            "cancel_at_period_end": False
        }
        
        self.subscriptions[subscription_id] = subscription
        
        # Inicializar créditos
        self._initialize_credits(user_id, plan_type)
        
        # Criar invoice
        invoice = self._create_invoice(user_id, subscription_id, price, f"Assinatura {plan_details['name']}")
        
        return {
            "subscription_id": subscription_id,
            "subscription": subscription,
            "invoice": invoice,
            "message": "Assinatura criada com sucesso"
        }
    
    def upgrade_subscription(
        self, 
        subscription_id: str, 
        new_plan: str
    ) -> Dict[str, Any]:
        """Faz upgrade de uma assinatura."""
        
        if subscription_id not in self.subscriptions:
            return {"error": "Assinatura não encontrada"}
        
        subscription = self.subscriptions[subscription_id]
        current_plan = subscription["plan"]
        
        try:
            new_plan_type = PlanType(new_plan)
            current_plan_type = PlanType(current_plan)
        except:
            return {"error": "Plano inválido"}
        
        # Verificar se é upgrade
        plan_order = [PlanType.FREE, PlanType.STARTER, PlanType.PROFESSIONAL, PlanType.ENTERPRISE, PlanType.UNLIMITED]
        if plan_order.index(new_plan_type) <= plan_order.index(current_plan_type):
            return {"error": "Novo plano deve ser superior ao atual"}
        
        new_plan_details = self.plans[new_plan_type]
        old_plan_details = self.plans[current_plan_type]
        
        # Calcular prorata
        days_remaining = (
            datetime.fromisoformat(subscription["current_period_end"]) - datetime.now()
        ).days
        
        if subscription["billing_cycle"] == "yearly":
            old_daily_rate = old_plan_details["price_yearly"] / 365
            new_daily_rate = new_plan_details["price_yearly"] / 365
        else:
            old_daily_rate = old_plan_details["price_monthly"] / 30
            new_daily_rate = new_plan_details["price_monthly"] / 30
        
        credit_remaining = old_daily_rate * days_remaining
        new_cost = new_daily_rate * days_remaining
        prorated_amount = max(0, new_cost - credit_remaining)
        
        # Atualizar assinatura
        subscription["plan"] = new_plan
        subscription["plan_name"] = new_plan_details["name"]
        subscription["features"] = new_plan_details["features"]
        
        if subscription["billing_cycle"] == "yearly":
            subscription["price"] = new_plan_details["price_yearly"]
        else:
            subscription["price"] = new_plan_details["price_monthly"]
        
        # Atualizar créditos
        self._upgrade_credits(subscription["user_id"], new_plan_type)
        
        # Criar invoice do upgrade
        if prorated_amount > 0:
            invoice = self._create_invoice(
                subscription["user_id"],
                subscription_id,
                prorated_amount,
                f"Upgrade para {new_plan_details['name']} (prorata)"
            )
        else:
            invoice = None
        
        return {
            "subscription_id": subscription_id,
            "old_plan": current_plan,
            "new_plan": new_plan,
            "prorated_amount": round(prorated_amount, 2),
            "credit_applied": round(credit_remaining, 2),
            "invoice": invoice,
            "message": "Upgrade realizado com sucesso"
        }
    
    def cancel_subscription(
        self, 
        subscription_id: str, 
        immediate: bool = False
    ) -> Dict[str, Any]:
        """Cancela uma assinatura."""
        
        if subscription_id not in self.subscriptions:
            return {"error": "Assinatura não encontrada"}
        
        subscription = self.subscriptions[subscription_id]
        
        if immediate:
            subscription["status"] = "cancelled"
            subscription["cancelled_at"] = datetime.now().isoformat()
        else:
            subscription["cancel_at_period_end"] = True
        
        return {
            "subscription_id": subscription_id,
            "status": subscription["status"],
            "cancel_at_period_end": subscription["cancel_at_period_end"],
            "access_until": subscription["current_period_end"],
            "message": "Assinatura cancelada" if immediate else "Assinatura será cancelada no fim do período"
        }
    
    def get_subscription_status(self, user_id: str) -> Dict[str, Any]:
        """Obtém status da assinatura de um usuário."""
        
        # Buscar assinatura ativa do usuário
        user_subscription = None
        for sub in self.subscriptions.values():
            if sub["user_id"] == user_id and sub["status"] == "active":
                user_subscription = sub
                break
        
        if not user_subscription:
            return {
                "has_subscription": False,
                "plan": "free",
                "features": self.plans[PlanType.FREE]["features"]
            }
        
        # Calcular dias restantes
        period_end = datetime.fromisoformat(user_subscription["current_period_end"])
        days_remaining = (period_end - datetime.now()).days
        
        return {
            "has_subscription": True,
            "subscription_id": user_subscription["id"],
            "plan": user_subscription["plan"],
            "plan_name": user_subscription["plan_name"],
            "status": user_subscription["status"],
            "billing_cycle": user_subscription["billing_cycle"],
            "price": user_subscription["price"],
            "days_remaining": max(0, days_remaining),
            "next_billing_date": user_subscription["next_billing_date"],
            "cancel_at_period_end": user_subscription["cancel_at_period_end"],
            "features": user_subscription["features"]
        }
    
    def get_credit_balance(self, user_id: str) -> Dict[str, Any]:
        """Obtém saldo de créditos de um usuário."""
        
        if user_id not in self.credit_balances:
            # Inicializar com créditos do plano free
            self._initialize_credits(user_id, PlanType.FREE)
        
        balance = self.credit_balances[user_id]
        
        return {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "balances": {
                credit_type.value: {
                    "available": balance.get(credit_type, {}).get("available", 0),
                    "used_this_period": balance.get(credit_type, {}).get("used", 0),
                    "limit": balance.get(credit_type, {}).get("limit", 0)
                }
                for credit_type in CreditType
            },
            "reset_date": balance.get("reset_date", (datetime.now() + timedelta(days=30)).isoformat())
        }
    
    def consume_credits(
        self, 
        user_id: str, 
        credit_type: str, 
        amount: int = 1
    ) -> Dict[str, Any]:
        """Consome créditos de um usuário."""
        
        try:
            credit_type_enum = CreditType(credit_type)
        except:
            return {"error": f"Tipo de crédito inválido: {credit_type}"}
        
        if user_id not in self.credit_balances:
            self._initialize_credits(user_id, PlanType.FREE)
        
        balance = self.credit_balances[user_id]
        credit_balance = balance.get(credit_type_enum, {"available": 0, "used": 0, "limit": 0})
        
        # Verificar se é ilimitado
        if credit_balance["limit"] == -1:
            credit_balance["used"] += amount
            return {
                "success": True,
                "consumed": amount,
                "remaining": -1,  # Ilimitado
                "message": "Créditos consumidos (plano ilimitado)"
            }
        
        # Verificar saldo
        if credit_balance["available"] < amount:
            return {
                "success": False,
                "error": "Créditos insuficientes",
                "available": credit_balance["available"],
                "required": amount,
                "suggestion": "Compre mais créditos ou faça upgrade do plano"
            }
        
        # Consumir
        credit_balance["available"] -= amount
        credit_balance["used"] += amount
        balance[credit_type_enum] = credit_balance
        
        return {
            "success": True,
            "consumed": amount,
            "remaining": credit_balance["available"],
            "message": "Créditos consumidos com sucesso"
        }
    
    def purchase_credits(
        self, 
        user_id: str, 
        package: str = None,
        custom_credits: Dict = None
    ) -> Dict[str, Any]:
        """Compra créditos avulsos."""
        
        if package:
            if package not in self.credit_packages:
                return {"error": f"Pacote inválido: {package}"}
            
            pkg = self.credit_packages[package]
            price = pkg["price"]
            credits_to_add = pkg["credits"]
        elif custom_credits:
            # Calcular preço de créditos customizados
            price = 0
            credits_to_add = {}
            for credit_type, amount in custom_credits.items():
                try:
                    ct = CreditType(credit_type)
                    price += self.credit_prices[ct] * amount
                    credits_to_add[ct] = amount
                except:
                    return {"error": f"Tipo de crédito inválido: {credit_type}"}
        else:
            return {"error": "Especifique um pacote ou créditos customizados"}
        
        # Adicionar créditos
        if user_id not in self.credit_balances:
            self._initialize_credits(user_id, PlanType.FREE)
        
        balance = self.credit_balances[user_id]
        
        for credit_type, amount in credits_to_add.items():
            if credit_type not in balance:
                balance[credit_type] = {"available": 0, "used": 0, "limit": 0}
            balance[credit_type]["available"] += amount
        
        # Criar invoice
        invoice = self._create_invoice(
            user_id,
            None,
            price,
            f"Compra de créditos - {package or 'customizado'}"
        )
        
        return {
            "success": True,
            "credits_added": {k.value if isinstance(k, CreditType) else k: v for k, v in credits_to_add.items()},
            "total_price": round(price, 2),
            "invoice": invoice,
            "message": "Créditos adicionados com sucesso"
        }
    
    def get_usage_report(
        self, 
        user_id: str, 
        period: str = "current"
    ) -> Dict[str, Any]:
        """Obtém relatório de uso."""
        
        balance = self.credit_balances.get(user_id, {})
        subscription = self.get_subscription_status(user_id)
        
        usage = {}
        for credit_type in CreditType:
            credit_data = balance.get(credit_type, {"available": 0, "used": 0, "limit": 0})
            limit = credit_data["limit"]
            used = credit_data["used"]
            
            if limit == -1:
                percentage = 0  # Ilimitado
            elif limit > 0:
                percentage = round((used / limit) * 100, 1)
            else:
                percentage = 100 if used > 0 else 0
            
            usage[credit_type.value] = {
                "used": used,
                "limit": limit if limit != -1 else "Ilimitado",
                "available": credit_data["available"] if limit != -1 else "Ilimitado",
                "percentage_used": percentage
            }
        
        return {
            "user_id": user_id,
            "period": period,
            "timestamp": datetime.now().isoformat(),
            "plan": subscription.get("plan", "free"),
            "usage": usage,
            "alerts": self._generate_usage_alerts(usage),
            "recommendations": self._generate_usage_recommendations(usage, subscription.get("plan", "free"))
        }
    
    def get_invoices(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Obtém faturas de um usuário."""
        
        user_invoices = [
            inv for inv in self.invoices.values()
            if inv["user_id"] == user_id
        ]
        
        # Ordenar por data (mais recente primeiro)
        user_invoices.sort(key=lambda x: x["created_at"], reverse=True)
        
        return user_invoices[:limit]
    
    def compare_plans(self) -> Dict[str, Any]:
        """Compara todos os planos disponíveis."""
        
        comparison = {
            "plans": [],
            "features_list": [
                "max_campaigns",
                "max_ad_accounts",
                "ai_generations_monthly",
                "api_calls_monthly",
                "reports_monthly",
                "exports_monthly",
                "automations",
                "support",
                "white_label",
                "custom_domain",
                "priority_support",
                "dedicated_manager"
            ]
        }
        
        for plan_type, plan_details in self.plans.items():
            comparison["plans"].append({
                "id": plan_type.value,
                "name": plan_details["name"],
                "price_monthly": plan_details["price_monthly"],
                "price_yearly": plan_details["price_yearly"],
                "yearly_savings": (plan_details["price_monthly"] * 12) - plan_details["price_yearly"],
                "features": plan_details["features"]
            })
        
        return comparison
    
    def _initialize_credits(self, user_id: str, plan_type: PlanType):
        """Inicializa créditos para um usuário."""
        
        plan_credits = self.plans[plan_type]["credits_included"]
        
        self.credit_balances[user_id] = {
            credit_type: {
                "available": amount,
                "used": 0,
                "limit": amount
            }
            for credit_type, amount in plan_credits.items()
        }
        
        self.credit_balances[user_id]["reset_date"] = (
            datetime.now() + timedelta(days=30)
        ).isoformat()
    
    def _upgrade_credits(self, user_id: str, new_plan_type: PlanType):
        """Atualiza créditos após upgrade."""
        
        new_credits = self.plans[new_plan_type]["credits_included"]
        
        if user_id not in self.credit_balances:
            self._initialize_credits(user_id, new_plan_type)
            return
        
        balance = self.credit_balances[user_id]
        
        for credit_type, new_limit in new_credits.items():
            if credit_type not in balance:
                balance[credit_type] = {"available": 0, "used": 0, "limit": 0}
            
            old_limit = balance[credit_type]["limit"]
            
            # Adicionar diferença de créditos
            if new_limit == -1:
                balance[credit_type]["limit"] = -1
                balance[credit_type]["available"] = -1
            elif old_limit != -1:
                additional = max(0, new_limit - old_limit)
                balance[credit_type]["available"] += additional
                balance[credit_type]["limit"] = new_limit
    
    def _create_invoice(
        self, 
        user_id: str, 
        subscription_id: str, 
        amount: float,
        description: str
    ) -> Dict:
        """Cria uma fatura."""
        
        invoice_id = f"inv_{secrets.token_hex(8)}"
        
        invoice = {
            "id": invoice_id,
            "user_id": user_id,
            "subscription_id": subscription_id,
            "amount": round(amount, 2),
            "currency": "BRL",
            "description": description,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "paid_at": None
        }
        
        self.invoices[invoice_id] = invoice
        
        return invoice
    
    def _generate_usage_alerts(self, usage: Dict) -> List[Dict]:
        """Gera alertas de uso."""
        
        alerts = []
        
        for credit_type, data in usage.items():
            if data["limit"] == "Ilimitado":
                continue
            
            percentage = data["percentage_used"]
            
            if percentage >= 90:
                alerts.append({
                    "type": "critical",
                    "credit_type": credit_type,
                    "message": f"Créditos de {credit_type} quase esgotados ({percentage}% usado)"
                })
            elif percentage >= 75:
                alerts.append({
                    "type": "warning",
                    "credit_type": credit_type,
                    "message": f"Créditos de {credit_type} em {percentage}% de uso"
                })
        
        return alerts
    
    def _generate_usage_recommendations(self, usage: Dict, current_plan: str) -> List[str]:
        """Gera recomendações baseadas no uso."""
        
        recommendations = []
        
        high_usage_types = []
        for credit_type, data in usage.items():
            if data["limit"] != "Ilimitado" and data["percentage_used"] >= 80:
                high_usage_types.append(credit_type)
        
        if len(high_usage_types) >= 2:
            recommendations.append(
                "Considere fazer upgrade do plano para ter mais créditos inclusos"
            )
        elif len(high_usage_types) == 1:
            recommendations.append(
                f"Considere comprar créditos avulsos de {high_usage_types[0]}"
            )
        
        if current_plan == "free":
            recommendations.append(
                "Upgrade para o plano Starter para 10x mais créditos"
            )
        
        return recommendations


# Instância global
monetization_system = MonetizationSystem()

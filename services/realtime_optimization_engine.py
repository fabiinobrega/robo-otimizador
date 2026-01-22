"""
REAL-TIME OPTIMIZATION ENGINE - Motor de Otimização em Tempo Real
Sistema de ajustes automáticos de campanhas em tempo real
Versão: 1.0 - Expansão Avançada
"""

import os
import json
import asyncio
import logging
import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OptimizationAction(Enum):
    """Tipos de ações de otimização"""
    INCREASE_BID = "increase_bid"
    DECREASE_BID = "decrease_bid"
    PAUSE_AD = "pause_ad"
    RESUME_AD = "resume_ad"
    INCREASE_BUDGET = "increase_budget"
    DECREASE_BUDGET = "decrease_budget"
    ADJUST_TARGETING = "adjust_targeting"
    ROTATE_CREATIVE = "rotate_creative"
    SCALE_CAMPAIGN = "scale_campaign"
    PAUSE_CAMPAIGN = "pause_campaign"


class TriggerCondition(Enum):
    """Condições de gatilho para otimização"""
    CPA_ABOVE_TARGET = "cpa_above_target"
    CPA_BELOW_TARGET = "cpa_below_target"
    ROAS_BELOW_TARGET = "roas_below_target"
    ROAS_ABOVE_TARGET = "roas_above_target"
    CTR_DROP = "ctr_drop"
    CTR_SPIKE = "ctr_spike"
    BUDGET_DEPLETING = "budget_depleting"
    HIGH_FREQUENCY = "high_frequency"
    LOW_IMPRESSIONS = "low_impressions"
    CONVERSION_SPIKE = "conversion_spike"


@dataclass
class OptimizationRule:
    """Regra de otimização automática"""
    id: str
    name: str
    condition: TriggerCondition
    threshold: float
    action: OptimizationAction
    action_value: float
    cooldown_minutes: int = 60
    is_active: bool = True
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0
    
    def can_trigger(self) -> bool:
        """Verifica se a regra pode ser acionada"""
        if not self.is_active:
            return False
        if self.last_triggered is None:
            return True
        return datetime.now() - self.last_triggered > timedelta(minutes=self.cooldown_minutes)


@dataclass
class OptimizationEvent:
    """Evento de otimização executado"""
    id: str
    rule_id: str
    campaign_id: str
    action: OptimizationAction
    old_value: float
    new_value: float
    reason: str
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "campaign_id": self.campaign_id,
            "action": self.action.value,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success
        }


@dataclass
class CampaignMetrics:
    """Métricas de campanha em tempo real"""
    campaign_id: str
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    spend: float = 0.0
    revenue: float = 0.0
    ctr: float = 0.0
    cpc: float = 0.0
    cpa: float = 0.0
    roas: float = 0.0
    frequency: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def calculate_derived_metrics(self):
        """Calcula métricas derivadas"""
        self.ctr = (self.clicks / self.impressions * 100) if self.impressions > 0 else 0
        self.cpc = (self.spend / self.clicks) if self.clicks > 0 else 0
        self.cpa = (self.spend / self.conversions) if self.conversions > 0 else 0
        self.roas = (self.revenue / self.spend) if self.spend > 0 else 0


class MetricsBuffer:
    """Buffer de métricas para análise em tempo real"""
    
    def __init__(self, max_size: int = 1000):
        self.buffer: Dict[str, deque] = {}
        self.max_size = max_size
        
    def add_metrics(self, campaign_id: str, metrics: CampaignMetrics):
        """Adiciona métricas ao buffer"""
        if campaign_id not in self.buffer:
            self.buffer[campaign_id] = deque(maxlen=self.max_size)
        self.buffer[campaign_id].append(metrics)
        
    def get_recent_metrics(self, campaign_id: str, minutes: int = 60) -> List[CampaignMetrics]:
        """Obtém métricas recentes"""
        if campaign_id not in self.buffer:
            return []
            
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [m for m in self.buffer[campaign_id] if m.timestamp > cutoff]
    
    def get_average_metrics(self, campaign_id: str, minutes: int = 60) -> Optional[Dict[str, float]]:
        """Calcula média das métricas recentes"""
        recent = self.get_recent_metrics(campaign_id, minutes)
        
        if not recent:
            return None
            
        return {
            "avg_ctr": sum(m.ctr for m in recent) / len(recent),
            "avg_cpc": sum(m.cpc for m in recent) / len(recent),
            "avg_cpa": sum(m.cpa for m in recent) / len(recent),
            "avg_roas": sum(m.roas for m in recent) / len(recent),
            "total_spend": sum(m.spend for m in recent),
            "total_conversions": sum(m.conversions for m in recent),
            "data_points": len(recent)
        }


class RuleEngine:
    """Motor de regras de otimização"""
    
    def __init__(self):
        self.rules: Dict[str, OptimizationRule] = {}
        self._initialize_default_rules()
        
    def _initialize_default_rules(self):
        """Inicializa regras padrão"""
        default_rules = [
            OptimizationRule(
                id="rule_cpa_high",
                name="CPA Alto - Reduzir Lance",
                condition=TriggerCondition.CPA_ABOVE_TARGET,
                threshold=1.3,  # 30% acima do target
                action=OptimizationAction.DECREASE_BID,
                action_value=0.15,  # Reduzir 15%
                cooldown_minutes=30
            ),
            OptimizationRule(
                id="rule_roas_low",
                name="ROAS Baixo - Pausar Anúncio",
                condition=TriggerCondition.ROAS_BELOW_TARGET,
                threshold=0.5,  # 50% do target
                action=OptimizationAction.PAUSE_AD,
                action_value=0,
                cooldown_minutes=120
            ),
            OptimizationRule(
                id="rule_roas_high",
                name="ROAS Alto - Escalar Campanha",
                condition=TriggerCondition.ROAS_ABOVE_TARGET,
                threshold=1.5,  # 50% acima do target
                action=OptimizationAction.INCREASE_BUDGET,
                action_value=0.20,  # Aumentar 20%
                cooldown_minutes=60
            ),
            OptimizationRule(
                id="rule_ctr_drop",
                name="Queda de CTR - Rotacionar Criativo",
                condition=TriggerCondition.CTR_DROP,
                threshold=0.3,  # Queda de 30%
                action=OptimizationAction.ROTATE_CREATIVE,
                action_value=0,
                cooldown_minutes=240
            ),
            OptimizationRule(
                id="rule_budget_depleting",
                name="Orçamento Esgotando - Ajustar",
                condition=TriggerCondition.BUDGET_DEPLETING,
                threshold=0.9,  # 90% gasto
                action=OptimizationAction.DECREASE_BID,
                action_value=0.10,
                cooldown_minutes=60
            ),
            OptimizationRule(
                id="rule_high_frequency",
                name="Frequência Alta - Expandir Público",
                condition=TriggerCondition.HIGH_FREQUENCY,
                threshold=4.0,  # Frequência > 4
                action=OptimizationAction.ADJUST_TARGETING,
                action_value=0,
                cooldown_minutes=180
            ),
            OptimizationRule(
                id="rule_conversion_spike",
                name="Pico de Conversões - Escalar",
                condition=TriggerCondition.CONVERSION_SPIKE,
                threshold=2.0,  # 2x a média
                action=OptimizationAction.SCALE_CAMPAIGN,
                action_value=0.30,  # Escalar 30%
                cooldown_minutes=120
            )
        ]
        
        for rule in default_rules:
            self.rules[rule.id] = rule
            
    def add_rule(self, rule: OptimizationRule):
        """Adiciona nova regra"""
        self.rules[rule.id] = rule
        
    def remove_rule(self, rule_id: str):
        """Remove regra"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            
    def evaluate_rules(
        self,
        campaign_id: str,
        current_metrics: CampaignMetrics,
        targets: Dict[str, float]
    ) -> List[OptimizationRule]:
        """Avalia quais regras devem ser acionadas"""
        triggered_rules = []
        
        for rule in self.rules.values():
            if not rule.can_trigger():
                continue
                
            should_trigger = False
            
            if rule.condition == TriggerCondition.CPA_ABOVE_TARGET:
                target_cpa = targets.get("cpa", 20)
                should_trigger = current_metrics.cpa > target_cpa * rule.threshold
                
            elif rule.condition == TriggerCondition.CPA_BELOW_TARGET:
                target_cpa = targets.get("cpa", 20)
                should_trigger = current_metrics.cpa < target_cpa * (2 - rule.threshold)
                
            elif rule.condition == TriggerCondition.ROAS_BELOW_TARGET:
                target_roas = targets.get("roas", 3)
                should_trigger = current_metrics.roas < target_roas * rule.threshold
                
            elif rule.condition == TriggerCondition.ROAS_ABOVE_TARGET:
                target_roas = targets.get("roas", 3)
                should_trigger = current_metrics.roas > target_roas * rule.threshold
                
            elif rule.condition == TriggerCondition.HIGH_FREQUENCY:
                should_trigger = current_metrics.frequency > rule.threshold
                
            elif rule.condition == TriggerCondition.BUDGET_DEPLETING:
                budget = targets.get("daily_budget", 100)
                should_trigger = current_metrics.spend > budget * rule.threshold
                
            if should_trigger:
                triggered_rules.append(rule)
                
        return triggered_rules


class RealtimeOptimizationEngine:
    """
    Motor principal de Otimização em Tempo Real
    Monitora e otimiza campanhas automaticamente
    """
    
    def __init__(self):
        self.metrics_buffer = MetricsBuffer()
        self.rule_engine = RuleEngine()
        self.optimization_events: List[OptimizationEvent] = []
        self.campaign_targets: Dict[str, Dict[str, float]] = {}
        self.is_running = False
        self.optimization_interval = 60  # segundos
        self._lock = threading.Lock()
        
    async def start(self):
        """Inicia o motor de otimização"""
        self.is_running = True
        logger.info("Real-Time Optimization Engine iniciado")
        
    async def stop(self):
        """Para o motor de otimização"""
        self.is_running = False
        logger.info("Real-Time Optimization Engine parado")
        
    def set_campaign_targets(self, campaign_id: str, targets: Dict[str, float]):
        """Define targets para uma campanha"""
        self.campaign_targets[campaign_id] = targets
        
    def ingest_metrics(self, campaign_id: str, metrics_data: Dict[str, Any]):
        """Ingere métricas de campanha"""
        metrics = CampaignMetrics(
            campaign_id=campaign_id,
            impressions=metrics_data.get("impressions", 0),
            clicks=metrics_data.get("clicks", 0),
            conversions=metrics_data.get("conversions", 0),
            spend=metrics_data.get("spend", 0),
            revenue=metrics_data.get("revenue", 0),
            frequency=metrics_data.get("frequency", 0)
        )
        metrics.calculate_derived_metrics()
        
        self.metrics_buffer.add_metrics(campaign_id, metrics)
        
        # Avaliar regras automaticamente
        if self.is_running:
            self._evaluate_and_optimize(campaign_id, metrics)
            
    def _evaluate_and_optimize(self, campaign_id: str, metrics: CampaignMetrics):
        """Avalia regras e executa otimizações"""
        targets = self.campaign_targets.get(campaign_id, {
            "cpa": 20,
            "roas": 3,
            "daily_budget": 100
        })
        
        triggered_rules = self.rule_engine.evaluate_rules(campaign_id, metrics, targets)
        
        for rule in triggered_rules:
            event = self._execute_optimization(campaign_id, rule, metrics)
            if event:
                self.optimization_events.append(event)
                rule.last_triggered = datetime.now()
                rule.trigger_count += 1
                
    def _execute_optimization(
        self,
        campaign_id: str,
        rule: OptimizationRule,
        metrics: CampaignMetrics
    ) -> Optional[OptimizationEvent]:
        """Executa uma otimização"""
        try:
            event_id = hashlib.md5(f"{campaign_id}{rule.id}{datetime.now()}".encode()).hexdigest()[:12]
            
            old_value = 0
            new_value = 0
            
            if rule.action == OptimizationAction.DECREASE_BID:
                old_value = metrics.cpc
                new_value = old_value * (1 - rule.action_value)
                
            elif rule.action == OptimizationAction.INCREASE_BID:
                old_value = metrics.cpc
                new_value = old_value * (1 + rule.action_value)
                
            elif rule.action == OptimizationAction.INCREASE_BUDGET:
                old_value = self.campaign_targets.get(campaign_id, {}).get("daily_budget", 100)
                new_value = old_value * (1 + rule.action_value)
                
            elif rule.action == OptimizationAction.DECREASE_BUDGET:
                old_value = self.campaign_targets.get(campaign_id, {}).get("daily_budget", 100)
                new_value = old_value * (1 - rule.action_value)
                
            elif rule.action == OptimizationAction.SCALE_CAMPAIGN:
                old_value = self.campaign_targets.get(campaign_id, {}).get("daily_budget", 100)
                new_value = old_value * (1 + rule.action_value)
                
            event = OptimizationEvent(
                id=event_id,
                rule_id=rule.id,
                campaign_id=campaign_id,
                action=rule.action,
                old_value=round(old_value, 2),
                new_value=round(new_value, 2),
                reason=f"Regra '{rule.name}' acionada: {rule.condition.value}"
            )
            
            logger.info(f"Otimização executada: {event.action.value} para campanha {campaign_id}")
            
            return event
            
        except Exception as e:
            logger.error(f"Erro ao executar otimização: {e}")
            return None
            
    def get_optimization_history(
        self,
        campaign_id: Optional[str] = None,
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Obtém histórico de otimizações"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        events = [e for e in self.optimization_events if e.timestamp > cutoff]
        
        if campaign_id:
            events = [e for e in events if e.campaign_id == campaign_id]
            
        return [e.to_dict() for e in events]
    
    def get_optimization_summary(self, campaign_id: str) -> Dict[str, Any]:
        """Obtém resumo de otimizações de uma campanha"""
        events = [e for e in self.optimization_events if e.campaign_id == campaign_id]
        
        if not events:
            return {
                "campaign_id": campaign_id,
                "total_optimizations": 0,
                "by_action": {},
                "success_rate": 0
            }
            
        by_action = {}
        for event in events:
            action = event.action.value
            by_action[action] = by_action.get(action, 0) + 1
            
        successful = len([e for e in events if e.success])
        
        return {
            "campaign_id": campaign_id,
            "total_optimizations": len(events),
            "by_action": by_action,
            "success_rate": (successful / len(events) * 100) if events else 0,
            "last_optimization": events[-1].to_dict() if events else None
        }
    
    def get_active_rules(self) -> List[Dict[str, Any]]:
        """Obtém regras ativas"""
        return [
            {
                "id": rule.id,
                "name": rule.name,
                "condition": rule.condition.value,
                "threshold": rule.threshold,
                "action": rule.action.value,
                "action_value": rule.action_value,
                "cooldown_minutes": rule.cooldown_minutes,
                "is_active": rule.is_active,
                "trigger_count": rule.trigger_count,
                "last_triggered": rule.last_triggered.isoformat() if rule.last_triggered else None
            }
            for rule in self.rule_engine.rules.values()
        ]
    
    def add_custom_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona regra personalizada"""
        rule_id = hashlib.md5(f"{rule_data.get('name', '')}{datetime.now()}".encode()).hexdigest()[:12]
        
        rule = OptimizationRule(
            id=rule_id,
            name=rule_data.get("name", "Custom Rule"),
            condition=TriggerCondition[rule_data.get("condition", "CPA_ABOVE_TARGET").upper()],
            threshold=rule_data.get("threshold", 1.0),
            action=OptimizationAction[rule_data.get("action", "DECREASE_BID").upper()],
            action_value=rule_data.get("action_value", 0.1),
            cooldown_minutes=rule_data.get("cooldown_minutes", 60)
        )
        
        self.rule_engine.add_rule(rule)
        
        return {
            "id": rule.id,
            "name": rule.name,
            "status": "created"
        }
    
    def toggle_rule(self, rule_id: str, is_active: bool) -> Dict[str, Any]:
        """Ativa/desativa uma regra"""
        if rule_id in self.rule_engine.rules:
            self.rule_engine.rules[rule_id].is_active = is_active
            return {"rule_id": rule_id, "is_active": is_active, "status": "updated"}
        return {"error": "Regra não encontrada"}
    
    def get_realtime_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Obtém métricas em tempo real de uma campanha"""
        recent = self.metrics_buffer.get_recent_metrics(campaign_id, minutes=60)
        
        if not recent:
            return {"campaign_id": campaign_id, "status": "no_data"}
            
        latest = recent[-1]
        avg = self.metrics_buffer.get_average_metrics(campaign_id, minutes=60)
        
        return {
            "campaign_id": campaign_id,
            "current": {
                "impressions": latest.impressions,
                "clicks": latest.clicks,
                "conversions": latest.conversions,
                "spend": latest.spend,
                "ctr": round(latest.ctr, 2),
                "cpc": round(latest.cpc, 2),
                "cpa": round(latest.cpa, 2),
                "roas": round(latest.roas, 2)
            },
            "hourly_average": avg,
            "timestamp": latest.timestamp.isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do motor"""
        return {
            "is_running": self.is_running,
            "active_rules": len([r for r in self.rule_engine.rules.values() if r.is_active]),
            "total_rules": len(self.rule_engine.rules),
            "campaigns_monitored": len(self.metrics_buffer.buffer),
            "total_optimizations": len(self.optimization_events),
            "optimizations_today": len([
                e for e in self.optimization_events 
                if e.timestamp.date() == datetime.now().date()
            ])
        }


# Instância global
realtime_engine = RealtimeOptimizationEngine()


# Funções de conveniência
async def start_realtime_optimization():
    """Inicia otimização em tempo real"""
    await realtime_engine.start()

async def stop_realtime_optimization():
    """Para otimização em tempo real"""
    await realtime_engine.stop()

def ingest_campaign_metrics(campaign_id: str, metrics: Dict[str, Any]):
    """Ingere métricas de campanha"""
    realtime_engine.ingest_metrics(campaign_id, metrics)

def set_campaign_targets(campaign_id: str, targets: Dict[str, float]):
    """Define targets de campanha"""
    realtime_engine.set_campaign_targets(campaign_id, targets)

def get_optimization_history(campaign_id: str = None, hours: int = 24) -> List[Dict[str, Any]]:
    """Obtém histórico de otimizações"""
    return realtime_engine.get_optimization_history(campaign_id, hours)

def get_active_rules() -> List[Dict[str, Any]]:
    """Obtém regras ativas"""
    return realtime_engine.get_active_rules()

def add_optimization_rule(rule_data: Dict[str, Any]) -> Dict[str, Any]:
    """Adiciona regra de otimização"""
    return realtime_engine.add_custom_rule(rule_data)

def get_realtime_status() -> Dict[str, Any]:
    """Obtém status do motor em tempo real"""
    return realtime_engine.get_status()

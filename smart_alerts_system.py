"""
SMART ALERTS SYSTEM - Sistema de Alertas Inteligentes
Sistema avançado de notificações e alertas em tempo real
Versão: 1.0 - Expansão Avançada
"""

import os
import json
import asyncio
import logging
import hashlib
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Severidade do alerta"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertCategory(Enum):
    """Categoria do alerta"""
    PERFORMANCE = "performance"
    BUDGET = "budget"
    ANOMALY = "anomaly"
    COMPETITOR = "competitor"
    SYSTEM = "system"
    OPPORTUNITY = "opportunity"


class NotificationChannel(Enum):
    """Canais de notificação"""
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    SLACK = "slack"
    TELEGRAM = "telegram"
    PUSH = "push"
    IN_APP = "in_app"


class AlertStatus(Enum):
    """Status do alerta"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SNOOZED = "snoozed"


@dataclass
class AlertRule:
    """Regra de alerta"""
    id: str
    name: str
    description: str
    category: AlertCategory
    severity: AlertSeverity
    condition: str  # Expressão de condição
    threshold: float
    comparison: str  # gt, lt, eq, gte, lte
    metric: str
    cooldown_minutes: int = 30
    channels: List[NotificationChannel] = field(default_factory=list)
    is_active: bool = True
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "severity": self.severity.value,
            "condition": self.condition,
            "threshold": self.threshold,
            "comparison": self.comparison,
            "metric": self.metric,
            "cooldown_minutes": self.cooldown_minutes,
            "channels": [c.value for c in self.channels],
            "is_active": self.is_active,
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None,
            "trigger_count": self.trigger_count
        }


@dataclass
class Alert:
    """Alerta gerado"""
    id: str
    rule_id: str
    title: str
    message: str
    category: AlertCategory
    severity: AlertSeverity
    status: AlertStatus
    campaign_id: Optional[str]
    metric_value: float
    threshold_value: float
    recommended_actions: List[str]
    metadata: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "title": self.title,
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "status": self.status.value,
            "campaign_id": self.campaign_id,
            "metric_value": self.metric_value,
            "threshold_value": self.threshold_value,
            "recommended_actions": self.recommended_actions,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        }


@dataclass
class NotificationPreferences:
    """Preferências de notificação do usuário"""
    user_id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    slack_webhook: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    enabled_channels: List[NotificationChannel] = field(default_factory=lambda: [NotificationChannel.IN_APP])
    quiet_hours_start: Optional[int] = None  # Hora (0-23)
    quiet_hours_end: Optional[int] = None
    min_severity: AlertSeverity = AlertSeverity.WARNING


class NotificationDispatcher:
    """Despachante de notificações"""
    
    def __init__(self):
        self.sent_notifications: List[Dict] = []
        
    async def send_notification(
        self,
        alert: Alert,
        channel: NotificationChannel,
        preferences: NotificationPreferences
    ) -> bool:
        """Envia notificação por um canal específico"""
        try:
            if channel == NotificationChannel.EMAIL:
                return await self._send_email(alert, preferences.email)
            elif channel == NotificationChannel.SLACK:
                return await self._send_slack(alert, preferences.slack_webhook)
            elif channel == NotificationChannel.TELEGRAM:
                return await self._send_telegram(alert, preferences.telegram_chat_id)
            elif channel == NotificationChannel.WEBHOOK:
                return await self._send_webhook(alert, preferences)
            elif channel == NotificationChannel.IN_APP:
                return await self._send_in_app(alert, preferences.user_id)
            else:
                logger.warning(f"Canal não suportado: {channel}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")
            return False
            
    async def _send_email(self, alert: Alert, email: str) -> bool:
        """Envia notificação por email"""
        if not email:
            return False
            
        # Simulação de envio de email
        logger.info(f"Email enviado para {email}: {alert.title}")
        
        self.sent_notifications.append({
            "channel": "email",
            "recipient": email,
            "alert_id": alert.id,
            "timestamp": datetime.now().isoformat()
        })
        
        return True
        
    async def _send_slack(self, alert: Alert, webhook_url: str) -> bool:
        """Envia notificação para Slack"""
        if not webhook_url:
            return False
            
        severity_emoji = {
            AlertSeverity.INFO: "ℹ️",
            AlertSeverity.WARNING: "⚠️",
            AlertSeverity.CRITICAL: "🚨",
            AlertSeverity.EMERGENCY: "🔴"
        }
        
        payload = {
            "text": f"{severity_emoji.get(alert.severity, '📢')} *{alert.title}*",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{alert.title}*\n{alert.message}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Severidade:* {alert.severity.value}"},
                        {"type": "mrkdwn", "text": f"*Categoria:* {alert.category.value}"},
                        {"type": "mrkdwn", "text": f"*Valor:* {alert.metric_value}"},
                        {"type": "mrkdwn", "text": f"*Threshold:* {alert.threshold_value}"}
                    ]
                }
            ]
        }
        
        # Simulação de envio para Slack
        logger.info(f"Slack notification enviada: {alert.title}")
        
        self.sent_notifications.append({
            "channel": "slack",
            "webhook": webhook_url[:30] + "...",
            "alert_id": alert.id,
            "timestamp": datetime.now().isoformat()
        })
        
        return True
        
    async def _send_telegram(self, alert: Alert, chat_id: str) -> bool:
        """Envia notificação para Telegram"""
        if not chat_id:
            return False
            
        message = f"""
🚨 *{alert.title}*

{alert.message}

📊 *Detalhes:*
• Severidade: {alert.severity.value}
• Categoria: {alert.category.value}
• Valor atual: {alert.metric_value}
• Threshold: {alert.threshold_value}

💡 *Ações recomendadas:*
{chr(10).join(f'• {action}' for action in alert.recommended_actions)}
        """
        
        # Simulação de envio para Telegram
        logger.info(f"Telegram notification enviada para {chat_id}: {alert.title}")
        
        self.sent_notifications.append({
            "channel": "telegram",
            "chat_id": chat_id,
            "alert_id": alert.id,
            "timestamp": datetime.now().isoformat()
        })
        
        return True
        
    async def _send_webhook(self, alert: Alert, preferences: NotificationPreferences) -> bool:
        """Envia notificação via webhook"""
        # Simulação de webhook
        logger.info(f"Webhook notification enviada: {alert.title}")
        return True
        
    async def _send_in_app(self, alert: Alert, user_id: str) -> bool:
        """Envia notificação in-app"""
        logger.info(f"In-app notification para user {user_id}: {alert.title}")
        
        self.sent_notifications.append({
            "channel": "in_app",
            "user_id": user_id,
            "alert_id": alert.id,
            "timestamp": datetime.now().isoformat()
        })
        
        return True


class AlertRuleEngine:
    """Motor de regras de alerta"""
    
    def __init__(self):
        self.rules: Dict[str, AlertRule] = {}
        self._initialize_default_rules()
        
    def _initialize_default_rules(self):
        """Inicializa regras padrão"""
        default_rules = [
            AlertRule(
                id="rule_cpa_critical",
                name="CPA Crítico",
                description="CPA está muito acima do target",
                category=AlertCategory.PERFORMANCE,
                severity=AlertSeverity.CRITICAL,
                condition="cpa > target * 1.5",
                threshold=1.5,
                comparison="gt",
                metric="cpa",
                cooldown_minutes=60,
                channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.IN_APP]
            ),
            AlertRule(
                id="rule_roas_low",
                name="ROAS Baixo",
                description="ROAS está abaixo do mínimo aceitável",
                category=AlertCategory.PERFORMANCE,
                severity=AlertSeverity.WARNING,
                condition="roas < 2",
                threshold=2.0,
                comparison="lt",
                metric="roas",
                cooldown_minutes=120,
                channels=[NotificationChannel.EMAIL, NotificationChannel.IN_APP]
            ),
            AlertRule(
                id="rule_budget_90",
                name="Orçamento 90%",
                description="90% do orçamento diário foi consumido",
                category=AlertCategory.BUDGET,
                severity=AlertSeverity.WARNING,
                condition="spend > budget * 0.9",
                threshold=0.9,
                comparison="gt",
                metric="budget_utilization",
                cooldown_minutes=240,
                channels=[NotificationChannel.IN_APP]
            ),
            AlertRule(
                id="rule_budget_depleted",
                name="Orçamento Esgotado",
                description="Orçamento diário foi totalmente consumido",
                category=AlertCategory.BUDGET,
                severity=AlertSeverity.CRITICAL,
                condition="spend >= budget",
                threshold=1.0,
                comparison="gte",
                metric="budget_utilization",
                cooldown_minutes=1440,
                channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.IN_APP]
            ),
            AlertRule(
                id="rule_ctr_drop",
                name="Queda de CTR",
                description="CTR caiu significativamente",
                category=AlertCategory.ANOMALY,
                severity=AlertSeverity.WARNING,
                condition="ctr < avg_ctr * 0.7",
                threshold=0.7,
                comparison="lt",
                metric="ctr_ratio",
                cooldown_minutes=180,
                channels=[NotificationChannel.IN_APP]
            ),
            AlertRule(
                id="rule_conversion_spike",
                name="Pico de Conversões",
                description="Conversões aumentaram significativamente",
                category=AlertCategory.OPPORTUNITY,
                severity=AlertSeverity.INFO,
                condition="conversions > avg_conversions * 2",
                threshold=2.0,
                comparison="gt",
                metric="conversion_ratio",
                cooldown_minutes=60,
                channels=[NotificationChannel.IN_APP]
            ),
            AlertRule(
                id="rule_competitor_new_ad",
                name="Novo Anúncio de Concorrente",
                description="Concorrente lançou novo anúncio",
                category=AlertCategory.COMPETITOR,
                severity=AlertSeverity.INFO,
                condition="competitor_new_ads > 0",
                threshold=1,
                comparison="gte",
                metric="competitor_ads",
                cooldown_minutes=1440,
                channels=[NotificationChannel.EMAIL, NotificationChannel.IN_APP]
            ),
            AlertRule(
                id="rule_system_error",
                name="Erro de Sistema",
                description="Erro detectado na integração",
                category=AlertCategory.SYSTEM,
                severity=AlertSeverity.EMERGENCY,
                condition="error_count > 0",
                threshold=1,
                comparison="gt",
                metric="errors",
                cooldown_minutes=15,
                channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.IN_APP]
            )
        ]
        
        for rule in default_rules:
            self.rules[rule.id] = rule
            
    def evaluate_rule(
        self,
        rule: AlertRule,
        metrics: Dict[str, float],
        targets: Dict[str, float]
    ) -> Optional[Dict[str, Any]]:
        """Avalia se uma regra deve ser acionada"""
        if not rule.is_active:
            return None
            
        # Verificar cooldown
        if rule.last_triggered:
            cooldown_end = rule.last_triggered + timedelta(minutes=rule.cooldown_minutes)
            if datetime.now() < cooldown_end:
                return None
                
        metric_value = metrics.get(rule.metric, 0)
        threshold = rule.threshold
        
        # Ajustar threshold baseado em targets se necessário
        if rule.metric in ["cpa", "cpc"]:
            target = targets.get(rule.metric, threshold)
            threshold = target * rule.threshold
        elif rule.metric == "roas":
            target = targets.get("roas", threshold)
            threshold = target * rule.threshold if rule.comparison == "lt" else threshold
            
        # Avaliar condição
        triggered = False
        if rule.comparison == "gt":
            triggered = metric_value > threshold
        elif rule.comparison == "lt":
            triggered = metric_value < threshold
        elif rule.comparison == "gte":
            triggered = metric_value >= threshold
        elif rule.comparison == "lte":
            triggered = metric_value <= threshold
        elif rule.comparison == "eq":
            triggered = metric_value == threshold
            
        if triggered:
            return {
                "rule": rule,
                "metric_value": metric_value,
                "threshold": threshold
            }
            
        return None
    
    def add_rule(self, rule: AlertRule):
        """Adiciona nova regra"""
        self.rules[rule.id] = rule
        
    def remove_rule(self, rule_id: str):
        """Remove regra"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            
    def toggle_rule(self, rule_id: str, is_active: bool):
        """Ativa/desativa regra"""
        if rule_id in self.rules:
            self.rules[rule_id].is_active = is_active


class SmartAlertsSystem:
    """
    Sistema principal de Alertas Inteligentes
    Monitora métricas e envia notificações
    """
    
    def __init__(self):
        self.rule_engine = AlertRuleEngine()
        self.notification_dispatcher = NotificationDispatcher()
        self.alerts: Dict[str, Alert] = {}
        self.user_preferences: Dict[str, NotificationPreferences] = {}
        self.alert_history: List[Alert] = []
        self.is_running = False
        
    async def start(self):
        """Inicia o sistema de alertas"""
        self.is_running = True
        logger.info("Smart Alerts System iniciado")
        
    async def stop(self):
        """Para o sistema de alertas"""
        self.is_running = False
        logger.info("Smart Alerts System parado")
        
    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Define preferências de notificação do usuário"""
        self.user_preferences[user_id] = NotificationPreferences(
            user_id=user_id,
            email=preferences.get("email"),
            phone=preferences.get("phone"),
            slack_webhook=preferences.get("slack_webhook"),
            telegram_chat_id=preferences.get("telegram_chat_id"),
            enabled_channels=[NotificationChannel[c.upper()] for c in preferences.get("channels", ["in_app"])],
            quiet_hours_start=preferences.get("quiet_hours_start"),
            quiet_hours_end=preferences.get("quiet_hours_end"),
            min_severity=AlertSeverity[preferences.get("min_severity", "WARNING").upper()]
        )
        
    async def evaluate_metrics(
        self,
        user_id: str,
        campaign_id: str,
        metrics: Dict[str, float],
        targets: Dict[str, float]
    ) -> List[Alert]:
        """Avalia métricas e gera alertas se necessário"""
        generated_alerts = []
        
        for rule in self.rule_engine.rules.values():
            result = self.rule_engine.evaluate_rule(rule, metrics, targets)
            
            if result:
                alert = self._create_alert(result, campaign_id, metrics)
                self.alerts[alert.id] = alert
                self.alert_history.append(alert)
                generated_alerts.append(alert)
                
                # Atualizar regra
                rule.last_triggered = datetime.now()
                rule.trigger_count += 1
                
                # Enviar notificações
                await self._dispatch_notifications(user_id, alert, rule)
                
        return generated_alerts
    
    def _create_alert(
        self,
        trigger_result: Dict[str, Any],
        campaign_id: str,
        metrics: Dict[str, float]
    ) -> Alert:
        """Cria um novo alerta"""
        rule = trigger_result["rule"]
        metric_value = trigger_result["metric_value"]
        threshold = trigger_result["threshold"]
        
        alert_id = hashlib.md5(f"{rule.id}{campaign_id}{datetime.now()}".encode()).hexdigest()[:12]
        
        # Gerar mensagem contextual
        message = self._generate_alert_message(rule, metric_value, threshold, metrics)
        
        # Gerar ações recomendadas
        actions = self._generate_recommended_actions(rule, metric_value, threshold)
        
        return Alert(
            id=alert_id,
            rule_id=rule.id,
            title=rule.name,
            message=message,
            category=rule.category,
            severity=rule.severity,
            status=AlertStatus.ACTIVE,
            campaign_id=campaign_id,
            metric_value=metric_value,
            threshold_value=threshold,
            recommended_actions=actions,
            metadata={
                "metrics_snapshot": metrics,
                "rule_condition": rule.condition
            }
        )
    
    def _generate_alert_message(
        self,
        rule: AlertRule,
        metric_value: float,
        threshold: float,
        metrics: Dict[str, float]
    ) -> str:
        """Gera mensagem contextual do alerta"""
        messages = {
            "cpa": f"O CPA atual é R$ {metric_value:.2f}, {((metric_value/threshold - 1) * 100):.0f}% acima do target de R$ {threshold:.2f}",
            "roas": f"O ROAS atual é {metric_value:.2f}x, abaixo do mínimo de {threshold:.2f}x",
            "budget_utilization": f"Já foi gasto {metric_value * 100:.0f}% do orçamento diário",
            "ctr_ratio": f"O CTR caiu {((1 - metric_value) * 100):.0f}% em relação à média",
            "conversion_ratio": f"As conversões aumentaram {((metric_value - 1) * 100):.0f}% em relação à média",
            "errors": f"Foram detectados {int(metric_value)} erros no sistema"
        }
        
        return messages.get(rule.metric, rule.description)
    
    def _generate_recommended_actions(
        self,
        rule: AlertRule,
        metric_value: float,
        threshold: float
    ) -> List[str]:
        """Gera ações recomendadas baseadas no alerta"""
        actions_map = {
            AlertCategory.PERFORMANCE: [
                "Revisar segmentação de público",
                "Analisar criativos de baixo desempenho",
                "Ajustar lances automaticamente",
                "Considerar pausar anúncios com CPA alto"
            ],
            AlertCategory.BUDGET: [
                "Revisar distribuição de orçamento",
                "Considerar aumentar orçamento diário",
                "Ajustar lances para otimizar gastos",
                "Pausar campanhas de baixo ROI"
            ],
            AlertCategory.ANOMALY: [
                "Investigar causa da anomalia",
                "Verificar mudanças recentes na campanha",
                "Comparar com período anterior",
                "Monitorar de perto nas próximas horas"
            ],
            AlertCategory.COMPETITOR: [
                "Analisar estratégia do concorrente",
                "Considerar ajustes nos criativos",
                "Revisar posicionamento de preço",
                "Monitorar impacto nas métricas"
            ],
            AlertCategory.SYSTEM: [
                "Verificar logs do sistema",
                "Testar integrações",
                "Contatar suporte técnico se persistir",
                "Verificar status das APIs"
            ],
            AlertCategory.OPPORTUNITY: [
                "Escalar campanhas de alto desempenho",
                "Aumentar orçamento para aproveitar momento",
                "Replicar estratégia em outras campanhas",
                "Documentar fatores de sucesso"
            ]
        }
        
        return actions_map.get(rule.category, ["Monitorar situação"])
    
    async def _dispatch_notifications(
        self,
        user_id: str,
        alert: Alert,
        rule: AlertRule
    ):
        """Despacha notificações para todos os canais configurados"""
        preferences = self.user_preferences.get(user_id)
        
        if not preferences:
            preferences = NotificationPreferences(user_id=user_id)
            
        # Verificar severidade mínima
        severity_order = [AlertSeverity.INFO, AlertSeverity.WARNING, AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]
        if severity_order.index(alert.severity) < severity_order.index(preferences.min_severity):
            return
            
        # Verificar horário silencioso
        if preferences.quiet_hours_start is not None and preferences.quiet_hours_end is not None:
            current_hour = datetime.now().hour
            if preferences.quiet_hours_start <= current_hour < preferences.quiet_hours_end:
                if alert.severity not in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]:
                    return
                    
        # Enviar para cada canal configurado
        for channel in rule.channels:
            if channel in preferences.enabled_channels:
                await self.notification_dispatcher.send_notification(alert, channel, preferences)
                
    def acknowledge_alert(self, alert_id: str) -> Dict[str, Any]:
        """Reconhece um alerta"""
        alert = self.alerts.get(alert_id)
        
        if not alert:
            return {"error": "Alerta não encontrado"}
            
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = datetime.now()
        
        return {"alert_id": alert_id, "status": "acknowledged"}
    
    def resolve_alert(self, alert_id: str) -> Dict[str, Any]:
        """Resolve um alerta"""
        alert = self.alerts.get(alert_id)
        
        if not alert:
            return {"error": "Alerta não encontrado"}
            
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.now()
        
        return {"alert_id": alert_id, "status": "resolved"}
    
    def snooze_alert(self, alert_id: str, minutes: int = 60) -> Dict[str, Any]:
        """Adia um alerta"""
        alert = self.alerts.get(alert_id)
        
        if not alert:
            return {"error": "Alerta não encontrado"}
            
        alert.status = AlertStatus.SNOOZED
        
        return {"alert_id": alert_id, "status": "snoozed", "snooze_until": (datetime.now() + timedelta(minutes=minutes)).isoformat()}
    
    def get_active_alerts(self, campaign_id: str = None) -> List[Dict[str, Any]]:
        """Obtém alertas ativos"""
        alerts = [a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE]
        
        if campaign_id:
            alerts = [a for a in alerts if a.campaign_id == campaign_id]
            
        return [a.to_dict() for a in sorted(alerts, key=lambda x: x.created_at, reverse=True)]
    
    def get_alert_history(
        self,
        campaign_id: str = None,
        hours: int = 24,
        severity: AlertSeverity = None
    ) -> List[Dict[str, Any]]:
        """Obtém histórico de alertas"""
        cutoff = datetime.now() - timedelta(hours=hours)
        alerts = [a for a in self.alert_history if a.created_at > cutoff]
        
        if campaign_id:
            alerts = [a for a in alerts if a.campaign_id == campaign_id]
            
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
            
        return [a.to_dict() for a in sorted(alerts, key=lambda x: x.created_at, reverse=True)]
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Obtém resumo de alertas"""
        active_alerts = [a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE]
        
        by_severity = defaultdict(int)
        by_category = defaultdict(int)
        
        for alert in active_alerts:
            by_severity[alert.severity.value] += 1
            by_category[alert.category.value] += 1
            
        return {
            "total_active": len(active_alerts),
            "by_severity": dict(by_severity),
            "by_category": dict(by_category),
            "critical_count": by_severity.get("critical", 0) + by_severity.get("emergency", 0),
            "last_24h": len([a for a in self.alert_history if a.created_at > datetime.now() - timedelta(hours=24)])
        }
    
    def get_rules(self) -> List[Dict[str, Any]]:
        """Obtém todas as regras de alerta"""
        return [r.to_dict() for r in self.rule_engine.rules.values()]
    
    def add_custom_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona regra personalizada"""
        rule_id = hashlib.md5(f"{rule_data.get('name', '')}{datetime.now()}".encode()).hexdigest()[:12]
        
        rule = AlertRule(
            id=rule_id,
            name=rule_data.get("name", "Custom Rule"),
            description=rule_data.get("description", ""),
            category=AlertCategory[rule_data.get("category", "PERFORMANCE").upper()],
            severity=AlertSeverity[rule_data.get("severity", "WARNING").upper()],
            condition=rule_data.get("condition", ""),
            threshold=rule_data.get("threshold", 1.0),
            comparison=rule_data.get("comparison", "gt"),
            metric=rule_data.get("metric", ""),
            cooldown_minutes=rule_data.get("cooldown_minutes", 60),
            channels=[NotificationChannel[c.upper()] for c in rule_data.get("channels", ["in_app"])]
        )
        
        self.rule_engine.add_rule(rule)
        
        return {"id": rule.id, "name": rule.name, "status": "created"}
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do sistema"""
        return {
            "is_running": self.is_running,
            "total_rules": len(self.rule_engine.rules),
            "active_rules": len([r for r in self.rule_engine.rules.values() if r.is_active]),
            "active_alerts": len([a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE]),
            "total_alerts_today": len([a for a in self.alert_history if a.created_at.date() == datetime.now().date()]),
            "notifications_sent": len(self.notification_dispatcher.sent_notifications)
        }


# Instância global
alerts_system = SmartAlertsSystem()


# Funções de conveniência
async def start_alerts_system():
    """Inicia sistema de alertas"""
    await alerts_system.start()

async def stop_alerts_system():
    """Para sistema de alertas"""
    await alerts_system.stop()

async def evaluate_campaign_metrics(
    user_id: str,
    campaign_id: str,
    metrics: Dict[str, float],
    targets: Dict[str, float]
) -> List[Dict[str, Any]]:
    """Avalia métricas e gera alertas"""
    alerts = await alerts_system.evaluate_metrics(user_id, campaign_id, metrics, targets)
    return [a.to_dict() for a in alerts]

def get_active_alerts(campaign_id: str = None) -> List[Dict[str, Any]]:
    """Obtém alertas ativos"""
    return alerts_system.get_active_alerts(campaign_id)

def get_alert_summary() -> Dict[str, Any]:
    """Obtém resumo de alertas"""
    return alerts_system.get_alert_summary()

def acknowledge_alert(alert_id: str) -> Dict[str, Any]:
    """Reconhece alerta"""
    return alerts_system.acknowledge_alert(alert_id)

def resolve_alert(alert_id: str) -> Dict[str, Any]:
    """Resolve alerta"""
    return alerts_system.resolve_alert(alert_id)

def get_alert_rules() -> List[Dict[str, Any]]:
    """Obtém regras de alerta"""
    return alerts_system.get_rules()

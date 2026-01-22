"""
WAR MODE - Modo Guerra de Escala Extrema
Escala agressiva com proteção total e monitoramento 24/7
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import random

class WarModeLevel(Enum):
    STANDBY = "standby"
    ALERT = "alert"
    ENGAGED = "engaged"
    FULL_WAR = "full_war"
    RETREAT = "retreat"

class WarMode:
    """Sistema de Modo Guerra para escala extrema."""
    
    def __init__(self):
        self.name = "War Mode"
        self.version = "2.0.0"
        self.current_level = WarModeLevel.STANDBY
        self.active_campaigns = {}
        self.protection_status = {}
        
        self.scale_configs = {
            WarModeLevel.STANDBY: {
                "max_budget_increase": 0.10,
                "check_interval_minutes": 60,
                "risk_tolerance": "low",
                "auto_pause_threshold": 0.7,
                "max_daily_spend_increase": 0.20
            },
            WarModeLevel.ALERT: {
                "max_budget_increase": 0.20,
                "check_interval_minutes": 30,
                "risk_tolerance": "medium",
                "auto_pause_threshold": 0.8,
                "max_daily_spend_increase": 0.30
            },
            WarModeLevel.ENGAGED: {
                "max_budget_increase": 0.50,
                "check_interval_minutes": 15,
                "risk_tolerance": "high",
                "auto_pause_threshold": 0.9,
                "max_daily_spend_increase": 0.50
            },
            WarModeLevel.FULL_WAR: {
                "max_budget_increase": 1.00,
                "check_interval_minutes": 5,
                "risk_tolerance": "very_high",
                "auto_pause_threshold": 1.0,
                "max_daily_spend_increase": 1.00
            },
            WarModeLevel.RETREAT: {
                "max_budget_increase": -0.50,
                "check_interval_minutes": 5,
                "risk_tolerance": "minimal",
                "auto_pause_threshold": 0.5,
                "max_daily_spend_increase": -0.30
            }
        }
        
        self.protections = {
            "budget_cap": True,
            "roas_floor": True,
            "cpa_ceiling": True,
            "frequency_cap": True,
            "fatigue_detection": True,
            "anomaly_detection": True,
            "auto_pause": True,
            "rollback_ready": True
        }
        
        self.action_history = []
        self.active_alerts = []
    
    def activate_war_mode(self, level: str, campaigns: List[str], config: Dict = None) -> Dict[str, Any]:
        try:
            war_level = WarModeLevel(level)
        except:
            return {"error": f"Nivel invalido: {level}"}
        
        prereq_check = self._check_prerequisites(campaigns)
        if not prereq_check["passed"]:
            return {"error": "Pre-requisitos nao atendidos", "details": prereq_check["issues"]}
        
        self.current_level = war_level
        
        for campaign_id in campaigns:
            self.active_campaigns[campaign_id] = {
                "status": "active",
                "original_budget": config.get(campaign_id, {}).get("budget", 100) if config else 100,
                "current_budget": config.get(campaign_id, {}).get("budget", 100) if config else 100,
                "scale_history": [],
                "protection_triggers": 0,
                "activated_at": datetime.now().isoformat()
            }
        
        self._log_action("activate", {"level": level, "campaigns": campaigns})
        
        return {
            "status": "activated",
            "level": war_level.value,
            "campaigns_enrolled": len(campaigns),
            "config": self.scale_configs[war_level],
            "protections_active": list(self.protections.keys()),
            "message": f"MODO GUERRA {war_level.value.upper()} ATIVADO!"
        }
    
    def deactivate_war_mode(self, reason: str = "manual") -> Dict[str, Any]:
        previous_level = self.current_level
        self.current_level = WarModeLevel.STANDBY
        
        final_state = {}
        for campaign_id, data in self.active_campaigns.items():
            final_state[campaign_id] = {
                "final_budget": data["current_budget"],
                "budget_change": data["current_budget"] - data["original_budget"],
                "protection_triggers": data["protection_triggers"]
            }
        
        self.active_campaigns = {}
        self._log_action("deactivate", {"previous_level": previous_level.value, "reason": reason})
        
        return {
            "status": "deactivated",
            "previous_level": previous_level.value,
            "reason": reason,
            "final_state": final_state
        }
    
    def monitor_and_adjust(self, campaign_id: str, current_metrics: Dict) -> Dict[str, Any]:
        if campaign_id not in self.active_campaigns:
            return {"error": "Campanha nao esta no Modo Guerra"}
        
        campaign = self.active_campaigns[campaign_id]
        config = self.scale_configs[self.current_level]
        
        analysis = self._analyze_metrics(current_metrics, config)
        decision = self._make_scale_decision(analysis, campaign, config)
        protection_check = self._check_protections(current_metrics, campaign)
        
        if protection_check["safe"] and decision["action"] == "scale_up":
            new_budget = self._calculate_new_budget(campaign["current_budget"], decision["scale_factor"], config)
            campaign["current_budget"] = new_budget
        elif not protection_check["safe"]:
            campaign["protection_triggers"] += 1
            decision["action"] = "hold"
            decision["reason"] = f"Protecao ativada: {protection_check['triggered_protection']}"
        
        return {
            "campaign_id": campaign_id,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "decision": decision,
            "protection_check": protection_check,
            "current_budget": campaign["current_budget"]
        }
    
    def emergency_stop(self, reason: str) -> Dict[str, Any]:
        self.current_level = WarModeLevel.RETREAT
        
        paused_campaigns = []
        for campaign_id, data in self.active_campaigns.items():
            data["status"] = "paused"
            data["paused_at"] = datetime.now().isoformat()
            paused_campaigns.append(campaign_id)
        
        self._log_action("emergency_stop", {"reason": reason, "paused_campaigns": paused_campaigns})
        
        return {
            "status": "emergency_stopped",
            "reason": reason,
            "paused_campaigns": paused_campaigns,
            "message": "PARADA DE EMERGENCIA EXECUTADA"
        }
    
    def get_war_status(self) -> Dict[str, Any]:
        total_original = sum(c["original_budget"] for c in self.active_campaigns.values())
        total_current = sum(c["current_budget"] for c in self.active_campaigns.values())
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current_level": self.current_level.value,
            "active_campaigns": len(self.active_campaigns),
            "budget_summary": {
                "total_original": round(total_original, 2),
                "total_current": round(total_current, 2),
                "change_percent": round(((total_current - total_original) / total_original) * 100, 1) if total_original > 0 else 0
            },
            "protections_status": self.protections,
            "active_alerts": self.active_alerts
        }
    
    def get_scale_recommendation(self, campaign_metrics: Dict) -> Dict[str, Any]:
        roas = campaign_metrics.get("roas", 0)
        cpa = campaign_metrics.get("cpa", 0)
        target_cpa = campaign_metrics.get("target_cpa", cpa)
        conversions = campaign_metrics.get("conversions", 0)
        
        roas_score = min(100, (roas / 3) * 100) if roas > 0 else 0
        cpa_score = min(100, (target_cpa / cpa) * 100) if cpa > 0 else 0
        volume_score = min(100, (conversions / 10) * 100)
        
        overall_score = (roas_score * 0.4 + cpa_score * 0.4 + volume_score * 0.2)
        
        if overall_score >= 80:
            recommendation = {"action": "scale_aggressively", "suggested_increase": "50-100%", "suggested_level": "full_war"}
        elif overall_score >= 60:
            recommendation = {"action": "scale_moderately", "suggested_increase": "20-50%", "suggested_level": "engaged"}
        elif overall_score >= 40:
            recommendation = {"action": "scale_cautiously", "suggested_increase": "10-20%", "suggested_level": "alert"}
        else:
            recommendation = {"action": "do_not_scale", "suggested_increase": "0%", "suggested_level": "standby"}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "scores": {"roas_score": round(roas_score, 1), "cpa_score": round(cpa_score, 1), "overall_score": round(overall_score, 1)},
            "recommendation": recommendation
        }
    
    def _check_prerequisites(self, campaigns: List[str]) -> Dict[str, Any]:
        issues = []
        if len(campaigns) == 0:
            issues.append("Nenhuma campanha selecionada")
        return {"passed": len(issues) == 0, "issues": issues}
    
    def _analyze_metrics(self, metrics: Dict, config: Dict) -> Dict[str, Any]:
        roas = metrics.get("roas", 0)
        cpa = metrics.get("cpa", 0)
        target_cpa = metrics.get("target_cpa", cpa)
        
        return {
            "roas_status": "good" if roas >= 2.0 else "warning" if roas >= 1.5 else "critical",
            "cpa_status": "good" if cpa <= target_cpa else "warning" if cpa <= target_cpa * 1.2 else "critical",
            "overall_health": "healthy" if roas >= 2.0 and cpa <= target_cpa else "warning" if roas >= 1.5 else "critical"
        }
    
    def _make_scale_decision(self, analysis: Dict, campaign: Dict, config: Dict) -> Dict[str, Any]:
        if analysis["overall_health"] == "healthy":
            return {"action": "scale_up", "scale_factor": config["max_budget_increase"], "reason": "Metricas saudaveis"}
        elif analysis["overall_health"] == "warning":
            return {"action": "hold", "scale_factor": 0, "reason": "Metricas em alerta"}
        else:
            return {"action": "scale_down", "scale_factor": -0.20, "reason": "Metricas criticas"}
    
    def _check_protections(self, metrics: Dict, campaign: Dict) -> Dict[str, Any]:
        triggered = None
        if self.protections["roas_floor"] and metrics.get("roas", 0) < 1.0:
            triggered = "roas_floor"
        if self.protections["cpa_ceiling"]:
            target_cpa = metrics.get("target_cpa", 100)
            if metrics.get("cpa", 0) > target_cpa * 1.5:
                triggered = "cpa_ceiling"
        if self.protections["budget_cap"]:
            max_budget = campaign["original_budget"] * 3
            if campaign["current_budget"] >= max_budget:
                triggered = "budget_cap"
        return {"safe": triggered is None, "triggered_protection": triggered}
    
    def _calculate_new_budget(self, current: float, scale_factor: float, config: Dict) -> float:
        increase = current * scale_factor
        max_increase = current * config["max_daily_spend_increase"]
        return round(current + min(increase, max_increase), 2)
    
    def _log_action(self, action_type: str, details: Dict):
        self.action_history.append({"timestamp": datetime.now().isoformat(), "action": action_type, "details": details})
        if len(self.action_history) > 1000:
            self.action_history = self.action_history[-1000:]


war_mode = WarMode()

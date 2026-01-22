"""
AUTOMATION HUB - Central de Automacao
Sistema de regras automaticas e workflows inteligentes
Nexora Prime V2 - Expansao Unicornio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
import random

class AutomationHub:
    """Central de automacao e regras."""
    
    def __init__(self):
        self.name = "Automation Hub"
        self.version = "2.0.0"
        
        # Regras ativas
        self.active_rules = {}
        
        # Workflows configurados
        self.workflows = {}
        
        # Historico de execucoes
        self.execution_history = []
        
        # Templates de regras
        self.rule_templates = self._init_rule_templates()
        
        # Templates de workflows
        self.workflow_templates = self._init_workflow_templates()
        
        # Condicoes disponiveis
        self.available_conditions = self._init_conditions()
        
        # Acoes disponiveis
        self.available_actions = self._init_actions()
    
    def _init_rule_templates(self) -> Dict[str, Dict]:
        """Inicializa templates de regras."""
        
        return {
            "pause_high_cpa": {
                "name": "Pausar CPA Alto",
                "description": "Pausa anuncios quando CPA excede limite",
                "conditions": [{"type": "cpa_above", "value": 50}],
                "actions": [{"type": "pause_ad", "delay": 0}],
                "category": "cost_control"
            },
            "scale_high_roas": {
                "name": "Escalar ROAS Alto",
                "description": "Aumenta orcamento quando ROAS esta alto",
                "conditions": [{"type": "roas_above", "value": 3.0}],
                "actions": [{"type": "increase_budget", "value": 20}],
                "category": "scaling"
            },
            "alert_low_ctr": {
                "name": "Alerta CTR Baixo",
                "description": "Envia alerta quando CTR cai muito",
                "conditions": [{"type": "ctr_below", "value": 0.5}],
                "actions": [{"type": "send_alert", "channel": "email"}],
                "category": "monitoring"
            },
            "rotate_creative_fatigue": {
                "name": "Rotacionar Criativo Cansado",
                "description": "Troca criativo quando frequencia alta",
                "conditions": [{"type": "frequency_above", "value": 3.0}],
                "actions": [{"type": "rotate_creative", "delay": 0}],
                "category": "creative_management"
            },
            "budget_protection": {
                "name": "Protecao de Orcamento",
                "description": "Pausa campanha se gastar muito rapido",
                "conditions": [{"type": "spend_rate_above", "value": 150}],
                "actions": [{"type": "pause_campaign", "delay": 0}],
                "category": "cost_control"
            }
        }
    
    def _init_workflow_templates(self) -> Dict[str, Dict]:
        """Inicializa templates de workflows."""
        
        return {
            "new_campaign_launch": {
                "name": "Lancamento de Nova Campanha",
                "description": "Workflow completo para lancar nova campanha",
                "steps": [
                    {"order": 1, "action": "create_campaign", "wait_hours": 0},
                    {"order": 2, "action": "monitor_learning", "wait_hours": 24},
                    {"order": 3, "action": "evaluate_performance", "wait_hours": 72},
                    {"order": 4, "action": "optimize_or_scale", "wait_hours": 0}
                ]
            },
            "creative_testing": {
                "name": "Teste de Criativos",
                "description": "Workflow para testar novos criativos",
                "steps": [
                    {"order": 1, "action": "create_test_adset", "wait_hours": 0},
                    {"order": 2, "action": "distribute_budget", "wait_hours": 0},
                    {"order": 3, "action": "collect_data", "wait_hours": 72},
                    {"order": 4, "action": "analyze_results", "wait_hours": 0},
                    {"order": 5, "action": "declare_winner", "wait_hours": 0}
                ]
            },
            "scaling_sequence": {
                "name": "Sequencia de Escala",
                "description": "Workflow para escalar campanhas vencedoras",
                "steps": [
                    {"order": 1, "action": "verify_stability", "wait_hours": 0},
                    {"order": 2, "action": "increase_budget_20", "wait_hours": 72},
                    {"order": 3, "action": "monitor_metrics", "wait_hours": 24},
                    {"order": 4, "action": "continue_or_pause", "wait_hours": 0}
                ]
            }
        }
    
    def _init_conditions(self) -> Dict[str, Dict]:
        """Inicializa condicoes disponiveis."""
        
        return {
            "cpa_above": {"name": "CPA acima de", "type": "numeric", "unit": "R$"},
            "cpa_below": {"name": "CPA abaixo de", "type": "numeric", "unit": "R$"},
            "roas_above": {"name": "ROAS acima de", "type": "numeric", "unit": "x"},
            "roas_below": {"name": "ROAS abaixo de", "type": "numeric", "unit": "x"},
            "ctr_above": {"name": "CTR acima de", "type": "numeric", "unit": "%"},
            "ctr_below": {"name": "CTR abaixo de", "type": "numeric", "unit": "%"},
            "cpc_above": {"name": "CPC acima de", "type": "numeric", "unit": "R$"},
            "cpc_below": {"name": "CPC abaixo de", "type": "numeric", "unit": "R$"},
            "spend_above": {"name": "Gasto acima de", "type": "numeric", "unit": "R$"},
            "spend_below": {"name": "Gasto abaixo de", "type": "numeric", "unit": "R$"},
            "conversions_above": {"name": "Conversoes acima de", "type": "numeric", "unit": ""},
            "conversions_below": {"name": "Conversoes abaixo de", "type": "numeric", "unit": ""},
            "frequency_above": {"name": "Frequencia acima de", "type": "numeric", "unit": "x"},
            "spend_rate_above": {"name": "Taxa de gasto acima de", "type": "numeric", "unit": "%"},
            "time_of_day": {"name": "Horario do dia", "type": "time_range", "unit": ""},
            "day_of_week": {"name": "Dia da semana", "type": "day_select", "unit": ""}
        }
    
    def _init_actions(self) -> Dict[str, Dict]:
        """Inicializa acoes disponiveis."""
        
        return {
            "pause_ad": {"name": "Pausar anuncio", "category": "control"},
            "pause_adset": {"name": "Pausar conjunto", "category": "control"},
            "pause_campaign": {"name": "Pausar campanha", "category": "control"},
            "activate_ad": {"name": "Ativar anuncio", "category": "control"},
            "activate_adset": {"name": "Ativar conjunto", "category": "control"},
            "activate_campaign": {"name": "Ativar campanha", "category": "control"},
            "increase_budget": {"name": "Aumentar orcamento", "category": "budget", "param": "percentage"},
            "decrease_budget": {"name": "Diminuir orcamento", "category": "budget", "param": "percentage"},
            "set_budget": {"name": "Definir orcamento", "category": "budget", "param": "value"},
            "increase_bid": {"name": "Aumentar lance", "category": "bidding", "param": "percentage"},
            "decrease_bid": {"name": "Diminuir lance", "category": "bidding", "param": "percentage"},
            "rotate_creative": {"name": "Rotacionar criativo", "category": "creative"},
            "duplicate_adset": {"name": "Duplicar conjunto", "category": "scaling"},
            "send_alert": {"name": "Enviar alerta", "category": "notification", "param": "channel"},
            "send_report": {"name": "Enviar relatorio", "category": "notification", "param": "type"},
            "add_tag": {"name": "Adicionar tag", "category": "organization", "param": "tag"},
            "remove_tag": {"name": "Remover tag", "category": "organization", "param": "tag"}
        }
    
    def create_rule(self, rule_config: Dict) -> Dict[str, Any]:
        """Cria uma nova regra de automacao."""
        
        rule_id = f"rule_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        rule = {
            "id": rule_id,
            "name": rule_config.get("name", f"Regra {rule_id}"),
            "description": rule_config.get("description", ""),
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "conditions": rule_config.get("conditions", []),
            "actions": rule_config.get("actions", []),
            "scope": rule_config.get("scope", {"type": "all"}),
            "schedule": rule_config.get("schedule", {"type": "continuous"}),
            "execution_count": 0,
            "last_executed": None
        }
        
        # Validar condicoes
        for condition in rule["conditions"]:
            if condition.get("type") not in self.available_conditions:
                return {"error": f"Condicao invalida: {condition.get('type')}"}
        
        # Validar acoes
        for action in rule["actions"]:
            if action.get("type") not in self.available_actions:
                return {"error": f"Acao invalida: {action.get('type')}"}
        
        self.active_rules[rule_id] = rule
        
        return {
            "status": "created",
            "rule_id": rule_id,
            "rule": rule
        }
    
    def create_rule_from_template(self, template_id: str, customizations: Dict = None) -> Dict[str, Any]:
        """Cria regra a partir de template."""
        
        if template_id not in self.rule_templates:
            return {"error": f"Template nao encontrado: {template_id}"}
        
        template = self.rule_templates[template_id].copy()
        
        # Aplicar customizacoes
        if customizations:
            if "conditions" in customizations:
                for i, cond in enumerate(customizations["conditions"]):
                    if i < len(template["conditions"]):
                        template["conditions"][i].update(cond)
            
            if "actions" in customizations:
                for i, act in enumerate(customizations["actions"]):
                    if i < len(template["actions"]):
                        template["actions"][i].update(act)
            
            if "name" in customizations:
                template["name"] = customizations["name"]
        
        return self.create_rule(template)
    
    def evaluate_rule(self, rule_id: str, metrics: Dict) -> Dict[str, Any]:
        """Avalia se uma regra deve ser executada."""
        
        if rule_id not in self.active_rules:
            return {"error": "Regra nao encontrada"}
        
        rule = self.active_rules[rule_id]
        
        if rule["status"] != "active":
            return {"should_execute": False, "reason": "Regra inativa"}
        
        # Avaliar todas as condicoes
        conditions_met = []
        for condition in rule["conditions"]:
            met = self._evaluate_condition(condition, metrics)
            conditions_met.append({
                "condition": condition,
                "met": met
            })
        
        # Todas as condicoes devem ser atendidas (AND)
        all_met = all(c["met"] for c in conditions_met)
        
        return {
            "rule_id": rule_id,
            "should_execute": all_met,
            "conditions_evaluated": conditions_met,
            "metrics_used": metrics
        }
    
    def execute_rule(self, rule_id: str, target: Dict) -> Dict[str, Any]:
        """Executa uma regra."""
        
        if rule_id not in self.active_rules:
            return {"error": "Regra nao encontrada"}
        
        rule = self.active_rules[rule_id]
        
        execution = {
            "rule_id": rule_id,
            "executed_at": datetime.now().isoformat(),
            "target": target,
            "actions_executed": [],
            "status": "success"
        }
        
        # Executar cada acao
        for action in rule["actions"]:
            action_result = self._execute_action(action, target)
            execution["actions_executed"].append({
                "action": action,
                "result": action_result
            })
            
            if not action_result.get("success"):
                execution["status"] = "partial_failure"
        
        # Atualizar estatisticas da regra
        rule["execution_count"] += 1
        rule["last_executed"] = execution["executed_at"]
        
        # Registrar no historico
        self.execution_history.append(execution)
        
        return execution
    
    def create_workflow(self, workflow_config: Dict) -> Dict[str, Any]:
        """Cria um novo workflow."""
        
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        workflow = {
            "id": workflow_id,
            "name": workflow_config.get("name", f"Workflow {workflow_id}"),
            "description": workflow_config.get("description", ""),
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "steps": workflow_config.get("steps", []),
            "trigger": workflow_config.get("trigger", {"type": "manual"}),
            "current_step": 0,
            "executions": []
        }
        
        self.workflows[workflow_id] = workflow
        
        return {
            "status": "created",
            "workflow_id": workflow_id,
            "workflow": workflow
        }
    
    def start_workflow(self, workflow_id: str, context: Dict = None) -> Dict[str, Any]:
        """Inicia execucao de um workflow."""
        
        if workflow_id not in self.workflows:
            return {"error": "Workflow nao encontrado"}
        
        workflow = self.workflows[workflow_id]
        
        execution = {
            "execution_id": f"exec_{random.randint(10000, 99999)}",
            "started_at": datetime.now().isoformat(),
            "context": context or {},
            "current_step": 1,
            "status": "running",
            "steps_completed": []
        }
        
        workflow["status"] = "running"
        workflow["executions"].append(execution)
        
        return {
            "status": "started",
            "workflow_id": workflow_id,
            "execution_id": execution["execution_id"],
            "first_step": workflow["steps"][0] if workflow["steps"] else None
        }
    
    def advance_workflow(self, workflow_id: str, execution_id: str) -> Dict[str, Any]:
        """Avanca workflow para proximo passo."""
        
        if workflow_id not in self.workflows:
            return {"error": "Workflow nao encontrado"}
        
        workflow = self.workflows[workflow_id]
        
        execution = next((e for e in workflow["executions"] if e["execution_id"] == execution_id), None)
        if not execution:
            return {"error": "Execucao nao encontrada"}
        
        current_step = execution["current_step"]
        
        if current_step >= len(workflow["steps"]):
            execution["status"] = "completed"
            execution["completed_at"] = datetime.now().isoformat()
            return {
                "status": "completed",
                "workflow_id": workflow_id,
                "execution_id": execution_id
            }
        
        # Marcar passo atual como completo
        execution["steps_completed"].append({
            "step": current_step,
            "completed_at": datetime.now().isoformat()
        })
        
        # Avancar para proximo
        execution["current_step"] += 1
        
        next_step = workflow["steps"][execution["current_step"] - 1] if execution["current_step"] <= len(workflow["steps"]) else None
        
        return {
            "status": "advanced",
            "workflow_id": workflow_id,
            "execution_id": execution_id,
            "current_step": execution["current_step"],
            "next_step": next_step
        }
    
    def get_rule_templates(self, category: str = None) -> Dict[str, Any]:
        """Obtem templates de regras."""
        
        templates = self.rule_templates
        
        if category:
            templates = {k: v for k, v in templates.items() if v.get("category") == category}
        
        return {
            "templates": templates,
            "categories": list(set(t.get("category") for t in self.rule_templates.values()))
        }
    
    def get_available_conditions(self) -> Dict[str, Any]:
        """Obtem condicoes disponiveis."""
        
        return {
            "conditions": self.available_conditions,
            "total": len(self.available_conditions)
        }
    
    def get_available_actions(self) -> Dict[str, Any]:
        """Obtem acoes disponiveis."""
        
        return {
            "actions": self.available_actions,
            "categories": list(set(a.get("category") for a in self.available_actions.values()))
        }
    
    def get_rule_status(self, rule_id: str) -> Dict[str, Any]:
        """Obtem status de uma regra."""
        
        if rule_id not in self.active_rules:
            return {"error": "Regra nao encontrada"}
        
        rule = self.active_rules[rule_id]
        
        return {
            "rule_id": rule_id,
            "name": rule["name"],
            "status": rule["status"],
            "execution_count": rule["execution_count"],
            "last_executed": rule["last_executed"],
            "conditions_count": len(rule["conditions"]),
            "actions_count": len(rule["actions"])
        }
    
    def pause_rule(self, rule_id: str) -> Dict[str, Any]:
        """Pausa uma regra."""
        
        if rule_id not in self.active_rules:
            return {"error": "Regra nao encontrada"}
        
        self.active_rules[rule_id]["status"] = "paused"
        self.active_rules[rule_id]["paused_at"] = datetime.now().isoformat()
        
        return {
            "status": "paused",
            "rule_id": rule_id
        }
    
    def activate_rule(self, rule_id: str) -> Dict[str, Any]:
        """Ativa uma regra."""
        
        if rule_id not in self.active_rules:
            return {"error": "Regra nao encontrada"}
        
        self.active_rules[rule_id]["status"] = "active"
        self.active_rules[rule_id]["activated_at"] = datetime.now().isoformat()
        
        return {
            "status": "activated",
            "rule_id": rule_id
        }
    
    def delete_rule(self, rule_id: str) -> Dict[str, Any]:
        """Deleta uma regra."""
        
        if rule_id not in self.active_rules:
            return {"error": "Regra nao encontrada"}
        
        del self.active_rules[rule_id]
        
        return {
            "status": "deleted",
            "rule_id": rule_id
        }
    
    def get_execution_history(self, filters: Dict = None) -> Dict[str, Any]:
        """Obtem historico de execucoes."""
        
        history = self.execution_history.copy()
        
        if filters:
            if filters.get("rule_id"):
                history = [h for h in history if h.get("rule_id") == filters["rule_id"]]
            if filters.get("status"):
                history = [h for h in history if h.get("status") == filters["status"]]
        
        return {
            "total_executions": len(history),
            "executions": history[-50:],  # Ultimas 50
            "retrieved_at": datetime.now().isoformat()
        }
    
    def get_automation_report(self) -> Dict[str, Any]:
        """Gera relatorio de automacao."""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_rules": len(self.active_rules),
                "active_rules": sum(1 for r in self.active_rules.values() if r["status"] == "active"),
                "paused_rules": sum(1 for r in self.active_rules.values() if r["status"] == "paused"),
                "total_workflows": len(self.workflows),
                "total_executions": len(self.execution_history)
            },
            "rules_by_category": {},
            "top_executed_rules": [],
            "recent_executions": self.execution_history[-10:]
        }
        
        # Regras por categoria
        for rule in self.active_rules.values():
            category = "uncategorized"
            for template in self.rule_templates.values():
                if template["name"] == rule["name"]:
                    category = template.get("category", "uncategorized")
                    break
            
            if category not in report["rules_by_category"]:
                report["rules_by_category"][category] = 0
            report["rules_by_category"][category] += 1
        
        # Top regras executadas
        sorted_rules = sorted(self.active_rules.values(), key=lambda x: x["execution_count"], reverse=True)
        report["top_executed_rules"] = [
            {"name": r["name"], "executions": r["execution_count"]}
            for r in sorted_rules[:5]
        ]
        
        return report
    
    def _evaluate_condition(self, condition: Dict, metrics: Dict) -> bool:
        """Avalia uma condicao."""
        
        condition_type = condition.get("type")
        threshold = condition.get("value", 0)
        
        # Mapear tipo de condicao para metrica
        metric_map = {
            "cpa_above": ("cpa", lambda v, t: v > t),
            "cpa_below": ("cpa", lambda v, t: v < t),
            "roas_above": ("roas", lambda v, t: v > t),
            "roas_below": ("roas", lambda v, t: v < t),
            "ctr_above": ("ctr", lambda v, t: v > t),
            "ctr_below": ("ctr", lambda v, t: v < t),
            "cpc_above": ("cpc", lambda v, t: v > t),
            "cpc_below": ("cpc", lambda v, t: v < t),
            "spend_above": ("spend", lambda v, t: v > t),
            "spend_below": ("spend", lambda v, t: v < t),
            "conversions_above": ("conversions", lambda v, t: v > t),
            "conversions_below": ("conversions", lambda v, t: v < t),
            "frequency_above": ("frequency", lambda v, t: v > t),
            "spend_rate_above": ("spend_rate", lambda v, t: v > t)
        }
        
        if condition_type in metric_map:
            metric_name, comparator = metric_map[condition_type]
            metric_value = metrics.get(metric_name, 0)
            return comparator(metric_value, threshold)
        
        return False
    
    def _execute_action(self, action: Dict, target: Dict) -> Dict[str, Any]:
        """Executa uma acao."""
        
        action_type = action.get("type")
        
        # Simulacao de execucao (em producao conectaria com APIs)
        result = {
            "action": action_type,
            "target": target,
            "success": True,
            "executed_at": datetime.now().isoformat()
        }
        
        if action_type in ["pause_ad", "pause_adset", "pause_campaign"]:
            result["message"] = f"Pausado: {target.get('id', 'unknown')}"
        elif action_type in ["activate_ad", "activate_adset", "activate_campaign"]:
            result["message"] = f"Ativado: {target.get('id', 'unknown')}"
        elif action_type == "increase_budget":
            percentage = action.get("value", 20)
            result["message"] = f"Orcamento aumentado em {percentage}%"
        elif action_type == "decrease_budget":
            percentage = action.get("value", 20)
            result["message"] = f"Orcamento reduzido em {percentage}%"
        elif action_type == "send_alert":
            channel = action.get("channel", "email")
            result["message"] = f"Alerta enviado via {channel}"
        else:
            result["message"] = f"Acao executada: {action_type}"
        
        return result


# Instancia global
automation_hub = AutomationHub()

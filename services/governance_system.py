# services/governance_system.py
"""
NEXORA PRIME - Sistema de Governança Enterprise
Controle de versões, rollback, auditoria e compliance
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any


class GovernanceSystem:
    """Sistema de Governança para controle de versões, rollback e auditoria."""
    
    def __init__(self):
        self.version_history = []
        self.audit_logs = []
        self.current_version = "1.0.0"
        self.rollback_points = []
        self.compliance_rules = {
            "max_budget_change_percent": 50,
            "require_approval_above": 10000,
            "audit_retention_days": 365,
            "max_concurrent_changes": 5
        }
    
    def create_version(self, entity_type: str, entity_id: str, data: Dict, user: str = "system") -> Dict:
        """Cria uma nova versão de uma entidade (campanha, regra, etc.)."""
        version_id = self._generate_version_id(entity_type, entity_id, data)
        
        version_record = {
            "version_id": version_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": data,
            "created_at": datetime.now().isoformat(),
            "created_by": user,
            "checksum": self._calculate_checksum(data),
            "is_current": True
        }
        
        # Marcar versões anteriores como não-atuais
        for v in self.version_history:
            if v["entity_type"] == entity_type and v["entity_id"] == entity_id:
                v["is_current"] = False
        
        self.version_history.append(version_record)
        self._log_audit("VERSION_CREATED", f"Nova versão criada: {version_id}", user)
        
        return version_record
    
    def rollback(self, entity_type: str, entity_id: str, target_version_id: str, user: str = "system") -> Dict:
        """Faz rollback para uma versão anterior."""
        target_version = None
        
        for v in self.version_history:
            if v["version_id"] == target_version_id:
                target_version = v
                break
        
        if not target_version:
            return {"success": False, "error": "Versão não encontrada"}
        
        # Criar nova versão com os dados antigos
        new_version = self.create_version(
            entity_type=entity_type,
            entity_id=entity_id,
            data=target_version["data"],
            user=user
        )
        
        self._log_audit(
            "ROLLBACK_EXECUTED",
            f"Rollback de {entity_id} para versão {target_version_id}",
            user
        )
        
        return {
            "success": True,
            "new_version": new_version,
            "rolled_back_from": target_version_id
        }
    
    def get_version_history(self, entity_type: str, entity_id: str) -> List[Dict]:
        """Retorna o histórico de versões de uma entidade."""
        return [
            v for v in self.version_history
            if v["entity_type"] == entity_type and v["entity_id"] == entity_id
        ]
    
    def get_audit_logs(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
        """Retorna logs de auditoria filtrados por data."""
        logs = self.audit_logs
        
        if start_date:
            logs = [l for l in logs if l["timestamp"] >= start_date]
        if end_date:
            logs = [l for l in logs if l["timestamp"] <= end_date]
        
        return logs
    
    def check_compliance(self, action: str, context: Dict) -> Dict:
        """Verifica se uma ação está em conformidade com as regras."""
        violations = []
        
        if action == "budget_change":
            current_budget = context.get("current_budget", 0)
            new_budget = context.get("new_budget", 0)
            
            if current_budget > 0:
                change_percent = abs((new_budget - current_budget) / current_budget) * 100
                if change_percent > self.compliance_rules["max_budget_change_percent"]:
                    violations.append({
                        "rule": "max_budget_change_percent",
                        "message": f"Mudança de orçamento de {change_percent:.1f}% excede o limite de {self.compliance_rules['max_budget_change_percent']}%"
                    })
            
            if new_budget > self.compliance_rules["require_approval_above"]:
                violations.append({
                    "rule": "require_approval_above",
                    "message": f"Orçamento de R${new_budget:,.2f} requer aprovação manual",
                    "requires_approval": True
                })
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations
        }
    
    def create_rollback_point(self, name: str, description: str, user: str = "system") -> Dict:
        """Cria um ponto de rollback nomeado (snapshot do sistema)."""
        rollback_point = {
            "id": f"RP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "created_by": user,
            "version_snapshot": [v for v in self.version_history if v["is_current"]]
        }
        
        self.rollback_points.append(rollback_point)
        self._log_audit("ROLLBACK_POINT_CREATED", f"Ponto de rollback criado: {name}", user)
        
        return rollback_point
    
    def _generate_version_id(self, entity_type: str, entity_id: str, data: Dict) -> str:
        """Gera um ID único para a versão."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"{entity_type}_{entity_id}_v{timestamp}"
    
    def _calculate_checksum(self, data: Dict) -> str:
        """Calcula checksum dos dados para verificação de integridade."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def _log_audit(self, action: str, details: str, user: str):
        """Registra uma entrada no log de auditoria."""
        self.audit_logs.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "user": user
        })
    
    def create_policy(self, name: str, policy_type: str, rules: Dict, scope: str = "all") -> Dict:
        """Cria uma nova política de governança."""
        policy_id = f"POL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        policy = {
            "id": policy_id,
            "name": name,
            "type": policy_type,
            "rules": rules,
            "scope": scope,
            "limit": rules.get("max_daily_spend", 0),
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        self.compliance_rules[policy_id] = policy
        self._log_audit("create_policy", f"Política criada: {name}", "system")
        return {"success": True, "policy": policy}
    
    def get_system_status(self) -> Dict:
        """Retorna o status atual do sistema de governança."""
        return {
            "current_version": self.current_version,
            "total_versions": len(self.version_history),
            "total_audit_logs": len(self.audit_logs),
            "rollback_points": len(self.rollback_points),
            "compliance_rules": self.compliance_rules,
            "last_audit": self.audit_logs[-1] if self.audit_logs else None
        }


# Instância global
governance_system = GovernanceSystem()

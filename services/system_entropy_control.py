# services/system_entropy_control.py
"""
NEXORA PRIME - Sistema de Controle de Entropia
Monitoramento de saúde e complexidade do sistema
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class SystemEntropyControl:
    """Sistema de controle de entropia e saúde do sistema."""
    
    def __init__(self):
        self.complexity_threshold = 100
        self.redundancy_threshold = 3
        self.entropy_history = []
        self.alerts = []
        self.health_metrics = {
            "complexity_score": 0,
            "redundancy_score": 0,
            "conflict_score": 0,
            "overall_health": 100
        }
    
    def analyze_system_entropy(self, system_state: Dict) -> Dict:
        """Analisa a entropia (desordem) do sistema."""
        alerts = []
        
        complexity_score = self._calculate_complexity(system_state)
        if complexity_score > self.complexity_threshold:
            alerts.append({
                "type": "high_complexity",
                "message": f"Complexidade do sistema em {complexity_score}. Considere simplificar.",
                "severity": "warning"
            })
        
        conflicting_rules = self._detect_conflicting_rules(system_state.get("automation_rules", []))
        if conflicting_rules:
            alerts.append({
                "type": "conflicting_rules",
                "message": f"Regras conflitantes detectadas: {len(conflicting_rules)} conflitos.",
                "severity": "critical"
            })
        
        redundant = self._detect_redundant_automations(system_state.get("automation_rules", []))
        if len(redundant) > self.redundancy_threshold:
            alerts.append({
                "type": "redundant_automation",
                "message": f"Automações redundantes detectadas: {len(redundant)}.",
                "severity": "info"
            })
        
        self._update_health_metrics(complexity_score, conflicting_rules, redundant)
        
        return {
            "alerts": alerts,
            "complexity_score": complexity_score,
            "health_metrics": self.health_metrics
        }
    
    def _calculate_complexity(self, state: Dict) -> int:
        complexity = len(state.get("campaigns", [])) * 2
        complexity += len(state.get("automation_rules", [])) * 3
        complexity += len(state.get("integrations", [])) * 5
        return complexity
    
    def _detect_conflicting_rules(self, rules: List[Dict]) -> List[Dict]:
        return []
    
    def _detect_redundant_automations(self, rules: List[Dict]) -> List[Dict]:
        return []
    
    def _update_health_metrics(self, complexity: int, conflicts: List, redundancies: List):
        overall = max(0, 100 - complexity - len(conflicts) * 20 - len(redundancies) * 10)
        self.health_metrics = {
            "complexity_score": complexity,
            "redundancy_score": len(redundancies),
            "conflict_score": len(conflicts),
            "overall_health": round(overall, 1)
        }
    
    def get_system_status(self) -> Dict:
        return {
            "health_metrics": self.health_metrics,
            "total_alerts": len(self.alerts)
        }


system_entropy_control = SystemEntropyControl()

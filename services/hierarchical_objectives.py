# services/hierarchical_objectives.py
"""
NEXORA PRIME - Sistema de Objetivos Hierárquicos
Conecta objetivos de negócio a KPIs de campanha
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class HierarchicalObjectives:
    """Sistema de objetivos hierárquicos conectando metas de negócio a campanhas."""
    
    def __init__(self):
        self.objectives_tree = {
            "business": [],
            "marketing": [],
            "campaign": [],
            "tactical": []
        }
        self.objective_links = []
        self.progress_tracking = {}
    
    def create_objective(self, level: str, name: str, target_value: float, 
                        metric: str, deadline: str, parent_id: Optional[str] = None) -> Dict:
        """Cria um novo objetivo em qualquer nível da hierarquia."""
        objective = {
            "id": f"OBJ_{level.upper()}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "level": level,
            "name": name,
            "target_value": target_value,
            "current_value": 0,
            "metric": metric,
            "deadline": deadline,
            "parent_id": parent_id,
            "children_ids": [],
            "status": "active",
            "progress": 0,
            "created_at": datetime.now().isoformat()
        }
        
        if level in self.objectives_tree:
            self.objectives_tree[level].append(objective)
        
        # Vincular ao pai se especificado
        if parent_id:
            self._link_to_parent(objective["id"], parent_id)
        
        # Inicializar tracking de progresso
        self.progress_tracking[objective["id"]] = {
            "history": [],
            "last_updated": datetime.now().isoformat()
        }
        
        return objective
    
    def update_progress(self, objective_id: str, current_value: float) -> Dict:
        """Atualiza o progresso de um objetivo."""
        objective = self._find_objective(objective_id)
        if not objective:
            return {"success": False, "error": "Objetivo não encontrado"}
        
        objective["current_value"] = current_value
        objective["progress"] = min(100, (current_value / objective["target_value"]) * 100) if objective["target_value"] > 0 else 0
        
        # Registrar no histórico
        if objective_id in self.progress_tracking:
            self.progress_tracking[objective_id]["history"].append({
                "value": current_value,
                "progress": objective["progress"],
                "timestamp": datetime.now().isoformat()
            })
            self.progress_tracking[objective_id]["last_updated"] = datetime.now().isoformat()
        
        # Propagar para objetivos pai
        if objective.get("parent_id"):
            self._update_parent_progress(objective["parent_id"])
        
        return {
            "success": True,
            "objective_id": objective_id,
            "current_value": current_value,
            "progress": objective["progress"]
        }
    
    def get_objective_cascade(self, objective_id: str) -> Dict:
        """Retorna a cascata completa de um objetivo (pais e filhos)."""
        objective = self._find_objective(objective_id)
        if not objective:
            return {"error": "Objetivo não encontrado"}
        
        cascade = {
            "objective": objective,
            "parent": None,
            "children": []
        }
        
        # Buscar pai
        if objective.get("parent_id"):
            cascade["parent"] = self._find_objective(objective["parent_id"])
        
        # Buscar filhos
        for child_id in objective.get("children_ids", []):
            child = self._find_objective(child_id)
            if child:
                cascade["children"].append(child)
        
        return cascade
    
    def get_objectives_by_level(self, level: str) -> List[Dict]:
        """Retorna todos os objetivos de um nível específico."""
        return self.objectives_tree.get(level, [])
    
    def get_all_objectives(self) -> Dict:
        """Retorna todos os objetivos organizados por nível."""
        return self.objectives_tree
    
    def calculate_alignment_score(self, campaign_id: str) -> Dict:
        """Calcula o score de alinhamento de uma campanha com objetivos de negócio."""
        # Encontrar objetivos táticos vinculados à campanha
        tactical_objectives = [
            obj for obj in self.objectives_tree["tactical"]
            if obj.get("campaign_id") == campaign_id
        ]
        
        if not tactical_objectives:
            return {
                "campaign_id": campaign_id,
                "alignment_score": 0,
                "message": "Nenhum objetivo tático vinculado a esta campanha"
            }
        
        # Calcular score baseado no progresso dos objetivos
        total_progress = sum(obj["progress"] for obj in tactical_objectives)
        avg_progress = total_progress / len(tactical_objectives)
        
        # Verificar alinhamento com objetivos superiores
        aligned_with_marketing = any(obj.get("parent_id") for obj in tactical_objectives)
        
        alignment_score = avg_progress * (1.2 if aligned_with_marketing else 0.8)
        
        return {
            "campaign_id": campaign_id,
            "alignment_score": min(100, round(alignment_score, 1)),
            "tactical_objectives_count": len(tactical_objectives),
            "aligned_with_marketing": aligned_with_marketing,
            "recommendation": self._get_alignment_recommendation(alignment_score)
        }
    
    def get_objective_insights(self, objective_id: str) -> Dict:
        """Gera insights sobre um objetivo específico."""
        objective = self._find_objective(objective_id)
        if not objective:
            return {"error": "Objetivo não encontrado"}
        
        tracking = self.progress_tracking.get(objective_id, {})
        history = tracking.get("history", [])
        
        insights = {
            "objective_id": objective_id,
            "current_status": "on_track" if objective["progress"] >= 50 else "at_risk",
            "days_to_deadline": self._calculate_days_to_deadline(objective["deadline"]),
            "velocity": self._calculate_velocity(history),
            "projected_completion": None,
            "recommendations": []
        }
        
        # Projetar conclusão
        if insights["velocity"] > 0:
            remaining = objective["target_value"] - objective["current_value"]
            days_needed = remaining / insights["velocity"]
            insights["projected_completion"] = f"{int(days_needed)} dias"
            
            if days_needed > insights["days_to_deadline"]:
                insights["recommendations"].append("Aumentar investimento para atingir meta no prazo")
        
        return insights
    
    def _find_objective(self, objective_id: str) -> Optional[Dict]:
        """Busca um objetivo pelo ID em todos os níveis."""
        for level in self.objectives_tree.values():
            for obj in level:
                if obj["id"] == objective_id:
                    return obj
        return None
    
    def _link_to_parent(self, child_id: str, parent_id: str):
        """Vincula um objetivo filho ao pai."""
        parent = self._find_objective(parent_id)
        if parent:
            if "children_ids" not in parent:
                parent["children_ids"] = []
            parent["children_ids"].append(child_id)
            
            self.objective_links.append({
                "parent_id": parent_id,
                "child_id": child_id,
                "linked_at": datetime.now().isoformat()
            })
    
    def _update_parent_progress(self, parent_id: str):
        """Atualiza o progresso do pai baseado nos filhos."""
        parent = self._find_objective(parent_id)
        if not parent or not parent.get("children_ids"):
            return
        
        children_progress = []
        for child_id in parent["children_ids"]:
            child = self._find_objective(child_id)
            if child:
                children_progress.append(child["progress"])
        
        if children_progress:
            parent["progress"] = sum(children_progress) / len(children_progress)
    
    def _calculate_days_to_deadline(self, deadline: str) -> int:
        """Calcula dias até o deadline."""
        try:
            deadline_date = datetime.fromisoformat(deadline)
            return (deadline_date - datetime.now()).days
        except:
            return 30  # Default
    
    def _calculate_velocity(self, history: List[Dict]) -> float:
        """Calcula a velocidade de progresso."""
        if len(history) < 2:
            return 0
        
        # Usar últimos 7 registros
        recent = history[-7:]
        if len(recent) < 2:
            return 0
        
        value_change = recent[-1]["value"] - recent[0]["value"]
        return max(0, value_change / len(recent))
    
    def _get_alignment_recommendation(self, score: float) -> str:
        """Gera recomendação baseada no score de alinhamento."""
        if score >= 80:
            return "Excelente alinhamento! Mantenha a estratégia atual."
        elif score >= 50:
            return "Bom alinhamento. Considere otimizar para melhorar resultados."
        else:
            return "Alinhamento baixo. Revise a estratégia da campanha."
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de objetivos."""
        total_objectives = sum(len(level) for level in self.objectives_tree.values())
        
        return {
            "total_objectives": total_objectives,
            "objectives_by_level": {k: len(v) for k, v in self.objectives_tree.items()},
            "total_links": len(self.objective_links)
        }


# Instância global
hierarchical_objectives = HierarchicalObjectives()

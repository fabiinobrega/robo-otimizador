# services/human_ai_collaboration.py
"""
NEXORA PRIME - Colaboração Humano-IA Avançada
Feedback loops e aprendizado com interações humanas
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class HumanAICollaboration:
    """Sistema de colaboração avançada entre humanos e IA."""
    
    def __init__(self):
        self.feedback_history = []
        self.pending_approvals = []
        self.learning_data = []
        self.user_preferences = {}
        self.collaboration_metrics = {
            "total_interactions": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "approvals_requested": 0,
            "approvals_granted": 0
        }
    
    def request_approval(self, action: Dict, reason: str, urgency: str = "normal") -> Dict:
        """Solicita aprovação humana para uma ação."""
        approval_request = {
            "id": f"APR_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "action": action,
            "reason": reason,
            "urgency": urgency,
            "status": "pending",
            "requested_at": datetime.now().isoformat(),
            "expires_at": None,
            "response": None
        }
        
        self.pending_approvals.append(approval_request)
        self.collaboration_metrics["approvals_requested"] += 1
        
        return approval_request
    
    def process_approval_response(self, approval_id: str, approved: bool, 
                                  feedback: Optional[str] = None) -> Dict:
        """Processa a resposta de aprovação do usuário."""
        for approval in self.pending_approvals:
            if approval["id"] == approval_id:
                approval["status"] = "approved" if approved else "rejected"
                approval["response"] = {
                    "approved": approved,
                    "feedback": feedback,
                    "responded_at": datetime.now().isoformat()
                }
                
                if approved:
                    self.collaboration_metrics["approvals_granted"] += 1
                
                # Aprender com a decisão
                self._learn_from_decision(approval, approved, feedback)
                
                return {
                    "success": True,
                    "approval_id": approval_id,
                    "status": approval["status"]
                }
        
        return {"success": False, "error": "Solicitação de aprovação não encontrada"}
    
    def submit_feedback(self, context: Dict, feedback_type: str, 
                       rating: int, comments: Optional[str] = None) -> Dict:
        """Recebe feedback do usuário sobre uma ação ou recomendação."""
        feedback = {
            "id": f"FB_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "context": context,
            "type": feedback_type,
            "rating": rating,
            "comments": comments,
            "submitted_at": datetime.now().isoformat()
        }
        
        self.feedback_history.append(feedback)
        self.collaboration_metrics["total_interactions"] += 1
        
        if rating >= 4:
            self.collaboration_metrics["positive_feedback"] += 1
        elif rating <= 2:
            self.collaboration_metrics["negative_feedback"] += 1
        
        # Aprender com o feedback
        self._learn_from_feedback(feedback)
        
        return {
            "success": True,
            "feedback_id": feedback["id"],
            "message": "Feedback registrado. Obrigado por ajudar a melhorar o sistema!"
        }
    
    def _learn_from_decision(self, approval: Dict, approved: bool, feedback: Optional[str]):
        """Aprende com decisões de aprovação."""
        learning = {
            "type": "approval_decision",
            "action_type": approval["action"].get("type"),
            "approved": approved,
            "feedback": feedback,
            "context": approval["action"].get("context", {}),
            "learned_at": datetime.now().isoformat()
        }
        self.learning_data.append(learning)
    
    def _learn_from_feedback(self, feedback: Dict):
        """Aprende com feedback do usuário."""
        learning = {
            "type": "user_feedback",
            "feedback_type": feedback["type"],
            "rating": feedback["rating"],
            "context": feedback["context"],
            "comments": feedback["comments"],
            "learned_at": datetime.now().isoformat()
        }
        self.learning_data.append(learning)
    
    def set_user_preferences(self, user_id: str, preferences: Dict) -> Dict:
        """Define preferências do usuário para colaboração."""
        self.user_preferences[user_id] = {
            **preferences,
            "updated_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "user_id": user_id,
            "preferences": self.user_preferences[user_id]
        }
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Retorna preferências do usuário."""
        return self.user_preferences.get(user_id, {
            "approval_threshold": "high_impact",
            "notification_frequency": "important_only",
            "automation_level": "supervised"
        })
    
    def should_request_approval(self, action: Dict, user_id: str) -> bool:
        """Determina se uma ação requer aprovação humana."""
        preferences = self.get_user_preferences(user_id)
        threshold = preferences.get("approval_threshold", "high_impact")
        
        action_impact = action.get("impact", "medium")
        
        if threshold == "all":
            return True
        elif threshold == "high_impact":
            return action_impact in ["high", "critical"]
        elif threshold == "critical_only":
            return action_impact == "critical"
        
        return False
    
    def get_pending_approvals(self, user_id: Optional[str] = None) -> List[Dict]:
        """Retorna aprovações pendentes."""
        pending = [a for a in self.pending_approvals if a["status"] == "pending"]
        return pending
    
    def get_collaboration_insights(self) -> Dict:
        """Gera insights sobre a colaboração humano-IA."""
        total = self.collaboration_metrics["total_interactions"]
        positive = self.collaboration_metrics["positive_feedback"]
        negative = self.collaboration_metrics["negative_feedback"]
        
        satisfaction_rate = positive / total if total > 0 else 0
        
        approval_rate = (
            self.collaboration_metrics["approvals_granted"] / 
            self.collaboration_metrics["approvals_requested"]
            if self.collaboration_metrics["approvals_requested"] > 0 else 0
        )
        
        return {
            "metrics": self.collaboration_metrics,
            "satisfaction_rate": round(satisfaction_rate, 2),
            "approval_rate": round(approval_rate, 2),
            "learning_data_points": len(self.learning_data),
            "insights": self._generate_collaboration_insights()
        }
    
    def _generate_collaboration_insights(self) -> List[str]:
        """Gera insights baseados nos dados de colaboração."""
        insights = []
        
        if self.collaboration_metrics["negative_feedback"] > self.collaboration_metrics["positive_feedback"]:
            insights.append("Feedback negativo predominante. Revisar qualidade das recomendações.")
        
        if self.collaboration_metrics["approvals_granted"] < self.collaboration_metrics["approvals_requested"] * 0.5:
            insights.append("Taxa de aprovação baixa. Ajustar critérios de solicitação.")
        
        if len(self.learning_data) > 100:
            insights.append("Base de aprendizado robusta. Considerar retreinamento do modelo.")
        
        if not insights:
            insights.append("Colaboração saudável. Manter padrões atuais.")
        
        return insights
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de colaboração."""
        return {
            "collaboration_metrics": self.collaboration_metrics,
            "pending_approvals_count": len([a for a in self.pending_approvals if a["status"] == "pending"]),
            "feedback_history_count": len(self.feedback_history),
            "learning_data_points": len(self.learning_data),
            "users_with_preferences": len(self.user_preferences)
        }


human_ai_collaboration = HumanAICollaboration()

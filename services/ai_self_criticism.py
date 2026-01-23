# services/ai_self_criticism.py
"""
NEXORA PRIME - Sistema de Auto-Crítica da IA
Meta-AI que avalia e melhora as decisões da IA principal
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class AISelfCriticism:
    """Sistema de auto-crítica e melhoria contínua da IA."""
    
    def __init__(self):
        self.decision_history = []
        self.evaluations = []
        self.improvement_suggestions = []
        self.confidence_calibration = {
            "total_predictions": 0,
            "correct_predictions": 0,
            "overconfident_count": 0,
            "underconfident_count": 0
        }
        self.bias_tracking = {}
    
    def evaluate_decision(self, decision: Dict, actual_outcome: Dict) -> Dict:
        """Avalia uma decisão da IA comparando com o resultado real."""
        evaluation = {
            "decision_id": decision.get("id", f"DEC_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
            "decision": decision,
            "actual_outcome": actual_outcome,
            "evaluated_at": datetime.now().isoformat(),
            "metrics": {}
        }
        
        # Calcular precisão da previsão
        predicted_value = decision.get("predicted_outcome", {}).get("value", 0)
        actual_value = actual_outcome.get("value", 0)
        
        if actual_value != 0:
            accuracy = 1 - abs(predicted_value - actual_value) / actual_value
            evaluation["metrics"]["accuracy"] = max(0, min(1, accuracy))
        else:
            evaluation["metrics"]["accuracy"] = 1 if predicted_value == 0 else 0
        
        # Avaliar confiança
        stated_confidence = decision.get("confidence", 0.5)
        was_correct = evaluation["metrics"]["accuracy"] > 0.8
        
        evaluation["metrics"]["confidence_calibration"] = self._evaluate_confidence(
            stated_confidence, was_correct
        )
        
        # Identificar vieses
        evaluation["metrics"]["potential_biases"] = self._detect_biases(decision)
        
        # Gerar crítica construtiva
        evaluation["criticism"] = self._generate_criticism(evaluation)
        
        # Sugerir melhorias
        evaluation["improvement_suggestions"] = self._suggest_improvements(evaluation)
        
        # Atualizar histórico
        self.decision_history.append(decision)
        self.evaluations.append(evaluation)
        self._update_calibration(stated_confidence, was_correct)
        
        return evaluation
    
    def _evaluate_confidence(self, stated_confidence: float, was_correct: bool) -> Dict:
        """Avalia se a confiança declarada estava calibrada."""
        if was_correct and stated_confidence < 0.7:
            return {"status": "underconfident", "message": "Confiança muito baixa para decisão correta"}
        elif not was_correct and stated_confidence > 0.8:
            return {"status": "overconfident", "message": "Confiança muito alta para decisão incorreta"}
        else:
            return {"status": "calibrated", "message": "Confiança bem calibrada"}
    
    def _detect_biases(self, decision: Dict) -> List[Dict]:
        """Detecta possíveis vieses na decisão."""
        biases = []
        
        # Viés de recência
        if decision.get("based_on_recent_data_only", False):
            biases.append({
                "type": "recency_bias",
                "description": "Decisão baseada apenas em dados recentes",
                "severity": "medium"
            })
        
        # Viés de confirmação
        if decision.get("ignored_contradicting_data", False):
            biases.append({
                "type": "confirmation_bias",
                "description": "Dados contraditórios podem ter sido ignorados",
                "severity": "high"
            })
        
        # Viés de ancoragem
        if decision.get("heavily_weighted_first_data", False):
            biases.append({
                "type": "anchoring_bias",
                "description": "Primeiro dado pode ter influenciado demais",
                "severity": "medium"
            })
        
        # Viés de otimismo
        predicted = decision.get("predicted_outcome", {}).get("value", 0)
        historical_avg = decision.get("historical_average", 0)
        if predicted > historical_avg * 1.5:
            biases.append({
                "type": "optimism_bias",
                "description": "Previsão significativamente acima da média histórica",
                "severity": "low"
            })
        
        return biases
    
    def _generate_criticism(self, evaluation: Dict) -> Dict:
        """Gera crítica construtiva sobre a decisão."""
        accuracy = evaluation["metrics"]["accuracy"]
        confidence_status = evaluation["metrics"]["confidence_calibration"]["status"]
        biases = evaluation["metrics"]["potential_biases"]
        
        criticism = {
            "overall_assessment": "",
            "strengths": [],
            "weaknesses": [],
            "learning_points": []
        }
        
        # Avaliação geral
        if accuracy > 0.9:
            criticism["overall_assessment"] = "Excelente decisão com alta precisão"
            criticism["strengths"].append("Alta precisão na previsão")
        elif accuracy > 0.7:
            criticism["overall_assessment"] = "Boa decisão com precisão aceitável"
            criticism["strengths"].append("Precisão dentro do esperado")
        else:
            criticism["overall_assessment"] = "Decisão precisa de revisão"
            criticism["weaknesses"].append("Precisão abaixo do esperado")
        
        # Avaliar confiança
        if confidence_status == "calibrated":
            criticism["strengths"].append("Confiança bem calibrada")
        elif confidence_status == "overconfident":
            criticism["weaknesses"].append("Excesso de confiança")
            criticism["learning_points"].append("Reduzir confiança em situações similares")
        else:
            criticism["weaknesses"].append("Confiança muito baixa")
            criticism["learning_points"].append("Aumentar confiança quando dados suportam")
        
        # Avaliar vieses
        for bias in biases:
            if bias["severity"] == "high":
                criticism["weaknesses"].append(f"Viés detectado: {bias['description']}")
                criticism["learning_points"].append(f"Mitigar {bias['type']}")
        
        return criticism
    
    def _suggest_improvements(self, evaluation: Dict) -> List[Dict]:
        """Sugere melhorias baseadas na avaliação."""
        suggestions = []
        
        accuracy = evaluation["metrics"]["accuracy"]
        biases = evaluation["metrics"]["potential_biases"]
        
        if accuracy < 0.8:
            suggestions.append({
                "area": "prediction_model",
                "suggestion": "Revisar modelo de previsão com mais variáveis",
                "priority": "high"
            })
        
        if any(b["severity"] == "high" for b in biases):
            suggestions.append({
                "area": "bias_mitigation",
                "suggestion": "Implementar checklist anti-viés antes de decisões",
                "priority": "high"
            })
        
        if evaluation["metrics"]["confidence_calibration"]["status"] != "calibrated":
            suggestions.append({
                "area": "confidence_calibration",
                "suggestion": "Ajustar algoritmo de cálculo de confiança",
                "priority": "medium"
            })
        
        return suggestions
    
    def _update_calibration(self, confidence: float, was_correct: bool):
        """Atualiza métricas de calibração."""
        self.confidence_calibration["total_predictions"] += 1
        if was_correct:
            self.confidence_calibration["correct_predictions"] += 1
        
        if was_correct and confidence < 0.7:
            self.confidence_calibration["underconfident_count"] += 1
        elif not was_correct and confidence > 0.8:
            self.confidence_calibration["overconfident_count"] += 1
    
    def get_performance_report(self) -> Dict:
        """Gera relatório de performance da IA."""
        total = self.confidence_calibration["total_predictions"]
        correct = self.confidence_calibration["correct_predictions"]
        
        return {
            "total_decisions_evaluated": len(self.evaluations),
            "overall_accuracy": correct / total if total > 0 else 0,
            "confidence_calibration": self.confidence_calibration,
            "calibration_score": self._calculate_calibration_score(),
            "common_biases": self._get_common_biases(),
            "improvement_trends": self._analyze_improvement_trends()
        }
    
    def _calculate_calibration_score(self) -> float:
        """Calcula score de calibração de confiança."""
        total = self.confidence_calibration["total_predictions"]
        if total == 0:
            return 1.0
        
        miscalibrated = (
            self.confidence_calibration["overconfident_count"] +
            self.confidence_calibration["underconfident_count"]
        )
        
        return 1 - (miscalibrated / total)
    
    def _get_common_biases(self) -> List[Dict]:
        """Identifica vieses mais comuns."""
        bias_counts = {}
        
        for evaluation in self.evaluations:
            for bias in evaluation["metrics"]["potential_biases"]:
                bias_type = bias["type"]
                bias_counts[bias_type] = bias_counts.get(bias_type, 0) + 1
        
        return [
            {"type": k, "count": v}
            for k, v in sorted(bias_counts.items(), key=lambda x: x[1], reverse=True)
        ][:5]
    
    def _analyze_improvement_trends(self) -> Dict:
        """Analisa tendências de melhoria ao longo do tempo."""
        if len(self.evaluations) < 10:
            return {"status": "insufficient_data", "message": "Dados insuficientes para análise de tendência"}
        
        # Comparar primeira e última metade
        mid = len(self.evaluations) // 2
        first_half = self.evaluations[:mid]
        second_half = self.evaluations[mid:]
        
        first_accuracy = sum(e["metrics"]["accuracy"] for e in first_half) / len(first_half)
        second_accuracy = sum(e["metrics"]["accuracy"] for e in second_half) / len(second_half)
        
        improvement = second_accuracy - first_accuracy
        
        return {
            "status": "improving" if improvement > 0.05 else "stable" if improvement > -0.05 else "declining",
            "first_period_accuracy": round(first_accuracy, 3),
            "second_period_accuracy": round(second_accuracy, 3),
            "improvement": round(improvement, 3)
        }
    
    def request_human_review(self, decision_id: str, reason: str) -> Dict:
        """Solicita revisão humana para uma decisão."""
        return {
            "decision_id": decision_id,
            "review_requested": True,
            "reason": reason,
            "requested_at": datetime.now().isoformat(),
            "status": "pending_review"
        }
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de auto-crítica."""
        return {
            "total_evaluations": len(self.evaluations),
            "calibration_score": self._calculate_calibration_score(),
            "improvement_suggestions_count": len(self.improvement_suggestions),
            "confidence_calibration": self.confidence_calibration
        }


# Instância global
ai_self_criticism = AISelfCriticism()

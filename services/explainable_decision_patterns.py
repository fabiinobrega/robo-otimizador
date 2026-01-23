# services/explainable_decision_patterns.py
"""
NEXORA PRIME - Padrões de Decisão Explicáveis
Transparência nas decisões da IA
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class ExplainableDecisionPatterns:
    """Sistema de decisões explicáveis da IA."""
    
    def __init__(self):
        self.decision_templates = {
            "scale_up": "A decisão de escalar a campanha {campaign_name} foi baseada em um ROAS de {roas} e um CPA de R${cpa}, indicando alta lucratividade e eficiência.",
            "pause": "A campanha {campaign_name} foi pausada devido a um baixo desempenho, com um ROAS de {roas} e um CPA de R${cpa}, para evitar mais perdas.",
            "budget_reallocation": "O orçamento foi realocado da campanha {from_campaign} para a {to_campaign} para maximizar o ROAS geral.",
            "creative_change": "O criativo foi alterado na campanha {campaign_name} devido a CTR abaixo de {ctr_threshold}%.",
            "audience_expansion": "A audiência da campanha {campaign_name} foi expandida para alcançar mais potenciais clientes.",
            "bid_adjustment": "O lance foi ajustado em {adjustment_percent}% na campanha {campaign_name} para otimizar o CPA."
        }
        self.decision_history = []
        self.explanation_formats = ["simple", "detailed", "technical"]
    
    def explain_decision(self, decision: Dict, format_type: str = "simple") -> str:
        """Gera uma explicação legível por humanos para uma decisão da IA."""
        decision_type = decision.get("type")
        context = decision.get("context", {})
        
        template = self.decision_templates.get(decision_type)
        if not template:
            return "Não foi possível gerar uma explicação para esta decisão."
        
        try:
            explanation = template.format(**context)
        except KeyError:
            explanation = f"Decisão do tipo '{decision_type}' executada com base nos dados disponíveis."
        
        if format_type == "detailed":
            explanation = self._add_detailed_context(explanation, decision)
        elif format_type == "technical":
            explanation = self._add_technical_context(explanation, decision)
        
        return explanation
    
    def _add_detailed_context(self, base_explanation: str, decision: Dict) -> str:
        """Adiciona contexto detalhado à explicação."""
        context = decision.get("context", {})
        factors = decision.get("factors", [])
        
        detailed = base_explanation + "\n\nFatores considerados:\n"
        for factor in factors:
            detailed += f"- {factor.get('name', 'Fator')}: {factor.get('value', 'N/A')} (peso: {factor.get('weight', 0):.0%})\n"
        
        return detailed
    
    def _add_technical_context(self, base_explanation: str, decision: Dict) -> str:
        """Adiciona contexto técnico à explicação."""
        technical = base_explanation + "\n\nDetalhes técnicos:\n"
        technical += f"- Algoritmo: {decision.get('algorithm', 'Padrão')}\n"
        technical += f"- Confiança: {decision.get('confidence', 0):.0%}\n"
        technical += f"- Dados utilizados: {decision.get('data_points', 0)} pontos\n"
        technical += f"- Modelo: {decision.get('model_version', '1.0')}\n"
        
        return technical
    
    def generate_decision_report(self, decisions: List[Dict]) -> Dict:
        """Gera um relatório explicativo de múltiplas decisões."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_decisions": len(decisions),
            "decisions_by_type": {},
            "explanations": []
        }
        
        for decision in decisions:
            decision_type = decision.get("type", "unknown")
            report["decisions_by_type"][decision_type] = report["decisions_by_type"].get(decision_type, 0) + 1
            
            report["explanations"].append({
                "decision_id": decision.get("id"),
                "type": decision_type,
                "explanation": self.explain_decision(decision),
                "confidence": decision.get("confidence", 0)
            })
        
        return report
    
    def log_decision(self, decision: Dict, explanation: str) -> Dict:
        """Registra uma decisão com sua explicação."""
        record = {
            "decision": decision,
            "explanation": explanation,
            "logged_at": datetime.now().isoformat()
        }
        self.decision_history.append(record)
        return record
    
    def get_decision_history(self, limit: int = 50) -> List[Dict]:
        """Retorna histórico de decisões explicadas."""
        return self.decision_history[-limit:]
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de explicações."""
        return {
            "total_decisions_logged": len(self.decision_history),
            "available_templates": list(self.decision_templates.keys()),
            "explanation_formats": self.explanation_formats
        }


explainable_decisions = ExplainableDecisionPatterns()

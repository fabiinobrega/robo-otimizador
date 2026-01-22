"""
ANTI-BAN AI - IA de Defesa de Conta
Proteção ativa contra banimentos e análise de compliance
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib

class AntiBanAI:
    """Sistema de proteção de contas e análise de compliance."""
    
    def __init__(self):
        self.name = "Anti-Ban AI"
        self.version = "2.0.0"
        
        # Palavras proibidas por plataforma
        self.forbidden_words = {
            "facebook": {
                "health_claims": [
                    "cura", "curar", "tratamento", "tratar", "elimina", "eliminar",
                    "100% eficaz", "garantido", "milagre", "milagroso", "revolucionário",
                    "cientificamente comprovado", "médicos recomendam", "aprovado pela anvisa"
                ],
                "financial_claims": [
                    "ganhe dinheiro fácil", "fique rico", "renda garantida", "lucro garantido",
                    "sem esforço", "dinheiro rápido", "enriqueça", "fortuna"
                ],
                "before_after": [
                    "antes e depois", "antes/depois", "transformação", "resultado garantido"
                ],
                "urgency_excessive": [
                    "última chance", "só hoje", "urgente", "não perca", "acabe agora"
                ],
                "personal_attributes": [
                    "você é gordo", "você é feio", "você está", "seu problema"
                ],
                "prohibited_content": [
                    "bitcoin", "criptomoeda", "forex", "opções binárias", "cassino",
                    "apostas", "jogo de azar", "pirâmide", "multinível"
                ]
            },
            "google": {
                "health_claims": [
                    "cura", "tratamento definitivo", "100% natural", "sem efeitos colaterais",
                    "aprovado", "certificado", "recomendado por médicos"
                ],
                "financial_claims": [
                    "ganhe dinheiro", "fique rico", "renda passiva garantida",
                    "investimento seguro", "retorno garantido"
                ],
                "comparative": [
                    "melhor que", "superior a", "número 1", "líder de mercado"
                ],
                "superlatives": [
                    "o melhor", "o único", "o mais", "incomparável", "imbatível"
                ]
            },
            "tiktok": {
                "health_claims": [
                    "emagreça", "perca peso", "queime gordura", "dieta milagrosa",
                    "suplemento", "remédio natural"
                ],
                "financial_claims": [
                    "ganhe dinheiro", "fique rico", "renda extra fácil"
                ],
                "adult_content": [
                    "sexy", "sensual", "adulto", "18+"
                ]
            }
        }
        
        # Padrões de risco
        self.risk_patterns = {
            "excessive_caps": {
                "pattern": r"[A-Z]{5,}",
                "risk_level": "medium",
                "description": "Uso excessivo de letras maiúsculas"
            },
            "excessive_emojis": {
                "pattern": r"[\U0001F600-\U0001F64F]{4,}",
                "risk_level": "low",
                "description": "Muitos emojis seguidos"
            },
            "excessive_punctuation": {
                "pattern": r"[!?]{3,}",
                "risk_level": "medium",
                "description": "Pontuação excessiva"
            },
            "money_symbols": {
                "pattern": r"[$€£¥]{2,}|R\$\s*\d+\.?\d*",
                "risk_level": "medium",
                "description": "Símbolos monetários excessivos"
            },
            "percentage_claims": {
                "pattern": r"\d{2,3}%",
                "risk_level": "high",
                "description": "Claims com porcentagens específicas"
            },
            "time_pressure": {
                "pattern": r"(últim[oa]s?\s+\d+|só\s+hoje|acaba\s+em|expira)",
                "risk_level": "medium",
                "description": "Pressão temporal excessiva"
            }
        }
        
        # Histórico de alertas por conta
        self.account_alerts = {}
        
        # Limites de segurança
        self.safety_limits = {
            "max_daily_spend_increase": 0.3,  # 30% máximo de aumento diário
            "max_campaigns_per_day": 10,
            "min_hours_between_changes": 4,
            "max_rejected_ads_before_pause": 3,
            "cooling_period_after_rejection_hours": 24
        }
    
    def analyze_copy_compliance(
        self,
        copy_text: str,
        platform: str = "facebook",
        niche: str = "geral"
    ) -> Dict[str, Any]:
        """Analisa compliance de uma copy."""
        
        analysis_id = f"compliance_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Obter palavras proibidas da plataforma
        platform_forbidden = self.forbidden_words.get(platform, self.forbidden_words["facebook"])
        
        # Análise de palavras proibidas
        forbidden_found = []
        copy_lower = copy_text.lower()
        
        for category, words in platform_forbidden.items():
            for word in words:
                if word.lower() in copy_lower:
                    forbidden_found.append({
                        "word": word,
                        "category": category,
                        "severity": self._get_word_severity(category)
                    })
        
        # Análise de padrões de risco
        pattern_risks = []
        for pattern_name, pattern_info in self.risk_patterns.items():
            matches = re.findall(pattern_info["pattern"], copy_text, re.IGNORECASE)
            if matches:
                pattern_risks.append({
                    "pattern": pattern_name,
                    "matches": matches[:3],  # Limitar a 3 exemplos
                    "risk_level": pattern_info["risk_level"],
                    "description": pattern_info["description"]
                })
        
        # Calcular score de risco
        risk_score = self._calculate_risk_score(forbidden_found, pattern_risks)
        
        # Gerar sugestões de correção
        suggestions = self._generate_compliance_suggestions(forbidden_found, pattern_risks, copy_text)
        
        # Determinar status
        if risk_score >= 80:
            status = "high_risk"
            recommendation = "NÃO PUBLICAR - Alto risco de rejeição/ban"
        elif risk_score >= 50:
            status = "medium_risk"
            recommendation = "REVISAR - Fazer ajustes antes de publicar"
        elif risk_score >= 20:
            status = "low_risk"
            recommendation = "ATENÇÃO - Pequenos ajustes recomendados"
        else:
            status = "safe"
            recommendation = "APROVADO - Copy dentro das diretrizes"
        
        return {
            "analysis_id": analysis_id,
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "risk_score": risk_score,
            "status": status,
            "recommendation": recommendation,
            "forbidden_words_found": forbidden_found,
            "pattern_risks": pattern_risks,
            "suggestions": suggestions,
            "safe_version": self._generate_safe_version(copy_text, forbidden_found) if forbidden_found else None
        }
    
    def detect_ban_risk(self, account_data: Dict) -> Dict[str, Any]:
        """Detecta risco de banimento de uma conta."""
        
        account_id = account_data.get("account_id", "unknown")
        
        risk_factors = []
        risk_score = 0
        
        # Verificar rejeições recentes
        rejected_ads = account_data.get("rejected_ads_last_30_days", 0)
        if rejected_ads >= 5:
            risk_factors.append({
                "factor": "rejected_ads",
                "value": rejected_ads,
                "impact": "high",
                "description": f"{rejected_ads} anúncios rejeitados nos últimos 30 dias"
            })
            risk_score += 30
        elif rejected_ads >= 2:
            risk_factors.append({
                "factor": "rejected_ads",
                "value": rejected_ads,
                "impact": "medium",
                "description": f"{rejected_ads} anúncios rejeitados nos últimos 30 dias"
            })
            risk_score += 15
        
        # Verificar mudanças bruscas de orçamento
        budget_changes = account_data.get("budget_changes_last_7_days", [])
        large_changes = [c for c in budget_changes if abs(c.get("change_percent", 0)) > 50]
        if large_changes:
            risk_factors.append({
                "factor": "budget_volatility",
                "value": len(large_changes),
                "impact": "medium",
                "description": f"{len(large_changes)} mudanças bruscas de orçamento"
            })
            risk_score += 20
        
        # Verificar idade da conta
        account_age_days = account_data.get("account_age_days", 365)
        if account_age_days < 30:
            risk_factors.append({
                "factor": "new_account",
                "value": account_age_days,
                "impact": "high",
                "description": "Conta nova (menos de 30 dias)"
            })
            risk_score += 25
        elif account_age_days < 90:
            risk_factors.append({
                "factor": "young_account",
                "value": account_age_days,
                "impact": "medium",
                "description": "Conta jovem (menos de 90 dias)"
            })
            risk_score += 10
        
        # Verificar histórico de pagamentos
        payment_issues = account_data.get("payment_issues_last_90_days", 0)
        if payment_issues > 0:
            risk_factors.append({
                "factor": "payment_issues",
                "value": payment_issues,
                "impact": "high",
                "description": f"{payment_issues} problemas de pagamento"
            })
            risk_score += 20
        
        # Verificar nicho de risco
        niche = account_data.get("niche", "geral")
        high_risk_niches = ["emagrecimento", "finanças", "saúde", "relacionamentos"]
        if niche.lower() in high_risk_niches:
            risk_factors.append({
                "factor": "high_risk_niche",
                "value": niche,
                "impact": "medium",
                "description": f"Nicho de alto risco: {niche}"
            })
            risk_score += 15
        
        # Determinar status
        if risk_score >= 70:
            status = "critical"
            action = "AÇÃO IMEDIATA NECESSÁRIA"
        elif risk_score >= 50:
            status = "high"
            action = "REDUZIR ATIVIDADE"
        elif risk_score >= 30:
            status = "medium"
            action = "MONITORAR DE PERTO"
        else:
            status = "low"
            action = "CONTINUAR NORMALMENTE"
        
        # Gerar recomendações
        recommendations = self._generate_account_recommendations(risk_factors, risk_score)
        
        return {
            "account_id": account_id,
            "timestamp": datetime.now().isoformat(),
            "risk_score": min(100, risk_score),
            "status": status,
            "action": action,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "monitoring_frequency": self._get_monitoring_frequency(risk_score)
        }
    
    def suggest_safe_adjustments(self, copy_text: str, issues: List[Dict]) -> Dict[str, Any]:
        """Sugere ajustes seguros para uma copy problemática."""
        
        adjusted_copy = copy_text
        adjustments_made = []
        
        # Substituições seguras
        safe_replacements = {
            "cura": "auxilia no tratamento",
            "curar": "ajudar a tratar",
            "elimina": "pode ajudar a reduzir",
            "100% eficaz": "altamente eficaz",
            "garantido": "com alta probabilidade",
            "milagre": "resultado surpreendente",
            "ganhe dinheiro fácil": "aumente sua renda",
            "fique rico": "melhore sua situação financeira",
            "renda garantida": "potencial de renda",
            "última chance": "oportunidade especial",
            "só hoje": "por tempo limitado",
            "antes e depois": "evolução",
            "você é gordo": "você quer emagrecer",
            "você é feio": "você quer melhorar sua aparência"
        }
        
        for issue in issues:
            word = issue.get("word", "")
            if word.lower() in safe_replacements:
                replacement = safe_replacements[word.lower()]
                adjusted_copy = re.sub(
                    re.escape(word), 
                    replacement, 
                    adjusted_copy, 
                    flags=re.IGNORECASE
                )
                adjustments_made.append({
                    "original": word,
                    "replacement": replacement,
                    "reason": f"Palavra de risco na categoria: {issue.get('category', 'geral')}"
                })
        
        # Reduzir caps excessivos
        def reduce_caps(match):
            return match.group(0).capitalize()
        
        adjusted_copy = re.sub(r'\b[A-Z]{5,}\b', reduce_caps, adjusted_copy)
        
        # Reduzir pontuação excessiva
        adjusted_copy = re.sub(r'[!]{3,}', '!', adjusted_copy)
        adjusted_copy = re.sub(r'[?]{3,}', '?', adjusted_copy)
        
        return {
            "original_copy": copy_text,
            "adjusted_copy": adjusted_copy,
            "adjustments_made": adjustments_made,
            "adjustments_count": len(adjustments_made),
            "compliance_improvement": self._estimate_compliance_improvement(issues, adjustments_made)
        }
    
    def get_account_alert_history(self, account_id: str) -> Dict[str, Any]:
        """Obtém histórico de alertas de uma conta."""
        
        alerts = self.account_alerts.get(account_id, [])
        
        # Agrupar por tipo
        alerts_by_type = {}
        for alert in alerts:
            alert_type = alert.get("type", "unknown")
            if alert_type not in alerts_by_type:
                alerts_by_type[alert_type] = []
            alerts_by_type[alert_type].append(alert)
        
        # Calcular tendência
        recent_alerts = [a for a in alerts if self._is_recent(a.get("timestamp"))]
        trend = "increasing" if len(recent_alerts) > len(alerts) / 2 else "stable"
        
        return {
            "account_id": account_id,
            "total_alerts": len(alerts),
            "recent_alerts": len(recent_alerts),
            "trend": trend,
            "alerts_by_type": alerts_by_type,
            "last_alert": alerts[-1] if alerts else None,
            "recommendation": self._get_alert_recommendation(len(recent_alerts), trend)
        }
    
    def monitor_account_continuously(self, account_data: Dict) -> Dict[str, Any]:
        """Monitora conta continuamente e gera alertas."""
        
        account_id = account_data.get("account_id", "unknown")
        
        # Detectar anomalias
        anomalies = []
        
        # Verificar picos de gasto
        daily_spend = account_data.get("daily_spend", [])
        if len(daily_spend) >= 2:
            avg_spend = sum(daily_spend[:-1]) / len(daily_spend[:-1])
            current_spend = daily_spend[-1]
            if current_spend > avg_spend * 1.5:
                anomalies.append({
                    "type": "spend_spike",
                    "severity": "medium",
                    "description": f"Gasto {((current_spend/avg_spend)-1)*100:.0f}% acima da média"
                })
        
        # Verificar queda de performance
        daily_roas = account_data.get("daily_roas", [])
        if len(daily_roas) >= 3:
            recent_avg = sum(daily_roas[-3:]) / 3
            historical_avg = sum(daily_roas[:-3]) / len(daily_roas[:-3]) if len(daily_roas) > 3 else recent_avg
            if recent_avg < historical_avg * 0.7:
                anomalies.append({
                    "type": "performance_drop",
                    "severity": "high",
                    "description": f"ROAS caiu {((1-recent_avg/historical_avg))*100:.0f}% vs histórico"
                })
        
        # Verificar rejeições
        recent_rejections = account_data.get("rejections_last_24h", 0)
        if recent_rejections > 0:
            anomalies.append({
                "type": "ad_rejection",
                "severity": "high" if recent_rejections >= 2 else "medium",
                "description": f"{recent_rejections} anúncio(s) rejeitado(s) nas últimas 24h"
            })
        
        # Registrar alertas
        for anomaly in anomalies:
            self._record_alert(account_id, anomaly)
        
        return {
            "account_id": account_id,
            "timestamp": datetime.now().isoformat(),
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "overall_status": "alert" if anomalies else "healthy",
            "recommended_actions": self._get_anomaly_actions(anomalies)
        }
    
    def _get_word_severity(self, category: str) -> str:
        """Retorna severidade baseada na categoria."""
        high_severity = ["health_claims", "financial_claims", "prohibited_content"]
        medium_severity = ["before_after", "personal_attributes"]
        
        if category in high_severity:
            return "high"
        elif category in medium_severity:
            return "medium"
        return "low"
    
    def _calculate_risk_score(self, forbidden_found: List, pattern_risks: List) -> int:
        """Calcula score de risco total."""
        score = 0
        
        # Pontuação por palavras proibidas
        for word in forbidden_found:
            if word["severity"] == "high":
                score += 25
            elif word["severity"] == "medium":
                score += 15
            else:
                score += 5
        
        # Pontuação por padrões de risco
        for pattern in pattern_risks:
            if pattern["risk_level"] == "high":
                score += 20
            elif pattern["risk_level"] == "medium":
                score += 10
            else:
                score += 5
        
        return min(100, score)
    
    def _generate_compliance_suggestions(
        self, 
        forbidden_found: List, 
        pattern_risks: List,
        original_copy: str
    ) -> List[Dict]:
        """Gera sugestões de compliance."""
        suggestions = []
        
        for word in forbidden_found:
            suggestions.append({
                "type": "word_replacement",
                "issue": f"Palavra proibida: '{word['word']}'",
                "suggestion": f"Remover ou substituir '{word['word']}' por termo mais neutro",
                "priority": "high" if word["severity"] == "high" else "medium"
            })
        
        for pattern in pattern_risks:
            suggestions.append({
                "type": "pattern_fix",
                "issue": pattern["description"],
                "suggestion": self._get_pattern_suggestion(pattern["pattern"]),
                "priority": "medium" if pattern["risk_level"] == "high" else "low"
            })
        
        return suggestions
    
    def _get_pattern_suggestion(self, pattern_name: str) -> str:
        """Retorna sugestão para padrão específico."""
        suggestions = {
            "excessive_caps": "Reduza o uso de letras maiúsculas. Use apenas no início de frases.",
            "excessive_emojis": "Limite o uso de emojis a 1-2 por parágrafo.",
            "excessive_punctuation": "Use apenas um ponto de exclamação ou interrogação.",
            "money_symbols": "Evite mostrar valores monetários diretamente no texto.",
            "percentage_claims": "Evite claims com porcentagens específicas sem comprovação.",
            "time_pressure": "Reduza a pressão temporal. Use termos mais suaves."
        }
        return suggestions.get(pattern_name, "Revise este elemento para reduzir risco.")
    
    def _generate_safe_version(self, original: str, forbidden_found: List) -> str:
        """Gera versão segura da copy."""
        safe_copy = original
        
        for word in forbidden_found:
            # Remover palavras proibidas
            safe_copy = re.sub(
                re.escape(word["word"]), 
                "[REVISAR]", 
                safe_copy, 
                flags=re.IGNORECASE
            )
        
        return safe_copy
    
    def _generate_account_recommendations(self, risk_factors: List, risk_score: int) -> List[Dict]:
        """Gera recomendações para conta."""
        recommendations = []
        
        if risk_score >= 70:
            recommendations.append({
                "priority": "critical",
                "action": "Pausar todas as campanhas por 24-48h",
                "reason": "Risco crítico de banimento"
            })
            recommendations.append({
                "priority": "critical",
                "action": "Revisar todos os anúncios ativos",
                "reason": "Identificar e corrigir problemas"
            })
        
        for factor in risk_factors:
            if factor["factor"] == "rejected_ads":
                recommendations.append({
                    "priority": "high",
                    "action": "Analisar motivos das rejeições",
                    "reason": "Evitar repetir erros"
                })
            elif factor["factor"] == "budget_volatility":
                recommendations.append({
                    "priority": "medium",
                    "action": "Estabilizar orçamentos",
                    "reason": "Mudanças bruscas são suspeitas"
                })
            elif factor["factor"] == "new_account":
                recommendations.append({
                    "priority": "high",
                    "action": "Aumentar gastos gradualmente",
                    "reason": "Contas novas precisam de aquecimento"
                })
        
        return recommendations
    
    def _get_monitoring_frequency(self, risk_score: int) -> str:
        """Retorna frequência de monitoramento recomendada."""
        if risk_score >= 70:
            return "A cada 2 horas"
        elif risk_score >= 50:
            return "A cada 6 horas"
        elif risk_score >= 30:
            return "Diariamente"
        return "Semanalmente"
    
    def _is_recent(self, timestamp: str, days: int = 7) -> bool:
        """Verifica se timestamp é recente."""
        if not timestamp:
            return False
        try:
            dt = datetime.fromisoformat(timestamp)
            return (datetime.now() - dt).days <= days
        except:
            return False
    
    def _get_alert_recommendation(self, recent_count: int, trend: str) -> str:
        """Retorna recomendação baseada em alertas."""
        if recent_count >= 5:
            return "URGENTE: Pausar atividades e revisar conta"
        elif recent_count >= 3:
            return "ATENÇÃO: Reduzir atividades e monitorar de perto"
        elif trend == "increasing":
            return "CUIDADO: Tendência de aumento de alertas"
        return "OK: Continuar monitorando normalmente"
    
    def _record_alert(self, account_id: str, anomaly: Dict):
        """Registra alerta para conta."""
        if account_id not in self.account_alerts:
            self.account_alerts[account_id] = []
        
        self.account_alerts[account_id].append({
            "timestamp": datetime.now().isoformat(),
            "type": anomaly["type"],
            "severity": anomaly["severity"],
            "description": anomaly["description"]
        })
        
        # Manter apenas últimos 100 alertas
        if len(self.account_alerts[account_id]) > 100:
            self.account_alerts[account_id] = self.account_alerts[account_id][-100:]
    
    def _get_anomaly_actions(self, anomalies: List) -> List[str]:
        """Retorna ações recomendadas para anomalias."""
        actions = []
        
        for anomaly in anomalies:
            if anomaly["type"] == "spend_spike":
                actions.append("Verificar se aumento de gasto foi intencional")
            elif anomaly["type"] == "performance_drop":
                actions.append("Analisar causa da queda de performance")
                actions.append("Considerar pausar campanhas problemáticas")
            elif anomaly["type"] == "ad_rejection":
                actions.append("Revisar anúncios rejeitados imediatamente")
                actions.append("Não resubmeter sem correções")
        
        if not actions:
            actions.append("Continuar monitoramento normal")
        
        return actions
    
    def _estimate_compliance_improvement(self, issues: List, adjustments: List) -> str:
        """Estima melhoria de compliance após ajustes."""
        if not issues:
            return "N/A - Sem problemas identificados"
        
        fixed_percentage = (len(adjustments) / len(issues)) * 100
        
        if fixed_percentage >= 80:
            return f"Alta ({fixed_percentage:.0f}% dos problemas corrigidos)"
        elif fixed_percentage >= 50:
            return f"Média ({fixed_percentage:.0f}% dos problemas corrigidos)"
        return f"Baixa ({fixed_percentage:.0f}% dos problemas corrigidos)"


# Instância global
anti_ban_ai = AntiBanAI()

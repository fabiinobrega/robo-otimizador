"""
LEARNING CYCLE - Ciclo de Aprendizado entre Campanhas
Sistema de aprendizado continuo que transfere conhecimento entre campanhas
Nexora Prime V2 - Expansao Unicornio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

class LearningCycle:
    """Sistema de ciclo de aprendizado entre campanhas."""
    
    def __init__(self):
        self.name = "Learning Cycle"
        self.version = "2.0.0"
        
        # Base de conhecimento acumulado
        self.knowledge_base = {
            "audiences": {},
            "creatives": {},
            "offers": {},
            "copy_patterns": {},
            "timing_patterns": {},
            "geo_patterns": {}
        }
        
        # Historico de campanhas
        self.campaign_history = []
        
        # Padroes identificados
        self.identified_patterns = []
        
        # Insights gerados
        self.insights = []
        
        # Regras aprendidas
        self.learned_rules = []
    
    def record_campaign(self, campaign_data: Dict) -> Dict[str, Any]:
        """Registra dados de uma campanha para aprendizado."""
        
        campaign_record = {
            "id": campaign_data.get("campaign_id"),
            "recorded_at": datetime.now().isoformat(),
            "niche": campaign_data.get("niche"),
            "objective": campaign_data.get("objective"),
            "budget": campaign_data.get("budget"),
            "duration_days": campaign_data.get("duration_days"),
            "metrics": {
                "spend": campaign_data.get("spend", 0),
                "impressions": campaign_data.get("impressions", 0),
                "clicks": campaign_data.get("clicks", 0),
                "conversions": campaign_data.get("conversions", 0),
                "revenue": campaign_data.get("revenue", 0),
                "ctr": campaign_data.get("ctr", 0),
                "cpc": campaign_data.get("cpc", 0),
                "cpa": campaign_data.get("cpa", 0),
                "roas": campaign_data.get("roas", 0)
            },
            "targeting": campaign_data.get("targeting", {}),
            "creatives": campaign_data.get("creatives", []),
            "success_level": self._calculate_success_level(campaign_data)
        }
        
        self.campaign_history.append(campaign_record)
        
        # Extrair aprendizados
        learnings = self._extract_learnings(campaign_record)
        
        # Atualizar base de conhecimento
        self._update_knowledge_base(campaign_record, learnings)
        
        return {
            "status": "recorded",
            "campaign_id": campaign_record["id"],
            "success_level": campaign_record["success_level"],
            "learnings_extracted": len(learnings),
            "learnings": learnings
        }
    
    def get_recommendations_for_new_campaign(self, config: Dict) -> Dict[str, Any]:
        """Obtem recomendacoes baseadas em aprendizados anteriores."""
        
        niche = config.get("niche", "geral")
        objective = config.get("objective", "conversions")
        budget = config.get("budget", 1000)
        
        recommendations = {
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "audience_recommendations": [],
            "creative_recommendations": [],
            "budget_recommendations": [],
            "timing_recommendations": [],
            "copy_recommendations": [],
            "warnings": []
        }
        
        # Buscar campanhas similares bem-sucedidas
        similar_successful = self._find_similar_successful_campaigns(niche, objective)
        
        # Recomendacoes de audiencia
        if niche in self.knowledge_base["audiences"]:
            audience_data = self.knowledge_base["audiences"][niche]
            recommendations["audience_recommendations"] = [
                {"type": "best_performing", "audiences": audience_data.get("top_performers", [])},
                {"type": "avoid", "audiences": audience_data.get("underperformers", [])}
            ]
        
        # Recomendacoes de criativos
        if niche in self.knowledge_base["creatives"]:
            creative_data = self.knowledge_base["creatives"][niche]
            recommendations["creative_recommendations"] = [
                {"type": "format", "recommendation": creative_data.get("best_format", "video")},
                {"type": "style", "recommendation": creative_data.get("best_style", "lifestyle")},
                {"type": "cta", "recommendation": creative_data.get("best_cta", "Saiba Mais")}
            ]
        
        # Recomendacoes de orcamento
        if similar_successful:
            avg_budget = sum(c["budget"] for c in similar_successful) / len(similar_successful)
            avg_roas = sum(c["metrics"]["roas"] for c in similar_successful) / len(similar_successful)
            
            recommendations["budget_recommendations"] = [
                {"type": "suggested_daily", "value": round(avg_budget / 30, 2)},
                {"type": "expected_roas", "value": round(avg_roas, 2)},
                {"type": "scale_threshold", "value": "Escale apos 50 conversoes com ROAS > 2"}
            ]
        
        # Recomendacoes de timing
        if niche in self.knowledge_base["timing_patterns"]:
            timing = self.knowledge_base["timing_patterns"][niche]
            recommendations["timing_recommendations"] = [
                {"type": "best_days", "value": timing.get("best_days", ["ter", "qua", "qui"])},
                {"type": "best_hours", "value": timing.get("best_hours", ["12-14", "19-22"])},
                {"type": "avoid_times", "value": timing.get("avoid_times", ["00-06"])}
            ]
        
        # Recomendacoes de copy
        if niche in self.knowledge_base["copy_patterns"]:
            copy = self.knowledge_base["copy_patterns"][niche]
            recommendations["copy_recommendations"] = [
                {"type": "headline_patterns", "value": copy.get("best_headlines", [])},
                {"type": "cta_patterns", "value": copy.get("best_ctas", [])},
                {"type": "avoid_words", "value": copy.get("avoid_words", [])}
            ]
        
        # Avisos baseados em campanhas falhas
        failed_patterns = self._get_failure_patterns(niche)
        if failed_patterns:
            recommendations["warnings"] = failed_patterns
        
        return recommendations
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Analisa padroes em todas as campanhas."""
        
        if len(self.campaign_history) < 5:
            return {"error": "Historico insuficiente para analise de padroes"}
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "campaigns_analyzed": len(self.campaign_history),
            "patterns": {
                "success_patterns": [],
                "failure_patterns": [],
                "timing_patterns": [],
                "budget_patterns": [],
                "creative_patterns": []
            },
            "insights": [],
            "recommendations": []
        }
        
        # Separar campanhas por sucesso
        successful = [c for c in self.campaign_history if c["success_level"] in ["high", "very_high"]]
        failed = [c for c in self.campaign_history if c["success_level"] in ["low", "very_low"]]
        
        # Padroes de sucesso
        if successful:
            analysis["patterns"]["success_patterns"] = self._extract_common_patterns(successful)
        
        # Padroes de falha
        if failed:
            analysis["patterns"]["failure_patterns"] = self._extract_common_patterns(failed)
        
        # Padroes de timing
        analysis["patterns"]["timing_patterns"] = self._analyze_timing_patterns()
        
        # Padroes de orcamento
        analysis["patterns"]["budget_patterns"] = self._analyze_budget_patterns()
        
        # Gerar insights
        analysis["insights"] = self._generate_insights(analysis["patterns"])
        
        # Gerar recomendacoes
        analysis["recommendations"] = self._generate_pattern_recommendations(analysis["patterns"])
        
        # Salvar padroes identificados
        self.identified_patterns = analysis["patterns"]
        
        return analysis
    
    def transfer_learning(self, source_campaign_id: str, target_config: Dict) -> Dict[str, Any]:
        """Transfere aprendizados de uma campanha para outra."""
        
        # Buscar campanha fonte
        source = next((c for c in self.campaign_history if c["id"] == source_campaign_id), None)
        
        if not source:
            return {"error": "Campanha fonte nao encontrada"}
        
        transfer = {
            "timestamp": datetime.now().isoformat(),
            "source_campaign": source_campaign_id,
            "source_success_level": source["success_level"],
            "transferable_elements": [],
            "adaptations_needed": [],
            "expected_performance": {}
        }
        
        # Elementos transferiveis
        if source["success_level"] in ["high", "very_high"]:
            # Transferir audiencias
            if source.get("targeting"):
                transfer["transferable_elements"].append({
                    "type": "audience",
                    "data": source["targeting"],
                    "confidence": "high"
                })
            
            # Transferir padroes de criativos
            if source.get("creatives"):
                transfer["transferable_elements"].append({
                    "type": "creative_patterns",
                    "data": self._extract_creative_patterns(source["creatives"]),
                    "confidence": "medium"
                })
            
            # Transferir estrategia de orcamento
            transfer["transferable_elements"].append({
                "type": "budget_strategy",
                "data": {
                    "initial_budget": source["budget"] * 0.5,
                    "scale_threshold": source["metrics"]["conversions"] * 0.3,
                    "max_cpa": source["metrics"]["cpa"] * 1.2
                },
                "confidence": "high"
            })
        
        # Adaptacoes necessarias
        if source.get("niche") != target_config.get("niche"):
            transfer["adaptations_needed"].append({
                "type": "niche_adaptation",
                "description": "Adaptar mensagens e criativos para o novo nicho"
            })
        
        if source.get("objective") != target_config.get("objective"):
            transfer["adaptations_needed"].append({
                "type": "objective_adaptation",
                "description": "Ajustar estrategia para novo objetivo"
            })
        
        # Performance esperada
        if source["success_level"] in ["high", "very_high"]:
            transfer["expected_performance"] = {
                "estimated_roas": round(source["metrics"]["roas"] * 0.8, 2),
                "estimated_cpa": round(source["metrics"]["cpa"] * 1.2, 2),
                "confidence": "medium",
                "note": "Estimativas baseadas em transferencia de aprendizado"
            }
        
        return transfer
    
    def get_best_practices(self, niche: str = None) -> Dict[str, Any]:
        """Obtem melhores praticas aprendidas."""
        
        practices = {
            "timestamp": datetime.now().isoformat(),
            "niche": niche or "geral",
            "audience_practices": [],
            "creative_practices": [],
            "budget_practices": [],
            "optimization_practices": [],
            "avoid_practices": []
        }
        
        # Filtrar campanhas por nicho se especificado
        campaigns = self.campaign_history
        if niche:
            campaigns = [c for c in campaigns if c.get("niche") == niche]
        
        successful = [c for c in campaigns if c["success_level"] in ["high", "very_high"]]
        
        if successful:
            # Praticas de audiencia
            practices["audience_practices"] = [
                "Use lookalikes de compradores com 1-3% de similaridade",
                "Combine interesses relacionados ao produto",
                "Exclua compradores recentes para aquisicao"
            ]
            
            # Praticas de criativos
            practices["creative_practices"] = [
                "Videos curtos (15-30s) performam melhor",
                "Mostre o produto em uso real",
                "Use legendas em todos os videos",
                "Teste pelo menos 3 variacoes de criativo"
            ]
            
            # Praticas de orcamento
            avg_budget = sum(c["budget"] for c in successful) / len(successful)
            practices["budget_practices"] = [
                f"Comece com orcamento diario de R${avg_budget/30:.0f}",
                "Escale 20-30% a cada 3 dias com ROAS positivo",
                "Nunca aumente mais de 50% de uma vez"
            ]
            
            # Praticas de otimizacao
            practices["optimization_practices"] = [
                "Aguarde 50 conversoes antes de otimizar",
                "Pause anuncios com frequencia > 3",
                "Teste novos publicos semanalmente"
            ]
        
        # Praticas a evitar
        failed = [c for c in campaigns if c["success_level"] in ["low", "very_low"]]
        if failed:
            practices["avoid_practices"] = [
                "Evite publicos muito amplos (> 10M)",
                "Nao escale campanhas com ROAS < 1.5",
                "Evite mudar criativos e publicos simultaneamente"
            ]
        
        return practices
    
    def create_learning_report(self, period: str = "30d") -> Dict[str, Any]:
        """Cria relatorio de aprendizados."""
        
        # Filtrar por periodo
        days = int(period.replace("d", ""))
        cutoff = datetime.now() - timedelta(days=days)
        
        recent_campaigns = [
            c for c in self.campaign_history
            if datetime.fromisoformat(c["recorded_at"]) >= cutoff
        ]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "period": period,
            "campaigns_analyzed": len(recent_campaigns),
            "summary": {},
            "key_learnings": [],
            "performance_trends": {},
            "recommendations": []
        }
        
        if not recent_campaigns:
            report["summary"] = {"message": "Nenhuma campanha no periodo"}
            return report
        
        # Resumo
        total_spend = sum(c["metrics"]["spend"] for c in recent_campaigns)
        total_revenue = sum(c["metrics"]["revenue"] for c in recent_campaigns)
        total_conversions = sum(c["metrics"]["conversions"] for c in recent_campaigns)
        
        report["summary"] = {
            "total_campaigns": len(recent_campaigns),
            "total_spend": round(total_spend, 2),
            "total_revenue": round(total_revenue, 2),
            "total_conversions": total_conversions,
            "avg_roas": round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
            "avg_cpa": round(total_spend / total_conversions, 2) if total_conversions > 0 else 0,
            "success_rate": f"{sum(1 for c in recent_campaigns if c['success_level'] in ['high', 'very_high']) / len(recent_campaigns) * 100:.1f}%"
        }
        
        # Aprendizados chave
        report["key_learnings"] = self._extract_key_learnings(recent_campaigns)
        
        # Tendencias de performance
        report["performance_trends"] = self._calculate_performance_trends(recent_campaigns)
        
        # Recomendacoes
        report["recommendations"] = self._generate_report_recommendations(report)
        
        return report
    
    def _calculate_success_level(self, campaign_data: Dict) -> str:
        """Calcula nivel de sucesso de uma campanha."""
        roas = campaign_data.get("roas", 0)
        
        if roas >= 3.0:
            return "very_high"
        elif roas >= 2.0:
            return "high"
        elif roas >= 1.5:
            return "medium"
        elif roas >= 1.0:
            return "low"
        return "very_low"
    
    def _extract_learnings(self, campaign: Dict) -> List[Dict]:
        """Extrai aprendizados de uma campanha."""
        learnings = []
        
        if campaign["success_level"] in ["high", "very_high"]:
            learnings.append({
                "type": "success_pattern",
                "description": f"Campanha bem-sucedida no nicho {campaign.get('niche')}",
                "details": campaign["targeting"]
            })
        elif campaign["success_level"] in ["low", "very_low"]:
            learnings.append({
                "type": "failure_pattern",
                "description": f"Campanha com baixo desempenho no nicho {campaign.get('niche')}",
                "details": campaign["targeting"]
            })
        
        return learnings
    
    def _update_knowledge_base(self, campaign: Dict, learnings: List[Dict]):
        """Atualiza base de conhecimento."""
        niche = campaign.get("niche", "geral")
        
        # Atualizar audiencias
        if niche not in self.knowledge_base["audiences"]:
            self.knowledge_base["audiences"][niche] = {"top_performers": [], "underperformers": []}
        
        if campaign["success_level"] in ["high", "very_high"]:
            self.knowledge_base["audiences"][niche]["top_performers"].append(campaign.get("targeting", {}))
        else:
            self.knowledge_base["audiences"][niche]["underperformers"].append(campaign.get("targeting", {}))
    
    def _find_similar_successful_campaigns(self, niche: str, objective: str) -> List[Dict]:
        """Encontra campanhas similares bem-sucedidas."""
        return [
            c for c in self.campaign_history
            if c.get("niche") == niche
            and c.get("objective") == objective
            and c["success_level"] in ["high", "very_high"]
        ]
    
    def _get_failure_patterns(self, niche: str) -> List[Dict]:
        """Obtem padroes de falha para um nicho."""
        failed = [
            c for c in self.campaign_history
            if c.get("niche") == niche
            and c["success_level"] in ["low", "very_low"]
        ]
        
        if not failed:
            return []
        
        return [
            {"type": "warning", "message": "Evite publicos muito amplos neste nicho"},
            {"type": "warning", "message": "Criativos estaticos tiveram baixa performance"}
        ]
    
    def _extract_common_patterns(self, campaigns: List[Dict]) -> List[Dict]:
        """Extrai padroes comuns de um conjunto de campanhas."""
        patterns = []
        
        if not campaigns:
            return patterns
        
        # Analisar metricas medias
        avg_roas = sum(c["metrics"]["roas"] for c in campaigns) / len(campaigns)
        avg_cpa = sum(c["metrics"]["cpa"] for c in campaigns) / len(campaigns)
        
        patterns.append({
            "type": "metrics",
            "avg_roas": round(avg_roas, 2),
            "avg_cpa": round(avg_cpa, 2)
        })
        
        return patterns
    
    def _analyze_timing_patterns(self) -> List[Dict]:
        """Analisa padroes de timing."""
        return [
            {"pattern": "Melhores dias", "value": ["terca", "quarta", "quinta"]},
            {"pattern": "Melhores horarios", "value": ["12:00-14:00", "19:00-22:00"]}
        ]
    
    def _analyze_budget_patterns(self) -> List[Dict]:
        """Analisa padroes de orcamento."""
        if not self.campaign_history:
            return []
        
        successful = [c for c in self.campaign_history if c["success_level"] in ["high", "very_high"]]
        
        if not successful:
            return []
        
        avg_budget = sum(c["budget"] for c in successful) / len(successful)
        
        return [
            {"pattern": "Orcamento medio de sucesso", "value": round(avg_budget, 2)},
            {"pattern": "Escala recomendada", "value": "20-30% a cada 3 dias"}
        ]
    
    def _extract_creative_patterns(self, creatives: List) -> Dict:
        """Extrai padroes de criativos."""
        return {
            "formats": ["video", "carousel"],
            "styles": ["lifestyle", "product_focus"],
            "ctas": ["Saiba Mais", "Compre Agora"]
        }
    
    def _generate_insights(self, patterns: Dict) -> List[str]:
        """Gera insights a partir dos padroes."""
        insights = []
        
        if patterns.get("success_patterns"):
            insights.append("Campanhas bem-sucedidas compartilham padroes de segmentacao")
        
        if patterns.get("timing_patterns"):
            insights.append("Horarios de pico influenciam significativamente o desempenho")
        
        return insights
    
    def _generate_pattern_recommendations(self, patterns: Dict) -> List[str]:
        """Gera recomendacoes a partir dos padroes."""
        return [
            "Replique estrategias de campanhas bem-sucedidas",
            "Evite padroes identificados em campanhas falhas",
            "Otimize para os melhores horarios identificados"
        ]
    
    def _extract_key_learnings(self, campaigns: List[Dict]) -> List[str]:
        """Extrai aprendizados chave."""
        learnings = []
        
        successful = [c for c in campaigns if c["success_level"] in ["high", "very_high"]]
        
        if successful:
            learnings.append(f"{len(successful)} campanhas bem-sucedidas identificadas")
        
        return learnings
    
    def _calculate_performance_trends(self, campaigns: List[Dict]) -> Dict:
        """Calcula tendencias de performance."""
        if len(campaigns) < 2:
            return {"trend": "insufficient_data"}
        
        # Ordenar por data
        sorted_campaigns = sorted(campaigns, key=lambda x: x["recorded_at"])
        
        first_half = sorted_campaigns[:len(sorted_campaigns)//2]
        second_half = sorted_campaigns[len(sorted_campaigns)//2:]
        
        first_roas = sum(c["metrics"]["roas"] for c in first_half) / len(first_half)
        second_roas = sum(c["metrics"]["roas"] for c in second_half) / len(second_half)
        
        return {
            "roas_trend": "improving" if second_roas > first_roas else "declining",
            "first_period_roas": round(first_roas, 2),
            "second_period_roas": round(second_roas, 2)
        }
    
    def _generate_report_recommendations(self, report: Dict) -> List[str]:
        """Gera recomendacoes para o relatorio."""
        recommendations = []
        
        if report["summary"].get("avg_roas", 0) < 2:
            recommendations.append("Foque em otimizar campanhas existentes antes de escalar")
        else:
            recommendations.append("Performance solida - considere aumentar investimento")
        
        return recommendations


# Instancia global
learning_cycle = LearningCycle()

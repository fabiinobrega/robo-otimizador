# services/living_knowledge_base.py
"""
NEXORA PRIME - Base de Conhecimento Viva
Playbooks dinâmicos que evoluem com aprendizado
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class LivingKnowledgeBase:
    """Base de conhecimento dinâmica que evolui com o tempo."""
    
    def __init__(self):
        self.playbooks = {}
        self.best_practices = []
        self.case_studies = []
        self.learning_history = []
        self.knowledge_version = "1.0.0"
        
        # Inicializar playbooks padrão
        self._initialize_default_playbooks()
    
    def _initialize_default_playbooks(self):
        """Inicializa playbooks padrão do sistema."""
        self.playbooks = {
            "campaign_launch": {
                "id": "PB_CAMPAIGN_LAUNCH",
                "name": "Lançamento de Campanha",
                "version": "1.0",
                "steps": [
                    {"order": 1, "action": "Definir objetivo claro", "tips": ["ROAS mínimo", "CPA máximo"]},
                    {"order": 2, "action": "Configurar pixel/tracking", "tips": ["Verificar eventos", "Testar conversões"]},
                    {"order": 3, "action": "Criar audiências", "tips": ["Lookalike 1-3%", "Remarketing 180 dias"]},
                    {"order": 4, "action": "Desenvolver criativos", "tips": ["3-5 variações", "Formatos diferentes"]},
                    {"order": 5, "action": "Configurar orçamento", "tips": ["Começar conservador", "Escalar gradualmente"]},
                    {"order": 6, "action": "Lançar e monitorar", "tips": ["Primeiras 24h críticas", "Não alterar muito cedo"]}
                ],
                "success_metrics": ["CTR > 1%", "CPA dentro do target", "ROAS > 2"],
                "common_mistakes": ["Orçamento muito baixo", "Audiência muito ampla", "Poucos criativos"],
                "last_updated": datetime.now().isoformat(),
                "effectiveness_score": 0.85
            },
            "optimization_cycle": {
                "id": "PB_OPTIMIZATION",
                "name": "Ciclo de Otimização",
                "version": "1.0",
                "steps": [
                    {"order": 1, "action": "Analisar métricas", "tips": ["Comparar com benchmarks", "Identificar outliers"]},
                    {"order": 2, "action": "Identificar gargalos", "tips": ["Funil de conversão", "Custo por etapa"]},
                    {"order": 3, "action": "Priorizar ações", "tips": ["Maior impacto primeiro", "Quick wins"]},
                    {"order": 4, "action": "Implementar mudanças", "tips": ["Uma variável por vez", "Documentar tudo"]},
                    {"order": 5, "action": "Medir resultados", "tips": ["Aguardar dados suficientes", "Significância estatística"]},
                    {"order": 6, "action": "Iterar", "tips": ["Aprender com erros", "Escalar sucessos"]}
                ],
                "success_metrics": ["Melhoria de 10%+ em KPI principal"],
                "common_mistakes": ["Muitas mudanças simultâneas", "Conclusões prematuras"],
                "last_updated": datetime.now().isoformat(),
                "effectiveness_score": 0.90
            },
            "crisis_management": {
                "id": "PB_CRISIS",
                "name": "Gestão de Crise",
                "version": "1.0",
                "steps": [
                    {"order": 1, "action": "Identificar o problema", "tips": ["Queda de ROAS?", "Aumento de CPA?", "Queda de impressões?"]},
                    {"order": 2, "action": "Pausar se necessário", "tips": ["Proteger orçamento", "Evitar mais perdas"]},
                    {"order": 3, "action": "Diagnosticar causa raiz", "tips": ["Mudança de algoritmo?", "Saturação de audiência?", "Problema técnico?"]},
                    {"order": 4, "action": "Desenvolver plano de ação", "tips": ["Ações imediatas", "Ações de médio prazo"]},
                    {"order": 5, "action": "Executar correções", "tips": ["Priorizar por impacto", "Monitorar de perto"]},
                    {"order": 6, "action": "Documentar aprendizados", "tips": ["Prevenir recorrência", "Atualizar playbooks"]}
                ],
                "success_metrics": ["Retorno à performance anterior em 7 dias"],
                "common_mistakes": ["Pânico", "Mudanças drásticas sem análise"],
                "last_updated": datetime.now().isoformat(),
                "effectiveness_score": 0.80
            },
            "scaling_strategy": {
                "id": "PB_SCALING",
                "name": "Estratégia de Escala",
                "version": "1.0",
                "steps": [
                    {"order": 1, "action": "Validar performance base", "tips": ["ROAS estável por 7+ dias", "Volume consistente"]},
                    {"order": 2, "action": "Identificar limitadores", "tips": ["Audiência", "Orçamento", "Criativos"]},
                    {"order": 3, "action": "Escalar horizontalmente", "tips": ["Novas audiências", "Novos formatos"]},
                    {"order": 4, "action": "Escalar verticalmente", "tips": ["Aumentar orçamento 20-30%", "Aguardar estabilização"]},
                    {"order": 5, "action": "Diversificar canais", "tips": ["Meta + Google", "TikTok para jovens"]},
                    {"order": 6, "action": "Automatizar", "tips": ["Regras de otimização", "Alertas de performance"]}
                ],
                "success_metrics": ["Manter ROAS ao escalar", "Aumentar volume 2x+"],
                "common_mistakes": ["Escalar muito rápido", "Ignorar sinais de saturação"],
                "last_updated": datetime.now().isoformat(),
                "effectiveness_score": 0.75
            }
        }
    
    def get_playbook(self, playbook_id: str) -> Optional[Dict]:
        """Retorna um playbook específico."""
        return self.playbooks.get(playbook_id)
    
    def get_all_playbooks(self) -> Dict:
        """Retorna todos os playbooks."""
        return self.playbooks
    
    def add_playbook(self, playbook_id: str, name: str, steps: List[Dict], 
                    success_metrics: List[str], common_mistakes: List[str]) -> Dict:
        """Adiciona um novo playbook."""
        playbook = {
            "id": playbook_id,
            "name": name,
            "version": "1.0",
            "steps": steps,
            "success_metrics": success_metrics,
            "common_mistakes": common_mistakes,
            "last_updated": datetime.now().isoformat(),
            "effectiveness_score": 0.5,
            "usage_count": 0
        }
        
        self.playbooks[playbook_id] = playbook
        return {"success": True, "playbook": playbook}
    
    def update_playbook_effectiveness(self, playbook_id: str, outcome: str, metrics: Dict) -> Dict:
        """Atualiza a efetividade de um playbook baseado em resultados."""
        if playbook_id not in self.playbooks:
            return {"success": False, "error": "Playbook não encontrado"}
        
        playbook = self.playbooks[playbook_id]
        
        # Calcular novo score de efetividade
        current_score = playbook["effectiveness_score"]
        outcome_score = 1.0 if outcome == "success" else 0.5 if outcome == "partial" else 0.0
        
        # Média ponderada (mais peso para resultados recentes)
        new_score = (current_score * 0.7) + (outcome_score * 0.3)
        playbook["effectiveness_score"] = round(new_score, 2)
        playbook["last_updated"] = datetime.now().isoformat()
        playbook["usage_count"] = playbook.get("usage_count", 0) + 1
        
        # Registrar aprendizado
        self.learning_history.append({
            "playbook_id": playbook_id,
            "outcome": outcome,
            "metrics": metrics,
            "new_effectiveness": new_score,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "playbook_id": playbook_id,
            "new_effectiveness_score": new_score
        }
    
    def add_best_practice(self, category: str, title: str, description: str, 
                         evidence: Dict, source: str = "learned") -> Dict:
        """Adiciona uma nova best practice."""
        practice = {
            "id": f"BP_{len(self.best_practices) + 1}",
            "category": category,
            "title": title,
            "description": description,
            "evidence": evidence,
            "source": source,
            "confidence": 0.7 if source == "learned" else 0.9,
            "created_at": datetime.now().isoformat(),
            "validations": 0
        }
        
        self.best_practices.append(practice)
        return {"success": True, "practice": practice}
    
    def get_best_practices(self, category: Optional[str] = None) -> List[Dict]:
        """Retorna best practices, opcionalmente filtradas por categoria."""
        if category:
            return [bp for bp in self.best_practices if bp["category"] == category]
        return self.best_practices
    
    def add_case_study(self, title: str, context: Dict, actions: List[str], 
                      results: Dict, learnings: List[str]) -> Dict:
        """Adiciona um case study para referência futura."""
        case = {
            "id": f"CS_{len(self.case_studies) + 1}",
            "title": title,
            "context": context,
            "actions": actions,
            "results": results,
            "learnings": learnings,
            "created_at": datetime.now().isoformat(),
            "relevance_score": 0.8
        }
        
        self.case_studies.append(case)
        return {"success": True, "case_study": case}
    
    def get_relevant_case_studies(self, context: Dict, limit: int = 5) -> List[Dict]:
        """Retorna case studies relevantes para um contexto."""
        # Ordenar por relevância (simplificado)
        sorted_cases = sorted(
            self.case_studies,
            key=lambda x: x["relevance_score"],
            reverse=True
        )
        return sorted_cases[:limit]
    
    def get_recommendation_for_situation(self, situation: str, context: Dict) -> Dict:
        """Gera recomendação baseada na base de conhecimento."""
        # Mapear situação para playbook
        situation_playbook_map = {
            "launching": "campaign_launch",
            "optimizing": "optimization_cycle",
            "crisis": "crisis_management",
            "scaling": "scaling_strategy"
        }
        
        playbook_id = situation_playbook_map.get(situation, "optimization_cycle")
        playbook = self.playbooks.get(playbook_id)
        
        # Buscar best practices relevantes
        relevant_practices = self.get_best_practices(situation)[:3]
        
        # Buscar case studies
        relevant_cases = self.get_relevant_case_studies(context, 2)
        
        return {
            "recommended_playbook": playbook,
            "relevant_best_practices": relevant_practices,
            "similar_case_studies": relevant_cases,
            "confidence": playbook["effectiveness_score"] if playbook else 0.5
        }
    
    def evolve_knowledge(self, new_data: Dict) -> Dict:
        """Evolui a base de conhecimento com novos dados."""
        evolution_actions = []
        
        # Verificar se há padrões para criar novas best practices
        if new_data.get("success_pattern"):
            pattern = new_data["success_pattern"]
            self.add_best_practice(
                category=pattern.get("category", "general"),
                title=pattern.get("title", "Novo padrão identificado"),
                description=pattern.get("description", ""),
                evidence=pattern.get("evidence", {}),
                source="learned"
            )
            evolution_actions.append("Nova best practice adicionada")
        
        # Atualizar versão do conhecimento
        self.knowledge_version = f"1.{len(self.learning_history)}.0"
        
        return {
            "success": True,
            "evolution_actions": evolution_actions,
            "new_version": self.knowledge_version
        }
    
    def get_system_status(self) -> Dict:
        """Retorna o status da base de conhecimento."""
        return {
            "knowledge_version": self.knowledge_version,
            "total_playbooks": len(self.playbooks),
            "total_best_practices": len(self.best_practices),
            "total_case_studies": len(self.case_studies),
            "total_learnings": len(self.learning_history),
            "avg_playbook_effectiveness": sum(p["effectiveness_score"] for p in self.playbooks.values()) / len(self.playbooks) if self.playbooks else 0
        }


# Instância global
living_knowledge = LivingKnowledgeBase()

"""
CONTEXTUAL ASSISTANT - Assistente Interativo Contextual
Assistente inteligente que entende o contexto e oferece ajuda proativa
Nexora Prime V2 - Expansao Unicornio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

class ContextualAssistant:
    """Assistente interativo contextual com IA."""
    
    def __init__(self):
        self.name = "Contextual Assistant"
        self.version = "2.0.0"
        
        # Contexto atual do usuario
        self.user_context = {
            "current_page": None,
            "current_campaign": None,
            "recent_actions": [],
            "skill_level": "intermediate",
            "preferences": {},
            "session_start": None
        }
        
        # Base de conhecimento
        self.knowledge_base = self._initialize_knowledge_base()
        
        # Historico de conversas
        self.conversation_history = []
        
        # Sugestoes proativas
        self.proactive_suggestions = []
        
        # Tutoriais disponiveis
        self.tutorials = self._initialize_tutorials()
    
    def start_session(self, user_data: Dict = None) -> Dict[str, Any]:
        """Inicia sessao do assistente."""
        
        self.user_context["session_start"] = datetime.now().isoformat()
        
        if user_data:
            self.user_context["skill_level"] = user_data.get("skill_level", "intermediate")
            self.user_context["preferences"] = user_data.get("preferences", {})
        
        # Gerar saudacao contextual
        greeting = self._generate_greeting()
        
        return {
            "status": "session_started",
            "timestamp": datetime.now().isoformat(),
            "greeting": greeting,
            "quick_actions": self._get_quick_actions()
        }
    
    def update_context(self, context_update: Dict) -> Dict[str, Any]:
        """Atualiza contexto do usuario."""
        
        if "page" in context_update:
            self.user_context["current_page"] = context_update["page"]
        
        if "campaign" in context_update:
            self.user_context["current_campaign"] = context_update["campaign"]
        
        if "action" in context_update:
            self.user_context["recent_actions"].append({
                "action": context_update["action"],
                "timestamp": datetime.now().isoformat()
            })
            # Manter apenas ultimas 50 acoes
            self.user_context["recent_actions"] = self.user_context["recent_actions"][-50:]
        
        # Gerar sugestoes baseadas no novo contexto
        suggestions = self._generate_contextual_suggestions()
        
        return {
            "status": "context_updated",
            "current_context": {
                "page": self.user_context["current_page"],
                "campaign": self.user_context["current_campaign"]
            },
            "suggestions": suggestions
        }
    
    def ask(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """Processa pergunta do usuario."""
        
        # Atualizar contexto se fornecido
        if context:
            self.update_context(context)
        
        # Registrar pergunta
        self.conversation_history.append({
            "role": "user",
            "content": question,
            "timestamp": datetime.now().isoformat()
        })
        
        # Processar pergunta
        intent = self._detect_intent(question)
        response = self._generate_response(question, intent)
        
        # Registrar resposta
        self.conversation_history.append({
            "role": "assistant",
            "content": response["text"],
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "intent_detected": intent,
            "response": response,
            "follow_up_suggestions": self._get_follow_up_suggestions(intent)
        }
    
    def get_help(self, topic: str = None) -> Dict[str, Any]:
        """Obtem ajuda sobre um topico."""
        
        if topic:
            # Buscar no knowledge base
            help_content = self._search_knowledge_base(topic)
            tutorial = self._get_relevant_tutorial(topic)
        else:
            # Ajuda contextual baseada na pagina atual
            help_content = self._get_contextual_help()
            tutorial = self._get_contextual_tutorial()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "topic": topic or self.user_context["current_page"],
            "help_content": help_content,
            "tutorial": tutorial,
            "related_topics": self._get_related_topics(topic)
        }
    
    def get_proactive_tips(self) -> List[Dict]:
        """Obtem dicas proativas baseadas no contexto."""
        
        tips = []
        
        # Dicas baseadas na pagina atual
        page = self.user_context["current_page"]
        if page:
            tips.extend(self._get_page_tips(page))
        
        # Dicas baseadas em acoes recentes
        recent_actions = self.user_context["recent_actions"]
        if recent_actions:
            tips.extend(self._get_action_tips(recent_actions))
        
        # Dicas baseadas no nivel de habilidade
        skill_level = self.user_context["skill_level"]
        tips.extend(self._get_skill_tips(skill_level))
        
        return tips[:5]  # Retornar no maximo 5 dicas
    
    def explain_metric(self, metric_name: str, value: float = None, context: Dict = None) -> Dict[str, Any]:
        """Explica uma metrica de forma didatica."""
        
        explanations = {
            "roas": {
                "name": "ROAS (Return on Ad Spend)",
                "description": "Retorno sobre o investimento em anuncios. Indica quanto voce ganha para cada real investido.",
                "formula": "ROAS = Receita / Gasto com Anuncios",
                "good_value": ">= 2.0",
                "interpretation": lambda v: f"Seu ROAS de {v:.2f} significa que para cada R$1 investido, voce ganha R${v:.2f}." if v else ""
            },
            "cpa": {
                "name": "CPA (Custo por Aquisicao)",
                "description": "Quanto custa em media para adquirir um cliente ou conversao.",
                "formula": "CPA = Gasto Total / Numero de Conversoes",
                "good_value": "Depende do seu ticket medio",
                "interpretation": lambda v: f"Seu CPA de R${v:.2f} significa que cada conversao custa em media R${v:.2f}." if v else ""
            },
            "ctr": {
                "name": "CTR (Click-Through Rate)",
                "description": "Taxa de cliques. Porcentagem de pessoas que clicam no seu anuncio apos ve-lo.",
                "formula": "CTR = (Cliques / Impressoes) x 100",
                "good_value": ">= 1%",
                "interpretation": lambda v: f"Seu CTR de {v:.2f}% significa que {v:.2f} em cada 100 pessoas que veem seu anuncio clicam nele." if v else ""
            },
            "cpc": {
                "name": "CPC (Custo por Clique)",
                "description": "Quanto voce paga em media por cada clique no seu anuncio.",
                "formula": "CPC = Gasto Total / Numero de Cliques",
                "good_value": "Depende do nicho",
                "interpretation": lambda v: f"Seu CPC de R${v:.2f} significa que cada clique custa em media R${v:.2f}." if v else ""
            },
            "frequency": {
                "name": "Frequencia",
                "description": "Numero medio de vezes que cada pessoa viu seu anuncio.",
                "formula": "Frequencia = Impressoes / Alcance",
                "good_value": "1.5 - 3.0",
                "interpretation": lambda v: f"Sua frequencia de {v:.1f} significa que cada pessoa viu seu anuncio em media {v:.1f} vezes." if v else ""
            }
        }
        
        metric_key = metric_name.lower().replace(" ", "_")
        
        if metric_key not in explanations:
            return {
                "error": f"Metrica '{metric_name}' nao encontrada",
                "available_metrics": list(explanations.keys())
            }
        
        explanation = explanations[metric_key]
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "metric": explanation["name"],
            "description": explanation["description"],
            "formula": explanation["formula"],
            "good_value": explanation["good_value"]
        }
        
        if value is not None:
            result["your_value"] = value
            result["interpretation"] = explanation["interpretation"](value)
            result["assessment"] = self._assess_metric_value(metric_key, value)
        
        return result
    
    def suggest_next_action(self, current_state: Dict) -> Dict[str, Any]:
        """Sugere proxima acao baseada no estado atual."""
        
        suggestions = []
        
        # Analisar estado atual
        if current_state.get("has_campaigns", False):
            campaigns = current_state.get("campaigns", [])
            
            for campaign in campaigns:
                if campaign.get("roas", 0) < 1.5:
                    suggestions.append({
                        "action": "optimize_campaign",
                        "campaign_id": campaign.get("id"),
                        "reason": "ROAS abaixo do ideal",
                        "priority": "high"
                    })
                
                if campaign.get("frequency", 0) > 3:
                    suggestions.append({
                        "action": "refresh_creative",
                        "campaign_id": campaign.get("id"),
                        "reason": "Frequencia alta - publico saturado",
                        "priority": "medium"
                    })
        else:
            suggestions.append({
                "action": "create_campaign",
                "reason": "Voce ainda nao tem campanhas ativas",
                "priority": "high"
            })
        
        # Sugestoes gerais
        if not current_state.get("has_pixel", False):
            suggestions.append({
                "action": "setup_pixel",
                "reason": "Pixel nao configurado - essencial para rastreamento",
                "priority": "critical"
            })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current_state_summary": self._summarize_state(current_state),
            "suggestions": sorted(suggestions, key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x["priority"], 4)),
            "top_recommendation": suggestions[0] if suggestions else None
        }
    
    def get_tutorial(self, tutorial_id: str) -> Dict[str, Any]:
        """Obtem um tutorial especifico."""
        
        if tutorial_id not in self.tutorials:
            return {
                "error": "Tutorial nao encontrado",
                "available_tutorials": list(self.tutorials.keys())
            }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "tutorial": self.tutorials[tutorial_id]
        }
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Inicializa base de conhecimento."""
        return {
            "campanhas": {
                "criacao": "Para criar uma campanha eficaz, defina seu objetivo, publico-alvo, orcamento e criativos.",
                "otimizacao": "Otimize campanhas ajustando publicos, criativos e lances baseado em dados.",
                "escala": "Escale campanhas vencedoras aumentando orcamento gradualmente (20-30% por vez)."
            },
            "metricas": {
                "roas": "ROAS ideal varia por nicho, mas geralmente >= 2.0 e considerado bom.",
                "cpa": "CPA deve ser menor que seu ticket medio para ter lucro.",
                "ctr": "CTR >= 1% e considerado bom para a maioria dos nichos."
            },
            "publicos": {
                "lookalike": "Publicos semelhantes sao criados a partir de uma lista de clientes existentes.",
                "interesse": "Publicos por interesse sao baseados em comportamentos e preferencias.",
                "remarketing": "Remarketing alcanca pessoas que ja interagiram com seu negocio."
            }
        }
    
    def _initialize_tutorials(self) -> Dict[str, Dict]:
        """Inicializa tutoriais."""
        return {
            "criar_campanha": {
                "title": "Como Criar sua Primeira Campanha",
                "duration": "10 min",
                "steps": [
                    {"step": 1, "title": "Defina seu Objetivo", "description": "Escolha entre conversoes, trafego ou reconhecimento."},
                    {"step": 2, "title": "Configure o Publico", "description": "Selecione idade, localizacao e interesses."},
                    {"step": 3, "title": "Defina o Orcamento", "description": "Comece com R$50-100/dia para testes."},
                    {"step": 4, "title": "Crie os Anuncios", "description": "Use imagens de alta qualidade e textos persuasivos."},
                    {"step": 5, "title": "Revise e Publique", "description": "Confira todas as configuracoes antes de publicar."}
                ]
            },
            "otimizar_roas": {
                "title": "Como Melhorar seu ROAS",
                "duration": "15 min",
                "steps": [
                    {"step": 1, "title": "Analise os Dados", "description": "Identifique quais publicos e criativos performam melhor."},
                    {"step": 2, "title": "Pause o que nao Funciona", "description": "Desative anuncios com ROAS < 1."},
                    {"step": 3, "title": "Escale o que Funciona", "description": "Aumente orcamento dos vencedores."},
                    {"step": 4, "title": "Teste Novos Criativos", "description": "Sempre tenha testes rodando."},
                    {"step": 5, "title": "Refine os Publicos", "description": "Use dados para criar publicos mais precisos."}
                ]
            }
        }
    
    def _generate_greeting(self) -> str:
        """Gera saudacao contextual."""
        hour = datetime.now().hour
        
        if hour < 12:
            period = "Bom dia"
        elif hour < 18:
            period = "Boa tarde"
        else:
            period = "Boa noite"
        
        greetings = [
            f"{period}! Como posso ajudar voce hoje?",
            f"{period}! Estou aqui para ajudar com suas campanhas.",
            f"{period}! Pronto para otimizar seus resultados?"
        ]
        
        return random.choice(greetings)
    
    def _get_quick_actions(self) -> List[Dict]:
        """Obtem acoes rapidas."""
        return [
            {"id": "create_campaign", "label": "Criar Campanha", "icon": "plus"},
            {"id": "analyze_performance", "label": "Analisar Performance", "icon": "chart"},
            {"id": "get_recommendations", "label": "Ver Recomendacoes", "icon": "lightbulb"},
            {"id": "help", "label": "Ajuda", "icon": "question"}
        ]
    
    def _generate_contextual_suggestions(self) -> List[Dict]:
        """Gera sugestoes contextuais."""
        suggestions = []
        page = self.user_context["current_page"]
        
        page_suggestions = {
            "dashboard": [
                {"text": "Quer ver um resumo das suas campanhas?", "action": "show_summary"},
                {"text": "Posso identificar oportunidades de otimizacao", "action": "find_opportunities"}
            ],
            "campaigns": [
                {"text": "Precisa de ajuda para criar uma campanha?", "action": "tutorial_campaign"},
                {"text": "Posso analisar suas campanhas atuais", "action": "analyze_campaigns"}
            ],
            "analytics": [
                {"text": "Quer que eu explique alguma metrica?", "action": "explain_metrics"},
                {"text": "Posso gerar um relatorio detalhado", "action": "generate_report"}
            ]
        }
        
        return page_suggestions.get(page, [])
    
    def _detect_intent(self, question: str) -> str:
        """Detecta intencao da pergunta."""
        question_lower = question.lower()
        
        intents = {
            "create": ["criar", "nova", "comecar", "iniciar"],
            "optimize": ["otimizar", "melhorar", "aumentar", "escalar"],
            "explain": ["o que e", "como funciona", "explica", "significa"],
            "troubleshoot": ["problema", "erro", "nao funciona", "baixo"],
            "recommend": ["recomenda", "sugere", "devo", "melhor"]
        }
        
        for intent, keywords in intents.items():
            if any(kw in question_lower for kw in keywords):
                return intent
        
        return "general"
    
    def _generate_response(self, question: str, intent: str) -> Dict[str, Any]:
        """Gera resposta para a pergunta."""
        
        responses = {
            "create": {
                "text": "Posso ajudar voce a criar! Para comecar, me conte mais sobre seu objetivo. Voce quer criar uma campanha, um publico ou um criativo?",
                "actions": ["create_campaign", "create_audience", "create_creative"]
            },
            "optimize": {
                "text": "Otimizacao e essencial! Vou analisar seus dados e sugerir melhorias. Qual campanha voce gostaria de otimizar?",
                "actions": ["analyze_all", "select_campaign"]
            },
            "explain": {
                "text": "Claro, vou explicar! Sobre qual metrica ou funcionalidade voce gostaria de saber mais?",
                "actions": ["explain_roas", "explain_cpa", "explain_ctr"]
            },
            "troubleshoot": {
                "text": "Vamos resolver isso! Me conte mais detalhes sobre o problema que voce esta enfrentando.",
                "actions": ["describe_problem", "show_logs"]
            },
            "recommend": {
                "text": "Baseado nos seus dados, tenho algumas recomendacoes. Quer que eu mostre as principais oportunidades?",
                "actions": ["show_recommendations", "detailed_analysis"]
            },
            "general": {
                "text": "Estou aqui para ajudar! Voce pode me perguntar sobre campanhas, metricas, otimizacao ou qualquer duvida sobre a plataforma.",
                "actions": ["help", "tutorials", "contact_support"]
            }
        }
        
        return responses.get(intent, responses["general"])
    
    def _get_follow_up_suggestions(self, intent: str) -> List[str]:
        """Obtem sugestoes de follow-up."""
        suggestions = {
            "create": ["Como definir meu publico-alvo?", "Qual orcamento devo comecar?"],
            "optimize": ["O que e um bom ROAS?", "Como escalar sem perder performance?"],
            "explain": ["Explique outras metricas", "Como interpretar meus dados?"],
            "troubleshoot": ["Ver logs de erros", "Contatar suporte"],
            "recommend": ["Aplicar recomendacoes automaticamente", "Ver detalhes de cada sugestao"]
        }
        return suggestions.get(intent, ["Como posso ajudar mais?"])
    
    def _search_knowledge_base(self, topic: str) -> Dict[str, Any]:
        """Busca na base de conhecimento."""
        topic_lower = topic.lower()
        
        results = []
        for category, items in self.knowledge_base.items():
            for key, content in items.items():
                if topic_lower in key or topic_lower in content.lower():
                    results.append({"category": category, "topic": key, "content": content})
        
        return {"results": results, "count": len(results)}
    
    def _get_relevant_tutorial(self, topic: str) -> Optional[Dict]:
        """Obtem tutorial relevante."""
        topic_lower = topic.lower()
        
        for tid, tutorial in self.tutorials.items():
            if topic_lower in tid or topic_lower in tutorial["title"].lower():
                return {"id": tid, **tutorial}
        
        return None
    
    def _get_contextual_help(self) -> Dict[str, Any]:
        """Obtem ajuda contextual."""
        page = self.user_context["current_page"]
        
        help_content = {
            "dashboard": {"title": "Dashboard", "description": "Visao geral das suas campanhas e metricas principais."},
            "campaigns": {"title": "Campanhas", "description": "Gerencie e crie suas campanhas de anuncios."},
            "analytics": {"title": "Analytics", "description": "Analise detalhada de performance e metricas."}
        }
        
        return help_content.get(page, {"title": "Ajuda Geral", "description": "Selecione um topico para obter ajuda."})
    
    def _get_contextual_tutorial(self) -> Optional[Dict]:
        """Obtem tutorial contextual."""
        page = self.user_context["current_page"]
        
        page_tutorials = {
            "campaigns": "criar_campanha",
            "analytics": "otimizar_roas"
        }
        
        tutorial_id = page_tutorials.get(page)
        if tutorial_id and tutorial_id in self.tutorials:
            return {"id": tutorial_id, **self.tutorials[tutorial_id]}
        
        return None
    
    def _get_related_topics(self, topic: str) -> List[str]:
        """Obtem topicos relacionados."""
        related = {
            "roas": ["cpa", "conversoes", "otimizacao"],
            "cpa": ["roas", "orcamento", "escala"],
            "campanha": ["publico", "criativo", "orcamento"],
            "publico": ["lookalike", "interesse", "remarketing"]
        }
        
        if topic:
            return related.get(topic.lower(), ["campanhas", "metricas", "otimizacao"])
        return ["campanhas", "metricas", "otimizacao"]
    
    def _get_page_tips(self, page: str) -> List[Dict]:
        """Obtem dicas para a pagina."""
        tips = {
            "dashboard": [
                {"text": "Verifique suas metricas principais diariamente", "priority": "medium"},
                {"text": "Configure alertas para mudancas significativas", "priority": "low"}
            ],
            "campaigns": [
                {"text": "Sempre teste multiplos criativos", "priority": "high"},
                {"text": "Comece com orcamentos menores e escale gradualmente", "priority": "medium"}
            ]
        }
        return tips.get(page, [])
    
    def _get_action_tips(self, actions: List[Dict]) -> List[Dict]:
        """Obtem dicas baseadas em acoes."""
        return []
    
    def _get_skill_tips(self, skill_level: str) -> List[Dict]:
        """Obtem dicas baseadas no nivel."""
        tips = {
            "beginner": [{"text": "Comece pelo tutorial de criacao de campanhas", "priority": "high"}],
            "intermediate": [{"text": "Explore as funcoes de otimizacao automatica", "priority": "medium"}],
            "advanced": [{"text": "Use o Modo Guerra para escala agressiva", "priority": "low"}]
        }
        return tips.get(skill_level, [])
    
    def _assess_metric_value(self, metric: str, value: float) -> str:
        """Avalia valor de uma metrica."""
        thresholds = {
            "roas": {"good": 2.0, "warning": 1.5},
            "ctr": {"good": 1.0, "warning": 0.5},
            "cpa": {"good": 50, "warning": 100},
            "cpc": {"good": 1.0, "warning": 2.0},
            "frequency": {"good": 2.0, "warning": 3.5}
        }
        
        if metric not in thresholds:
            return "normal"
        
        t = thresholds[metric]
        
        if metric in ["cpa", "cpc", "frequency"]:
            if value <= t["good"]:
                return "excellent"
            elif value <= t["warning"]:
                return "good"
            return "needs_improvement"
        else:
            if value >= t["good"]:
                return "excellent"
            elif value >= t["warning"]:
                return "good"
            return "needs_improvement"
    
    def _summarize_state(self, state: Dict) -> str:
        """Resume estado atual."""
        parts = []
        
        if state.get("has_campaigns"):
            parts.append(f"{len(state.get('campaigns', []))} campanhas ativas")
        else:
            parts.append("Nenhuma campanha ativa")
        
        if state.get("has_pixel"):
            parts.append("Pixel configurado")
        else:
            parts.append("Pixel nao configurado")
        
        return " | ".join(parts)


# Instancia global
contextual_assistant = ContextualAssistant()

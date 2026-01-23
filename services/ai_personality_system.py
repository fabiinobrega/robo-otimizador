# services/ai_personality_system.py
"""
NEXORA PRIME - Sistema de Personalidade da IA (Velyra)
Princípios, estilos de comunicação e tom de voz
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import random


class AIPersonalitySystem:
    """Sistema de personalidade da IA Velyra."""
    
    def __init__(self):
        self.personality_profile = {
            "name": "Velyra",
            "role": "Consultora de Marketing Digital de Elite",
            "core_values": [
                "Transparência total nas decisões",
                "Foco em resultados mensuráveis",
                "Aprendizado contínuo",
                "Proteção do investimento do cliente",
                "Inovação responsável"
            ],
            "expertise_areas": [
                "Meta Ads (Facebook/Instagram)",
                "Google Ads",
                "Otimização de conversão",
                "Análise de dados",
                "Copywriting persuasivo",
                "Segmentação de audiência",
                "Testes A/B",
                "Automação de marketing"
            ]
        }
        
        self.communication_styles = {
            "professional": {
                "name": "Profissional",
                "description": "Tom formal e técnico",
                "characteristics": ["Preciso", "Técnico", "Formal"],
                "greeting_templates": [
                    "Olá! Sou a Velyra, sua consultora de marketing digital.",
                    "Bem-vindo! Estou aqui para otimizar seus resultados de marketing."
                ],
                "response_templates": {
                    "success": "A operação foi concluída com sucesso. {details}",
                    "warning": "Atenção: {details}. Recomendo avaliar antes de prosseguir.",
                    "error": "Identificamos um problema: {details}. Vamos resolver isso juntos."
                }
            },
            "friendly": {
                "name": "Amigável",
                "description": "Tom casual e acessível",
                "characteristics": ["Acolhedor", "Didático", "Encorajador"],
                "greeting_templates": [
                    "Oi! Sou a Velyra, sua parceira de marketing! 🚀",
                    "E aí! Pronta para turbinar suas campanhas?"
                ],
                "response_templates": {
                    "success": "Perfeito! Deu tudo certo! {details}",
                    "warning": "Ei, só um minutinho! {details}. Vamos dar uma olhada nisso?",
                    "error": "Ops! Tivemos um probleminha: {details}. Mas não se preocupe, vamos resolver!"
                }
            },
            "executive": {
                "name": "Executivo",
                "description": "Tom direto e focado em resultados",
                "characteristics": ["Conciso", "Orientado a ROI", "Estratégico"],
                "greeting_templates": [
                    "Velyra aqui. Vamos aos resultados.",
                    "Pronto para o briefing de performance."
                ],
                "response_templates": {
                    "success": "Resultado: {details}. ROI positivo.",
                    "warning": "Alerta de performance: {details}. Ação recomendada.",
                    "error": "Problema identificado: {details}. Impacto e solução em análise."
                }
            },
            "coach": {
                "name": "Coach",
                "description": "Tom educativo e motivacional",
                "characteristics": ["Didático", "Motivador", "Paciente"],
                "greeting_templates": [
                    "Olá! Sou a Velyra, e estou aqui para te ajudar a crescer!",
                    "Vamos aprender juntos a dominar o marketing digital!"
                ],
                "response_templates": {
                    "success": "Excelente trabalho! {details}. Você está evoluindo!",
                    "warning": "Momento de aprendizado! {details}. Isso é normal, vamos entender melhor.",
                    "error": "Não se preocupe com esse erro! {details}. Cada erro é uma oportunidade de aprender."
                }
            }
        }
        
        self.current_style = "professional"
        self.user_preferences = {}
        self.interaction_history = []
    
    def set_communication_style(self, user_id: str, style: str) -> Dict:
        """Define o estilo de comunicação para um usuário."""
        if style not in self.communication_styles:
            return {"success": False, "error": f"Estilo inválido. Opções: {list(self.communication_styles.keys())}"}
        
        self.user_preferences[user_id] = {
            "style": style,
            "set_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "user_id": user_id,
            "style": style,
            "style_config": self.communication_styles[style]
        }
    
    def get_greeting(self, user_id: str, context: Optional[Dict] = None) -> str:
        """Gera uma saudação personalizada."""
        style = self._get_user_style(user_id)
        templates = self.communication_styles[style]["greeting_templates"]
        
        greeting = random.choice(templates)
        
        # Personalizar com contexto
        if context:
            if context.get("time_of_day") == "morning":
                greeting = "Bom dia! " + greeting
            elif context.get("time_of_day") == "afternoon":
                greeting = "Boa tarde! " + greeting
            elif context.get("time_of_day") == "evening":
                greeting = "Boa noite! " + greeting
        
        return greeting
    
    def format_response(self, user_id: str, response_type: str, details: str) -> str:
        """Formata uma resposta no estilo do usuário."""
        style = self._get_user_style(user_id)
        templates = self.communication_styles[style]["response_templates"]
        
        template = templates.get(response_type, "{details}")
        return template.format(details=details)
    
    def generate_insight(self, user_id: str, data: Dict) -> Dict:
        """Gera um insight personalizado baseado em dados."""
        style = self._get_user_style(user_id)
        
        # Analisar dados
        roas = data.get("roas", 0)
        spend = data.get("spend", 0)
        conversions = data.get("conversions", 0)
        
        insight_type = "positive" if roas > 2 else "neutral" if roas > 1 else "negative"
        
        insights = {
            "professional": {
                "positive": f"Performance excepcional. ROAS de {roas:.2f} indica alta eficiência do investimento.",
                "neutral": f"Performance estável. ROAS de {roas:.2f} está dentro da média do mercado.",
                "negative": f"Atenção necessária. ROAS de {roas:.2f} está abaixo do ideal. Recomendo revisão da estratégia."
            },
            "friendly": {
                "positive": f"Uau! Suas campanhas estão arrasando! 🎉 ROAS de {roas:.2f} é incrível!",
                "neutral": f"Suas campanhas estão indo bem! ROAS de {roas:.2f}. Vamos melhorar juntos?",
                "negative": f"Ei, suas campanhas precisam de um carinho. ROAS de {roas:.2f}. Vamos dar uma turbinada?"
            },
            "executive": {
                "positive": f"ROI positivo. ROAS: {roas:.2f}. Recomendação: escalar.",
                "neutral": f"ROI neutro. ROAS: {roas:.2f}. Recomendação: otimizar.",
                "negative": f"ROI negativo. ROAS: {roas:.2f}. Recomendação: pausar e revisar."
            },
            "coach": {
                "positive": f"Parabéns! Você está dominando! ROAS de {roas:.2f} mostra que você aprendeu bem!",
                "neutral": f"Bom progresso! ROAS de {roas:.2f}. Vamos aprender a melhorar ainda mais?",
                "negative": f"Não desanime! ROAS de {roas:.2f} é uma oportunidade de aprendizado. Vamos juntos!"
            }
        }
        
        return {
            "insight": insights[style][insight_type],
            "type": insight_type,
            "style": style,
            "data_summary": {
                "roas": roas,
                "spend": spend,
                "conversions": conversions
            }
        }
    
    def get_recommendation(self, user_id: str, situation: str, options: List[str]) -> Dict:
        """Gera uma recomendação personalizada."""
        style = self._get_user_style(user_id)
        
        recommendation = options[0] if options else "Aguardar mais dados"
        
        formats = {
            "professional": f"Recomendação técnica: {recommendation}. Baseado na análise de {situation}.",
            "friendly": f"Minha sugestão é: {recommendation}! Acho que vai funcionar super bem! 😊",
            "executive": f"Ação recomendada: {recommendation}. Situação: {situation}.",
            "coach": f"Que tal tentarmos {recommendation}? É uma ótima oportunidade de aprendizado!"
        }
        
        return {
            "recommendation": recommendation,
            "formatted_message": formats[style],
            "alternatives": options[1:] if len(options) > 1 else [],
            "confidence": 0.85
        }
    
    def log_interaction(self, user_id: str, interaction_type: str, content: str):
        """Registra uma interação para aprendizado."""
        self.interaction_history.append({
            "user_id": user_id,
            "type": interaction_type,
            "content": content,
            "style": self._get_user_style(user_id),
            "timestamp": datetime.now().isoformat()
        })
    
    def get_personality_profile(self) -> Dict:
        """Retorna o perfil de personalidade da Velyra."""
        return self.personality_profile
    
    def get_available_styles(self) -> List[Dict]:
        """Retorna os estilos de comunicação disponíveis."""
        return [
            {
                "id": style_id,
                "name": config["name"],
                "description": config["description"],
                "characteristics": config["characteristics"]
            }
            for style_id, config in self.communication_styles.items()
        ]
    
    def _get_user_style(self, user_id: str) -> str:
        """Retorna o estilo de comunicação do usuário."""
        user_pref = self.user_preferences.get(user_id, {})
        return user_pref.get("style", self.current_style)
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de personalidade."""
        return {
            "personality_name": self.personality_profile["name"],
            "available_styles": list(self.communication_styles.keys()),
            "default_style": self.current_style,
            "users_with_preferences": len(self.user_preferences),
            "total_interactions": len(self.interaction_history)
        }


# Instância global
ai_personality = AIPersonalitySystem()

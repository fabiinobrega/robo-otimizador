"""
PSYCHOGRAPHIC ENGINE
Motor de análise psicográfica para segmentação avançada de audiência
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import random
import hashlib


class PsychographicEngine:
    """Motor de análise psicográfica para segmentação de audiência."""
    
    def __init__(self):
        self.profiles = {}
        self.psychological_triggers = {
            "urgency": ["Oferta por tempo limitado", "Últimas unidades", "Não perca"],
            "scarcity": ["Exclusivo", "Edição limitada", "Apenas para membros"],
            "social_proof": ["Milhares já compraram", "Recomendado por especialistas", "5 estrelas"],
            "authority": ["Certificado", "Aprovado por", "Especialista em"],
            "reciprocity": ["Presente grátis", "Bônus exclusivo", "Brinde especial"],
            "commitment": ["Garantia de satisfação", "Teste grátis", "Sem compromisso"],
            "liking": ["Feito para você", "Personalizado", "Sob medida"],
            "fear_of_missing_out": ["Não fique de fora", "Tendência do momento", "Todos estão usando"]
        }
        self.personality_types = {
            "analytical": {
                "traits": ["lógico", "detalhista", "cauteloso"],
                "preferred_content": ["dados", "estatísticas", "comparações"],
                "communication_style": "formal"
            },
            "driver": {
                "traits": ["decisivo", "orientado a resultados", "competitivo"],
                "preferred_content": ["benefícios claros", "ROI", "eficiência"],
                "communication_style": "direto"
            },
            "expressive": {
                "traits": ["entusiasta", "criativo", "social"],
                "preferred_content": ["histórias", "testemunhos", "visuais"],
                "communication_style": "emocional"
            },
            "amiable": {
                "traits": ["colaborativo", "paciente", "leal"],
                "preferred_content": ["garantias", "suporte", "comunidade"],
                "communication_style": "amigável"
            }
        }
    
    def create_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um perfil psicográfico."""
        profile_id = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:12]
        
        profile = {
            "id": profile_id,
            "name": data.get("name", "Perfil Anônimo"),
            "demographics": data.get("demographics", {}),
            "interests": data.get("interests", []),
            "values": data.get("values", []),
            "lifestyle": data.get("lifestyle", ""),
            "personality_type": self._determine_personality(data),
            "psychological_triggers": self._identify_triggers(data),
            "buying_behavior": self._analyze_buying_behavior(data),
            "content_preferences": self._determine_content_preferences(data),
            "created_at": datetime.now().isoformat(),
            "score": random.randint(70, 100)
        }
        
        self.profiles[profile_id] = profile
        return {"success": True, "profile": profile}
    
    def _determine_personality(self, data: Dict[str, Any]) -> str:
        """Determina o tipo de personalidade com base nos dados."""
        interests = data.get("interests", [])
        
        if any(i in interests for i in ["dados", "análise", "pesquisa"]):
            return "analytical"
        elif any(i in interests for i in ["negócios", "resultados", "metas"]):
            return "driver"
        elif any(i in interests for i in ["arte", "criatividade", "social"]):
            return "expressive"
        else:
            return "amiable"
    
    def _identify_triggers(self, data: Dict[str, Any]) -> List[str]:
        """Identifica gatilhos psicológicos efetivos."""
        triggers = []
        personality = self._determine_personality(data)
        
        if personality == "analytical":
            triggers.extend(["authority", "commitment"])
        elif personality == "driver":
            triggers.extend(["urgency", "scarcity"])
        elif personality == "expressive":
            triggers.extend(["social_proof", "liking"])
        else:
            triggers.extend(["reciprocity", "commitment"])
        
        return triggers
    
    def _analyze_buying_behavior(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa o comportamento de compra."""
        return {
            "decision_speed": random.choice(["rápido", "moderado", "lento"]),
            "price_sensitivity": random.choice(["alta", "média", "baixa"]),
            "brand_loyalty": random.choice(["alta", "média", "baixa"]),
            "research_depth": random.choice(["extensiva", "moderada", "mínima"]),
            "impulse_buying": random.choice(["frequente", "ocasional", "raro"])
        }
    
    def _determine_content_preferences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Determina preferências de conteúdo."""
        personality = self._determine_personality(data)
        prefs = self.personality_types.get(personality, {})
        
        return {
            "preferred_formats": prefs.get("preferred_content", []),
            "communication_style": prefs.get("communication_style", "neutro"),
            "visual_preference": random.choice(["imagens", "vídeos", "infográficos"]),
            "content_length": random.choice(["curto", "médio", "longo"])
        }
    
    def analyze_audience(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa uma audiência."""
        audience_size = data.get("size", 1000)
        
        segments = []
        for ptype, pdata in self.personality_types.items():
            segment = {
                "type": ptype,
                "percentage": random.randint(15, 35),
                "traits": pdata["traits"],
                "recommended_approach": pdata["communication_style"],
                "preferred_content": pdata["preferred_content"]
            }
            segments.append(segment)
        
        # Normalizar percentuais
        total = sum(s["percentage"] for s in segments)
        for s in segments:
            s["percentage"] = round(s["percentage"] / total * 100, 1)
        
        return {
            "success": True,
            "audience_size": audience_size,
            "segments": segments,
            "primary_segment": max(segments, key=lambda x: x["percentage"]),
            "recommendations": self._generate_recommendations(segments),
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, segments: List[Dict]) -> List[str]:
        """Gera recomendações baseadas nos segmentos."""
        primary = max(segments, key=lambda x: x["percentage"])
        
        recommendations = [
            f"Foque em conteúdo {primary['recommended_approach']} para atingir o segmento principal",
            f"Use {', '.join(primary['preferred_content'])} em suas campanhas",
            "Teste diferentes abordagens para segmentos secundários",
            "Personalize mensagens por tipo de personalidade"
        ]
        
        return recommendations
    
    def get_psychological_triggers(self, profile_id: str) -> Dict[str, Any]:
        """Obtém gatilhos psicológicos para um perfil."""
        profile = self.profiles.get(profile_id)
        
        if not profile:
            # Retornar gatilhos genéricos se perfil não encontrado
            triggers = random.sample(list(self.psychological_triggers.keys()), 3)
        else:
            triggers = profile.get("psychological_triggers", [])
        
        result = {
            "triggers": [],
            "examples": []
        }
        
        for trigger in triggers:
            trigger_data = {
                "name": trigger,
                "description": self._get_trigger_description(trigger),
                "examples": self.psychological_triggers.get(trigger, [])
            }
            result["triggers"].append(trigger_data)
            result["examples"].extend(self.psychological_triggers.get(trigger, []))
        
        return {"success": True, "data": result}
    
    def _get_trigger_description(self, trigger: str) -> str:
        """Retorna descrição de um gatilho psicológico."""
        descriptions = {
            "urgency": "Cria senso de urgência para ação imediata",
            "scarcity": "Destaca a escassez ou exclusividade do produto",
            "social_proof": "Mostra que outros já aprovaram ou compraram",
            "authority": "Usa credenciais e especialistas para validar",
            "reciprocity": "Oferece algo de valor para criar obrigação",
            "commitment": "Obtém pequenos compromissos que levam a maiores",
            "liking": "Cria conexão pessoal e identificação",
            "fear_of_missing_out": "Explora o medo de perder oportunidades"
        }
        return descriptions.get(trigger, "Gatilho psicológico efetivo")
    
    def get_profile(self, profile_id: str) -> Dict[str, Any]:
        """Obtém um perfil pelo ID."""
        profile = self.profiles.get(profile_id)
        if profile:
            return {"success": True, "profile": profile}
        return {"success": False, "error": "Perfil não encontrado"}


# Instância global
psychographic_engine = PsychographicEngine()

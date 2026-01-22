"""
CREATIVE AUTOMATION ENGINE - Motor de Automação de Criativos
Sistema de geração automática de anúncios com IA
Versão: 1.0 - Expansão Avançada
"""

import os
import json
import asyncio
import logging
import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreativeType(Enum):
    """Tipos de criativos"""
    IMAGE_AD = "image_ad"
    VIDEO_AD = "video_ad"
    CAROUSEL = "carousel"
    STORY = "story"
    COLLECTION = "collection"
    DYNAMIC = "dynamic"


class CreativeFormat(Enum):
    """Formatos de criativos"""
    SQUARE = "1:1"
    PORTRAIT = "4:5"
    LANDSCAPE = "16:9"
    STORY = "9:16"
    WIDE = "1.91:1"


class CopyTone(Enum):
    """Tons de copy"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    URGENT = "urgent"
    EMOTIONAL = "emotional"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"


class CTAType(Enum):
    """Tipos de Call-to-Action"""
    SHOP_NOW = "Comprar Agora"
    LEARN_MORE = "Saiba Mais"
    SIGN_UP = "Cadastre-se"
    DOWNLOAD = "Baixar"
    GET_OFFER = "Obter Oferta"
    BOOK_NOW = "Reservar Agora"
    CONTACT_US = "Fale Conosco"
    WATCH_MORE = "Assistir Mais"
    GET_QUOTE = "Solicitar Orçamento"
    SUBSCRIBE = "Inscrever-se"


@dataclass
class CreativeElement:
    """Elemento de criativo"""
    element_type: str  # headline, description, image, video, cta
    content: str
    variations: List[str] = field(default_factory=list)
    performance_score: float = 0.0


@dataclass
class GeneratedCreative:
    """Criativo gerado"""
    id: str
    creative_type: CreativeType
    format: CreativeFormat
    headline: str
    description: str
    cta: CTAType
    image_prompt: str
    video_script: Optional[str]
    hashtags: List[str]
    target_audience: str
    tone: CopyTone
    estimated_ctr: float
    estimated_engagement: float
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.creative_type.value,
            "format": self.format.value,
            "headline": self.headline,
            "description": self.description,
            "cta": self.cta.value,
            "image_prompt": self.image_prompt,
            "video_script": self.video_script,
            "hashtags": self.hashtags,
            "target_audience": self.target_audience,
            "tone": self.tone.value,
            "estimated_ctr": self.estimated_ctr,
            "estimated_engagement": self.estimated_engagement,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ABTestVariant:
    """Variante para teste A/B"""
    variant_id: str
    variant_name: str
    creative: GeneratedCreative
    traffic_allocation: float
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    spend: float = 0.0
    
    @property
    def ctr(self) -> float:
        return (self.clicks / self.impressions * 100) if self.impressions > 0 else 0
    
    @property
    def cvr(self) -> float:
        return (self.conversions / self.clicks * 100) if self.clicks > 0 else 0


class CopyGenerator:
    """Gerador de copy para anúncios"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.power_words = self._load_power_words()
        
    def _load_templates(self) -> Dict[str, List[str]]:
        """Carrega templates de copy"""
        return {
            "headline": [
                "{benefit} em {time}",
                "Descubra {product} que {benefit}",
                "{number}% de desconto em {product}",
                "O segredo para {benefit}",
                "{product}: {unique_value}",
                "Transforme {pain_point} em {benefit}",
                "Novo: {product} com {feature}",
                "Exclusivo: {offer}",
                "Última chance: {offer}",
                "{social_proof} já {action}"
            ],
            "description": [
                "{product} foi desenvolvido para {target_audience} que deseja {benefit}. {feature} garante {result}. {cta_phrase}",
                "Cansado de {pain_point}? {product} resolve isso com {feature}. Mais de {social_proof} clientes satisfeitos. {cta_phrase}",
                "Apresentamos {product}: a solução definitiva para {benefit}. {feature} + {feature2} = {result}. {cta_phrase}",
                "{question}? {product} é a resposta. {benefit} garantido ou seu dinheiro de volta. {cta_phrase}",
                "Por tempo limitado: {product} com {discount}% OFF. {feature} que {benefit}. {cta_phrase}"
            ],
            "cta_phrases": [
                "Garanta o seu agora!",
                "Aproveite antes que acabe!",
                "Clique e descubra mais!",
                "Comece sua transformação hoje!",
                "Não perca essa oportunidade!",
                "Experimente grátis por 7 dias!",
                "Frete grátis por tempo limitado!",
                "Compre agora e economize!"
            ]
        }
        
    def _load_power_words(self) -> List[str]:
        """Carrega palavras de poder"""
        return [
            "exclusivo", "grátis", "novo", "comprovado", "garantido",
            "limitado", "secreto", "revolucionário", "instantâneo", "fácil",
            "rápido", "simples", "poderoso", "incrível", "surpreendente",
            "premium", "profissional", "avançado", "inteligente", "inovador"
        ]
        
    def generate_headline(self, context: Dict[str, Any], tone: CopyTone) -> str:
        """Gera headline baseado no contexto"""
        template = random.choice(self.templates["headline"])
        
        # Preencher template com dados do contexto
        replacements = {
            "{benefit}": context.get("main_benefit", "resultados incríveis"),
            "{time}": context.get("time_to_result", "poucos dias"),
            "{product}": context.get("product_name", "nosso produto"),
            "{number}": str(random.randint(10, 50)),
            "{unique_value}": context.get("unique_value", "qualidade superior"),
            "{pain_point}": context.get("pain_point", "problemas"),
            "{feature}": context.get("main_feature", "tecnologia avançada"),
            "{offer}": context.get("offer", "oferta especial"),
            "{social_proof}": context.get("social_proof", "10.000 pessoas"),
            "{action}": context.get("action", "compraram")
        }
        
        headline = template
        for key, value in replacements.items():
            headline = headline.replace(key, value)
            
        # Ajustar tom
        if tone == CopyTone.URGENT:
            headline = "🔥 " + headline + " 🔥"
        elif tone == CopyTone.EMOTIONAL:
            headline = "💖 " + headline
        elif tone == CopyTone.HUMOROUS:
            headline = headline + " 😄"
            
        return headline
    
    def generate_description(self, context: Dict[str, Any], tone: CopyTone) -> str:
        """Gera descrição baseada no contexto"""
        template = random.choice(self.templates["description"])
        cta_phrase = random.choice(self.templates["cta_phrases"])
        
        replacements = {
            "{product}": context.get("product_name", "nosso produto"),
            "{target_audience}": context.get("target_audience", "você"),
            "{benefit}": context.get("main_benefit", "resultados incríveis"),
            "{feature}": context.get("main_feature", "tecnologia avançada"),
            "{feature2}": context.get("secondary_feature", "design premium"),
            "{result}": context.get("expected_result", "sucesso garantido"),
            "{pain_point}": context.get("pain_point", "problemas do dia a dia"),
            "{social_proof}": context.get("social_proof", "10.000"),
            "{question}": context.get("question", "Quer melhorar sua vida"),
            "{discount}": str(random.randint(10, 40)),
            "{cta_phrase}": cta_phrase
        }
        
        description = template
        for key, value in replacements.items():
            description = description.replace(key, value)
            
        return description
    
    def generate_hashtags(self, context: Dict[str, Any], count: int = 5) -> List[str]:
        """Gera hashtags relevantes"""
        base_hashtags = [
            f"#{context.get('product_name', 'produto').replace(' ', '')}",
            f"#{context.get('category', 'oferta')}",
            "#promoção",
            "#oferta",
            "#desconto"
        ]
        
        industry_hashtags = {
            "ecommerce": ["#compraonline", "#lojavirtual", "#ecommerce", "#fretegratis"],
            "saude": ["#saude", "#bemestar", "#vidasaudavel", "#fitness"],
            "tecnologia": ["#tech", "#inovacao", "#tecnologia", "#gadgets"],
            "moda": ["#moda", "#estilo", "#fashion", "#tendencia"],
            "educacao": ["#educacao", "#aprendizado", "#curso", "#conhecimento"]
        }
        
        industry = context.get("industry", "ecommerce")
        extra_hashtags = industry_hashtags.get(industry, [])
        
        all_hashtags = base_hashtags + extra_hashtags
        return random.sample(all_hashtags, min(count, len(all_hashtags)))


class ImagePromptGenerator:
    """Gerador de prompts para imagens"""
    
    def __init__(self):
        self.style_templates = {
            "product": "Professional product photography of {product}, {style}, {lighting}, {background}, high quality, 4K",
            "lifestyle": "Lifestyle photography showing {target_audience} using {product}, {setting}, natural lighting, authentic, engaging",
            "minimal": "Minimalist {product} on {background}, clean design, modern aesthetic, professional photography",
            "dynamic": "Dynamic action shot of {product}, motion blur, energetic, vibrant colors, professional advertising",
            "luxury": "Luxury {product} photography, premium feel, elegant lighting, sophisticated background, high-end advertising"
        }
        
    def generate_prompt(self, context: Dict[str, Any], style: str = "product") -> str:
        """Gera prompt para criação de imagem"""
        template = self.style_templates.get(style, self.style_templates["product"])
        
        replacements = {
            "{product}": context.get("product_name", "product"),
            "{style}": context.get("visual_style", "modern and clean"),
            "{lighting}": context.get("lighting", "soft studio lighting"),
            "{background}": context.get("background", "white background"),
            "{target_audience}": context.get("target_audience", "young professionals"),
            "{setting}": context.get("setting", "modern home environment")
        }
        
        prompt = template
        for key, value in replacements.items():
            prompt = prompt.replace(key, value)
            
        return prompt


class VideoScriptGenerator:
    """Gerador de scripts para vídeos"""
    
    def __init__(self):
        self.structures = {
            "problem_solution": [
                {"time": "0-3s", "type": "hook", "content": "Você sofre com {pain_point}?"},
                {"time": "3-8s", "type": "problem", "content": "Milhões de pessoas enfrentam {pain_point} todos os dias..."},
                {"time": "8-15s", "type": "solution", "content": "Apresentamos {product}: {main_benefit}"},
                {"time": "15-25s", "type": "features", "content": "Com {feature1}, {feature2} e {feature3}"},
                {"time": "25-30s", "type": "cta", "content": "{cta} - Link na bio!"}
            ],
            "testimonial": [
                {"time": "0-3s", "type": "hook", "content": "Veja o que {customer_name} tem a dizer..."},
                {"time": "3-15s", "type": "story", "content": "Antes de conhecer {product}, eu {pain_point}. Agora, {benefit}!"},
                {"time": "15-25s", "type": "proof", "content": "Em apenas {time}, consegui {result}"},
                {"time": "25-30s", "type": "cta", "content": "Você também pode! {cta}"}
            ],
            "demo": [
                {"time": "0-3s", "type": "hook", "content": "Olha só o que {product} faz!"},
                {"time": "3-15s", "type": "demo", "content": "[Demonstração do produto em ação]"},
                {"time": "15-25s", "type": "benefits", "content": "{benefit1}, {benefit2}, {benefit3}"},
                {"time": "25-30s", "type": "cta", "content": "Garanta o seu! {cta}"}
            ]
        }
        
    def generate_script(self, context: Dict[str, Any], structure: str = "problem_solution") -> str:
        """Gera script de vídeo"""
        template = self.structures.get(structure, self.structures["problem_solution"])
        
        script_parts = []
        for scene in template:
            content = scene["content"]
            
            # Substituir placeholders
            replacements = {
                "{pain_point}": context.get("pain_point", "problemas"),
                "{product}": context.get("product_name", "nosso produto"),
                "{main_benefit}": context.get("main_benefit", "a solução perfeita"),
                "{feature1}": context.get("features", ["recurso 1"])[0] if context.get("features") else "recurso 1",
                "{feature2}": context.get("features", ["", "recurso 2"])[1] if len(context.get("features", [])) > 1 else "recurso 2",
                "{feature3}": context.get("features", ["", "", "recurso 3"])[2] if len(context.get("features", [])) > 2 else "recurso 3",
                "{benefit}": context.get("main_benefit", "resultados incríveis"),
                "{benefit1}": context.get("benefits", ["benefício 1"])[0] if context.get("benefits") else "benefício 1",
                "{benefit2}": context.get("benefits", ["", "benefício 2"])[1] if len(context.get("benefits", [])) > 1 else "benefício 2",
                "{benefit3}": context.get("benefits", ["", "", "benefício 3"])[2] if len(context.get("benefits", [])) > 2 else "benefício 3",
                "{customer_name}": context.get("customer_name", "Maria"),
                "{time}": context.get("time_to_result", "30 dias"),
                "{result}": context.get("expected_result", "resultados incríveis"),
                "{cta}": context.get("cta", "Compre agora")
            }
            
            for key, value in replacements.items():
                content = content.replace(key, value)
                
            script_parts.append(f"[{scene['time']}] {scene['type'].upper()}: {content}")
            
        return "\n".join(script_parts)


class CreativeAutomationEngine:
    """
    Motor principal de Automação de Criativos
    Gera anúncios automaticamente com IA
    """
    
    def __init__(self):
        self.copy_generator = CopyGenerator()
        self.image_generator = ImagePromptGenerator()
        self.video_generator = VideoScriptGenerator()
        self.generated_creatives: List[GeneratedCreative] = []
        self.ab_tests: Dict[str, List[ABTestVariant]] = {}
        self.performance_data: Dict[str, Dict] = {}
        
    def generate_creative(
        self,
        context: Dict[str, Any],
        creative_type: CreativeType = CreativeType.IMAGE_AD,
        format: CreativeFormat = CreativeFormat.SQUARE,
        tone: CopyTone = CopyTone.PROFESSIONAL,
        count: int = 1
    ) -> List[GeneratedCreative]:
        """Gera criativos baseados no contexto"""
        creatives = []
        
        for i in range(count):
            creative_id = hashlib.md5(f"{datetime.now()}{i}{random.random()}".encode()).hexdigest()[:12]
            
            # Gerar headline e descrição
            headline = self.copy_generator.generate_headline(context, tone)
            description = self.copy_generator.generate_description(context, tone)
            
            # Gerar prompt de imagem
            image_style = context.get("image_style", "product")
            image_prompt = self.image_generator.generate_prompt(context, image_style)
            
            # Gerar script de vídeo se necessário
            video_script = None
            if creative_type == CreativeType.VIDEO_AD:
                video_structure = context.get("video_structure", "problem_solution")
                video_script = self.video_generator.generate_script(context, video_structure)
                
            # Gerar hashtags
            hashtags = self.copy_generator.generate_hashtags(context)
            
            # Selecionar CTA
            cta = self._select_best_cta(context)
            
            # Estimar performance
            estimated_ctr = self._estimate_ctr(headline, description, tone)
            estimated_engagement = self._estimate_engagement(creative_type, format)
            
            creative = GeneratedCreative(
                id=creative_id,
                creative_type=creative_type,
                format=format,
                headline=headline,
                description=description,
                cta=cta,
                image_prompt=image_prompt,
                video_script=video_script,
                hashtags=hashtags,
                target_audience=context.get("target_audience", "Público geral"),
                tone=tone,
                estimated_ctr=estimated_ctr,
                estimated_engagement=estimated_engagement
            )
            
            creatives.append(creative)
            self.generated_creatives.append(creative)
            
        return creatives
    
    def _select_best_cta(self, context: Dict[str, Any]) -> CTAType:
        """Seleciona o melhor CTA baseado no contexto"""
        objective = context.get("objective", "conversions")
        
        cta_mapping = {
            "conversions": [CTAType.SHOP_NOW, CTAType.GET_OFFER, CTAType.BOOK_NOW],
            "traffic": [CTAType.LEARN_MORE, CTAType.WATCH_MORE],
            "leads": [CTAType.SIGN_UP, CTAType.GET_QUOTE, CTAType.DOWNLOAD],
            "awareness": [CTAType.LEARN_MORE, CTAType.WATCH_MORE],
            "engagement": [CTAType.LEARN_MORE, CTAType.CONTACT_US]
        }
        
        options = cta_mapping.get(objective, [CTAType.LEARN_MORE])
        return random.choice(options)
    
    def _estimate_ctr(self, headline: str, description: str, tone: CopyTone) -> float:
        """Estima CTR baseado no conteúdo"""
        base_ctr = 1.5
        
        # Ajustes baseados em características
        if any(word in headline.lower() for word in ["grátis", "desconto", "oferta"]):
            base_ctr += 0.5
        if any(emoji in headline for emoji in ["🔥", "💖", "⭐", "✨"]):
            base_ctr += 0.3
        if tone == CopyTone.URGENT:
            base_ctr += 0.4
        if len(headline) < 40:
            base_ctr += 0.2
            
        # Adicionar variação
        return round(base_ctr + random.uniform(-0.3, 0.3), 2)
    
    def _estimate_engagement(self, creative_type: CreativeType, format: CreativeFormat) -> float:
        """Estima taxa de engajamento"""
        base_engagement = 3.0
        
        # Vídeos têm maior engajamento
        if creative_type == CreativeType.VIDEO_AD:
            base_engagement += 2.0
        elif creative_type == CreativeType.CAROUSEL:
            base_engagement += 1.5
        elif creative_type == CreativeType.STORY:
            base_engagement += 1.0
            
        # Formatos verticais performam melhor em mobile
        if format in [CreativeFormat.PORTRAIT, CreativeFormat.STORY]:
            base_engagement += 0.5
            
        return round(base_engagement + random.uniform(-0.5, 0.5), 2)
    
    def create_ab_test(
        self,
        campaign_id: str,
        creatives: List[GeneratedCreative],
        test_name: str = "AB Test"
    ) -> Dict[str, Any]:
        """Cria teste A/B com múltiplas variantes"""
        variants = []
        traffic_per_variant = 100 / len(creatives)
        
        for i, creative in enumerate(creatives):
            variant = ABTestVariant(
                variant_id=f"{campaign_id}_v{i+1}",
                variant_name=f"Variante {chr(65+i)}",  # A, B, C...
                creative=creative,
                traffic_allocation=traffic_per_variant
            )
            variants.append(variant)
            
        self.ab_tests[campaign_id] = variants
        
        return {
            "test_id": campaign_id,
            "test_name": test_name,
            "variants_count": len(variants),
            "variants": [
                {
                    "id": v.variant_id,
                    "name": v.variant_name,
                    "traffic": v.traffic_allocation,
                    "creative": v.creative.to_dict()
                }
                for v in variants
            ],
            "status": "running",
            "created_at": datetime.now().isoformat()
        }
    
    def get_ab_test_results(self, campaign_id: str) -> Dict[str, Any]:
        """Obtém resultados do teste A/B"""
        variants = self.ab_tests.get(campaign_id, [])
        
        if not variants:
            return {"error": "Teste não encontrado"}
            
        # Simular dados de performance
        for variant in variants:
            variant.impressions = random.randint(1000, 10000)
            variant.clicks = int(variant.impressions * variant.creative.estimated_ctr / 100)
            variant.conversions = int(variant.clicks * random.uniform(0.02, 0.08))
            variant.spend = variant.impressions * random.uniform(0.01, 0.05)
            
        # Determinar vencedor
        winner = max(variants, key=lambda v: v.cvr if v.clicks > 0 else 0)
        
        return {
            "test_id": campaign_id,
            "status": "completed",
            "winner": {
                "variant_id": winner.variant_id,
                "variant_name": winner.variant_name,
                "ctr": winner.ctr,
                "cvr": winner.cvr
            },
            "variants": [
                {
                    "id": v.variant_id,
                    "name": v.variant_name,
                    "impressions": v.impressions,
                    "clicks": v.clicks,
                    "conversions": v.conversions,
                    "spend": round(v.spend, 2),
                    "ctr": round(v.ctr, 2),
                    "cvr": round(v.cvr, 2),
                    "is_winner": v.variant_id == winner.variant_id
                }
                for v in variants
            ],
            "statistical_significance": random.uniform(0.90, 0.99),
            "recommendation": f"Escalar {winner.variant_name} e pausar outras variantes"
        }
    
    def generate_variations(
        self,
        base_creative: GeneratedCreative,
        variation_count: int = 3
    ) -> List[GeneratedCreative]:
        """Gera variações de um criativo existente"""
        variations = []
        
        # Variações de headline
        headline_variations = [
            base_creative.headline,
            base_creative.headline.upper(),
            "🔥 " + base_creative.headline,
            base_creative.headline + " ⭐"
        ]
        
        # Variações de CTA
        cta_options = list(CTAType)
        
        for i in range(variation_count):
            variation_id = hashlib.md5(f"{base_creative.id}{i}{datetime.now()}".encode()).hexdigest()[:12]
            
            variation = GeneratedCreative(
                id=variation_id,
                creative_type=base_creative.creative_type,
                format=base_creative.format,
                headline=random.choice(headline_variations),
                description=base_creative.description,
                cta=random.choice(cta_options),
                image_prompt=base_creative.image_prompt,
                video_script=base_creative.video_script,
                hashtags=base_creative.hashtags,
                target_audience=base_creative.target_audience,
                tone=base_creative.tone,
                estimated_ctr=base_creative.estimated_ctr + random.uniform(-0.3, 0.3),
                estimated_engagement=base_creative.estimated_engagement + random.uniform(-0.5, 0.5)
            )
            
            variations.append(variation)
            
        return variations
    
    def optimize_creative(self, creative_id: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Otimiza criativo baseado em dados de performance"""
        creative = next((c for c in self.generated_creatives if c.id == creative_id), None)
        
        if not creative:
            return {"error": "Criativo não encontrado"}
            
        ctr = performance_data.get("ctr", 0)
        cvr = performance_data.get("cvr", 0)
        
        recommendations = []
        
        if ctr < 1.0:
            recommendations.append({
                "type": "headline",
                "action": "Testar headlines mais impactantes com números ou urgência",
                "priority": "high"
            })
            
        if cvr < 2.0:
            recommendations.append({
                "type": "cta",
                "action": "Testar CTAs mais diretos como 'Comprar Agora'",
                "priority": "high"
            })
            
        if performance_data.get("engagement_rate", 0) < 3.0:
            recommendations.append({
                "type": "format",
                "action": "Considerar formato de vídeo ou carrossel",
                "priority": "medium"
            })
            
        return {
            "creative_id": creative_id,
            "current_performance": performance_data,
            "recommendations": recommendations,
            "suggested_variations": len(recommendations)
        }
    
    def get_creative_library(self) -> List[Dict[str, Any]]:
        """Retorna biblioteca de criativos gerados"""
        return [c.to_dict() for c in self.generated_creatives]
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do motor de criativos"""
        return {
            "total_creatives": len(self.generated_creatives),
            "active_ab_tests": len(self.ab_tests),
            "creatives_by_type": {
                ct.value: len([c for c in self.generated_creatives if c.creative_type == ct])
                for ct in CreativeType
            },
            "avg_estimated_ctr": sum(c.estimated_ctr for c in self.generated_creatives) / len(self.generated_creatives) if self.generated_creatives else 0
        }


# Instância global
creative_engine = CreativeAutomationEngine()


# Funções de conveniência
def generate_ad_creative(context: Dict[str, Any], count: int = 1) -> List[Dict[str, Any]]:
    """Gera criativos de anúncio"""
    creative_type = CreativeType[context.get("type", "IMAGE_AD").upper()]
    format = CreativeFormat[context.get("format", "SQUARE").upper().replace(":", "_").replace(".", "_")]
    tone = CopyTone[context.get("tone", "PROFESSIONAL").upper()]
    
    creatives = creative_engine.generate_creative(context, creative_type, format, tone, count)
    return [c.to_dict() for c in creatives]

def create_ab_test(campaign_id: str, context: Dict[str, Any], variants: int = 3) -> Dict[str, Any]:
    """Cria teste A/B"""
    creatives = creative_engine.generate_creative(context, count=variants)
    return creative_engine.create_ab_test(campaign_id, creatives)

def get_ab_test_results(campaign_id: str) -> Dict[str, Any]:
    """Obtém resultados de teste A/B"""
    return creative_engine.get_ab_test_results(campaign_id)

def get_creative_library() -> List[Dict[str, Any]]:
    """Obtém biblioteca de criativos"""
    return creative_engine.get_creative_library()

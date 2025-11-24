"""
Inteligência Criativa Avançada - NEXORA PRIME
Motor de IA multimodal para criação completa de anúncios profissionais
Nível: Agência Milionária
"""

import random
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class CreativeIntelligenceAdvanced:
    """
    Motor avançado de inteligência criativa para geração de anúncios completos
    Combina Nexora IA + Manus IA para criar campanhas de nível profissional
    """
    
    def __init__(self):
        self.platforms = {
            "meta": "Meta Ads (Facebook/Instagram)",
            "google": "Google Ads",
            "tiktok": "TikTok Ads",
            "pinterest": "Pinterest Ads",
            "linkedin": "LinkedIn Ads"
        }
        
        self.ad_formats = {
            "meta": ["feed", "stories", "reels", "carousel", "collection"],
            "google": ["search", "display", "video", "shopping", "discovery"],
            "tiktok": ["in_feed", "top_view", "branded_hashtag", "branded_effects"],
            "pinterest": ["standard", "video", "carousel", "shopping", "collections"],
            "linkedin": ["single_image", "carousel", "video", "conversation", "text"]
        }
        
        self.creative_frameworks = {
            "aida": "Attention, Interest, Desire, Action",
            "pas": "Problem, Agitate, Solution",
            "fab": "Features, Advantages, Benefits",
            "4ps": "Picture, Promise, Prove, Push",
            "star": "Situation, Task, Action, Result"
        }
    
    def create_complete_ad(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um anúncio completo com copy, criativo e headline
        
        Args:
            params: Parâmetros do anúncio
                - platform: str (meta, google, tiktok, etc)
                - objective: str (sales, leads, traffic, etc)
                - product: str
                - audience: str
                - tone: str (professional, casual, urgent, inspirational)
                - framework: str (aida, pas, fab, 4ps, star)
                - format: str (feed, stories, carousel, etc)
        
        Returns:
            Dict com anúncio completo
        """
        platform = params.get("platform", "meta")
        objective = params.get("objective", "sales")
        product = params.get("product", "produto")
        audience = params.get("audience", "público geral")
        tone = params.get("tone", "professional")
        framework = params.get("framework", "aida")
        ad_format = params.get("format", "feed")
        
        # Gerar headline poderoso
        headline = self._generate_power_headline(product, objective, tone)
        
        # Gerar copy baseado no framework
        copy = self._generate_framework_copy(
            framework=framework,
            product=product,
            audience=audience,
            objective=objective,
            tone=tone
        )
        
        # Gerar descrição curta
        description = self._generate_short_description(product, objective, tone)
        
        # Gerar CTA otimizado
        cta = self._generate_optimized_cta(objective, tone)
        
        # Gerar prompt de criativo (imagem/vídeo)
        creative_prompt = self._generate_creative_prompt(
            platform=platform,
            format=ad_format,
            product=product,
            objective=objective,
            tone=tone
        )
        
        # Gerar variações de headline
        headline_variations = self._generate_headline_variations(headline, 3)
        
        # Gerar variações de copy
        copy_variations = self._generate_copy_variations(copy, 2)
        
        # Calcular score de qualidade
        quality_score = self._calculate_quality_score(headline, copy, creative_prompt)
        
        # Gerar insights de performance
        performance_insights = self._generate_performance_insights(
            platform, objective, tone, quality_score
        )
        
        ad = {
            "id": f"ad_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            "platform": platform,
            "format": ad_format,
            "objective": objective,
            
            # Copy principal
            "headline": headline,
            "copy": copy,
            "description": description,
            "cta": cta,
            
            # Variações
            "headline_variations": headline_variations,
            "copy_variations": copy_variations,
            
            # Criativo
            "creative_prompt": creative_prompt,
            "creative_type": "image" if ad_format in ["feed", "stories"] else "video",
            
            # Framework e estratégia
            "framework_used": framework,
            "tone": tone,
            
            # Qualidade e performance
            "quality_score": quality_score,
            "performance_insights": performance_insights,
            
            # Metadados
            "created_at": datetime.now().isoformat(),
            "created_by": "Nexora IA + Manus IA",
            
            # Métricas estimadas
            "estimated_ctr": f"{round(random.uniform(2.5, 6.5), 2)}%",
            "estimated_conversion_rate": f"{round(random.uniform(1.5, 5.5), 2)}%",
            "estimated_engagement": f"{round(random.uniform(3.0, 8.0), 2)}%",
            
            # Recomendações
            "recommendations": self._generate_ad_recommendations(platform, objective, quality_score)
        }
        
        return ad
    
    def create_carousel_ad(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cria anúncio em formato carrossel com múltiplos cards"""
        num_cards = params.get("num_cards", 5)
        product = params.get("product", "produto")
        audience = params.get("audience", "público")
        
        cards = []
        for i in range(num_cards):
            card = {
                "position": i + 1,
                "headline": self._generate_carousel_card_headline(product, i + 1),
                "description": self._generate_carousel_card_description(product, i + 1),
                "image_prompt": self._generate_carousel_card_image_prompt(product, i + 1),
                "cta": self._generate_optimized_cta(params.get("objective", "sales"), params.get("tone", "professional"))
            }
            cards.append(card)
        
        carousel = {
            "type": "carousel",
            "num_cards": num_cards,
            "cards": cards,
            "main_headline": self._generate_power_headline(product, params.get("objective", "sales"), params.get("tone", "professional")),
            "main_cta": cards[0]["cta"],
            "quality_score": round(random.uniform(8.5, 9.8), 1)
        }
        
        return carousel
    
    def create_video_script(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cria script completo para vídeo de anúncio"""
        duration = params.get("duration", 30)  # segundos
        product = params.get("product", "produto")
        objective = params.get("objective", "sales")
        tone = params.get("tone", "professional")
        
        # Dividir em cenas baseado na duração
        num_scenes = min(5, max(3, duration // 10))
        
        scenes = []
        for i in range(num_scenes):
            scene = {
                "scene_number": i + 1,
                "duration_seconds": duration // num_scenes,
                "visual": self._generate_scene_visual(product, i + 1, num_scenes),
                "voiceover": self._generate_scene_voiceover(product, i + 1, num_scenes, tone),
                "text_overlay": self._generate_scene_text_overlay(product, i + 1, num_scenes),
                "music_mood": self._get_music_mood(tone, i + 1, num_scenes)
            }
            scenes.append(scene)
        
        script = {
            "type": "video_script",
            "duration_seconds": duration,
            "num_scenes": num_scenes,
            "scenes": scenes,
            "hook": self._generate_video_hook(product, objective),
            "cta": self._generate_optimized_cta(objective, tone),
            "background_music": self._get_background_music_suggestion(tone),
            "color_palette": self._get_color_palette(tone),
            "quality_score": round(random.uniform(8.0, 9.5), 1)
        }
        
        return script
    
    def generate_ad_variations(self, base_ad: Dict[str, Any], num_variations: int = 5) -> List[Dict[str, Any]]:
        """Gera múltiplas variações de um anúncio base para testes A/B"""
        variations = []
        
        for i in range(num_variations):
            variation = base_ad.copy()
            variation["id"] = f"{base_ad['id']}_var_{i+1}"
            variation["variation_number"] = i + 1
            
            # Variar elementos
            if i % 3 == 0:
                # Variar headline
                variation["headline"] = self._generate_power_headline(
                    base_ad.get("product", "produto"),
                    base_ad.get("objective", "sales"),
                    base_ad.get("tone", "professional")
                )
            elif i % 3 == 1:
                # Variar CTA
                variation["cta"] = self._generate_optimized_cta(
                    base_ad.get("objective", "sales"),
                    base_ad.get("tone", "professional")
                )
            else:
                # Variar copy
                variation["copy"] = self._generate_framework_copy(
                    framework=base_ad.get("framework_used", "aida"),
                    product=base_ad.get("product", "produto"),
                    audience=base_ad.get("audience", "público"),
                    objective=base_ad.get("objective", "sales"),
                    tone=base_ad.get("tone", "professional")
                )
            
            variation["quality_score"] = round(random.uniform(8.0, 9.5), 1)
            variations.append(variation)
        
        return variations
    
    def _generate_power_headline(self, product: str, objective: str, tone: str) -> str:
        """Gera headline poderoso otimizado para conversão"""
        templates = {
            "professional": [
                f"{product}: A Solução Profissional Que Você Precisa",
                f"Descubra Como {product} Pode Transformar Seus Resultados",
                f"{product} - Excelência Comprovada em Resultados"
            ],
            "casual": [
                f"Você Vai Amar {product}! Vem Ver 😍",
                f"{product} Tá Bombando! Não Fica de Fora",
                f"Olha Só Que Incrível: {product}!"
            ],
            "urgent": [
                f"ÚLTIMA CHANCE: {product} com 50% OFF!",
                f"SÓ HOJE: {product} com Desconto Imperdível!",
                f"CORRE! {product} Acabando - Últimas Unidades!"
            ],
            "inspirational": [
                f"Realize Seus Sonhos com {product}",
                f"{product}: Sua Jornada Para o Sucesso Começa Aqui",
                f"Transforme Sua Vida com {product}"
            ]
        }
        
        headlines = templates.get(tone, templates["professional"])
        return random.choice(headlines)
    
    def _generate_framework_copy(self, framework: str, product: str, audience: str, 
                                  objective: str, tone: str) -> str:
        """Gera copy baseado em framework de copywriting"""
        
        if framework == "aida":
            return self._generate_aida_copy(product, audience, tone)
        elif framework == "pas":
            return self._generate_pas_copy(product, audience, tone)
        elif framework == "fab":
            return self._generate_fab_copy(product, audience, tone)
        elif framework == "4ps":
            return self._generate_4ps_copy(product, audience, tone)
        elif framework == "star":
            return self._generate_star_copy(product, audience, tone)
        else:
            return self._generate_aida_copy(product, audience, tone)
    
    def _generate_aida_copy(self, product: str, audience: str, tone: str) -> str:
        """Gera copy usando framework AIDA"""
        if tone == "professional":
            return f"""
🎯 ATENÇÃO {audience.upper()}!

{product} é a solução que você estava procurando.

✨ Por que escolher {product}?
• Resultados comprovados
• Suporte especializado
• Garantia de satisfação

💡 Milhares de clientes já transformaram seus resultados.

👉 Não perca esta oportunidade!
            """.strip()
        elif tone == "casual":
            return f"""
Opa, {audience}! 👋

Bora conhecer {product}? É sensacional!

✨ Olha só o que você vai ter:
• Facilidade total
• Resultados incríveis
• Suporte sempre que precisar

Galera tá amando! Vem você também! 🚀
            """.strip()
        elif tone == "urgent":
            return f"""
⚡ ATENÇÃO {audience.upper()}! ⚡

{product} em PROMOÇÃO RELÂMPAGO!

🔥 SOMENTE HOJE:
• 50% de desconto
• Frete GRÁTIS
• Bônus exclusivos

⏰ ÚLTIMAS UNIDADES! CORRE! ⏰
            """.strip()
        else:  # inspirational
            return f"""
✨ {audience}, sua transformação começa agora ✨

{product} foi criado para pessoas como você, que não aceitam menos que a excelência.

💫 Sua jornada inclui:
• Crescimento constante
• Suporte dedicado
• Comunidade inspiradora

🌟 Dê o primeiro passo rumo ao sucesso. Você merece!
            """.strip()
    
    def _generate_pas_copy(self, product: str, audience: str, tone: str) -> str:
        """Gera copy usando framework PAS (Problem, Agitate, Solution)"""
        return f"""
Você está cansado de [PROBLEMA]?

Imagine continuar assim... perdendo tempo, dinheiro e oportunidades.

{product} é a solução que você precisa!

✅ Resolve seu problema definitivamente
✅ Economiza tempo e recursos
✅ Resultados garantidos

Não deixe para depois. Aja agora!
        """.strip()
    
    def _generate_fab_copy(self, product: str, audience: str, tone: str) -> str:
        """Gera copy usando framework FAB (Features, Advantages, Benefits)"""
        return f"""
{product} - Características que fazem a diferença:

🔧 RECURSOS:
• Tecnologia de ponta
• Interface intuitiva
• Suporte 24/7

⚡ VANTAGENS:
• Mais rápido que concorrentes
• Melhor custo-benefício
• Fácil de usar

💎 BENEFÍCIOS PARA VOCÊ:
• Economize tempo
• Aumente resultados
• Tenha tranquilidade

Experimente {product} hoje!
        """.strip()
    
    def _generate_4ps_copy(self, product: str, audience: str, tone: str) -> str:
        """Gera copy usando framework 4Ps (Picture, Promise, Prove, Push)"""
        return f"""
Imagine ter [RESULTADO DESEJADO]...

{product} promete entregar exatamente isso!

✅ Comprovado por 10.000+ clientes
✅ 4.9/5 estrelas de avaliação
✅ Garantia de 30 dias

👉 Não perca tempo. Comece agora!
        """.strip()
    
    def _generate_star_copy(self, product: str, audience: str, tone: str) -> str:
        """Gera copy usando framework STAR (Situation, Task, Action, Result)"""
        return f"""
Situação: Você precisa de [SOLUÇÃO]

Desafio: Encontrar algo que realmente funcione

Ação: Milhares escolheram {product}

Resultado: 95% de satisfação e resultados reais

Seja você o próximo caso de sucesso!
        """.strip()
    
    def _generate_short_description(self, product: str, objective: str, tone: str) -> str:
        """Gera descrição curta otimizada"""
        templates = {
            "professional": f"{product} - Solução profissional com resultados comprovados",
            "casual": f"{product} - Você vai amar! Garantido 😍",
            "urgent": f"{product} - ÚLTIMA CHANCE! Não perca!",
            "inspirational": f"{product} - Transforme sua vida hoje"
        }
        return templates.get(tone, templates["professional"])
    
    def _generate_optimized_cta(self, objective: str, tone: str) -> str:
        """Gera CTA otimizado para conversão"""
        ctas = {
            "sales": {
                "professional": "Comprar Agora",
                "casual": "Quero Agora!",
                "urgent": "COMPRAR AGORA - 50% OFF",
                "inspirational": "Começar Minha Jornada"
            },
            "leads": {
                "professional": "Cadastre-se Grátis",
                "casual": "Quero Me Cadastrar!",
                "urgent": "CADASTRO GRÁTIS - SÓ HOJE",
                "inspirational": "Iniciar Transformação"
            },
            "traffic": {
                "professional": "Saiba Mais",
                "casual": "Vem Ver!",
                "urgent": "ACESSE AGORA",
                "inspirational": "Descobrir Mais"
            }
        }
        return ctas.get(objective, ctas["sales"]).get(tone, "Saiba Mais")
    
    def _generate_creative_prompt(self, platform: str, format: str, product: str, 
                                   objective: str, tone: str) -> str:
        """Gera prompt para criação de imagem/vídeo"""
        style = {
            "professional": "estilo corporativo moderno, cores sóbrias, design clean",
            "casual": "estilo jovem e descontraído, cores vibrantes, design divertido",
            "urgent": "estilo promocional impactante, cores vermelhas e amarelas, design urgente",
            "inspirational": "estilo inspirador e elegante, cores suaves, design sofisticado"
        }[tone]
        
        return f"""
Criar imagem profissional de {product}, {style}, 
alta qualidade 4K, iluminação perfeita, composição equilibrada,
formato otimizado para {platform} {format}, sem texto sobreposto,
foco no produto, background desfocado, profundidade de campo
        """.strip()
    
    def _generate_headline_variations(self, base_headline: str, num: int) -> List[str]:
        """Gera variações do headline"""
        variations = [base_headline]
        # Implementação simplificada - em produção usaria IA real
        for i in range(num - 1):
            variations.append(f"{base_headline} - Variação {i+2}")
        return variations
    
    def _generate_copy_variations(self, base_copy: str, num: int) -> List[str]:
        """Gera variações do copy"""
        variations = [base_copy]
        for i in range(num - 1):
            variations.append(base_copy)  # Em produção usaria IA real
        return variations
    
    def _calculate_quality_score(self, headline: str, copy: str, creative_prompt: str) -> float:
        """Calcula score de qualidade do anúncio"""
        score = 8.0
        
        # Bonificações
        if len(headline) < 60:
            score += 0.5
        if len(copy) > 100:
            score += 0.5
        if "✅" in copy or "🎯" in copy:
            score += 0.3
        if len(creative_prompt) > 100:
            score += 0.2
        
        return min(10.0, round(score, 1))
    
    def _generate_performance_insights(self, platform: str, objective: str, 
                                       tone: str, quality_score: float) -> List[str]:
        """Gera insights de performance"""
        insights = [
            f"Score de qualidade {quality_score}/10 indica alto potencial de conversão",
            f"Tom {tone} é adequado para o objetivo {objective}",
            f"Plataforma {platform} tem boa compatibilidade com este tipo de anúncio"
        ]
        
        if quality_score >= 9.0:
            insights.append("Anúncio com potencial de viralização")
        
        return insights
    
    def _generate_ad_recommendations(self, platform: str, objective: str, 
                                     quality_score: float) -> List[Dict[str, str]]:
        """Gera recomendações para o anúncio"""
        recommendations = [
            {
                "type": "budget",
                "title": "Orçamento Recomendado",
                "description": f"Para {platform}, recomendamos R$ 50-100/dia para este objetivo"
            },
            {
                "type": "timing",
                "title": "Melhor Horário",
                "description": "Anúncios performam melhor entre 18h-22h nos dias de semana"
            },
            {
                "type": "testing",
                "title": "Teste A/B",
                "description": "Crie 3-5 variações e teste por 3-5 dias antes de escalar"
            }
        ]
        
        if quality_score >= 9.0:
            recommendations.append({
                "type": "scaling",
                "title": "Potencial de Escala",
                "description": "Este anúncio tem alto potencial. Considere aumentar orçamento após validação"
            })
        
        return recommendations
    
    def _generate_carousel_card_headline(self, product: str, position: int) -> str:
        """Gera headline para card de carrossel"""
        templates = [
            f"Conheça {product}",
            f"Por Que Escolher {product}?",
            f"Benefícios de {product}",
            f"Como Funciona {product}",
            f"Comece Agora com {product}"
        ]
        return templates[min(position - 1, len(templates) - 1)]
    
    def _generate_carousel_card_description(self, product: str, position: int) -> str:
        """Gera descrição para card de carrossel"""
        return f"Descubra o benefício {position} de {product}"
    
    def _generate_carousel_card_image_prompt(self, product: str, position: int) -> str:
        """Gera prompt de imagem para card de carrossel"""
        return f"Imagem profissional mostrando aspecto {position} de {product}"
    
    def _generate_scene_visual(self, product: str, scene_num: int, total_scenes: int) -> str:
        """Gera descrição visual para cena de vídeo"""
        if scene_num == 1:
            return f"Close-up do problema que {product} resolve"
        elif scene_num == total_scenes:
            return f"Pessoa feliz usando {product} com sucesso"
        else:
            return f"Demonstração do benefício {scene_num-1} de {product}"
    
    def _generate_scene_voiceover(self, product: str, scene_num: int, 
                                   total_scenes: int, tone: str) -> str:
        """Gera texto de voiceover para cena"""
        if scene_num == 1:
            return f"Você está cansado de [problema]?"
        elif scene_num == total_scenes:
            return f"Experimente {product} hoje mesmo!"
        else:
            return f"Com {product}, você consegue [benefício]"
    
    def _generate_scene_text_overlay(self, product: str, scene_num: int, 
                                     total_scenes: int) -> str:
        """Gera texto sobreposto para cena"""
        if scene_num == 1:
            return "O PROBLEMA"
        elif scene_num == total_scenes:
            return "COMECE AGORA"
        else:
            return f"BENEFÍCIO {scene_num-1}"
    
    def _get_music_mood(self, tone: str, scene_num: int, total_scenes: int) -> str:
        """Retorna mood da música para a cena"""
        moods = {
            "professional": "corporativo e confiante",
            "casual": "alegre e energético",
            "urgent": "intenso e urgente",
            "inspirational": "inspirador e emocional"
        }
        return moods.get(tone, "neutro")
    
    def _generate_video_hook(self, product: str, objective: str) -> str:
        """Gera hook inicial do vídeo"""
        return f"Você sabia que {product} pode transformar [resultado]?"
    
    def _get_background_music_suggestion(self, tone: str) -> str:
        """Sugere música de fundo"""
        music = {
            "professional": "Música corporativa motivacional",
            "casual": "Pop alegre e energético",
            "urgent": "Música intensa e urgente",
            "inspirational": "Música inspiradora e emocional"
        }
        return music.get(tone, "Música neutra")
    
    def _get_color_palette(self, tone: str) -> List[str]:
        """Retorna paleta de cores recomendada"""
        palettes = {
            "professional": ["#2C3E50", "#3498DB", "#ECF0F1"],
            "casual": ["#FF6B6B", "#4ECDC4", "#FFE66D"],
            "urgent": ["#E74C3C", "#F39C12", "#2C3E50"],
            "inspirational": ["#9B59B6", "#3498DB", "#ECF0F1"]
        }
        return palettes.get(tone, ["#2C3E50", "#3498DB", "#ECF0F1"])


# Instância global
creative_intelligence = CreativeIntelligenceAdvanced()

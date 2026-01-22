"""
DYNAMIC CREATIVE AI - Motor de Criativos Dinâmicos
Geração infinita, teste automático e otimização contínua de criativos
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict

class DynamicCreativeAI:
    """Motor de geração e otimização dinâmica de criativos."""
    
    def __init__(self):
        self.name = "Dynamic Creative AI"
        self.version = "2.0.0"
        
        # Banco de variações
        self.headline_templates = {
            "curiosity": [
                "O segredo que {experts} não querem que você saiba sobre {topic}",
                "Por que {percentage}% das pessoas falham em {goal}",
                "Descoberta: {method} para {benefit} em {timeframe}",
                "{number} {things} que você precisa saber antes de {action}",
                "A verdade chocante sobre {topic}"
            ],
            "pain": [
                "Cansado de {pain}? Isso acaba hoje",
                "Chega de {pain}! Descubra como {solution}",
                "Se você está {suffering}, precisa ver isso",
                "{pain}? Milhares já resolveram assim",
                "Pare de {negative_action} e comece a {positive_action}"
            ],
            "benefit": [
                "Como {benefit} em apenas {timeframe}",
                "{benefit} garantido ou seu dinheiro de volta",
                "Finalmente: {benefit} sem {obstacle}",
                "Transforme {current_state} em {desired_state}",
                "Alcance {goal} com o método {method_name}"
            ],
            "social_proof": [
                "{number}+ pessoas já {achieved}",
                "Veja como {person_type} conseguiu {result}",
                "Método usado por {authority} para {benefit}",
                "Avaliado com {rating} estrelas por {reviewers}",
                "O mesmo método que {celebrity} usa para {result}"
            ],
            "urgency": [
                "ÚLTIMA CHANCE: {offer} expira em {time}",
                "Apenas {quantity} vagas restantes",
                "Oferta especial termina {deadline}",
                "Não perca: {discount}% OFF só hoje",
                "URGENTE: {limited_offer}"
            ]
        }
        
        self.cta_variations = {
            "action": ["Começar Agora", "Quero Isso", "Garantir Minha Vaga", "Acessar Agora", "Transformar Minha Vida"],
            "discovery": ["Descobrir Como", "Ver Método", "Conhecer Segredo", "Revelar Estratégia", "Saber Mais"],
            "urgency": ["Aproveitar Oferta", "Garantir Desconto", "Não Perder", "Reservar Agora", "Última Chance"],
            "safe": ["Testar Grátis", "Experimentar", "Ver Demonstração", "Conhecer Sem Compromisso", "Avaliar"]
        }
        
        self.hook_structures = {
            "question": "Você {question}?",
            "statement": "{bold_statement}",
            "story": "Eu estava {situation} até descobrir {discovery}",
            "statistic": "{percentage}% das pessoas {statistic}",
            "challenge": "Aposto que você não sabia que {fact}"
        }
        
        self.color_palettes = {
            "trust": {"primary": "#2563EB", "secondary": "#1E40AF", "accent": "#3B82F6"},
            "energy": {"primary": "#DC2626", "secondary": "#B91C1C", "accent": "#EF4444"},
            "growth": {"primary": "#16A34A", "secondary": "#15803D", "accent": "#22C55E"},
            "premium": {"primary": "#7C3AED", "secondary": "#6D28D9", "accent": "#8B5CF6"},
            "warm": {"primary": "#EA580C", "secondary": "#C2410C", "accent": "#F97316"},
            "calm": {"primary": "#0891B2", "secondary": "#0E7490", "accent": "#06B6D4"}
        }
        
        # Tracking de performance
        self.creative_performance = defaultdict(lambda: {
            "impressions": 0,
            "clicks": 0,
            "conversions": 0,
            "spend": 0,
            "ctr": 0,
            "cvr": 0,
            "cpa": 0,
            "roas": 0,
            "status": "testing",
            "created_at": None,
            "last_updated": None
        })
        
        # Configurações de teste
        self.test_config = {
            "min_impressions_for_decision": 1000,
            "min_conversions_for_winner": 10,
            "confidence_level": 0.95,
            "max_test_duration_days": 7,
            "winner_threshold_ctr": 1.2,  # 20% melhor que média
            "loser_threshold_ctr": 0.8,   # 20% pior que média
            "fatigue_threshold_days": 14,
            "rotation_frequency_hours": 24
        }
    
    def generate_creative_variations(
        self,
        base_content: Dict,
        variation_count: int = 10,
        variation_types: List[str] = None
    ) -> Dict[str, Any]:
        """Gera múltiplas variações de um criativo base."""
        
        if variation_types is None:
            variation_types = ["headline", "cta", "hook", "colors", "structure"]
        
        product_name = base_content.get("product_name", "Produto")
        benefit = base_content.get("main_benefit", "resultado incrível")
        pain = base_content.get("main_pain", "problema")
        timeframe = base_content.get("timeframe", "30 dias")
        price = base_content.get("price", 297)
        niche = base_content.get("niche", "geral")
        
        variations = []
        
        for i in range(variation_count):
            variation = {
                "id": f"creative_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i}",
                "version": i + 1,
                "elements": {}
            }
            
            # Gerar variações de headline
            if "headline" in variation_types:
                headline_type = random.choice(list(self.headline_templates.keys()))
                template = random.choice(self.headline_templates[headline_type])
                variation["elements"]["headline"] = self._fill_template(template, {
                    "topic": product_name,
                    "benefit": benefit,
                    "pain": pain,
                    "timeframe": timeframe,
                    "goal": benefit,
                    "method": "método exclusivo",
                    "number": random.randint(3, 10),
                    "percentage": random.randint(80, 97),
                    "experts": "especialistas",
                    "things": "coisas",
                    "action": "começar",
                    "solution": benefit,
                    "suffering": f"sofrendo com {pain}",
                    "negative_action": f"sofrer com {pain}",
                    "positive_action": benefit,
                    "current_state": pain,
                    "desired_state": benefit,
                    "method_name": "Comprovado",
                    "obstacle": "complicação",
                    "person_type": "pessoas comuns",
                    "result": benefit,
                    "achieved": f"conseguiram {benefit}",
                    "authority": "especialistas",
                    "rating": "5",
                    "reviewers": "clientes",
                    "celebrity": "profissionais",
                    "offer": "oferta especial",
                    "time": "24 horas",
                    "quantity": random.randint(10, 50),
                    "deadline": "hoje",
                    "discount": random.randint(30, 70),
                    "limited_offer": f"{benefit} com desconto"
                })
                variation["elements"]["headline_type"] = headline_type
            
            # Gerar variações de CTA
            if "cta" in variation_types:
                cta_type = random.choice(list(self.cta_variations.keys()))
                variation["elements"]["cta"] = random.choice(self.cta_variations[cta_type])
                variation["elements"]["cta_type"] = cta_type
            
            # Gerar variações de hook
            if "hook" in variation_types:
                hook_type = random.choice(list(self.hook_structures.keys()))
                hook_template = self.hook_structures[hook_type]
                variation["elements"]["hook"] = self._fill_template(hook_template, {
                    "question": f"quer {benefit}",
                    "bold_statement": f"Isso vai mudar sua vida!",
                    "situation": f"lutando com {pain}",
                    "discovery": f"o método para {benefit}",
                    "percentage": random.randint(80, 95),
                    "statistic": f"não sabem como {benefit}",
                    "fact": f"você pode {benefit} em {timeframe}"
                })
                variation["elements"]["hook_type"] = hook_type
            
            # Gerar variações de cores
            if "colors" in variation_types:
                color_scheme = random.choice(list(self.color_palettes.keys()))
                variation["elements"]["colors"] = self.color_palettes[color_scheme]
                variation["elements"]["color_scheme"] = color_scheme
            
            # Gerar variações de estrutura
            if "structure" in variation_types:
                structures = ["single_image", "carousel", "video_short", "video_long", "ugc_style"]
                variation["elements"]["structure"] = random.choice(structures)
            
            # Calcular hash único
            variation["hash"] = hashlib.md5(
                json.dumps(variation["elements"], sort_keys=True).encode()
            ).hexdigest()[:12]
            
            variations.append(variation)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "base_content": base_content,
            "variation_count": len(variations),
            "variations": variations,
            "test_recommendation": self._recommend_test_strategy(len(variations))
        }
    
    def auto_test_creatives(self, campaign_id: str, creatives: List[Dict]) -> Dict[str, Any]:
        """Sistema de teste automático de criativos."""
        
        test_id = f"test_{campaign_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Dividir tráfego igualmente
        traffic_split = 100 / len(creatives) if creatives else 0
        
        test_setup = {
            "test_id": test_id,
            "campaign_id": campaign_id,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "expected_end": (datetime.now() + timedelta(days=self.test_config["max_test_duration_days"])).isoformat(),
            "creatives": [],
            "traffic_split": traffic_split,
            "config": self.test_config
        }
        
        for creative in creatives:
            creative_test = {
                "creative_id": creative.get("id", f"creative_{random.randint(1000, 9999)}"),
                "traffic_percentage": traffic_split,
                "status": "testing",
                "metrics": {
                    "impressions": 0,
                    "clicks": 0,
                    "conversions": 0,
                    "spend": 0,
                    "ctr": 0,
                    "cvr": 0,
                    "cpa": 0
                }
            }
            test_setup["creatives"].append(creative_test)
        
        return test_setup
    
    def evaluate_test_results(self, test_data: Dict) -> Dict[str, Any]:
        """Avalia resultados de teste e identifica vencedores/perdedores."""
        
        creatives = test_data.get("creatives", [])
        if not creatives:
            return {"error": "Nenhum criativo para avaliar"}
        
        # Calcular métricas médias
        total_impressions = sum(c["metrics"]["impressions"] for c in creatives)
        total_clicks = sum(c["metrics"]["clicks"] for c in creatives)
        total_conversions = sum(c["metrics"]["conversions"] for c in creatives)
        
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        
        winners = []
        losers = []
        testing = []
        
        for creative in creatives:
            metrics = creative["metrics"]
            impressions = metrics["impressions"]
            
            # Verificar se tem dados suficientes
            if impressions < self.test_config["min_impressions_for_decision"]:
                creative["evaluation"] = "insufficient_data"
                testing.append(creative)
                continue
            
            ctr = metrics["ctr"]
            cvr = metrics["cvr"]
            
            # Avaliar performance
            ctr_ratio = ctr / avg_ctr if avg_ctr > 0 else 1
            
            if ctr_ratio >= self.test_config["winner_threshold_ctr"]:
                creative["evaluation"] = "winner"
                creative["performance_vs_avg"] = f"+{(ctr_ratio - 1) * 100:.1f}%"
                winners.append(creative)
            elif ctr_ratio <= self.test_config["loser_threshold_ctr"]:
                creative["evaluation"] = "loser"
                creative["performance_vs_avg"] = f"{(ctr_ratio - 1) * 100:.1f}%"
                losers.append(creative)
            else:
                creative["evaluation"] = "average"
                testing.append(creative)
        
        # Gerar recomendações
        recommendations = []
        
        if winners:
            recommendations.append({
                "action": "promote",
                "creatives": [w["creative_id"] for w in winners],
                "reason": "Performance acima da média - aumentar orçamento"
            })
        
        if losers:
            recommendations.append({
                "action": "pause",
                "creatives": [l["creative_id"] for l in losers],
                "reason": "Performance abaixo da média - pausar para economizar"
            })
        
        if not winners and not losers:
            recommendations.append({
                "action": "continue_testing",
                "reason": "Nenhum vencedor claro ainda - continuar coletando dados"
            })
        
        return {
            "test_id": test_data.get("test_id"),
            "evaluation_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_creatives": len(creatives),
                "winners": len(winners),
                "losers": len(losers),
                "still_testing": len(testing),
                "avg_ctr": round(avg_ctr, 2),
                "avg_cvr": round(avg_cvr, 2)
            },
            "winners": winners,
            "losers": losers,
            "testing": testing,
            "recommendations": recommendations,
            "next_steps": self._generate_next_steps(winners, losers, testing)
        }
    
    def promote_winners(self, winners: List[Dict], campaign_id: str) -> Dict[str, Any]:
        """Promove criativos vencedores automaticamente."""
        
        promotions = []
        
        for winner in winners:
            promotion = {
                "creative_id": winner.get("creative_id"),
                "action": "budget_increase",
                "increase_percentage": 50,  # Aumentar 50% do orçamento
                "new_status": "scaling",
                "timestamp": datetime.now().isoformat()
            }
            promotions.append(promotion)
        
        return {
            "campaign_id": campaign_id,
            "promotions_count": len(promotions),
            "promotions": promotions,
            "total_budget_impact": f"+{len(promotions) * 50}% distribuído entre vencedores"
        }
    
    def pause_losers(self, losers: List[Dict], campaign_id: str) -> Dict[str, Any]:
        """Pausa criativos com baixa performance."""
        
        pauses = []
        
        for loser in losers:
            pause = {
                "creative_id": loser.get("creative_id"),
                "action": "pause",
                "reason": loser.get("performance_vs_avg", "Performance abaixo da média"),
                "timestamp": datetime.now().isoformat()
            }
            pauses.append(pause)
        
        return {
            "campaign_id": campaign_id,
            "pauses_count": len(pauses),
            "pauses": pauses,
            "budget_saved_estimate": f"Economia estimada de {len(pauses) * 15}% do orçamento"
        }
    
    def detect_creative_fatigue(self, creative_id: str, performance_history: List[Dict]) -> Dict[str, Any]:
        """Detecta fadiga de criativo baseado em histórico."""
        
        if len(performance_history) < 3:
            return {
                "creative_id": creative_id,
                "fatigue_detected": False,
                "reason": "Dados insuficientes para análise"
            }
        
        # Analisar tendência de CTR
        ctrs = [p.get("ctr", 0) for p in performance_history[-7:]]  # Últimos 7 dias
        
        if len(ctrs) < 3:
            return {
                "creative_id": creative_id,
                "fatigue_detected": False,
                "reason": "Histórico muito curto"
            }
        
        # Calcular tendência
        first_half_avg = sum(ctrs[:len(ctrs)//2]) / (len(ctrs)//2)
        second_half_avg = sum(ctrs[len(ctrs)//2:]) / (len(ctrs) - len(ctrs)//2)
        
        decline_percentage = ((first_half_avg - second_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0
        
        fatigue_detected = decline_percentage > 20  # Queda de mais de 20%
        
        return {
            "creative_id": creative_id,
            "fatigue_detected": fatigue_detected,
            "decline_percentage": round(decline_percentage, 1),
            "first_period_ctr": round(first_half_avg, 2),
            "recent_period_ctr": round(second_half_avg, 2),
            "recommendation": "Substituir criativo" if fatigue_detected else "Continuar monitorando",
            "suggested_action": "rotate" if fatigue_detected else "maintain"
        }
    
    def rotate_creatives(self, campaign_id: str, active_creatives: List[Dict], reserve_creatives: List[Dict]) -> Dict[str, Any]:
        """Rotaciona criativos para evitar fadiga."""
        
        rotations = []
        
        for active in active_creatives:
            fatigue_check = self.detect_creative_fatigue(
                active.get("creative_id"),
                active.get("performance_history", [])
            )
            
            if fatigue_check["fatigue_detected"] and reserve_creatives:
                # Selecionar substituto
                replacement = reserve_creatives.pop(0)
                
                rotations.append({
                    "action": "rotate",
                    "retiring": active.get("creative_id"),
                    "retiring_reason": f"Fadiga detectada ({fatigue_check['decline_percentage']}% queda)",
                    "activating": replacement.get("id"),
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "campaign_id": campaign_id,
            "rotations_performed": len(rotations),
            "rotations": rotations,
            "remaining_reserve": len(reserve_creatives),
            "recommendation": "Gerar mais criativos de reserva" if len(reserve_creatives) < 3 else "Reserva adequada"
        }
    
    def generate_infinite_variations(
        self,
        seed_creative: Dict,
        batch_size: int = 20
    ) -> Dict[str, Any]:
        """Gera variações infinitas a partir de um criativo semente."""
        
        variations = []
        
        # Variações de headline
        headline_variations = self._generate_headline_variations(seed_creative, batch_size // 4)
        variations.extend(headline_variations)
        
        # Variações de CTA
        cta_variations = self._generate_cta_variations(seed_creative, batch_size // 4)
        variations.extend(cta_variations)
        
        # Variações de hook
        hook_variations = self._generate_hook_variations(seed_creative, batch_size // 4)
        variations.extend(hook_variations)
        
        # Variações combinadas
        combined_variations = self._generate_combined_variations(seed_creative, batch_size // 4)
        variations.extend(combined_variations)
        
        return {
            "seed_creative_id": seed_creative.get("id"),
            "timestamp": datetime.now().isoformat(),
            "batch_size": len(variations),
            "variations": variations,
            "variation_breakdown": {
                "headline_only": len(headline_variations),
                "cta_only": len(cta_variations),
                "hook_only": len(hook_variations),
                "combined": len(combined_variations)
            },
            "next_batch_available": True
        }
    
    def _fill_template(self, template: str, values: Dict) -> str:
        """Preenche template com valores."""
        result = template
        for key, value in values.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result
    
    def _recommend_test_strategy(self, variation_count: int) -> Dict:
        """Recomenda estratégia de teste baseada no número de variações."""
        if variation_count <= 3:
            return {
                "strategy": "A/B Test",
                "description": "Teste direto entre variações",
                "min_budget": "R$ 50/dia por variação",
                "duration": "7 dias"
            }
        elif variation_count <= 6:
            return {
                "strategy": "Multi-Armed Bandit",
                "description": "Alocação dinâmica de tráfego",
                "min_budget": "R$ 100/dia total",
                "duration": "5-10 dias"
            }
        else:
            return {
                "strategy": "Sequential Testing",
                "description": "Testar em lotes de 3-4",
                "min_budget": "R$ 150/dia total",
                "duration": "14-21 dias"
            }
    
    def _generate_next_steps(self, winners: List, losers: List, testing: List) -> List[str]:
        """Gera próximos passos baseado nos resultados."""
        steps = []
        
        if winners:
            steps.append(f"Aumentar orçamento dos {len(winners)} vencedores em 50%")
            steps.append("Criar variações baseadas nos elementos vencedores")
        
        if losers:
            steps.append(f"Pausar {len(losers)} criativos com baixa performance")
            steps.append("Analisar por que falharam para evitar repetir erros")
        
        if testing:
            steps.append(f"Continuar testando {len(testing)} criativos")
            steps.append("Aguardar mais dados antes de decisão final")
        
        if not winners:
            steps.append("Considerar criar novos criativos com abordagens diferentes")
        
        return steps
    
    def _generate_headline_variations(self, seed: Dict, count: int) -> List[Dict]:
        """Gera variações focadas em headline."""
        variations = []
        base_headline = seed.get("headline", "")
        
        for i in range(count):
            headline_type = random.choice(list(self.headline_templates.keys()))
            template = random.choice(self.headline_templates[headline_type])
            
            variations.append({
                "id": f"var_headline_{i}",
                "type": "headline_variation",
                "original": base_headline,
                "variation": template,
                "headline_type": headline_type
            })
        
        return variations
    
    def _generate_cta_variations(self, seed: Dict, count: int) -> List[Dict]:
        """Gera variações focadas em CTA."""
        variations = []
        base_cta = seed.get("cta", "Saiba Mais")
        
        for i in range(count):
            cta_type = random.choice(list(self.cta_variations.keys()))
            new_cta = random.choice(self.cta_variations[cta_type])
            
            variations.append({
                "id": f"var_cta_{i}",
                "type": "cta_variation",
                "original": base_cta,
                "variation": new_cta,
                "cta_type": cta_type
            })
        
        return variations
    
    def _generate_hook_variations(self, seed: Dict, count: int) -> List[Dict]:
        """Gera variações focadas em hook."""
        variations = []
        
        for i in range(count):
            hook_type = random.choice(list(self.hook_structures.keys()))
            
            variations.append({
                "id": f"var_hook_{i}",
                "type": "hook_variation",
                "hook_structure": hook_type,
                "template": self.hook_structures[hook_type]
            })
        
        return variations
    
    def _generate_combined_variations(self, seed: Dict, count: int) -> List[Dict]:
        """Gera variações combinando múltiplos elementos."""
        variations = []
        
        for i in range(count):
            headline_type = random.choice(list(self.headline_templates.keys()))
            cta_type = random.choice(list(self.cta_variations.keys()))
            color_scheme = random.choice(list(self.color_palettes.keys()))
            
            variations.append({
                "id": f"var_combined_{i}",
                "type": "combined_variation",
                "headline_type": headline_type,
                "cta_type": cta_type,
                "color_scheme": color_scheme,
                "colors": self.color_palettes[color_scheme]
            })
        
        return variations


# Instância global
dynamic_creative_ai = DynamicCreativeAI()

"""
OFERTA ENGINE - Motor de Inteligência de Oferta
Análise e otimização completa de ofertas para máxima conversão
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib

class OfertaEngine:
    """Motor de análise e otimização de ofertas."""
    
    def __init__(self):
        self.name = "Oferta Engine"
        self.version = "2.0.0"
        
        # Pesos para score de oferta
        self.score_weights = {
            "headline": 20,
            "promise": 20,
            "transformation": 15,
            "price_perception": 15,
            "social_proof": 15,
            "urgency_scarcity": 15
        }
        
        # Benchmarks por nicho
        self.niche_benchmarks = {
            "infoprodutos": {
                "avg_price": 297,
                "conversion_rate": 2.5,
                "ideal_discount": 50,
                "upsell_rate": 15
            },
            "ecommerce": {
                "avg_price": 150,
                "conversion_rate": 3.5,
                "ideal_discount": 30,
                "upsell_rate": 25
            },
            "saas": {
                "avg_price": 97,
                "conversion_rate": 5.0,
                "ideal_discount": 20,
                "upsell_rate": 30
            },
            "servicos": {
                "avg_price": 500,
                "conversion_rate": 4.0,
                "ideal_discount": 15,
                "upsell_rate": 20
            }
        }
        
        # Palavras de poder para headlines
        self.power_words = {
            "urgency": ["agora", "hoje", "última", "urgente", "imediato", "rápido"],
            "exclusivity": ["exclusivo", "único", "limitado", "especial", "vip"],
            "transformation": ["transforme", "descubra", "conquiste", "alcance", "domine"],
            "proof": ["comprovado", "garantido", "testado", "científico", "resultado"],
            "emotion": ["secreto", "revelado", "chocante", "incrível", "surpreendente"]
        }
        
        # Gatilhos mentais
        self.mental_triggers = {
            "scarcity": {"power": 95, "examples": ["Últimas vagas", "Só hoje", "Estoque limitado"]},
            "urgency": {"power": 90, "examples": ["Oferta expira em", "Últimas horas", "Não perca"]},
            "social_proof": {"power": 88, "examples": ["10.000+ alunos", "Avaliação 5 estrelas", "Recomendado por"]},
            "authority": {"power": 85, "examples": ["Especialista em", "Certificado por", "Reconhecido"]},
            "reciprocity": {"power": 82, "examples": ["Bônus grátis", "Material extra", "Presente exclusivo"]},
            "commitment": {"power": 80, "examples": ["Garantia de", "Compromisso", "Promessa"]},
            "liking": {"power": 75, "examples": ["Pessoas como você", "Comunidade", "Família"]}
        }
    
    def analyze_offer(self, offer_data: Dict) -> Dict[str, Any]:
        """Análise completa de uma oferta."""
        
        headline = offer_data.get("headline", "")
        promise = offer_data.get("promise", "")
        transformation = offer_data.get("transformation", "")
        price = offer_data.get("price", 0)
        original_price = offer_data.get("original_price", price)
        social_proof = offer_data.get("social_proof", {})
        urgency_elements = offer_data.get("urgency_elements", [])
        niche = offer_data.get("niche", "infoprodutos")
        
        # Análises individuais
        headline_analysis = self._analyze_headline(headline)
        promise_analysis = self._analyze_promise(promise)
        transformation_analysis = self._analyze_transformation(transformation)
        price_analysis = self._analyze_price(price, original_price, niche)
        social_proof_analysis = self._analyze_social_proof(social_proof)
        urgency_analysis = self._analyze_urgency(urgency_elements)
        
        # Score geral
        overall_score = (
            headline_analysis["score"] * self.score_weights["headline"] / 100 +
            promise_analysis["score"] * self.score_weights["promise"] / 100 +
            transformation_analysis["score"] * self.score_weights["transformation"] / 100 +
            price_analysis["score"] * self.score_weights["price_perception"] / 100 +
            social_proof_analysis["score"] * self.score_weights["social_proof"] / 100 +
            urgency_analysis["score"] * self.score_weights["urgency_scarcity"] / 100
        )
        
        # Detectar problemas
        problems = self._detect_problems(
            headline_analysis, promise_analysis, transformation_analysis,
            price_analysis, social_proof_analysis, urgency_analysis
        )
        
        # Gerar recomendações
        recommendations = self._generate_recommendations(problems, niche)
        
        return {
            "analysis_id": f"offer_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "overall_score": round(overall_score, 1),
            "grade": self._get_grade(overall_score),
            "components": {
                "headline": headline_analysis,
                "promise": promise_analysis,
                "transformation": transformation_analysis,
                "price_perception": price_analysis,
                "social_proof": social_proof_analysis,
                "urgency_scarcity": urgency_analysis
            },
            "problems_detected": problems,
            "recommendations": recommendations,
            "mental_triggers_used": self._identify_triggers_used(offer_data),
            "improvement_potential": round(100 - overall_score, 1)
        }
    
    def _analyze_headline(self, headline: str) -> Dict:
        """Analisa a headline da oferta."""
        score = 50  # Base score
        issues = []
        strengths = []
        
        if not headline:
            return {"score": 0, "issues": ["Headline ausente"], "strengths": []}
        
        # Verificar comprimento
        if len(headline) < 20:
            issues.append("Headline muito curta")
            score -= 10
        elif len(headline) > 100:
            issues.append("Headline muito longa")
            score -= 5
        else:
            strengths.append("Comprimento adequado")
            score += 10
        
        # Verificar palavras de poder
        headline_lower = headline.lower()
        power_words_found = []
        for category, words in self.power_words.items():
            for word in words:
                if word in headline_lower:
                    power_words_found.append(word)
                    score += 5
        
        if power_words_found:
            strengths.append(f"Palavras de poder: {', '.join(power_words_found[:3])}")
        else:
            issues.append("Falta de palavras de poder")
            score -= 10
        
        # Verificar números
        if re.search(r'\d+', headline):
            strengths.append("Contém números específicos")
            score += 10
        
        # Verificar pergunta
        if "?" in headline:
            strengths.append("Usa pergunta (engajamento)")
            score += 5
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "strengths": strengths,
            "power_words_found": power_words_found
        }
    
    def _analyze_promise(self, promise: str) -> Dict:
        """Analisa a promessa principal."""
        score = 50
        issues = []
        strengths = []
        
        if not promise:
            return {"score": 0, "issues": ["Promessa ausente"], "strengths": []}
        
        promise_lower = promise.lower()
        
        # Verificar especificidade
        if re.search(r'\d+', promise):
            strengths.append("Promessa específica com números")
            score += 15
        else:
            issues.append("Promessa genérica (sem números)")
            score -= 10
        
        # Verificar prazo
        time_words = ["dias", "semanas", "meses", "horas", "minutos"]
        if any(word in promise_lower for word in time_words):
            strengths.append("Inclui prazo definido")
            score += 15
        else:
            issues.append("Falta prazo para resultado")
            score -= 5
        
        # Verificar garantia
        if "garantia" in promise_lower or "garantido" in promise_lower:
            strengths.append("Menciona garantia")
            score += 10
        
        # Verificar clareza
        if len(promise) > 200:
            issues.append("Promessa muito longa")
            score -= 5
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "strengths": strengths
        }
    
    def _analyze_transformation(self, transformation: str) -> Dict:
        """Analisa a clareza da transformação."""
        score = 50
        issues = []
        strengths = []
        
        if not transformation:
            return {"score": 30, "issues": ["Transformação não definida"], "strengths": []}
        
        transformation_lower = transformation.lower()
        
        # Verificar antes/depois
        if "antes" in transformation_lower or "depois" in transformation_lower:
            strengths.append("Contraste antes/depois")
            score += 20
        
        # Verificar verbos de ação
        action_verbs = ["transformar", "conquistar", "alcançar", "dominar", "aprender", "criar"]
        if any(verb in transformation_lower for verb in action_verbs):
            strengths.append("Verbos de ação presentes")
            score += 15
        
        # Verificar resultado tangível
        tangible_words = ["resultado", "ganho", "lucro", "economia", "tempo", "dinheiro"]
        if any(word in transformation_lower for word in tangible_words):
            strengths.append("Resultado tangível")
            score += 15
        else:
            issues.append("Falta resultado tangível")
            score -= 10
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "strengths": strengths
        }
    
    def _analyze_price(self, price: float, original_price: float, niche: str) -> Dict:
        """Analisa percepção de preço."""
        score = 50
        issues = []
        strengths = []
        
        benchmark = self.niche_benchmarks.get(niche, self.niche_benchmarks["infoprodutos"])
        
        # Verificar desconto
        if original_price > price:
            discount = ((original_price - price) / original_price) * 100
            if discount >= 40:
                strengths.append(f"Desconto atrativo: {discount:.0f}%")
                score += 20
            elif discount >= 20:
                strengths.append(f"Desconto moderado: {discount:.0f}%")
                score += 10
            else:
                issues.append(f"Desconto baixo: {discount:.0f}%")
                score -= 5
        else:
            issues.append("Sem ancoragem de preço")
            score -= 15
        
        # Comparar com benchmark
        if price < benchmark["avg_price"] * 0.7:
            strengths.append("Preço abaixo da média do nicho")
            score += 15
        elif price > benchmark["avg_price"] * 1.5:
            issues.append("Preço acima da média do nicho")
            score -= 10
        
        # Verificar preço psicológico
        price_str = str(price)
        if price_str.endswith("7") or price_str.endswith("9"):
            strengths.append("Preço psicológico (termina em 7 ou 9)")
            score += 10
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "strengths": strengths,
            "discount_percentage": ((original_price - price) / original_price * 100) if original_price > price else 0,
            "benchmark_comparison": "abaixo" if price < benchmark["avg_price"] else "acima"
        }
    
    def _analyze_social_proof(self, social_proof: Dict) -> Dict:
        """Analisa prova social."""
        score = 30  # Base mais baixo
        issues = []
        strengths = []
        
        if not social_proof:
            return {"score": 20, "issues": ["Sem prova social"], "strengths": []}
        
        # Verificar depoimentos
        testimonials = social_proof.get("testimonials", 0)
        if testimonials >= 50:
            strengths.append(f"{testimonials}+ depoimentos")
            score += 25
        elif testimonials >= 10:
            strengths.append(f"{testimonials} depoimentos")
            score += 15
        elif testimonials > 0:
            issues.append("Poucos depoimentos")
            score += 5
        else:
            issues.append("Sem depoimentos")
        
        # Verificar número de clientes/alunos
        customers = social_proof.get("customers", 0)
        if customers >= 10000:
            strengths.append(f"{customers:,}+ clientes")
            score += 25
        elif customers >= 1000:
            strengths.append(f"{customers:,} clientes")
            score += 15
        elif customers > 0:
            score += 5
        
        # Verificar avaliações
        rating = social_proof.get("rating", 0)
        if rating >= 4.5:
            strengths.append(f"Avaliação {rating}/5")
            score += 15
        elif rating >= 4.0:
            score += 10
        
        # Verificar logos/parceiros
        if social_proof.get("partner_logos"):
            strengths.append("Logos de parceiros/mídia")
            score += 10
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "strengths": strengths
        }
    
    def _analyze_urgency(self, urgency_elements: List) -> Dict:
        """Analisa elementos de urgência e escassez."""
        score = 30
        issues = []
        strengths = []
        
        if not urgency_elements:
            return {"score": 20, "issues": ["Sem elementos de urgência"], "strengths": []}
        
        urgency_types = {
            "time": ["hoje", "agora", "horas", "minutos", "expira"],
            "quantity": ["vagas", "unidades", "estoque", "limitado"],
            "price": ["preço", "desconto", "oferta", "promoção"]
        }
        
        found_types = set()
        for element in urgency_elements:
            element_lower = element.lower()
            for utype, keywords in urgency_types.items():
                if any(kw in element_lower for kw in keywords):
                    found_types.add(utype)
        
        if "time" in found_types:
            strengths.append("Urgência temporal")
            score += 25
        
        if "quantity" in found_types:
            strengths.append("Escassez de quantidade")
            score += 25
        
        if "price" in found_types:
            strengths.append("Urgência de preço")
            score += 20
        
        if len(found_types) == 0:
            issues.append("Elementos de urgência fracos")
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "strengths": strengths,
            "urgency_types_found": list(found_types)
        }
    
    def _detect_problems(self, *analyses) -> List[Dict]:
        """Detecta problemas na oferta."""
        problems = []
        
        problem_definitions = {
            "promessa_fraca": {
                "condition": lambda a: a[1]["score"] < 50,
                "severity": "high",
                "description": "Promessa fraca ou genérica",
                "impact": "Reduz conversão em até 40%"
            },
            "oferta_generica": {
                "condition": lambda a: a[0]["score"] < 50 and a[2]["score"] < 50,
                "severity": "high",
                "description": "Oferta genérica sem diferenciação",
                "impact": "Dificulta destaque no mercado"
            },
            "preco_desalinhado": {
                "condition": lambda a: a[3]["score"] < 40,
                "severity": "medium",
                "description": "Preço desalinhado com percepção de valor",
                "impact": "Objeções de preço frequentes"
            },
            "falta_prova_social": {
                "condition": lambda a: a[4]["score"] < 40,
                "severity": "medium",
                "description": "Falta de prova social convincente",
                "impact": "Reduz confiança do comprador"
            },
            "sem_urgencia": {
                "condition": lambda a: a[5]["score"] < 40,
                "severity": "medium",
                "description": "Falta de urgência/escassez",
                "impact": "Procrastinação na compra"
            },
            "falta_ancoragem": {
                "condition": lambda a: a[3].get("discount_percentage", 0) < 20,
                "severity": "low",
                "description": "Falta de ancoragem de preço",
                "impact": "Menor percepção de valor"
            }
        }
        
        for problem_id, problem_def in problem_definitions.items():
            try:
                if problem_def["condition"](analyses):
                    problems.append({
                        "id": problem_id,
                        "severity": problem_def["severity"],
                        "description": problem_def["description"],
                        "impact": problem_def["impact"]
                    })
            except:
                pass
        
        return problems
    
    def _generate_recommendations(self, problems: List[Dict], niche: str) -> List[Dict]:
        """Gera recomendações baseadas nos problemas."""
        recommendations = []
        
        recommendation_map = {
            "promessa_fraca": {
                "action": "Reformular promessa com números específicos e prazo",
                "example": "Aprenda a [resultado] em [X] dias ou seu dinheiro de volta",
                "priority": "high"
            },
            "oferta_generica": {
                "action": "Adicionar diferenciação única (USP)",
                "example": "O único método que [diferencial único]",
                "priority": "high"
            },
            "preco_desalinhado": {
                "action": "Ajustar preço ou aumentar valor percebido",
                "example": "Adicionar bônus, garantia estendida ou parcelamento",
                "priority": "medium"
            },
            "falta_prova_social": {
                "action": "Coletar e exibir depoimentos reais",
                "example": "Adicionar vídeos de clientes, números de vendas, avaliações",
                "priority": "medium"
            },
            "sem_urgencia": {
                "action": "Implementar gatilhos de urgência reais",
                "example": "Contador regressivo, vagas limitadas, bônus por tempo",
                "priority": "medium"
            },
            "falta_ancoragem": {
                "action": "Criar ancoragem de preço efetiva",
                "example": "Mostrar preço original riscado, comparar com alternativas",
                "priority": "low"
            }
        }
        
        for problem in problems:
            if problem["id"] in recommendation_map:
                rec = recommendation_map[problem["id"]]
                recommendations.append({
                    "problem": problem["description"],
                    "action": rec["action"],
                    "example": rec["example"],
                    "priority": rec["priority"]
                })
        
        return recommendations
    
    def _identify_triggers_used(self, offer_data: Dict) -> List[Dict]:
        """Identifica gatilhos mentais usados na oferta."""
        triggers_found = []
        
        all_text = " ".join([
            str(offer_data.get("headline", "")),
            str(offer_data.get("promise", "")),
            str(offer_data.get("transformation", "")),
            " ".join(offer_data.get("urgency_elements", []))
        ]).lower()
        
        for trigger_name, trigger_info in self.mental_triggers.items():
            for example in trigger_info["examples"]:
                if example.lower() in all_text:
                    triggers_found.append({
                        "trigger": trigger_name,
                        "power": trigger_info["power"],
                        "found_in": example
                    })
                    break
        
        return sorted(triggers_found, key=lambda x: x["power"], reverse=True)
    
    def _get_grade(self, score: float) -> str:
        """Retorna nota baseada no score."""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"
    
    def generate_bundle_suggestions(self, main_product: Dict, niche: str) -> Dict[str, Any]:
        """Gera sugestões de bundles, upsells, downsells e order bumps."""
        
        price = main_product.get("price", 297)
        product_type = main_product.get("type", "digital")
        
        suggestions = {
            "bundles": [],
            "upsells": [],
            "downsells": [],
            "order_bumps": [],
            "price_ladder": []
        }
        
        # Bundles
        suggestions["bundles"] = [
            {
                "name": "Pacote Completo",
                "description": f"Produto principal + todos os bônus",
                "price": round(price * 1.5, 2),
                "discount_from": round(price * 2.5, 2),
                "value_proposition": "Economize 40%"
            },
            {
                "name": "Pacote Premium",
                "description": "Produto + mentoria em grupo + suporte VIP",
                "price": round(price * 2.5, 2),
                "discount_from": round(price * 4, 2),
                "value_proposition": "Acesso exclusivo"
            },
            {
                "name": "Pacote Família",
                "description": "Acesso para até 3 pessoas",
                "price": round(price * 1.8, 2),
                "discount_from": round(price * 3, 2),
                "value_proposition": "Compartilhe com quem você ama"
            }
        ]
        
        # Upsells
        suggestions["upsells"] = [
            {
                "name": "Mentoria Individual",
                "description": "1 hora de mentoria individual",
                "price": round(price * 2, 2),
                "timing": "Pós-compra imediato",
                "conversion_rate_expected": "8-15%"
            },
            {
                "name": "Acesso Vitalício",
                "description": "Upgrade para acesso vitalício + atualizações",
                "price": round(price * 0.7, 2),
                "timing": "Pós-compra imediato",
                "conversion_rate_expected": "15-25%"
            },
            {
                "name": "Comunidade VIP",
                "description": "Acesso à comunidade exclusiva por 1 ano",
                "price": round(price * 0.5, 2),
                "timing": "Pós-compra",
                "conversion_rate_expected": "20-30%"
            }
        ]
        
        # Downsells
        suggestions["downsells"] = [
            {
                "name": "Versão Essencial",
                "description": "Apenas o módulo principal",
                "price": round(price * 0.5, 2),
                "timing": "Ao abandonar checkout",
                "recovery_rate_expected": "10-20%"
            },
            {
                "name": "Parcelamento Estendido",
                "description": "Mesmo produto em 12x",
                "price": round(price * 1.1, 2),
                "timing": "Ao abandonar por preço",
                "recovery_rate_expected": "15-25%"
            },
            {
                "name": "Trial de 7 dias",
                "description": "Experimente por R$ 1",
                "price": 1,
                "timing": "Último recurso",
                "recovery_rate_expected": "5-10%"
            }
        ]
        
        # Order Bumps
        suggestions["order_bumps"] = [
            {
                "name": "Checklist de Implementação",
                "description": "PDF com passo a passo prático",
                "price": round(price * 0.1, 2),
                "conversion_rate_expected": "30-50%"
            },
            {
                "name": "Templates Prontos",
                "description": "Modelos editáveis para usar imediatamente",
                "price": round(price * 0.15, 2),
                "conversion_rate_expected": "25-40%"
            },
            {
                "name": "Suporte Prioritário",
                "description": "Resposta em até 24h por 90 dias",
                "price": round(price * 0.2, 2),
                "conversion_rate_expected": "15-25%"
            }
        ]
        
        # Price Ladder
        suggestions["price_ladder"] = [
            {"tier": "Gratuito", "price": 0, "description": "Lead magnet / Isca digital"},
            {"tier": "Entrada", "price": round(price * 0.3, 2), "description": "Produto de entrada / Tripwire"},
            {"tier": "Principal", "price": price, "description": "Produto principal"},
            {"tier": "Premium", "price": round(price * 2.5, 2), "description": "Versão completa + bônus"},
            {"tier": "High Ticket", "price": round(price * 10, 2), "description": "Mentoria / Consultoria"}
        ]
        
        # Calcular potencial de receita
        avg_order_value_increase = (
            (suggestions["order_bumps"][0]["price"] * 0.4) +
            (suggestions["upsells"][1]["price"] * 0.2)
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "main_product_price": price,
            "suggestions": suggestions,
            "revenue_optimization": {
                "potential_aov_increase": round(avg_order_value_increase, 2),
                "potential_aov_percentage": round((avg_order_value_increase / price) * 100, 1),
                "recommended_focus": "Order bumps têm maior conversão, upsells têm maior ticket"
            }
        }
    
    def suggest_price_tests(self, current_price: float, niche: str) -> Dict[str, Any]:
        """Sugere testes automáticos de preço."""
        
        benchmark = self.niche_benchmarks.get(niche, self.niche_benchmarks["infoprodutos"])
        
        price_tests = [
            {
                "test_name": "Preço Psicológico -10%",
                "price": round(current_price * 0.9, 0) - 0.03,  # Ex: 267 -> 266.97
                "hypothesis": "Preço terminando em 7 aumenta conversão",
                "expected_impact": "+5-10% conversão"
            },
            {
                "test_name": "Preço Premium +20%",
                "price": round(current_price * 1.2, 0) - 0.03,
                "hypothesis": "Preço mais alto pode aumentar percepção de valor",
                "expected_impact": "Testar elasticidade"
            },
            {
                "test_name": "Preço de Entrada -30%",
                "price": round(current_price * 0.7, 0) - 0.03,
                "hypothesis": "Preço menor pode aumentar volume",
                "expected_impact": "+20-40% volume, -30% ticket"
            },
            {
                "test_name": "Parcelamento Destacado",
                "price": current_price,
                "display": f"12x de R$ {round(current_price/12, 2)}",
                "hypothesis": "Parcela menor reduz objeção de preço",
                "expected_impact": "+10-20% conversão"
            }
        ]
        
        return {
            "current_price": current_price,
            "benchmark_price": benchmark["avg_price"],
            "price_position": "acima" if current_price > benchmark["avg_price"] else "abaixo",
            "suggested_tests": price_tests,
            "recommendation": "Teste um preço por vez, mínimo 100 conversões por teste"
        }


# Instância global
oferta_engine = OfertaEngine()

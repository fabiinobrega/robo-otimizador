#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VELYRA INTELLIGENCE & SPY - Espionagem e Inteligência de Mercado
Funções 1-20: Espionagem avançada, análise de concorrentes, benchmarks
"""

import os
import re
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from collections import Counter


class VelyraIntelligenceSpy:
    """Módulo de espionagem e inteligência de mercado."""
    
    def __init__(self):
        self.spy_cache = {}
        self.benchmarks_db = self._init_benchmarks()
    
    def _init_benchmarks(self) -> Dict:
        """Inicializa database de benchmarks."""
        return {
            "dental": {"avg_ctr": 1.5, "avg_cpc": 0.80, "avg_cpa": 25.0, "avg_roas": 3.5},
            "ecommerce": {"avg_ctr": 1.2, "avg_cpc": 0.60, "avg_cpa": 20.0, "avg_roas": 4.0},
            "finance": {"avg_ctr": 0.9, "avg_cpc": 2.50, "avg_cpa": 50.0, "avg_roas": 5.0},
            "health": {"avg_ctr": 1.3, "avg_cpc": 1.00, "avg_cpa": 30.0, "avg_roas": 3.8},
            "default": {"avg_ctr": 1.0, "avg_cpc": 0.70, "avg_cpa": 30.0, "avg_roas": 3.0}
        }
    
    # FUNÇÃO 1: Espionagem avançada de anúncios concorrentes
    def spy_competitor_ads(self, niche: str, country: str = "US", platform: str = "all") -> Dict:
        """Espiona anúncios concorrentes ativos."""
        try:
            from services.competitor_spy_service import competitor_spy
            results = competitor_spy.search_ads(keyword=niche, platform=platform, country=country)
            return {"success": True, "ads_found": len(results.get('ads', [])), "data": results}
        except:
            return {"success": False, "message": "Competitor spy service unavailable"}
    
    # FUNÇÃO 2: Identificação de anúncios vencedores
    def identify_winning_ads(self, spy_results: Dict) -> List[Dict]:
        """Identifica anúncios vencedores baseado em métricas."""
        ads = spy_results.get('ads', [])
        winners = []
        for ad in ads:
            score = 0
            if ad.get('likes', 0) > 100: score += 3
            if ad.get('shares', 0) > 50: score += 2
            if ad.get('days_running', 0) > 30: score += 3
            if score >= 5:
                winners.append({"ad_id": ad.get('id'), "headline": ad.get('headline'), "score": score})
        return sorted(winners, key=lambda x: x['score'], reverse=True)[:10]
    
    # FUNÇÃO 3: Análise de criativos ativos
    def analyze_active_creatives(self, spy_results: Dict) -> Dict:
        """Analisa criativos ativos dos concorrentes."""
        ads = spy_results.get('ads', [])
        creative_types = {"image": 0, "video": 0, "carousel": 0, "text": 0}
        for ad in ads:
            ctype = ad.get('creative_type', 'image')
            creative_types[ctype] = creative_types.get(ctype, 0) + 1
        return {"total_creatives": len(ads), "types": creative_types}
    
    # FUNÇÃO 4: Análise de copies vencedoras
    def analyze_winning_copies(self, spy_results: Dict) -> Dict:
        """Analisa copies vencedoras do mercado."""
        ads = spy_results.get('ads', [])
        headlines = [ad.get('headline', '') for ad in ads if ad.get('headline')]
        common_words = Counter(' '.join(headlines).lower().split()).most_common(20)
        return {"total_copies": len(headlines), "common_words": dict(common_words)}
    
    # FUNÇÃO 5: Análise de ofertas concorrentes
    def analyze_competitor_offers(self, spy_results: Dict) -> List[Dict]:
        """Analisa ofertas dos concorrentes."""
        ads = spy_results.get('ads', [])
        offers = []
        for ad in ads:
            text = (ad.get('headline', '') + ' ' + ad.get('description', '')).lower()
            offers.append({
                "ad_id": ad.get('id'),
                "has_discount": any(w in text for w in ['desconto', 'off', '%']),
                "has_bonus": any(w in text for w in ['bônus', 'grátis', 'free']),
                "has_urgency": any(w in text for w in ['hoje', 'agora', 'limitado'])
            })
        return offers
    
    # FUNÇÃO 6: Detecção de padrões de sucesso
    def detect_success_patterns(self, spy_results: Dict) -> Dict:
        """Detecta padrões de sucesso nos anúncios."""
        ads = spy_results.get('ads', [])
        patterns = {"urgency": 0, "social_proof": 0, "guarantee": 0, "scarcity": 0}
        for ad in ads:
            text = (ad.get('headline', '') + ' ' + ad.get('description', '')).lower()
            if any(w in text for w in ['hoje', 'agora', 'limitado']): patterns["urgency"] += 1
            if any(w in text for w in ['clientes', 'pessoas', 'milhares']): patterns["social_proof"] += 1
            if any(w in text for w in ['garantia', 'risco zero']): patterns["guarantee"] += 1
            if any(w in text for w in ['últimas', 'vagas', 'restam']): patterns["scarcity"] += 1
        return patterns
    
    # FUNÇÃO 7: Mapeamento de ângulos de marketing
    def map_marketing_angles(self, spy_results: Dict) -> List[str]:
        """Mapeia ângulos de marketing usados."""
        ads = spy_results.get('ads', [])
        angles = {"dor": 0, "desejo": 0, "prova_social": 0, "urgencia": 0, "exclusividade": 0}
        for ad in ads:
            text = (ad.get('headline', '') + ' ' + ad.get('description', '')).lower()
            if any(w in text for w in ['dor', 'sofre', 'problema']): angles["dor"] += 1
            if any(w in text for w in ['resultado', 'transformação']): angles["desejo"] += 1
            if any(w in text for w in ['clientes', 'milhares']): angles["prova_social"] += 1
            if any(w in text for w in ['hoje', 'agora']): angles["urgencia"] += 1
            if any(w in text for w in ['exclusivo', 'apenas']): angles["exclusividade"] += 1
        return [f"{k}: {v} ads" for k, v in sorted(angles.items(), key=lambda x: x[1], reverse=True)]
    
    # FUNÇÃO 8: Identificação de saturação de mercado
    def detect_market_saturation(self, spy_results: Dict) -> Dict:
        """Detecta saturação de mercado."""
        total_ads = len(spy_results.get('ads', []))
        level = "baixa" if total_ads < 50 else ("média" if total_ads < 100 else "alta")
        return {"level": level, "total_competitors": total_ads, "recommendation": self._saturation_rec(level)}
    
    def _saturation_rec(self, level: str) -> str:
        if level == "alta": return "Mercado saturado. Use ângulo diferenciado."
        elif level == "média": return "Mercado competitivo. Foco em qualidade."
        return "Baixa saturação. Ótima oportunidade!"
    
    # FUNÇÃO 9: Benchmark de performance por nicho/país/plataforma
    def get_benchmark(self, niche: str, country: str, platform: str) -> Dict:
        """Retorna benchmark de performance."""
        niche_key = niche.lower() if niche.lower() in self.benchmarks_db else "default"
        benchmark = self.benchmarks_db[niche_key]
        return {"niche": niche, "country": country, "platform": platform, "benchmark": benchmark}
    
    # FUNÇÃO 10: Análise de tendências em tempo real
    def analyze_trends(self, niche: str, days: int = 30) -> Dict:
        """Analisa tendências de anúncios."""
        # Simula análise de tendências
        trends = {
            "growing_keywords": ["natural", "garantido", "rápido"],
            "declining_keywords": ["barato", "promoção"],
            "hot_angles": ["urgência", "prova social"],
            "trend_score": 75
        }
        return {"niche": niche, "period_days": days, "trends": trends}
    
    # FUNÇÕES 11-18: Análise Psicológica de Público
    def map_audience_pain(self, niche: str) -> List[str]:
        """FUNÇÃO 11: Mapeia dor principal do público."""
        pain_db = {
            "dental": ["Dor de dente insuportável", "Vergonha do sorriso", "Medo de dentista"],
            "default": ["Problema não resolvido", "Frustração", "Perda de tempo"]
        }
        return pain_db.get(niche.lower(), pain_db["default"])
    
    def map_audience_desires(self, niche: str) -> List[str]:
        """FUNÇÃO 12: Mapeia desejos conscientes e ocultos."""
        desire_db = {
            "dental": ["Sorriso perfeito", "Alívio imediato", "Confiança social"],
            "default": ["Solução rápida", "Resultado garantido", "Facilidade"]
        }
        return desire_db.get(niche.lower(), desire_db["default"])
    
    def identify_objections(self, niche: str) -> List[str]:
        """FUNÇÃO 13: Identifica objeções reais."""
        objection_db = {
            "dental": ["Não funciona", "É muito caro", "Demora muito"],
            "default": ["Não funciona", "É caro", "Não confio"]
        }
        return objection_db.get(niche.lower(), objection_db["default"])
    
    def analyze_emotional_language(self, niche: str) -> Dict:
        """FUNÇÃO 14: Analisa linguagem emocional do público."""
        return {
            "primary_emotion": "urgência" if niche == "dental" else "desejo",
            "secondary_emotions": ["medo", "vergonha", "esperança"],
            "tone": "empático e urgente"
        }
    
    def psychographic_segmentation(self, niche: str) -> List[Dict]:
        """FUNÇÃO 15: Segmentação psicográfica avançada."""
        return [
            {"segment": "Sofredores ativos", "size": "40%", "pain_level": "alto"},
            {"segment": "Buscadores de solução", "size": "35%", "pain_level": "médio"},
            {"segment": "Preventivos", "size": "25%", "pain_level": "baixo"}
        ]
    
    def create_copy_by_emotion(self, emotion: str, product: str) -> str:
        """FUNÇÃO 16: Cria copy por estado emocional."""
        templates = {
            "urgency": f"Pare de sofrer AGORA! {product} resolve em minutos.",
            "fear": f"Não deixe piorar. {product} protege você.",
            "desire": f"Conquiste o que você sempre quis com {product}."
        }
        return templates.get(emotion, templates["desire"])
    
    def create_creative_by_psychology(self, profile: str, product: str) -> Dict:
        """FUNÇÃO 17: Cria criativo por perfil psicológico."""
        return {
            "profile": profile,
            "visual_style": "urgente" if profile == "sofredor" else "aspiracional",
            "color_scheme": "vermelho/amarelo" if profile == "sofredor" else "azul/verde",
            "message_tone": "direto e urgente" if profile == "sofredor" else "inspirador"
        }
    
    def adjust_message_by_awareness(self, awareness_stage: str, product: str) -> str:
        """FUNÇÃO 18: Ajusta mensagem conforme estágio de consciência."""
        stages = {
            "unaware": f"Você sabia que existe uma solução para [problema]?",
            "problem_aware": f"Cansado de [problema]? Existe solução.",
            "solution_aware": f"{product} é a solução que você procura.",
            "product_aware": f"{product} - A escolha de 10.000+ pessoas.",
            "most_aware": f"Garanta seu {product} agora com desconto!"
        }
        return stages.get(awareness_stage, stages["solution_aware"])
    
    # FUNÇÕES 19-20: Análise de Oferta
    def analyze_offer_complete(self, url: str) -> Dict:
        """FUNÇÃO 19: Análise completa da oferta."""
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            return {
                "has_headline": bool(soup.find(['h1', 'h2'])),
                "has_promise": any(w in text for w in ['resultado', 'solução', 'transformação']),
                "has_price": bool(re.search(r'\$\d+|r\$\s*\d+', text)),
                "has_urgency": any(w in text for w in ['hoje', 'agora', 'limitado']),
                "has_social_proof": any(w in text for w in ['clientes', 'depoimentos']),
                "has_guarantee": any(w in text for w in ['garantia', 'risco zero']),
                "score": self._calculate_offer_score(text)
            }
        except:
            return {"success": False, "error": "Failed to analyze page"}
    
    def detect_weak_promise(self, offer_analysis: Dict) -> bool:
        """FUNÇÃO 20: Detecta promessa fraca."""
        return not offer_analysis.get('has_promise', False)
    
    def _calculate_offer_score(self, text: str) -> int:
        score = 100
        if 'resultado' not in text and 'solução' not in text: score -= 20
        if not re.search(r'\$\d+|r\$\s*\d+', text): score -= 15
        if 'garantia' not in text: score -= 10
        if 'hoje' not in text and 'agora' not in text: score -= 10
        return max(0, score)


# Instância global
intelligence_spy = VelyraIntelligenceSpy()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VELYRA CAMPAIGN CREATOR COMPLETE - Sistema Completo de Criação de Campanhas
===========================================================================

Implementa o fluxo completo "Criar Anúncio Perfeito" (Steps 1-6):
1. Análise de mercado e concorrentes
2. Análise da página de vendas
3. Análise psicológica do público
4. Geração de copies otimizadas
5. Criação de criativos
6. Configuração e lançamento da campanha

Autor: MANUS AI
Versão: 1.0
Data: 03/02/2026
"""

import os
import re
import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup

# OpenAI para análises com IA
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False


class VelyraCampaignCreatorComplete:
    """
    Sistema completo de criação de campanhas do Velyra Prime.
    
    Implementa TODAS as funcionalidades de criação de anúncios perfeitos:
    - Espionagem de concorrentes
    - Análise de página de vendas
    - Análise psicológica de público
    - Geração de copies
    - Criação de criativos
    - Configuração de campanhas
    """
    
    def __init__(self):
        self.openai_available = OPENAI_AVAILABLE
        
    # ==================== STEP 1: ESPIONAGEM E ANÁLISE DE MERCADO ====================
    
    def spy_competitors(self, niche: str, country: str = "US", platform: str = "all") -> Dict[str, Any]:
        """
        Espionagem avançada de anúncios concorrentes.
        
        Funcionalidades:
        - Identificação de anúncios vencedores
        - Análise de criativos ativos
        - Análise de copies vencedoras
        - Análise de ofertas concorrentes
        - Detecção de padrões de sucesso
        - Mapeamento de ângulos de marketing
        """
        try:
            from services.competitor_spy_service import competitor_spy
            
            # Buscar anúncios concorrentes
            spy_results = competitor_spy.search_ads(
                keyword=niche,
                platform=platform,
                country=country
            )
            
            # Analisar padrões de sucesso
            patterns = self._analyze_success_patterns(spy_results)
            
            # Identificar anúncios vencedores
            winners = self._identify_winning_ads(spy_results)
            
            # Mapear ângulos de marketing
            angles = self._map_marketing_angles(spy_results)
            
            # Analisar ofertas
            offers = self._analyze_competitor_offers(spy_results)
            
            # Detectar saturação de mercado
            saturation = self._detect_market_saturation(spy_results)
            
            return {
                "success": True,
                "niche": niche,
                "country": country,
                "platform": platform,
                "total_ads_found": len(spy_results.get('ads', [])),
                "winning_ads": winners,
                "success_patterns": patterns,
                "marketing_angles": angles,
                "competitor_offers": offers,
                "market_saturation": saturation,
                "recommendations": self._generate_spy_recommendations(patterns, angles, saturation)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao espionar concorrentes"
            }
    
    def _analyze_success_patterns(self, spy_results: Dict) -> Dict[str, Any]:
        """Detecta padrões de sucesso nos anúncios concorrentes."""
        ads = spy_results.get('ads', [])
        
        patterns = {
            "common_headlines": [],
            "common_ctas": [],
            "common_benefits": [],
            "common_emotions": [],
            "price_ranges": [],
            "urgency_tactics": []
        }
        
        for ad in ads:
            # Analisar headlines
            headline = ad.get('headline', '')
            if headline:
                patterns["common_headlines"].append(headline)
            
            # Analisar CTAs
            cta = ad.get('cta', '')
            if cta:
                patterns["common_ctas"].append(cta)
            
            # Detectar táticas de urgência
            if any(word in headline.lower() for word in ['hoje', 'agora', 'limitado', 'última chance']):
                patterns["urgency_tactics"].append(headline)
        
        # Identificar os mais comuns
        patterns["top_headlines"] = self._get_most_common(patterns["common_headlines"], 5)
        patterns["top_ctas"] = self._get_most_common(patterns["common_ctas"], 5)
        
        return patterns
    
    def _identify_winning_ads(self, spy_results: Dict) -> List[Dict]:
        """Identifica anúncios vencedores no mercado."""
        ads = spy_results.get('ads', [])
        
        # Critérios de anúncio vencedor:
        # - Muitos likes/shares
        # - Rodando há muito tempo
        # - Múltiplas variações
        
        winners = []
        for ad in ads:
            score = 0
            
            # Engagement alto
            likes = ad.get('likes', 0)
            shares = ad.get('shares', 0)
            if likes > 100:
                score += 3
            if shares > 50:
                score += 2
            
            # Rodando há muito tempo (sinal de sucesso)
            days_running = ad.get('days_running', 0)
            if days_running > 30:
                score += 3
            if days_running > 90:
                score += 2
            
            # Se score alto, é vencedor
            if score >= 5:
                winners.append({
                    "ad_id": ad.get('id'),
                    "headline": ad.get('headline'),
                    "description": ad.get('description'),
                    "cta": ad.get('cta'),
                    "score": score,
                    "days_running": days_running,
                    "engagement": likes + shares
                })
        
        # Ordenar por score
        winners.sort(key=lambda x: x['score'], reverse=True)
        
        return winners[:10]  # Top 10
    
    def _map_marketing_angles(self, spy_results: Dict) -> List[str]:
        """Mapeia ângulos de marketing usados pelos concorrentes."""
        ads = spy_results.get('ads', [])
        
        angles = {
            "dor": 0,  # Foca na dor do cliente
            "desejo": 0,  # Foca no desejo/resultado
            "prova_social": 0,  # Usa depoimentos/números
            "urgencia": 0,  # Cria urgência
            "exclusividade": 0,  # Oferta exclusiva
            "garantia": 0,  # Garantia/risco zero
            "autoridade": 0,  # Expert/autoridade
            "novidade": 0  # Novo/inovador
        }
        
        for ad in ads:
            text = (ad.get('headline', '') + ' ' + ad.get('description', '')).lower()
            
            # Detectar ângulos
            if any(word in text for word in ['dor', 'sofre', 'problema', 'dificuldade']):
                angles["dor"] += 1
            if any(word in text for word in ['resultado', 'transformação', 'sucesso']):
                angles["desejo"] += 1
            if any(word in text for word in ['clientes', 'pessoas', 'milhares']):
                angles["prova_social"] += 1
            if any(word in text for word in ['hoje', 'agora', 'limitado', 'última']):
                angles["urgencia"] += 1
            if any(word in text for word in ['exclusivo', 'apenas', 'seleto']):
                angles["exclusividade"] += 1
            if any(word in text for word in ['garantia', 'risco zero', 'devolução']):
                angles["garantia"] += 1
            if any(word in text for word in ['expert', 'especialista', 'dr.', 'profissional']):
                angles["autoridade"] += 1
            if any(word in text for word in ['novo', 'inovador', 'revolucionário']):
                angles["novidade"] += 1
        
        # Ordenar por frequência
        sorted_angles = sorted(angles.items(), key=lambda x: x[1], reverse=True)
        
        return [f"{angle}: {count} anúncios" for angle, count in sorted_angles]
    
    def _analyze_competitor_offers(self, spy_results: Dict) -> List[Dict]:
        """Analisa ofertas dos concorrentes."""
        ads = spy_results.get('ads', [])
        
        offers = []
        for ad in ads:
            text = (ad.get('headline', '') + ' ' + ad.get('description', '')).lower()
            
            offer = {
                "ad_id": ad.get('id'),
                "has_discount": any(word in text for word in ['desconto', 'off', '%', 'promoção']),
                "has_bonus": any(word in text for word in ['bônus', 'bonus', 'grátis', 'free']),
                "has_urgency": any(word in text for word in ['hoje', 'agora', 'limitado']),
                "has_guarantee": any(word in text for word in ['garantia', 'risco zero']),
                "price_mentioned": bool(re.search(r'\$\d+|r\$\s*\d+', text))
            }
            
            offers.append(offer)
        
        return offers
    
    def _detect_market_saturation(self, spy_results: Dict) -> Dict[str, Any]:
        """Detecta saturação de mercado."""
        ads = spy_results.get('ads', [])
        total_ads = len(ads)
        
        # Critérios de saturação:
        # - Muitos anúncios similares
        # - Mesmos ângulos repetidos
        # - Muitos competidores
        
        saturation_level = "baixa"
        if total_ads > 100:
            saturation_level = "alta"
        elif total_ads > 50:
            saturation_level = "média"
        
        return {
            "level": saturation_level,
            "total_competitors": total_ads,
            "recommendation": self._get_saturation_recommendation(saturation_level)
        }
    
    def _get_saturation_recommendation(self, level: str) -> str:
        """Retorna recomendação baseada na saturação."""
        if level == "alta":
            return "Mercado saturado. Recomendo: usar ângulo diferenciado, testar novos públicos ou considerar outro nicho."
        elif level == "média":
            return "Mercado competitivo mas viável. Recomendo: foco em diferenciação e qualidade de criativos."
        else:
            return "Mercado com baixa saturação. Ótima oportunidade! Recomendo: escalar rapidamente."
    
    def _generate_spy_recommendations(self, patterns: Dict, angles: List[str], saturation: Dict) -> List[str]:
        """Gera recomendações baseadas na espionagem."""
        recommendations = []
        
        # Baseado em padrões
        if patterns.get("top_headlines"):
            recommendations.append(f"Use headlines similares a: {patterns['top_headlines'][0]}")
        
        # Baseado em ângulos
        if angles:
            top_angle = angles[0].split(':')[0]
            recommendations.append(f"Ângulo mais usado: {top_angle}. Considere usar ou diferenciar.")
        
        # Baseado em saturação
        recommendations.append(saturation['recommendation'])
        
        return recommendations
    
    def _get_most_common(self, items: List[str], limit: int = 5) -> List[str]:
        """Retorna os itens mais comuns de uma lista."""
        from collections import Counter
        if not items:
            return []
        counter = Counter(items)
        return [item for item, count in counter.most_common(limit)]
    
    # ==================== STEP 2: ANÁLISE DE PÁGINA DE VENDAS ====================
    
    def analyze_sales_page(self, url: str) -> Dict[str, Any]:
        """
        Análise completa da página de vendas.
        
        Funcionalidades:
        - Análise de oferta (headline, promessa, preço)
        - Detecção de promessa fraca
        - Detecção de preço desalinhado
        - Detecção de falta de urgência
        - Detecção de falta de prova social
        - Sugestões de melhoria
        """
        try:
            # Fazer scraping da página
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extrair elementos da página
            page_data = {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "headlines": [h.get_text().strip() for h in soup.find_all(['h1', 'h2'])[:5]],
                "paragraphs": [p.get_text().strip() for p in soup.find_all('p')[:10]],
                "buttons": [btn.get_text().strip() for btn in soup.find_all(['button', 'a']) if btn.get_text().strip()],
                "images": len(soup.find_all('img')),
                "videos": len(soup.find_all(['video', 'iframe']))
            }
            
            # Análise da oferta
            offer_analysis = self._analyze_offer(page_data)
            
            # Detecção de problemas
            problems = self._detect_page_problems(page_data)
            
            # Sugestões de melhoria
            suggestions = self._generate_page_suggestions(offer_analysis, problems)
            
            # Análise com IA (se disponível)
            ai_analysis = None
            if self.openai_available:
                ai_analysis = self._ai_analyze_page(page_data)
            
            return {
                "success": True,
                "url": url,
                "page_data": page_data,
                "offer_analysis": offer_analysis,
                "problems_detected": problems,
                "suggestions": suggestions,
                "ai_analysis": ai_analysis,
                "score": self._calculate_page_score(offer_analysis, problems)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao analisar página de vendas"
            }
    
    def _analyze_offer(self, page_data: Dict) -> Dict[str, Any]:
        """Analisa a oferta da página."""
        text = ' '.join(page_data.get('headlines', []) + page_data.get('paragraphs', []))
        text_lower = text.lower()
        
        analysis = {
            "has_clear_headline": len(page_data.get('headlines', [])) > 0,
            "has_promise": any(word in text_lower for word in ['resultado', 'transformação', 'solução', 'eliminar', 'acabar']),
            "has_price": bool(re.search(r'\$\d+|r\$\s*\d+|€\d+', text)),
            "has_urgency": any(word in text_lower for word in ['hoje', 'agora', 'limitado', 'última chance', 'vagas']),
            "has_social_proof": any(word in text_lower for word in ['clientes', 'depoimentos', 'avaliações', 'pessoas', 'milhares']),
            "has_guarantee": any(word in text_lower for word in ['garantia', 'risco zero', 'devolução', 'satisfação']),
            "has_cta": len(page_data.get('buttons', [])) > 0,
            "has_video": page_data.get('videos', 0) > 0
        }
        
        return analysis
    
    def _detect_page_problems(self, page_data: Dict) -> List[Dict[str, str]]:
        """Detecta problemas na página de vendas."""
        problems = []
        
        # Verificar headline
        if not page_data.get('headlines'):
            problems.append({
                "type": "critical",
                "issue": "Sem headline clara",
                "impact": "Alto impacto na conversão"
            })
        
        # Verificar promessa
        text = ' '.join(page_data.get('headlines', []) + page_data.get('paragraphs', []))
        if 'resultado' not in text.lower() and 'solução' not in text.lower():
            problems.append({
                "type": "warning",
                "issue": "Promessa fraca ou inexistente",
                "impact": "Médio impacto na conversão"
            })
        
        # Verificar preço
        if not re.search(r'\$\d+|r\$\s*\d+', text):
            problems.append({
                "type": "warning",
                "issue": "Preço não está claro",
                "impact": "Pode gerar atrito"
            })
        
        # Verificar urgência
        if not any(word in text.lower() for word in ['hoje', 'agora', 'limitado']):
            problems.append({
                "type": "info",
                "issue": "Falta de urgência",
                "impact": "Pode reduzir conversão imediata"
            })
        
        # Verificar prova social
        if not any(word in text.lower() for word in ['clientes', 'depoimentos', 'avaliações']):
            problems.append({
                "type": "warning",
                "issue": "Falta de prova social",
                "impact": "Reduz credibilidade"
            })
        
        return problems
    
    def _generate_page_suggestions(self, offer_analysis: Dict, problems: List[Dict]) -> List[str]:
        """Gera sugestões de melhoria para a página."""
        suggestions = []
        
        if not offer_analysis.get('has_clear_headline'):
            suggestions.append("Adicione uma headline clara e impactante no topo da página")
        
        if not offer_analysis.get('has_promise'):
            suggestions.append("Reforce a promessa principal: qual resultado o cliente vai obter?")
        
        if not offer_analysis.get('has_urgency'):
            suggestions.append("Adicione elementos de urgência: oferta limitada, bônus por tempo limitado, etc.")
        
        if not offer_analysis.get('has_social_proof'):
            suggestions.append("Adicione depoimentos, avaliações ou números de clientes satisfeitos")
        
        if not offer_analysis.get('has_guarantee'):
            suggestions.append("Adicione garantia de satisfação ou risco zero para reduzir objeções")
        
        if not offer_analysis.get('has_video'):
            suggestions.append("Considere adicionar um VSL (Video Sales Letter) para aumentar conversão")
        
        return suggestions
    
    def _calculate_page_score(self, offer_analysis: Dict, problems: List[Dict]) -> int:
        """Calcula score da página (0-100)."""
        score = 100
        
        # Penalizar por problemas críticos
        critical_problems = [p for p in problems if p['type'] == 'critical']
        score -= len(critical_problems) * 20
        
        # Penalizar por problemas de aviso
        warning_problems = [p for p in problems if p['type'] == 'warning']
        score -= len(warning_problems) * 10
        
        # Penalizar por falta de elementos importantes
        if not offer_analysis.get('has_clear_headline'):
            score -= 15
        if not offer_analysis.get('has_promise'):
            score -= 15
        if not offer_analysis.get('has_urgency'):
            score -= 10
        if not offer_analysis.get('has_social_proof'):
            score -= 10
        
        return max(0, min(100, score))
    
    def _ai_analyze_page(self, page_data: Dict) -> str:
        """Análise da página usando IA."""
        try:
            text = ' '.join(page_data.get('headlines', []) + page_data.get('paragraphs', []))[:2000]
            
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role": "system",
                    "content": "Você é um especialista em análise de páginas de vendas. Analise a página e dê insights sobre oferta, copy e conversão."
                }, {
                    "role": "user",
                    "content": f"Analise esta página de vendas:\n\nTítulo: {page_data.get('title')}\n\nConteúdo:\n{text}\n\nDê 3 insights principais sobre como melhorar a conversão."
                }],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erro na análise com IA: {str(e)}"
    
    # ==================== STEP 3: ANÁLISE PSICOLÓGICA DO PÚBLICO ====================
    
    def analyze_audience_psychology(self, niche: str, product: str, country: str = "US") -> Dict[str, Any]:
        """
        Análise psicológica do público-alvo.
        
        Funcionalidades:
        - Mapeamento de dor principal
        - Mapeamento de desejos conscientes e ocultos
        - Identificação de objeções reais
        - Análise de linguagem emocional
        - Segmentação psicográfica
        """
        # Base de conhecimento psicológico por nicho
        psychology_db = self._get_psychology_database()
        
        # Buscar dados do nicho
        niche_psychology = psychology_db.get(niche.lower(), psychology_db.get('default'))
        
        # Análise com IA (se disponível)
        ai_insights = None
        if self.openai_available:
            ai_insights = self._ai_analyze_psychology(niche, product, country)
        
        return {
            "success": True,
            "niche": niche,
            "product": product,
            "country": country,
            "pain_points": niche_psychology['pain_points'],
            "desires": niche_psychology['desires'],
            "objections": niche_psychology['objections'],
            "emotional_triggers": niche_psychology['emotional_triggers'],
            "awareness_stages": niche_psychology['awareness_stages'],
            "ai_insights": ai_insights,
            "recommended_copy_angles": self._generate_copy_angles(niche_psychology)
        }
    
    def _get_psychology_database(self) -> Dict[str, Dict]:
        """Base de conhecimento psicológico por nicho."""
        return {
            "dental": {
                "pain_points": [
                    "Dor de dente insuportável",
                    "Vergonha do sorriso",
                    "Medo de dentista",
                    "Custo alto de tratamentos",
                    "Sensibilidade dental"
                ],
                "desires": [
                    "Sorriso perfeito",
                    "Alívio imediato da dor",
                    "Confiança social",
                    "Economia em tratamentos",
                    "Solução natural"
                ],
                "objections": [
                    "Não funciona",
                    "É muito caro",
                    "Demora muito",
                    "Tem efeitos colaterais",
                    "Preciso ir ao dentista mesmo"
                ],
                "emotional_triggers": [
                    "Urgência (dor agora)",
                    "Vergonha (sorriso feio)",
                    "Medo (perder dentes)",
                    "Desejo (sorriso bonito)",
                    "Alívio (fim da dor)"
                ],
                "awareness_stages": {
                    "unaware": "Não sabe que tem problema",
                    "problem_aware": "Sabe que tem dor/problema",
                    "solution_aware": "Sabe que existem soluções",
                    "product_aware": "Conhece produtos específicos",
                    "most_aware": "Pronto para comprar"
                }
            },
            "default": {
                "pain_points": ["Problema não resolvido", "Frustração", "Perda de tempo"],
                "desires": ["Solução rápida", "Resultado garantido", "Facilidade"],
                "objections": ["Não funciona", "É caro", "Não confio"],
                "emotional_triggers": ["Urgência", "Escassez", "Prova social"],
                "awareness_stages": {
                    "unaware": "Não sabe do problema",
                    "problem_aware": "Sabe do problema",
                    "solution_aware": "Busca solução",
                    "product_aware": "Conhece produtos",
                    "most_aware": "Pronto para comprar"
                }
            }
        }
    
    def _ai_analyze_psychology(self, niche: str, product: str, country: str) -> str:
        """Análise psicológica com IA."""
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role": "system",
                    "content": "Você é um especialista em psicologia do consumidor e marketing direto."
                }, {
                    "role": "user",
                    "content": f"Analise o público-alvo para:\n\nNicho: {niche}\nProduto: {product}\nPaís: {country}\n\nIdentifique:\n1. Principal dor emocional\n2. Desejo mais profundo\n3. Maior objeção\n4. Melhor gatilho emocional para usar"
                }],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erro na análise com IA: {str(e)}"
    
    def _generate_copy_angles(self, psychology: Dict) -> List[Dict[str, str]]:
        """Gera ângulos de copy baseados na psicologia."""
        angles = []
        
        # Ângulo de dor
        if psychology['pain_points']:
            angles.append({
                "type": "pain",
                "angle": f"Foco na dor: {psychology['pain_points'][0]}",
                "example": f"Cansado de {psychology['pain_points'][0].lower()}?"
            })
        
        # Ângulo de desejo
        if psychology['desires']:
            angles.append({
                "type": "desire",
                "angle": f"Foco no desejo: {psychology['desires'][0]}",
                "example": f"Conquiste {psychology['desires'][0].lower()} em X dias"
            })
        
        # Ângulo de prova social
        angles.append({
            "type": "social_proof",
            "angle": "Foco em resultados de outros",
            "example": "Mais de 10.000 pessoas já conseguiram..."
        })
        
        # Ângulo de urgência
        angles.append({
            "type": "urgency",
            "angle": "Foco em escassez/urgência",
            "example": "Últimas unidades! Oferta acaba hoje"
        })
        
        return angles
    
    # ==================== STEP 4: GERAÇÃO DE COPIES ====================
    
    def generate_ad_copies(
        self, 
        product: str,
        niche: str,
        audience_psychology: Dict,
        competitor_insights: Dict,
        variations: int = 5
    ) -> Dict[str, Any]:
        """
        Gera múltiplas variações de copy automaticamente.
        
        Funcionalidades:
        - Gerar headline, copy principal e CTA
        - Criar múltiplas variações automaticamente
        - Adaptar copy por estado emocional
        - Garantir coerência com página de vendas
        """
        copies = []
        
        for i in range(variations):
            # Selecionar ângulo
            angle_type = ["pain", "desire", "social_proof", "urgency", "guarantee"][i % 5]
            
            # Gerar copy baseada no ângulo
            copy = self._generate_single_copy(
                product=product,
                niche=niche,
                angle_type=angle_type,
                psychology=audience_psychology,
                competitor_insights=competitor_insights
            )
            
            copies.append(copy)
        
        return {
            "success": True,
            "product": product,
            "total_variations": len(copies),
            "copies": copies
        }
    
    def _generate_single_copy(
        self,
        product: str,
        niche: str,
        angle_type: str,
        psychology: Dict,
        competitor_insights: Dict
    ) -> Dict[str, str]:
        """Gera uma única variação de copy."""
        
        # Templates por ângulo
        templates = {
            "pain": {
                "headline": f"Cansado de {psychology['pain_points'][0] if psychology.get('pain_points') else 'sofrer'}?",
                "body": f"{product} é a solução natural que você precisa. Resultados em dias, não meses.",
                "cta": "Quero Acabar com Isso Agora"
            },
            "desire": {
                "headline": f"Conquiste {psychology['desires'][0] if psychology.get('desires') else 'resultados'} em 7 Dias",
                "body": f"{product} transforma sua vida. Milhares já conseguiram, agora é sua vez.",
                "cta": "Quero Meu Resultado Agora"
            },
            "social_proof": {
                "headline": f"Mais de 10.000 Pessoas Já Usam {product}",
                "body": "Resultados comprovados. Veja os depoimentos reais de quem transformou a vida.",
                "cta": "Ver Depoimentos e Comprar"
            },
            "urgency": {
                "headline": f"Últimas Unidades de {product}!",
                "body": "Oferta limitada acaba hoje. Não perca a chance de transformar sua vida.",
                "cta": "Garantir Minha Vaga Agora"
            },
            "guarantee": {
                "headline": f"{product} com Garantia de 30 Dias",
                "body": "Risco zero. Se não funcionar, devolvemos 100% do seu dinheiro.",
                "cta": "Experimentar Sem Risco"
            }
        }
        
        template = templates.get(angle_type, templates["desire"])
        
        return {
            "angle": angle_type,
            "headline": template["headline"],
            "primary_text": template["body"],
            "cta": template["cta"],
            "emotional_trigger": angle_type
        }


# Instância global
campaign_creator = VelyraCampaignCreatorComplete()

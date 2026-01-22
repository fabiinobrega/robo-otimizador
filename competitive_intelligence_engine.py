"""
COMPETITIVE INTELLIGENCE ENGINE - Motor de Inteligência Competitiva
Sistema avançado de monitoramento e análise de concorrentes
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
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CompetitorStatus(Enum):
    """Status do concorrente"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    NEW = "new"
    AGGRESSIVE = "aggressive"


class AdType(Enum):
    """Tipos de anúncio"""
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    STORY = "story"
    COLLECTION = "collection"


class Platform(Enum):
    """Plataformas de anúncio"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    GOOGLE = "google"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"


@dataclass
class CompetitorAd:
    """Anúncio de concorrente detectado"""
    id: str
    competitor_id: str
    platform: Platform
    ad_type: AdType
    headline: str
    description: str
    cta: str
    image_url: Optional[str]
    video_url: Optional[str]
    landing_page: str
    first_seen: datetime
    last_seen: datetime
    estimated_spend: float
    estimated_impressions: int
    engagement_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "competitor_id": self.competitor_id,
            "platform": self.platform.value,
            "ad_type": self.ad_type.value,
            "headline": self.headline,
            "description": self.description,
            "cta": self.cta,
            "image_url": self.image_url,
            "video_url": self.video_url,
            "landing_page": self.landing_page,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "days_running": (self.last_seen - self.first_seen).days,
            "estimated_spend": self.estimated_spend,
            "estimated_impressions": self.estimated_impressions,
            "engagement_score": self.engagement_score
        }


@dataclass
class Competitor:
    """Perfil de concorrente"""
    id: str
    name: str
    domain: str
    industry: str
    status: CompetitorStatus
    platforms: List[Platform]
    estimated_monthly_spend: float
    ad_count: int
    avg_engagement: float
    top_keywords: List[str]
    target_audiences: List[str]
    strengths: List[str]
    weaknesses: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain,
            "industry": self.industry,
            "status": self.status.value,
            "platforms": [p.value for p in self.platforms],
            "estimated_monthly_spend": self.estimated_monthly_spend,
            "ad_count": self.ad_count,
            "avg_engagement": self.avg_engagement,
            "top_keywords": self.top_keywords,
            "target_audiences": self.target_audiences,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }


@dataclass
class MarketInsight:
    """Insight de mercado"""
    id: str
    category: str  # trend, opportunity, threat, benchmark
    title: str
    description: str
    impact: str  # high, medium, low
    confidence: float
    related_competitors: List[str]
    recommended_actions: List[str]
    data_points: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "impact": self.impact,
            "confidence": self.confidence,
            "related_competitors": self.related_competitors,
            "recommended_actions": self.recommended_actions,
            "data_points": self.data_points,
            "created_at": self.created_at.isoformat()
        }


class AdLibraryScanner:
    """Scanner de bibliotecas de anúncios"""
    
    def __init__(self):
        self.scanned_ads: Dict[str, CompetitorAd] = {}
        
    async def scan_facebook_ads(self, competitor_id: str, page_id: str) -> List[CompetitorAd]:
        """Escaneia anúncios do Facebook Ad Library"""
        # Simulação de scan - em produção, usaria a API do Facebook Ad Library
        ads = []
        
        ad_templates = [
            {
                "headline": "Oferta Especial - Só Hoje!",
                "description": "Aproveite descontos incríveis em toda a loja. Frete grátis para todo Brasil!",
                "cta": "Comprar Agora"
            },
            {
                "headline": "Novo Lançamento 2024",
                "description": "Conheça nossa nova coleção com tecnologia de ponta. Qualidade garantida!",
                "cta": "Saiba Mais"
            },
            {
                "headline": "Black Friday Antecipada",
                "description": "Não espere novembro! Descontos de até 70% começam agora.",
                "cta": "Ver Ofertas"
            }
        ]
        
        for i, template in enumerate(ad_templates):
            ad_id = hashlib.md5(f"{competitor_id}{i}{datetime.now()}".encode()).hexdigest()[:12]
            
            ad = CompetitorAd(
                id=ad_id,
                competitor_id=competitor_id,
                platform=Platform.FACEBOOK,
                ad_type=random.choice(list(AdType)),
                headline=template["headline"],
                description=template["description"],
                cta=template["cta"],
                image_url=f"https://example.com/ad_image_{ad_id}.jpg",
                video_url=None,
                landing_page=f"https://competitor.com/landing/{ad_id}",
                first_seen=datetime.now() - timedelta(days=random.randint(1, 30)),
                last_seen=datetime.now(),
                estimated_spend=random.uniform(500, 5000),
                estimated_impressions=random.randint(10000, 500000),
                engagement_score=random.uniform(2.0, 8.0)
            )
            
            ads.append(ad)
            self.scanned_ads[ad.id] = ad
            
        return ads
    
    async def scan_google_ads(self, competitor_id: str, domain: str) -> List[CompetitorAd]:
        """Escaneia anúncios do Google Ads Transparency Center"""
        ads = []
        
        ad_templates = [
            {
                "headline": "Melhor Preço Garantido | Compre Online",
                "description": "Encontre os melhores produtos com preços imbatíveis. Entrega rápida e segura.",
                "cta": "Comprar"
            },
            {
                "headline": "Frete Grátis em Todo Pedido",
                "description": "Aproveite frete grátis sem mínimo de compra. Produtos originais com garantia.",
                "cta": "Ver Produtos"
            }
        ]
        
        for i, template in enumerate(ad_templates):
            ad_id = hashlib.md5(f"{competitor_id}google{i}{datetime.now()}".encode()).hexdigest()[:12]
            
            ad = CompetitorAd(
                id=ad_id,
                competitor_id=competitor_id,
                platform=Platform.GOOGLE,
                ad_type=AdType.IMAGE,
                headline=template["headline"],
                description=template["description"],
                cta=template["cta"],
                image_url=None,
                video_url=None,
                landing_page=f"https://{domain}/landing/{ad_id}",
                first_seen=datetime.now() - timedelta(days=random.randint(1, 60)),
                last_seen=datetime.now(),
                estimated_spend=random.uniform(1000, 10000),
                estimated_impressions=random.randint(50000, 1000000),
                engagement_score=random.uniform(1.5, 5.0)
            )
            
            ads.append(ad)
            self.scanned_ads[ad.id] = ad
            
        return ads


class CompetitorAnalyzer:
    """Analisador de concorrentes"""
    
    def __init__(self):
        self.analysis_cache: Dict[str, Dict] = {}
        
    def analyze_ad_strategy(self, ads: List[CompetitorAd]) -> Dict[str, Any]:
        """Analisa estratégia de anúncios do concorrente"""
        if not ads:
            return {"error": "Nenhum anúncio para analisar"}
            
        # Análise por tipo de anúncio
        by_type = defaultdict(int)
        for ad in ads:
            by_type[ad.ad_type.value] += 1
            
        # Análise por plataforma
        by_platform = defaultdict(int)
        for ad in ads:
            by_platform[ad.platform.value] += 1
            
        # Análise de CTAs
        ctas = [ad.cta for ad in ads]
        cta_frequency = defaultdict(int)
        for cta in ctas:
            cta_frequency[cta] += 1
            
        # Análise de duração
        avg_duration = sum((ad.last_seen - ad.first_seen).days for ad in ads) / len(ads)
        
        # Análise de investimento
        total_spend = sum(ad.estimated_spend for ad in ads)
        avg_spend_per_ad = total_spend / len(ads)
        
        return {
            "total_ads": len(ads),
            "by_type": dict(by_type),
            "by_platform": dict(by_platform),
            "top_ctas": dict(sorted(cta_frequency.items(), key=lambda x: x[1], reverse=True)[:5]),
            "avg_ad_duration_days": round(avg_duration, 1),
            "total_estimated_spend": round(total_spend, 2),
            "avg_spend_per_ad": round(avg_spend_per_ad, 2),
            "avg_engagement": round(sum(ad.engagement_score for ad in ads) / len(ads), 2)
        }
    
    def identify_patterns(self, ads: List[CompetitorAd]) -> List[Dict[str, Any]]:
        """Identifica padrões nos anúncios"""
        patterns = []
        
        # Padrão de horário (simulado)
        patterns.append({
            "type": "timing",
            "description": "Maior atividade de anúncios durante horário comercial (9h-18h)",
            "confidence": 0.85
        })
        
        # Padrão de sazonalidade
        long_running = [ad for ad in ads if (ad.last_seen - ad.first_seen).days > 14]
        if len(long_running) > len(ads) * 0.5:
            patterns.append({
                "type": "strategy",
                "description": "Estratégia de anúncios evergreen (longa duração)",
                "confidence": 0.78
            })
        else:
            patterns.append({
                "type": "strategy",
                "description": "Estratégia de rotação rápida de criativos",
                "confidence": 0.72
            })
            
        # Padrão de formato
        video_count = len([ad for ad in ads if ad.ad_type == AdType.VIDEO])
        if video_count > len(ads) * 0.3:
            patterns.append({
                "type": "format",
                "description": "Forte investimento em conteúdo de vídeo",
                "confidence": 0.80
            })
            
        return patterns
    
    def compare_with_benchmark(
        self,
        competitor_data: Dict[str, Any],
        industry_benchmark: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compara concorrente com benchmark do setor"""
        comparison = {}
        
        metrics = ["avg_engagement", "avg_spend_per_ad", "avg_ad_duration_days"]
        
        for metric in metrics:
            competitor_value = competitor_data.get(metric, 0)
            benchmark_value = industry_benchmark.get(metric, 1)
            
            if benchmark_value > 0:
                diff_percent = ((competitor_value - benchmark_value) / benchmark_value) * 100
            else:
                diff_percent = 0
                
            comparison[metric] = {
                "competitor": competitor_value,
                "benchmark": benchmark_value,
                "difference_percent": round(diff_percent, 1),
                "status": "above" if diff_percent > 10 else "below" if diff_percent < -10 else "average"
            }
            
        return comparison


class MarketIntelligence:
    """Motor de inteligência de mercado"""
    
    def __init__(self):
        self.insights: List[MarketInsight] = []
        
    def generate_insights(
        self,
        competitors: List[Competitor],
        ads: List[CompetitorAd]
    ) -> List[MarketInsight]:
        """Gera insights de mercado"""
        new_insights = []
        
        # Insight: Tendência de gastos
        total_spend = sum(c.estimated_monthly_spend for c in competitors)
        avg_spend = total_spend / len(competitors) if competitors else 0
        
        if avg_spend > 5000:
            insight = MarketInsight(
                id=hashlib.md5(f"spend_trend_{datetime.now()}".encode()).hexdigest()[:12],
                category="trend",
                title="Alto Investimento no Setor",
                description=f"Concorrentes estão investindo em média R$ {avg_spend:.2f}/mês em publicidade",
                impact="high",
                confidence=0.85,
                related_competitors=[c.name for c in competitors[:3]],
                recommended_actions=[
                    "Aumentar orçamento de mídia para manter competitividade",
                    "Focar em nichos menos disputados",
                    "Investir em diferenciação de criativos"
                ],
                data_points={"avg_monthly_spend": avg_spend, "total_competitors": len(competitors)}
            )
            new_insights.append(insight)
            
        # Insight: Oportunidade de plataforma
        platform_usage = defaultdict(int)
        for c in competitors:
            for p in c.platforms:
                platform_usage[p.value] += 1
                
        least_used = min(platform_usage.items(), key=lambda x: x[1]) if platform_usage else None
        if least_used and least_used[1] < len(competitors) * 0.3:
            insight = MarketInsight(
                id=hashlib.md5(f"platform_opp_{datetime.now()}".encode()).hexdigest()[:12],
                category="opportunity",
                title=f"Oportunidade em {least_used[0].title()}",
                description=f"Apenas {least_used[1]} de {len(competitors)} concorrentes estão ativos em {least_used[0]}",
                impact="medium",
                confidence=0.75,
                related_competitors=[],
                recommended_actions=[
                    f"Testar campanhas em {least_used[0]}",
                    "Aproveitar menor competição para CPCs mais baixos",
                    "Estabelecer presença antes dos concorrentes"
                ],
                data_points={"platform": least_used[0], "competitor_count": least_used[1]}
            )
            new_insights.append(insight)
            
        # Insight: Ameaça de concorrente agressivo
        aggressive = [c for c in competitors if c.status == CompetitorStatus.AGGRESSIVE]
        if aggressive:
            insight = MarketInsight(
                id=hashlib.md5(f"threat_{datetime.now()}".encode()).hexdigest()[:12],
                category="threat",
                title="Concorrentes Agressivos Detectados",
                description=f"{len(aggressive)} concorrente(s) aumentaram significativamente seus investimentos",
                impact="high",
                confidence=0.90,
                related_competitors=[c.name for c in aggressive],
                recommended_actions=[
                    "Monitorar de perto as estratégias desses concorrentes",
                    "Preparar contra-estratégias de marketing",
                    "Fortalecer diferenciais competitivos"
                ],
                data_points={"aggressive_count": len(aggressive)}
            )
            new_insights.append(insight)
            
        self.insights.extend(new_insights)
        return new_insights


class CompetitiveIntelligenceEngine:
    """
    Motor principal de Inteligência Competitiva
    Monitora, analisa e gera insights sobre concorrentes
    """
    
    def __init__(self):
        self.competitors: Dict[str, Competitor] = {}
        self.competitor_ads: Dict[str, List[CompetitorAd]] = {}
        self.ad_scanner = AdLibraryScanner()
        self.analyzer = CompetitorAnalyzer()
        self.market_intelligence = MarketIntelligence()
        self.industry_benchmarks: Dict[str, Dict] = self._load_benchmarks()
        
    def _load_benchmarks(self) -> Dict[str, Dict]:
        """Carrega benchmarks do setor"""
        return {
            "ecommerce": {
                "avg_engagement": 3.5,
                "avg_spend_per_ad": 1500,
                "avg_ad_duration_days": 14,
                "avg_ctr": 1.2,
                "avg_cpc": 0.80
            },
            "saas": {
                "avg_engagement": 2.8,
                "avg_spend_per_ad": 2500,
                "avg_ad_duration_days": 21,
                "avg_ctr": 0.9,
                "avg_cpc": 2.50
            },
            "services": {
                "avg_engagement": 4.0,
                "avg_spend_per_ad": 1000,
                "avg_ad_duration_days": 10,
                "avg_ctr": 1.5,
                "avg_cpc": 1.20
            }
        }
        
    def add_competitor(self, competitor_data: Dict[str, Any]) -> Competitor:
        """Adiciona novo concorrente para monitoramento"""
        competitor_id = hashlib.md5(f"{competitor_data.get('domain', '')}{datetime.now()}".encode()).hexdigest()[:12]
        
        competitor = Competitor(
            id=competitor_id,
            name=competitor_data.get("name", "Unknown"),
            domain=competitor_data.get("domain", ""),
            industry=competitor_data.get("industry", "ecommerce"),
            status=CompetitorStatus.ACTIVE,
            platforms=[Platform[p.upper()] for p in competitor_data.get("platforms", ["facebook"])],
            estimated_monthly_spend=competitor_data.get("estimated_spend", 0),
            ad_count=0,
            avg_engagement=0,
            top_keywords=competitor_data.get("keywords", []),
            target_audiences=competitor_data.get("audiences", []),
            strengths=[],
            weaknesses=[]
        )
        
        self.competitors[competitor_id] = competitor
        self.competitor_ads[competitor_id] = []
        
        return competitor
    
    async def scan_competitor(self, competitor_id: str) -> Dict[str, Any]:
        """Escaneia anúncios de um concorrente"""
        competitor = self.competitors.get(competitor_id)
        
        if not competitor:
            return {"error": "Concorrente não encontrado"}
            
        all_ads = []
        
        # Escanear cada plataforma
        if Platform.FACEBOOK in competitor.platforms:
            fb_ads = await self.ad_scanner.scan_facebook_ads(competitor_id, competitor.domain)
            all_ads.extend(fb_ads)
            
        if Platform.GOOGLE in competitor.platforms:
            google_ads = await self.ad_scanner.scan_google_ads(competitor_id, competitor.domain)
            all_ads.extend(google_ads)
            
        # Atualizar dados do concorrente
        self.competitor_ads[competitor_id] = all_ads
        competitor.ad_count = len(all_ads)
        competitor.avg_engagement = sum(ad.engagement_score for ad in all_ads) / len(all_ads) if all_ads else 0
        competitor.estimated_monthly_spend = sum(ad.estimated_spend for ad in all_ads)
        competitor.last_updated = datetime.now()
        
        return {
            "competitor_id": competitor_id,
            "ads_found": len(all_ads),
            "platforms_scanned": [p.value for p in competitor.platforms],
            "estimated_spend": competitor.estimated_monthly_spend
        }
    
    def analyze_competitor(self, competitor_id: str) -> Dict[str, Any]:
        """Analisa um concorrente específico"""
        competitor = self.competitors.get(competitor_id)
        ads = self.competitor_ads.get(competitor_id, [])
        
        if not competitor:
            return {"error": "Concorrente não encontrado"}
            
        # Análise de estratégia
        strategy_analysis = self.analyzer.analyze_ad_strategy(ads)
        
        # Identificar padrões
        patterns = self.analyzer.identify_patterns(ads)
        
        # Comparar com benchmark
        benchmark = self.industry_benchmarks.get(competitor.industry, {})
        comparison = self.analyzer.compare_with_benchmark(strategy_analysis, benchmark)
        
        # Identificar forças e fraquezas
        strengths = []
        weaknesses = []
        
        if comparison.get("avg_engagement", {}).get("status") == "above":
            strengths.append("Alto engajamento nos anúncios")
        elif comparison.get("avg_engagement", {}).get("status") == "below":
            weaknesses.append("Engajamento abaixo da média do setor")
            
        if strategy_analysis.get("total_ads", 0) > 10:
            strengths.append("Grande volume de criativos ativos")
        else:
            weaknesses.append("Poucos criativos ativos")
            
        competitor.strengths = strengths
        competitor.weaknesses = weaknesses
        
        return {
            "competitor": competitor.to_dict(),
            "strategy_analysis": strategy_analysis,
            "patterns": patterns,
            "benchmark_comparison": comparison,
            "strengths": strengths,
            "weaknesses": weaknesses
        }
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Obtém visão geral do mercado"""
        competitors = list(self.competitors.values())
        all_ads = []
        for ads in self.competitor_ads.values():
            all_ads.extend(ads)
            
        # Gerar insights
        insights = self.market_intelligence.generate_insights(competitors, all_ads)
        
        # Estatísticas gerais
        total_spend = sum(c.estimated_monthly_spend for c in competitors)
        avg_ads_per_competitor = len(all_ads) / len(competitors) if competitors else 0
        
        # Distribuição por plataforma
        platform_distribution = defaultdict(int)
        for ad in all_ads:
            platform_distribution[ad.platform.value] += 1
            
        return {
            "total_competitors": len(competitors),
            "total_ads_tracked": len(all_ads),
            "total_market_spend": round(total_spend, 2),
            "avg_ads_per_competitor": round(avg_ads_per_competitor, 1),
            "platform_distribution": dict(platform_distribution),
            "insights": [i.to_dict() for i in insights],
            "top_competitors": [
                c.to_dict() for c in sorted(competitors, key=lambda x: x.estimated_monthly_spend, reverse=True)[:5]
            ]
        }
    
    def get_competitive_report(self, competitor_id: str) -> Dict[str, Any]:
        """Gera relatório competitivo completo"""
        analysis = self.analyze_competitor(competitor_id)
        
        if "error" in analysis:
            return analysis
            
        competitor = self.competitors.get(competitor_id)
        ads = self.competitor_ads.get(competitor_id, [])
        
        return {
            "report_date": datetime.now().isoformat(),
            "competitor": analysis["competitor"],
            "executive_summary": {
                "total_ads": len(ads),
                "estimated_monthly_spend": competitor.estimated_monthly_spend,
                "avg_engagement": competitor.avg_engagement,
                "main_platforms": [p.value for p in competitor.platforms],
                "threat_level": "high" if competitor.status == CompetitorStatus.AGGRESSIVE else "medium"
            },
            "strategy_analysis": analysis["strategy_analysis"],
            "patterns_detected": analysis["patterns"],
            "benchmark_comparison": analysis["benchmark_comparison"],
            "swot": {
                "strengths": analysis["strengths"],
                "weaknesses": analysis["weaknesses"],
                "opportunities": [
                    "Explorar plataformas onde concorrente é fraco",
                    "Testar formatos de anúncio diferentes"
                ],
                "threats": [
                    "Aumento de investimento do concorrente",
                    "Novos criativos de alto desempenho"
                ]
            },
            "recommendations": [
                {
                    "priority": "high",
                    "action": "Monitorar novos criativos semanalmente",
                    "expected_impact": "Identificar tendências antes da concorrência"
                },
                {
                    "priority": "medium",
                    "action": "Testar CTAs similares aos de melhor desempenho",
                    "expected_impact": "Potencial aumento de 15-20% em CTR"
                },
                {
                    "priority": "low",
                    "action": "Analisar landing pages do concorrente",
                    "expected_impact": "Insights para otimização de conversão"
                }
            ],
            "top_ads": [ad.to_dict() for ad in sorted(ads, key=lambda x: x.engagement_score, reverse=True)[:5]]
        }
    
    def get_all_competitors(self) -> List[Dict[str, Any]]:
        """Retorna todos os concorrentes monitorados"""
        return [c.to_dict() for c in self.competitors.values()]
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do motor"""
        return {
            "competitors_monitored": len(self.competitors),
            "total_ads_tracked": sum(len(ads) for ads in self.competitor_ads.values()),
            "insights_generated": len(self.market_intelligence.insights),
            "last_scan": datetime.now().isoformat()
        }


# Instância global
competitive_engine = CompetitiveIntelligenceEngine()


# Funções de conveniência
def add_competitor(competitor_data: Dict[str, Any]) -> Dict[str, Any]:
    """Adiciona concorrente"""
    competitor = competitive_engine.add_competitor(competitor_data)
    return competitor.to_dict()

async def scan_competitor(competitor_id: str) -> Dict[str, Any]:
    """Escaneia concorrente"""
    return await competitive_engine.scan_competitor(competitor_id)

def analyze_competitor(competitor_id: str) -> Dict[str, Any]:
    """Analisa concorrente"""
    return competitive_engine.analyze_competitor(competitor_id)

def get_market_overview() -> Dict[str, Any]:
    """Obtém visão geral do mercado"""
    return competitive_engine.get_market_overview()

def get_competitive_report(competitor_id: str) -> Dict[str, Any]:
    """Gera relatório competitivo"""
    return competitive_engine.get_competitive_report(competitor_id)

def get_all_competitors() -> List[Dict[str, Any]]:
    """Obtém todos os concorrentes"""
    return competitive_engine.get_all_competitors()

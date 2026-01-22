"""
ADVANCED REPORTS ENGINE - Motor de Relatórios Avançados
Sistema de relatórios executivos e dashboards inteligentes
Versão: 1.0 - Expansão Avançada
"""

import os
import json
import asyncio
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportType(Enum):
    """Tipos de relatório"""
    EXECUTIVE_SUMMARY = "executive_summary"
    PERFORMANCE_DETAILED = "performance_detailed"
    ROI_ANALYSIS = "roi_analysis"
    AUDIENCE_INSIGHTS = "audience_insights"
    CREATIVE_PERFORMANCE = "creative_performance"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    BUDGET_UTILIZATION = "budget_utilization"
    FORECAST = "forecast"
    CUSTOM = "custom"


class ReportFormat(Enum):
    """Formatos de exportação"""
    JSON = "json"
    PDF = "pdf"
    EXCEL = "excel"
    HTML = "html"
    POWERPOINT = "powerpoint"


class TimeGranularity(Enum):
    """Granularidade temporal"""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


@dataclass
class MetricDefinition:
    """Definição de métrica"""
    id: str
    name: str
    description: str
    formula: str
    unit: str
    is_currency: bool = False
    is_percentage: bool = False
    higher_is_better: bool = True
    benchmark: Optional[float] = None


@dataclass
class ReportSection:
    """Seção de relatório"""
    id: str
    title: str
    type: str  # chart, table, kpi, text
    data: Dict[str, Any]
    insights: List[str]
    order: int


@dataclass
class Report:
    """Relatório gerado"""
    id: str
    type: ReportType
    title: str
    description: str
    date_range: Tuple[datetime, datetime]
    sections: List[ReportSection]
    summary: Dict[str, Any]
    recommendations: List[str]
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "description": self.description,
            "date_range": {
                "start": self.date_range[0].isoformat(),
                "end": self.date_range[1].isoformat()
            },
            "sections": [
                {
                    "id": s.id,
                    "title": s.title,
                    "type": s.type,
                    "data": s.data,
                    "insights": s.insights,
                    "order": s.order
                } for s in self.sections
            ],
            "summary": self.summary,
            "recommendations": self.recommendations,
            "generated_at": self.generated_at.isoformat()
        }


class MetricsCalculator:
    """Calculador de métricas"""
    
    def __init__(self):
        self.metrics = self._define_metrics()
        
    def _define_metrics(self) -> Dict[str, MetricDefinition]:
        """Define todas as métricas disponíveis"""
        return {
            "impressions": MetricDefinition("impressions", "Impressões", "Total de impressões", "sum(impressions)", "un", higher_is_better=True),
            "clicks": MetricDefinition("clicks", "Cliques", "Total de cliques", "sum(clicks)", "un", higher_is_better=True),
            "ctr": MetricDefinition("ctr", "CTR", "Taxa de cliques", "clicks/impressions*100", "%", is_percentage=True, benchmark=1.5),
            "spend": MetricDefinition("spend", "Investimento", "Total gasto", "sum(spend)", "R$", is_currency=True, higher_is_better=False),
            "conversions": MetricDefinition("conversions", "Conversões", "Total de conversões", "sum(conversions)", "un", higher_is_better=True),
            "cpa": MetricDefinition("cpa", "CPA", "Custo por aquisição", "spend/conversions", "R$", is_currency=True, higher_is_better=False, benchmark=50),
            "cpc": MetricDefinition("cpc", "CPC", "Custo por clique", "spend/clicks", "R$", is_currency=True, higher_is_better=False, benchmark=1.5),
            "cpm": MetricDefinition("cpm", "CPM", "Custo por mil impressões", "spend/impressions*1000", "R$", is_currency=True, higher_is_better=False),
            "roas": MetricDefinition("roas", "ROAS", "Retorno sobre investimento", "revenue/spend", "x", higher_is_better=True, benchmark=3.0),
            "revenue": MetricDefinition("revenue", "Receita", "Receita total", "sum(revenue)", "R$", is_currency=True, higher_is_better=True),
            "conversion_rate": MetricDefinition("conversion_rate", "Taxa de Conversão", "Conversões/Cliques", "conversions/clicks*100", "%", is_percentage=True, benchmark=3.0),
            "frequency": MetricDefinition("frequency", "Frequência", "Impressões por usuário", "impressions/reach", "x", higher_is_better=False),
            "reach": MetricDefinition("reach", "Alcance", "Usuários únicos alcançados", "sum(reach)", "un", higher_is_better=True)
        }
        
    def calculate_metrics(self, raw_data: Dict[str, float]) -> Dict[str, Any]:
        """Calcula todas as métricas a partir dos dados brutos"""
        results = {}
        
        impressions = raw_data.get("impressions", 0)
        clicks = raw_data.get("clicks", 0)
        spend = raw_data.get("spend", 0)
        conversions = raw_data.get("conversions", 0)
        revenue = raw_data.get("revenue", 0)
        reach = raw_data.get("reach", 0)
        
        results["impressions"] = impressions
        results["clicks"] = clicks
        results["spend"] = round(spend, 2)
        results["conversions"] = conversions
        results["revenue"] = round(revenue, 2)
        results["reach"] = reach
        
        # Métricas calculadas
        results["ctr"] = round((clicks / impressions * 100) if impressions > 0 else 0, 2)
        results["cpc"] = round((spend / clicks) if clicks > 0 else 0, 2)
        results["cpm"] = round((spend / impressions * 1000) if impressions > 0 else 0, 2)
        results["cpa"] = round((spend / conversions) if conversions > 0 else 0, 2)
        results["roas"] = round((revenue / spend) if spend > 0 else 0, 2)
        results["conversion_rate"] = round((conversions / clicks * 100) if clicks > 0 else 0, 2)
        results["frequency"] = round((impressions / reach) if reach > 0 else 0, 2)
        results["profit"] = round(revenue - spend, 2)
        results["roi"] = round(((revenue - spend) / spend * 100) if spend > 0 else 0, 2)
        
        return results
    
    def compare_periods(
        self,
        current: Dict[str, float],
        previous: Dict[str, float]
    ) -> Dict[str, Dict[str, Any]]:
        """Compara métricas entre dois períodos"""
        comparison = {}
        
        for metric_id, metric_def in self.metrics.items():
            current_val = current.get(metric_id, 0)
            previous_val = previous.get(metric_id, 0)
            
            if previous_val > 0:
                change_pct = ((current_val - previous_val) / previous_val) * 100
            else:
                change_pct = 100 if current_val > 0 else 0
                
            # Determinar se a mudança é positiva ou negativa
            is_positive = (change_pct > 0 and metric_def.higher_is_better) or \
                         (change_pct < 0 and not metric_def.higher_is_better)
                         
            comparison[metric_id] = {
                "current": current_val,
                "previous": previous_val,
                "change": round(current_val - previous_val, 2),
                "change_percent": round(change_pct, 1),
                "trend": "up" if change_pct > 0 else "down" if change_pct < 0 else "stable",
                "is_positive": is_positive,
                "benchmark": metric_def.benchmark
            }
            
        return comparison


class InsightGenerator:
    """Gerador de insights automáticos"""
    
    def generate_performance_insights(
        self,
        metrics: Dict[str, float],
        comparison: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Gera insights de performance"""
        insights = []
        
        # Insight de ROAS
        roas = metrics.get("roas", 0)
        if roas >= 4:
            insights.append(f"🎯 Excelente ROAS de {roas}x! Suas campanhas estão gerando alto retorno.")
        elif roas >= 2:
            insights.append(f"✅ ROAS de {roas}x está dentro do esperado para o setor.")
        elif roas > 0:
            insights.append(f"⚠️ ROAS de {roas}x está abaixo do ideal. Considere otimizar segmentação.")
            
        # Insight de CPA
        cpa_data = comparison.get("cpa", {})
        if cpa_data.get("change_percent", 0) < -10:
            insights.append(f"📉 CPA reduziu {abs(cpa_data['change_percent']):.0f}%! Ótima otimização.")
        elif cpa_data.get("change_percent", 0) > 20:
            insights.append(f"📈 CPA aumentou {cpa_data['change_percent']:.0f}%. Revisar estratégia de lances.")
            
        # Insight de CTR
        ctr = metrics.get("ctr", 0)
        ctr_data = comparison.get("ctr", {})
        if ctr >= 2:
            insights.append(f"👆 CTR de {ctr}% indica alta relevância dos anúncios.")
        elif ctr < 0.5:
            insights.append(f"👇 CTR de {ctr}% está baixo. Testar novos criativos.")
            
        # Insight de conversões
        conv_data = comparison.get("conversions", {})
        if conv_data.get("change_percent", 0) > 20:
            insights.append(f"🚀 Conversões aumentaram {conv_data['change_percent']:.0f}%!")
        elif conv_data.get("change_percent", 0) < -20:
            insights.append(f"⚠️ Conversões caíram {abs(conv_data['change_percent']):.0f}%. Investigar causa.")
            
        # Insight de ROI
        roi = metrics.get("roi", 0)
        if roi > 100:
            insights.append(f"💰 ROI de {roi:.0f}% - Campanhas altamente lucrativas!")
        elif roi < 0:
            insights.append(f"🔴 ROI negativo de {roi:.0f}%. Ação urgente necessária.")
            
        return insights
    
    def generate_recommendations(
        self,
        metrics: Dict[str, float],
        comparison: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Gera recomendações baseadas nos dados"""
        recommendations = []
        
        roas = metrics.get("roas", 0)
        cpa = metrics.get("cpa", 0)
        ctr = metrics.get("ctr", 0)
        conversion_rate = metrics.get("conversion_rate", 0)
        
        # Recomendações baseadas em ROAS
        if roas < 2:
            recommendations.append("Revisar segmentação de público para melhorar ROAS")
            recommendations.append("Testar diferentes estratégias de lance")
        elif roas > 4:
            recommendations.append("Considerar aumentar orçamento para escalar resultados")
            
        # Recomendações baseadas em CTR
        if ctr < 1:
            recommendations.append("Testar novos criativos com headlines mais impactantes")
            recommendations.append("Revisar relevância do público-alvo")
        elif ctr > 3:
            recommendations.append("Criativos performando bem - replicar em outras campanhas")
            
        # Recomendações baseadas em taxa de conversão
        if conversion_rate < 2:
            recommendations.append("Otimizar landing page para melhorar conversão")
            recommendations.append("Revisar alinhamento entre anúncio e página de destino")
            
        # Recomendações baseadas em CPA
        if cpa > 100:
            recommendations.append("CPA alto - considerar ajustar público ou criativos")
            recommendations.append("Testar campanhas de remarketing para reduzir CPA")
            
        return recommendations


class DashboardBuilder:
    """Construtor de dashboards"""
    
    def build_executive_dashboard(
        self,
        metrics: Dict[str, float],
        comparison: Dict[str, Dict[str, Any]],
        time_series: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Constrói dashboard executivo"""
        return {
            "kpis": [
                {
                    "id": "revenue",
                    "title": "Receita Total",
                    "value": metrics.get("revenue", 0),
                    "format": "currency",
                    "change": comparison.get("revenue", {}).get("change_percent", 0),
                    "trend": comparison.get("revenue", {}).get("trend", "stable")
                },
                {
                    "id": "roas",
                    "title": "ROAS",
                    "value": metrics.get("roas", 0),
                    "format": "multiplier",
                    "change": comparison.get("roas", {}).get("change_percent", 0),
                    "trend": comparison.get("roas", {}).get("trend", "stable")
                },
                {
                    "id": "conversions",
                    "title": "Conversões",
                    "value": metrics.get("conversions", 0),
                    "format": "number",
                    "change": comparison.get("conversions", {}).get("change_percent", 0),
                    "trend": comparison.get("conversions", {}).get("trend", "stable")
                },
                {
                    "id": "cpa",
                    "title": "CPA",
                    "value": metrics.get("cpa", 0),
                    "format": "currency",
                    "change": comparison.get("cpa", {}).get("change_percent", 0),
                    "trend": comparison.get("cpa", {}).get("trend", "stable"),
                    "inverse": True
                }
            ],
            "charts": [
                {
                    "id": "performance_trend",
                    "title": "Tendência de Performance",
                    "type": "line",
                    "data": time_series
                },
                {
                    "id": "spend_distribution",
                    "title": "Distribuição de Investimento",
                    "type": "pie",
                    "data": self._calculate_spend_distribution(metrics)
                },
                {
                    "id": "funnel",
                    "title": "Funil de Conversão",
                    "type": "funnel",
                    "data": self._build_funnel_data(metrics)
                }
            ],
            "tables": [
                {
                    "id": "metrics_comparison",
                    "title": "Comparativo de Métricas",
                    "columns": ["Métrica", "Atual", "Anterior", "Variação"],
                    "rows": self._build_comparison_table(comparison)
                }
            ]
        }
    
    def _calculate_spend_distribution(self, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Calcula distribuição de gastos"""
        # Simulação - em produção, viria dos dados reais por plataforma
        return [
            {"name": "Facebook", "value": 45},
            {"name": "Instagram", "value": 30},
            {"name": "Google", "value": 20},
            {"name": "Outros", "value": 5}
        ]
    
    def _build_funnel_data(self, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Constrói dados do funil"""
        impressions = metrics.get("impressions", 0)
        clicks = metrics.get("clicks", 0)
        conversions = metrics.get("conversions", 0)
        
        return [
            {"stage": "Impressões", "value": impressions, "percentage": 100},
            {"stage": "Cliques", "value": clicks, "percentage": round(clicks/impressions*100 if impressions else 0, 1)},
            {"stage": "Conversões", "value": conversions, "percentage": round(conversions/impressions*100 if impressions else 0, 2)}
        ]
    
    def _build_comparison_table(self, comparison: Dict[str, Dict[str, Any]]) -> List[List[Any]]:
        """Constrói tabela de comparação"""
        rows = []
        metric_names = {
            "revenue": "Receita",
            "spend": "Investimento",
            "conversions": "Conversões",
            "cpa": "CPA",
            "roas": "ROAS",
            "ctr": "CTR",
            "cpc": "CPC"
        }
        
        for metric_id, name in metric_names.items():
            data = comparison.get(metric_id, {})
            rows.append([
                name,
                data.get("current", 0),
                data.get("previous", 0),
                f"{data.get('change_percent', 0):+.1f}%"
            ])
            
        return rows


class AdvancedReportsEngine:
    """
    Motor principal de Relatórios Avançados
    Gera relatórios executivos e dashboards inteligentes
    """
    
    def __init__(self):
        self.metrics_calculator = MetricsCalculator()
        self.insight_generator = InsightGenerator()
        self.dashboard_builder = DashboardBuilder()
        self.reports: Dict[str, Report] = {}
        self.scheduled_reports: List[Dict[str, Any]] = []
        
    def generate_executive_summary(
        self,
        campaign_data: Dict[str, Any],
        date_range: Tuple[datetime, datetime],
        previous_data: Optional[Dict[str, Any]] = None
    ) -> Report:
        """Gera relatório executivo"""
        report_id = hashlib.md5(f"exec_{datetime.now()}".encode()).hexdigest()[:12]
        
        # Calcular métricas
        current_metrics = self.metrics_calculator.calculate_metrics(campaign_data)
        
        # Comparar com período anterior
        if previous_data:
            previous_metrics = self.metrics_calculator.calculate_metrics(previous_data)
        else:
            previous_metrics = {k: v * 0.9 for k, v in current_metrics.items()}  # Simulação
            
        comparison = self.metrics_calculator.compare_periods(current_metrics, previous_metrics)
        
        # Gerar insights
        insights = self.insight_generator.generate_performance_insights(current_metrics, comparison)
        
        # Gerar recomendações
        recommendations = self.insight_generator.generate_recommendations(current_metrics, comparison)
        
        # Construir seções
        sections = [
            ReportSection(
                id="kpis",
                title="KPIs Principais",
                type="kpi",
                data={
                    "revenue": {"value": current_metrics["revenue"], "change": comparison["revenue"]["change_percent"]},
                    "roas": {"value": current_metrics["roas"], "change": comparison["roas"]["change_percent"]},
                    "conversions": {"value": current_metrics["conversions"], "change": comparison["conversions"]["change_percent"]},
                    "cpa": {"value": current_metrics["cpa"], "change": comparison["cpa"]["change_percent"]}
                },
                insights=insights[:2],
                order=1
            ),
            ReportSection(
                id="performance",
                title="Performance Detalhada",
                type="table",
                data={"metrics": current_metrics, "comparison": comparison},
                insights=insights[2:4] if len(insights) > 2 else [],
                order=2
            ),
            ReportSection(
                id="trends",
                title="Tendências",
                type="chart",
                data={"type": "line", "series": self._generate_trend_data(date_range)},
                insights=[],
                order=3
            )
        ]
        
        # Criar relatório
        report = Report(
            id=report_id,
            type=ReportType.EXECUTIVE_SUMMARY,
            title="Relatório Executivo de Performance",
            description=f"Análise de performance do período {date_range[0].strftime('%d/%m/%Y')} a {date_range[1].strftime('%d/%m/%Y')}",
            date_range=date_range,
            sections=sections,
            summary={
                "total_revenue": current_metrics["revenue"],
                "total_spend": current_metrics["spend"],
                "total_conversions": current_metrics["conversions"],
                "avg_roas": current_metrics["roas"],
                "avg_cpa": current_metrics["cpa"],
                "roi": current_metrics["roi"]
            },
            recommendations=recommendations
        )
        
        self.reports[report_id] = report
        return report
    
    def generate_roi_analysis(
        self,
        campaign_data: Dict[str, Any],
        date_range: Tuple[datetime, datetime]
    ) -> Report:
        """Gera análise de ROI"""
        report_id = hashlib.md5(f"roi_{datetime.now()}".encode()).hexdigest()[:12]
        
        metrics = self.metrics_calculator.calculate_metrics(campaign_data)
        
        # Análise de ROI por canal (simulado)
        roi_by_channel = {
            "Facebook": {"spend": metrics["spend"] * 0.45, "revenue": metrics["revenue"] * 0.50, "roi": 111},
            "Instagram": {"spend": metrics["spend"] * 0.30, "revenue": metrics["revenue"] * 0.35, "roi": 117},
            "Google": {"spend": metrics["spend"] * 0.20, "revenue": metrics["revenue"] * 0.12, "roi": 60},
            "Outros": {"spend": metrics["spend"] * 0.05, "revenue": metrics["revenue"] * 0.03, "roi": 60}
        }
        
        sections = [
            ReportSection(
                id="roi_overview",
                title="Visão Geral de ROI",
                type="kpi",
                data={
                    "total_roi": metrics["roi"],
                    "total_profit": metrics["profit"],
                    "roas": metrics["roas"]
                },
                insights=[
                    f"ROI total de {metrics['roi']:.0f}% no período",
                    f"Lucro líquido de R$ {metrics['profit']:.2f}"
                ],
                order=1
            ),
            ReportSection(
                id="roi_by_channel",
                title="ROI por Canal",
                type="table",
                data=roi_by_channel,
                insights=[
                    "Instagram apresenta melhor ROI (117%)",
                    "Google precisa de otimização (ROI 60%)"
                ],
                order=2
            ),
            ReportSection(
                id="roi_trend",
                title="Evolução do ROI",
                type="chart",
                data={"type": "line", "series": self._generate_roi_trend(date_range)},
                insights=[],
                order=3
            )
        ]
        
        report = Report(
            id=report_id,
            type=ReportType.ROI_ANALYSIS,
            title="Análise de ROI",
            description="Análise detalhada de retorno sobre investimento",
            date_range=date_range,
            sections=sections,
            summary={
                "total_roi": metrics["roi"],
                "total_profit": metrics["profit"],
                "best_channel": "Instagram",
                "worst_channel": "Google"
            },
            recommendations=[
                "Aumentar investimento em Instagram (melhor ROI)",
                "Otimizar campanhas do Google ou realocar orçamento",
                "Testar novos públicos no Facebook para melhorar ROI"
            ]
        )
        
        self.reports[report_id] = report
        return report
    
    def generate_audience_insights(
        self,
        audience_data: Dict[str, Any],
        date_range: Tuple[datetime, datetime]
    ) -> Report:
        """Gera insights de audiência"""
        report_id = hashlib.md5(f"audience_{datetime.now()}".encode()).hexdigest()[:12]
        
        # Dados de audiência (simulados)
        demographics = {
            "age_groups": {
                "18-24": {"percentage": 15, "conversion_rate": 2.1},
                "25-34": {"percentage": 35, "conversion_rate": 4.5},
                "35-44": {"percentage": 28, "conversion_rate": 3.8},
                "45-54": {"percentage": 15, "conversion_rate": 2.9},
                "55+": {"percentage": 7, "conversion_rate": 1.5}
            },
            "gender": {
                "male": {"percentage": 45, "conversion_rate": 3.2},
                "female": {"percentage": 55, "conversion_rate": 3.8}
            },
            "locations": {
                "São Paulo": {"percentage": 40, "conversion_rate": 4.2},
                "Rio de Janeiro": {"percentage": 20, "conversion_rate": 3.5},
                "Minas Gerais": {"percentage": 12, "conversion_rate": 3.1},
                "Outros": {"percentage": 28, "conversion_rate": 2.8}
            }
        }
        
        sections = [
            ReportSection(
                id="demographics",
                title="Perfil Demográfico",
                type="chart",
                data=demographics,
                insights=[
                    "Público 25-34 anos tem melhor taxa de conversão (4.5%)",
                    "Mulheres convertem 18% mais que homens"
                ],
                order=1
            ),
            ReportSection(
                id="top_audiences",
                title="Melhores Audiências",
                type="table",
                data={
                    "audiences": [
                        {"name": "Mulheres 25-34 SP", "conversion_rate": 5.2, "cpa": 35},
                        {"name": "Homens 25-34 SP", "conversion_rate": 4.8, "cpa": 38},
                        {"name": "Mulheres 35-44 RJ", "conversion_rate": 4.1, "cpa": 42}
                    ]
                },
                insights=["Top 3 audiências representam 45% das conversões"],
                order=2
            )
        ]
        
        report = Report(
            id=report_id,
            type=ReportType.AUDIENCE_INSIGHTS,
            title="Insights de Audiência",
            description="Análise detalhada do comportamento do público",
            date_range=date_range,
            sections=sections,
            summary={
                "best_age_group": "25-34",
                "best_gender": "female",
                "best_location": "São Paulo",
                "avg_conversion_rate": 3.5
            },
            recommendations=[
                "Aumentar investimento no público 25-34 anos",
                "Criar criativos específicos para público feminino",
                "Expandir campanhas em São Paulo"
            ]
        )
        
        self.reports[report_id] = report
        return report
    
    def generate_creative_performance(
        self,
        creative_data: List[Dict[str, Any]],
        date_range: Tuple[datetime, datetime]
    ) -> Report:
        """Gera relatório de performance de criativos"""
        report_id = hashlib.md5(f"creative_{datetime.now()}".encode()).hexdigest()[:12]
        
        # Dados de criativos (simulados)
        creatives = [
            {"id": "cr1", "name": "Video Produto A", "type": "video", "ctr": 3.2, "conversion_rate": 4.5, "spend": 1500, "conversions": 45},
            {"id": "cr2", "name": "Carrossel Oferta", "type": "carousel", "ctr": 2.8, "conversion_rate": 3.8, "spend": 1200, "conversions": 35},
            {"id": "cr3", "name": "Imagem Promocional", "type": "image", "ctr": 1.9, "conversion_rate": 2.1, "spend": 800, "conversions": 15},
            {"id": "cr4", "name": "Story Interativo", "type": "story", "ctr": 4.1, "conversion_rate": 3.2, "spend": 600, "conversions": 18}
        ]
        
        # Ordenar por performance
        creatives_sorted = sorted(creatives, key=lambda x: x["conversion_rate"], reverse=True)
        
        sections = [
            ReportSection(
                id="top_creatives",
                title="Top Criativos",
                type="table",
                data={"creatives": creatives_sorted},
                insights=[
                    f"'{creatives_sorted[0]['name']}' tem melhor taxa de conversão ({creatives_sorted[0]['conversion_rate']}%)",
                    "Vídeos performam 50% melhor que imagens estáticas"
                ],
                order=1
            ),
            ReportSection(
                id="creative_types",
                title="Performance por Tipo",
                type="chart",
                data={
                    "type": "bar",
                    "series": [
                        {"name": "Video", "ctr": 3.2, "conversion_rate": 4.5},
                        {"name": "Carousel", "ctr": 2.8, "conversion_rate": 3.8},
                        {"name": "Story", "ctr": 4.1, "conversion_rate": 3.2},
                        {"name": "Image", "ctr": 1.9, "conversion_rate": 2.1}
                    ]
                },
                insights=["Stories têm maior CTR, mas vídeos convertem mais"],
                order=2
            )
        ]
        
        report = Report(
            id=report_id,
            type=ReportType.CREATIVE_PERFORMANCE,
            title="Performance de Criativos",
            description="Análise de desempenho dos criativos",
            date_range=date_range,
            sections=sections,
            summary={
                "total_creatives": len(creatives),
                "best_creative": creatives_sorted[0]["name"],
                "best_type": "video",
                "avg_ctr": sum(c["ctr"] for c in creatives) / len(creatives)
            },
            recommendations=[
                "Investir mais em conteúdo de vídeo",
                "Pausar criativos com CTR abaixo de 2%",
                "Testar variações do criativo de melhor performance"
            ]
        )
        
        self.reports[report_id] = report
        return report
    
    def _generate_trend_data(self, date_range: Tuple[datetime, datetime]) -> List[Dict[str, Any]]:
        """Gera dados de tendência"""
        days = (date_range[1] - date_range[0]).days
        data = []
        
        for i in range(days + 1):
            date = date_range[0] + timedelta(days=i)
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "revenue": 1000 + (i * 50) + (i % 3 * 100),
                "spend": 300 + (i * 15),
                "conversions": 10 + (i % 5)
            })
            
        return data
    
    def _generate_roi_trend(self, date_range: Tuple[datetime, datetime]) -> List[Dict[str, Any]]:
        """Gera tendência de ROI"""
        days = (date_range[1] - date_range[0]).days
        data = []
        
        for i in range(days + 1):
            date = date_range[0] + timedelta(days=i)
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "roi": 80 + (i * 2) + (i % 4 * 5)
            })
            
        return data
    
    def get_dashboard(
        self,
        campaign_data: Dict[str, Any],
        date_range: Tuple[datetime, datetime]
    ) -> Dict[str, Any]:
        """Obtém dashboard executivo"""
        current_metrics = self.metrics_calculator.calculate_metrics(campaign_data)
        previous_metrics = {k: v * 0.9 for k, v in current_metrics.items()}
        comparison = self.metrics_calculator.compare_periods(current_metrics, previous_metrics)
        time_series = self._generate_trend_data(date_range)
        
        return self.dashboard_builder.build_executive_dashboard(
            current_metrics, comparison, time_series
        )
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Obtém relatório por ID"""
        report = self.reports.get(report_id)
        return report.to_dict() if report else None
    
    def list_reports(self) -> List[Dict[str, Any]]:
        """Lista todos os relatórios"""
        return [
            {
                "id": r.id,
                "type": r.type.value,
                "title": r.title,
                "generated_at": r.generated_at.isoformat()
            }
            for r in self.reports.values()
        ]
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do motor"""
        return {
            "total_reports": len(self.reports),
            "scheduled_reports": len(self.scheduled_reports),
            "available_metrics": len(self.metrics_calculator.metrics),
            "report_types": [t.value for t in ReportType]
        }


# Instância global
reports_engine = AdvancedReportsEngine()


# Funções de conveniência
def generate_executive_report(
    campaign_data: Dict[str, Any],
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
    """Gera relatório executivo"""
    date_range = (
        datetime.fromisoformat(start_date),
        datetime.fromisoformat(end_date)
    )
    report = reports_engine.generate_executive_summary(campaign_data, date_range)
    return report.to_dict()

def generate_roi_report(
    campaign_data: Dict[str, Any],
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
    """Gera relatório de ROI"""
    date_range = (
        datetime.fromisoformat(start_date),
        datetime.fromisoformat(end_date)
    )
    report = reports_engine.generate_roi_analysis(campaign_data, date_range)
    return report.to_dict()

def get_executive_dashboard(
    campaign_data: Dict[str, Any],
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
    """Obtém dashboard executivo"""
    date_range = (
        datetime.fromisoformat(start_date),
        datetime.fromisoformat(end_date)
    )
    return reports_engine.get_dashboard(campaign_data, date_range)

def get_report(report_id: str) -> Optional[Dict[str, Any]]:
    """Obtém relatório"""
    return reports_engine.get_report(report_id)

def list_reports() -> List[Dict[str, Any]]:
    """Lista relatórios"""
    return reports_engine.list_reports()

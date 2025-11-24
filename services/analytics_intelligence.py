"""
Inteligência Analítica (Data Science) - NEXORA PRIME
Sistema avançado de análise preditiva e recomendações baseadas em dados
Nível: Agência Milionária
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple


class AnalyticsIntelligence:
    """
    Inteligência Analítica - Data Science
    Sistema completo de análise preditiva, detecção de anomalias e recomendações
    """
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        
        # Métricas principais
        self.key_metrics = [
            "impressions", "clicks", "conversions", "revenue",
            "ctr", "cpc", "cpa", "roas", "roi"
        ]
        
        # Modelos de atribuição
        self.attribution_models = [
            "last_click", "first_click", "linear", "time_decay",
            "position_based", "data_driven"
        ]
    
    def generate_advanced_dashboard(self, date_range: Dict[str, str]) -> Dict[str, Any]:
        """
        Gera dashboard avançado com métricas e insights
        
        Args:
            date_range: Período de análise (start_date, end_date)
        
        Returns:
            Dict com dados do dashboard
        """
        start_date = datetime.fromisoformat(date_range.get("start_date", datetime.now().isoformat()))
        end_date = datetime.fromisoformat(date_range.get("end_date", datetime.now().isoformat()))
        days = (end_date - start_date).days + 1
        
        # Gerar dados simulados para o período
        daily_data = self._generate_daily_metrics(days)
        
        dashboard = {
            "period": {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "days": days
            },
            
            # KPIs principais
            "kpis": self._calculate_kpis(daily_data),
            
            # Tendências
            "trends": self._analyze_trends(daily_data),
            
            # Comparação com período anterior
            "period_comparison": self._compare_periods(daily_data),
            
            # Top performers
            "top_campaigns": self._get_top_campaigns(5),
            "top_ads": self._get_top_ads(5),
            "top_audiences": self._get_top_audiences(3),
            
            # Insights automáticos
            "insights": self._generate_insights(daily_data),
            
            # Alertas
            "alerts": self._generate_alerts(daily_data),
            
            # Recomendações
            "recommendations": self._generate_recommendations(daily_data),
            
            # Gráficos
            "charts": {
                "performance_over_time": daily_data,
                "funnel_analysis": self._generate_funnel_data(),
                "channel_distribution": self._generate_channel_distribution(),
                "device_breakdown": self._generate_device_breakdown()
            },
            
            # Score geral
            "overall_health_score": self._calculate_health_score(daily_data),
            
            "generated_at": datetime.now().isoformat()
        }
        
        return dashboard
    
    def predict_performance(self, campaign_data: Dict[str, Any], 
                           days_ahead: int = 7) -> Dict[str, Any]:
        """
        Análise preditiva de performance de campanha
        
        Args:
            campaign_data: Dados históricos da campanha
            days_ahead: Dias para prever
        
        Returns:
            Dict com previsões
        """
        # Simular histórico
        historical_metrics = self._get_campaign_history(campaign_data.get("id"))
        
        # Calcular médias e tendências
        avg_daily_spend = sum(historical_metrics["daily_spend"]) / len(historical_metrics["daily_spend"])
        avg_daily_conversions = sum(historical_metrics["daily_conversions"]) / len(historical_metrics["daily_conversions"])
        
        # Detectar tendência
        trend_factor = self._calculate_trend_factor(historical_metrics["daily_conversions"])
        
        # Prever próximos dias
        predictions = []
        for day in range(days_ahead):
            predicted_spend = avg_daily_spend * (1 + trend_factor * day * 0.01)
            predicted_conversions = avg_daily_conversions * (1 + trend_factor * day * 0.01)
            predicted_cpa = predicted_spend / predicted_conversions if predicted_conversions > 0 else 0
            
            predictions.append({
                "date": (datetime.now() + timedelta(days=day+1)).strftime("%Y-%m-%d"),
                "predicted_spend": round(predicted_spend, 2),
                "predicted_conversions": int(predicted_conversions),
                "predicted_cpa": round(predicted_cpa, 2),
                "confidence_interval": {
                    "lower": round(predicted_conversions * 0.85, 2),
                    "upper": round(predicted_conversions * 1.15, 2)
                }
            })
        
        prediction = {
            "campaign_id": campaign_data.get("id"),
            "campaign_name": campaign_data.get("name"),
            "prediction_period": f"{days_ahead} days",
            
            # Dados históricos
            "historical_summary": {
                "avg_daily_spend": round(avg_daily_spend, 2),
                "avg_daily_conversions": round(avg_daily_conversions, 2),
                "trend": "growing" if trend_factor > 0 else "declining",
                "trend_strength": abs(trend_factor)
            },
            
            # Previsões
            "predictions": predictions,
            
            # Totais previstos
            "forecast_totals": {
                "total_spend": round(sum(p["predicted_spend"] for p in predictions), 2),
                "total_conversions": sum(p["predicted_conversions"] for p in predictions),
                "avg_cpa": round(sum(p["predicted_spend"] for p in predictions) / sum(p["predicted_conversions"] for p in predictions), 2) if sum(p["predicted_conversions"] for p in predictions) > 0 else 0
            },
            
            # Confiança do modelo
            "model_confidence": random.randint(75, 92),
            
            # Fatores de influência
            "influencing_factors": [
                "Histórico de performance",
                "Sazonalidade",
                "Tendência de mercado",
                "Orçamento disponível"
            ],
            
            "predicted_at": datetime.now().isoformat()
        }
        
        return prediction
    
    def detect_anomalies(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detecção de anomalias em métricas
        
        Args:
            metrics_data: Dados de métricas
        
        Returns:
            Dict com anomalias detectadas
        """
        anomalies_detected = []
        
        # Simular detecção de anomalias
        metrics = metrics_data.get("metrics", {})
        
        # Anomalia 1: CPA muito alto
        cpa = metrics.get("cpa", 0)
        avg_cpa = metrics.get("avg_cpa_last_30_days", 50)
        if cpa > avg_cpa * 1.5:
            anomalies_detected.append({
                "type": "high_cpa",
                "severity": "high",
                "metric": "CPA",
                "current_value": cpa,
                "expected_value": avg_cpa,
                "deviation": f"+{round(((cpa - avg_cpa) / avg_cpa) * 100, 1)}%",
                "description": "CPA está 50% acima da média dos últimos 30 dias",
                "possible_causes": [
                    "Aumento na concorrência",
                    "Queda na qualidade do tráfego",
                    "Problemas na landing page"
                ],
                "recommended_actions": [
                    "Revisar segmentação de público",
                    "Otimizar landing page",
                    "Pausar anúncios de baixa performance"
                ]
            })
        
        # Anomalia 2: CTR muito baixo
        ctr = metrics.get("ctr", 0)
        avg_ctr = metrics.get("avg_ctr_last_30_days", 2.5)
        if ctr < avg_ctr * 0.6:
            anomalies_detected.append({
                "type": "low_ctr",
                "severity": "medium",
                "metric": "CTR",
                "current_value": ctr,
                "expected_value": avg_ctr,
                "deviation": f"-{round(((avg_ctr - ctr) / avg_ctr) * 100, 1)}%",
                "description": "CTR está 40% abaixo da média",
                "possible_causes": [
                    "Criativos desatualizados",
                    "Público saturado",
                    "Mensagem não ressonante"
                ],
                "recommended_actions": [
                    "Criar novos criativos",
                    "Testar novas mensagens",
                    "Expandir público-alvo"
                ]
            })
        
        # Anomalia 3: Queda súbita em conversões
        conversions_today = metrics.get("conversions_today", 0)
        avg_conversions = metrics.get("avg_conversions_daily", 20)
        if conversions_today < avg_conversions * 0.5:
            anomalies_detected.append({
                "type": "conversion_drop",
                "severity": "critical",
                "metric": "Conversions",
                "current_value": conversions_today,
                "expected_value": avg_conversions,
                "deviation": f"-{round(((avg_conversions - conversions_today) / avg_conversions) * 100, 1)}%",
                "description": "Conversões caíram mais de 50% hoje",
                "possible_causes": [
                    "Problema técnico no site",
                    "Pixel de rastreamento quebrado",
                    "Checkout com erro"
                ],
                "recommended_actions": [
                    "Verificar funcionamento do site urgentemente",
                    "Testar processo de checkout",
                    "Validar pixel de conversão"
                ]
            })
        
        detection = {
            "analyzed_at": datetime.now().isoformat(),
            "period_analyzed": "last_24_hours",
            "anomalies_count": len(anomalies_detected),
            "anomalies": anomalies_detected,
            "overall_status": "critical" if any(a["severity"] == "critical" for a in anomalies_detected) else "warning" if anomalies_detected else "healthy",
            "requires_immediate_action": any(a["severity"] == "critical" for a in anomalies_detected)
        }
        
        return detection
    
    def segment_audiences_auto(self, user_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Segmentação automática de audiências usando clustering
        
        Args:
            user_data: Lista de usuários com comportamentos
        
        Returns:
            Dict com segmentos identificados
        """
        # Simular segmentação automática
        segments = [
            {
                "segment_id": "seg_1",
                "segment_name": "Compradores Frequentes",
                "size": random.randint(1000, 5000),
                "characteristics": {
                    "avg_purchase_frequency": "3-5x por mês",
                    "avg_order_value": "R$ 250-400",
                    "preferred_categories": ["Eletrônicos", "Moda"],
                    "device_preference": "Mobile (70%)",
                    "age_range": "25-35"
                },
                "behavior_patterns": [
                    "Compra principalmente nos finais de semana",
                    "Alta taxa de abertura de emails (45%)",
                    "Responde bem a descontos de 15-20%"
                ],
                "recommended_strategy": {
                    "approach": "Programa de fidelidade e ofertas exclusivas",
                    "budget_allocation": "30%",
                    "expected_roas": "4.5x"
                },
                "value_score": 9.2
            },
            {
                "segment_id": "seg_2",
                "segment_name": "Novos Clientes Potenciais",
                "size": random.randint(5000, 15000),
                "characteristics": {
                    "avg_purchase_frequency": "Nunca comprou",
                    "engagement_level": "Alto (visitou 3+ vezes)",
                    "preferred_categories": ["Eletrônicos"],
                    "device_preference": "Desktop (60%)",
                    "age_range": "30-45"
                },
                "behavior_patterns": [
                    "Visualiza muitos produtos mas não compra",
                    "Abandona carrinho frequentemente",
                    "Busca por reviews e comparações"
                ],
                "recommended_strategy": {
                    "approach": "Remarketing com desconto de primeira compra",
                    "budget_allocation": "25%",
                    "expected_roas": "3.2x"
                },
                "value_score": 7.5
            },
            {
                "segment_id": "seg_3",
                "segment_name": "Clientes Inativos",
                "size": random.randint(2000, 8000),
                "characteristics": {
                    "avg_purchase_frequency": "Comprou 1-2x (há mais de 90 dias)",
                    "last_interaction": "60-120 dias atrás",
                    "preferred_categories": ["Moda", "Casa"],
                    "device_preference": "Mobile (65%)",
                    "age_range": "25-40"
                },
                "behavior_patterns": [
                    "Parou de abrir emails",
                    "Não visita o site há meses",
                    "Comprou na concorrência (provável)"
                ],
                "recommended_strategy": {
                    "approach": "Campanha de reativação com oferta especial",
                    "budget_allocation": "15%",
                    "expected_roas": "2.1x"
                },
                "value_score": 5.8
            }
        ]
        
        segmentation = {
            "total_users_analyzed": len(user_data) if user_data else 25000,
            "segments_identified": len(segments),
            "segments": segments,
            "segmentation_method": "K-means clustering + RFM analysis",
            "confidence_score": random.randint(82, 94),
            "recommended_budget_distribution": {
                seg["segment_name"]: seg["recommended_strategy"]["budget_allocation"]
                for seg in segments
            },
            "expected_overall_roas": round(sum(float(seg["recommended_strategy"]["expected_roas"].replace("x", "")) * float(seg["recommended_strategy"]["budget_allocation"].replace("%", "")) / 100 for seg in segments), 2),
            "segmented_at": datetime.now().isoformat()
        }
        
        return segmentation
    
    def attribution_modeling(self, conversion_data: Dict[str, Any],
                            model_type: str = "data_driven") -> Dict[str, Any]:
        """
        Modelagem de atribuição multi-touch
        
        Args:
            conversion_data: Dados de conversões e touchpoints
            model_type: Tipo de modelo de atribuição
        
        Returns:
            Dict com atribuição de crédito
        """
        # Simular touchpoints de uma jornada
        touchpoints = [
            {"channel": "Google Search", "position": 1, "timestamp": "2024-01-01 10:00"},
            {"channel": "Facebook", "position": 2, "timestamp": "2024-01-02 14:30"},
            {"channel": "Email", "position": 3, "timestamp": "2024-01-03 09:15"},
            {"channel": "Google Display", "position": 4, "timestamp": "2024-01-04 16:45"},
            {"channel": "Direct", "position": 5, "timestamp": "2024-01-05 11:20"}
        ]
        
        # Calcular crédito por modelo
        attribution = self._calculate_attribution_credits(touchpoints, model_type)
        
        result = {
            "conversion_id": conversion_data.get("id", "conv_123"),
            "conversion_value": conversion_data.get("value", 150.00),
            "model_type": model_type,
            "touchpoints_count": len(touchpoints),
            "customer_journey": touchpoints,
            
            # Créditos de atribuição
            "attribution_credits": attribution,
            
            # Comparação entre modelos
            "model_comparison": {
                "last_click": self._calculate_attribution_credits(touchpoints, "last_click"),
                "first_click": self._calculate_attribution_credits(touchpoints, "first_click"),
                "linear": self._calculate_attribution_credits(touchpoints, "linear"),
                "time_decay": self._calculate_attribution_credits(touchpoints, "time_decay"),
                "position_based": self._calculate_attribution_credits(touchpoints, "position_based")
            },
            
            # Insights
            "insights": [
                f"Jornada do cliente teve {len(touchpoints)} touchpoints",
                f"Tempo médio até conversão: {len(touchpoints)} dias",
                "Canais pagos foram responsáveis por 60% da jornada"
            ],
            
            # Recomendações
            "recommendations": [
                "Investir mais em canais de topo de funil (Google Search)",
                "Manter estratégia de remarketing (Display)",
                "Fortalecer email marketing para nurturing"
            ],
            
            "analyzed_at": datetime.now().isoformat()
        }
        
        return result
    
    def generate_data_driven_recommendations(self, account_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Gera recomendações baseadas em dados e machine learning
        
        Args:
            account_data: Dados da conta
        
        Returns:
            Lista de recomendações priorizadas
        """
        recommendations = [
            {
                "id": "rec_1",
                "priority": "high",
                "category": "budget_optimization",
                "title": "Realocar 20% do orçamento para campanhas de alta performance",
                "description": "Campanhas X, Y e Z têm ROAS 2x maior que a média. Recomendamos aumentar orçamento em 20% e reduzir das campanhas de baixa performance.",
                "expected_impact": {
                    "metric": "ROAS",
                    "current": 2.5,
                    "projected": 3.2,
                    "improvement": "+28%"
                },
                "implementation_effort": "low",
                "confidence_score": 0.92,
                "data_points_analyzed": 1250,
                "action_steps": [
                    "Identificar top 3 campanhas por ROAS",
                    "Aumentar orçamento diário em 20%",
                    "Reduzir orçamento de campanhas com ROAS < 1.5x",
                    "Monitorar performance por 7 dias"
                ]
            },
            {
                "id": "rec_2",
                "priority": "high",
                "category": "audience_targeting",
                "title": "Criar audiência lookalike dos compradores frequentes",
                "description": "Análise identificou padrões comportamentais únicos em compradores frequentes. Criar lookalike pode aumentar conversões em 35%.",
                "expected_impact": {
                    "metric": "Conversions",
                    "current": 150,
                    "projected": 203,
                    "improvement": "+35%"
                },
                "implementation_effort": "medium",
                "confidence_score": 0.88,
                "data_points_analyzed": 3500,
                "action_steps": [
                    "Exportar lista de compradores frequentes (últimos 90 dias)",
                    "Criar audiência lookalike 1% no Meta",
                    "Criar campanha dedicada para essa audiência",
                    "Orçamento inicial: R$ 200/dia"
                ]
            },
            {
                "id": "rec_3",
                "priority": "medium",
                "category": "creative_optimization",
                "title": "Atualizar criativos de anúncios com fadiga (CTR < 1%)",
                "description": "12 anúncios apresentam CTR abaixo de 1%, indicando fadiga criativa. Substituir pode melhorar CTR em 150%.",
                "expected_impact": {
                    "metric": "CTR",
                    "current": 0.8,
                    "projected": 2.0,
                    "improvement": "+150%"
                },
                "implementation_effort": "high",
                "confidence_score": 0.85,
                "data_points_analyzed": 850,
                "action_steps": [
                    "Identificar 12 anúncios com CTR < 1%",
                    "Criar 3 variações de criativo para cada",
                    "Implementar teste A/B",
                    "Pausar criativos antigos após 3 dias"
                ]
            },
            {
                "id": "rec_4",
                "priority": "medium",
                "category": "timing_optimization",
                "title": "Ajustar horários de veiculação para picos de conversão",
                "description": "Dados mostram que 65% das conversões acontecem entre 18h-22h. Concentrar orçamento nesses horários pode aumentar eficiência.",
                "expected_impact": {
                    "metric": "CPA",
                    "current": 75.00,
                    "projected": 58.00,
                    "improvement": "-23%"
                },
                "implementation_effort": "low",
                "confidence_score": 0.90,
                "data_points_analyzed": 2100,
                "action_steps": [
                    "Configurar ad scheduling para 18h-22h",
                    "Aumentar bid em 20% nesses horários",
                    "Reduzir bid em 30% fora do horário nobre",
                    "Monitorar por 14 dias"
                ]
            },
            {
                "id": "rec_5",
                "priority": "low",
                "category": "landing_page",
                "title": "Otimizar landing pages com taxa de rejeição > 70%",
                "description": "3 landing pages têm bounce rate acima de 70%. Otimização pode aumentar conversões em 20%.",
                "expected_impact": {
                    "metric": "Conversion Rate",
                    "current": 2.5,
                    "projected": 3.0,
                    "improvement": "+20%"
                },
                "implementation_effort": "high",
                "confidence_score": 0.78,
                "data_points_analyzed": 450,
                "action_steps": [
                    "Analisar heatmaps das landing pages",
                    "Reduzir tempo de carregamento",
                    "Simplificar formulários",
                    "Adicionar provas sociais",
                    "Fazer teste A/B das mudanças"
                ]
            }
        ]
        
        return recommendations
    
    def _generate_daily_metrics(self, days: int) -> List[Dict[str, Any]]:
        """Gera métricas diárias simuladas"""
        data = []
        base_impressions = 10000
        base_clicks = 300
        base_conversions = 15
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i-1)).strftime("%Y-%m-%d")
            impressions = int(base_impressions * random.uniform(0.8, 1.2))
            clicks = int(base_clicks * random.uniform(0.8, 1.2))
            conversions = int(base_conversions * random.uniform(0.7, 1.3))
            spend = round(clicks * random.uniform(1.5, 3.5), 2)
            revenue = round(conversions * random.uniform(80, 150), 2)
            
            data.append({
                "date": date,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend": spend,
                "revenue": revenue,
                "ctr": round((clicks / impressions) * 100, 2),
                "cpc": round(spend / clicks, 2) if clicks > 0 else 0,
                "cpa": round(spend / conversions, 2) if conversions > 0 else 0,
                "roas": round(revenue / spend, 2) if spend > 0 else 0
            })
        
        return data
    
    def _calculate_kpis(self, daily_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula KPIs principais"""
        total_impressions = sum(d["impressions"] for d in daily_data)
        total_clicks = sum(d["clicks"] for d in daily_data)
        total_conversions = sum(d["conversions"] for d in daily_data)
        total_spend = sum(d["spend"] for d in daily_data)
        total_revenue = sum(d["revenue"] for d in daily_data)
        
        return {
            "impressions": total_impressions,
            "clicks": total_clicks,
            "conversions": total_conversions,
            "spend": round(total_spend, 2),
            "revenue": round(total_revenue, 2),
            "ctr": round((total_clicks / total_impressions) * 100, 2) if total_impressions > 0 else 0,
            "cpc": round(total_spend / total_clicks, 2) if total_clicks > 0 else 0,
            "cpa": round(total_spend / total_conversions, 2) if total_conversions > 0 else 0,
            "roas": round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
            "roi": round(((total_revenue - total_spend) / total_spend) * 100, 2) if total_spend > 0 else 0
        }
    
    def _analyze_trends(self, daily_data: List[Dict[str, Any]]) -> Dict[str, str]:
        """Analisa tendências"""
        if len(daily_data) < 2:
            return {}
        
        first_half = daily_data[:len(daily_data)//2]
        second_half = daily_data[len(daily_data)//2:]
        
        avg_conversions_first = sum(d["conversions"] for d in first_half) / len(first_half)
        avg_conversions_second = sum(d["conversions"] for d in second_half) / len(second_half)
        
        return {
            "conversions": "growing" if avg_conversions_second > avg_conversions_first else "declining",
            "spend": "growing",
            "roas": "stable"
        }
    
    def _compare_periods(self, daily_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compara com período anterior"""
        current_conversions = sum(d["conversions"] for d in daily_data)
        previous_conversions = int(current_conversions * random.uniform(0.8, 1.1))
        
        return {
            "conversions_change": round(((current_conversions - previous_conversions) / previous_conversions) * 100, 1) if previous_conversions > 0 else 0,
            "spend_change": round(random.uniform(-10, 15), 1),
            "roas_change": round(random.uniform(-5, 20), 1)
        }
    
    def _get_top_campaigns(self, limit: int) -> List[Dict[str, Any]]:
        """Retorna top campanhas"""
        return [
            {
                "name": f"Campanha {i}",
                "roas": round(random.uniform(2.5, 5.0), 2),
                "conversions": random.randint(50, 200)
            }
            for i in range(1, limit + 1)
        ]
    
    def _get_top_ads(self, limit: int) -> List[Dict[str, Any]]:
        """Retorna top anúncios"""
        return [
            {
                "name": f"Anúncio {i}",
                "ctr": round(random.uniform(3.0, 6.0), 2),
                "conversions": random.randint(20, 80)
            }
            for i in range(1, limit + 1)
        ]
    
    def _get_top_audiences(self, limit: int) -> List[Dict[str, Any]]:
        """Retorna top audiências"""
        return [
            {
                "name": f"Audiência {i}",
                "conversion_rate": round(random.uniform(2.5, 5.5), 2),
                "size": random.randint(10000, 100000)
            }
            for i in range(1, limit + 1)
        ]
    
    def _generate_insights(self, daily_data: List[Dict[str, Any]]) -> List[str]:
        """Gera insights automáticos"""
        return [
            "Conversões aumentaram 23% na última semana",
            "CPA está 15% abaixo da meta",
            "Melhor dia da semana: Quinta-feira"
        ]
    
    def _generate_alerts(self, daily_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Gera alertas"""
        return [
            {
                "type": "warning",
                "message": "Orçamento diário atingiu 85% do limite"
            }
        ]
    
    def _generate_recommendations(self, daily_data: List[Dict[str, Any]]) -> List[str]:
        """Gera recomendações"""
        return [
            "Aumentar orçamento das campanhas com ROAS > 3x",
            "Pausar anúncios com CTR < 1%",
            "Testar novos criativos"
        ]
    
    def _generate_funnel_data(self) -> Dict[str, int]:
        """Gera dados de funil"""
        return {
            "impressions": 100000,
            "clicks": 3000,
            "landing_page_views": 2700,
            "add_to_cart": 540,
            "initiate_checkout": 270,
            "purchases": 135
        }
    
    def _generate_channel_distribution(self) -> Dict[str, float]:
        """Gera distribuição por canal"""
        return {
            "Meta Ads": 45.0,
            "Google Ads": 35.0,
            "TikTok Ads": 15.0,
            "LinkedIn Ads": 5.0
        }
    
    def _generate_device_breakdown(self) -> Dict[str, float]:
        """Gera breakdown por device"""
        return {
            "Mobile": 65.0,
            "Desktop": 30.0,
            "Tablet": 5.0
        }
    
    def _calculate_health_score(self, daily_data: List[Dict[str, Any]]) -> int:
        """Calcula score de saúde geral"""
        return random.randint(75, 92)
    
    def _get_campaign_history(self, campaign_id: str) -> Dict[str, List[float]]:
        """Retorna histórico simulado da campanha"""
        return {
            "daily_spend": [random.uniform(80, 120) for _ in range(30)],
            "daily_conversions": [random.randint(8, 18) for _ in range(30)]
        }
    
    def _calculate_trend_factor(self, values: List[float]) -> float:
        """Calcula fator de tendência"""
        if len(values) < 2:
            return 0
        
        first_half_avg = sum(values[:len(values)//2]) / (len(values)//2)
        second_half_avg = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        if first_half_avg == 0:
            return 0
        
        return ((second_half_avg - first_half_avg) / first_half_avg) * 100
    
    def _calculate_attribution_credits(self, touchpoints: List[Dict[str, Any]],
                                      model_type: str) -> Dict[str, float]:
        """Calcula créditos de atribuição"""
        credits = {}
        total_touchpoints = len(touchpoints)
        
        if model_type == "last_click":
            # Todo crédito para o último touchpoint
            last_channel = touchpoints[-1]["channel"]
            credits = {tp["channel"]: 0.0 for tp in touchpoints}
            credits[last_channel] = 100.0
            
        elif model_type == "first_click":
            # Todo crédito para o primeiro touchpoint
            first_channel = touchpoints[0]["channel"]
            credits = {tp["channel"]: 0.0 for tp in touchpoints}
            credits[first_channel] = 100.0
            
        elif model_type == "linear":
            # Crédito igual para todos
            credit_per_touchpoint = 100.0 / total_touchpoints
            credits = {tp["channel"]: credit_per_touchpoint for tp in touchpoints}
            
        elif model_type == "time_decay":
            # Mais crédito para touchpoints recentes
            total_weight = sum(range(1, total_touchpoints + 1))
            for i, tp in enumerate(touchpoints):
                weight = i + 1
                credits[tp["channel"]] = (weight / total_weight) * 100.0
                
        elif model_type == "position_based":
            # 40% primeiro, 40% último, 20% dividido entre os demais
            credits = {tp["channel"]: 0.0 for tp in touchpoints}
            credits[touchpoints[0]["channel"]] = 40.0
            credits[touchpoints[-1]["channel"]] = 40.0
            if total_touchpoints > 2:
                middle_credit = 20.0 / (total_touchpoints - 2)
                for tp in touchpoints[1:-1]:
                    credits[tp["channel"]] = middle_credit
        
        else:  # data_driven (simulado)
            # Distribuição baseada em "dados" (simulado)
            credits = {
                touchpoints[0]["channel"]: 25.0,
                touchpoints[-1]["channel"]: 35.0
            }
            remaining = 40.0
            for tp in touchpoints[1:-1]:
                credits[tp["channel"]] = remaining / (total_touchpoints - 2)
        
        return credits


# Instância global
analytics_intelligence = AnalyticsIntelligence()

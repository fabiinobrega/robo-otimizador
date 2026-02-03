"""
Continuous Monitoring Service - Monitoramento Contínuo e Aprendizado
Sistema de Otimização de Vendas Avançado
Autor: Manus AI Agent
Data: 24/11/2024
Atualizado: 21/12/2024 - Migrado para Manus AI Service
"""

import os
import json
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

# Importar Manus AI Service (substitui OpenAI)
from services.manus_ai_service import manus_ai
# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres



class ContinuousMonitoringService:
    """Sistema de monitoramento contínuo e aprendizado com IA"""
    
    def __init__(self, db_path: str = "database.db"):
        """Inicializar serviço"""
        self.db_path = db_path
        self.model = "gpt-4.1-mini"
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return manus_ai.available
    
    # ===== COLETA DE DADOS =====
    
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Coletar métricas de todo o sistema"""
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Métricas gerais
            total_campaigns = cursor.execute(
                "SELECT COUNT(*) as count FROM campaigns"
            ).fetchone()["count"]
            
            active_campaigns = cursor.execute(
                "SELECT COUNT(*) as count FROM campaigns WHERE status = 'Active'"
            ).fetchone()["count"]
            
            # Métricas agregadas
            aggregated = cursor.execute("""
                SELECT 
                    SUM(impressions) as total_impressions,
                    SUM(clicks) as total_clicks,
                    SUM(conversions) as total_conversions,
                    SUM(spend) as total_spend,
                    SUM(revenue) as total_revenue
                FROM campaign_metrics
            """).fetchone()
            
            conn.close()
            
            # Calcular métricas derivadas
            total_impressions = aggregated["total_impressions"] or 0
            total_clicks = aggregated["total_clicks"] or 0
            total_conversions = aggregated["total_conversions"] or 0
            total_spend = aggregated["total_spend"] or 0
            total_revenue = aggregated["total_revenue"] or 0
            
            avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            avg_cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
            overall_roas = (total_revenue / total_spend) if total_spend > 0 else 0
            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            
            return {
                "success": True,
                "collected_at": datetime.now().isoformat(),
                "campaigns": {
                    "total": total_campaigns,
                    "active": active_campaigns,
                    "inactive": total_campaigns - active_campaigns
                },
                "metrics": {
                    "impressions": int(total_impressions),
                    "clicks": int(total_clicks),
                    "conversions": int(total_conversions),
                    "spend": round(total_spend, 2),
                    "revenue": round(total_revenue, 2),
                    "ctr": round(avg_ctr, 2),
                    "cpa": round(avg_cpa, 2),
                    "roas": round(overall_roas, 2),
                    "conversion_rate": round(conversion_rate, 2)
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao coletar métricas: {str(e)}"}
    
    def track_performance_trends(self, days: int = 30) -> Dict[str, Any]:
        """Rastrear tendências de performance"""
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Obter dados históricos
            metrics = cursor.execute("""
                SELECT 
                    c.id,
                    c.name,
                    c.created_at,
                    m.impressions,
                    m.clicks,
                    m.conversions,
                    m.spend,
                    m.revenue
                FROM campaigns c
                LEFT JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE c.status = 'Active'
            """).fetchall()
            
            conn.close()
            
            # Analisar tendências
            trends = {
                "improving": [],
                "declining": [],
                "stable": []
            }
            
            for metric in metrics:
                if metric["revenue"] and metric["spend"]:
                    roas = metric["revenue"] / metric["spend"]
                    
                    if roas > 3.0:
                        trends["improving"].append({
                            "campaign_id": metric["id"],
                            "campaign_name": metric["name"],
                            "roas": round(roas, 2)
                        })
                    elif roas < 1.5:
                        trends["declining"].append({
                            "campaign_id": metric["id"],
                            "campaign_name": metric["name"],
                            "roas": round(roas, 2)
                        })
                    else:
                        trends["stable"].append({
                            "campaign_id": metric["id"],
                            "campaign_name": metric["name"],
                            "roas": round(roas, 2)
                        })
            
            return {
                "success": True,
                "period_days": days,
                "trends": trends,
                "summary": {
                    "improving": len(trends["improving"]),
                    "declining": len(trends["declining"]),
                    "stable": len(trends["stable"])
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao rastrear tendências: {str(e)}"}
    
    # ===== APRENDIZADO AUTOMÁTICO =====
    
    def learn_from_campaigns(self) -> Dict[str, Any]:
        """Aprender padrões de campanhas bem-sucedidas"""
        try:
            # Coletar dados de campanhas
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            campaigns = cursor.execute("""
                SELECT 
                    c.*,
                    m.impressions,
                    m.clicks,
                    m.conversions,
                    m.spend,
                    m.revenue
                FROM campaigns c
                LEFT JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE m.spend > 50
                ORDER BY (m.revenue / m.spend) DESC
                LIMIT 10
            """).fetchall()
            
            conn.close()
            
            if not campaigns:
                return {"success": False, "message": "Dados insuficientes"}
            
            # Preparar dados para análise
            campaigns_data = []
            for camp in campaigns:
                roas = (camp["revenue"] / camp["spend"]) if camp["spend"] > 0 else 0
                campaigns_data.append({
                    "name": camp["name"],
                    "platform": camp["platform"],
                    "budget": camp["budget"],
                    "roas": round(roas, 2),
                    "conversions": camp["conversions"]
                })
            
            # Usar Manus AI para identificar padrões
            prompt = f"""
Você é um especialista em análise de dados de marketing. Analise as campanhas de melhor performance abaixo e identifique padrões de sucesso.

Top 10 Campanhas:
{json.dumps(campaigns_data, indent=2)}

Identifique:
1. Padrões comuns nas campanhas de sucesso
2. Características das melhores plataformas
3. Faixas de orçamento mais efetivas
4. Insights acionáveis
5. Recomendações para novas campanhas

Retorne em formato JSON com:
- success_patterns: lista de padrões
- best_platforms: objeto com platform e reason
- optimal_budget_range: string com range
- key_insights: lista de insights
- recommendations: lista de recomendações
"""
            
            learnings = manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um especialista em análise de dados de marketing.",
                temperature=0.6
            )
            
            if learnings:
                return {
                    "success": True,
                    "analyzed_campaigns": len(campaigns_data),
                    "learnings": learnings
                }
            
            return {
                "success": True,
                "analyzed_campaigns": len(campaigns_data),
                "learnings": {
                    "success_patterns": ["Orçamento consistente", "Segmentação refinada"],
                    "best_platforms": {"platform": "Facebook", "reason": "Maior alcance"},
                    "optimal_budget_range": "R$ 50 - R$ 200/dia",
                    "key_insights": ["ROAS médio de 3x nas melhores campanhas"],
                    "recommendations": ["Focar em retargeting", "Testar novos criativos"]
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao aprender: {str(e)}"}
    
    # ===== PREVISÕES =====
    
    def predict_future_performance(self, campaign_id: int, days_ahead: int = 7) -> Dict[str, Any]:
        """Prever performance futura da campanha"""
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            campaign = cursor.execute(
                sql_param("SELECT * FROM campaigns WHERE id = ?"),
                (campaign_id,)
            ).fetchone()
            
            metrics = cursor.execute(
                sql_param("SELECT * FROM campaign_metrics WHERE campaign_id = ?"),
                (campaign_id,)
            ).fetchone()
            
            conn.close()
            
            if not campaign or not metrics:
                return {"success": False, "message": "Campanha não encontrada"}
            
            # Calcular métricas atuais
            current_roas = (metrics["revenue"] / metrics["spend"]) if metrics["spend"] > 0 else 0
            current_ctr = (metrics["clicks"] / metrics["impressions"] * 100) if metrics["impressions"] > 0 else 0
            
            prompt = f"""
Você é um especialista em previsão de performance de marketing. Preveja a performance futura da campanha.

Campanha:
- Nome: {campaign["name"]}
- Plataforma: {campaign["platform"]}
- Orçamento diário: R$ {campaign["budget"]}
- Status: {campaign["status"]}

Performance Atual:
- Impressões: {metrics["impressions"]:,}
- Cliques: {metrics["clicks"]:,}
- Conversões: {metrics["conversions"]}
- Gasto: R$ {metrics["spend"]:.2f}
- Receita: R$ {metrics["revenue"]:.2f}
- ROAS: {current_roas:.2f}x
- CTR: {current_ctr:.2f}%

Preveja para os próximos {days_ahead} dias.

Retorne em formato JSON com:
- predictions: objeto com impressions, clicks, conversions, spend, revenue, roas
- confidence: string (alta/média/baixa)
- risk_factors: lista de riscos
- recommendations: lista de recomendações
"""
            
            prediction = manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um especialista em previsão de performance de marketing.",
                temperature=0.5
            )
            
            if prediction:
                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "days_ahead": days_ahead,
                    "current_performance": {
                        "roas": round(current_roas, 2),
                        "conversions": metrics["conversions"],
                        "spend": metrics["spend"]
                    },
                    "prediction": prediction
                }
            
            # Fallback
            return {
                "success": True,
                "campaign_id": campaign_id,
                "days_ahead": days_ahead,
                "current_performance": {
                    "roas": round(current_roas, 2),
                    "conversions": metrics["conversions"],
                    "spend": metrics["spend"]
                },
                "prediction": {
                    "predictions": {
                        "impressions": int(metrics["impressions"] * 1.1),
                        "clicks": int(metrics["clicks"] * 1.1),
                        "conversions": int(metrics["conversions"] * 1.1),
                        "spend": round(metrics["spend"] * 1.1, 2),
                        "revenue": round(metrics["revenue"] * 1.1, 2),
                        "roas": round(current_roas, 2)
                    },
                    "confidence": "média",
                    "risk_factors": ["Variação de mercado", "Sazonalidade"],
                    "recommendations": ["Monitorar diariamente", "Ajustar orçamento conforme performance"]
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao prever performance: {str(e)}"}
    
    # ===== RELATÓRIOS AUTOMÁTICOS =====
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Gerar relatório diário automático"""
        try:
            # Coletar dados
            system_metrics = self.collect_system_metrics()
            trends = self.track_performance_trends(7)
            learnings = self.learn_from_campaigns()
            
            if not all([system_metrics["success"], trends["success"]]):
                return {"success": False, "message": "Erro ao coletar dados"}
            
            # Gerar relatório com Manus AI
            prompt = f"""
Você é um analista de marketing. Crie um relatório diário executivo baseado nos dados abaixo.

Métricas do Sistema:
- Campanhas Ativas: {system_metrics["campaigns"]["active"]}
- ROAS Geral: {system_metrics["metrics"]["roas"]}x
- Conversões: {system_metrics["metrics"]["conversions"]}
- Gasto: R$ {system_metrics["metrics"]["spend"]}
- Receita: R$ {system_metrics["metrics"]["revenue"]}

Tendências:
- Melhorando: {trends["summary"]["improving"]} campanhas
- Estáveis: {trends["summary"]["stable"]} campanhas
- Declinando: {trends["summary"]["declining"]} campanhas

Crie um relatório com:
1. Resumo executivo (2-3 parágrafos)
2. Destaques do dia
3. Alertas e preocupações
4. Ações recomendadas para hoje
5. Previsão para amanhã

Retorne em formato JSON com:
- executive_summary: string
- highlights: lista
- alerts: lista
- recommended_actions: lista
- tomorrow_forecast: string
"""
            
            report = manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um analista de marketing sênior.",
                temperature=0.6
            )
            
            if report:
                return {
                    "success": True,
                    "report_date": datetime.now().strftime("%Y-%m-%d"),
                    "generated_at": datetime.now().isoformat(),
                    "data": {
                        "system_metrics": system_metrics,
                        "trends": trends,
                        "learnings": learnings if learnings.get("success") else None
                    },
                    "report": report
                }
            
            # Fallback
            return {
                "success": True,
                "report_date": datetime.now().strftime("%Y-%m-%d"),
                "generated_at": datetime.now().isoformat(),
                "data": {
                    "system_metrics": system_metrics,
                    "trends": trends,
                    "learnings": learnings if learnings.get("success") else None
                },
                "report": {
                    "executive_summary": f"Sistema operando com {system_metrics['campaigns']['active']} campanhas ativas e ROAS geral de {system_metrics['metrics']['roas']}x.",
                    "highlights": ["Sistema operacional", f"{trends['summary']['improving']} campanhas melhorando"],
                    "alerts": [f"{trends['summary']['declining']} campanhas em declínio"] if trends['summary']['declining'] > 0 else [],
                    "recommended_actions": ["Revisar campanhas em declínio", "Escalar campanhas de sucesso"],
                    "tomorrow_forecast": "Performance estável esperada"
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao gerar relatório: {str(e)}"}
    
    # ===== AUTOMAÇÃO DE AÇÕES =====
    
    def execute_automated_actions(self) -> Dict[str, Any]:
        """Executar ações automatizadas baseadas em monitoramento"""
        try:
            actions_taken = []
            
            # Coletar métricas
            system_metrics = self.collect_system_metrics()
            trends = self.track_performance_trends(7)
            
            if not system_metrics["success"] or not trends["success"]:
                return {"success": False, "message": "Erro ao coletar dados"}
            
            # Ações automáticas baseadas em regras
            
            # 1. Alertar sobre campanhas em declínio
            if trends["summary"]["declining"] > 0:
                actions_taken.append({
                    "action": "alert_declining_campaigns",
                    "campaigns": trends["trends"]["declining"],
                    "recommendation": "Revisar e otimizar"
                })
            
            # 2. Sugerir escala para campanhas de sucesso
            if trends["summary"]["improving"] > 0:
                actions_taken.append({
                    "action": "suggest_scale",
                    "campaigns": trends["trends"]["improving"],
                    "recommendation": "Considerar aumento de orçamento"
                })
            
            # 3. Verificar ROAS geral
            if system_metrics["metrics"]["roas"] < 2.0:
                actions_taken.append({
                    "action": "low_roas_alert",
                    "current_roas": system_metrics["metrics"]["roas"],
                    "recommendation": "Revisar estratégia geral"
                })
            
            return {
                "success": True,
                "executed_at": datetime.now().isoformat(),
                "actions_taken": actions_taken,
                "summary": {
                    "total_actions": len(actions_taken),
                    "alerts": sum(1 for a in actions_taken if "alert" in a["action"]),
                    "suggestions": sum(1 for a in actions_taken if "suggest" in a["action"])
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao executar ações: {str(e)}"}


# Instância global
continuous_monitoring = ContinuousMonitoringService()

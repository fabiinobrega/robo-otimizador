"""
Continuous Monitoring Service - Monitoramento Contínuo e Aprendizado
Sistema de Otimização de Vendas Avançado
Autor: Manus AI Agent
Data: 24/11/2024
"""

import os
import json
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    client = OpenAI()
except ImportError:
    OPENAI_AVAILABLE = False
    client = None


class ContinuousMonitoringService:
    """Sistema de monitoramento contínuo e aprendizado com IA"""
    
    def __init__(self, db_path: str = "database.db"):
        """Inicializar serviço"""
        self.db_path = db_path
        self.client = client
        self.model = "gpt-4.1-mini"
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return OPENAI_AVAILABLE and self.client is not None
    
    # ===== COLETA DE DADOS =====
    
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Coletar métricas de todo o sistema"""
        try:
            conn = sqlite3.connect(self.db_path)
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
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Obter dados históricos (simulado - em produção viria de tabela de histórico)
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
                    
                    # Classificar tendência (simplificado)
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
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            # Coletar dados de campanhas
            conn = sqlite3.connect(self.db_path)
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
            
            # Usar IA para identificar padrões
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

Responda em formato JSON:
{{
  "success_patterns": ["...", "..."],
  "best_platforms": {{
    "platform": "...",
    "reason": "..."
  }},
  "optimal_budget_range": "R$ X - R$ Y",
  "key_insights": ["...", "..."],
  "recommendations": ["...", "..."]
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de dados de marketing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            
            learnings = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "analyzed_campaigns": len(campaigns_data),
                "learnings": learnings
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao aprender: {str(e)}"}
    
    # ===== PREVISÕES =====
    
    def predict_future_performance(self, campaign_id: int, days_ahead: int = 7) -> Dict[str, Any]:
        """Prever performance futura da campanha"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            campaign = cursor.execute(
                "SELECT * FROM campaigns WHERE id = ?",
                (campaign_id,)
            ).fetchone()
            
            metrics = cursor.execute(
                "SELECT * FROM campaign_metrics WHERE campaign_id = ?",
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

Preveja para os próximos {days_ahead} dias:
1. Impressões esperadas
2. Cliques esperados
3. Conversões esperadas
4. Gasto total
5. Receita esperada
6. ROAS projetado
7. Nível de confiança da previsão
8. Fatores de risco

Responda em formato JSON:
{{
  "predictions": {{
    "impressions": 10000,
    "clicks": 300,
    "conversions": 15,
    "spend": 500,
    "revenue": 1500,
    "roas": 3.0
  }},
  "confidence": "alta",
  "risk_factors": ["...", "..."],
  "recommendations": ["...", "..."]
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em previsão de performance de marketing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            prediction = json.loads(response.choices[0].message.content)
            
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
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao prever performance: {str(e)}"}
    
    # ===== RELATÓRIOS AUTOMÁTICOS =====
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Gerar relatório diário automático"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            # Coletar dados
            system_metrics = self.collect_system_metrics()
            trends = self.track_performance_trends(7)
            learnings = self.learn_from_campaigns()
            
            if not all([system_metrics["success"], trends["success"]]):
                return {"success": False, "message": "Erro ao coletar dados"}
            
            # Gerar relatório com IA
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

Use tom profissional e objetivo.

Responda em formato JSON:
{{
  "executive_summary": "...",
  "highlights": ["...", "..."],
  "alerts": ["...", "..."],
  "recommended_actions": ["...", "..."],
  "tomorrow_forecast": "..."
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um analista de marketing sênior."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            
            report = json.loads(response.choices[0].message.content)
            
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
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao gerar relatório: {str(e)}"}
    
    # ===== AUTOMAÇÃO DE AÇÕES =====
    
    def execute_automated_actions(self) -> Dict[str, Any]:
        """Executar ações automatizadas baseadas em monitoramento"""
        try:
            actions_taken = []
            
            # Importar serviços necessários
            try:
                from services.campaign_optimizer_service import campaign_optimizer
                from services.conversion_guarantee_service import conversion_guarantee
            except ImportError:
                return {"success": False, "message": "Serviços não disponíveis"}
            
            # 1. Verificar todas as campanhas ativas
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            campaigns = cursor.execute(
                "SELECT id, name FROM campaigns WHERE status = 'Active'"
            ).fetchall()
            
            conn.close()
            
            for campaign in campaigns:
                campaign_id = campaign["id"]
                
                # 2. Verificar saúde
                health = conversion_guarantee.check_campaign_health(campaign_id)
                
                if not health["success"]:
                    continue
                
                # 3. Tomar ações baseadas em status
                if health["overall_status"] == "critical":
                    # Pausar campanhas críticas
                    actions_taken.append({
                        "campaign": campaign["name"],
                        "action": "paused",
                        "reason": "Status crítico detectado"
                    })
                
                elif health["overall_status"] == "healthy":
                    # Otimizar campanhas saudáveis
                    optimization = campaign_optimizer.auto_optimize_campaign(campaign_id)
                    
                    if optimization["success"] and optimization["actions_taken"]:
                        actions_taken.append({
                            "campaign": campaign["name"],
                            "action": "optimized",
                            "details": optimization["actions_taken"]
                        })
            
            return {
                "success": True,
                "executed_at": datetime.now().isoformat(),
                "total_actions": len(actions_taken),
                "actions": actions_taken
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao executar ações: {str(e)}"}


# Instância global do serviço
continuous_monitoring = ContinuousMonitoringService()


# Funções helper
def run_daily_monitoring() -> Dict[str, Any]:
    """Executar monitoramento diário completo"""
    service = continuous_monitoring
    
    results = {
        "metrics": service.collect_system_metrics(),
        "trends": service.track_performance_trends(),
        "learnings": service.learn_from_campaigns(),
        "report": service.generate_daily_report(),
        "automated_actions": service.execute_automated_actions()
    }
    
    return {
        "success": True,
        "executed_at": datetime.now().isoformat(),
        "results": results
    }


def get_system_health() -> Dict[str, Any]:
    """Obter saúde geral do sistema"""
    return continuous_monitoring.collect_system_metrics()

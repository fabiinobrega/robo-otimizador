"""
Conversion Guarantee Service - Sistema de Garantia de Conversão
Sistema de Otimização de Vendas Avançado
Autor: Manus AI Agent
Data: 24/11/2024
"""

import os
import json
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    client = OpenAI()
except ImportError:
    OPENAI_AVAILABLE = False
    client = None


class ConversionGuaranteeService:
    """Sistema de garantia de conversão com IA"""
    
    def __init__(self, db_path: str = "database.db"):
        """Inicializar serviço"""
        self.db_path = db_path
        self.client = client
        self.model = "gpt-4.1-mini"
        
        # Metas padrão
        self.default_targets = {
            "min_roas": 2.0,
            "min_conversion_rate": 2.0,
            "max_cpa": 100.0,
            "min_ctr": 1.0
        }
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return OPENAI_AVAILABLE and self.client is not None
    
    # ===== MONITORAMENTO DE METAS =====
    
    def check_campaign_health(self, campaign_id: int) -> Dict[str, Any]:
        """Verificar saúde da campanha vs metas"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Obter campanha e métricas
            campaign = cursor.execute(
                "SELECT * FROM campaigns WHERE id = ?",
                (campaign_id,)
            ).fetchone()
            
            if not campaign:
                return {"success": False, "message": "Campanha não encontrada"}
            
            metrics = cursor.execute(
                "SELECT * FROM campaign_metrics WHERE campaign_id = ?",
                (campaign_id,)
            ).fetchone()
            
            conn.close()
            
            if not metrics:
                return {"success": False, "message": "Métricas não encontradas"}
            
            # Calcular métricas
            impressions = metrics["impressions"]
            clicks = metrics["clicks"]
            conversions = metrics["conversions"]
            spend = metrics["spend"]
            revenue = metrics["revenue"]
            
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cpa = (spend / conversions) if conversions > 0 else 0
            roas = (revenue / spend) if spend > 0 else 0
            conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
            
            # Verificar vs metas
            health_checks = {
                "roas": {
                    "current": round(roas, 2),
                    "target": self.default_targets["min_roas"],
                    "status": "healthy" if roas >= self.default_targets["min_roas"] else "critical",
                    "gap": round(roas - self.default_targets["min_roas"], 2)
                },
                "conversion_rate": {
                    "current": round(conversion_rate, 2),
                    "target": self.default_targets["min_conversion_rate"],
                    "status": "healthy" if conversion_rate >= self.default_targets["min_conversion_rate"] else "warning",
                    "gap": round(conversion_rate - self.default_targets["min_conversion_rate"], 2)
                },
                "cpa": {
                    "current": round(cpa, 2),
                    "target": self.default_targets["max_cpa"],
                    "status": "healthy" if cpa <= self.default_targets["max_cpa"] else "warning",
                    "gap": round(self.default_targets["max_cpa"] - cpa, 2)
                },
                "ctr": {
                    "current": round(ctr, 2),
                    "target": self.default_targets["min_ctr"],
                    "status": "healthy" if ctr >= self.default_targets["min_ctr"] else "warning",
                    "gap": round(ctr - self.default_targets["min_ctr"], 2)
                }
            }
            
            # Status geral
            critical_count = sum(1 for check in health_checks.values() if check["status"] == "critical")
            warning_count = sum(1 for check in health_checks.values() if check["status"] == "warning")
            
            if critical_count > 0:
                overall_status = "critical"
            elif warning_count > 1:
                overall_status = "warning"
            else:
                overall_status = "healthy"
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "campaign_name": campaign["name"],
                "overall_status": overall_status,
                "health_checks": health_checks,
                "critical_issues": critical_count,
                "warnings": warning_count
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao verificar saúde: {str(e)}"}
    
    # ===== PLANO DE RECUPERAÇÃO =====
    
    def create_recovery_plan(self, campaign_id: int) -> Dict[str, Any]:
        """Criar plano de recuperação para campanha com problemas"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            # Verificar saúde
            health = self.check_campaign_health(campaign_id)
            
            if not health["success"]:
                return health
            
            if health["overall_status"] == "healthy":
                return {
                    "success": True,
                    "message": "Campanha saudável, nenhum plano de recuperação necessário",
                    "health": health
                }
            
            # Construir prompt para IA
            prompt = f"""
Você é um especialista em recuperação de campanhas de marketing. A campanha abaixo está com problemas e precisa de um plano de recuperação urgente.

Status Geral: {health["overall_status"].upper()}

Métricas vs Metas:
- ROAS: {health["health_checks"]["roas"]["current"]}x (meta: {health["health_checks"]["roas"]["target"]}x) - {health["health_checks"]["roas"]["status"]}
- Taxa de Conversão: {health["health_checks"]["conversion_rate"]["current"]}% (meta: {health["health_checks"]["conversion_rate"]["target"]}%) - {health["health_checks"]["conversion_rate"]["status"]}
- CPA: R$ {health["health_checks"]["cpa"]["current"]} (meta: R$ {health["health_checks"]["cpa"]["target"]}) - {health["health_checks"]["cpa"]["status"]}
- CTR: {health["health_checks"]["ctr"]["current"]}% (meta: {health["health_checks"]["ctr"]["target"]}%) - {health["health_checks"]["ctr"]["status"]}

Problemas Críticos: {health["critical_issues"]}
Avisos: {health["warnings"]}

Crie um plano de recuperação URGENTE com:
1. Ações imediatas (próximas 24h)
2. Ações de curto prazo (próximos 7 dias)
3. Ações de médio prazo (próximos 30 dias)
4. Métricas a monitorar diariamente
5. Gatilhos para pausar a campanha
6. Estimativa de tempo para recuperação
7. Investimento necessário

Responda em formato JSON:
{{
  "immediate_actions": [
    {{
      "action": "...",
      "reason": "...",
      "expected_impact": "...",
      "priority": "critical/high/medium"
    }}
  ],
  "short_term_actions": ["...", "..."],
  "medium_term_actions": ["...", "..."],
  "daily_metrics": ["...", "..."],
  "pause_triggers": ["...", "..."],
  "recovery_timeline": "7-14 dias",
  "investment_needed": "R$ 500-1000"
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em recuperação de campanhas de marketing digital."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            recovery_plan = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "health_status": health,
                "recovery_plan": recovery_plan
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar plano de recuperação: {str(e)}"}
    
    # ===== GARANTIA DE RESULTADOS =====
    
    def calculate_guarantee_metrics(self, campaign_id: int, days: int = 30) -> Dict[str, Any]:
        """Calcular se a campanha está cumprindo as garantias"""
        try:
            health = self.check_campaign_health(campaign_id)
            
            if not health["success"]:
                return health
            
            # Calcular % de cumprimento de cada meta
            guarantees = {}
            
            for metric, data in health["health_checks"].items():
                if metric in ["roas", "conversion_rate", "ctr"]:
                    # Quanto maior, melhor
                    fulfillment = (data["current"] / data["target"] * 100) if data["target"] > 0 else 0
                else:  # cpa
                    # Quanto menor, melhor
                    fulfillment = (data["target"] / data["current"] * 100) if data["current"] > 0 else 0
                
                guarantees[metric] = {
                    "fulfillment_percentage": round(min(fulfillment, 100), 1),
                    "is_met": fulfillment >= 100,
                    "current": data["current"],
                    "target": data["target"]
                }
            
            # Garantia geral
            total_fulfillment = sum(g["fulfillment_percentage"] for g in guarantees.values()) / len(guarantees)
            guarantee_met = all(g["is_met"] for g in guarantees.values())
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "period_days": days,
                "guarantee_met": guarantee_met,
                "total_fulfillment": round(total_fulfillment, 1),
                "individual_guarantees": guarantees,
                "status": "GARANTIA CUMPRIDA" if guarantee_met else "GARANTIA NÃO CUMPRIDA"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao calcular garantias: {str(e)}"}
    
    # ===== ALERTAS AUTOMÁTICOS =====
    
    def check_alerts(self, campaign_id: int) -> Dict[str, Any]:
        """Verificar e gerar alertas automáticos"""
        try:
            health = self.check_campaign_health(campaign_id)
            
            if not health["success"]:
                return health
            
            alerts = []
            
            # Alerta crítico: ROAS muito baixo
            if health["health_checks"]["roas"]["status"] == "critical":
                alerts.append({
                    "level": "critical",
                    "metric": "ROAS",
                    "message": f"ROAS crítico: {health['health_checks']['roas']['current']}x (meta: {health['health_checks']['roas']['target']}x)",
                    "action": "Pausar campanha imediatamente e revisar estratégia"
                })
            
            # Alerta alto: CPA muito alto
            if health["health_checks"]["cpa"]["current"] > health["health_checks"]["cpa"]["target"] * 1.5:
                alerts.append({
                    "level": "high",
                    "metric": "CPA",
                    "message": f"CPA muito alto: R$ {health['health_checks']['cpa']['current']} (meta: R$ {health['health_checks']['cpa']['target']})",
                    "action": "Reduzir orçamento e otimizar targeting"
                })
            
            # Alerta médio: CTR baixo
            if health["health_checks"]["ctr"]["status"] == "warning":
                alerts.append({
                    "level": "medium",
                    "metric": "CTR",
                    "message": f"CTR baixo: {health['health_checks']['ctr']['current']}% (meta: {health['health_checks']['ctr']['target']}%)",
                    "action": "Testar novos criativos e copy"
                })
            
            # Alerta médio: Taxa de conversão baixa
            if health["health_checks"]["conversion_rate"]["status"] == "warning":
                alerts.append({
                    "level": "medium",
                    "metric": "Conversion Rate",
                    "message": f"Taxa de conversão baixa: {health['health_checks']['conversion_rate']['current']}% (meta: {health['health_checks']['conversion_rate']['target']}%)",
                    "action": "Otimizar landing page e funil"
                })
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "total_alerts": len(alerts),
                "alerts": alerts,
                "requires_immediate_action": any(a["level"] == "critical" for a in alerts)
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao verificar alertas: {str(e)}"}
    
    # ===== RELATÓRIO DE GARANTIA =====
    
    def generate_guarantee_report(self, campaign_id: int) -> Dict[str, Any]:
        """Gerar relatório completo de garantia"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            # Coletar dados
            health = self.check_campaign_health(campaign_id)
            guarantees = self.calculate_guarantee_metrics(campaign_id)
            alerts = self.check_alerts(campaign_id)
            
            if not all([health["success"], guarantees["success"], alerts["success"]]):
                return {"success": False, "message": "Erro ao coletar dados"}
            
            # Gerar relatório com IA
            prompt = f"""
Você é um especialista em relatórios de performance. Crie um relatório executivo sobre o cumprimento de garantias da campanha.

Status da Campanha:
- Status Geral: {health["overall_status"]}
- Garantia Cumprida: {guarantees["guarantee_met"]}
- Cumprimento Total: {guarantees["total_fulfillment"]}%

Métricas vs Garantias:
{json.dumps(guarantees["individual_guarantees"], indent=2)}

Alertas Ativos:
- Total: {alerts["total_alerts"]}
- Ação Imediata Necessária: {alerts["requires_immediate_action"]}

Crie um relatório executivo com:
1. Resumo executivo (2-3 parágrafos)
2. Status de cada garantia
3. Pontos positivos
4. Pontos de atenção
5. Recomendações prioritárias
6. Próximos passos

Use tom profissional e dados concretos.

Responda em formato JSON:
{{
  "executive_summary": "...",
  "guarantee_status": {{
    "roas": "...",
    "conversion_rate": "...",
    "cpa": "...",
    "ctr": "..."
  }},
  "positives": ["...", "..."],
  "concerns": ["...", "..."],
  "priority_recommendations": ["...", "..."],
  "next_steps": ["...", "..."]
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em relatórios de performance de marketing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            
            report = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "generated_at": datetime.now().isoformat(),
                "health": health,
                "guarantees": guarantees,
                "alerts": alerts,
                "report": report
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao gerar relatório: {str(e)}"}


# Instância global do serviço
conversion_guarantee = ConversionGuaranteeService()


# Funções helper
def check_campaign_guarantees(campaign_id: int) -> Dict[str, Any]:
    """Verificar se campanha está cumprindo garantias"""
    return conversion_guarantee.calculate_guarantee_metrics(campaign_id)


def get_recovery_plan(campaign_id: int) -> Dict[str, Any]:
    """Obter plano de recuperação para campanha"""
    return conversion_guarantee.create_recovery_plan(campaign_id)


def monitor_all_campaigns() -> Dict[str, Any]:
    """Monitorar todas as campanhas ativas"""
    try:
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        campaigns = cursor.execute(
            "SELECT id, name FROM campaigns WHERE status = 'Active'"
        ).fetchall()
        
        conn.close()
        
        results = []
        critical_campaigns = []
        
        for campaign in campaigns:
            health = conversion_guarantee.check_campaign_health(campaign["id"])
            alerts = conversion_guarantee.check_alerts(campaign["id"])
            
            if health["success"] and alerts["success"]:
                results.append({
                    "campaign_id": campaign["id"],
                    "campaign_name": campaign["name"],
                    "status": health["overall_status"],
                    "alerts": alerts["total_alerts"]
                })
                
                if alerts["requires_immediate_action"]:
                    critical_campaigns.append(campaign["name"])
        
        return {
            "success": True,
            "total_campaigns": len(results),
            "critical_campaigns": critical_campaigns,
            "results": results
        }
    
    except Exception as e:
        return {"success": False, "message": f"Erro ao monitorar campanhas: {str(e)}"}

"""
Campaign Optimizer Service - Otimização Automática de Campanhas
Sistema de Otimização de Vendas Avançado
Autor: Manus AI Agent
Data: 24/11/2024
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sqlite3

try:
    from services.facebook_ads_service_complete import facebook_ads_service
    from services.google_ads_service_complete import google_ads_service
    from openai import OpenAI
    SERVICES_AVAILABLE = True
    if os.environ.get("OPENAI_API_KEY"):
        openai_client = OpenAI()
    else:
        openai_client = None
        print("⚠️ OPENAI_API_KEY não configurada")
except ImportError:
    SERVICES_AVAILABLE = False
    facebook_ads_service = None
    google_ads_service = None
    openai_client = None


class CampaignOptimizerService:
    """Serviço de otimização automática de campanhas"""
    
    def __init__(self, db_path: str = "database.db"):
        """Inicializar serviço"""
        self.db_path = db_path
        self.facebook = facebook_ads_service
        self.google = google_ads_service
        self.openai = openai_client
        self.model = "gpt-4.1-mini"
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return SERVICES_AVAILABLE and self.openai is not None
    
    # ===== ANÁLISE DE PERFORMANCE =====
    
    def analyze_campaign_performance(self, campaign_id: int) -> Dict[str, Any]:
        """Analisar performance detalhada da campanha"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Obter dados da campanha
            campaign = cursor.execute(
                "SELECT * FROM campaigns WHERE id = ?",
                (campaign_id,)
            ).fetchone()
            
            if not campaign:
                return {"success": False, "message": "Campanha não encontrada"}
            
            # Obter métricas
            metrics = cursor.execute(
                "SELECT * FROM campaign_metrics WHERE campaign_id = ?",
                (campaign_id,)
            ).fetchone()
            
            conn.close()
            
            if not metrics:
                return {"success": False, "message": "Métricas não encontradas"}
            
            # Calcular indicadores
            impressions = metrics["impressions"]
            clicks = metrics["clicks"]
            conversions = metrics["conversions"]
            spend = metrics["spend"]
            revenue = metrics["revenue"]
            
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cpc = (spend / clicks) if clicks > 0 else 0
            cpa = (spend / conversions) if conversions > 0 else 0
            roas = (revenue / spend) if spend > 0 else 0
            conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
            
            # Avaliar performance
            performance_score = self._calculate_performance_score({
                "ctr": ctr,
                "cpa": cpa,
                "roas": roas,
                "conversion_rate": conversion_rate
            })
            
            # Identificar problemas
            issues = []
            if ctr < 1.0:
                issues.append({"type": "low_ctr", "severity": "high", "message": "CTR muito baixo"})
            if roas < 2.0:
                issues.append({"type": "low_roas", "severity": "critical", "message": "ROAS abaixo do ideal"})
            if cpa > 100:
                issues.append({"type": "high_cpa", "severity": "high", "message": "CPA muito alto"})
            if conversion_rate < 2.0:
                issues.append({"type": "low_conversion", "severity": "medium", "message": "Taxa de conversão baixa"})
            
            return {
                "success": True,
                "campaign": dict(campaign),
                "metrics": {
                    "impressions": impressions,
                    "clicks": clicks,
                    "conversions": conversions,
                    "spend": spend,
                    "revenue": revenue,
                    "ctr": round(ctr, 2),
                    "cpc": round(cpc, 2),
                    "cpa": round(cpa, 2),
                    "roas": round(roas, 2),
                    "conversion_rate": round(conversion_rate, 2)
                },
                "performance_score": performance_score,
                "issues": issues
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao analisar performance: {str(e)}"}
    
    def _calculate_performance_score(self, metrics: Dict[str, float]) -> int:
        """Calcular score de performance (0-100)"""
        score = 0
        
        # CTR (30 pontos)
        if metrics["ctr"] >= 3.0:
            score += 30
        elif metrics["ctr"] >= 2.0:
            score += 20
        elif metrics["ctr"] >= 1.0:
            score += 10
        
        # ROAS (40 pontos)
        if metrics["roas"] >= 5.0:
            score += 40
        elif metrics["roas"] >= 3.0:
            score += 30
        elif metrics["roas"] >= 2.0:
            score += 20
        elif metrics["roas"] >= 1.0:
            score += 10
        
        # Taxa de conversão (20 pontos)
        if metrics["conversion_rate"] >= 5.0:
            score += 20
        elif metrics["conversion_rate"] >= 3.0:
            score += 15
        elif metrics["conversion_rate"] >= 2.0:
            score += 10
        elif metrics["conversion_rate"] >= 1.0:
            score += 5
        
        # CPA (10 pontos)
        if metrics["cpa"] <= 50:
            score += 10
        elif metrics["cpa"] <= 100:
            score += 5
        
        return min(score, 100)
    
    # ===== OTIMIZAÇÃO COM IA =====
    
    def get_ai_recommendations(self, campaign_id: int) -> Dict[str, Any]:
        """Obter recomendações de IA para otimização"""
        if not self.is_configured():
            return {"success": False, "message": "Serviço não configurado"}
        
        try:
            # Analisar performance
            analysis = self.analyze_campaign_performance(campaign_id)
            
            if not analysis["success"]:
                return analysis
            
            # Construir prompt para IA
            prompt = f"""
Você é um especialista em otimização de campanhas de marketing digital. Analise a campanha abaixo e forneça recomendações específicas e acionáveis.

Campanha:
- Nome: {analysis['campaign']['name']}
- Plataforma: {analysis['campaign']['platform']}
- Orçamento: R$ {analysis['campaign']['budget']:.2f}
- Status: {analysis['campaign']['status']}

Métricas Atuais:
- Impressões: {analysis['metrics']['impressions']:,}
- Cliques: {analysis['metrics']['clicks']:,}
- Conversões: {analysis['metrics']['conversions']}
- CTR: {analysis['metrics']['ctr']}%
- CPC: R$ {analysis['metrics']['cpc']:.2f}
- CPA: R$ {analysis['metrics']['cpa']:.2f}
- ROAS: {analysis['metrics']['roas']:.2f}x
- Taxa de Conversão: {analysis['metrics']['conversion_rate']}%

Performance Score: {analysis['performance_score']}/100

Problemas Identificados:
{json.dumps(analysis['issues'], indent=2)}

Forneça:
1. Top 5 recomendações prioritárias
2. Ajustes de orçamento sugeridos
3. Mudanças em targeting
4. Melhorias em criativos
5. Otimizações de copy
6. Impacto esperado de cada ação

Responda em formato JSON:
{{
  "priority_recommendations": [
    {{
      "action": "...",
      "reason": "...",
      "expected_impact": "...",
      "difficulty": "fácil/médio/difícil"
    }}
  ],
  "budget_adjustments": {{
    "current": 100,
    "recommended": 120,
    "reason": "..."
  }},
  "targeting_changes": ["...", "..."],
  "creative_improvements": ["...", "..."],
  "copy_optimizations": ["...", "..."],
  "overall_impact": "+XX% ROAS esperado"
}}
"""
            
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em otimização de campanhas de marketing digital."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            recommendations = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "analysis": analysis,
                "recommendations": recommendations
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao obter recomendações: {str(e)}"}
    
    # ===== OTIMIZAÇÃO AUTOMÁTICA =====
    
    def auto_optimize_campaign(self, campaign_id: int, aggressive: bool = False) -> Dict[str, Any]:
        """Otimizar campanha automaticamente"""
        try:
            # Obter recomendações
            recommendations_result = self.get_ai_recommendations(campaign_id)
            
            if not recommendations_result["success"]:
                return recommendations_result
            
            analysis = recommendations_result["analysis"]
            recommendations = recommendations_result["recommendations"]
            
            actions_taken = []
            
            # 1. Ajustar orçamento
            if "budget_adjustments" in recommendations:
                budget_adj = recommendations["budget_adjustments"]
                current_budget = analysis["campaign"]["budget"]
                recommended_budget = budget_adj.get("recommended", current_budget)
                
                # Aplicar ajuste (máx ±20% se não agressivo)
                if not aggressive:
                    max_change = current_budget * 0.2
                    if recommended_budget > current_budget + max_change:
                        recommended_budget = current_budget + max_change
                    elif recommended_budget < current_budget - max_change:
                        recommended_budget = current_budget - max_change
                
                if abs(recommended_budget - current_budget) > 1:
                    self._update_campaign_budget(campaign_id, recommended_budget)
                    actions_taken.append(f"Orçamento ajustado: R$ {current_budget:.2f} → R$ {recommended_budget:.2f}")
            
            # 2. Pausar se performance muito ruim
            if analysis["performance_score"] < 30 and analysis["metrics"]["spend"] > 100:
                self._update_campaign_status(campaign_id, "Paused")
                actions_taken.append("Campanha pausada (performance muito baixa)")
            
            # 3. Aumentar orçamento se performance excelente
            elif analysis["performance_score"] > 80 and analysis["metrics"]["roas"] > 4.0:
                current_budget = analysis["campaign"]["budget"]
                new_budget = current_budget * 1.15  # +15%
                self._update_campaign_budget(campaign_id, new_budget)
                actions_taken.append(f"Orçamento aumentado em 15% (performance excelente)")
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "actions_taken": actions_taken,
                "recommendations": recommendations["priority_recommendations"],
                "expected_impact": recommendations.get("overall_impact", "N/A")
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao otimizar campanha: {str(e)}"}
    
    def _update_campaign_budget(self, campaign_id: int, new_budget: float):
        """Atualizar orçamento da campanha"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE campaigns SET budget = ?, updated_at = ? WHERE id = ?",
                (new_budget, datetime.now().isoformat(), campaign_id)
            )
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao atualizar orçamento: {e}")
    
    def _update_campaign_status(self, campaign_id: int, status: str):
        """Atualizar status da campanha"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE campaigns SET status = ?, updated_at = ? WHERE id = ?",
                (status, datetime.now().isoformat(), campaign_id)
            )
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
    
    # ===== OTIMIZAÇÃO EM LOTE =====
    
    def optimize_all_campaigns(self, min_spend: float = 50.0) -> Dict[str, Any]:
        """Otimizar todas as campanhas ativas"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Obter campanhas ativas com gasto mínimo
            campaigns = cursor.execute("""
                SELECT c.id, c.name, c.status, m.spend
                FROM campaigns c
                LEFT JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE c.status = 'Active' AND m.spend >= ?
            """, (min_spend,)).fetchall()
            
            conn.close()
            
            results = []
            
            for campaign in campaigns:
                result = self.auto_optimize_campaign(campaign["id"])
                results.append({
                    "campaign_id": campaign["id"],
                    "campaign_name": campaign["name"],
                    "optimization_result": result
                })
            
            return {
                "success": True,
                "total_campaigns": len(results),
                "results": results
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao otimizar campanhas: {str(e)}"}
    
    # ===== TESTES A/B =====
    
    def create_ab_test(self, campaign_id: int, variant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar teste A/B para campanha"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Criar registro de teste A/B
            cursor.execute("""
                INSERT INTO ab_tests (
                    campaign_id, variant_a, variant_b, 
                    test_type, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                campaign_id,
                json.dumps(variant_data.get("variant_a", {})),
                json.dumps(variant_data.get("variant_b", {})),
                variant_data.get("test_type", "creative"),
                "running",
                datetime.now().isoformat()
            ))
            
            test_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "test_id": test_id,
                "message": "Teste A/B criado com sucesso"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar teste A/B: {str(e)}"}
    
    def analyze_ab_test(self, test_id: int) -> Dict[str, Any]:
        """Analisar resultados de teste A/B"""
        if not self.is_configured():
            return {"success": False, "message": "Serviço não configurado"}
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            test = cursor.execute(
                "SELECT * FROM ab_tests WHERE id = ?",
                (test_id,)
            ).fetchone()
            
            conn.close()
            
            if not test:
                return {"success": False, "message": "Teste não encontrado"}
            
            # Usar IA para analisar resultados
            prompt = f"""
Analise os resultados do teste A/B abaixo e determine o vencedor.

Teste:
- Tipo: {test["test_type"]}
- Status: {test["status"]}

Variante A:
{test["variant_a"]}

Variante B:
{test["variant_b"]}

Forneça:
1. Variante vencedora (A ou B)
2. Nível de confiança (%)
3. Diferença de performance
4. Recomendação final
5. Próximos passos

Responda em formato JSON:
{{
  "winner": "A",
  "confidence": 95,
  "performance_diff": "+25% CTR",
  "recommendation": "...",
  "next_steps": ["...", "..."]
}}
"""
            
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de testes A/B."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "test": dict(test),
                "analysis": analysis
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao analisar teste A/B: {str(e)}"}


# Instância global do serviço
campaign_optimizer = CampaignOptimizerService()


# Funções helper
def optimize_campaign(campaign_id: int) -> Dict[str, Any]:
    """Otimizar campanha específica"""
    return campaign_optimizer.auto_optimize_campaign(campaign_id)


def optimize_all_active_campaigns() -> Dict[str, Any]:
    """Otimizar todas as campanhas ativas"""
    return campaign_optimizer.optimize_all_campaigns()


def get_optimization_recommendations(campaign_id: int) -> Dict[str, Any]:
    """Obter recomendações de otimização"""
    return campaign_optimizer.get_ai_recommendations(campaign_id)

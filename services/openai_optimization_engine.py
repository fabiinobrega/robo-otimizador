"""
MANUS OPTIMIZATION ENGINE
Motor de otimização usando EXCLUSIVAMENTE Manus AI
OpenAI foi REMOVIDA conforme solicitação do usuário.
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

# Importar Manus AI Service (ÚNICO provedor de IA)
from services.manus_ai_service import manus_ai


class OpenAIOptimizationEngine:
    """
    Motor de otimização baseado em Manus AI (nome mantido para compatibilidade)
    
    Responsabilidades:
    - Avaliação inteligente de campanhas
    - Recomendações de performance
    - Raciocínio avançado sobre dados
    - Tomada de decisão estratégica
    
    NOTA: Usa APENAS Manus AI. OpenAI foi removida.
    """
    
    def __init__(self):
        self.manus_ai = manus_ai
        
    def evaluate_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Avaliar campanha com critérios profissionais
        
        Args:
            campaign_data: Dados da campanha
            
        Returns:
            Avaliação completa
        """
        try:
            prompt = f"""
            Como auditor de campanhas de marketing, avalie esta campanha:
            
            Campanha: {campaign_data.get('name', 'Não informado')}
            Objetivo: {campaign_data.get('objective', 'Conversões')}
            Orçamento: R$ {campaign_data.get('budget', 0)}/dia
            
            Avalie em 10 critérios (nota 0-10 cada):
            1. Alinhamento com objetivo
            2. Qualidade do copy
            3. Segmentação de público
            4. Estratégia de lances
            5. Estrutura da campanha
            6. Performance vs benchmarks
            7. Eficiência de custo
            8. Potencial de escala
            9. Qualidade do tráfego
            10. ROI geral
            
            Retorne em formato JSON estruturado.
            """
            
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um auditor de campanhas de marketing digital."
            )
            
            if result:
                result['evaluated_at'] = datetime.now().isoformat()
                result['campaign_name'] = campaign_data.get('name')
                return {"success": True, "evaluation": result}
                
        except Exception as e:
            pass
            
        return {"success": False, "error": "Manus AI temporariamente indisponível"}
    
    def analyze_performance_trends(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analisar tendências de performance
        """
        try:
            data_summary = []
            for i, data in enumerate(historical_data[-30:], 1):
                data_summary.append({
                    "day": i,
                    "impressions": data.get('impressions', 0),
                    "clicks": data.get('clicks', 0),
                    "conversions": data.get('conversions', 0),
                    "cost": data.get('cost', 0),
                    "revenue": data.get('revenue', 0)
                })
            
            prompt = f"""
            Como analista de dados de marketing, analise estas tendências dos últimos 30 dias:
            
            Dados: {json.dumps(data_summary[:10], indent=2)}
            
            Analise:
            1. Tendências gerais
            2. Padrões identificados
            3. Anomalias
            4. Previsão para próximos 7 dias
            5. Recomendações de ação
            
            Retorne em formato JSON estruturado.
            """
            
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um analista de dados de marketing."
            )
            
            if result:
                result['analyzed_at'] = datetime.now().isoformat()
                result['days_analyzed'] = len(data_summary)
                return {"success": True, "analysis": result}
                
        except Exception as e:
            pass
            
        return {"success": False, "error": "Manus AI temporariamente indisponível"}
    
    def recommend_budget_allocation(self, campaigns: List[Dict[str, Any]], total_budget: float) -> Dict[str, Any]:
        """
        Recomendar alocação de orçamento
        """
        try:
            campaigns_summary = []
            for camp in campaigns:
                campaigns_summary.append({
                    "name": camp.get('name'),
                    "current_budget": camp.get('budget', 0),
                    "roas": camp.get('roas', 0),
                    "conversions": camp.get('conversions', 0)
                })
            
            prompt = f"""
            Como consultor financeiro de marketing, recomende a melhor alocação de orçamento:
            
            Orçamento Total: R$ {total_budget}/dia
            Campanhas: {json.dumps(campaigns_summary, indent=2)}
            
            Recomende:
            1. Alocação ideal para cada campanha
            2. Justificativa
            3. Campanhas para escalar
            4. Campanhas para pausar
            
            Retorne em formato JSON estruturado.
            """
            
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um consultor financeiro de marketing."
            )
            
            if result:
                result['recommended_at'] = datetime.now().isoformat()
                result['total_budget'] = total_budget
                return {"success": True, "recommendation": result}
                
        except Exception as e:
            pass
            
        return {"success": False, "error": "Manus AI temporariamente indisponível"}
    
    def diagnose_low_performance(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnosticar campanha com baixa performance
        """
        try:
            prompt = f"""
            Como especialista em troubleshooting de campanhas, diagnostique este problema:
            
            Campanha: {campaign_data.get('name', 'Não informado')}
            Problema: {campaign_data.get('issue', 'Baixa performance')}
            
            Diagnostique:
            1. Problema principal identificado
            2. Causas raiz
            3. Soluções possíveis
            4. Plano de ação
            
            Retorne em formato JSON estruturado.
            """
            
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um especialista em troubleshooting de campanhas."
            )
            
            if result:
                result['diagnosed_at'] = datetime.now().isoformat()
                result['campaign_name'] = campaign_data.get('name')
                return {"success": True, "diagnosis": result}
                
        except Exception as e:
            pass
            
        return {"success": False, "error": "Manus AI temporariamente indisponível"}
    
    def suggest_scaling_strategy(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sugerir estratégia de escala
        """
        try:
            prompt = f"""
            Como especialista em escala de campanhas, crie uma estratégia para:
            
            Campanha: {campaign_data.get('name', 'Não informado')}
            Orçamento Atual: R$ {campaign_data.get('current_budget', 0)}/dia
            ROAS Atual: {campaign_data.get('roas', 0)}
            
            Crie uma estratégia de escala com:
            1. Viabilidade de escala
            2. Plano de escala gradual
            3. Métricas para monitorar
            4. Sinais de alerta
            
            Retorne em formato JSON estruturado.
            """
            
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um especialista em escala de campanhas."
            )
            
            if result:
                result['suggested_at'] = datetime.now().isoformat()
                result['campaign_name'] = campaign_data.get('name')
                return {"success": True, "strategy": result}
                
        except Exception as e:
            pass
            
        return {"success": False, "error": "Manus AI temporariamente indisponível"}


# Instância global
optimization_engine = OpenAIOptimizationEngine()

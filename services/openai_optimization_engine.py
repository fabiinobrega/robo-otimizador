"""
OPENAI OPTIMIZATION ENGINE
Motor de otimização usando ChatGPT para análise e recomendações
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

class OpenAIOptimizationEngine:
    """
    Motor de otimização baseado em ChatGPT
    
    Responsabilidades:
    - Avaliação inteligente de campanhas
    - Recomendações de performance
    - Raciocínio avançado sobre dados
    - Tomada de decisão estratégica
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-4"
        
    def evaluate_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Avaliar campanha com critérios profissionais
        
        Args:
            campaign_data: Dados da campanha
            
        Returns:
            Avaliação completa
        """
        prompt = f"""
        Como auditor de campanhas de marketing, avalie esta campanha:
        
        **Campanha:** {campaign_data.get('name', 'Não informado')}
        **Objetivo:** {campaign_data.get('objective', 'Conversões')}
        **Orçamento:** R$ {campaign_data.get('budget', 0)}/dia
        **Duração:** {campaign_data.get('duration', 0)} dias
        
        **Performance:**
        - Impressões: {campaign_data.get('impressions', 0):,}
        - Cliques: {campaign_data.get('clicks', 0):,}
        - CTR: {campaign_data.get('ctr', 0):.2f}%
        - Conversões: {campaign_data.get('conversions', 0)}
        - Taxa de Conversão: {campaign_data.get('conversion_rate', 0):.2f}%
        - CPC: R$ {campaign_data.get('cpc', 0):.2f}
        - CPA: R$ {campaign_data.get('cpa', 0):.2f}
        - ROAS: {campaign_data.get('roas', 0):.2f}
        
        **Copy:**
        - Headlines: {', '.join(campaign_data.get('headlines', [])[:3])}
        - Descrições: {', '.join(campaign_data.get('descriptions', [])[:2])}
        
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
        
        Para cada critério, forneça:
        - Nota (0-10)
        - Justificativa
        - Pontos fortes
        - Pontos fracos
        - Recomendações específicas
        
        Forneça também:
        - Nota geral (média ponderada)
        - Classificação (Excelente/Bom/Regular/Ruim)
        - 3 vitórias rápidas (quick wins)
        - 3 melhorias de médio prazo
        - Decisão: Escalar/Manter/Pausar
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            evaluation = self._parse_json_response(response)
            
            evaluation['evaluated_at'] = datetime.now().isoformat()
            evaluation['campaign_name'] = campaign_data.get('name')
            
            return {
                "success": True,
                "evaluation": evaluation
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_performance_trends(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analisar tendências de performance
        
        Args:
            historical_data: Dados históricos
            
        Returns:
            Análise de tendências
        """
        # Preparar dados para o GPT
        data_summary = []
        for i, data in enumerate(historical_data[-30:], 1):  # Últimos 30 dias
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
        
        **Dados:**
        {json.dumps(data_summary, indent=2)}
        
        Analise:
        1. Tendências gerais (crescimento, estabilidade, declínio)
        2. Padrões identificados (sazonalidade, dias da semana, etc)
        3. Anomalias e outliers
        4. Correlações entre métricas
        5. Previsão para próximos 7 dias
        6. Fatores que podem estar influenciando
        7. Oportunidades identificadas
        8. Riscos identificados
        9. Recomendações de ação
        10. Próximos passos
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            analysis = self._parse_json_response(response)
            
            analysis['analyzed_at'] = datetime.now().isoformat()
            analysis['days_analyzed'] = len(data_summary)
            
            return {
                "success": True,
                "analysis": analysis
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def recommend_budget_allocation(self, campaigns: List[Dict[str, Any]], total_budget: float) -> Dict[str, Any]:
        """
        Recomendar alocação de orçamento
        
        Args:
            campaigns: Lista de campanhas
            total_budget: Orçamento total
            
        Returns:
            Recomendação de alocação
        """
        campaigns_summary = []
        for camp in campaigns:
            campaigns_summary.append({
                "name": camp.get('name'),
                "current_budget": camp.get('budget', 0),
                "roas": camp.get('roas', 0),
                "conversions": camp.get('conversions', 0),
                "cpa": camp.get('cpa', 0),
                "potential": camp.get('potential_scale', 'medium')
            })
        
        prompt = f"""
        Como consultor financeiro de marketing, recomende a melhor alocação de orçamento:
        
        **Orçamento Total:** R$ {total_budget:,.2f}/dia
        
        **Campanhas:**
        {json.dumps(campaigns_summary, indent=2)}
        
        Recomende:
        1. Alocação ideal para cada campanha
        2. Justificativa para cada alocação
        3. Campanhas para escalar
        4. Campanhas para reduzir
        5. Campanhas para pausar
        6. ROI esperado da nova alocação
        7. Riscos da mudança
        8. Plano de implementação gradual
        9. Métricas para monitorar
        10. Critérios de sucesso
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            recommendation = self._parse_json_response(response)
            
            recommendation['recommended_at'] = datetime.now().isoformat()
            recommendation['total_budget'] = total_budget
            
            return {
                "success": True,
                "recommendation": recommendation
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def diagnose_low_performance(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnosticar campanha com baixa performance
        
        Args:
            campaign_data: Dados da campanha
            
        Returns:
            Diagnóstico completo
        """
        prompt = f"""
        Como especialista em troubleshooting de campanhas, diagnostique este problema:
        
        **Campanha:** {campaign_data.get('name', 'Não informado')}
        **Problema:** {campaign_data.get('issue', 'Baixa performance')}
        
        **Métricas:**
        - CTR: {campaign_data.get('ctr', 0):.2f}% (Benchmark: 2-5%)
        - Taxa de Conversão: {campaign_data.get('conversion_rate', 0):.2f}% (Benchmark: 2-4%)
        - CPA: R$ {campaign_data.get('cpa', 0):.2f} (Target: R$ {campaign_data.get('target_cpa', 0):.2f})
        - ROAS: {campaign_data.get('roas', 0):.2f} (Target: {campaign_data.get('target_roas', 0):.2f})
        
        **Configuração:**
        - Segmentação: {campaign_data.get('targeting', 'Não informado')}
        - Lances: {campaign_data.get('bidding', 'Não informado')}
        - Orçamento: R$ {campaign_data.get('budget', 0)}/dia
        
        Diagnostique:
        1. Problema principal identificado
        2. Causas raiz (análise de 5 porquês)
        3. Sintomas secundários
        4. Impacto no negócio
        5. Urgência (Alta/Média/Baixa)
        6. Soluções possíveis (mínimo 3)
        7. Solução recomendada
        8. Plano de ação passo a passo
        9. Tempo estimado para correção
        10. Resultados esperados
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            diagnosis = self._parse_json_response(response)
            
            diagnosis['diagnosed_at'] = datetime.now().isoformat()
            diagnosis['campaign_name'] = campaign_data.get('name')
            
            return {
                "success": True,
                "diagnosis": diagnosis
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def suggest_scaling_strategy(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sugerir estratégia de escala
        
        Args:
            campaign_data: Dados da campanha
            
        Returns:
            Estratégia de escala
        """
        prompt = f"""
        Como especialista em escala de campanhas, crie uma estratégia para:
        
        **Campanha:** {campaign_data.get('name', 'Não informado')}
        **Orçamento Atual:** R$ {campaign_data.get('current_budget', 0)}/dia
        **ROAS Atual:** {campaign_data.get('roas', 0):.2f}
        **Conversões/dia:** {campaign_data.get('daily_conversions', 0)}
        **Orçamento Desejado:** R$ {campaign_data.get('target_budget', 0)}/dia
        
        Crie uma estratégia de escala com:
        1. Viabilidade de escala (0-100%)
        2. Riscos identificados
        3. Plano de escala gradual (semana a semana)
        4. Incrementos de orçamento recomendados
        5. Métricas para monitorar
        6. Sinais de alerta
        7. Plano B se performance cair
        8. Otimizações paralelas necessárias
        9. Timeline de execução
        10. ROI esperado em cada etapa
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            strategy = self._parse_json_response(response)
            
            strategy['created_at'] = datetime.now().isoformat()
            strategy['campaign_name'] = campaign_data.get('name')
            
            return {
                "success": True,
                "strategy": strategy
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _call_gpt(self, prompt: str, temperature: float = 0.5) -> str:
        """Chamar API do ChatGPT"""
        if not self.api_key:
            return json.dumps({"error": "API key not configured"})
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Você é um consultor de marketing digital e analista de dados de classe mundial. Sempre responda em formato JSON estruturado e em português. Seja preciso, analítico e orientado a resultados."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return json.dumps({"error": f"API returned status {response.status_code}"})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse resposta JSON do GPT"""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except:
            return {"response": response}

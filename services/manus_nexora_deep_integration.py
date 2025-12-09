"""
MANUS + NEXORA - INTEGRAÇÃO AVANÇADA PROFUNDA
Sistema de conexão profunda entre assistentes, IA, copilotos e automação
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any

class ManusNexoraDeepIntegration:
    """
    Integração profunda entre Manus AI e Nexora Prime
    
    Funcionalidades:
    - Geração automática de campanhas completas
    - Escrita de anúncios com IA
    - Direcionamento inteligente de verba
    - Testes A/B automatizados
    - Otimização de funis de vendas
    - Integração de dados de retorno e conversão
    """
    
    def __init__(self):
        self.manus_api_key = os.getenv('OPENAI_API_KEY', '')
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-4.1-mini"
        
    def generate_complete_campaign(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerar campanha completa com IA
        
        Args:
            product_data: Dados do produto/serviço
            
        Returns:
            Campanha completa gerada
        """
        prompt = f"""
        Crie uma campanha de marketing completa para o seguinte produto:
        
        Nome: {product_data.get('name', 'Produto')}
        Descrição: {product_data.get('description', 'Sem descrição')}
        Público-alvo: {product_data.get('target_audience', 'Geral')}
        Orçamento: R$ {product_data.get('budget', 1000)}/dia
        Objetivo: {product_data.get('objective', 'Conversões')}
        
        Gere:
        1. Nome da campanha (criativo e impactante)
        2. 5 headlines diferentes
        3. 3 descrições longas
        4. 10 palavras-chave principais
        5. Segmentação demográfica recomendada
        6. Estratégia de lances
        7. Distribuição de orçamento por plataforma
        
        Formato JSON.
        """
        
        try:
            response = self._call_ai(prompt)
            campaign = self._parse_campaign_response(response)
            
            # Adicionar metadados
            campaign['generated_at'] = datetime.now().isoformat()
            campaign['product_data'] = product_data
            campaign['status'] = 'draft'
            
            return {
                "success": True,
                "campaign": campaign
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def write_ad_copy(self, campaign_data: Dict[str, Any], platform: str = "google") -> Dict[str, Any]:
        """
        Escrever copy de anúncio automaticamente
        
        Args:
            campaign_data: Dados da campanha
            platform: Plataforma (google, facebook, etc)
            
        Returns:
            Copy gerado
        """
        prompt = f"""
        Escreva copy de anúncio para {platform.upper()} com base nesta campanha:
        
        Campanha: {campaign_data.get('name', 'Campanha')}
        Produto: {campaign_data.get('product', 'Produto')}
        Objetivo: {campaign_data.get('objective', 'Conversões')}
        Público: {campaign_data.get('audience', 'Geral')}
        
        Gere 3 variações de anúncio completo com:
        - Headline (máx 30 caracteres)
        - Description 1 (máx 90 caracteres)
        - Description 2 (máx 90 caracteres)
        - Call-to-action
        - Palavras-chave de destaque
        
        Formato JSON.
        """
        
        try:
            response = self._call_ai(prompt)
            ads = self._parse_ads_response(response)
            
            return {
                "success": True,
                "platform": platform,
                "ads": ads,
                "count": len(ads)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def optimize_budget_allocation(self, campaigns: List[Dict], total_budget: float) -> Dict[str, Any]:
        """
        Direcionar verba inteligentemente entre campanhas
        
        Args:
            campaigns: Lista de campanhas
            total_budget: Orçamento total disponível
            
        Returns:
            Distribuição otimizada de orçamento
        """
        # Analisar performance de cada campanha
        campaign_scores = []
        for campaign in campaigns:
            score = self._calculate_campaign_score(campaign)
            campaign_scores.append({
                "campaign_id": campaign.get('id'),
                "campaign_name": campaign.get('name'),
                "score": score,
                "current_budget": campaign.get('budget', 0)
            })
        
        # Ordenar por score
        campaign_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Distribuir orçamento proporcionalmente ao score
        total_score = sum(c['score'] for c in campaign_scores)
        
        allocations = []
        for campaign in campaign_scores:
            allocation_percentage = (campaign['score'] / total_score) * 100
            allocated_budget = (campaign['score'] / total_score) * total_budget
            
            allocations.append({
                "campaign_id": campaign['campaign_id'],
                "campaign_name": campaign['campaign_name'],
                "score": campaign['score'],
                "allocation_percentage": round(allocation_percentage, 2),
                "allocated_budget": round(allocated_budget, 2),
                "current_budget": campaign['current_budget'],
                "budget_change": round(allocated_budget - campaign['current_budget'], 2)
            })
        
        return {
            "success": True,
            "total_budget": total_budget,
            "allocations": allocations,
            "optimization_date": datetime.now().isoformat()
        }
    
    def create_ab_test(self, campaign_id: int, variations: List[Dict]) -> Dict[str, Any]:
        """
        Criar teste A/B automatizado
        
        Args:
            campaign_id: ID da campanha
            variations: Variações para testar
            
        Returns:
            Teste A/B criado
        """
        if len(variations) < 2:
            return {
                "success": False,
                "error": "Mínimo de 2 variações necessárias"
            }
        
        test = {
            "test_id": f"ab_test_{campaign_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "campaign_id": campaign_id,
            "variations": variations,
            "status": "running",
            "start_date": datetime.now().isoformat(),
            "end_date": None,
            "winner": None,
            "metrics": {
                "impressions": 0,
                "clicks": 0,
                "conversions": 0,
                "cost": 0
            }
        }
        
        return {
            "success": True,
            "test": test
        }
    
    def optimize_sales_funnel(self, funnel_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Otimizar funil de vendas com IA
        
        Args:
            funnel_data: Dados do funil atual
            
        Returns:
            Recomendações de otimização
        """
        prompt = f"""
        Analise este funil de vendas e sugira otimizações:
        
        Estágios:
        - Awareness: {funnel_data.get('awareness', 0)} visitantes
        - Interest: {funnel_data.get('interest', 0)} interessados
        - Consideration: {funnel_data.get('consideration', 0)} considerando
        - Decision: {funnel_data.get('decision', 0)} decidindo
        - Purchase: {funnel_data.get('purchase', 0)} compraram
        
        Taxa de conversão atual: {funnel_data.get('conversion_rate', 0)}%
        Ticket médio: R$ {funnel_data.get('average_ticket', 0)}
        
        Sugira:
        1. Gargalos identificados
        2. Ações para melhorar cada estágio
        3. Conteúdo recomendado
        4. Automações sugeridas
        5. Meta de conversão otimizada
        
        Formato JSON.
        """
        
        try:
            response = self._call_ai(prompt)
            recommendations = self._parse_funnel_response(response)
            
            return {
                "success": True,
                "current_funnel": funnel_data,
                "recommendations": recommendations,
                "analyzed_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def integrate_conversion_data(self, campaign_id: int, conversion_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrar dados de conversão e retorno
        
        Args:
            campaign_id: ID da campanha
            conversion_data: Dados de conversão
            
        Returns:
            Análise de conversão
        """
        # Calcular métricas
        impressions = conversion_data.get('impressions', 0)
        clicks = conversion_data.get('clicks', 0)
        conversions = conversion_data.get('conversions', 0)
        cost = conversion_data.get('cost', 0)
        revenue = conversion_data.get('revenue', 0)
        
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
        cpc = (cost / clicks) if clicks > 0 else 0
        cpa = (cost / conversions) if conversions > 0 else 0
        roas = (revenue / cost) if cost > 0 else 0
        roi = ((revenue - cost) / cost * 100) if cost > 0 else 0
        
        analysis = {
            "campaign_id": campaign_id,
            "metrics": {
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "cost": round(cost, 2),
                "revenue": round(revenue, 2)
            },
            "kpis": {
                "ctr": round(ctr, 2),
                "conversion_rate": round(conversion_rate, 2),
                "cpc": round(cpc, 2),
                "cpa": round(cpa, 2),
                "roas": round(roas, 2),
                "roi": round(roi, 2)
            },
            "performance": self._classify_performance(roas, roi),
            "recommendations": self._generate_recommendations(ctr, conversion_rate, roas),
            "analyzed_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "analysis": analysis
        }
    
    def _call_ai(self, prompt: str) -> str:
        """Chamar API da IA"""
        if not self.manus_api_key:
            return json.dumps({
                "campaign_name": "Campanha Gerada por IA",
                "headlines": ["Headline 1", "Headline 2", "Headline 3"],
                "descriptions": ["Descrição 1", "Descrição 2"],
                "keywords": ["palavra1", "palavra2", "palavra3"]
            })
        
        try:
            headers = {
                "Authorization": f"Bearer {self.manus_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Você é um especialista em marketing digital e criação de campanhas."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return json.dumps({"error": "API call failed"})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _parse_campaign_response(self, response: str) -> Dict[str, Any]:
        """Parse resposta de campanha"""
        try:
            return json.loads(response)
        except:
            return {
                "campaign_name": "Campanha Gerada",
                "headlines": ["Headline 1", "Headline 2"],
                "descriptions": ["Descrição 1"],
                "keywords": ["palavra1", "palavra2"]
            }
    
    def _parse_ads_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse resposta de anúncios"""
        try:
            data = json.loads(response)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'ads' in data:
                return data['ads']
            else:
                return [data]
        except:
            return [{
                "headline": "Anúncio Gerado",
                "description1": "Descrição 1",
                "description2": "Descrição 2",
                "cta": "Saiba Mais"
            }]
    
    def _parse_funnel_response(self, response: str) -> Dict[str, Any]:
        """Parse resposta de funil"""
        try:
            return json.loads(response)
        except:
            return {
                "bottlenecks": ["Awareness → Interest"],
                "actions": ["Melhorar copy", "Aumentar segmentação"],
                "target_conversion": 5.0
            }
    
    def _calculate_campaign_score(self, campaign: Dict[str, Any]) -> float:
        """Calcular score de campanha"""
        # Fatores: CTR, Conversion Rate, ROAS, ROI
        ctr = campaign.get('ctr', 0)
        conversion_rate = campaign.get('conversion_rate', 0)
        roas = campaign.get('roas', 0)
        roi = campaign.get('roi', 0)
        
        # Pesos
        score = (ctr * 0.2) + (conversion_rate * 0.3) + (roas * 0.3) + (roi * 0.2)
        
        return max(0, min(100, score))
    
    def _classify_performance(self, roas: float, roi: float) -> str:
        """Classificar performance"""
        if roas >= 4.0 and roi >= 300:
            return "Excelente"
        elif roas >= 2.0 and roi >= 100:
            return "Bom"
        elif roas >= 1.0 and roi >= 0:
            return "Regular"
        else:
            return "Ruim"
    
    def _generate_recommendations(self, ctr: float, conversion_rate: float, roas: float) -> List[str]:
        """Gerar recomendações"""
        recommendations = []
        
        if ctr < 2.0:
            recommendations.append("Melhorar headlines e descrições para aumentar CTR")
        
        if conversion_rate < 3.0:
            recommendations.append("Otimizar landing page e processo de conversão")
        
        if roas < 2.0:
            recommendations.append("Revisar segmentação e palavras-chave")
        
        if not recommendations:
            recommendations.append("Campanha performando bem, continue monitorando")
        
        return recommendations

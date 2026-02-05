"""
MANUS STRATEGIC ENGINE
Motor estratégico usando EXCLUSIVAMENTE Manus AI
OpenAI foi REMOVIDA conforme solicitação do usuário.
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

# Importar Manus AI Service (ÚNICO provedor de IA)
from services.manus_ai_service import manus_ai


class OpenAIStrategicEngine:
    """
    Motor estratégico baseado em Manus AI (nome mantido para compatibilidade)
    
    Responsabilidades:
    - Análise de persona e público-alvo
    - Análise de mercado e concorrência
    - Criação de estratégias de marketing
    - Planejamento de funis de venda
    - Estratégias de teste A/B
    - Otimização contínua
    
    NOTA: Usa APENAS Manus AI. OpenAI foi removida.
    """
    
    def __init__(self):
        self.manus_ai = manus_ai
        
    def analyze_persona(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisar e criar persona detalhada
        
        Args:
            business_data: Dados do negócio
            
        Returns:
            Persona completa
        """
        prompt = f"""
        Como especialista em marketing digital, analise este negócio e crie uma persona detalhada:
        
        **Negócio:**
        - Nome: {business_data.get('name', 'Não informado')}
        - Setor: {business_data.get('industry', 'Não informado')}
        - Produto/Serviço: {business_data.get('product', 'Não informado')}
        - Ticket Médio: R$ {business_data.get('average_ticket', 0)}
        - Localização: {business_data.get('location', 'Brasil')}
        
        Crie uma persona completa com:
        1. Nome fictício
        2. Idade e demografia
        3. Ocupação e renda
        4. Dores e desafios
        5. Objetivos e aspirações
        6. Comportamento online
        7. Canais preferidos
        8. Objeções comuns
        9. Gatilhos de compra
        10. Jornada de compra
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            persona = self._parse_json_response(response)
            
            persona['generated_at'] = datetime.now().isoformat()
            persona['business_name'] = business_data.get('name')
            
            return {
                "success": True,
                "persona": persona
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_market(self, industry: str, location: str = "Brasil") -> Dict[str, Any]:
        """
        Analisar mercado e concorrência
        
        Args:
            industry: Setor/indústria
            location: Localização
            
        Returns:
            Análise de mercado
        """
        prompt = f"""
        Como analista de mercado, faça uma análise completa do setor {industry} em {location}:
        
        Analise:
        1. Tamanho do mercado e crescimento
        2. Principais players e market share
        3. Tendências atuais
        4. Oportunidades e ameaças
        5. Barreiras de entrada
        6. Comportamento do consumidor
        7. Canais de marketing mais efetivos
        8. Faixa de preço praticada
        9. Sazonalidade
        10. Recomendações estratégicas
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            analysis = self._parse_json_response(response)
            
            analysis['analyzed_at'] = datetime.now().isoformat()
            analysis['industry'] = industry
            analysis['location'] = location
            
            return {
                "success": True,
                "analysis": analysis
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_marketing_strategy(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar estratégia de marketing completa
        
        Args:
            campaign_data: Dados da campanha
            
        Returns:
            Estratégia completa
        """
        prompt = f"""
        Como estrategista de marketing digital, crie uma estratégia completa para esta campanha:
        
        **Campanha:**
        - Objetivo: {campaign_data.get('objective', 'Conversões')}
        - Produto: {campaign_data.get('product', 'Não informado')}
        - Público: {campaign_data.get('target_audience', 'Geral')}
        - Orçamento: R$ {campaign_data.get('budget', 0)}/dia
        - Duração: {campaign_data.get('duration', 30)} dias
        - Plataformas: {', '.join(campaign_data.get('platforms', ['Google', 'Facebook']))}
        
        Crie uma estratégia com:
        1. Posicionamento e proposta de valor
        2. Mensagem principal
        3. Segmentação detalhada
        4. Estratégia de lances
        5. Distribuição de orçamento por plataforma
        6. Tipos de anúncios recomendados
        7. Landing page strategy
        8. Funil de conversão
        9. KPIs e metas
        10. Cronograma de execução
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            strategy = self._parse_json_response(response)
            
            strategy['created_at'] = datetime.now().isoformat()
            strategy['campaign_objective'] = campaign_data.get('objective')
            
            return {
                "success": True,
                "strategy": strategy
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_sales_funnel(self, funnel_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar estratégia de funil de vendas
        
        Args:
            funnel_data: Dados do funil
            
        Returns:
            Funil completo
        """
        prompt = f"""
        Como especialista em funis de venda, crie um funil completo para:
        
        **Produto/Serviço:** {funnel_data.get('product', 'Não informado')}
        **Preço:** R$ {funnel_data.get('price', 0)}
        **Público:** {funnel_data.get('audience', 'Geral')}
        **Objetivo:** {funnel_data.get('objective', 'Vendas')}
        
        Crie um funil com:
        1. Estágios do funil (Topo, Meio, Fundo)
        2. Conteúdo para cada estágio
        3. Canais de aquisição
        4. Estratégia de nutrição
        5. Gatilhos de conversão
        6. Automações recomendadas
        7. Métricas de sucesso
        8. Tempo médio por estágio
        9. Taxa de conversão esperada
        10. Pontos de otimização
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            funnel = self._parse_json_response(response)
            
            funnel['created_at'] = datetime.now().isoformat()
            funnel['product'] = funnel_data.get('product')
            
            return {
                "success": True,
                "funnel": funnel
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_ab_test_strategy(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar estratégia de teste A/B
        
        Args:
            test_data: Dados do teste
            
        Returns:
            Estratégia de teste
        """
        prompt = f"""
        Como especialista em testes A/B, crie uma estratégia de teste para:
        
        **Elemento a testar:** {test_data.get('element', 'Headline')}
        **Objetivo:** {test_data.get('objective', 'Aumentar CTR')}
        **Tráfego disponível:** {test_data.get('traffic', 1000)}/dia
        **Duração:** {test_data.get('duration', 14)} dias
        
        Crie uma estratégia com:
        1. Hipótese do teste
        2. Variações recomendadas (mínimo 3)
        3. Tamanho da amostra necessário
        4. Nível de significância
        5. Métricas primárias e secundárias
        6. Critérios de sucesso
        7. Duração ideal do teste
        8. Análise de riscos
        9. Plano de implementação do vencedor
        10. Próximos testes recomendados
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            strategy = self._parse_json_response(response)
            
            strategy['created_at'] = datetime.now().isoformat()
            strategy['element'] = test_data.get('element')
            
            return {
                "success": True,
                "strategy": strategy
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def recommend_optimization(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recomendar otimizações baseadas em performance
        
        Args:
            performance_data: Dados de performance
            
        Returns:
            Recomendações de otimização
        """
        prompt = f"""
        Como consultor de performance de marketing, analise estes dados e recomende otimizações:
        
        **Performance Atual:**
        - Impressões: {performance_data.get('impressions', 0):,}
        - Cliques: {performance_data.get('clicks', 0):,}
        - CTR: {performance_data.get('ctr', 0):.2f}%
        - Conversões: {performance_data.get('conversions', 0)}
        - Taxa de Conversão: {performance_data.get('conversion_rate', 0):.2f}%
        - Custo: R$ {performance_data.get('cost', 0):,.2f}
        - CPC: R$ {performance_data.get('cpc', 0):.2f}
        - CPA: R$ {performance_data.get('cpa', 0):.2f}
        - ROAS: {performance_data.get('roas', 0):.2f}
        
        Forneça:
        1. Análise geral da performance
        2. Pontos fortes identificados
        3. Gargalos e problemas
        4. 5 recomendações prioritárias
        5. Impacto esperado de cada recomendação
        6. Dificuldade de implementação
        7. Ordem de execução
        8. Métricas para acompanhar
        9. Alertas e cuidados
        10. Próximos passos
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            response = self._call_gpt(prompt)
            recommendations = self._parse_json_response(response)
            
            recommendations['analyzed_at'] = datetime.now().isoformat()
            recommendations['current_roas'] = performance_data.get('roas', 0)
            
            return {
                "success": True,
                "recommendations": recommendations
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _call_gpt(self, prompt: str, temperature: float = 0.7) -> str:
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
                        "content": "Você é um especialista em marketing digital e estratégia de negócios. Sempre responda em formato JSON estruturado e em português."
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
            # Tentar extrair JSON da resposta
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except:
            # Fallback: retornar resposta como texto
            return {"response": response}

"""
Competitor Spy Engine - Motor de Espionagem de Concorrência
Analisa anúncios concorrentes ANTES de gerar campanhas
Atualizado: 21/12/2024 - Migrado para Manus AI Service
"""

import os
import json
import logging
from datetime import datetime

# Importar Manus AI Service (substitui OpenAI)
from services.manus_ai_service import manus_ai

logger = logging.getLogger(__name__)


class CompetitorSpyEngine:
    """
    Motor de espionagem que analisa concorrentes antes de criar anúncios
    """
    
    def __init__(self):
        pass
    
    def analyze_competitors(self, product, niche, platform='facebook'):
        """
        Analisa concorrentes e gera relatório interno
        
        Args:
            product (str): Produto/serviço a ser anunciado
            niche (str): Nicho de mercado
            platform (str): Plataforma (facebook, google, etc)
            
        Returns:
            dict: Relatório de espionagem
        """
        try:
            # Gerar análise com Manus AI
            analysis = self._generate_spy_analysis(product, niche, platform)
            
            # Estruturar relatório
            report = {
                "timestamp": datetime.now().isoformat(),
                "product": product,
                "niche": niche,
                "platform": platform,
                "analysis": analysis,
                "status": "completed"
            }
            
            logger.info(f"Análise de concorrência concluída para {product} no nicho {niche}")
            return report
            
        except Exception as e:
            logger.error(f"Erro na análise de concorrência: {str(e)}")
            return self._get_fallback_analysis(product, niche, platform)
    
    def _generate_spy_analysis(self, product, niche, platform):
        """Gera análise usando Manus AI"""
        
        prompt = f"""
        Você é um especialista em análise competitiva de anúncios digitais.
        
        Analise o mercado de anúncios para:
        - Produto: {product}
        - Nicho: {niche}
        - Plataforma: {platform}
        
        Forneça uma análise DETALHADA incluindo:
        
        1. PRINCIPAIS CONCORRENTES (5-10)
           - Nome/marca
           - Posicionamento
           - Pontos fortes
           - Pontos fracos
        
        2. PADRÕES DE ANÚNCIOS IDENTIFICADOS
           - Headlines mais usados
           - CTAs mais comuns
           - Formatos predominantes
           - Cores e estilos visuais
        
        3. GAPS E OPORTUNIDADES
           - O que ninguém está fazendo
           - Ângulos inexplorados
           - Públicos negligenciados
        
        4. ESTRATÉGIAS DE DIFERENCIAÇÃO
           - Como se destacar
           - Unique Selling Propositions
           - Posicionamento recomendado
        
        5. ESTIMATIVAS DE INVESTIMENTO
           - Budget médio dos concorrentes
           - CPM/CPC estimados
           - ROAS típico do nicho
        
        Retorne em formato JSON estruturado.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um analista de inteligência competitiva especializado em marketing digital.",
            temperature=0.6
        )
        
        if result:
            return result
        
        return self._get_fallback_analysis(product, niche, platform)["analysis"]
    
    def _get_fallback_analysis(self, product, niche, platform):
        """Análise básica quando IA não está disponível"""
        return {
            "timestamp": datetime.now().isoformat(),
            "product": product,
            "niche": niche,
            "platform": platform,
            "analysis": {
                "competitors": [
                    {"name": "Concorrente A", "positioning": "Premium", "strengths": ["marca forte"], "weaknesses": ["preço alto"]},
                    {"name": "Concorrente B", "positioning": "Custo-benefício", "strengths": ["preço"], "weaknesses": ["qualidade"]},
                    {"name": "Concorrente C", "positioning": "Inovador", "strengths": ["tecnologia"], "weaknesses": ["pouco conhecido"]}
                ],
                "ad_patterns": {
                    "common_headlines": ["Transforme sua vida", "Resultados em 30 dias", "Oferta limitada"],
                    "common_ctas": ["Compre agora", "Saiba mais", "Comece grátis"],
                    "formats": ["Carrossel", "Vídeo curto", "Imagem única"],
                    "colors": ["Azul", "Laranja", "Verde"]
                },
                "opportunities": [
                    "Foco em sustentabilidade",
                    "Atendimento personalizado",
                    "Garantia estendida"
                ],
                "differentiation": {
                    "usp": "Único no mercado com [diferencial]",
                    "positioning": "Premium acessível",
                    "key_message": "Qualidade sem pagar mais"
                },
                "investment_estimates": {
                    "avg_budget": 5000,
                    "cpm_estimate": 15,
                    "cpc_estimate": 1.5,
                    "typical_roas": 3.0
                }
            },
            "status": "fallback"
        }
    
    def get_trending_angles(self, niche):
        """
        Identifica ângulos de venda em tendência no nicho
        """
        prompt = f"""
        Identifique os 10 ângulos de venda mais eficazes atualmente para o nicho: {niche}
        
        Para cada ângulo, forneça:
        - Nome do ângulo
        - Descrição
        - Exemplo de headline
        - Público-alvo ideal
        - Nível de saturação (baixo/médio/alto)
        
        Retorne em formato JSON.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é um especialista em copywriting e tendências de marketing.",
            temperature=0.7
        )
        
        if result:
            return result
        
        return {
            "angles": [
                {"name": "Urgência", "description": "Criar senso de escassez", "headline": "Últimas unidades!", "audience": "Compradores impulsivos", "saturation": "alto"},
                {"name": "Prova Social", "description": "Mostrar resultados de outros", "headline": "+10.000 clientes satisfeitos", "audience": "Cautelosos", "saturation": "médio"},
                {"name": "Transformação", "description": "Antes vs Depois", "headline": "De R$0 a R$10k/mês", "audience": "Aspiracionais", "saturation": "médio"},
                {"name": "Autoridade", "description": "Expertise e credenciais", "headline": "Método usado por especialistas", "audience": "Profissionais", "saturation": "baixo"},
                {"name": "Curiosidade", "description": "Gerar interesse", "headline": "O segredo que ninguém conta", "audience": "Curiosos", "saturation": "médio"}
            ]
        }


    def get_spy_summary(self, report):
        """
        Gera um resumo executivo do relatório de espionagem
        
        Args:
            report (dict): Relatório completo de espionagem
            
        Returns:
            dict: Resumo executivo
        """
        try:
            analysis = report.get('analysis', {})
            
            # Extrair informações principais
            competitors = analysis.get('competitors', [])
            ad_patterns = analysis.get('ad_patterns', {})
            opportunities = analysis.get('opportunities', [])
            investment = analysis.get('investment_estimates', {})
            
            summary = {
                "total_competitors_analyzed": len(competitors),
                "top_competitor": competitors[0].get('name', 'N/A') if competitors else 'N/A',
                "main_opportunity": opportunities[0] if opportunities else 'Não identificada',
                "recommended_budget": investment.get('avg_budget', 5000),
                "expected_cpc": investment.get('cpc_estimate', 1.5),
                "expected_roas": investment.get('typical_roas', 3.0),
                "most_used_format": ad_patterns.get('formats', ['Imagem única'])[0] if ad_patterns.get('formats') else 'Imagem única',
                "key_insight": f"Mercado com {len(competitors)} concorrentes ativos. Oportunidade em {opportunities[0] if opportunities else 'diferenciação'}",
                "action_items": [
                    "Criar anúncios com headlines diferenciados",
                    "Focar em ângulos inexplorados",
                    "Testar formatos menos saturados",
                    f"Budget inicial recomendado: R$ {investment.get('avg_budget', 5000)}"
                ]
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo: {str(e)}")
            return {
                "total_competitors_analyzed": 0,
                "top_competitor": "N/A",
                "main_opportunity": "Análise indisponível",
                "recommended_budget": 5000,
                "expected_cpc": 1.5,
                "expected_roas": 3.0,
                "most_used_format": "Imagem única",
                "key_insight": "Análise de concorrência em processamento",
                "action_items": ["Aguardar análise completa"]
            }


# Instância global
competitor_spy = CompetitorSpyEngine()

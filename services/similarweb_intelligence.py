"""
SIMILARWEB INTELLIGENCE - VIA MANUS IA
======================================

Integração Similarweb usando EXCLUSIVAMENTE créditos do Manus IA.

REGRAS ABSOLUTAS:
❌ NÃO criar integração direta com API da Similarweb
❌ NÃO solicitar credenciais da Similarweb ao usuário
❌ NÃO exigir assinatura paga da Similarweb
❌ NÃO usar OpenAI

✅ USAR APENAS Manus IA como intermediário
✅ CONSUMIR SOMENTE créditos do Manus
✅ LOGAR consumo de créditos
✅ FUNCIONAR MESMO SEM Similarweb externa

FLUXO:
1. Nexora chama SimilarwebIntelligence
2. SimilarwebIntelligence envia prompt estruturado ao Manus
3. Manus consulta Similarweb usando SEUS PRÓPRIOS CRÉDITOS
4. Manus retorna dados normalizados
5. Nexora processa, exibe e armazena os dados

Autor: Manus AI
Data: 13 de Janeiro de 2026
"""

import logging
import json
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Importar Manus AI Service
try:
    from services.manus_ai_service import manus_ai
    MANUS_AVAILABLE = True
except ImportError:
    MANUS_AVAILABLE = False
    manus_ai = None
    logger.warning("Manus AI Service não disponível")


class SimilarwebIntelligence:
    """
    Serviço de inteligência de mercado via Similarweb através do Manus IA.
    
    NÃO faz chamadas diretas à API Similarweb.
    Usa o Manus IA como intermediário, consumindo créditos do Manus.
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hora
        self.credits_used = 0
        
        logger.info("🔍 Similarweb Intelligence inicializado (via Manus IA)")
    
    def get_market_insights(
        self,
        domain: str,
        country: str = 'BR',
        timeframe: str = '3m'
    ) -> Optional[Dict[str, Any]]:
        """
        Obtém insights de mercado via Manus IA.
        
        O Manus IA consulta a Similarweb usando seus próprios créditos
        e retorna dados normalizados.
        
        Args:
            domain: Domínio do site a analisar (ex: 'amazon.com.br')
            country: Código do país (ex: 'BR', 'US', 'global')
            timeframe: Período de análise ('1m', '3m', '6m', '12m')
            
        Returns:
            Dicionário com insights de mercado ou None se indisponível
        """
        if not MANUS_AVAILABLE:
            logger.warning("Manus IA não disponível - Similarweb desabilitado")
            return None
        
        # Check cache
        cache_key = f"market_insights_{domain}_{country}_{timeframe}"
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if (datetime.now() - cached_time).seconds < self.cache_ttl:
                logger.info(f"✅ Cache hit para {domain}")
                return cached_data
        
        logger.info(f"🔍 Solicitando insights de mercado via Manus IA: {domain}")
        
        # Criar prompt estruturado para o Manus
        prompt = self._create_market_insights_prompt(domain, country, timeframe)
        
        try:
            # Solicitar ao Manus IA
            result = manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um analista de inteligência de mercado especializado em dados da Similarweb. Forneça dados precisos e estruturados.",
                temperature=0.3
            )
            
            if result:
                # Incrementar contador de créditos
                self.credits_used += 1
                
                # Adicionar metadata
                result['_metadata'] = {
                    'domain': domain,
                    'country': country,
                    'timeframe': timeframe,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'manus_ai',
                    'credits_used': 1
                }
                
                # Cache result
                self.cache[cache_key] = (result, datetime.now())
                
                logger.info(f"✅ Insights obtidos via Manus IA (créditos usados: {self.credits_used})")
                return result
            else:
                logger.warning(f"⚠️ Manus IA não retornou dados para {domain}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro ao obter insights via Manus IA: {str(e)}")
            return None
    
    def _create_market_insights_prompt(
        self,
        domain: str,
        country: str,
        timeframe: str
    ) -> str:
        """
        Cria prompt estruturado para solicitar dados ao Manus IA.
        
        O Manus IA interpretará este prompt e consultará a Similarweb
        usando seus próprios créditos e parceria oficial.
        """
        timeframe_map = {
            '1m': '1 mês',
            '3m': '3 meses',
            '6m': '6 meses',
            '12m': '12 meses'
        }
        
        timeframe_text = timeframe_map.get(timeframe, '3 meses')
        
        prompt = f"""
Você tem acesso à Similarweb através da sua parceria oficial.
Consulte os dados de mercado para o domínio: {domain}
País/Região: {country}
Período: {timeframe_text}

Forneça um relatório estruturado em JSON com os seguintes dados:

{{
  "traffic_overview": {{
    "total_visits": <número estimado de visitas totais>,
    "monthly_visits": <número estimado de visitas mensais>,
    "growth_rate": <taxa de crescimento em % (positivo ou negativo)>,
    "trend": "<'up' | 'down' | 'stable'>"
  }},
  "traffic_sources": {{
    "paid_search": <% de tráfego pago>,
    "organic_search": <% de tráfego orgânico>,
    "social": <% de tráfego de redes sociais>,
    "direct": <% de tráfego direto>,
    "referrals": <% de tráfego de referências>,
    "display_ads": <% de tráfego de display ads>
  }},
  "geography": {{
    "top_countries": [
      {{"country": "<país>", "percentage": <% de tráfego>}},
      ...
    ]
  }},
  "devices": {{
    "mobile": <% de tráfego mobile>,
    "desktop": <% de tráfego desktop>
  }},
  "engagement": {{
    "avg_visit_duration": <duração média em segundos>,
    "pages_per_visit": <páginas por visita>,
    "bounce_rate": <taxa de rejeição em %>
  }},
  "market_analysis": {{
    "market_trend": "<descrição da tendência de mercado>",
    "seasonality": "<se há sazonalidade identificada>",
    "top_competitors": [
      "<domínio concorrente 1>",
      "<domínio concorrente 2>",
      "<domínio concorrente 3>"
    ],
    "market_share_estimate": <estimativa de market share em % (se disponível)>
  }},
  "confidence_score": {{
    "score": <0-100, baseado na qualidade e volume de dados>,
    "classification": "<'high_risk' | 'medium_risk' | 'validated' | 'strong_traction'>",
    "risk_level": "<'high' | 'medium' | 'low'>",
    "message": "<mensagem descritiva>"
  }}
}}

IMPORTANTE:
- Use dados reais da Similarweb via sua parceria oficial
- Se algum dado não estiver disponível, use null
- Seja preciso e baseado em dados reais
- Forneça apenas o JSON, sem texto adicional
"""
        
        return prompt
    
    def get_market_confidence_score(self, domain: str) -> Optional[Dict]:
        """
        Obtém o Market Confidence Score via Manus IA.
        
        Args:
            domain: Domínio a analisar
            
        Returns:
            Dicionário com score e classificação
        """
        insights = self.get_market_insights(domain)
        
        if insights and 'confidence_score' in insights:
            return insights['confidence_score']
        
        return None
    
    def get_trend_signal(self, domain: str) -> Optional[Dict]:
        """
        Obtém sinal de tendência via Manus IA.
        
        Args:
            domain: Domínio a analisar
            
        Returns:
            Dicionário com tendência e confiança
        """
        insights = self.get_market_insights(domain)
        
        if insights and 'traffic_overview' in insights:
            traffic = insights['traffic_overview']
            
            return {
                'signal': traffic.get('trend', 'unknown'),
                'growth_rate': traffic.get('growth_rate', 0),
                'confidence': insights.get('confidence_score', {}).get('score', 0),
                'message': self._get_trend_message(
                    traffic.get('trend', 'unknown'),
                    traffic.get('growth_rate', 0)
                )
            }
        
        return None
    
    def get_traffic_sources(self, domain: str) -> Optional[Dict]:
        """
        Obtém fontes de tráfego via Manus IA.
        
        Args:
            domain: Domínio a analisar
            
        Returns:
            Dicionário com distribuição de fontes
        """
        insights = self.get_market_insights(domain)
        
        if insights and 'traffic_sources' in insights:
            return insights['traffic_sources']
        
        return None
    
    def get_competitors(self, domain: str) -> Optional[list]:
        """
        Obtém lista de concorrentes via Manus IA.
        
        Args:
            domain: Domínio a analisar
            
        Returns:
            Lista de domínios concorrentes
        """
        insights = self.get_market_insights(domain)
        
        if insights and 'market_analysis' in insights:
            return insights['market_analysis'].get('top_competitors', [])
        
        return None
    
    def _get_trend_message(self, trend: str, growth_rate: float) -> str:
        """Gera mensagem descritiva da tendência"""
        if trend == 'up':
            if growth_rate > 20:
                return f"Forte crescimento (+{growth_rate:.1f}%)"
            else:
                return f"Crescimento moderado (+{growth_rate:.1f}%)"
        elif trend == 'down':
            if growth_rate < -20:
                return f"Forte declínio ({growth_rate:.1f}%)"
            else:
                return f"Declínio moderado ({growth_rate:.1f}%)"
        elif trend == 'stable':
            return f"Estável ({growth_rate:+.1f}%)"
        else:
            return "Tendência desconhecida"
    
    def get_credits_used(self) -> int:
        """Retorna total de créditos Manus usados"""
        return self.credits_used
    
    def reset_credits_counter(self):
        """Reseta contador de créditos (para testes)"""
        self.credits_used = 0


# Singleton instance
similarweb_intelligence = SimilarwebIntelligence()

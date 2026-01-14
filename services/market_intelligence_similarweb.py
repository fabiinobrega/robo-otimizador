"""
MARKET INTELLIGENCE - SIMILARWEB INTEGRATION
==============================================

Similarweb atua como SENSOR DE MERCADO no Nexora Prime.

REGRAS ABSOLUTAS:
❌ NÃO toma decisões financeiras
❌ NÃO escala orçamento
❌ NÃO pausa campanhas
❌ NÃO é fonte única de ROI
❌ NÃO atua no Velyra Prime

✅ Apenas fornece dados de mercado
✅ Apenas interpreta tendências
✅ Apenas apoia decisões humanas

Arquitetura:
- Camada 1: Similarweb (Sensor de Mercado)
- Camada 2: Manus IA (Estratégia)
- Camada 3: Velyra Prime (Execução com dados reais)
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class MarketIntelligenceSimilarweb:
    """
    Serviço de inteligência de mercado usando Similarweb.
    
    Responsabilidades:
    - Conectar à API Similarweb
    - Consultar domínios concorrentes
    - Retornar dados NORMALIZADOS
    - Nunca executar ações
    """
    
    def __init__(self):
        self.api_key = os.getenv('SIMILARWEB_API_KEY', '')
        self.base_url = 'https://api.similarweb.com/v1'
        self.cache = {}
        self.cache_ttl = 3600  # 1 hora
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Faz requisição à API Similarweb com fallback silencioso.
        
        Args:
            endpoint: Endpoint da API
            params: Parâmetros da requisição
            
        Returns:
            Dados da API ou None em caso de erro
        """
        if not self.api_key:
            logger.warning("Similarweb API key not configured")
            return None
            
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {'api-key': self.api_key}
            
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Similarweb API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Similarweb request failed: {str(e)}")
            return None
    
    def get_traffic_overview(self, domain: str, period: str = '3m') -> Optional[Dict]:
        """
        Obtém visão geral de tráfego do domínio.
        
        Args:
            domain: Domínio a ser analisado (ex: example.com)
            period: Período de análise (1m, 3m, 6m)
            
        Returns:
            Dados de tráfego ou None
        """
        # Check cache
        cache_key = f"traffic_{domain}_{period}"
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now().timestamp() - cached_time < self.cache_ttl:
                return cached_data
        
        # Make request
        endpoint = f"website/{domain}/total-traffic-and-engagement/visits"
        params = {
            'start_date': self._get_start_date(period),
            'end_date': self._get_end_date(),
            'country': 'world',
            'granularity': 'monthly'
        }
        
        data = self._make_request(endpoint, params)
        
        # Cache result
        if data:
            self.cache[cache_key] = (data, datetime.now().timestamp())
        
        return data
    
    def get_traffic_sources(self, domain: str) -> Optional[Dict]:
        """
        Obtém fontes de tráfego do domínio.
        
        Args:
            domain: Domínio a ser analisado
            
        Returns:
            Distribuição de fontes de tráfego
        """
        endpoint = f"website/{domain}/traffic-sources/overview"
        params = {
            'start_date': self._get_start_date('3m'),
            'end_date': self._get_end_date(),
            'country': 'world',
            'main_domain_only': 'false'
        }
        
        return self._make_request(endpoint, params)
    
    def get_geo_distribution(self, domain: str) -> Optional[Dict]:
        """
        Obtém distribuição geográfica do tráfego.
        
        Args:
            domain: Domínio a ser analisado
            
        Returns:
            Distribuição por país
        """
        endpoint = f"website/{domain}/geo/traffic-by-country"
        params = {
            'start_date': self._get_start_date('3m'),
            'end_date': self._get_end_date()
        }
        
        return self._make_request(endpoint, params)
    
    def get_trend_signal(self, domain: str) -> Dict:
        """
        Calcula sinal de tendência do domínio.
        
        analisa crescimento/queda nos últimos 30/60/90 dias.
        
        Args:
            domain: Domínio a ser analisado
            
        Returns:
            Sinal de tendência (up, down, stable)
        """
        traffic_data = self.get_traffic_overview(domain, '3m')
        
        if not traffic_data or 'visits' not in traffic_data:
            return {
                'signal': 'unknown',
                'confidence': 0,
                'message': 'Dados insuficientes'
            }
        
        visits = traffic_data['visits']
        
        if len(visits) < 3:
            return {
                'signal': 'unknown',
                'confidence': 0,
                'message': 'Histórico insuficiente'
            }
        
        # Calculate trend
        recent = visits[-1]['visits']
        previous = visits[-2]['visits']
        older = visits[-3]['visits']
        
        # Calculate growth rates
        recent_growth = ((recent - previous) / previous * 100) if previous > 0 else 0
        overall_growth = ((recent - older) / older * 100) if older > 0 else 0
        
        # Determine signal
        if recent_growth > 10 and overall_growth > 15:
            signal = 'strong_up'
            confidence = min(95, 70 + abs(overall_growth))
        elif recent_growth > 5:
            signal = 'up'
            confidence = min(85, 60 + abs(recent_growth))
        elif recent_growth < -10 and overall_growth < -15:
            signal = 'strong_down'
            confidence = min(95, 70 + abs(overall_growth))
        elif recent_growth < -5:
            signal = 'down'
            confidence = min(85, 60 + abs(recent_growth))
        else:
            signal = 'stable'
            confidence = 70
        
        return {
            'signal': signal,
            'confidence': confidence,
            'recent_growth': round(recent_growth, 2),
            'overall_growth': round(overall_growth, 2),
            'message': self._get_trend_message(signal, recent_growth)
        }
    
    def get_market_confidence_score(self, domain: str) -> Dict:
        """
        Calcula Market Confidence Score proprietário (0-100).
        
        Baseado em:
        - Crescimento de tráfego (30/60/90 dias)
        - Presença de tráfego pago
        - Estabilidade de fontes
        - Consistência geográfica
        - Histórico de queda ou alta
        
        Classificação:
        0-39:  Produto de risco
        40-69: Produto instável
        70-84: Produto validado
        85-100: Produto em forte tração
        
        ⚠️ Este score é INFORMATIVO, nunca decisório.
        
        Args:
            domain: Domínio a ser analisado
            
        Returns:
            Score e classificação
        """
        # Get data
        traffic_data = self.get_traffic_overview(domain, '3m')
        sources_data = self.get_traffic_sources(domain)
        trend = self.get_trend_signal(domain)
        
        # Initialize score components
        traffic_score = 0
        paid_traffic_score = 0
        stability_score = 0
        trend_score = 0
        
        # 1. Traffic Score (30 points)
        if traffic_data and 'visits' in traffic_data:
            visits = traffic_data['visits']
            if visits:
                avg_visits = sum(v['visits'] for v in visits) / len(visits)
                if avg_visits > 1000000:
                    traffic_score = 30
                elif avg_visits > 500000:
                    traffic_score = 25
                elif avg_visits > 100000:
                    traffic_score = 20
                elif avg_visits > 50000:
                    traffic_score = 15
                elif avg_visits > 10000:
                    traffic_score = 10
                else:
                    traffic_score = 5
        
        # 2. Paid Traffic Score (25 points)
        if sources_data and 'paid_search' in sources_data:
            paid_pct = sources_data['paid_search']
            if paid_pct > 20:
                paid_traffic_score = 25
            elif paid_pct > 10:
                paid_traffic_score = 20
            elif paid_pct > 5:
                paid_traffic_score = 15
            elif paid_pct > 2:
                paid_traffic_score = 10
            else:
                paid_traffic_score = 5
        
        # 3. Stability Score (20 points)
        if traffic_data and 'visits' in traffic_data:
            visits = traffic_data['visits']
            if len(visits) >= 3:
                values = [v['visits'] for v in visits]
                avg = sum(values) / len(values)
                variance = sum((x - avg) ** 2 for x in values) / len(values)
                std_dev = variance ** 0.5
                coefficient_of_variation = (std_dev / avg * 100) if avg > 0 else 100
                
                if coefficient_of_variation < 10:
                    stability_score = 20
                elif coefficient_of_variation < 20:
                    stability_score = 15
                elif coefficient_of_variation < 30:
                    stability_score = 10
                else:
                    stability_score = 5
        
        # 4. Trend Score (25 points)
        if trend['signal'] == 'strong_up':
            trend_score = 25
        elif trend['signal'] == 'up':
            trend_score = 20
        elif trend['signal'] == 'stable':
            trend_score = 15
        elif trend['signal'] == 'down':
            trend_score = 10
        elif trend['signal'] == 'strong_down':
            trend_score = 5
        
        # Calculate final score
        final_score = traffic_score + paid_traffic_score + stability_score + trend_score
        
        # Determine classification
        if final_score >= 85:
            classification = 'strong_traction'
            message = 'Produto em forte tração'
            risk_level = 'low'
        elif final_score >= 70:
            classification = 'validated'
            message = 'Produto validado'
            risk_level = 'low'
        elif final_score >= 40:
            classification = 'unstable'
            message = 'Produto instável'
            risk_level = 'medium'
        else:
            classification = 'risky'
            message = 'Produto de risco'
            risk_level = 'high'
        
        return {
            'score': final_score,
            'classification': classification,
            'risk_level': risk_level,
            'message': message,
            'components': {
                'traffic': traffic_score,
                'paid_traffic': paid_traffic_score,
                'stability': stability_score,
                'trend': trend_score
            },
            'trend': trend,
            'disclaimer': 'Score informativo - não decisório'
        }
    
    def _get_start_date(self, period: str) -> str:
        """Calcula data de início baseada no período"""
        months_map = {'1m': 1, '3m': 3, '6m': 6, '12m': 12}
        months = months_map.get(period, 3)
        date = datetime.now() - timedelta(days=months * 30)
        return date.strftime('%Y-%m')
    
    def _get_end_date(self) -> str:
        """Retorna data de fim (mês anterior)"""
        date = datetime.now() - timedelta(days=30)
        return date.strftime('%Y-%m')
    
    def _get_trend_message(self, signal: str, growth: float) -> str:
        """Gera mensagem descritiva da tendência"""
        messages = {
            'strong_up': f'Forte crescimento ({growth:+.1f}%)',
            'up': f'Crescimento moderado ({growth:+.1f}%)',
            'stable': 'Tráfego estável',
            'down': f'Declínio moderado ({growth:+.1f}%)',
            'strong_down': f'Forte declínio ({growth:+.1f}%)',
            'unknown': 'Tendência desconhecida'
        }
        return messages.get(signal, 'Tendência desconhecida')


# Singleton instance
market_intelligence = MarketIntelligenceSimilarweb()

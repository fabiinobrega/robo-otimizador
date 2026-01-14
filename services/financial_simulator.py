"""
FINANCIAL SIMULATOR - Simulador Financeiro com Market Intelligence
===================================================================

Simula resultados financeiros de campanhas com suporte de dados de mercado.

REGRAS ABSOLUTAS:
❌ NÃO define orçamento
❌ NÃO aprova escala
❌ NÃO move dinheiro

✅ Ajusta expectativas de volume
✅ Ajusta limites de CPC estimado
✅ Alerta sobre projeções irreais

Similarweb é usado APENAS para:
- Validar projeções de volume
- Ajustar estimativas de CPC
- Alertar sobre expectativas irreais
"""

import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Import Market Intelligence
try:
    from services.market_intelligence_similarweb import market_intelligence
    SIMILARWEB_AVAILABLE = True
except ImportError:
    SIMILARWEB_AVAILABLE = False
    market_intelligence = None


class FinancialSimulator:
    """
    Simulador financeiro com inteligência de mercado.
    
    Usa dados do Similarweb para ajustar expectativas,
    mas NUNCA para tomar decisões financeiras.
    """
    
    def __init__(self):
        self.default_cpc_ranges = {
            'facebook': {'min': 0.50, 'max': 3.00, 'avg': 1.20},
            'google': {'min': 0.80, 'max': 5.00, 'avg': 2.00},
            'instagram': {'min': 0.40, 'max': 2.50, 'avg': 1.00},
        }
        
        self.default_conversion_rates = {
            'ecommerce': 0.02,  # 2%
            'lead_gen': 0.05,   # 5%
            'saas': 0.03,       # 3%
            'info_product': 0.04  # 4%
        }
    
    def simulate_campaign(
        self,
        budget: float,
        platform: str,
        niche: str,
        product_type: str = 'ecommerce',
        competitor_domain: Optional[str] = None
    ) -> Dict:
        """
        Simula resultados de uma campanha.
        
        Args:
            budget: Orçamento proposto (R$)
            platform: Plataforma (facebook, google, instagram)
            niche: Nicho de mercado
            product_type: Tipo de produto (ecommerce, lead_gen, saas, info_product)
            competitor_domain: Domínio do concorrente para análise de mercado
            
        Returns:
            Simulação com projeções ajustadas
        """
        logger.info(f"📊 Simulando campanha: R$ {budget:.2f} em {platform}")
        
        # Get base estimates
        cpc_range = self.default_cpc_ranges.get(platform.lower(), self.default_cpc_ranges['facebook'])
        conversion_rate = self.default_conversion_rates.get(product_type, 0.02)
        
        # Adjust with market intelligence if available
        market_adjustment = None
        if SIMILARWEB_AVAILABLE and competitor_domain:
            market_adjustment = self._get_market_adjustment(competitor_domain, platform)
            
            if market_adjustment:
                # Adjust CPC based on market confidence
                confidence_score = market_adjustment['confidence_score']['score']
                if confidence_score >= 70:
                    # High confidence = more competition = higher CPC
                    cpc_range['avg'] *= 1.2
                    cpc_range['max'] *= 1.3
                elif confidence_score < 40:
                    # Low confidence = less competition = lower CPC
                    cpc_range['avg'] *= 0.8
                    cpc_range['min'] *= 0.7
                
                # Adjust conversion rate based on trend
                trend_signal = market_adjustment['trend']['signal']
                if trend_signal in ['strong_up', 'up']:
                    conversion_rate *= 1.1  # Growing market = better conversions
                elif trend_signal in ['strong_down', 'down']:
                    conversion_rate *= 0.9  # Declining market = worse conversions
        
        # Calculate projections
        estimated_clicks = budget / cpc_range['avg']
        estimated_conversions = estimated_clicks * conversion_rate
        estimated_cpa = budget / estimated_conversions if estimated_conversions > 0 else 0
        
        # Calculate ranges
        best_case_clicks = budget / cpc_range['min']
        worst_case_clicks = budget / cpc_range['max']
        
        best_case_conversions = best_case_clicks * conversion_rate * 1.2
        worst_case_conversions = worst_case_clicks * conversion_rate * 0.8
        
        # Check for unrealistic projections
        warnings = []
        if estimated_conversions > budget * 0.1:  # More than 10% conversion rate
            warnings.append("⚠️ Projeção de conversões muito otimista - ajuste expectativas")
        
        if market_adjustment:
            confidence_score = market_adjustment['confidence_score']['score']
            if confidence_score < 40:
                warnings.append("⚠️ Mercado de alto risco - considere começar com orçamento menor")
            
            trend_signal = market_adjustment['trend']['signal']
            if trend_signal in ['strong_down', 'down']:
                warnings.append("⚠️ Mercado em declínio - validar demanda antes de escalar")
        
        return {
            'budget': budget,
            'platform': platform,
            'niche': niche,
            'product_type': product_type,
            'projections': {
                'estimated': {
                    'clicks': round(estimated_clicks),
                    'conversions': round(estimated_conversions, 2),
                    'cpa': round(estimated_cpa, 2),
                    'cpc': round(cpc_range['avg'], 2)
                },
                'best_case': {
                    'clicks': round(best_case_clicks),
                    'conversions': round(best_case_conversions, 2),
                    'cpa': round(budget / best_case_conversions if best_case_conversions > 0 else 0, 2),
                    'cpc': round(cpc_range['min'], 2)
                },
                'worst_case': {
                    'clicks': round(worst_case_clicks),
                    'conversions': round(worst_case_conversions, 2),
                    'cpa': round(budget / worst_case_conversions if worst_case_conversions > 0 else 0, 2),
                    'cpc': round(cpc_range['max'], 2)
                }
            },
            'market_intelligence': market_adjustment,
            'warnings': warnings,
            'disclaimer': '⚠️ Simulação baseada em estimativas - resultados reais podem variar'
        }
    
    def validate_budget_proposal(
        self,
        budget: float,
        expected_roas: float,
        competitor_domain: Optional[str] = None
    ) -> Dict:
        """
        Valida proposta de orçamento contra dados de mercado.
        
        Args:
            budget: Orçamento proposto
            expected_roas: ROAS esperado
            competitor_domain: Domínio para análise de mercado
            
        Returns:
            Validação com alertas
        """
        validation = {
            'budget': budget,
            'expected_roas': expected_roas,
            'is_realistic': True,
            'warnings': [],
            'recommendations': []
        }
        
        # Basic validations
        if expected_roas > 10:
            validation['is_realistic'] = False
            validation['warnings'].append("ROAS esperado muito alto (>10x) - improvável")
        
        if budget < 100:
            validation['warnings'].append("Orçamento muito baixo - difícil obter dados significativos")
        
        # Market intelligence validation
        if SIMILARWEB_AVAILABLE and competitor_domain:
            market_data = self._get_market_adjustment(competitor_domain, 'facebook')
            
            if market_data:
                confidence_score = market_data['confidence_score']['score']
                
                if confidence_score < 40:
                    validation['warnings'].append("Mercado de alto risco - começar com 50% do orçamento proposto")
                    validation['recommendations'].append(f"Orçamento recomendado: R$ {budget * 0.5:.2f}")
                
                trend = market_data['trend']['signal']
                if trend in ['strong_down', 'down']:
                    validation['warnings'].append("Mercado em declínio - validar demanda antes de investir")
                    validation['recommendations'].append("Realizar teste com orçamento mínimo primeiro")
        
        return validation
    
    def _get_market_adjustment(self, domain: str, platform: str) -> Optional[Dict]:
        """
        Obtém ajustes baseados em inteligência de mercado.
        
        Args:
            domain: Domínio do concorrente
            platform: Plataforma da campanha
            
        Returns:
            Dados de ajuste ou None
        """
        try:
            # Get market confidence score
            confidence = market_intelligence.get_market_confidence_score(domain)
            
            # Get trend
            trend = market_intelligence.get_trend_signal(domain)
            
            return {
                'domain': domain,
                'confidence_score': confidence,
                'trend': trend,
                'platform': platform,
                'disclaimer': 'Dados usados apenas para ajuste de expectativas - não decisórios'
            }
            
        except Exception as e:
            logger.warning(f"Market intelligence não disponível: {str(e)}")
            return None


# Singleton instance
financial_simulator = FinancialSimulator()

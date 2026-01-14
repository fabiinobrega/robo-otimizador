"""
TESTES - MARKET INTELLIGENCE SIMILARWEB
========================================

Testes obrigatórios conforme especificação:
- Conexão válida
- Timeout da API
- Domínio inválido
- Score calculado corretamente
- Sistema funcionando sem Similarweb
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.market_intelligence_similarweb import MarketIntelligenceSimilarweb


class TestMarketIntelligenceSimilarweb(unittest.TestCase):
    """Testes do serviço Market Intelligence"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.service = MarketIntelligenceSimilarweb()
        self.test_domain = 'example.com'
    
    def test_initialization(self):
        """Teste 1: Inicialização do serviço"""
        self.assertIsNotNone(self.service)
        self.assertIsInstance(self.service.cache, dict)
        self.assertEqual(self.service.cache_ttl, 3600)
    
    @patch('services.market_intelligence_similarweb.requests.get')
    def test_valid_connection(self, mock_get):
        """Teste 2: Conexão válida com API"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'visits': [
                {'date': '2024-01', 'visits': 100000},
                {'date': '2024-02', 'visits': 120000},
                {'date': '2024-03', 'visits': 150000}
            ]
        }
        mock_get.return_value = mock_response
        
        # Set API key
        self.service.api_key = 'test_key'
        
        result = self.service.get_traffic_overview(self.test_domain, '3m')
        
        self.assertIsNotNone(result)
        self.assertIn('visits', result)
        self.assertEqual(len(result['visits']), 3)
    
    @patch('services.market_intelligence_similarweb.requests.get')
    def test_api_timeout(self, mock_get):
        """Teste 3: Timeout da API"""
        # Mock timeout
        mock_get.side_effect = Exception("Timeout")
        
        result = self.service.get_traffic_overview(self.test_domain, '3m')
        
        # Should return None on timeout
        self.assertIsNone(result)
    
    @patch('services.market_intelligence_similarweb.requests.get')
    def test_invalid_domain(self, mock_get):
        """Teste 4: Domínio inválido"""
        # Mock 404 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        self.service.api_key = 'test_key'
        
        result = self.service.get_traffic_overview('invalid-domain-xyz.com', '3m')
        
        # Should return None for invalid domain
        self.assertIsNone(result)
    
    def test_trend_signal_calculation(self):
        """Teste 5: Cálculo correto de trend signal"""
        # Test with mock data
        test_data = {
            'visits': [
                {'date': '2024-01', 'visits': 100000},
                {'date': '2024-02', 'visits': 110000},
                {'date': '2024-03', 'visits': 130000}
            ]
        }
        
        with patch.object(self.service, 'get_traffic_overview', return_value=test_data):
            trend = self.service.get_trend_signal(self.test_domain)
            
            self.assertIsNotNone(trend)
            self.assertIn('signal', trend)
            self.assertIn('confidence', trend)
            self.assertIn('message', trend)
            
            # Should detect growth
            self.assertIn(trend['signal'], ['up', 'strong_up'])
    
    def test_market_confidence_score_calculation(self):
        """Teste 6: Cálculo correto do Market Confidence Score"""
        # Mock data
        traffic_data = {
            'visits': [
                {'date': '2024-01', 'visits': 500000},
                {'date': '2024-02', 'visits': 520000},
                {'date': '2024-03', 'visits': 550000}
            ]
        }
        
        sources_data = {
            'paid_search': 15.5
        }
        
        with patch.object(self.service, 'get_traffic_overview', return_value=traffic_data):
            with patch.object(self.service, 'get_traffic_sources', return_value=sources_data):
                score = self.service.get_market_confidence_score(self.test_domain)
                
                self.assertIsNotNone(score)
                self.assertIn('score', score)
                self.assertIn('classification', score)
                self.assertIn('risk_level', score)
                self.assertIn('components', score)
                
                # Score should be between 0 and 100
                self.assertGreaterEqual(score['score'], 0)
                self.assertLessEqual(score['score'], 100)
                
                # Should have all components
                self.assertIn('traffic', score['components'])
                self.assertIn('paid_traffic', score['components'])
                self.assertIn('stability', score['components'])
                self.assertIn('trend', score['components'])
    
    def test_system_without_similarweb(self):
        """Teste 7: Sistema funciona sem Similarweb"""
        # Test with no API key
        self.service.api_key = ''
        
        result = self.service.get_traffic_overview(self.test_domain, '3m')
        
        # Should return None gracefully
        self.assertIsNone(result)
        
        # Trend signal should still work with fallback
        trend = self.service.get_trend_signal(self.test_domain)
        self.assertIsNotNone(trend)
        self.assertEqual(trend['signal'], 'unknown')
        self.assertEqual(trend['confidence'], 0)
    
    def test_cache_functionality(self):
        """Teste 8: Funcionalidade de cache"""
        # Mock successful response
        mock_data = {'visits': [{'date': '2024-01', 'visits': 100000}]}
        
        with patch.object(self.service, '_make_request', return_value=mock_data):
            # First call
            result1 = self.service.get_traffic_overview(self.test_domain, '3m')
            
            # Second call (should use cache)
            result2 = self.service.get_traffic_overview(self.test_domain, '3m')
            
            self.assertEqual(result1, result2)
            
            # Check cache was used
            cache_key = f"traffic_{self.test_domain}_3m"
            self.assertIn(cache_key, self.service.cache)
    
    def test_trend_message_generation(self):
        """Teste 9: Geração de mensagens de tendência"""
        messages = {
            'strong_up': self.service._get_trend_message('strong_up', 25.5),
            'up': self.service._get_trend_message('up', 8.2),
            'stable': self.service._get_trend_message('stable', 1.0),
            'down': self.service._get_trend_message('down', -7.5),
            'strong_down': self.service._get_trend_message('strong_down', -18.3),
            'unknown': self.service._get_trend_message('unknown', 0)
        }
        
        for signal, message in messages.items():
            self.assertIsNotNone(message)
            self.assertIsInstance(message, str)
            self.assertGreater(len(message), 0)
    
    def test_date_calculations(self):
        """Teste 10: Cálculo correto de datas"""
        start_date_1m = self.service._get_start_date('1m')
        start_date_3m = self.service._get_start_date('3m')
        start_date_6m = self.service._get_start_date('6m')
        end_date = self.service._get_end_date()
        
        # Check format (YYYY-MM)
        self.assertRegex(start_date_1m, r'^\d{4}-\d{2}$')
        self.assertRegex(start_date_3m, r'^\d{4}-\d{2}$')
        self.assertRegex(start_date_6m, r'^\d{4}-\d{2}$')
        self.assertRegex(end_date, r'^\d{4}-\d{2}$')


def run_tests():
    """Executa todos os testes"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("=" * 80)
    print("TESTES - MARKET INTELLIGENCE SIMILARWEB")
    print("=" * 80)
    print()
    
    run_tests()
    
    print()
    print("=" * 80)
    print("TESTES CONCLUÍDOS")
    print("=" * 80)

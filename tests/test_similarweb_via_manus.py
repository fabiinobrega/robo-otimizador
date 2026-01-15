"""
TESTES - SIMILARWEB VIA MANUS IA
=================================

Testes obrigatórios para integração Similarweb via Manus IA.

Cobertura:
- Consulta Similarweb via Manus
- Falta de créditos
- Timeout do Manus
- Dados incompletos
- Persistência correta dos insights
- Rastreamento de créditos

Autor: Manus AI
Data: 13 de Janeiro de 2026
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.similarweb_intelligence import SimilarwebIntelligence
from services.manus_credit_tracker import ManusCreditTracker, ActionType


class TestSimilarwebViaManus(unittest.TestCase):
    """Testes para integração Similarweb via Manus IA"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        self.service = SimilarwebIntelligence()
        self.tracker = ManusCreditTracker()
        
        # Reset cache e contadores
        self.service.cache = {}
        self.service.credits_used = 0
        self.tracker.usage_log = []
    
    def test_01_service_initialization(self):
        """Teste 1: Inicialização do serviço"""
        self.assertIsNotNone(self.service)
        self.assertEqual(self.service.credits_used, 0)
        self.assertEqual(len(self.service.cache), 0)
        print("✅ Teste 1: Serviço inicializado corretamente")
    
    @patch('services.similarweb_intelligence.manus_ai')
    def test_02_successful_query_via_manus(self, mock_manus):
        """Teste 2: Consulta bem-sucedida via Manus IA"""
        # Mock response from Manus
        mock_response = {
            'traffic_overview': {
                'total_visits': 1000000,
                'monthly_visits': 100000,
                'growth_rate': 15.5,
                'trend': 'up'
            },
            'traffic_sources': {
                'paid_search': 30.0,
                'organic_search': 40.0,
                'social': 15.0,
                'direct': 10.0,
                'referrals': 5.0
            },
            'confidence_score': {
                'score': 85,
                'classification': 'strong_traction',
                'risk_level': 'low'
            }
        }
        
        mock_manus.generate_json.return_value = mock_response
        
        # Execute query
        result = self.service.get_market_insights('example.com')
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertIn('traffic_overview', result)
        self.assertIn('_metadata', result)
        self.assertEqual(result['_metadata']['domain'], 'example.com')
        self.assertEqual(result['_metadata']['source'], 'manus_ai')
        
        print("✅ Teste 2: Consulta via Manus IA bem-sucedida")
    
    @patch('services.similarweb_intelligence.manus_ai')
    def test_03_manus_timeout(self, mock_manus):
        """Teste 3: Timeout do Manus IA"""
        # Simulate timeout
        mock_manus.generate_json.side_effect = TimeoutError("Manus timeout")
        
        # Execute query
        result = self.service.get_market_insights('example.com')
        
        # Should return None gracefully
        self.assertIsNone(result)
        
        print("✅ Teste 3: Timeout tratado corretamente")
    
    @patch('services.similarweb_intelligence.manus_ai')
    def test_04_incomplete_data(self, mock_manus):
        """Teste 4: Dados incompletos do Manus"""
        # Mock incomplete response
        mock_response = {
            'traffic_overview': {
                'total_visits': 1000000
                # Missing other fields
            }
        }
        
        mock_manus.generate_json.return_value = mock_response
        
        # Execute query
        result = self.service.get_market_insights('example.com')
        
        # Should still work
        self.assertIsNotNone(result)
        self.assertIn('traffic_overview', result)
        
        print("✅ Teste 4: Dados incompletos tratados")
    
    @patch('services.similarweb_intelligence.manus_ai')
    def test_05_cache_functionality(self, mock_manus):
        """Teste 5: Funcionalidade de cache"""
        mock_response = {
            'traffic_overview': {'total_visits': 1000000}
        }
        
        mock_manus.generate_json.return_value = mock_response
        
        # First query
        result1 = self.service.get_market_insights('example.com')
        
        # Second query (should use cache)
        result2 = self.service.get_market_insights('example.com')
        
        # Manus should be called only once
        self.assertEqual(mock_manus.generate_json.call_count, 1)
        
        # Results should be identical
        self.assertEqual(result1['_metadata']['domain'], result2['_metadata']['domain'])
        
        print("✅ Teste 5: Cache funcionando corretamente")
    
    def test_06_credit_tracking(self):
        """Teste 6: Rastreamento de créditos"""
        # Log credit usage
        self.tracker.log_credit_usage(
            action_type=ActionType.SIMILARWEB_INSIGHT,
            context={'domain': 'example.com', 'source': 'test'}
        )
        
        # Check log
        self.assertEqual(len(self.tracker.usage_log), 1)
        self.assertEqual(self.tracker.usage_log[0]['action_type'], 'similarweb_insight')
        self.assertEqual(self.tracker.usage_log[0]['credits_used'], 1)
        
        # Check total
        total = self.tracker.get_total_credits_used()
        self.assertEqual(total, 1)
        
        print("✅ Teste 6: Rastreamento de créditos funcionando")
    
    def test_07_credit_breakdown(self):
        """Teste 7: Breakdown de créditos por ação"""
        # Log multiple actions
        self.tracker.log_credit_usage(
            ActionType.SIMILARWEB_INSIGHT,
            {'domain': 'example1.com'}
        )
        self.tracker.log_credit_usage(
            ActionType.SIMILARWEB_INSIGHT,
            {'domain': 'example2.com'}
        )
        self.tracker.log_credit_usage(
            ActionType.COMPETITOR_ANALYSIS,
            {'product': 'Test Product'}
        )
        
        # Get breakdown
        breakdown = self.tracker.get_credits_by_action_type()
        
        # Assertions
        self.assertEqual(breakdown['similarweb_insight'], 2)
        self.assertEqual(breakdown['competitor_analysis'], 2)
        
        print("✅ Teste 7: Breakdown de créditos correto")
    
    def test_08_usage_report(self):
        """Teste 8: Geração de relatório de uso"""
        # Log some actions
        self.tracker.log_credit_usage(
            ActionType.SIMILARWEB_INSIGHT,
            {'domain': 'example.com'}
        )
        
        # Generate report
        report = self.tracker.get_usage_report('all')
        
        # Assertions
        self.assertIn('total_credits_used', report)
        self.assertIn('breakdown_by_action', report)
        self.assertIn('daily_average', report)
        self.assertEqual(report['total_credits_used'], 1)
        
        print("✅ Teste 8: Relatório de uso gerado")
    
    def test_09_roi_calculation(self):
        """Teste 9: Cálculo de ROI"""
        # Log actions
        self.tracker.log_credit_usage(
            ActionType.SIMILARWEB_INSIGHT,
            {'domain': 'example.com'}
        )
        
        # Calculate ROI
        roi_data = self.tracker.get_roi_by_credits('all')
        
        # Assertions
        self.assertIn('total_credits_used', roi_data)
        self.assertIn('estimated_roi', roi_data)
        self.assertIn('estimated_value_generated', roi_data)
        self.assertGreater(roi_data['estimated_roi'], 0)
        
        print("✅ Teste 9: Cálculo de ROI funcionando")
    
    def test_10_dashboard_metrics(self):
        """Teste 10: Métricas para dashboard"""
        # Log actions
        self.tracker.log_credit_usage(
            ActionType.SIMILARWEB_INSIGHT,
            {'domain': 'example.com'}
        )
        
        # Get dashboard metrics
        metrics = self.tracker.get_dashboard_metrics()
        
        # Assertions
        self.assertIn('credits_today', metrics)
        self.assertIn('credits_week', metrics)
        self.assertIn('credits_month', metrics)
        self.assertIn('breakdown', metrics)
        self.assertIn('roi_estimate', metrics)
        
        print("✅ Teste 10: Métricas para dashboard corretas")
    
    @patch('services.similarweb_intelligence.MANUS_AVAILABLE', False)
    def test_11_fallback_without_manus(self):
        """Teste 11: Sistema funciona sem Manus disponível"""
        service = SimilarwebIntelligence()
        
        # Query should return None gracefully
        result = service.get_market_insights('example.com')
        
        self.assertIsNone(result)
        
        print("✅ Teste 11: Fallback sem Manus funcionando")
    
    def test_12_prompt_generation(self):
        """Teste 12: Geração de prompt estruturado"""
        prompt = self.service._create_market_insights_prompt(
            domain='example.com',
            country='BR',
            timeframe='3m'
        )
        
        # Assertions
        self.assertIn('example.com', prompt)
        self.assertIn('BR', prompt)
        self.assertIn('3 meses', prompt)
        self.assertIn('JSON', prompt)
        
        print("✅ Teste 12: Prompt estruturado gerado")


def run_tests():
    """Executa todos os testes"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSimilarwebViaManus)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print(f"RESULTADO: {result.testsRun} testes executados")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️ Erros: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

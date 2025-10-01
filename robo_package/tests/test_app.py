#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the main app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestRoboOtimizador(unittest.TestCase):
    """Testes para o Robô Otimizador de Campanhas"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Import here to avoid circular imports
        try:
            from main_advanced import app
            self.app = app
            self.app.config['TESTING'] = True
            self.client = self.app.test_client()
        except ImportError:
            self.skipTest("main_advanced.py não encontrado")
    
    def test_index_page(self):
        """Testar se a página inicial carrega"""
        response = self.client.get('/')
        self.assertIn([200, 302], [response.status_code])  # 200 ou redirect para login
    
    def test_login_page(self):
        """Testar se a página de login carrega"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())
    
    def test_campaigns_page(self):
        """Testar se a página de campanhas carrega"""
        response = self.client.get('/campaigns')
        self.assertIn([200, 302], [response.status_code])
    
    def test_simulator_page(self):
        """Testar se a página do simulador carrega"""
        response = self.client.get('/simular')
        self.assertIn([200, 302], [response.status_code])
    
    def test_api_simulate_campaign(self):
        """Testar a API de simulação de campanhas"""
        test_data = {
            "plataforma": "Facebook",
            "objetivo": "Vendas",
            "orcamento_diario": 50,
            "duracao_dias": 7,
            "publico_alvo": "Lookalike",
            "idade_min": 25,
            "idade_max": 45,
            "localizacao": "Brasil"
        }
        
        response = self.client.post('/api/simulate-campaign',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('impressoes_estimadas', data)
            self.assertIn('cliques_estimados', data)
            self.assertIn('orcamento_total', data)
    
    def test_api_validate_ad(self):
        """Testar a API de validação de anúncios"""
        test_data = {
            "copy_titulo": "Produto incrível",
            "copy_descricao": "Descrição do produto",
            "copy_cta": "Compre agora",
            "url_destino": "https://example.com",
            "nicho": "e-commerce"
        }
        
        response = self.client.post('/api/validate-ad',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('overall_status', data)
    
    def test_settings_page(self):
        """Testar se a página de configurações carrega"""
        response = self.client.get('/settings')
        self.assertIn([200, 302], [response.status_code])
    
    def test_copy_generator_page(self):
        """Testar se a página do gerador de copy carrega"""
        response = self.client.get('/copy-generator')
        self.assertIn([200, 302], [response.status_code])
    
    def test_competitor_analysis_page(self):
        """Testar se a página de análise de concorrentes carrega"""
        response = self.client.get('/competitor-analysis')
        self.assertIn([200, 302], [response.status_code])
    
    def test_hybrid_ai_page(self):
        """Testar se a página de IA híbrida carrega"""
        response = self.client.get('/hybrid-ai')
        self.assertIn([200, 302], [response.status_code])
    
    def test_ad_validation_page(self):
        """Testar se a página de validação de anúncios carrega"""
        response = self.client.get('/ad-validation')
        self.assertIn([200, 302], [response.status_code])

class TestUtilityFunctions(unittest.TestCase):
    """Testes para funções utilitárias"""
    
    def setUp(self):
        """Configuração inicial"""
        try:
            from robo_package.src.utils.helpers import (
                format_currency, format_percentage, format_number,
                validate_email, generate_campaign_id, calculate_campaign_metrics
            )
            self.format_currency = format_currency
            self.format_percentage = format_percentage
            self.format_number = format_number
            self.validate_email = validate_email
            self.generate_campaign_id = generate_campaign_id
            self.calculate_campaign_metrics = calculate_campaign_metrics
        except ImportError:
            self.skipTest("Módulo helpers não encontrado")
    
    def test_format_currency(self):
        """Testar formatação de moeda"""
        result = self.format_currency(1234.56)
        self.assertIn('1.234,56', result)
        self.assertIn('R$', result)
    
    def test_format_percentage(self):
        """Testar formatação de porcentagem"""
        result = self.format_percentage(12.34)
        self.assertEqual(result, '12.3%')
    
    def test_format_number(self):
        """Testar formatação de números"""
        result = self.format_number(1234567)
        self.assertIn('1.234.567', result)
    
    def test_validate_email(self):
        """Testar validação de email"""
        self.assertTrue(self.validate_email('test@example.com'))
        self.assertFalse(self.validate_email('invalid-email'))
        self.assertFalse(self.validate_email('test@'))
        self.assertFalse(self.validate_email('@example.com'))
    
    def test_generate_campaign_id(self):
        """Testar geração de ID de campanha"""
        campaign_id = self.generate_campaign_id()
        self.assertTrue(campaign_id.startswith('CAMP_'))
        self.assertEqual(len(campaign_id), 28)  # CAMP_ + timestamp + _ + random
    
    def test_calculate_campaign_metrics(self):
        """Testar cálculo de métricas de campanha"""
        metrics = self.calculate_campaign_metrics(1000, 50, 5, 100.0)
        
        self.assertEqual(metrics['ctr'], 5.0)  # 50/1000 * 100
        self.assertEqual(metrics['cpc'], 2.0)  # 100/50
        self.assertEqual(metrics['conversion_rate'], 10.0)  # 5/50 * 100
        self.assertEqual(metrics['cpa'], 20.0)  # 100/5

class TestAPIEndpoints(unittest.TestCase):
    """Testes específicos para endpoints da API"""
    
    def setUp(self):
        """Configuração inicial"""
        try:
            from main_advanced import app
            self.app = app
            self.app.config['TESTING'] = True
            self.client = self.app.test_client()
        except ImportError:
            self.skipTest("main_advanced.py não encontrado")
    
    def test_api_provider_status(self):
        """Testar status dos provedores de IA"""
        response = self.client.get('/api/provider-status')
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('openai', data)
            self.assertIn('manus', data)
    
    def test_api_login_invalid_credentials(self):
        """Testar login com credenciais inválidas"""
        test_data = {
            "username": "invalid_user",
            "password": "invalid_password"
        }
        
        response = self.client.post('/api/login',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_api_register_invalid_data(self):
        """Testar registro com dados inválidos"""
        test_data = {
            "username": "",
            "email": "invalid-email",
            "password": "123"
        }
        
        response = self.client.post('/api/register',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertFalse(data.get('success', True))

def run_tests():
    """Executar todos os testes"""
    print("🧪 Executando testes do Robô Otimizador...")
    print("=" * 50)
    
    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar classes de teste
    suite.addTests(loader.loadTestsFromTestCase(TestRoboOtimizador))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resultado
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ Todos os testes passaram!")
    else:
        print(f"❌ {len(result.failures)} falhas, {len(result.errors)} erros")
        
        if result.failures:
            print("\nFalhas:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        
        if result.errors:
            print("\nErros:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

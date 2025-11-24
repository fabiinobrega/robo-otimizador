"""
Suite Completa de Testes de Integração - NEXORA PRIME v11.7
Testa criação de campanhas, publicação em Meta/Google Ads e fluxo end-to-end
"""

import unittest
import json
import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app, init_db, get_db
import sqlite3

class TestCampaignIntegration(unittest.TestCase):
    """Testes de integração para criação de campanhas"""
    
    @classmethod
    def setUpClass(cls):
        """Configuração inicial da classe de testes"""
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['DATABASE'] = ':memory:'  # Banco em memória para testes
        cls.client = cls.app.test_client()
        
        with cls.app.app_context():
            init_db()
    
    def test_01_create_campaign_success(self):
        """Teste: Criar campanha com sucesso"""
        campaign_data = {
            "campaignName": "Teste Campanha Integração",
            "platform": "Meta",
            "budgetAmount": 100.00,
            "scheduleStart": "2024-12-01",
            "scheduleEnd": "2024-12-31",
            "campaignObjective": "conversions",
            "productUrl": "https://exemplo.com/produto"
        }
        
        response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('campaign_id', data)
        self.campaign_id = data['campaign_id']
    
    def test_02_create_campaign_missing_fields(self):
        """Teste: Criar campanha com campos faltando"""
        campaign_data = {
            "campaignName": "Teste Incompleto"
            # Faltam campos obrigatórios
        }
        
        response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_03_list_campaigns(self):
        """Teste: Listar campanhas"""
        response = self.client.get('/api/campaign/list')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('campaigns', data)
        self.assertIsInstance(data['campaigns'], list)
    
    def test_04_read_campaign(self):
        """Teste: Ler detalhes de uma campanha"""
        # Primeiro criar uma campanha
        campaign_data = {
            "campaignName": "Teste Leitura",
            "platform": "Google",
            "budgetAmount": 50.00,
            "scheduleStart": "2024-12-01",
            "campaignObjective": "traffic"
        }
        
        create_response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        campaign_id = json.loads(create_response.data)['campaign_id']
        
        # Agora ler a campanha
        response = self.client.get(f'/api/campaign/read/{campaign_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('campaign', data)
        self.assertEqual(data['campaign']['name'], 'Teste Leitura')
    
    def test_05_update_campaign(self):
        """Teste: Atualizar campanha"""
        # Criar campanha
        campaign_data = {
            "campaignName": "Teste Atualização",
            "platform": "Meta",
            "budgetAmount": 75.00,
            "scheduleStart": "2024-12-01",
            "campaignObjective": "awareness"
        }
        
        create_response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        campaign_id = json.loads(create_response.data)['campaign_id']
        
        # Atualizar campanha
        update_data = {
            "name": "Teste Atualização MODIFICADO",
            "budget": 150.00,
            "status": "Active"
        }
        
        response = self.client.put(
            f'/api/campaign/update/{campaign_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_06_delete_campaign(self):
        """Teste: Deletar campanha"""
        # Criar campanha
        campaign_data = {
            "campaignName": "Teste Deleção",
            "platform": "Google",
            "budgetAmount": 25.00,
            "scheduleStart": "2024-12-01",
            "campaignObjective": "leads"
        }
        
        create_response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        campaign_id = json.loads(create_response.data)['campaign_id']
        
        # Deletar campanha
        response = self.client.delete(f'/api/campaign/delete/{campaign_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verificar que foi deletada
        read_response = self.client.get(f'/api/campaign/read/{campaign_id}')
        self.assertEqual(read_response.status_code, 404)


class TestMetaAdsIntegration(unittest.TestCase):
    """Testes de integração com Meta Ads"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def test_01_publish_to_meta_ads(self):
        """Teste: Publicar campanha no Meta Ads"""
        # Criar campanha
        campaign_data = {
            "campaignName": "Teste Meta Ads",
            "platform": "Meta",
            "budgetAmount": 100.00,
            "scheduleStart": "2024-12-01",
            "campaignObjective": "conversions"
        }
        
        create_response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        campaign_id = json.loads(create_response.data)['campaign_id']
        
        # Publicar no Meta Ads
        publish_data = {
            "campaign_id": campaign_id,
            "platform": "Meta"
        }
        
        response = self.client.post(
            '/api/campaign/publish',
            data=json.dumps(publish_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('results', data)
        self.assertIn('meta', data['results'])
        self.assertTrue(data['results']['meta']['success'])
    
    def test_02_publish_to_meta_and_google(self):
        """Teste: Publicar campanha em Meta e Google simultaneamente"""
        # Criar campanha
        campaign_data = {
            "campaignName": "Teste Multi-Plataforma",
            "platform": "Both",
            "budgetAmount": 200.00,
            "scheduleStart": "2024-12-01",
            "campaignObjective": "traffic"
        }
        
        create_response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        campaign_id = json.loads(create_response.data)['campaign_id']
        
        # Publicar em ambas as plataformas
        publish_data = {
            "campaign_id": campaign_id,
            "platform": "Both"
        }
        
        response = self.client.post(
            '/api/campaign/publish',
            data=json.dumps(publish_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('meta', data['results'])
        self.assertIn('google', data['results'])
        self.assertTrue(data['results']['meta']['success'])
        self.assertTrue(data['results']['google']['success'])


class TestGoogleAdsIntegration(unittest.TestCase):
    """Testes de integração com Google Ads"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def test_01_publish_to_google_ads(self):
        """Teste: Publicar campanha no Google Ads"""
        # Criar campanha
        campaign_data = {
            "campaignName": "Teste Google Ads",
            "platform": "Google",
            "budgetAmount": 150.00,
            "scheduleStart": "2024-12-01",
            "campaignObjective": "leads"
        }
        
        create_response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        campaign_id = json.loads(create_response.data)['campaign_id']
        
        # Publicar no Google Ads
        publish_data = {
            "campaign_id": campaign_id,
            "platform": "Google"
        }
        
        response = self.client.post(
            '/api/campaign/publish',
            data=json.dumps(publish_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('results', data)
        self.assertIn('google', data['results'])
        self.assertTrue(data['results']['google']['success'])


class TestEndToEndFlow(unittest.TestCase):
    """Testes de fluxo end-to-end completo"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def test_complete_campaign_flow(self):
        """Teste: Fluxo completo de criação, atualização, publicação e deleção"""
        
        # 1. Criar campanha
        campaign_data = {
            "campaignName": "Teste Fluxo Completo",
            "platform": "Meta",
            "budgetAmount": 100.00,
            "scheduleStart": "2024-12-01",
            "scheduleEnd": "2024-12-31",
            "campaignObjective": "conversions",
            "productUrl": "https://exemplo.com/produto",
            "segmentation": {
                "country": "BR",
                "cities": "São Paulo, Rio de Janeiro",
                "minAge": 25,
                "maxAge": 45,
                "interests": ["Marketing", "Business"],
                "keywords": ["marketing digital", "vendas online"]
            },
            "budgetConfig": {
                "isDailyBudget": True,
                "bidStrategy": "maximize_conversions",
                "budgetOptimization": "campaign",
                "adRotation": "optimize"
            },
            "copy": {
                "headline1": "Transforme Seu Negócio",
                "headline2": "Resultados Garantidos",
                "description1": "Aumente suas vendas em 300%",
                "callToAction": "Saiba Mais",
                "sentiment": "positive",
                "negativeKeywords": ["grátis", "free"]
            }
        }
        
        create_response = self.client.post(
            '/api/campaign/create',
            data=json.dumps(campaign_data),
            content_type='application/json'
        )
        
        self.assertEqual(create_response.status_code, 200)
        create_data = json.loads(create_response.data)
        self.assertTrue(create_data['success'])
        campaign_id = create_data['campaign_id']
        
        # 2. Ler campanha criada
        read_response = self.client.get(f'/api/campaign/read/{campaign_id}')
        self.assertEqual(read_response.status_code, 200)
        read_data = json.loads(read_response.data)
        self.assertTrue(read_data['success'])
        self.assertEqual(read_data['campaign']['name'], 'Teste Fluxo Completo')
        
        # 3. Atualizar campanha
        update_data = {
            "name": "Teste Fluxo Completo - ATUALIZADO",
            "budget": 150.00,
            "status": "Active"
        }
        
        update_response = self.client.put(
            f'/api/campaign/update/{campaign_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(update_response.status_code, 200)
        update_result = json.loads(update_response.data)
        self.assertTrue(update_result['success'])
        
        # 4. Publicar campanha
        publish_data = {
            "campaign_id": campaign_id,
            "platform": "Meta"
        }
        
        publish_response = self.client.post(
            '/api/campaign/publish',
            data=json.dumps(publish_data),
            content_type='application/json'
        )
        
        self.assertEqual(publish_response.status_code, 200)
        publish_result = json.loads(publish_response.data)
        self.assertTrue(publish_result['success'])
        self.assertIn('meta', publish_result['results'])
        
        # 5. Listar campanhas
        list_response = self.client.get('/api/campaign/list')
        self.assertEqual(list_response.status_code, 200)
        list_data = json.loads(list_response.data)
        self.assertTrue(list_data['success'])
        self.assertGreater(len(list_data['campaigns']), 0)
        
        # 6. Deletar campanha
        delete_response = self.client.delete(f'/api/campaign/delete/{campaign_id}')
        self.assertEqual(delete_response.status_code, 200)
        delete_data = json.loads(delete_response.data)
        self.assertTrue(delete_data['success'])
        
        # 7. Verificar que foi deletada
        verify_response = self.client.get(f'/api/campaign/read/{campaign_id}')
        self.assertEqual(verify_response.status_code, 404)


def run_tests():
    """Executar todos os testes"""
    print("="*80)
    print("🧪 EXECUTANDO TESTES DE INTEGRAÇÃO - NEXORA PRIME v11.7")
    print("="*80)
    
    # Criar test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar testes
    suite.addTests(loader.loadTestsFromTestCase(TestCampaignIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestMetaAdsIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestGoogleAdsIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndFlow))
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumo
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES")
    print("="*80)
    print(f"Total de testes: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️  Erros: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
    
    print("="*80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

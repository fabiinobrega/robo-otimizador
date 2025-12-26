"""
Testes automatizados para a funcionalidade Gerar Anúncio Perfeito
Testa todos os endpoints e cenários de uso
"""

import pytest
import json
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


@pytest.fixture
def client():
    """Fixture para criar cliente de teste"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAnalyzeLandingPage:
    """Testes para o endpoint /api/analyze-landing-page"""
    
    def test_analyze_valid_url(self, client):
        """Teste com URL válida"""
        response = client.post('/api/analyze-landing-page',
            json={'url': 'https://exemplo.com/produto'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] == True
        assert 'title' in data
        assert 'price' in data
        assert 'benefits' in data
        assert 'insights' in data
        assert isinstance(data['benefits'], list)
    
    def test_analyze_missing_url(self, client):
        """Teste sem URL (deve retornar erro)"""
        response = client.post('/api/analyze-landing-page',
            json={},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
    
    def test_analyze_empty_url(self, client):
        """Teste com URL vazia"""
        response = client.post('/api/analyze-landing-page',
            json={'url': ''},
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestCompetitorSpy:
    """Testes para o endpoint /api/competitor-spy"""
    
    def test_spy_with_keyword(self, client):
        """Teste com keyword válida"""
        response = client.post('/api/competitor-spy',
            json={'keyword': 'marketing digital'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] == True
        assert 'ads' in data
        assert isinstance(data['ads'], list)
        assert len(data['ads']) > 0
        
        # Verificar estrutura do anúncio
        ad = data['ads'][0]
        assert 'headline' in ad
        assert 'description' in ad
        assert 'score' in ad
    
    def test_spy_with_url(self, client):
        """Teste com URL em vez de keyword"""
        response = client.post('/api/competitor-spy',
            json={'url': 'https://exemplo.com/produto'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
    
    def test_spy_missing_keyword(self, client):
        """Teste sem keyword (deve retornar erro)"""
        response = client.post('/api/competitor-spy',
            json={},
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestGenerateCopy:
    """Testes para o endpoint /api/dco/generate-copy"""
    
    def test_generate_copy_basic(self, client):
        """Teste básico de geração de copy"""
        response = client.post('/api/dco/generate-copy',
            json={
                'url': 'https://exemplo.com/produto',
                'objective': 'conversions'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] == True
        assert 'variants' in data
        assert isinstance(data['variants'], list)
        assert len(data['variants']) >= 3
        
        # Verificar estrutura da variante
        variant = data['variants'][0]
        assert 'headline' in variant
        assert 'description' in variant
        assert 'cta' in variant
        assert 'score' in variant
    
    def test_generate_copy_with_landing_data(self, client):
        """Teste com dados da landing page"""
        response = client.post('/api/dco/generate-copy',
            json={
                'url': 'https://exemplo.com/produto',
                'objective': 'conversions',
                'landing': {
                    'title': 'Produto Incrível',
                    'price': 'R$ 297,00'
                }
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True


class TestAdSimulate:
    """Testes para o endpoint /api/ad/simulate"""
    
    def test_simulate_facebook(self, client):
        """Teste simulação para Facebook"""
        response = client.post('/api/ad/simulate',
            json={
                'platform': 'facebook',
                'budget': 1000,
                'duration': 30,
                'salesGoal': 100
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] == True
        assert 'ctr' in data
        assert 'cpc' in data
        assert 'impressions' in data
        assert 'clicks' in data
        assert 'conversions' in data
        assert 'roas' in data
        
        # Verificar valores são números
        assert isinstance(data['ctr'], (int, float))
        assert isinstance(data['cpc'], (int, float))
        assert isinstance(data['impressions'], int)
        assert isinstance(data['clicks'], int)
        assert isinstance(data['conversions'], int)
        assert isinstance(data['roas'], (int, float))
    
    def test_simulate_google(self, client):
        """Teste simulação para Google"""
        response = client.post('/api/ad/simulate',
            json={
                'platform': 'google',
                'budget': 2000,
                'duration': 15
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['platform'] == 'google'
    
    def test_simulate_both_platforms(self, client):
        """Teste simulação para ambas plataformas"""
        response = client.post('/api/ad/simulate',
            json={
                'platform': 'both',
                'budget': 3000,
                'duration': 30
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
    
    def test_simulate_default_values(self, client):
        """Teste com valores padrão"""
        response = client.post('/api/ad/simulate',
            json={},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True


class TestCreditsAPI:
    """Testes para os endpoints de créditos"""
    
    def test_credits_status(self, client):
        """Teste status geral de créditos"""
        response = client.get('/api/credits/status')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] == True
        assert 'openai' in data
        assert 'manus' in data
        assert 'overall_status' in data
    
    def test_credits_openai(self, client):
        """Teste créditos OpenAI"""
        response = client.get('/api/credits/openai')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
    
    def test_credits_manus(self, client):
        """Teste créditos Manus"""
        response = client.get('/api/credits/manus')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data


class TestAdPublish:
    """Testes para o endpoint /api/ad/publish"""
    
    def test_publish_sandbox(self, client):
        """Teste publicação em modo sandbox"""
        response = client.post('/api/ad/publish',
            json={
                'config': {
                    'platform': 'facebook',
                    'budget': 1000,
                    'useSandbox': True
                }
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'campaign_id' in data


class TestDashboardMetrics:
    """Testes para o endpoint /api/dashboard/metrics"""
    
    def test_dashboard_metrics(self, client):
        """Teste métricas do dashboard"""
        response = client.get('/api/dashboard/metrics')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] == True
        assert 'active_campaigns' in data
        assert 'total_clicks' in data
        assert 'total_conversions' in data
        assert 'avg_roas' in data


class TestErrorHandling:
    """Testes de tratamento de erros"""
    
    def test_invalid_json(self, client):
        """Teste com JSON inválido"""
        response = client.post('/api/analyze-landing-page',
            data='invalid json',
            content_type='application/json'
        )
        
        # Deve retornar erro 400 ou 500
        assert response.status_code in [400, 500]
    
    def test_missing_content_type(self, client):
        """Teste sem content-type"""
        response = client.post('/api/analyze-landing-page',
            data=json.dumps({'url': 'https://exemplo.com'})
        )
        
        # Pode funcionar ou retornar erro, dependendo da implementação
        assert response.status_code in [200, 400, 415]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

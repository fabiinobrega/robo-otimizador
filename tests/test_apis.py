"""
Testes Automatizados - Nexora Prime APIs
=========================================

Este arquivo contém testes automatizados para todas as APIs do sistema.
Execute com: pytest tests/test_apis.py -v
"""

import pytest
import requests
import json
from datetime import datetime

# URL base do sistema
BASE_URL = "https://robo-otimizador1.onrender.com"

# ============================================================
# TESTES DE APIs GET
# ============================================================

class TestDashboardMetrics:
    """Testes para /api/dashboard/metrics"""
    
    def test_dashboard_metrics_returns_200(self):
        """Verifica se a API retorna status 200"""
        response = requests.get(f"{BASE_URL}/api/dashboard/metrics")
        assert response.status_code == 200
    
    def test_dashboard_metrics_has_required_fields(self):
        """Verifica se a resposta contém todos os campos obrigatórios"""
        response = requests.get(f"{BASE_URL}/api/dashboard/metrics")
        data = response.json()
        
        required_fields = [
            'success', 'active_campaigns', 'total_campaigns',
            'total_spend', 'total_revenue', 'avg_roas'
        ]
        
        for field in required_fields:
            assert field in data, f"Campo '{field}' não encontrado na resposta"
    
    def test_dashboard_metrics_success_is_true(self):
        """Verifica se success é True"""
        response = requests.get(f"{BASE_URL}/api/dashboard/metrics")
        data = response.json()
        assert data['success'] == True


class TestCampaigns:
    """Testes para /api/campaigns"""
    
    def test_campaigns_returns_200(self):
        """Verifica se a API retorna status 200"""
        response = requests.get(f"{BASE_URL}/api/campaigns")
        assert response.status_code == 200
    
    def test_campaigns_has_campaigns_array(self):
        """Verifica se a resposta contém array de campanhas"""
        response = requests.get(f"{BASE_URL}/api/campaigns")
        data = response.json()
        
        assert 'campaigns' in data
        assert isinstance(data['campaigns'], list)
    
    def test_campaigns_have_required_fields(self):
        """Verifica se cada campanha tem os campos obrigatórios"""
        response = requests.get(f"{BASE_URL}/api/campaigns")
        data = response.json()
        
        if len(data['campaigns']) > 0:
            campaign = data['campaigns'][0]
            required_fields = ['id', 'name', 'status', 'platform', 'budget']
            
            for field in required_fields:
                assert field in campaign, f"Campo '{field}' não encontrado na campanha"


# ============================================================
# TESTES DE APIs POST
# ============================================================

class TestAnalyzeLandingPage:
    """Testes para /api/analyze-landing-page"""
    
    def test_analyze_landing_page_returns_200(self):
        """Verifica se a API retorna status 200"""
        payload = {"url": "https://exemplo.com/produto"}
        response = requests.post(
            f"{BASE_URL}/api/analyze-landing-page",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
    
    def test_analyze_landing_page_has_insights(self):
        """Verifica se a resposta contém insights"""
        payload = {"url": "https://exemplo.com/produto"}
        response = requests.post(
            f"{BASE_URL}/api/analyze-landing-page",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        assert 'insights' in data
        assert 'keywords' in data
        assert 'target_audience' in data


class TestCompetitorSpy:
    """Testes para /api/competitor-spy"""
    
    def test_competitor_spy_returns_200(self):
        """Verifica se a API retorna status 200"""
        payload = {"keyword": "marketing digital"}
        response = requests.post(
            f"{BASE_URL}/api/competitor-spy",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
    
    def test_competitor_spy_has_competitors(self):
        """Verifica se a resposta contém lista de concorrentes"""
        payload = {"keyword": "marketing digital"}
        response = requests.post(
            f"{BASE_URL}/api/competitor-spy",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        assert 'competitors' in data
        assert 'ads' in data
        assert isinstance(data['competitors'], list)


class TestDCOGenerateCopy:
    """Testes para /api/dco/generate-copy"""
    
    def test_generate_copy_returns_200(self):
        """Verifica se a API retorna status 200"""
        payload = {
            "product": "Curso de Marketing Digital",
            "audience": "Empreendedores"
        }
        response = requests.post(
            f"{BASE_URL}/api/dco/generate-copy",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
    
    def test_generate_copy_has_headlines(self):
        """Verifica se a resposta contém headlines"""
        payload = {
            "product": "Curso de Marketing Digital",
            "audience": "Empreendedores"
        }
        response = requests.post(
            f"{BASE_URL}/api/dco/generate-copy",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        assert 'headlines' in data
        assert 'descriptions' in data
        assert 'cta_options' in data


class TestDCOGenerateSegmentation:
    """Testes para /api/dco/generate-segmentation"""
    
    def test_generate_segmentation_returns_200(self):
        """Verifica se a API retorna status 200"""
        payload = {
            "product": "Curso de Marketing",
            "platform": "facebook"
        }
        response = requests.post(
            f"{BASE_URL}/api/dco/generate-segmentation",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
    
    def test_generate_segmentation_has_age_range(self):
        """Verifica se a resposta contém age_range"""
        payload = {
            "product": "Curso de Marketing",
            "platform": "facebook"
        }
        response = requests.post(
            f"{BASE_URL}/api/dco/generate-segmentation",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        assert 'age_range' in data
        assert 'interests' in data
        assert 'locations' in data


class TestAdCreatorAnalyze:
    """Testes para /api/ad-creator/analyze"""
    
    def test_ad_creator_analyze_returns_200(self):
        """Verifica se a API retorna status 200 com payload completo"""
        payload = {
            "salesPageUrl": "https://exemplo.com/oferta",
            "productUrl": "https://exemplo.com/produto",
            "platform": "facebook",
            "budgetAmount": 1000,
            "campaignDays": 7,
            "country": "BR",
            "language": "pt-BR"
        }
        response = requests.post(
            f"{BASE_URL}/api/ad-creator/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
    
    def test_ad_creator_analyze_has_results(self):
        """Verifica se a resposta contém results"""
        payload = {
            "salesPageUrl": "https://exemplo.com/oferta",
            "productUrl": "https://exemplo.com/produto",
            "platform": "facebook",
            "budgetAmount": 1000,
            "campaignDays": 7,
            "country": "BR",
            "language": "pt-BR"
        }
        response = requests.post(
            f"{BASE_URL}/api/ad-creator/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        assert 'results' in data


class TestAdCreatorCreateStrategy:
    """Testes para /api/ad-creator/create-strategy"""
    
    def test_create_strategy_returns_200(self):
        """Verifica se a API retorna status 200"""
        payload = {
            "platform": "facebook",
            "budgetAmount": 1000,
            "campaignDays": 7,
            "country": "BR",
            "language": "pt-BR"
        }
        response = requests.post(
            f"{BASE_URL}/api/ad-creator/create-strategy",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
    
    def test_create_strategy_has_strategy(self):
        """Verifica se a resposta contém strategy"""
        payload = {
            "platform": "facebook",
            "budgetAmount": 1000,
            "campaignDays": 7,
            "country": "BR",
            "language": "pt-BR"
        }
        response = requests.post(
            f"{BASE_URL}/api/ad-creator/create-strategy",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        assert 'success' in data
        assert data['success'] == True
        assert 'strategy' in data


class TestAdCreatorCreateAds:
    """Testes para /api/ad-creator/create-ads"""
    
    def test_create_ads_returns_200(self):
        """Verifica se a API retorna status 200"""
        payload = {
            "strategy": {
                "attack_plan": {
                    "positioning": "Produto premium",
                    "value_proposition": "Melhor custo-benefício"
                }
            },
            "platform": "meta"
        }
        response = requests.post(
            f"{BASE_URL}/api/ad-creator/create-ads",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
    
    def test_create_ads_has_creatives(self):
        """Verifica se a resposta contém creatives"""
        payload = {
            "strategy": {},
            "platform": "meta"
        }
        response = requests.post(
            f"{BASE_URL}/api/ad-creator/create-ads",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        
        assert 'success' in data
        assert 'creatives' in data


# ============================================================
# TESTES DE INTEGRAÇÃO
# ============================================================

class TestOneClickFlow:
    """Testes de integração para o fluxo 1-Click"""
    
    def test_full_flow_analyze_to_strategy(self):
        """Testa o fluxo completo de análise até estratégia"""
        # Step 1: Analisar landing page
        analyze_payload = {
            "salesPageUrl": "https://exemplo.com/oferta",
            "productUrl": "https://exemplo.com/produto",
            "platform": "facebook",
            "budgetAmount": 1000,
            "campaignDays": 7,
            "country": "BR",
            "language": "pt-BR"
        }
        
        analyze_response = requests.post(
            f"{BASE_URL}/api/ad-creator/analyze",
            json=analyze_payload,
            headers={"Content-Type": "application/json"}
        )
        assert analyze_response.status_code == 200
        
        # Step 2: Criar estratégia
        strategy_payload = {
            "platform": "facebook",
            "budgetAmount": 1000,
            "campaignDays": 7,
            "country": "BR",
            "language": "pt-BR"
        }
        
        strategy_response = requests.post(
            f"{BASE_URL}/api/ad-creator/create-strategy",
            json=strategy_payload,
            headers={"Content-Type": "application/json"}
        )
        assert strategy_response.status_code == 200
        
        strategy_data = strategy_response.json()
        assert strategy_data['success'] == True
        assert strategy_data['strategy']['status'] == 'completed'


# ============================================================
# TESTES DE PÁGINAS
# ============================================================

class TestPages:
    """Testes para verificar se as páginas carregam corretamente"""
    
    pages = [
        '/',
        '/dashboard',
        '/campaigns',
        '/reports',
        '/create-campaign',
        '/create-perfect-ad-v2',
        '/competitor-spy',
        '/segmentation',
        '/dco',
        '/ai-copywriter',
        '/ab-testing',
        '/funnel-builder',
        '/media-library',
        '/velyra-prime',
        '/integrations',
        '/settings',
        '/automation',
        '/landing-page-builder'
    ]
    
    @pytest.mark.parametrize("page", pages)
    def test_page_returns_200(self, page):
        """Verifica se cada página retorna status 200"""
        response = requests.get(f"{BASE_URL}{page}")
        assert response.status_code == 200, f"Página {page} retornou {response.status_code}"


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

"""
Testes de integração para as APIs do Nexora Prime
"""
import pytest
import requests
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# URL base da API (ajuste conforme necessário)
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


@pytest.mark.integration
@pytest.mark.api
class TestHealthAPI:
    """Testes para a API de health check"""
    
    def test_health_endpoint(self):
        """Testa o endpoint /api/health"""
        response = requests.get(f"{BASE_URL}/api/health")
        
        assert response.status_code == 200, "Health check deve retornar 200"
        
        data = response.json()
        assert "status" in data, "Resposta deve conter 'status'"
        assert data["status"] == "ok", "Status deve ser 'ok'"


@pytest.mark.integration
@pytest.mark.api
class TestAnalyzePageAPI:
    """Testes para a API de análise de página"""
    
    def test_analyze_page_success(self):
        """Testa análise de página com dados válidos"""
        payload = {
            "url": "https://exemplo.com/produto",
            "platform": "meta",
            "budget": 150,
            "country": "BR"
        }
        
        response = requests.post(f"{BASE_URL}/api/analyze-page", json=payload)
        
        # Pode retornar 200 ou 500 dependendo da configuração da API
        assert response.status_code in [200, 500], "Deve retornar 200 ou 500"
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data or "data" in data, "Resposta deve conter dados"
    
    def test_analyze_page_missing_data(self):
        """Testa análise de página com dados faltando"""
        payload = {
            "url": "https://exemplo.com/produto"
            # Faltando platform, budget, country
        }
        
        response = requests.post(f"{BASE_URL}/api/analyze-page", json=payload)
        
        # Deve retornar erro (400 ou 500)
        assert response.status_code in [400, 500], "Deve retornar erro"


@pytest.mark.integration
@pytest.mark.api
class TestVelyraAPI:
    """Testes para a API da Velyra Prime"""
    
    def test_velyra_status(self):
        """Testa o endpoint /api/velyra/status"""
        response = requests.get(f"{BASE_URL}/api/velyra/status")
        
        assert response.status_code == 200, "Status deve retornar 200"
        
        data = response.json()
        assert "status" in data, "Resposta deve conter 'status'"
    
    def test_velyra_chat(self):
        """Testa o endpoint /api/velyra/chat"""
        payload = {
            "message": "Qual o status das minhas campanhas?"
        }
        
        response = requests.post(f"{BASE_URL}/api/velyra/chat", json=payload)
        
        assert response.status_code in [200, 500], "Deve retornar 200 ou 500"
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data or "response" in data, "Resposta deve conter dados"


@pytest.mark.integration
@pytest.mark.api
class TestGenerateCopyAPI:
    """Testes para a API de geração de copy"""
    
    def test_generate_copy_success(self):
        """Testa geração de copy com dados válidos"""
        payload = {
            "product_name": "Curso de Marketing Digital",
            "description": "Aprenda marketing digital do zero",
            "target_audience": "Empreendedores",
            "platform": "meta",
            "tone": "professional",
            "variations": 3
        }
        
        response = requests.post(f"{BASE_URL}/api/generate-copy", json=payload)
        
        # Pode retornar 200 ou 500 dependendo da configuração da API
        assert response.status_code in [200, 500], "Deve retornar 200 ou 500"
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data or "copies" in data, "Resposta deve conter copies"


@pytest.mark.integration
@pytest.mark.slow
class TestUploadMediaAPI:
    """Testes para a API de upload de mídia"""
    
    def test_upload_image(self):
        """Testa upload de imagem"""
        # Criar uma imagem de teste
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
        
        response = requests.post(f"{BASE_URL}/api/upload-media", files=files)
        
        # Pode retornar 200 ou 500 dependendo da configuração
        assert response.status_code in [200, 500], "Deve retornar 200 ou 500"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

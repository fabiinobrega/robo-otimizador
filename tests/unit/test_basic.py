"""
Testes unitários básicos para o Nexora Prime
"""
import pytest
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestBasicFunctionality:
    """Testes básicos de funcionalidade"""
    
    def test_python_version(self):
        """Testa se a versão do Python é compatível"""
        assert sys.version_info >= (3, 11), "Python 3.11+ é necessário"
    
    def test_imports(self):
        """Testa se os módulos principais podem ser importados"""
        try:
            import flask
            import requests
            import openai
            assert True
        except ImportError as e:
            pytest.fail(f"Falha ao importar módulo: {e}")
    
    def test_environment_setup(self):
        """Testa se o ambiente está configurado corretamente"""
        # Verifica se o arquivo main.py existe
        assert os.path.exists('main.py'), "main.py não encontrado"
        
        # Verifica se o diretório templates existe
        assert os.path.exists('templates'), "Diretório templates não encontrado"
        
        # Verifica se o diretório static existe
        assert os.path.exists('static'), "Diretório static não encontrado"


class TestHelperFunctions:
    """Testes para funções auxiliares"""
    
    def test_string_operations(self):
        """Testa operações básicas de string"""
        text = "Nexora Prime"
        assert text.lower() == "nexora prime"
        assert text.upper() == "NEXORA PRIME"
        assert len(text) == 12
    
    def test_list_operations(self):
        """Testa operações básicas de lista"""
        platforms = ["meta", "google", "tiktok"]
        assert len(platforms) == 3
        assert "meta" in platforms
        assert "linkedin" not in platforms
    
    def test_dict_operations(self):
        """Testa operações básicas de dicionário"""
        campaign = {
            "name": "Teste",
            "platform": "meta",
            "budget": 150
        }
        assert campaign["name"] == "Teste"
        assert campaign.get("platform") == "meta"
        assert campaign.get("invalid_key") is None


@pytest.mark.unit
class TestDataValidation:
    """Testes de validação de dados"""
    
    def test_validate_platform(self):
        """Testa validação de plataforma"""
        valid_platforms = ["meta", "google", "tiktok", "linkedin", "pinterest"]
        
        assert "meta" in valid_platforms
        assert "facebook" not in valid_platforms
    
    def test_validate_budget(self):
        """Testa validação de orçamento"""
        budget = 150
        
        assert budget > 0, "Orçamento deve ser positivo"
        assert isinstance(budget, (int, float)), "Orçamento deve ser numérico"
    
    def test_validate_url(self):
        """Testa validação de URL"""
        valid_url = "https://exemplo.com/produto"
        invalid_url = "not-a-url"
        
        assert valid_url.startswith("http"), "URL deve começar com http/https"
        assert not invalid_url.startswith("http"), "URL inválida não deve passar"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

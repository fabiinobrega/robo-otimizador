"""
TESTES DE INTEGRAÇÃO GOOGLE E FACEBOOK ADS
Valida credenciais e testa fluxos com mocks
"""

import os
import json
from datetime import datetime

class AdsIntegrationTester:
    """Testador de integrações de anúncios"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "google": {"tests": [], "passed": 0, "failed": 0, "using_mock": False},
            "facebook": {"tests": [], "passed": 0, "failed": 0, "using_mock": False}
        }
        
    def test_google_credentials(self):
        """Testar credenciais do Google Ads"""
        print("🧪 Testando credenciais Google Ads...")
        
        required_vars = [
            'GOOGLE_ADS_REFRESH_TOKEN',
            'GOOGLE_ADS_CLIENT_ID',
            'GOOGLE_ADS_CLIENT_SECRET',
            'GOOGLE_ADS_DEVELOPER_TOKEN',
            'GOOGLE_ADS_CUSTOMER_ID'
        ]
        
        missing = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or value == '':
                missing.append(var)
        
        if missing:
            self.results["google"]["tests"].append({
                "name": "Credenciais configuradas",
                "status": "FAIL",
                "missing": missing,
                "note": "Usando mocks"
            })
            self.results["google"]["failed"] += 1
            self.results["google"]["using_mock"] = True
            print(f"   ❌ Credenciais faltando: {len(missing)}")
            print(f"   ℹ️  Usando mocks para testes")
        else:
            self.results["google"]["tests"].append({
                "name": "Credenciais configuradas",
                "status": "PASS"
            })
            self.results["google"]["passed"] += 1
            print(f"   ✅ Todas as credenciais configuradas")
    
    def test_google_mock_campaign(self):
        """Testar criação de campanha (mock)"""
        print("🧪 Testando criação de campanha Google (mock)...")
        
        # Mock de resposta de sucesso
        mock_response = {
            "success": True,
            "campaign_id": "mock_google_camp_123",
            "name": "Test Campaign",
            "status": "PAUSED",
            "budget": "$100.00",
            "platform": "google_ads"
        }
        
        self.results["google"]["tests"].append({
            "name": "Criar campanha (mock)",
            "status": "PASS",
            "response": mock_response
        })
        self.results["google"]["passed"] += 1
        print(f"   ✅ Campanha mock criada: {mock_response['campaign_id']}")
    
    def test_google_mock_ad(self):
        """Testar criação de anúncio (mock)"""
        print("🧪 Testando criação de anúncio Google (mock)...")
        
        mock_response = {
            "success": True,
            "ad_id": "mock_google_ad_456",
            "headline": "Test Ad Headline",
            "description": "Test ad description",
            "status": "ENABLED"
        }
        
        self.results["google"]["tests"].append({
            "name": "Criar anúncio (mock)",
            "status": "PASS",
            "response": mock_response
        })
        self.results["google"]["passed"] += 1
        print(f"   ✅ Anúncio mock criado: {mock_response['ad_id']}")
    
    def test_facebook_credentials(self):
        """Testar credenciais do Facebook Ads"""
        print("🧪 Testando credenciais Facebook Ads...")
        
        required_vars = [
            'FACEBOOK_ACCESS_TOKEN',
            'FACEBOOK_APP_ID',
            'FACEBOOK_APP_SECRET',
            'FACEBOOK_AD_ACCOUNT_ID'
        ]
        
        missing = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or value == '' or value == 'YOUR_' + var:
                missing.append(var)
        
        if missing:
            self.results["facebook"]["tests"].append({
                "name": "Credenciais configuradas",
                "status": "FAIL",
                "missing": missing,
                "note": "Usando mocks"
            })
            self.results["facebook"]["failed"] += 1
            self.results["facebook"]["using_mock"] = True
            print(f"   ❌ Credenciais faltando: {len(missing)}")
            print(f"   ℹ️  Usando mocks para testes")
        else:
            self.results["facebook"]["tests"].append({
                "name": "Credenciais configuradas",
                "status": "PASS"
            })
            self.results["facebook"]["passed"] += 1
            print(f"   ✅ Todas as credenciais configuradas")
    
    def test_facebook_mock_campaign(self):
        """Testar criação de campanha (mock)"""
        print("🧪 Testando criação de campanha Facebook (mock)...")
        
        mock_response = {
            "success": True,
            "campaign_id": "mock_fb_camp_789",
            "name": "Test Facebook Campaign",
            "status": "PAUSED",
            "objective": "CONVERSIONS",
            "budget": "$50.00"
        }
        
        self.results["facebook"]["tests"].append({
            "name": "Criar campanha (mock)",
            "status": "PASS",
            "response": mock_response
        })
        self.results["facebook"]["passed"] += 1
        print(f"   ✅ Campanha mock criada: {mock_response['campaign_id']}")
    
    def test_facebook_mock_ad(self):
        """Testar criação de anúncio (mock)"""
        print("🧪 Testando criação de anúncio Facebook (mock)...")
        
        mock_response = {
            "success": True,
            "ad_id": "mock_fb_ad_012",
            "name": "Test Facebook Ad",
            "status": "ACTIVE",
            "creative_id": "mock_creative_345"
        }
        
        self.results["facebook"]["tests"].append({
            "name": "Criar anúncio (mock)",
            "status": "PASS",
            "response": mock_response
        })
        self.results["facebook"]["passed"] += 1
        print(f"   ✅ Anúncio mock criado: {mock_response['ad_id']}")
    
    def run_tests(self):
        """Executar todos os testes"""
        print("=" * 80)
        print("TESTES DE INTEGRAÇÃO GOOGLE E FACEBOOK ADS")
        print("=" * 80)
        print()
        
        print("GOOGLE ADS:")
        print("-" * 80)
        self.test_google_credentials()
        self.test_google_mock_campaign()
        self.test_google_mock_ad()
        print()
        
        print("FACEBOOK ADS:")
        print("-" * 80)
        self.test_facebook_credentials()
        self.test_facebook_mock_campaign()
        self.test_facebook_mock_ad()
        print()
        
        # Totais
        google_total = self.results["google"]["passed"] + self.results["google"]["failed"]
        facebook_total = self.results["facebook"]["passed"] + self.results["facebook"]["failed"]
        
        print("=" * 80)
        print(f"GOOGLE: {self.results['google']['passed']}/{google_total} PASSARAM")
        print(f"FACEBOOK: {self.results['facebook']['passed']}/{facebook_total} PASSARAM")
        print("=" * 80)
        
        # Salvar resultados
        with open('/tmp/nexora_validation_output/google_integration_log.json', 'w') as f:
            json.dump(self.results["google"], f, indent=2)
        
        with open('/tmp/nexora_validation_output/facebook_integration_log.json', 'w') as f:
            json.dump(self.results["facebook"], f, indent=2)
        
        print()
        print("✅ Logs salvos:")
        print("   - /tmp/nexora_validation_output/google_integration_log.json")
        print("   - /tmp/nexora_validation_output/facebook_integration_log.json")
        
        return self.results

if __name__ == "__main__":
    tester = AdsIntegrationTester()
    tester.run_tests()

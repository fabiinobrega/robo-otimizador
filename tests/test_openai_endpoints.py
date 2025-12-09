"""
TESTES COMPLETOS - ENDPOINTS OPENAI (CHATGPT)
"""

import sys
sys.path.insert(0, '/home/ubuntu/robo-otimizador')

import json
from services.openai_strategic_engine import OpenAIStrategicEngine
from services.openai_campaign_creator import OpenAICampaignCreator
from services.openai_optimization_engine import OpenAIOptimizationEngine

class TestOpenAIEndpoints:
    """Testes para endpoints OpenAI"""
    
    def __init__(self):
        self.strategic = OpenAIStrategicEngine()
        self.campaign = OpenAICampaignCreator()
        self.optimization = OpenAIOptimizationEngine()
        self.results = []
        
    def test_analyze_persona(self):
        """Testar análise de persona"""
        print("🧪 Testando: Análise de Persona")
        
        business_data = {
            "name": "TechStore",
            "industry": "E-commerce de Tecnologia",
            "product": "Smartphones e Acessórios",
            "average_ticket": 1500,
            "location": "São Paulo, Brasil"
        }
        
        result = self.strategic.analyze_persona(business_data)
        
        success = result.get('success', False)
        self.results.append({
            "test": "analyze_persona",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_analyze_market(self):
        """Testar análise de mercado"""
        print("🧪 Testando: Análise de Mercado")
        
        result = self.strategic.analyze_market("E-commerce", "Brasil")
        
        success = result.get('success', False)
        self.results.append({
            "test": "analyze_market",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_create_marketing_strategy(self):
        """Testar criação de estratégia"""
        print("🧪 Testando: Criação de Estratégia de Marketing")
        
        campaign_data = {
            "objective": "Conversões",
            "product": "Smartphone Premium",
            "target_audience": "Profissionais 25-40 anos",
            "budget": 200,
            "duration": 30,
            "platforms": ["Google", "Facebook"]
        }
        
        result = self.strategic.create_marketing_strategy(campaign_data)
        
        success = result.get('success', False)
        self.results.append({
            "test": "create_marketing_strategy",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_generate_campaign_copy(self):
        """Testar geração de copy"""
        print("🧪 Testando: Geração de Copy de Campanha")
        
        campaign_data = {
            "product": "Smartphone X Pro",
            "objective": "Conversões",
            "audience": "Tech enthusiasts",
            "value_proposition": "Melhor câmera do mercado",
            "tone": "Moderno e inovador"
        }
        
        result = self.campaign.generate_campaign_copy(campaign_data, "google")
        
        success = result.get('success', False)
        self.results.append({
            "test": "generate_campaign_copy",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_generate_headlines(self):
        """Testar geração de headlines"""
        print("🧪 Testando: Geração de Headlines")
        
        product_data = {
            "name": "Smartphone X Pro",
            "main_benefit": "Câmera profissional",
            "unique_selling_point": "IA de última geração",
            "target_audience": "Fotógrafos e criadores"
        }
        
        result = self.campaign.generate_headlines(product_data, 5)
        
        success = result.get('success', False)
        self.results.append({
            "test": "generate_headlines",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_evaluate_campaign(self):
        """Testar avaliação de campanha"""
        print("🧪 Testando: Avaliação de Campanha")
        
        campaign_data = {
            "name": "Campanha Teste",
            "objective": "Conversões",
            "budget": 150,
            "duration": 15,
            "impressions": 50000,
            "clicks": 1250,
            "ctr": 2.5,
            "conversions": 75,
            "conversion_rate": 6.0,
            "cpc": 2.40,
            "cpa": 40,
            "roas": 3.2,
            "headlines": ["Compre Agora", "Oferta Limitada", "Melhor Preço"],
            "descriptions": ["Produto incrível", "Entrega rápida"]
        }
        
        result = self.optimization.evaluate_campaign(campaign_data)
        
        success = result.get('success', False)
        self.results.append({
            "test": "evaluate_campaign",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_recommend_budget_allocation(self):
        """Testar recomendação de orçamento"""
        print("🧪 Testando: Recomendação de Orçamento")
        
        campaigns = [
            {"name": "Campanha A", "budget": 100, "roas": 4.5, "conversions": 50, "cpa": 40, "potential_scale": "high"},
            {"name": "Campanha B", "budget": 80, "roas": 2.1, "conversions": 30, "cpa": 53, "potential_scale": "medium"},
            {"name": "Campanha C", "budget": 60, "roas": 1.2, "conversions": 15, "cpa": 80, "potential_scale": "low"}
        ]
        
        result = self.optimization.recommend_budget_allocation(campaigns, 300)
        
        success = result.get('success', False)
        self.results.append({
            "test": "recommend_budget_allocation",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def run_all_tests(self):
        """Executar todos os testes"""
        print("=" * 80)
        print("TESTES DE ENDPOINTS OPENAI (CHATGPT)")
        print("=" * 80)
        print()
        
        tests = [
            self.test_analyze_persona,
            self.test_analyze_market,
            self.test_create_marketing_strategy,
            self.test_generate_campaign_copy,
            self.test_generate_headlines,
            self.test_evaluate_campaign,
            self.test_recommend_budget_allocation
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"   ❌ ERRO: {str(e)}")
                failed += 1
            print()
        
        print("=" * 80)
        print(f"RESULTADO: {passed} PASSARAM | {failed} FALHARAM")
        print("=" * 80)
        
        return {
            "total": len(tests),
            "passed": passed,
            "failed": failed,
            "results": self.results
        }

if __name__ == "__main__":
    tester = TestOpenAIEndpoints()
    result = tester.run_all_tests()
    
    # Salvar resultados
    with open('/home/ubuntu/robo-otimizador/tests/openai_test_results.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✅ Resultados salvos em: tests/openai_test_results.json")

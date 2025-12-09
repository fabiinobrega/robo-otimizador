"""
TESTES COMPLETOS - ENDPOINTS MANUS (EXECUÇÃO)
"""

import sys
sys.path.insert(0, '/home/ubuntu/robo-otimizador')

import json
from services.manus_executor_bridge import ManusExecutorBridge
from services.nexora_automation import NexoraAutomation

class TestManusEndpoints:
    """Testes para endpoints Manus"""
    
    def __init__(self):
        self.executor = ManusExecutorBridge()
        self.automation = NexoraAutomation()
        self.results = []
        self.test_campaign_id = None
        
    def test_apply_campaign(self):
        """Testar aplicação de campanha"""
        print("🧪 Testando: Aplicação de Campanha")
        
        campaign_strategy = {
            "campaign_name": "Campanha Teste Manus",
            "objective": "CONVERSIONS",
            "budget": 150,
            "platforms": ["google"],
            "copy_variations": [
                {
                    "headline": "Compre Agora",
                    "description": "Melhor oferta do mercado"
                },
                {
                    "headline": "Oferta Limitada",
                    "description": "Não perca esta chance"
                }
            ],
            "targeting": {
                "age_range": "25-45",
                "interests": ["tecnologia", "inovação"]
            }
        }
        
        result = self.executor.apply_campaign(campaign_strategy)
        
        success = result.get('success', False)
        if success:
            self.test_campaign_id = result.get('campaign_id')
        
        self.results.append({
            "test": "apply_campaign",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        if success:
            print(f"   Campaign ID: {self.test_campaign_id}")
        return success
    
    def test_sync_to_google_ads(self):
        """Testar sincronização com Google Ads"""
        print("🧪 Testando: Sincronização com Google Ads")
        
        if not self.test_campaign_id:
            print("   ⚠️  SKIP: Nenhuma campanha criada")
            return False
        
        result = self.executor.sync_to_google_ads(self.test_campaign_id)
        
        success = result.get('success', False)
        self.results.append({
            "test": "sync_to_google_ads",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_sync_to_facebook_ads(self):
        """Testar sincronização com Facebook Ads"""
        print("🧪 Testando: Sincronização com Facebook Ads")
        
        if not self.test_campaign_id:
            print("   ⚠️  SKIP: Nenhuma campanha criada")
            return False
        
        result = self.executor.sync_to_facebook_ads(self.test_campaign_id)
        
        success = result.get('success', False)
        self.results.append({
            "test": "sync_to_facebook_ads",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_update_system_structure(self):
        """Testar atualização de estrutura"""
        print("🧪 Testando: Atualização de Estrutura do Sistema")
        
        updates = {
            "config": {
                "test_mode": True,
                "last_update": "2025-01-01"
            }
        }
        
        result = self.executor.update_system_structure(updates)
        
        success = result.get('success', False)
        self.results.append({
            "test": "update_system_structure",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_execute_budget_optimization(self):
        """Testar automação de otimização de orçamento"""
        print("🧪 Testando: Automação - Otimização de Orçamento")
        
        automation_config = {
            "type": "budget_optimization",
            "config": {
                "threshold_roas": 1.5
            }
        }
        
        result = self.executor.execute_automation(automation_config)
        
        success = result.get('success', False)
        self.results.append({
            "test": "execute_budget_optimization",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_create_automation(self):
        """Testar criação de automação"""
        print("🧪 Testando: Criação de Automação")
        
        automation_data = {
            "name": "Relatório Diário Teste",
            "type": "daily_report",
            "config": {},
            "schedule": "daily"
        }
        
        result = self.automation.create_automation(automation_data)
        
        success = result.get('success', False)
        self.results.append({
            "test": "create_automation",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        return success
    
    def test_get_automations(self):
        """Testar listagem de automações"""
        print("🧪 Testando: Listagem de Automações")
        
        result = self.automation.get_automations()
        
        success = result.get('success', False)
        self.results.append({
            "test": "get_automations",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        if success:
            print(f"   Total de automações: {result.get('count', 0)}")
        return success
    
    def run_all_tests(self):
        """Executar todos os testes"""
        print("=" * 80)
        print("TESTES DE ENDPOINTS MANUS (EXECUÇÃO)")
        print("=" * 80)
        print()
        
        tests = [
            self.test_apply_campaign,
            self.test_sync_to_google_ads,
            self.test_sync_to_facebook_ads,
            self.test_update_system_structure,
            self.test_execute_budget_optimization,
            self.test_create_automation,
            self.test_get_automations
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
    tester = TestManusEndpoints()
    result = tester.run_all_tests()
    
    # Salvar resultados
    with open('/home/ubuntu/robo-otimizador/tests/manus_test_results.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✅ Resultados salvos em: tests/manus_test_results.json")

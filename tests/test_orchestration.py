"""
TESTES COMPLETOS - ORQUESTRAÇÃO GPT → MANUS → NEXORA
"""

import sys
sys.path.insert(0, '/home/ubuntu/robo-otimizador')

import json
from services.orchestration_engine import AIOrchestrator

class TestOrchestration:
    """Testes para orquestração"""
    
    def __init__(self):
        self.orchestrator = AIOrchestrator()
        self.results = []
        
    def test_orchestration_status(self):
        """Testar status da orquestração"""
        print("🧪 Testando: Status da Orquestração")
        
        status = self.orchestrator.get_orchestration_status()
        
        success = (
            status.get('gpt_strategic_available') is not None and
            status.get('manus_executor_available') is not None
        )
        
        self.results.append({
            "test": "orchestration_status",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": status
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        print(f"   GPT Strategic: {status.get('gpt_strategic_available')}")
        print(f"   GPT Campaign: {status.get('gpt_campaign_available')}")
        print(f"   GPT Optimization: {status.get('gpt_optimization_available')}")
        print(f"   Manus Executor: {status.get('manus_executor_available')}")
        print(f"   Nexora Automation: {status.get('nexora_automation_available')}")
        
        return success
    
    def test_create_and_deploy_campaign(self):
        """Testar criação e deploy completo de campanha"""
        print("🧪 Testando: Criar e Implementar Campanha Completa")
        print("   (Este teste pode levar alguns minutos...)")
        
        campaign_request = {
            "name": "Campanha Orquestrada Teste",
            "product": "Smartphone Premium",
            "objective": "CONVERSIONS",
            "budget": 200,
            "audience": "Profissionais 25-40 anos, interessados em tecnologia",
            "platforms": ["google"],
            "value_proposition": "Melhor câmera do mercado com IA",
            "tone": "Profissional e inovador"
        }
        
        result = self.orchestrator.create_and_deploy_campaign(campaign_request)
        
        success = result.get('success', False)
        self.results.append({
            "test": "create_and_deploy_campaign",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        if success:
            print(f"   Execution ID: {result.get('execution_id')}")
            print(f"   Campaign ID: {result.get('campaign_id')}")
            print(f"   Etapas executadas: {len(result.get('execution_log', []))}")
        
        return success
    
    def test_optimize_and_scale(self):
        """Testar otimização e escala"""
        print("🧪 Testando: Otimizar e Escalar Campanha")
        print("   (Este teste pode levar alguns minutos...)")
        
        # Usar campanha fictícia para teste
        campaign_id = 1
        
        result = self.orchestrator.optimize_and_scale(campaign_id)
        
        success = result.get('success', False)
        self.results.append({
            "test": "optimize_and_scale",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        if success:
            print(f"   Execution ID: {result.get('execution_id')}")
            print(f"   Ações executadas: {len(result.get('actions_executed', []))}")
        
        return success
    
    def test_create_complete_funnel(self):
        """Testar criação de funil completo"""
        print("🧪 Testando: Criar Funil Completo")
        print("   (Este teste pode levar alguns minutos...)")
        
        funnel_request = {
            "name": "Funil de Vendas Teste",
            "product": "Curso Online Premium",
            "price": 497,
            "audience": "Empreendedores digitais",
            "objective": "Vendas"
        }
        
        result = self.orchestrator.create_complete_funnel(funnel_request)
        
        success = result.get('success', False)
        self.results.append({
            "test": "create_complete_funnel",
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": result
        })
        
        print(f"   {'✅ PASS' if success else '❌ FAIL'}")
        if success:
            print(f"   Execution ID: {result.get('execution_id')}")
            print(f"   Automações criadas: {len(result.get('automations', []))}")
        
        return success
    
    def run_all_tests(self):
        """Executar todos os testes"""
        print("=" * 80)
        print("TESTES DE ORQUESTRAÇÃO GPT → MANUS → NEXORA")
        print("=" * 80)
        print()
        
        tests = [
            self.test_orchestration_status,
            self.test_create_and_deploy_campaign,
            self.test_optimize_and_scale,
            self.test_create_complete_funnel
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
    tester = TestOrchestration()
    result = tester.run_all_tests()
    
    # Salvar resultados
    with open('/home/ubuntu/robo-otimizador/tests/orchestration_test_results.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✅ Resultados salvos em: tests/orchestration_test_results.json")

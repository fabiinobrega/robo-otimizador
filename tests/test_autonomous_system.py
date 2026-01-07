"""
🧪 TEST AUTONOMOUS SYSTEM - Testes do Sistema Autônomo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Suite completa de testes para o sistema de automação absoluta.

Cobertura:
- Agente residente
- Ciclo de vida de campanhas
- Modos de operação
- Validações de segurança
- Automação financeira
- Integração end-to-end

Autor: Manus AI
Data: 05 de Janeiro de 2026
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestManusAgent(unittest.TestCase):
    """Testes do Agente Residente"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        from services.manus_agent import ManusAgent
        self.agent = ManusAgent()
    
    def test_agent_initialization(self):
        """Testa inicialização do agente"""
        self.assertIsNotNone(self.agent)
        self.assertFalse(self.agent.is_running)
    
    def test_add_task(self):
        """Testa adição de tarefa"""
        from services.manus_agent import TaskPriority
        
        # Conectar ao banco (mock)
        self.agent.db_connection = MockDBConnection()
        
        task_id = self.agent.add_task(
            'monitor_campaign',
            TaskPriority.MEDIUM,
            {'campaign_id': 1}
        )
        
        self.assertIsNotNone(task_id)
    
    def test_task_retry_logic(self):
        """Testa lógica de retry automático"""
        # TODO: Implementar teste de retry
        pass
    
    def test_heartbeat_update(self):
        """Testa atualização de heartbeat"""
        # TODO: Implementar teste de heartbeat
        pass


class TestAutonomousCampaignEngine(unittest.TestCase):
    """Testes do Motor de Campanhas Autônomas"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        from services.autonomous_campaign_engine import AutonomousCampaignEngine
        self.engine = AutonomousCampaignEngine(None, None, None)
    
    def test_landing_page_analysis(self):
        """Testa análise de landing page"""
        result = self.engine._analyze_landing_page('https://exemplo.com/produto')
        
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('benefits', result)
    
    def test_scenario_simulation(self):
        """Testa simulação de cenários"""
        strategic_analysis = {
            'funnel_stage': 'conversion',
            'success_metrics': {
                'min_roas': 2.0
            }
        }
        
        result = self.engine._simulate_scenarios(
            strategic_analysis,
            budget=1000.0,
            duration=7,
            mode='SAFE'
        )
        
        self.assertIsNotNone(result)
        self.assertIn('scenarios', result)
        self.assertIn('estimated_roas', result)
    
    def test_approval_required(self):
        """Testa que aprovação é sempre necessária"""
        result = self.engine.create_campaign_autonomous(
            product_url='https://exemplo.com/produto',
            budget_total=1000.0,
            duration_days=7,
            mode='SAFE'
        )
        
        self.assertTrue(result.get('requires_approval'))
        self.assertEqual(result.get('status'), 'AWAITING_APPROVAL')


class TestOperationModes(unittest.TestCase):
    """Testes dos Modos de Operação"""
    
    def test_safe_mode_config(self):
        """Testa configuração do SAFE MODE"""
        from services.operation_modes import SafeMode
        
        config = SafeMode.get_config()
        
        self.assertEqual(config['mode'], 'SAFE')
        self.assertEqual(config['budget_strategy']['initial_test_budget_pct'], 0.20)
        self.assertEqual(config['pause_criteria']['min_roas'], 1.2)
    
    def test_aggressive_mode_config(self):
        """Testa configuração do AGGRESSIVE SCALE MODE"""
        from services.operation_modes import AggressiveScaleMode
        
        config = AggressiveScaleMode.get_config()
        
        self.assertEqual(config['mode'], 'AGGRESSIVE_SCALE')
        self.assertEqual(config['budget_strategy']['scale_increment_pct'], 0.50)
    
    def test_scale_readiness_checker(self):
        """Testa checklist de prontidão para escala"""
        from services.operation_modes import ScaleReadinessChecker
        
        campaign_metrics = {
            'roas_history': [2.5, 2.6, 2.7],
            'cpa': 45.0,
            'max_cpa_limit': 50.0,
            'ctr_history': [1.5, 1.6, 1.5],
            'frequency': 2.0,
            'conversion_rate': 2.5,
            'scale_approved_by_user': False,
            'critical_errors_24h': 0
        }
        
        result = ScaleReadinessChecker.check_readiness(campaign_metrics)
        
        self.assertIsNotNone(result)
        self.assertIn('ready_to_scale', result)
        self.assertIn('checklist', result)
        
        # Deve ser False porque budget não foi aprovado
        self.assertFalse(result['ready_to_scale'])
    
    def test_mode_selection(self):
        """Testa seleção automática de modo"""
        from services.operation_modes import OperationModeManager, OperationMode
        
        # Contexto de risco alto
        context_high_risk = {
            'is_new_account': True,
            'is_new_product': True,
            'budget_total': 300
        }
        
        mode = OperationModeManager.select_mode(context_high_risk)
        self.assertEqual(mode, OperationMode.SAFE)
        
        # Contexto de baixo risco
        context_low_risk = {
            'is_new_account': False,
            'is_new_product': False,
            'budget_total': 5000,
            'has_stable_metrics': True,
            'roas': 3.0
        }
        
        mode = OperationModeManager.select_mode(context_low_risk)
        self.assertEqual(mode, OperationMode.AGGRESSIVE_SCALE)


class TestPreExecutionValidator(unittest.TestCase):
    """Testes do Validador de Pré-Execução"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        from services.pre_execution_validator_global import PreExecutionValidator
        self.validator = PreExecutionValidator()
    
    def test_budget_validation_minimum(self):
        """Testa validação de orçamento mínimo"""
        context = {
            'budget_total': 30.0,  # Abaixo do mínimo (R$ 50)
            'duration_days': 7
        }
        
        result = self.validator._validate_budget(context)
        
        self.assertFalse(result.passed)
        self.assertIn('mínimo', result.message.lower())
    
    def test_budget_validation_daily_minimum(self):
        """Testa validação de orçamento diário mínimo"""
        context = {
            'budget_total': 50.0,
            'duration_days': 15  # R$ 3.33/dia (abaixo do mínimo R$ 5/dia)
        }
        
        result = self.validator._validate_budget(context)
        
        self.assertFalse(result.passed)
        self.assertIn('diário', result.message.lower())
    
    def test_budget_validation_valid(self):
        """Testa validação de orçamento válido"""
        context = {
            'budget_total': 500.0,
            'duration_days': 7
        }
        
        result = self.validator._validate_budget(context)
        
        self.assertTrue(result.passed)
    
    def test_pixel_validation_missing(self):
        """Testa validação de pixel ausente"""
        context = {
            'pixel_id': None
        }
        
        result = self.validator._validate_pixel(context)
        
        self.assertFalse(result.passed)
        self.assertIn('pixel', result.message.lower())
    
    def test_user_approval_required(self):
        """Testa que aprovação do usuário é obrigatória"""
        context = {
            'action_type': 'create_campaign',
            'budget_total': 1000.0,
            'approval_token': None
        }
        
        result = self.validator._validate_user_approval(context)
        
        self.assertFalse(result.passed)
        self.assertIn('aprovação', result.message.lower())
    
    def test_validate_all_blocks_on_critical(self):
        """Testa que validação bloqueia em falhas críticas"""
        context = {
            'action_type': 'create_campaign',
            'budget_total': 30.0,  # Abaixo do mínimo
            'duration_days': 7,
            'platform': 'facebook',
            'pixel_id': None,  # Pixel ausente
            'approval_token': None  # Sem aprovação
        }
        
        can_execute, results = self.validator.validate_all(context)
        
        self.assertFalse(can_execute)
        self.assertGreater(len(results), 0)


class TestFinancialAutomation(unittest.TestCase):
    """Testes da Automação Financeira"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        from services.financial_automation_service import FinancialAutomationService
        self.service = FinancialAutomationService()
    
    def test_credit_purchase_requires_approval(self):
        """Testa que compra de créditos requer aprovação"""
        result = self.service.request_credit_purchase(
            user_id=1,
            amount=100.0,
            reason='Teste',
            auto_approved=False
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], 'PENDING_APPROVAL')
        self.assertIn('approval_url', result)
    
    def test_ads_reload_requires_approval(self):
        """Testa que recarga de anúncios requer aprovação"""
        result = self.service.request_ads_reload(
            user_id=1,
            platform='facebook',
            amount=200.0,
            campaign_id=123,
            reason='Escala automática',
            auto_approved=False
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], 'PENDING_APPROVAL')
    
    def test_auto_approved_processes_immediately(self):
        """Testa que transações pré-aprovadas processam imediatamente"""
        result = self.service.request_credit_purchase(
            user_id=1,
            amount=100.0,
            reason='Teste pré-aprovado',
            auto_approved=True
        )
        
        # Deve processar imediatamente (ou falhar se Stripe não configurado)
        self.assertIn('status', result)


class TestEndToEndIntegration(unittest.TestCase):
    """Testes de Integração End-to-End"""
    
    def test_full_campaign_cycle(self):
        """Testa ciclo completo de campanha"""
        # TODO: Implementar teste end-to-end completo
        pass
    
    def test_auto_optimization_flow(self):
        """Testa fluxo de otimização automática"""
        # TODO: Implementar teste de otimização
        pass
    
    def test_scale_decision_flow(self):
        """Testa fluxo de decisão de escala"""
        # TODO: Implementar teste de escala
        pass


class MockDBConnection:
    """Mock de conexão de banco de dados para testes"""
    
    def __init__(self):
        self.is_connected_flag = True
    
    def is_connected(self):
        return self.is_connected_flag
    
    def cursor(self, dictionary=False):
        return MockCursor()
    
    def commit(self):
        pass
    
    def close(self):
        self.is_connected_flag = False


class MockCursor:
    """Mock de cursor de banco de dados"""
    
    def execute(self, query, params=None):
        pass
    
    def fetchone(self):
        return None
    
    def fetchall(self):
        return []
    
    def close(self):
        pass
    
    @property
    def lastrowid(self):
        return 1


def run_all_tests():
    """Executa todos os testes"""
    print("🧪 Executando suite de testes do Nexora Prime...")
    print("=" * 80)
    
    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar testes
    suite.addTests(loader.loadTestsFromTestCase(TestManusAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestAutonomousCampaignEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestOperationModes))
    suite.addTests(loader.loadTestsFromTestCase(TestPreExecutionValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestFinancialAutomation))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndIntegration))
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 80)
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"❌ Erros: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

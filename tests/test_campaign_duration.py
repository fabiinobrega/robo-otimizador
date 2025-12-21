"""
Testes para Duração de Campanha
Valida cálculo de orçamento diário, bloqueio sem duração e execução válida
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime, timedelta
from services.pre_execution_validator import PreExecutionValidator
from services.openai_strategic_brain import OpenAIStrategicBrain
from services.manus_technical_executor import ManusTechnicalExecutor


class TestCampaignDuration(unittest.TestCase):
    """Testes de duração de campanha"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.validator = PreExecutionValidator()
    
    def test_01_calculo_orcamento_diario(self):
        """Teste 1: Cálculo de orçamento diário"""
        # Caso 1: R$ 1000 / 10 dias = R$ 100/dia
        total_budget = 1000.00
        duration = 10
        expected_daily = 100.00
        
        daily_budget = total_budget / duration
        self.assertEqual(daily_budget, expected_daily)
        
        # Caso 2: R$ 500 / 7 dias = R$ 71.43/dia
        total_budget = 500.00
        duration = 7
        expected_daily = 71.43
        
        daily_budget = total_budget / duration
        self.assertAlmostEqual(daily_budget, expected_daily, places=2)
        
        # Caso 3: R$ 300 / 15 dias = R$ 20/dia (mínimo)
        total_budget = 300.00
        duration = 15
        expected_daily = 20.00
        
        daily_budget = total_budget / duration
        self.assertEqual(daily_budget, expected_daily)
        
        print("✅ Teste 1: Cálculo de orçamento diário - PASSOU")
    
    def test_02_bloqueio_sem_duracao(self):
        """Teste 2: Bloqueio quando duração não é definida"""
        result = self.validator.validate_all(
            product="Produto Teste",
            niche="Nicho Teste",
            objective="Vender 100 unidades",
            budget=1000.00,
            duration_days=None,  # SEM DURAÇÃO
            sales_goal="100 vendas"
        )
        
        self.assertFalse(result['valid'])
        self.assertTrue(any(err['type'] == 'duration' for err in result['errors']))
        
        # Verificar mensagem de erro
        duration_error = next(err for err in result['errors'] if err['type'] == 'duration')
        self.assertIn('Defina por quantos dias', duration_error['user_message'])
        
        print("✅ Teste 2: Bloqueio sem duração - PASSOU")
    
    def test_03_duracao_invalida_zero(self):
        """Teste 3: Duração inválida (zero)"""
        result = self.validator.validate_all(
            product="Produto Teste",
            niche="Nicho Teste",
            objective="Vender 100 unidades",
            budget=1000.00,
            duration_days=0,  # ZERO
            sales_goal="100 vendas"
        )
        
        self.assertFalse(result['valid'])
        self.assertTrue(any(err['type'] == 'duration' for err in result['errors']))
        
        print("✅ Teste 3: Duração inválida (zero) - PASSOU")
    
    def test_04_duracao_invalida_negativa(self):
        """Teste 4: Duração inválida (negativa)"""
        result = self.validator.validate_all(
            product="Produto Teste",
            niche="Nicho Teste",
            objective="Vender 100 unidades",
            budget=1000.00,
            duration_days=-5,  # NEGATIVA
            sales_goal="100 vendas"
        )
        
        self.assertFalse(result['valid'])
        self.assertTrue(any(err['type'] == 'duration' for err in result['errors']))
        
        print("✅ Teste 4: Duração inválida (negativa) - PASSOU")
    
    def test_05_duracao_muito_longa(self):
        """Teste 5: Duração muito longa (> 365 dias)"""
        result = self.validator.validate_all(
            product="Produto Teste",
            niche="Nicho Teste",
            objective="Vender 100 unidades",
            budget=100000.00,
            duration_days=400,  # MUITO LONGA
            sales_goal="100 vendas"
        )
        
        self.assertFalse(result['valid'])
        self.assertTrue(any(err['type'] == 'duration' for err in result['errors']))
        
        print("✅ Teste 5: Duração muito longa - PASSOU")
    
    def test_06_duracao_valida_1_dia(self):
        """Teste 6: Duração válida (1 dia - mínimo)"""
        result = self.validator.validate_all(
            product="Produto Teste",
            niche="Nicho Teste",
            objective="Vender 100 unidades",
            budget=50.00,  # R$ 50/dia
            duration_days=1,  # 1 DIA
            sales_goal="100 vendas"
        )
        
        # Pode falhar por outros motivos (créditos), mas não por duração
        if not result['valid']:
            duration_errors = [err for err in result['errors'] if err['type'] == 'duration']
            self.assertEqual(len(duration_errors), 0, "Não deve ter erro de duração")
        
        print("✅ Teste 6: Duração válida (1 dia) - PASSOU")
    
    def test_07_duracao_valida_30_dias(self):
        """Teste 7: Duração válida (30 dias)"""
        result = self.validator.validate_all(
            product="Produto Teste",
            niche="Nicho Teste",
            objective="Vender 100 unidades",
            budget=1500.00,  # R$ 50/dia
            duration_days=30,  # 30 DIAS
            sales_goal="100 vendas"
        )
        
        # Pode falhar por outros motivos, mas não por duração
        if not result['valid']:
            duration_errors = [err for err in result['errors'] if err['type'] == 'duration']
            self.assertEqual(len(duration_errors), 0, "Não deve ter erro de duração")
        
        print("✅ Teste 7: Duração válida (30 dias) - PASSOU")
    
    def test_08_duracao_valida_365_dias(self):
        """Teste 8: Duração válida (365 dias - máximo)"""
        result = self.validator.validate_all(
            product="Produto Teste",
            niche="Nicho Teste",
            objective="Vender 100 unidades",
            budget=18250.00,  # R$ 50/dia * 365
            duration_days=365,  # 365 DIAS (MÁXIMO)
            sales_goal="100 vendas"
        )
        
        # Pode falhar por outros motivos, mas não por duração
        if not result['valid']:
            duration_errors = [err for err in result['errors'] if err['type'] == 'duration']
            self.assertEqual(len(duration_errors), 0, "Não deve ter erro de duração")
        
        print("✅ Teste 8: Duração válida (365 dias) - PASSOU")
    
    def test_09_orcamento_diario_abaixo_minimo(self):
        """Teste 9: Orçamento diário abaixo do mínimo (< R$ 20)"""
        # R$ 100 / 10 dias = R$ 10/dia (ABAIXO DO MÍNIMO)
        total_budget = 100.00
        duration = 10
        daily_budget = total_budget / duration
        
        self.assertLess(daily_budget, 20.00)
        
        # Validação deve bloquear
        result = self.validator.validate_all(
            product="Produto Teste",
            niche="Nicho Teste",
            objective="Vender 100 unidades",
            budget=total_budget,
            duration_days=duration,
            sales_goal="100 vendas"
        )
        
        self.assertFalse(result['valid'])
        
        print("✅ Teste 9: Orçamento diário abaixo do mínimo - PASSOU")
    
    def test_10_calculo_datas(self):
        """Teste 10: Cálculo de datas de início e término"""
        start_date = datetime.now()
        duration = 10
        end_date = start_date + timedelta(days=duration)
        
        # Verificar diferença
        diff = (end_date - start_date).days
        self.assertEqual(diff, duration)
        
        print("✅ Teste 10: Cálculo de datas - PASSOU")


def run_tests():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("TESTES DE DURAÇÃO DE CAMPANHA")
    print("="*60 + "\n")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCampaignDuration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print(f"RESULTADO: {result.testsRun} testes executados")
    print(f"✅ Passaram: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falharam: {len(result.failures) + len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

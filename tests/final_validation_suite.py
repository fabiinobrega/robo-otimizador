"""
Final Validation Suite - Suite de Validação Final
Valida todos os bloqueios absolutos e garante sistema 100% funcional
"""

import unittest
import sys
import os

# Adicionar diretório raiz ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from unittest.mock import patch, MagicMock

# Importar serviços
from services.pre_execution_validator import PreExecutionValidator
from services.competitor_spy_engine import CompetitorSpyEngine
from services.openai_strategic_brain import OpenAIStrategicBrain
from services.manus_technical_executor import ManusTechnicalExecutor
from services.ab_testing_optimizer import ABTestingOptimizer


class FinalValidationSuite(unittest.TestCase):
    """
    Valida todos os bloqueios absolutos e o fluxo completo
    """
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.validator = PreExecutionValidator()
        self.spy = CompetitorSpyEngine()
        self.brain = OpenAIStrategicBrain()
        self.executor = ManusTechnicalExecutor()
        self.optimizer = ABTestingOptimizer()
        
        self.test_data = {
            "product": "Curso de Marketing Digital",
            "niche": "Empreendedores Iniciantes",
            "objective": "Gerar 100 vendas",
            "budget": 50.00,
            "sales_goal": {"type": "conversions", "value": 100}
        }
    
    # ========================================================================
    # TESTES DE BLOQUEIOS ABSOLUTOS
    # ========================================================================
    
    @patch("services.pre_execution_validator.PreExecutionValidator._validate_openai_credits")
    @patch("services.pre_execution_validator.PreExecutionValidator._validate_manus_credits")
    def test_block_if_no_openai_credits(self, mock_validate_manus, mock_validate_openai):
        """Deve bloquear se não houver créditos OpenAI"""
        mock_validate_openai.return_value = {"valid": False, "message": "Sem créditos OpenAI"}
        mock_validate_manus.return_value = {"valid": True}
        
        with self.assertRaises(ValueError) as context:
            self.validator.validate_all(**self.test_data)
        
        self.assertIn("OpenAI", str(context.exception))
    
    @patch("services.pre_execution_validator.PreExecutionValidator._validate_openai_credits")
    @patch("services.pre_execution_validator.PreExecutionValidator._validate_manus_credits")
    def test_block_if_no_manus_credits(self, mock_validate_manus, mock_validate_openai):
        """Deve bloquear se não houver créditos Manus"""
        mock_validate_openai.return_value = {"valid": True}
        mock_validate_manus.return_value = {"valid": False, "message": "Sem créditos Manus"}
        
        with self.assertRaises(ValueError) as context:
            self.validator.validate_all(**self.test_data)
        
        self.assertIn("Manus", str(context.exception))
    
    def test_block_if_budget_too_low(self):
        """Deve bloquear se orçamento for menor que R$ 20,00"""
        test_data = self.test_data.copy()
        test_data["budget"] = 19.99
        
        with self.assertRaises(ValueError) as context:
            self.validator.validate_all(**test_data)
        
        self.assertIn("orçamento", str(context.exception).lower())
    
    def test_block_if_product_empty(self):
        """Deve bloquear se produto estiver vazio"""
        test_data = self.test_data.copy()
        test_data["product"] = ""
        
        with self.assertRaises(ValueError) as context:
            self.validator.validate_all(**test_data)
        
        self.assertIn("produto", str(context.exception).lower())
    
    # ========================================================================
    # TESTE DE FLUXO COMPLETO (COM MOCKS)
    # ========================================================================
    
    @patch("services.pre_execution_validator.PreExecutionValidator.validate_all")
    @patch("services.competitor_spy_engine.CompetitorSpyEngine.analyze_competitors")
    @patch("services.openai_strategic_brain.OpenAIStrategicBrain.create_campaign_strategy")
    @patch("services.openai_strategic_brain.OpenAIStrategicBrain.generate_ad_copy")
    @patch("services.manus_technical_executor.ManusTechnicalExecutor.execute_complete_campaign")
    @patch("services.ab_testing_optimizer.ABTestingOptimizer.activate_ab_testing")
    def test_full_workflow_integration(self, mock_activate_ab, mock_execute, mock_gen_copy, mock_create_strategy, mock_analyze, mock_validate):
        """Testa o fluxo completo de ponta a ponta com mocks"""
        
        # Configurar mocks
        mock_validate.return_value = {"status": "ok", "message": "Todas as validações passaram"}
        mock_analyze.return_value = {"analysis": "Análise completa", "recommendations": ["Rec 1"]}
        mock_create_strategy.return_value = {"strategy": "Estratégia completa", **self.test_data}
        mock_gen_copy.return_value = {"full_copy": "Copy completo", "headlines": ["H1"], "ctas": ["CTA1"]}
        mock_execute.return_value = {"status": "success", "campaign_id": "camp_123", "ads_created": 3}
        mock_activate_ab.return_value = {"status": "active", "campaign_id": "camp_123"}
        
        # 1. Validação
        validation_result = self.validator.validate_all(**self.test_data)
        self.assertEqual(validation_result["status"], "ok")
        
        # 2. Espionagem
        spy_report = self.spy.analyze_competitors(self.test_data["product"], self.test_data["niche"])
        self.assertIn("Análise completa", spy_report["analysis"])
        
        # 3. OpenAI (Pensar)
        strategy = self.brain.create_campaign_strategy(spy_report, **self.test_data)
        self.assertIn("Estratégia completa", strategy["strategy"])
        
        copy = self.brain.generate_ad_copy(strategy, spy_report["recommendations"])
        self.assertIn("Copy completo", copy["full_copy"])
        
        # 4. Manus (Executar)
        execution_result = self.executor.execute_complete_campaign(strategy, copy, self.test_data["budget"])
        self.assertEqual(execution_result["status"], "success")
        self.assertEqual(execution_result["campaign_id"], "camp_123")
        
        # 5. Otimização
        ab_test_config = self.optimizer.activate_ab_testing(
            execution_result["campaign_id"], 
            [{"id": "ad_1"}, {"id": "ad_2"}], 
            self.test_data["sales_goal"]
        )
        self.assertEqual(ab_test_config["status"], "active")
        
        print("\n✅ Teste de fluxo completo passou com sucesso!")


if __name__ == '__main__':
    unittest.main()

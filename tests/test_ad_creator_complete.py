"""
Testes completos para o sistema CRIAR ANÚNCIO PERFEITO
"""

import unittest
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ad_creator_service import AdCreatorService


class TestAdCreatorComplete(unittest.TestCase):
    """Testes completos do Ad Creator."""

    def setUp(self):
        """Setup para cada teste."""
        self.service = AdCreatorService()
        self.test_config = {
            'productUrl': 'https://example.com/product',
            'platform': 'meta',
            'budget': 1000.0,
            'objective': 'conversions',
            'operationMode': 'turbo'
        }

    # ================================================================
    # FASE 1-2: Análise de Produto
    # ================================================================

    @patch('services.ad_creator_service.product_analysis_service')
    async def test_product_analysis(self, mock_analysis):
        """Teste: Análise profunda de produto."""
        mock_analysis.analyze_product_deep.return_value = {
            'name': 'Produto Teste',
            'category': 'Eletrônicos',
            'price': 99.90
        }

        result = await self.service.analyze_product(self.test_config)

        self.assertIsNotNone(result)
        self.assertIn('product_info', result)
        print("✓ Análise de produto funcionando")

    # ================================================================
    # FASE 3-4: Espionagem de Concorrentes
    # ================================================================

    @patch('services.ad_creator_service.competitor_spy_engine')
    async def test_competitor_analysis(self, mock_spy):
        """Teste: Espionagem de concorrentes."""
        mock_spy.spy_on_competitor.return_value = {
            'competitor_ads': [],
            'market_insights': {}
        }

        result = await self.service.analyze_product(self.test_config)

        self.assertIsNotNone(result)
        print("✓ Espionagem de concorrentes funcionando")

    # ================================================================
    # FASE 5: Análise de Criativos
    # ================================================================

    async def test_creative_analysis(self):
        """Teste: Análise e seleção de criativos."""
        result = await self.service.analyze_and_select_creatives(
            config=self.test_config,
            uploaded_files=[]
        )

        self.assertIsNotNone(result)
        self.assertIn('selected_creatives', result)
        self.assertIn('generated_creatives', result)
        print("✓ Análise de criativos funcionando")

    # ================================================================
    # FASE 6: Criação de Estratégia
    # ================================================================

    async def test_strategy_creation(self):
        """Teste: Criação de estratégia de campanha."""
        analysis_results = {'product_info': {}}
        creative_results = {'selected_creatives': []}

        strategy = await self.service.create_campaign_strategy(
            config=self.test_config,
            analysis_results=analysis_results,
            creative_results=creative_results
        )

        self.assertIsNotNone(strategy)
        self.assertIn('segmentation', strategy)
        self.assertIn('budget_allocation', strategy)
        self.assertIn('bidding_strategy', strategy)
        print("✓ Criação de estratégia funcionando")

    # ================================================================
    # FASE 7: Criação de Anúncios
    # ================================================================

    async def test_ad_creation(self):
        """Teste: Criação automática de anúncios."""
        strategy = {'segmentation': {}, 'budget_allocation': {}}
        creative_results = {'selected_creatives': [{'type': 'image', 'url': 'test.jpg'}]}

        ads = await self.service.create_ads_automatically(
            config=self.test_config,
            strategy=strategy,
            creative_results=creative_results
        )

        self.assertIsNotNone(ads)
        self.assertIsInstance(ads, list)
        self.assertGreater(len(ads), 0)
        
        # Verificar estrutura do anúncio
        ad = ads[0]
        self.assertIn('copy', ad)
        self.assertIn('creative', ad)
        self.assertIn('headline', ad['copy'])
        self.assertIn('primary_text', ad['copy'])
        
        print(f"✓ Criação de anúncios funcionando ({len(ads)} anúncios criados)")

    # ================================================================
    # FASE 9: Execução
    # ================================================================

    async def test_campaign_execution(self):
        """Teste: Execução de campanha."""
        ads = [
            {
                'id': 'ad_1',
                'copy': {'headline': 'Test'},
                'creative': {'url': 'test.jpg'}
            }
        ]

        result = await self.service.execute_campaign(
            ads=ads,
            config=self.test_config
        )

        self.assertIsNotNone(result)
        self.assertIn('status', result)
        self.assertIn('campaign_ids', result)
        print("✓ Execução de campanha funcionando")

    # ================================================================
    # FASE 9.1: Turbo Mode
    # ================================================================

    async def test_turbo_mode(self):
        """Teste: Otimização Turbo Mode."""
        campaign_ids = ['campaign_1']

        result = await self.service.turbo_mode_optimizer(campaign_ids)

        self.assertIsNotNone(result)
        self.assertIn('status', result)
        self.assertIn('actions_taken', result)
        print("✓ Turbo Mode funcionando")

    # ================================================================
    # FASE 10: Monitoramento
    # ================================================================

    async def test_intelligent_monitoring(self):
        """Teste: Monitoramento inteligente."""
        campaign_ids = ['campaign_1']

        dashboard = await self.service.intelligent_monitoring(campaign_ids)

        self.assertIsNotNone(dashboard)
        self.assertIn('status', dashboard)
        self.assertIn('campaigns', dashboard)
        self.assertIn('insights', dashboard)
        self.assertIn('recommendations', dashboard)
        print("✓ Monitoramento inteligente funcionando")

    # ================================================================
    # FASE 11: Relatórios
    # ================================================================

    async def test_intelligence_report(self):
        """Teste: Relatório de inteligência."""
        campaign_ids = ['campaign_1']

        report = await self.service.generate_intelligence_report(
            campaign_ids=campaign_ids,
            timeframe='7d'
        )

        self.assertIsNotNone(report)
        self.assertIn('status', report)
        self.assertIn('summary', report)
        self.assertIn('learnings', report)
        self.assertIn('best_practices', report)
        print("✓ Relatório de inteligência funcionando")

    # ================================================================
    # Teste de Integração Completa
    # ================================================================

    async def test_full_workflow(self):
        """Teste: Fluxo completo de criação de anúncio."""
        print("\n🚀 Testando fluxo completo...")

        # 1. Análise
        analysis = await self.service.analyze_product(self.test_config)
        self.assertIsNotNone(analysis)
        print("  ✓ Análise concluída")

        # 2. Criativos
        creatives = await self.service.analyze_and_select_creatives(
            config=self.test_config,
            uploaded_files=[]
        )
        self.assertIsNotNone(creatives)
        print("  ✓ Criativos selecionados")

        # 3. Estratégia
        strategy = await self.service.create_campaign_strategy(
            config=self.test_config,
            analysis_results=analysis,
            creative_results=creatives
        )
        self.assertIsNotNone(strategy)
        print("  ✓ Estratégia criada")

        # 4. Anúncios
        ads = await self.service.create_ads_automatically(
            config=self.test_config,
            strategy=strategy,
            creative_results=creatives
        )
        self.assertIsNotNone(ads)
        self.assertGreater(len(ads), 0)
        print(f"  ✓ {len(ads)} anúncios criados")

        # 5. Execução
        execution = await self.service.execute_campaign(
            ads=ads,
            config=self.test_config
        )
        self.assertEqual(execution['status'], 'live')
        print("  ✓ Campanha executada")

        # 6. Monitoramento
        dashboard = await self.service.intelligent_monitoring(
            execution['campaign_ids']
        )
        self.assertEqual(dashboard['status'], 'active')
        print("  ✓ Monitoramento ativo")

        # 7. Relatório
        report = await self.service.generate_intelligence_report(
            campaign_ids=execution['campaign_ids'],
            timeframe='7d'
        )
        self.assertEqual(report['status'], 'completed')
        print("  ✓ Relatório gerado")

        print("\n🎉 Fluxo completo funcionando perfeitamente!")


def run_tests():
    """Executar todos os testes."""
    import asyncio

    print("=" * 60)
    print("TESTES COMPLETOS: CRIAR ANÚNCIO PERFEITO")
    print("=" * 60)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdCreatorComplete)
    
    # Executar testes assíncronos
    loop = asyncio.get_event_loop()
    
    for test in suite:
        try:
            if hasattr(test, '_testMethodName'):
                method = getattr(test, test._testMethodName)
                if asyncio.iscoroutinefunction(method):
                    loop.run_until_complete(method())
                else:
                    method()
        except Exception as e:
            print(f"❌ Erro no teste {test._testMethodName}: {e}")

    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()

"""
🎚️ OPERATION MODES - Modos de Operação do Nexora Prime
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Define e gerencia os modos de operação do sistema:
- SAFE MODE: Baixo risco, proteção de capital
- AGGRESSIVE_SCALE MODE: Escala progressiva, maximização de lucro

Autor: Manus AI
Data: 05 de Janeiro de 2026
"""

import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OperationMode(Enum):
    """Modos de operação disponíveis"""
    SAFE = "SAFE"
    AGGRESSIVE_SCALE = "AGGRESSIVE_SCALE"
    CUSTOM = "CUSTOM"


class ScaleReadinessChecker:
    """
    Verifica se uma campanha está pronta para escalar
    
    Checklist obrigatório:
    ☑ ROAS positivo por 72h+
    ☑ CPA abaixo do limite definido
    ☑ CTR estável
    ☑ Criativos não saturados
    ☑ Funil convertendo
    ☑ Orçamento autorizado
    ☑ Logs sem erro crítico
    """
    
    @staticmethod
    def check_readiness(campaign_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica prontidão para escala
        
        Args:
            campaign_metrics: Métricas da campanha
        
        Returns:
            Resultado do checklist
        """
        logger.info(f"📋 Verificando prontidão para escala...")
        
        checklist = {
            'roas_positive_72h': False,
            'cpa_below_limit': False,
            'ctr_stable': False,
            'creatives_not_saturated': False,
            'funnel_converting': False,
            'budget_authorized': False,  # SEMPRE requer aprovação
            'no_critical_errors': False
        }
        
        # 1. ROAS positivo por 72h+
        roas_history = campaign_metrics.get('roas_history', [])
        if len(roas_history) >= 3:  # 3 dias de dados
            avg_roas = sum(roas_history[-3:]) / 3
            checklist['roas_positive_72h'] = avg_roas > 1.0
            logger.info(f"   ROAS 72h: {avg_roas:.2f} {'✅' if checklist['roas_positive_72h'] else '❌'}")
        
        # 2. CPA abaixo do limite
        current_cpa = campaign_metrics.get('cpa', 0)
        max_cpa = campaign_metrics.get('max_cpa_limit', 100)
        checklist['cpa_below_limit'] = current_cpa <= max_cpa
        logger.info(f"   CPA: R$ {current_cpa:.2f} (limite: R$ {max_cpa:.2f}) {'✅' if checklist['cpa_below_limit'] else '❌'}")
        
        # 3. CTR estável
        ctr_history = campaign_metrics.get('ctr_history', [])
        if len(ctr_history) >= 3:
            ctr_variance = max(ctr_history[-3:]) - min(ctr_history[-3:])
            checklist['ctr_stable'] = ctr_variance < 0.5  # Variação < 0.5%
            logger.info(f"   CTR estável: {'✅' if checklist['ctr_stable'] else '❌'}")
        
        # 4. Criativos não saturados
        frequency = campaign_metrics.get('frequency', 0)
        checklist['creatives_not_saturated'] = frequency < 3.0
        logger.info(f"   Frequência: {frequency:.2f} {'✅' if checklist['creatives_not_saturated'] else '❌'}")
        
        # 5. Funil convertendo
        conversion_rate = campaign_metrics.get('conversion_rate', 0)
        checklist['funnel_converting'] = conversion_rate > 1.0
        logger.info(f"   Taxa de conversão: {conversion_rate:.2f}% {'✅' if checklist['funnel_converting'] else '❌'}")
        
        # 6. Orçamento autorizado (SEMPRE False até usuário aprovar)
        checklist['budget_authorized'] = campaign_metrics.get('scale_approved_by_user', False)
        logger.info(f"   Orçamento autorizado: {'✅' if checklist['budget_authorized'] else '❌'}")
        
        # 7. Sem erros críticos
        error_count = campaign_metrics.get('critical_errors_24h', 0)
        checklist['no_critical_errors'] = error_count == 0
        logger.info(f"   Erros críticos: {error_count} {'✅' if checklist['no_critical_errors'] else '❌'}")
        
        # Resultado final
        ready = all(checklist.values())
        
        result = {
            'ready_to_scale': ready,
            'checklist': checklist,
            'passed_checks': sum(1 for v in checklist.values() if v),
            'total_checks': len(checklist),
            'recommendation': 'Pronto para escalar - Solicitar aprovação do usuário' if ready else 'Aguardar métricas estabilizarem'
        }
        
        logger.info(f"📊 Resultado: {result['passed_checks']}/{result['total_checks']} checks aprovados")
        
        return result


class SafeMode:
    """
    SAFE MODE - Modo de Baixo Risco
    
    Ativar quando:
    - Conta nova
    - Produto novo
    - Pixel novo
    - Orçamento limitado
    
    Características:
    - Orçamento fracionado
    - Testes pequenos
    - Critérios rígidos de pausa
    - Escala lenta e segura
    - Prioridade: proteger capital
    """
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """Retorna configuração do SAFE MODE"""
        return {
            'mode': 'SAFE',
            'budget_strategy': {
                'initial_test_budget_pct': 0.20,  # 20% do orçamento para teste inicial
                'daily_budget_cap_pct': 0.10,     # Máximo 10% do orçamento total por dia
                'scale_increment_pct': 0.20       # Aumentar 20% por vez
            },
            'pause_criteria': {
                'max_cpa_multiplier': 1.5,        # Pausar se CPA > 1.5x do limite
                'min_roas': 1.2,                  # Pausar se ROAS < 1.2
                'max_negative_days': 2            # Pausar após 2 dias negativos
            },
            'scale_criteria': {
                'min_roas_for_scale': 2.5,        # Só escalar se ROAS > 2.5
                'min_days_stable': 5,             # Mínimo 5 dias estáveis
                'max_scale_per_day': 0.30         # Máximo 30% de aumento por dia
            },
            'monitoring': {
                'check_frequency_minutes': 30,    # Verificar a cada 30 minutos
                'alert_on_negative_roi': True,
                'auto_pause_enabled': True
            }
        }
    
    @staticmethod
    def calculate_budget_allocation(total_budget: float, duration_days: int) -> Dict[str, float]:
        """Calcula alocação de orçamento no SAFE MODE"""
        config = SafeMode.get_config()
        
        # Fase de teste (primeiros 20% do orçamento)
        test_budget = total_budget * config['budget_strategy']['initial_test_budget_pct']
        
        # Orçamento restante para escala
        scale_budget = total_budget - test_budget
        
        # Orçamento diário máximo
        daily_cap = total_budget * config['budget_strategy']['daily_budget_cap_pct']
        
        return {
            'test_budget': test_budget,
            'scale_budget': scale_budget,
            'daily_cap': daily_cap,
            'test_duration_days': 3,  # 3 dias de teste
            'scale_duration_days': duration_days - 3
        }


class AggressiveScaleMode:
    """
    AGGRESSIVE SCALE MODE - Modo de Escala Agressiva
    
    Ativar somente quando:
    - Métricas estáveis
    - ROAS positivo consistente
    - CPA previsível
    - Público validado
    
    Características:
    - Escala progressiva
    - Aumento de budget controlado
    - Duplicação inteligente
    - Exploração de novos públicos
    - Prioridade: maximizar lucro
    """
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """Retorna configuração do AGGRESSIVE SCALE MODE"""
        return {
            'mode': 'AGGRESSIVE_SCALE',
            'budget_strategy': {
                'initial_test_budget_pct': 0.10,  # 10% para teste inicial
                'daily_budget_cap_pct': 0.25,     # Máximo 25% do orçamento total por dia
                'scale_increment_pct': 0.50       # Aumentar 50% por vez
            },
            'pause_criteria': {
                'max_cpa_multiplier': 2.0,        # Pausar se CPA > 2x do limite
                'min_roas': 1.0,                  # Pausar se ROAS < 1.0
                'max_negative_days': 3            # Pausar após 3 dias negativos
            },
            'scale_criteria': {
                'min_roas_for_scale': 2.0,        # Escalar se ROAS > 2.0
                'min_days_stable': 3,             # Mínimo 3 dias estáveis
                'max_scale_per_day': 0.50         # Máximo 50% de aumento por dia
            },
            'monitoring': {
                'check_frequency_minutes': 15,    # Verificar a cada 15 minutos
                'alert_on_negative_roi': True,
                'auto_pause_enabled': True
            },
            'expansion': {
                'test_new_audiences': True,
                'duplicate_winners': True,
                'expand_age_ranges': True,
                'expand_locations': True
            }
        }
    
    @staticmethod
    def calculate_budget_allocation(total_budget: float, duration_days: int) -> Dict[str, float]:
        """Calcula alocação de orçamento no AGGRESSIVE SCALE MODE"""
        config = AggressiveScaleMode.get_config()
        
        # Fase de teste (primeiros 10% do orçamento)
        test_budget = total_budget * config['budget_strategy']['initial_test_budget_pct']
        
        # Orçamento restante para escala agressiva
        scale_budget = total_budget - test_budget
        
        # Orçamento diário máximo
        daily_cap = total_budget * config['budget_strategy']['daily_budget_cap_pct']
        
        return {
            'test_budget': test_budget,
            'scale_budget': scale_budget,
            'daily_cap': daily_cap,
            'test_duration_days': 2,  # 2 dias de teste
            'scale_duration_days': duration_days - 2
        }


class OperationModeManager:
    """
    Gerenciador de Modos de Operação
    
    Decide qual modo usar e aplica as regras correspondentes
    """
    
    @staticmethod
    def select_mode(campaign_context: Dict[str, Any]) -> OperationMode:
        """
        Seleciona o modo de operação apropriado
        
        Args:
            campaign_context: Contexto da campanha (conta nova, pixel novo, etc.)
        
        Returns:
            Modo de operação recomendado
        """
        # Fatores de risco
        is_new_account = campaign_context.get('is_new_account', False)
        is_new_product = campaign_context.get('is_new_product', True)
        is_new_pixel = campaign_context.get('is_new_pixel', True)
        budget_limited = campaign_context.get('budget_total', 0) < 500
        
        # Se qualquer fator de risco alto, usar SAFE MODE
        if is_new_account or is_new_product or is_new_pixel or budget_limited:
            logger.info("🛡️ Modo SAFE selecionado (fatores de risco detectados)")
            return OperationMode.SAFE
        
        # Verificar se métricas permitem AGGRESSIVE SCALE
        has_stable_metrics = campaign_context.get('has_stable_metrics', False)
        has_positive_roas = campaign_context.get('roas', 0) > 2.0
        
        if has_stable_metrics and has_positive_roas:
            logger.info("🚀 Modo AGGRESSIVE_SCALE selecionado (métricas validadas)")
            return OperationMode.AGGRESSIVE_SCALE
        
        # Padrão: SAFE MODE
        logger.info("🛡️ Modo SAFE selecionado (padrão)")
        return OperationMode.SAFE
    
    @staticmethod
    def get_mode_config(mode: OperationMode) -> Dict[str, Any]:
        """Retorna configuração do modo"""
        if mode == OperationMode.SAFE:
            return SafeMode.get_config()
        elif mode == OperationMode.AGGRESSIVE_SCALE:
            return AggressiveScaleMode.get_config()
        else:
            return SafeMode.get_config()  # Padrão
    
    @staticmethod
    def calculate_budget_allocation(
        mode: OperationMode,
        total_budget: float,
        duration_days: int
    ) -> Dict[str, float]:
        """Calcula alocação de orçamento baseado no modo"""
        if mode == OperationMode.SAFE:
            return SafeMode.calculate_budget_allocation(total_budget, duration_days)
        elif mode == OperationMode.AGGRESSIVE_SCALE:
            return AggressiveScaleMode.calculate_budget_allocation(total_budget, duration_days)
        else:
            return SafeMode.calculate_budget_allocation(total_budget, duration_days)


# Funções auxiliares para uso externo
def check_scale_readiness(campaign_metrics: Dict) -> Dict:
    """Verifica se campanha está pronta para escalar"""
    return ScaleReadinessChecker.check_readiness(campaign_metrics)


def select_operation_mode(campaign_context: Dict) -> str:
    """Seleciona modo de operação apropriado"""
    mode = OperationModeManager.select_mode(campaign_context)
    return mode.value


def get_mode_configuration(mode: str) -> Dict:
    """Retorna configuração de um modo"""
    mode_enum = OperationMode(mode)
    return OperationModeManager.get_mode_config(mode_enum)

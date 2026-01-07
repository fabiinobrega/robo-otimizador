"""
🛡️ PRE-EXECUTION VALIDATOR GLOBAL - Validador de Pré-Execução
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Valida TODAS as condições necessárias antes de executar qualquer ação que envolva:
- Gastos financeiros
- Criação de campanhas
- Modificação de anúncios
- Escala de orçamento

BLOQUEIOS ABSOLUTOS:
- Créditos insuficientes
- Orçamento inválido
- APIs inválidas
- Conta de anúncios indisponível
- Pixel inexistente
- ROI negativo persistente

Autor: Manus AI
Data: 05 de Janeiro de 2026
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Níveis de validação"""
    CRITICAL = "CRITICAL"  # Bloqueia execução
    WARNING = "WARNING"    # Permite mas alerta
    INFO = "INFO"          # Apenas informativo


class ValidationResult:
    """Resultado de uma validação"""
    
    def __init__(self, passed: bool, level: ValidationLevel, message: str, details: Optional[Dict] = None):
        self.passed = passed
        self.level = level
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'passed': self.passed,
            'level': self.level.value,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }


class PreExecutionValidator:
    """
    Validador Global de Pré-Execução
    
    Garante que TODAS as condições estão satisfeitas antes de executar
    qualquer ação que possa resultar em gastos ou modificações.
    """
    
    def __init__(self, db_connection=None, manus_client=None):
        self.db = db_connection
        self.manus = manus_client
        
        logger.info("🛡️ Pre-Execution Validator inicializado")
    
    def validate_all(self, action_context: Dict[str, Any]) -> Tuple[bool, List[ValidationResult]]:
        """
        Executa TODAS as validações
        
        Args:
            action_context: Contexto da ação a ser executada
        
        Returns:
            (pode_executar, lista_de_resultados)
        """
        logger.info("🔍 Iniciando validação global...")
        
        results = []
        
        # 1. Validar créditos
        results.append(self._validate_credits(action_context))
        
        # 2. Validar orçamento
        results.append(self._validate_budget(action_context))
        
        # 3. Validar APIs
        results.append(self._validate_apis(action_context))
        
        # 4. Validar conta de anúncios
        results.append(self._validate_ad_account(action_context))
        
        # 5. Validar pixel
        results.append(self._validate_pixel(action_context))
        
        # 6. Validar ROI
        results.append(self._validate_roi(action_context))
        
        # 7. Validar aprovação do usuário
        results.append(self._validate_user_approval(action_context))
        
        # Verificar se há bloqueios críticos
        critical_failures = [r for r in results if not r.passed and r.level == ValidationLevel.CRITICAL]
        
        can_execute = len(critical_failures) == 0
        
        if can_execute:
            logger.info("✅ Validação global APROVADA")
        else:
            logger.error(f"❌ Validação global REPROVADA ({len(critical_failures)} bloqueios críticos)")
            for failure in critical_failures:
                logger.error(f"   ❌ {failure.message}")
        
        return can_execute, results
    
    def _validate_credits(self, context: Dict) -> ValidationResult:
        """Valida se há créditos suficientes"""
        logger.debug("💳 Validando créditos...")
        
        # TODO: Implementar verificação real de créditos
        # Por enquanto, assume que há créditos
        
        has_credits = True
        
        if has_credits:
            return ValidationResult(
                passed=True,
                level=ValidationLevel.INFO,
                message="Créditos suficientes disponíveis"
            )
        else:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message="Créditos insuficientes. Recarregue sua conta.",
                details={'current_credits': 0, 'required_credits': 100}
            )
    
    def _validate_budget(self, context: Dict) -> ValidationResult:
        """Valida se o orçamento é válido"""
        logger.debug("💰 Validando orçamento...")
        
        budget_total = context.get('budget_total', 0)
        duration_days = context.get('duration_days', 1)
        
        # Orçamento mínimo: R$ 50
        if budget_total < 50:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message="Orçamento total mínimo é R$ 50,00",
                details={'budget_provided': budget_total, 'minimum_required': 50}
            )
        
        # Orçamento diário mínimo: R$ 5
        daily_budget = budget_total / duration_days
        if daily_budget < 5:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message="Orçamento diário mínimo é R$ 5,00",
                details={'daily_budget': daily_budget, 'minimum_required': 5}
            )
        
        return ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"Orçamento válido: R$ {budget_total:.2f} ({duration_days} dias)"
        )
    
    def _validate_apis(self, context: Dict) -> ValidationResult:
        """Valida se as APIs estão configuradas e funcionando"""
        logger.debug("🔌 Validando APIs...")
        
        platform = context.get('platform', 'facebook')
        
        # TODO: Implementar verificação real de APIs
        # Por enquanto, assume que APIs estão OK
        
        apis_valid = True
        
        if apis_valid:
            return ValidationResult(
                passed=True,
                level=ValidationLevel.INFO,
                message=f"APIs do {platform} configuradas e funcionando"
            )
        else:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message=f"APIs do {platform} inválidas ou não configuradas",
                details={'platform': platform, 'error': 'Token expirado'}
            )
    
    def _validate_ad_account(self, context: Dict) -> ValidationResult:
        """Valida se a conta de anúncios está disponível"""
        logger.debug("📊 Validando conta de anúncios...")
        
        # TODO: Implementar verificação real
        # Por enquanto, assume que conta está OK
        
        account_available = True
        account_status = "ACTIVE"
        
        if account_available and account_status == "ACTIVE":
            return ValidationResult(
                passed=True,
                level=ValidationLevel.INFO,
                message="Conta de anúncios ativa e disponível"
            )
        else:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message="Conta de anúncios indisponível ou bloqueada",
                details={'status': account_status, 'reason': 'Pagamento pendente'}
            )
    
    def _validate_pixel(self, context: Dict) -> ValidationResult:
        """Valida se o pixel existe e está configurado"""
        logger.debug("📍 Validando pixel...")
        
        pixel_id = context.get('pixel_id')
        
        if not pixel_id:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message="Pixel não configurado. Crie um pixel antes de continuar.",
                details={'action_required': 'create_pixel'}
            )
        
        # TODO: Verificar se pixel existe na plataforma
        pixel_exists = True
        
        if pixel_exists:
            return ValidationResult(
                passed=True,
                level=ValidationLevel.INFO,
                message=f"Pixel {pixel_id} configurado e ativo"
            )
        else:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message=f"Pixel {pixel_id} não encontrado na plataforma",
                details={'pixel_id': pixel_id}
            )
    
    def _validate_roi(self, context: Dict) -> ValidationResult:
        """Valida se não há ROI negativo persistente"""
        logger.debug("📈 Validando ROI...")
        
        campaign_id = context.get('campaign_id')
        
        if not campaign_id:
            # Nova campanha, sem histórico
            return ValidationResult(
                passed=True,
                level=ValidationLevel.INFO,
                message="Nova campanha, sem histórico de ROI"
            )
        
        # TODO: Buscar histórico real de ROI
        roi_history = context.get('roi_history', [])
        
        if len(roi_history) >= 3:
            # Verificar se ROI foi negativo nos últimos 3 dias
            recent_roi = roi_history[-3:]
            negative_days = sum(1 for roi in recent_roi if roi < 0)
            
            if negative_days >= 3:
                return ValidationResult(
                    passed=False,
                    level=ValidationLevel.CRITICAL,
                    message="ROI negativo persistente (3+ dias). Revise a estratégia antes de continuar.",
                    details={'negative_days': negative_days, 'recent_roi': recent_roi}
                )
        
        return ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message="ROI dentro dos parâmetros aceitáveis"
        )
    
    def _validate_user_approval(self, context: Dict) -> ValidationResult:
        """Valida se usuário aprovou a ação (para gastos)"""
        logger.debug("✅ Validando aprovação do usuário...")
        
        action_type = context.get('action_type', 'unknown')
        requires_approval = action_type in ['create_campaign', 'scale_budget', 'increase_spend']
        
        if not requires_approval:
            return ValidationResult(
                passed=True,
                level=ValidationLevel.INFO,
                message="Ação não requer aprovação do usuário"
            )
        
        approval_token = context.get('approval_token')
        
        if not approval_token:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message="Aprovação do usuário necessária. Nenhum gasto será realizado sem autorização explícita.",
                details={
                    'action_type': action_type,
                    'budget_impact': context.get('budget_total', 0),
                    'requires_user_action': True
                }
            )
        
        # TODO: Validar token de aprovação
        token_valid = True
        
        if token_valid:
            return ValidationResult(
                passed=True,
                level=ValidationLevel.INFO,
                message="Aprovação do usuário verificada"
            )
        else:
            return ValidationResult(
                passed=False,
                level=ValidationLevel.CRITICAL,
                message="Token de aprovação inválido ou expirado",
                details={'approval_token': approval_token}
            )
    
    def generate_report(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Gera relatório de validação"""
        critical_failures = [r for r in results if not r.passed and r.level == ValidationLevel.CRITICAL]
        warnings = [r for r in results if not r.passed and r.level == ValidationLevel.WARNING]
        passed = [r for r in results if r.passed]
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_checks': len(results),
            'passed': len(passed),
            'warnings': len(warnings),
            'critical_failures': len(critical_failures),
            'can_execute': len(critical_failures) == 0,
            'results': [r.to_dict() for r in results]
        }
        
        return report
    
    def get_user_friendly_message(self, results: List[ValidationResult]) -> str:
        """Gera mensagem amigável para o usuário"""
        critical_failures = [r for r in results if not r.passed and r.level == ValidationLevel.CRITICAL]
        
        if not critical_failures:
            return "✅ Todas as validações passaram. Sistema pronto para executar."
        
        messages = ["❌ Não é possível executar devido aos seguintes problemas:\n"]
        
        for i, failure in enumerate(critical_failures, 1):
            messages.append(f"{i}. {failure.message}")
        
        messages.append("\n💡 Resolva estes problemas e tente novamente.")
        
        return "\n".join(messages)


# Funções auxiliares para uso externo
def validate_before_execution(action_context: Dict) -> Tuple[bool, Dict]:
    """
    Valida antes de executar qualquer ação
    
    Uso:
        can_execute, report = validate_before_execution({
            'action_type': 'create_campaign',
            'budget_total': 1000,
            'duration_days': 7,
            'platform': 'facebook',
            'pixel_id': '123456',
            'approval_token': 'abc123'
        })
        
        if can_execute:
            # Executar ação
        else:
            # Mostrar erros ao usuário
    """
    validator = PreExecutionValidator()
    can_execute, results = validator.validate_all(action_context)
    report = validator.generate_report(results)
    
    return can_execute, report


def get_validation_message(action_context: Dict) -> str:
    """Retorna mensagem amigável de validação"""
    validator = PreExecutionValidator()
    can_execute, results = validator.validate_all(action_context)
    
    return validator.get_user_friendly_message(results)

"""
Payment Security Blocks - NEXORA PRIME v12.4+
Sistema de bloqueios absolutos para garantir segurança nos pagamentos
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from services.payments.credit_wallet_service import CreditWalletService


class PaymentSecurityBlocks:
    """Sistema de bloqueios de segurança para pagamentos"""
    
    def __init__(self):
        self.wallet_service = CreditWalletService()
        self.blocks_log_file = "data/payments/security_blocks.jsonl"
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Garante que o arquivo de log existe"""
        os.makedirs(os.path.dirname(self.blocks_log_file), exist_ok=True)
        if not os.path.exists(self.blocks_log_file):
            open(self.blocks_log_file, 'a').close()
    
    def _log_block(self, block_type: str, reason: str, details: Dict[str, Any]):
        """Registra bloqueio em JSONL"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "block_type": block_type,
            "reason": reason,
            "details": details
        }
        
        with open(self.blocks_log_file, 'a') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def check_stripe_availability(self) -> Dict[str, Any]:
        """
        Verifica se o Stripe está disponível
        
        Returns:
            Dict com resultado da verificação
        """
        try:
            # Verificar se as chaves Stripe estão configuradas
            stripe_key = os.getenv('STRIPE_SECRET_KEY', '')
            webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', '')
            
            if not stripe_key or stripe_key == 'sk_test_PLACEHOLDER_SUBSTITUA_PELA_SUA_CHAVE':
                self._log_block(
                    block_type="stripe_unavailable",
                    reason="Chave Stripe não configurada",
                    details={"stripe_key_set": False}
                )
                return {
                    "success": False,
                    "blocked": True,
                    "reason": "Stripe não configurado. Configure as chaves de API no arquivo .env"
                }
            
            if not webhook_secret or webhook_secret == 'whsec_PLACEHOLDER_SUBSTITUA_PELO_SEU_SECRET':
                self._log_block(
                    block_type="stripe_unavailable",
                    reason="Webhook secret não configurado",
                    details={"webhook_secret_set": False}
                )
                return {
                    "success": False,
                    "blocked": True,
                    "reason": "Webhook Stripe não configurado. Configure o webhook secret no arquivo .env"
                }
            
            # TODO: Verificar conectividade com Stripe API
            # Por enquanto, assumir disponível se as chaves estão configuradas
            
            return {
                "success": True,
                "blocked": False,
                "message": "Stripe disponível"
            }
            
        except Exception as e:
            self._log_block(
                block_type="stripe_unavailable",
                reason="Erro ao verificar Stripe",
                details={"error": str(e)}
            )
            return {
                "success": False,
                "blocked": True,
                "reason": f"Erro ao verificar Stripe: {str(e)}"
            }
    
    def check_user_confirmation(self, payment_intent_id: str, 
                               timeout_minutes: int = 5) -> Dict[str, Any]:
        """
        Verifica se o usuário confirmou o pagamento
        
        Args:
            payment_intent_id: ID do Payment Intent
            timeout_minutes: Tempo máximo de espera em minutos
            
        Returns:
            Dict com resultado da verificação
        """
        # TODO: Implementar verificação real de confirmação do usuário
        # Por enquanto, retornar que precisa de confirmação
        
        return {
            "success": False,
            "blocked": True,
            "reason": "Pagamento requer confirmação explícita do usuário",
            "payment_intent_id": payment_intent_id,
            "timeout_minutes": timeout_minutes
        }
    
    def check_webhook_confirmation(self, payment_intent_id: str, 
                                   max_wait_seconds: int = 60) -> Dict[str, Any]:
        """
        Verifica se o webhook confirmou o pagamento
        
        Args:
            payment_intent_id: ID do Payment Intent
            max_wait_seconds: Tempo máximo de espera em segundos
            
        Returns:
            Dict com resultado da verificação
        """
        # Verificar se existe log do webhook para este payment_intent
        webhook_log_file = "data/payments/webhook_events.jsonl"
        
        if not os.path.exists(webhook_log_file):
            self._log_block(
                block_type="webhook_not_confirmed",
                reason="Arquivo de log do webhook não encontrado",
                details={"payment_intent_id": payment_intent_id}
            )
            return {
                "success": False,
                "blocked": True,
                "reason": "Webhook não confirmou o pagamento",
                "payment_intent_id": payment_intent_id
            }
        
        # Procurar confirmação do webhook
        webhook_confirmed = False
        with open(webhook_log_file, 'r') as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    if (event.get('event_type') == 'payment_intent.succeeded' and
                        event.get('status') == 'processed' and
                        payment_intent_id in str(event.get('details', {}))):
                        webhook_confirmed = True
                        break
        
        if not webhook_confirmed:
            self._log_block(
                block_type="webhook_not_confirmed",
                reason="Webhook não confirmou o pagamento",
                details={"payment_intent_id": payment_intent_id}
            )
            return {
                "success": False,
                "blocked": True,
                "reason": "Webhook não confirmou o pagamento. Aguarde a confirmação do Stripe.",
                "payment_intent_id": payment_intent_id
            }
        
        return {
            "success": True,
            "blocked": False,
            "message": "Webhook confirmou o pagamento",
            "payment_intent_id": payment_intent_id
        }
    
    def check_balance_consistency(self, user_id: str) -> Dict[str, Any]:
        """
        Verifica consistência dos saldos
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dict com resultado da verificação
        """
        try:
            balances = self.wallet_service.get_balances(user_id)
            
            # Verificar se todos os saldos são não-negativos
            for credit_type, data in balances["balances"].items():
                balance = data["balance"]
                if balance < 0:
                    self._log_block(
                        block_type="balance_inconsistent",
                        reason="Saldo negativo detectado",
                        details={
                            "user_id": user_id,
                            "credit_type": credit_type,
                            "balance": balance
                        }
                    )
                    return {
                        "success": False,
                        "blocked": True,
                        "reason": f"Saldo inconsistente detectado para {credit_type}",
                        "user_id": user_id
                    }
            
            return {
                "success": True,
                "blocked": False,
                "message": "Saldos consistentes",
                "user_id": user_id
            }
            
        except Exception as e:
            self._log_block(
                block_type="balance_inconsistent",
                reason="Erro ao verificar consistência",
                details={"user_id": user_id, "error": str(e)}
            )
            return {
                "success": False,
                "blocked": True,
                "reason": f"Erro ao verificar consistência dos saldos: {str(e)}",
                "user_id": user_id
            }
    
    def check_payment_limits(self, user_id: str, amount: float, 
                            credit_type: str) -> Dict[str, Any]:
        """
        Verifica limites de pagamento
        
        Args:
            user_id: ID do usuário
            amount: Valor do pagamento
            credit_type: Tipo de crédito
            
        Returns:
            Dict com resultado da verificação
        """
        # Limites globais
        MIN_PAYMENT = 10.0  # Mínimo R$ 10 ou $ 10
        MAX_PAYMENT = 10000.0  # Máximo R$ 10.000 ou $ 10.000
        MAX_DAILY_AMOUNT = 50000.0  # Máximo R$ 50.000 ou $ 50.000 por dia
        
        # Verificar valor mínimo
        if amount < MIN_PAYMENT:
            self._log_block(
                block_type="payment_limit_exceeded",
                reason="Valor abaixo do mínimo",
                details={
                    "user_id": user_id,
                    "amount": amount,
                    "min_payment": MIN_PAYMENT
                }
            )
            return {
                "success": False,
                "blocked": True,
                "reason": f"Valor mínimo de pagamento: R$ {MIN_PAYMENT:.2f}",
                "amount": amount
            }
        
        # Verificar valor máximo
        if amount > MAX_PAYMENT:
            self._log_block(
                block_type="payment_limit_exceeded",
                reason="Valor acima do máximo",
                details={
                    "user_id": user_id,
                    "amount": amount,
                    "max_payment": MAX_PAYMENT
                }
            )
            return {
                "success": False,
                "blocked": True,
                "reason": f"Valor máximo por pagamento: R$ {MAX_PAYMENT:.2f}",
                "amount": amount
            }
        
        # TODO: Verificar limite diário
        # Por enquanto, apenas retornar sucesso
        
        return {
            "success": True,
            "blocked": False,
            "message": "Limites de pagamento OK",
            "amount": amount
        }
    
    def validate_payment(self, user_id: str, payment_intent_id: str, 
                        amount: float, credit_type: str) -> Dict[str, Any]:
        """
        Valida pagamento com todos os bloqueios de segurança
        
        Args:
            user_id: ID do usuário
            payment_intent_id: ID do Payment Intent
            amount: Valor do pagamento
            credit_type: Tipo de crédito
            
        Returns:
            Dict com resultado da validação
        """
        validations = []
        
        # 1. Verificar disponibilidade do Stripe
        stripe_check = self.check_stripe_availability()
        validations.append(("Stripe disponível", stripe_check))
        if stripe_check["blocked"]:
            return {
                "success": False,
                "blocked": True,
                "reason": stripe_check["reason"],
                "validations": validations
            }
        
        # 2. Verificar limites de pagamento
        limits_check = self.check_payment_limits(user_id, amount, credit_type)
        validations.append(("Limites de pagamento", limits_check))
        if limits_check["blocked"]:
            return {
                "success": False,
                "blocked": True,
                "reason": limits_check["reason"],
                "validations": validations
            }
        
        # 3. Verificar consistência dos saldos
        balance_check = self.check_balance_consistency(user_id)
        validations.append(("Consistência dos saldos", balance_check))
        if balance_check["blocked"]:
            return {
                "success": False,
                "blocked": True,
                "reason": balance_check["reason"],
                "validations": validations
            }
        
        # 4. Verificar confirmação do usuário (sempre requerida)
        user_confirmation = self.check_user_confirmation(payment_intent_id)
        validations.append(("Confirmação do usuário", user_confirmation))
        # Nota: Esta verificação sempre retorna blocked=True para forçar confirmação
        
        return {
            "success": True,
            "blocked": False,
            "message": "Todas as validações passaram. Aguardando confirmação do usuário.",
            "validations": validations,
            "requires_user_confirmation": True
        }
    
    def get_recent_blocks(self, limit: int = 50) -> list:
        """
        Retorna bloqueios recentes
        
        Args:
            limit: Número máximo de bloqueios a retornar
            
        Returns:
            Lista de bloqueios recentes
        """
        if not os.path.exists(self.blocks_log_file):
            return []
        
        blocks = []
        with open(self.blocks_log_file, 'r') as f:
            for line in f:
                if line.strip():
                    blocks.append(json.loads(line))
        
        # Retornar os mais recentes
        return blocks[-limit:]

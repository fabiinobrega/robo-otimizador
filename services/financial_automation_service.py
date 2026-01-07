"""
💰 FINANCIAL AUTOMATION SERVICE - Automação Financeira com Stripe
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gerencia automação financeira inteligente:
- Compra automática de créditos (com aprovação)
- Recarga de Facebook Ads (com aprovação)
- Recarga de Google Ads (com aprovação)
- Decisões financeiras baseadas em performance

REGRA ABSOLUTA: Nenhuma transação sem aprovação explícita do usuário.

Autor: Manus AI
Data: 05 de Janeiro de 2026
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import stripe

logger = logging.getLogger(__name__)

# Configurar Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '')


class TransactionType(Enum):
    """Tipos de transação"""
    BUY_CREDITS = "BUY_CREDITS"
    RELOAD_FACEBOOK_ADS = "RELOAD_FACEBOOK_ADS"
    RELOAD_GOOGLE_ADS = "RELOAD_GOOGLE_ADS"
    REFUND = "REFUND"


class TransactionStatus(Enum):
    """Status de transação"""
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class FinancialAutomationService:
    """
    Serviço de Automação Financeira
    
    Gerencia todas as transações financeiras do sistema de forma
    inteligente, auditável e segura.
    """
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        
        logger.info("💰 Financial Automation Service inicializado")
    
    def request_credit_purchase(
        self,
        user_id: int,
        amount: float,
        reason: str,
        auto_approved: bool = False
    ) -> Dict[str, Any]:
        """
        Solicita compra de créditos
        
        Args:
            user_id: ID do usuário
            amount: Valor em R$
            reason: Motivo da compra
            auto_approved: Se True, usuário pré-autorizou compras automáticas
        
        Returns:
            Resultado da solicitação
        """
        logger.info(f"💳 Solicitando compra de créditos: R$ {amount:.2f}")
        logger.info(f"   Motivo: {reason}")
        
        # Criar registro de transação
        transaction = self._create_transaction(
            user_id=user_id,
            transaction_type=TransactionType.BUY_CREDITS,
            amount=amount,
            reason=reason,
            status=TransactionStatus.APPROVED if auto_approved else TransactionStatus.PENDING_APPROVAL
        )
        
        if auto_approved:
            logger.info("✅ Compra pré-aprovada pelo usuário")
            return self._process_credit_purchase(transaction)
        else:
            logger.info("⏳ Aguardando aprovação do usuário")
            return {
                'success': True,
                'transaction_id': transaction['id'],
                'status': 'PENDING_APPROVAL',
                'message': 'Compra de créditos aguardando aprovação do usuário',
                'approval_url': f'/approve-transaction/{transaction["id"]}'
            }
    
    def request_ads_reload(
        self,
        user_id: int,
        platform: str,
        amount: float,
        campaign_id: int,
        reason: str,
        auto_approved: bool = False
    ) -> Dict[str, Any]:
        """
        Solicita recarga de plataforma de anúncios
        
        Args:
            user_id: ID do usuário
            platform: 'facebook' ou 'google'
            amount: Valor em R$
            campaign_id: ID da campanha
            reason: Motivo da recarga
            auto_approved: Se True, usuário pré-autorizou recargas automáticas
        
        Returns:
            Resultado da solicitação
        """
        logger.info(f"📢 Solicitando recarga de {platform.upper()}: R$ {amount:.2f}")
        logger.info(f"   Campanha: #{campaign_id}")
        logger.info(f"   Motivo: {reason}")
        
        transaction_type = (
            TransactionType.RELOAD_FACEBOOK_ADS if platform == 'facebook' 
            else TransactionType.RELOAD_GOOGLE_ADS
        )
        
        # Criar registro de transação
        transaction = self._create_transaction(
            user_id=user_id,
            transaction_type=transaction_type,
            amount=amount,
            reason=reason,
            metadata={'campaign_id': campaign_id, 'platform': platform},
            status=TransactionStatus.APPROVED if auto_approved else TransactionStatus.PENDING_APPROVAL
        )
        
        if auto_approved:
            logger.info("✅ Recarga pré-aprovada pelo usuário")
            return self._process_ads_reload(transaction)
        else:
            logger.info("⏳ Aguardando aprovação do usuário")
            return {
                'success': True,
                'transaction_id': transaction['id'],
                'status': 'PENDING_APPROVAL',
                'message': f'Recarga de {platform.upper()} aguardando aprovação do usuário',
                'approval_url': f'/approve-transaction/{transaction["id"]}'
            }
    
    def approve_transaction(self, transaction_id: int, user_id: int) -> Dict[str, Any]:
        """
        Aprova uma transação pendente
        
        Args:
            transaction_id: ID da transação
            user_id: ID do usuário aprovando
        
        Returns:
            Resultado da aprovação
        """
        logger.info(f"✅ Aprovando transação #{transaction_id}")
        
        # Buscar transação
        transaction = self._get_transaction(transaction_id)
        
        if not transaction:
            return {
                'success': False,
                'error': 'Transação não encontrada'
            }
        
        if transaction['user_id'] != user_id:
            return {
                'success': False,
                'error': 'Usuário não autorizado'
            }
        
        if transaction['status'] != TransactionStatus.PENDING_APPROVAL.value:
            return {
                'success': False,
                'error': f'Transação não está pendente (status: {transaction["status"]})'
            }
        
        # Atualizar status
        self._update_transaction_status(transaction_id, TransactionStatus.APPROVED)
        
        # Processar transação
        transaction_type = TransactionType(transaction['transaction_type'])
        
        if transaction_type == TransactionType.BUY_CREDITS:
            return self._process_credit_purchase(transaction)
        elif transaction_type in [TransactionType.RELOAD_FACEBOOK_ADS, TransactionType.RELOAD_GOOGLE_ADS]:
            return self._process_ads_reload(transaction)
        else:
            return {
                'success': False,
                'error': f'Tipo de transação não suportado: {transaction_type}'
            }
    
    def cancel_transaction(self, transaction_id: int, user_id: int) -> Dict[str, Any]:
        """
        Cancela uma transação pendente
        
        Args:
            transaction_id: ID da transação
            user_id: ID do usuário cancelando
        
        Returns:
            Resultado do cancelamento
        """
        logger.info(f"❌ Cancelando transação #{transaction_id}")
        
        transaction = self._get_transaction(transaction_id)
        
        if not transaction:
            return {
                'success': False,
                'error': 'Transação não encontrada'
            }
        
        if transaction['user_id'] != user_id:
            return {
                'success': False,
                'error': 'Usuário não autorizado'
            }
        
        self._update_transaction_status(transaction_id, TransactionStatus.CANCELLED)
        
        return {
            'success': True,
            'message': 'Transação cancelada com sucesso'
        }
    
    def check_auto_reload_needed(self, campaign_id: int) -> Optional[Dict[str, Any]]:
        """
        Verifica se campanha precisa de recarga automática
        
        Args:
            campaign_id: ID da campanha
        
        Returns:
            Recomendação de recarga ou None
        """
        # TODO: Implementar lógica real baseada em métricas
        
        # Critérios para recarga automática:
        # 1. ROAS > 2.5 (consistente)
        # 2. Budget restante < 20%
        # 3. Campanha ativa
        # 4. Sem erros críticos
        
        return None  # Por enquanto, não recomenda recarga automática
    
    def _create_transaction(
        self,
        user_id: int,
        transaction_type: TransactionType,
        amount: float,
        reason: str,
        metadata: Optional[Dict] = None,
        status: TransactionStatus = TransactionStatus.PENDING_APPROVAL
    ) -> Dict[str, Any]:
        """Cria registro de transação no banco"""
        # TODO: Implementar persistência real
        
        transaction = {
            'id': 1,  # Mock
            'user_id': user_id,
            'transaction_type': transaction_type.value,
            'amount': amount,
            'reason': reason,
            'metadata': metadata or {},
            'status': status.value,
            'created_at': datetime.now().isoformat()
        }
        
        logger.info(f"📝 Transação criada: #{transaction['id']}")
        
        return transaction
    
    def _get_transaction(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """Busca transação no banco"""
        # TODO: Implementar busca real
        return None
    
    def _update_transaction_status(self, transaction_id: int, status: TransactionStatus):
        """Atualiza status da transação"""
        # TODO: Implementar atualização real
        logger.info(f"📝 Transação #{transaction_id} atualizada para {status.value}")
    
    def _process_credit_purchase(self, transaction: Dict) -> Dict[str, Any]:
        """Processa compra de créditos via Stripe"""
        logger.info(f"💳 Processando compra de créditos...")
        
        try:
            # Criar Payment Intent no Stripe
            amount_cents = int(transaction['amount'] * 100)  # Converter para centavos
            
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='brl',
                description=f"Compra de créditos - {transaction['reason']}",
                metadata={
                    'transaction_id': transaction['id'],
                    'user_id': transaction['user_id']
                }
            )
            
            self._update_transaction_status(transaction['id'], TransactionStatus.PROCESSING)
            
            logger.info(f"✅ Payment Intent criado: {payment_intent.id}")
            
            return {
                'success': True,
                'transaction_id': transaction['id'],
                'payment_intent_id': payment_intent.id,
                'client_secret': payment_intent.client_secret,
                'status': 'PROCESSING',
                'message': 'Pagamento em processamento'
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"❌ Erro no Stripe: {e}")
            self._update_transaction_status(transaction['id'], TransactionStatus.FAILED)
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def _process_ads_reload(self, transaction: Dict) -> Dict[str, Any]:
        """Processa recarga de plataforma de anúncios"""
        logger.info(f"📢 Processando recarga de anúncios...")
        
        platform = transaction['metadata'].get('platform')
        campaign_id = transaction['metadata'].get('campaign_id')
        amount = transaction['amount']
        
        try:
            if platform == 'facebook':
                result = self._reload_facebook_ads(campaign_id, amount)
            elif platform == 'google':
                result = self._reload_google_ads(campaign_id, amount)
            else:
                raise ValueError(f"Plataforma não suportada: {platform}")
            
            if result['success']:
                self._update_transaction_status(transaction['id'], TransactionStatus.COMPLETED)
                logger.info(f"✅ Recarga concluída com sucesso")
            else:
                self._update_transaction_status(transaction['id'], TransactionStatus.FAILED)
                logger.error(f"❌ Falha na recarga: {result.get('error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar recarga: {e}", exc_info=True)
            self._update_transaction_status(transaction['id'], TransactionStatus.FAILED)
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def _reload_facebook_ads(self, campaign_id: int, amount: float) -> Dict[str, Any]:
        """Recarrega budget de campanha do Facebook Ads"""
        # TODO: Implementar via Facebook Ads API
        logger.info(f"📘 Recarregando Facebook Ads: R$ {amount:.2f}")
        
        return {
            'success': True,
            'platform': 'facebook',
            'campaign_id': campaign_id,
            'amount_added': amount,
            'message': f'Budget aumentado em R$ {amount:.2f}'
        }
    
    def _reload_google_ads(self, campaign_id: int, amount: float) -> Dict[str, Any]:
        """Recarrega budget de campanha do Google Ads"""
        # TODO: Implementar via Google Ads API
        logger.info(f"🔍 Recarregando Google Ads: R$ {amount:.2f}")
        
        return {
            'success': True,
            'platform': 'google',
            'campaign_id': campaign_id,
            'amount_added': amount,
            'message': f'Budget aumentado em R$ {amount:.2f}'
        }
    
    def get_pending_transactions(self, user_id: int) -> List[Dict[str, Any]]:
        """Retorna transações pendentes de aprovação"""
        # TODO: Implementar busca real
        return []
    
    def get_transaction_history(
        self,
        user_id: int,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Retorna histórico de transações"""
        # TODO: Implementar busca real
        return []


# Funções auxiliares para uso externo
def request_credit_purchase_auto(user_id: int, amount: float, reason: str) -> Dict:
    """Solicita compra de créditos"""
    service = FinancialAutomationService()
    return service.request_credit_purchase(user_id, amount, reason, auto_approved=False)


def request_ads_reload_auto(
    user_id: int,
    platform: str,
    amount: float,
    campaign_id: int,
    reason: str
) -> Dict:
    """Solicita recarga de anúncios"""
    service = FinancialAutomationService()
    return service.request_ads_reload(user_id, platform, amount, campaign_id, reason, auto_approved=False)

"""
Stripe Payment Service - Integração Completa com Stripe
Implementa Payment Intents, Webhooks e Idempotency Keys
"""

import os
import json
import logging
import hashlib
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class StripePaymentService:
    """
    Serviço de pagamentos via Stripe
    Gerencia Payment Intents com segurança e idempotência
    """
    
    def __init__(self):
        """Inicializa serviço Stripe"""
        # Carregar chaves do ambiente
        self.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_PLACEHOLDER')
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_PLACEHOLDER')
        self.mode = os.getenv('STRIPE_MODE', 'test')  # test ou live
        
        # Diretórios
        self.log_dir = Path('logs/payments')
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Importar Stripe (será instalado)
        try:
            import stripe
            self.stripe = stripe
            self.stripe.api_key = self.api_key
            self.stripe_available = True
            logger.info(f"Stripe inicializado em modo: {self.mode}")
        except ImportError:
            self.stripe_available = False
            logger.warning("Stripe não instalado. Execute: pip install stripe")
    
    def create_payment_intent(self, amount, currency, credit_type, user_id, metadata=None):
        """
        Cria Payment Intent com idempotency key
        
        Args:
            amount (float): Valor em reais/dólares
            currency (str): Moeda (BRL ou USD)
            credit_type (str): Tipo de crédito
            user_id (str): ID do usuário
            metadata (dict): Metadados adicionais
            
        Returns:
            dict: Payment Intent criado
        """
        if not self.stripe_available:
            return self._mock_payment_intent(amount, currency, credit_type, user_id)
        
        try:
            # Gerar idempotency key única
            idempotency_key = self._generate_idempotency_key(
                user_id, credit_type, amount, currency
            )
            
            # Converter para centavos
            amount_cents = int(amount * 100)
            
            # Metadados padrão
            payment_metadata = {
                'user_id': user_id,
                'credit_type': credit_type,
                'amount_original': amount,
                'currency': currency,
                'created_at': datetime.now().isoformat()
            }
            
            if metadata:
                payment_metadata.update(metadata)
            
            # Criar Payment Intent
            payment_intent = self.stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency.lower(),
                metadata=payment_metadata,
                idempotency_key=idempotency_key,
                automatic_payment_methods={'enabled': True}
            )
            
            # Registrar log
            self._log_payment_event({
                'timestamp': datetime.now().isoformat(),
                'event_type': 'payment_intent_created',
                'payment_intent_id': payment_intent.id,
                'user_id': user_id,
                'credit_type': credit_type,
                'amount': amount,
                'currency': currency,
                'status': payment_intent.status,
                'client_secret': payment_intent.client_secret
            })
            
            logger.info(f"Payment Intent criado: {payment_intent.id}")
            
            return {
                'success': True,
                'payment_intent_id': payment_intent.id,
                'client_secret': payment_intent.client_secret,
                'amount': amount,
                'currency': currency,
                'status': payment_intent.status
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar Payment Intent: {e}")
            
            self._log_payment_event({
                'timestamp': datetime.now().isoformat(),
                'event_type': 'payment_intent_error',
                'user_id': user_id,
                'credit_type': credit_type,
                'amount': amount,
                'currency': currency,
                'error': str(e)
            })
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def confirm_payment_intent(self, payment_intent_id, payment_method_id=None):
        """
        Confirma Payment Intent
        
        Args:
            payment_intent_id (str): ID do Payment Intent
            payment_method_id (str): ID do método de pagamento
            
        Returns:
            dict: Resultado da confirmação
        """
        if not self.stripe_available:
            return self._mock_confirm_payment(payment_intent_id)
        
        try:
            params = {}
            if payment_method_id:
                params['payment_method'] = payment_method_id
            
            payment_intent = self.stripe.PaymentIntent.confirm(
                payment_intent_id,
                **params
            )
            
            self._log_payment_event({
                'timestamp': datetime.now().isoformat(),
                'event_type': 'payment_intent_confirmed',
                'payment_intent_id': payment_intent.id,
                'status': payment_intent.status
            })
            
            logger.info(f"Payment Intent confirmado: {payment_intent.id}")
            
            return {
                'success': True,
                'payment_intent_id': payment_intent.id,
                'status': payment_intent.status
            }
            
        except Exception as e:
            logger.error(f"Erro ao confirmar Payment Intent: {e}")
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def retrieve_payment_intent(self, payment_intent_id):
        """
        Recupera Payment Intent
        
        Args:
            payment_intent_id (str): ID do Payment Intent
            
        Returns:
            dict: Payment Intent
        """
        if not self.stripe_available:
            return self._mock_retrieve_payment(payment_intent_id)
        
        try:
            payment_intent = self.stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'success': True,
                'payment_intent': {
                    'id': payment_intent.id,
                    'amount': payment_intent.amount / 100,
                    'currency': payment_intent.currency.upper(),
                    'status': payment_intent.status,
                    'metadata': payment_intent.metadata
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao recuperar Payment Intent: {e}")
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_webhook_signature(self, payload, signature):
        """
        Verifica assinatura do webhook
        
        Args:
            payload (str): Payload do webhook
            signature (str): Assinatura do webhook
            
        Returns:
            dict: Evento verificado ou erro
        """
        if not self.stripe_available:
            return {'success': False, 'error': 'Stripe não disponível'}
        
        try:
            event = self.stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            
            logger.info(f"Webhook verificado: {event['type']}")
            
            return {
                'success': True,
                'event': event
            }
            
        except Exception as e:
            logger.error(f"Erro ao verificar webhook: {e}")
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_idempotency_key(self, user_id, credit_type, amount, currency):
        """Gera chave de idempotência única"""
        data = f"{user_id}:{credit_type}:{amount}:{currency}:{datetime.now().date()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _log_payment_event(self, event_data):
        """Registra evento de pagamento"""
        log_file = self.log_dir / 'stripe_events.jsonl'
        with open(log_file, 'a') as f:
            f.write(json.dumps(event_data) + '\n')
    
    def _mock_payment_intent(self, amount, currency, credit_type, user_id):
        """Mock de Payment Intent para testes"""
        mock_id = f"pi_mock_{hashlib.md5(f'{user_id}{credit_type}'.encode()).hexdigest()[:10]}"
        
        return {
            'success': True,
            'payment_intent_id': mock_id,
            'client_secret': f"{mock_id}_secret_mock",
            'amount': amount,
            'currency': currency,
            'status': 'requires_payment_method',
            'mock': True
        }
    
    def _mock_confirm_payment(self, payment_intent_id):
        """Mock de confirmação de pagamento"""
        return {
            'success': True,
            'payment_intent_id': payment_intent_id,
            'status': 'succeeded',
            'mock': True
        }
    
    def _mock_retrieve_payment(self, payment_intent_id):
        """Mock de recuperação de pagamento"""
        return {
            'success': True,
            'payment_intent': {
                'id': payment_intent_id,
                'amount': 100.00,
                'currency': 'BRL',
                'status': 'succeeded',
                'metadata': {'mock': True}
            },
            'mock': True
        }

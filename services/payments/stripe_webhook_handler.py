"""
Stripe Webhook Handler - NEXORA PRIME v12.4+
Processa eventos do Stripe e atualiza carteiras de crédito automaticamente
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from services.payments.credit_wallet_service import CreditWalletService
from models.payments.credit_wallet import CreditType


class StripeWebhookHandler:
    """Manipulador de eventos do Stripe Webhook"""
    
    def __init__(self):
        self.wallet_service = CreditWalletService()
        self.webhook_log_file = "data/payments/webhook_events.jsonl"
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Garante que o arquivo de log existe"""
        os.makedirs(os.path.dirname(self.webhook_log_file), exist_ok=True)
        if not os.path.exists(self.webhook_log_file):
            open(self.webhook_log_file, 'a').close()
    
    def _log_webhook_event(self, event_type: str, event_id: str, 
                          status: str, details: Dict[str, Any]):
        """Registra evento do webhook em JSONL"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "event_id": event_id,
            "status": status,
            "details": details
        }
        
        with open(self.webhook_log_file, 'a') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa evento do webhook do Stripe
        
        Args:
            event: Evento completo do Stripe
            
        Returns:
            Dict com resultado do processamento
        """
        event_type = event.get('type')
        event_id = event.get('id')
        
        # Log do evento recebido
        self._log_webhook_event(
            event_type=event_type,
            event_id=event_id,
            status="received",
            details={"data": event.get('data', {})}
        )
        
        # Roteamento de eventos
        if event_type == 'payment_intent.succeeded':
            return self._handle_payment_succeeded(event)
        elif event_type == 'payment_intent.payment_failed':
            return self._handle_payment_failed(event)
        elif event_type == 'charge.refunded':
            return self._handle_charge_refunded(event)
        else:
            return {
                "success": True,
                "message": f"Evento {event_type} recebido mas não processado",
                "event_id": event_id
            }
    
    def _handle_payment_succeeded(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa pagamento bem-sucedido
        Adiciona créditos à carteira do usuário
        """
        event_id = event.get('id')
        payment_intent = event['data']['object']
        
        # Extrair metadados
        metadata = payment_intent.get('metadata', {})
        user_id = metadata.get('user_id')
        credit_type_str = metadata.get('credit_type')
        amount = payment_intent.get('amount', 0) / 100  # Converter de centavos
        currency = payment_intent.get('currency', 'brl').upper()
        payment_intent_id = payment_intent.get('id')
        
        if not user_id or not credit_type_str:
            error_msg = "Metadados incompletos no payment_intent"
            self._log_webhook_event(
                event_type='payment_intent.succeeded',
                event_id=event_id,
                status="error",
                details={"error": error_msg, "metadata": metadata}
            )
            return {
                "success": False,
                "error": error_msg,
                "event_id": event_id
            }
        
        try:
            # Converter string para CreditType
            credit_type = CreditType[credit_type_str]
            
            # Adicionar créditos
            result = self.wallet_service.add_credits(
                user_id=user_id,
                credit_type=credit_type,
                amount=amount,
                transaction_id=payment_intent_id,
                description=f"Pagamento via Stripe - {currency} {amount:.2f}"
            )
            
            if result["success"]:
                self._log_webhook_event(
                    event_type='payment_intent.succeeded',
                    event_id=event_id,
                    status="processed",
                    details={
                        "user_id": user_id,
                        "credit_type": credit_type_str,
                        "amount": amount,
                        "currency": currency,
                        "payment_intent_id": payment_intent_id,
                        "new_balance": result["new_balance"]
                    }
                )
                
                return {
                    "success": True,
                    "message": "Créditos adicionados com sucesso",
                    "event_id": event_id,
                    "user_id": user_id,
                    "credit_type": credit_type_str,
                    "amount": amount,
                    "new_balance": result["new_balance"]
                }
            else:
                raise Exception(result.get("error", "Erro ao adicionar créditos"))
                
        except Exception as e:
            error_msg = str(e)
            self._log_webhook_event(
                event_type='payment_intent.succeeded',
                event_id=event_id,
                status="error",
                details={"error": error_msg, "payment_intent": payment_intent}
            )
            return {
                "success": False,
                "error": error_msg,
                "event_id": event_id
            }
    
    def _handle_payment_failed(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa falha de pagamento
        Registra o erro para análise
        """
        event_id = event.get('id')
        payment_intent = event['data']['object']
        
        metadata = payment_intent.get('metadata', {})
        user_id = metadata.get('user_id')
        credit_type = metadata.get('credit_type')
        amount = payment_intent.get('amount', 0) / 100
        error_message = payment_intent.get('last_payment_error', {}).get('message', 'Erro desconhecido')
        
        self._log_webhook_event(
            event_type='payment_intent.payment_failed',
            event_id=event_id,
            status="failed",
            details={
                "user_id": user_id,
                "credit_type": credit_type,
                "amount": amount,
                "error_message": error_message,
                "payment_intent_id": payment_intent.get('id')
            }
        )
        
        return {
            "success": True,
            "message": "Falha de pagamento registrada",
            "event_id": event_id,
            "user_id": user_id,
            "error": error_message
        }
    
    def _handle_charge_refunded(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa reembolso
        Remove créditos da carteira do usuário
        """
        event_id = event.get('id')
        charge = event['data']['object']
        
        # Extrair metadados
        metadata = charge.get('metadata', {})
        user_id = metadata.get('user_id')
        credit_type_str = metadata.get('credit_type')
        amount_refunded = charge.get('amount_refunded', 0) / 100
        charge_id = charge.get('id')
        
        if not user_id or not credit_type_str:
            error_msg = "Metadados incompletos no charge"
            self._log_webhook_event(
                event_type='charge.refunded',
                event_id=event_id,
                status="error",
                details={"error": error_msg, "metadata": metadata}
            )
            return {
                "success": False,
                "error": error_msg,
                "event_id": event_id
            }
        
        try:
            # Converter string para CreditType
            credit_type = CreditType[credit_type_str]
            
            # Remover créditos (reembolso)
            result = self.wallet_service.deduct_credits(
                user_id=user_id,
                credit_type=credit_type,
                amount=amount_refunded,
                transaction_id=charge_id,
                description=f"Reembolso Stripe - {amount_refunded:.2f}"
            )
            
            if result["success"]:
                self._log_webhook_event(
                    event_type='charge.refunded',
                    event_id=event_id,
                    status="processed",
                    details={
                        "user_id": user_id,
                        "credit_type": credit_type_str,
                        "amount_refunded": amount_refunded,
                        "charge_id": charge_id,
                        "new_balance": result["new_balance"]
                    }
                )
                
                return {
                    "success": True,
                    "message": "Reembolso processado com sucesso",
                    "event_id": event_id,
                    "user_id": user_id,
                    "credit_type": credit_type_str,
                    "amount_refunded": amount_refunded,
                    "new_balance": result["new_balance"]
                }
            else:
                raise Exception(result.get("error", "Erro ao processar reembolso"))
                
        except Exception as e:
            error_msg = str(e)
            self._log_webhook_event(
                event_type='charge.refunded',
                event_id=event_id,
                status="error",
                details={"error": error_msg, "charge": charge}
            )
            return {
                "success": False,
                "error": error_msg,
                "event_id": event_id
            }
    
    def get_recent_events(self, limit: int = 50) -> list:
        """
        Retorna eventos recentes do webhook
        
        Args:
            limit: Número máximo de eventos a retornar
            
        Returns:
            Lista de eventos recentes
        """
        if not os.path.exists(self.webhook_log_file):
            return []
        
        events = []
        with open(self.webhook_log_file, 'r') as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
        
        # Retornar os mais recentes
        return events[-limit:]

"""
Google Ads Funding Service - NEXORA PRIME v12.4+
Serviço intermediário para adicionar saldo em contas Google Ads
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from services.payments.credit_wallet_service import CreditWalletService
from models.payments.credit_wallet import CreditType


class GoogleAdsFundingService:
    """Serviço de funding para Google Ads"""
    
    def __init__(self):
        self.wallet_service = CreditWalletService()
        self.funding_log_file = "data/payments/google_ads_funding.jsonl"
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Garante que o arquivo de log existe"""
        os.makedirs(os.path.dirname(self.funding_log_file), exist_ok=True)
        if not os.path.exists(self.funding_log_file):
            open(self.funding_log_file, 'a').close()
    
    def _log_funding_operation(self, user_id: str, operation: str, 
                               amount: float, status: str, details: Dict[str, Any]):
        """Registra operação de funding em JSONL"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "operation": operation,
            "amount": amount,
            "status": status,
            "details": details
        }
        
        with open(self.funding_log_file, 'a') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def validate_google_account(self, user_id: str, customer_id: str) -> Dict[str, Any]:
        """
        Valida se a conta Google Ads está conectada e ativa
        
        Args:
            user_id: ID do usuário
            customer_id: ID do cliente Google Ads (formato: XXX-XXX-XXXX)
            
        Returns:
            Dict com resultado da validação
        """
        # TODO: Implementar validação real com Google Ads API
        # Por enquanto, retorna mock para desenvolvimento
        
        # Validar formato do customer_id
        if not customer_id or len(customer_id) < 10:
            return {
                "success": False,
                "error": "Customer ID inválido. Formato esperado: XXX-XXX-XXXX"
            }
        
        # Simular validação
        is_valid = True  # Em produção, verificar via Google Ads API
        
        if is_valid:
            return {
                "success": True,
                "customer_id": customer_id,
                "account_name": f"Conta Google Ads - {customer_id}",
                "status": "ENABLED",
                "currency": "BRL"
            }
        else:
            return {
                "success": False,
                "error": "Conta Google Ads não encontrada ou inativa"
            }
    
    def check_funding_limits(self, user_id: str, amount: float) -> Dict[str, Any]:
        """
        Verifica limites de funding
        
        Args:
            user_id: ID do usuário
            amount: Valor a ser adicionado
            
        Returns:
            Dict com resultado da verificação
        """
        # Obter saldo atual
        balances = self.wallet_service.get_balances(user_id)
        current_balance = balances["balances"]["GOOGLE_ADS"]["balance"]
        
        # Limites de segurança
        MIN_FUNDING = 10.0  # Mínimo R$ 10
        MAX_FUNDING = 10000.0  # Máximo R$ 10.000 por operação
        MAX_BALANCE = 50000.0  # Saldo máximo R$ 50.000
        
        # Validações
        if amount < MIN_FUNDING:
            return {
                "success": False,
                "error": f"Valor mínimo para funding: R$ {MIN_FUNDING:.2f}"
            }
        
        if amount > MAX_FUNDING:
            return {
                "success": False,
                "error": f"Valor máximo por operação: R$ {MAX_FUNDING:.2f}"
            }
        
        if current_balance + amount > MAX_BALANCE:
            return {
                "success": False,
                "error": f"Saldo máximo permitido: R$ {MAX_BALANCE:.2f}. Saldo atual: R$ {current_balance:.2f}"
            }
        
        return {
            "success": True,
            "current_balance": current_balance,
            "amount": amount,
            "new_balance": current_balance + amount
        }
    
    def fund_account(self, user_id: str, customer_id: str, 
                    amount: float, transaction_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Adiciona saldo na conta Google Ads
        
        Args:
            user_id: ID do usuário
            customer_id: ID do cliente Google Ads
            amount: Valor a adicionar
            transaction_id: ID da transação (opcional)
            
        Returns:
            Dict com resultado da operação
        """
        try:
            # 1. Validar conta Google
            account_validation = self.validate_google_account(user_id, customer_id)
            if not account_validation["success"]:
                self._log_funding_operation(
                    user_id=user_id,
                    operation="fund_account",
                    amount=amount,
                    status="failed",
                    details={"error": account_validation["error"], "step": "account_validation"}
                )
                return account_validation
            
            # 2. Verificar limites
            limits_check = self.check_funding_limits(user_id, amount)
            if not limits_check["success"]:
                self._log_funding_operation(
                    user_id=user_id,
                    operation="fund_account",
                    amount=amount,
                    status="failed",
                    details={"error": limits_check["error"], "step": "limits_check"}
                )
                return limits_check
            
            # 3. Verificar saldo na carteira
            balances = self.wallet_service.get_balances(user_id)
            wallet_balance = balances["balances"]["GOOGLE_ADS"]["balance"]
            
            if wallet_balance < amount:
                error_msg = f"Saldo insuficiente. Disponível: R$ {wallet_balance:.2f}, Necessário: R$ {amount:.2f}"
                self._log_funding_operation(
                    user_id=user_id,
                    operation="fund_account",
                    amount=amount,
                    status="failed",
                    details={"error": error_msg, "step": "balance_check"}
                )
                return {
                    "success": False,
                    "error": error_msg
                }
            
            # 4. Deduzir da carteira
            deduct_result = self.wallet_service.deduct_credits(
                user_id=user_id,
                credit_type=CreditType.GOOGLE_ADS,
                amount=amount,
                transaction_id=transaction_id or f"google_funding_{datetime.now().timestamp()}",
                description=f"Funding Google Ads - Conta {customer_id}"
            )
            
            if not deduct_result["success"]:
                self._log_funding_operation(
                    user_id=user_id,
                    operation="fund_account",
                    amount=amount,
                    status="failed",
                    details={"error": deduct_result["error"], "step": "deduct_credits"}
                )
                return deduct_result
            
            # 5. TODO: Adicionar saldo na conta Google via API
            # Por enquanto, simular sucesso
            google_funding_success = True
            
            if google_funding_success:
                self._log_funding_operation(
                    user_id=user_id,
                    operation="fund_account",
                    amount=amount,
                    status="success",
                    details={
                        "customer_id": customer_id,
                        "transaction_id": transaction_id,
                        "new_wallet_balance": deduct_result["new_balance"]
                    }
                )
                
                return {
                    "success": True,
                    "message": "Saldo adicionado com sucesso na conta Google Ads",
                    "customer_id": customer_id,
                    "amount_funded": amount,
                    "wallet_balance": deduct_result["new_balance"],
                    "transaction_id": transaction_id
                }
            else:
                # Se falhar no Google, devolver créditos
                self.wallet_service.add_credits(
                    user_id=user_id,
                    credit_type=CreditType.GOOGLE_ADS,
                    amount=amount,
                    transaction_id=f"refund_{transaction_id}",
                    description="Reembolso - Falha no funding Google"
                )
                
                error_msg = "Falha ao adicionar saldo no Google Ads. Créditos reembolsados."
                self._log_funding_operation(
                    user_id=user_id,
                    operation="fund_account",
                    amount=amount,
                    status="failed",
                    details={"error": error_msg, "step": "google_api"}
                )
                
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            error_msg = str(e)
            self._log_funding_operation(
                user_id=user_id,
                operation="fund_account",
                amount=amount,
                status="error",
                details={"error": error_msg, "step": "exception"}
            )
            return {
                "success": False,
                "error": f"Erro ao processar funding: {error_msg}"
            }
    
    def get_funding_history(self, user_id: str, limit: int = 50) -> list:
        """
        Retorna histórico de funding do usuário
        
        Args:
            user_id: ID do usuário
            limit: Número máximo de registros
            
        Returns:
            Lista de operações de funding
        """
        if not os.path.exists(self.funding_log_file):
            return []
        
        history = []
        with open(self.funding_log_file, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if entry["user_id"] == user_id:
                        history.append(entry)
        
        # Retornar os mais recentes
        return history[-limit:]

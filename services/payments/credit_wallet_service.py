"""
Credit Wallet Service - Serviço de Gerenciamento de Carteira
Gerencia operações de créditos com persistência e logs
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Importar modelo
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.payments.credit_wallet import CreditWallet, CreditType

logger = logging.getLogger(__name__)


class CreditWalletService:
    """
    Serviço de gerenciamento de carteira de créditos
    Responsável por operações seguras e auditáveis
    """
    
    def __init__(self, storage_dir='data/wallets'):
        """
        Inicializa serviço
        
        Args:
            storage_dir (str): Diretório de armazenamento
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_dir = Path('logs/payments')
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def get_wallet(self, user_id):
        """
        Obtém carteira do usuário
        
        Args:
            user_id (str): ID do usuário
            
        Returns:
            CreditWallet: Carteira do usuário
        """
        wallet_file = self.storage_dir / f"{user_id}.json"
        
        if wallet_file.exists():
            with open(wallet_file, 'r') as f:
                data = json.load(f)
                wallet = CreditWallet(user_id)
                wallet.balances = data['balances']
                return wallet
        else:
            # Criar nova carteira
            wallet = CreditWallet(user_id)
            self._save_wallet(wallet)
            return wallet
    
    def get_balances(self, user_id):
        """
        Obtém todos os saldos do usuário
        
        Args:
            user_id (str): ID do usuário
            
        Returns:
            dict: Todos os saldos
        """
        wallet = self.get_wallet(user_id)
        return wallet.get_all_balances()
    
    def get_balance(self, user_id, credit_type):
        """
        Obtém saldo de um tipo específico
        
        Args:
            user_id (str): ID do usuário
            credit_type (str): Tipo de crédito
            
        Returns:
            dict: Informações do saldo
        """
        wallet = self.get_wallet(user_id)
        return wallet.get_balance(credit_type)
    
    def add_credits(self, user_id, credit_type, amount, transaction_id=None, source='manual'):
        """
        Adiciona créditos com log de auditoria
        
        Args:
            user_id (str): ID do usuário
            credit_type (str): Tipo de crédito
            amount (float): Valor a adicionar
            transaction_id (str): ID da transação (Stripe)
            source (str): Origem da adição
            
        Returns:
            dict: Resultado da operação
        """
        try:
            wallet = self.get_wallet(user_id)
            
            # Adicionar créditos
            new_balance = wallet.add_credits(credit_type, amount)
            
            # Salvar carteira
            self._save_wallet(wallet)
            
            # Registrar log
            self._log_transaction({
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'operation': 'add_credits',
                'credit_type': credit_type,
                'amount': amount,
                'new_balance': new_balance['balance'],
                'transaction_id': transaction_id,
                'source': source,
                'status': 'success'
            })
            
            logger.info(f"Créditos adicionados: {user_id} - {credit_type} - {amount}")
            
            return {
                'success': True,
                'credit_type': credit_type,
                'amount_added': amount,
                'new_balance': new_balance['balance'],
                'currency': new_balance['currency']
            }
            
        except Exception as e:
            logger.error(f"Erro ao adicionar créditos: {e}")
            
            # Registrar erro
            self._log_transaction({
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'operation': 'add_credits',
                'credit_type': credit_type,
                'amount': amount,
                'transaction_id': transaction_id,
                'source': source,
                'status': 'error',
                'error': str(e)
            })
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def deduct_credits(self, user_id, credit_type, amount, reason='usage'):
        """
        Deduz créditos com log de auditoria
        
        Args:
            user_id (str): ID do usuário
            credit_type (str): Tipo de crédito
            amount (float): Valor a deduzir
            reason (str): Motivo da dedução
            
        Returns:
            dict: Resultado da operação
        """
        try:
            wallet = self.get_wallet(user_id)
            
            # Deduzir créditos
            new_balance = wallet.deduct_credits(credit_type, amount)
            
            # Salvar carteira
            self._save_wallet(wallet)
            
            # Registrar log
            self._log_transaction({
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'operation': 'deduct_credits',
                'credit_type': credit_type,
                'amount': amount,
                'new_balance': new_balance['balance'],
                'reason': reason,
                'status': 'success'
            })
            
            logger.info(f"Créditos deduzidos: {user_id} - {credit_type} - {amount}")
            
            return {
                'success': True,
                'credit_type': credit_type,
                'amount_deducted': amount,
                'new_balance': new_balance['balance'],
                'currency': new_balance['currency']
            }
            
        except Exception as e:
            logger.error(f"Erro ao deduzir créditos: {e}")
            
            # Registrar erro
            self._log_transaction({
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'operation': 'deduct_credits',
                'credit_type': credit_type,
                'amount': amount,
                'reason': reason,
                'status': 'error',
                'error': str(e)
            })
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_sufficient_balance(self, user_id, credit_type, amount):
        """
        Verifica se há saldo suficiente
        
        Args:
            user_id (str): ID do usuário
            credit_type (str): Tipo de crédito
            amount (float): Valor necessário
            
        Returns:
            dict: Resultado da verificação
        """
        wallet = self.get_wallet(user_id)
        has_balance = wallet.has_sufficient_balance(credit_type, amount)
        current_balance = wallet.get_balance(credit_type)['balance']
        
        return {
            'sufficient': has_balance,
            'current_balance': current_balance,
            'required_amount': amount,
            'deficit': max(0, amount - current_balance)
        }
    
    def _save_wallet(self, wallet):
        """Salva carteira no disco"""
        wallet_file = self.storage_dir / f"{wallet.user_id}.json"
        with open(wallet_file, 'w') as f:
            json.dump(wallet.to_dict(), f, indent=2)
    
    def _log_transaction(self, transaction_data):
        """Registra transação em log"""
        log_file = self.log_dir / 'wallet_transactions.jsonl'
        with open(log_file, 'a') as f:
            f.write(json.dumps(transaction_data) + '\n')

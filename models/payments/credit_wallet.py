"""
Credit Wallet Model - Modelo Unificado de Créditos
Gerencia saldos de Manus, OpenAI, Facebook Ads e Google Ads
"""

from datetime import datetime
from enum import Enum


class CreditType(Enum):
    """Tipos de crédito disponíveis"""
    MANUS = "MANUS"
    OPENAI = "OPENAI"
    FACEBOOK_ADS = "FACEBOOK_ADS"
    GOOGLE_ADS = "GOOGLE_ADS"


class CreditWallet:
    """
    Carteira de créditos unificada
    Armazena saldos de diferentes tipos de crédito
    """
    
    def __init__(self, user_id):
        """
        Inicializa carteira de créditos
        
        Args:
            user_id (str): ID do usuário
        """
        self.user_id = user_id
        self.balances = {
            CreditType.MANUS.value: {
                'balance': 0.0,
                'currency': 'BRL',
                'updated_at': datetime.now().isoformat()
            },
            CreditType.OPENAI.value: {
                'balance': 0.0,
                'currency': 'USD',
                'updated_at': datetime.now().isoformat()
            },
            CreditType.FACEBOOK_ADS.value: {
                'balance': 0.0,
                'currency': 'BRL',
                'updated_at': datetime.now().isoformat()
            },
            CreditType.GOOGLE_ADS.value: {
                'balance': 0.0,
                'currency': 'BRL',
                'updated_at': datetime.now().isoformat()
            }
        }
    
    def get_balance(self, credit_type):
        """
        Obtém saldo de um tipo de crédito
        
        Args:
            credit_type (str): Tipo de crédito
            
        Returns:
            dict: Informações do saldo
        """
        if credit_type not in self.balances:
            raise ValueError(f"Tipo de crédito inválido: {credit_type}")
        
        return self.balances[credit_type]
    
    def get_all_balances(self):
        """
        Obtém todos os saldos
        
        Returns:
            dict: Todos os saldos
        """
        return {
            'user_id': self.user_id,
            'balances': self.balances,
            'last_updated': max(
                balance['updated_at'] 
                for balance in self.balances.values()
            )
        }
    
    def add_credits(self, credit_type, amount):
        """
        Adiciona créditos
        
        Args:
            credit_type (str): Tipo de crédito
            amount (float): Valor a adicionar
            
        Returns:
            dict: Novo saldo
        """
        if credit_type not in self.balances:
            raise ValueError(f"Tipo de crédito inválido: {credit_type}")
        
        if amount <= 0:
            raise ValueError("Valor deve ser positivo")
        
        self.balances[credit_type]['balance'] += amount
        self.balances[credit_type]['updated_at'] = datetime.now().isoformat()
        
        return self.balances[credit_type]
    
    def deduct_credits(self, credit_type, amount):
        """
        Deduz créditos
        
        Args:
            credit_type (str): Tipo de crédito
            amount (float): Valor a deduzir
            
        Returns:
            dict: Novo saldo
        """
        if credit_type not in self.balances:
            raise ValueError(f"Tipo de crédito inválido: {credit_type}")
        
        if amount <= 0:
            raise ValueError("Valor deve ser positivo")
        
        current_balance = self.balances[credit_type]['balance']
        
        if current_balance < amount:
            raise ValueError(
                f"Saldo insuficiente. Disponível: {current_balance}, "
                f"Necessário: {amount}"
            )
        
        self.balances[credit_type]['balance'] -= amount
        self.balances[credit_type]['updated_at'] = datetime.now().isoformat()
        
        return self.balances[credit_type]
    
    def has_sufficient_balance(self, credit_type, amount):
        """
        Verifica se há saldo suficiente
        
        Args:
            credit_type (str): Tipo de crédito
            amount (float): Valor necessário
            
        Returns:
            bool: True se há saldo suficiente
        """
        if credit_type not in self.balances:
            return False
        
        return self.balances[credit_type]['balance'] >= amount
    
    def to_dict(self):
        """
        Converte para dicionário
        
        Returns:
            dict: Representação em dicionário
        """
        return {
            'user_id': self.user_id,
            'balances': self.balances
        }

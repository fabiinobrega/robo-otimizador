"""
Manus Payment Commands - Interpretação de Comandos de Pagamento
NUNCA executa pagamento direto - SEMPRE exige confirmação humana
"""

import re
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ManusPaymentCommands:
    """
    Interpreta comandos de pagamento via Manus
    REGRA ABSOLUTA: Nunca executar pagamento sem confirmação humana
    """
    
    def __init__(self):
        """Inicializa serviço de comandos"""
        self.log_dir = Path('logs/payments')
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Padrões de comando
        self.patterns = {
            'add_credits_manus': r'adicionar?\s+r?\$?\s*(\d+(?:[.,]\d+)?)\s+(?:em\s+)?(?:créditos?\s+)?manus',
            'add_credits_openai': r'adicionar?\s+(?:r?\$|usd?)\s*(\d+(?:[.,]\d+)?)\s+(?:em\s+)?(?:créditos?\s+)?openai',
            'add_credits_facebook': r'adicionar?\s+r?\$?\s*(\d+(?:[.,]\d+)?)\s+(?:em\s+)?facebook\s*ads?',
            'add_credits_google': r'adicionar?\s+r?\$?\s*(\d+(?:[.,]\d+)?)\s+(?:em\s+)?google\s*ads?',
        }
    
    def interpret_command(self, command_text, user_id):
        """
        Interpreta comando de pagamento
        
        Args:
            command_text (str): Texto do comando
            user_id (str): ID do usuário
            
        Returns:
            dict: Intenção interpretada (NÃO executa pagamento)
        """
        command_lower = command_text.lower().strip()
        
        # Tentar identificar intenção
        for intent, pattern in self.patterns.items():
            match = re.search(pattern, command_lower, re.IGNORECASE)
            
            if match:
                amount_str = match.group(1).replace(',', '.')
                amount = float(amount_str)
                
                # Mapear intenção para tipo de crédito
                credit_type_map = {
                    'add_credits_manus': 'MANUS',
                    'add_credits_openai': 'OPENAI',
                    'add_credits_facebook': 'FACEBOOK_ADS',
                    'add_credits_google': 'GOOGLE_ADS'
                }
                
                credit_type = credit_type_map[intent]
                
                # Determinar moeda
                currency = 'USD' if credit_type == 'OPENAI' else 'BRL'
                
                # Gerar resumo para confirmação
                payment_summary = self._generate_payment_summary(
                    user_id=user_id,
                    credit_type=credit_type,
                    amount=amount,
                    currency=currency,
                    original_command=command_text
                )
                
                # Registrar log de intenção (NÃO de execução)
                self._log_payment_intention({
                    'timestamp': datetime.now().isoformat(),
                    'user_id': user_id,
                    'original_command': command_text,
                    'interpreted_intent': intent,
                    'credit_type': credit_type,
                    'amount': amount,
                    'currency': currency,
                    'status': 'awaiting_confirmation'
                })
                
                logger.info(f"Comando interpretado (aguardando confirmação): {intent}")
                
                return {
                    'success': True,
                    'intent_recognized': True,
                    'credit_type': credit_type,
                    'amount': amount,
                    'currency': currency,
                    'payment_summary': payment_summary,
                    'requires_confirmation': True,
                    'warning': '⚠️ PAGAMENTO NÃO EXECUTADO - Aguardando confirmação humana'
                }
        
        # Comando não reconhecido
        return {
            'success': False,
            'intent_recognized': False,
            'error': 'Comando não reconhecido. Exemplos válidos:\n'
                    '- "Adicionar R$500 em créditos Manus"\n'
                    '- "Adicionar R$300 em Facebook Ads"\n'
                    '- "Adicionar $50 em OpenAI"'
        }
    
    def _generate_payment_summary(self, user_id, credit_type, amount, currency, original_command):
        """
        Gera resumo detalhado para confirmação humana
        
        Returns:
            dict: Resumo do pagamento
        """
        # Nomes amigáveis
        credit_names = {
            'MANUS': 'Créditos Manus',
            'OPENAI': 'Créditos OpenAI',
            'FACEBOOK_ADS': 'Saldo Facebook Ads',
            'GOOGLE_ADS': 'Saldo Google Ads'
        }
        
        # Símbolos de moeda
        currency_symbols = {
            'BRL': 'R$',
            'USD': '$'
        }
        
        summary = {
            'user_id': user_id,
            'credit_type': credit_type,
            'credit_name': credit_names.get(credit_type, credit_type),
            'amount': amount,
            'currency': currency,
            'currency_symbol': currency_symbols.get(currency, currency),
            'formatted_amount': f"{currency_symbols.get(currency, currency)} {amount:.2f}",
            'original_command': original_command,
            'confirmation_required': True,
            'confirmation_message': (
                f"Você está prestes a adicionar {currency_symbols.get(currency, currency)} {amount:.2f} "
                f"em {credit_names.get(credit_type, credit_type)}.\n\n"
                f"⚠️ Esta ação irá cobrar o valor no seu cartão de crédito.\n\n"
                f"Deseja confirmar este pagamento?"
            ),
            'next_steps': [
                '1. Revise os detalhes do pagamento',
                '2. Clique em "CONFIRMAR PAGAMENTO"',
                '3. Insira os dados do cartão de crédito',
                '4. Aguarde a confirmação'
            ]
        }
        
        return summary
    
    def _log_payment_intention(self, intention_data):
        """Registra intenção de pagamento (não execução)"""
        log_file = self.log_dir / 'payment_intentions.jsonl'
        with open(log_file, 'a') as f:
            f.write(json.dumps(intention_data) + '\n')

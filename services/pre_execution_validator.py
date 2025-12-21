"""
Serviço de Validação Pré-Execução
Valida todas as condições necessárias antes de chamar o Manus
"""

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PreExecutionValidator:
    """
    Valida condições obrigatórias antes de executar qualquer ação com Manus
    """
    
    def __init__(self):
        self.validation_log = []
    
    def validate_all(self, product, niche, objective, budget, duration_days, sales_goal):
        """
        Valida TODAS as condições obrigatórias
        
        Args:
            campaign_data (dict): Dados da campanha a ser criada
            
        Returns:
            dict: {
                'valid': bool,
                'errors': list,
                'warnings': list,
                'log': list
            }
        """
        errors = []
        warnings = []
        self.validation_log = []
        
        # 1. Validar créditos OpenAI
        openai_valid = self._validate_openai_credits()
        if not openai_valid['valid']:
            errors.append({
                'type': 'openai_credits',
                'message': 'Sem créditos OpenAI disponíveis',
                'user_message': '❌ Você está sem créditos no OpenAI. Recarregue para gerar estratégias de anúncios.',
                'action': 'block_openai'
            })
        
        # 2. Validar créditos Manus
        manus_valid = self._validate_manus_credits()
        if not manus_valid['valid']:
            errors.append({
                'type': 'manus_credits',
                'message': 'Sem créditos Manus disponíveis',
                'user_message': '❌ Você está sem créditos no Manus. Recarregue para executar tarefas.',
                'action': 'block_manus'
            })
        
        # 3. Validar orçamento total
        budget_valid = self._validate_budget(budget)
        if not budget_valid['valid']:
            errors.append({
                'type': 'budget',
                'message': budget_valid['message'],
                'user_message': f'❌ {budget_valid["user_message"]}',
                'action': 'block_execution'
            })
        
        # 4. Validar duração da campanha
        duration_valid = self._validate_duration(duration_days)
        if not duration_valid['valid']:
            errors.append({
                'type': 'duration',
                'message': duration_valid['message'],
                'user_message': f'❌ {duration_valid["user_message"]}',
                'action': 'block_execution'
            })
        
        # 4.1. Validar orçamento diário (se duração for válida)
        if budget_valid['valid'] and duration_valid['valid']:
            daily_budget = float(budget) / int(duration_days)
            if daily_budget < 20:
                errors.append({
                    'type': 'daily_budget',
                    'message': f'Orçamento diário abaixo do mínimo: R$ {daily_budget:.2f}',
                    'user_message': f'❌ Com este orçamento e duração, o orçamento diário seria R$ {daily_budget:.2f}, mas o mínimo recomendado é R$ 20,00/dia. Aumente o orçamento total ou reduza a duração.',
                    'action': 'block_execution'
                })
        
        # 5. Validar produto
        product_valid = self._validate_product(product)
        if not product_valid['valid']:
            errors.append({
                'type': 'product',
                'message': product_valid['message'],
                'user_message': f'❌ {product_valid["user_message"]}',
                'action': 'block_execution'
            })
        
        # 6. Validar objetivo de venda
        objective_valid = self._validate_sales_objective(objective)
        if not objective_valid['valid']:
            errors.append({
                'type': 'objective',
                'message': objective_valid['message'],
                'user_message': f'❌ {objective_valid["user_message"]}',
                'action': 'block_execution'
            })
        
        # Registrar log
        self._log_validation({
            'timestamp': datetime.now().isoformat(),
            'valid': len(errors) == 0,
            'errors_count': len(errors),
            'warnings_count': len(warnings),
            'errors': errors,
            'warnings': warnings
        })
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'log': self.validation_log
        }
    
    def _validate_openai_credits(self):
        """Valida se há créditos OpenAI disponíveis"""
        try:
            # Verificar se API key existe
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key or api_key == 'your_openai_api_key_here':
                return {
                    'valid': False,
                    'message': 'API key OpenAI não configurada'
                }
            
            # Aqui seria feita uma chamada real para verificar créditos
            # Por enquanto, assumimos que está OK se a key existe
            return {
                'valid': True,
                'message': 'Créditos OpenAI disponíveis'
            }
            
        except Exception as e:
            logger.error(f"Erro ao validar créditos OpenAI: {e}")
            return {
                'valid': False,
                'message': f'Erro ao verificar créditos: {str(e)}'
            }
    
    def _validate_manus_credits(self):
        """Valida se há créditos Manus disponíveis"""
        try:
            # Aqui seria feita uma chamada real para verificar créditos Manus
            # Por enquanto, assumimos que está OK (integrado)
            return {
                'valid': True,
                'message': 'Sistema Manus integrado e disponível'
            }
            
        except Exception as e:
            logger.error(f"Erro ao validar créditos Manus: {e}")
            return {
                'valid': False,
                'message': f'Erro ao verificar créditos: {str(e)}'
            }
    
    def _validate_duration(self, duration_days):
        """Valida se a duração foi definida e é válida"""
        if not duration_days:
            return {
                'valid': False,
                'message': 'Duração não definida',
                'user_message': 'Defina por quantos dias a campanha deve rodar para calcular o orçamento diário'
            }
        
        try:
            duration_value = int(duration_days)
            if duration_value <= 0:
                return {
                    'valid': False,
                    'message': 'Duração deve ser maior que zero',
                    'user_message': 'A duração da campanha deve ser de pelo menos 1 dia'
                }
            
            if duration_value > 365:
                return {
                    'valid': False,
                    'message': 'Duração muito longa',
                    'user_message': 'A duração máxima permitida é 365 dias (1 ano)'
                }
            
            return {
                'valid': True,
                'message': f'Duração válida: {duration_value} dias'
            }
            
        except (ValueError, TypeError):
            return {
                'valid': False,
                'message': 'Duração inválida',
                'user_message': 'A duração informada é inválida'
            }
    
    def _validate_budget(self, budget):
        """Valida se o orçamento foi definido e é válido"""
        if not budget:
            return {
                'valid': False,
                'message': 'Orçamento não definido',
                'user_message': 'Defina um orçamento para continuar'
            }
        
        try:
            budget_value = float(budget)
            if budget_value <= 0:
                return {
                    'valid': False,
                    'message': 'Orçamento deve ser maior que zero',
                    'user_message': 'O orçamento deve ser maior que zero'
                }
            
            if budget_value < 20:
                return {
                    'valid': False,
                    'message': 'Orçamento abaixo do mínimo recomendado',
                    'user_message': 'O orçamento mínimo recomendado é R$ 20,00'
                }
            
            return {
                'valid': True,
                'message': f'Orçamento válido: R$ {budget_value:.2f}'
            }
            
        except (ValueError, TypeError):
            return {
                'valid': False,
                'message': 'Orçamento inválido',
                'user_message': 'O orçamento informado é inválido'
            }
    
    def _validate_product(self, product):
        """Valida se o produto foi definido"""
        if not product or not product.strip():
            return {
                'valid': False,
                'message': 'Produto não definido',
                'user_message': 'Defina o produto ou serviço que será anunciado'
            }
        
        if len(product.strip()) < 3:
            return {
                'valid': False,
                'message': 'Nome do produto muito curto',
                'user_message': 'O nome do produto deve ter pelo menos 3 caracteres'
            }
        
        return {
            'valid': True,
            'message': f'Produto definido: {product}'
        }
    
    def _validate_sales_objective(self, objective):
        """Valida se o objetivo de venda foi definido"""
        if not objective or not objective.strip():
            return {
                'valid': False,
                'message': 'Objetivo de venda não definido',
                'user_message': 'Defina o objetivo de venda (ex: aumentar vendas em 30%)'
            }
        
        if len(objective.strip()) < 5:
            return {
                'valid': False,
                'message': 'Objetivo de venda muito vago',
                'user_message': 'Descreva melhor o objetivo de venda'
            }
        
        return {
            'valid': True,
            'message': f'Objetivo definido: {objective}'
        }
    
    def _log_validation(self, log_entry):
        """Registra log de validação"""
        self.validation_log.append(log_entry)
        
        # Salvar em arquivo JSON para auditoria
        try:
            log_file = 'logs/pre_execution_validation.jsonl'
            os.makedirs('logs', exist_ok=True)
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            logger.error(f"Erro ao salvar log de validação: {e}")

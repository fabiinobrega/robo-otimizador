"""
Helper para Mensagens de Erro Padronizadas
Carrega e formata mensagens humanizadas
"""

import json
import os

class ErrorMessagesHelper:
    """
    Helper para carregar e formatar mensagens de erro padronizadas
    """
    
    def __init__(self):
        self.messages = self._load_messages()
    
    def _load_messages(self):
        """Carrega mensagens do arquivo JSON"""
        try:
            config_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'config',
                'error_messages.json'
            )
            
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Erro ao carregar mensagens: {e}")
            return {}
    
    def get_message(self, category, error_type):
        """
        Obtém mensagem formatada
        
        Args:
            category (str): Categoria do erro (openai_credits, manus_credits, etc)
            error_type (str): Tipo do erro (no_credits, invalid_key, etc)
            
        Returns:
            dict: Mensagem formatada
        """
        try:
            message_data = self.messages.get(category, {}).get(error_type, {})
            
            if not message_data:
                # Mensagem padrão se não encontrar
                return {
                    'title': 'Erro',
                    'message': 'Ocorreu um erro. Tente novamente.',
                    'icon': '❌',
                    'type': 'error',
                    'action': 'Tentar Novamente'
                }
            
            return message_data
            
        except Exception as e:
            print(f"Erro ao obter mensagem: {e}")
            return {
                'title': 'Erro',
                'message': str(e),
                'icon': '❌',
                'type': 'error',
                'action': 'Tentar Novamente'
            }
    
    def format_for_frontend(self, category, error_type, extra_data=None):
        """
        Formata mensagem para exibição no frontend
        
        Args:
            category (str): Categoria do erro
            error_type (str): Tipo do erro
            extra_data (dict): Dados adicionais opcionais
            
        Returns:
            dict: Mensagem formatada para frontend
        """
        message = self.get_message(category, error_type)
        
        result = {
            'status': 'error' if message['type'] == 'error' else 'warning',
            'title': f"{message['icon']} {message['title']}",
            'message': message['message'],
            'action_text': message['action'],
            'type': message['type']
        }
        
        if extra_data:
            result['extra'] = extra_data
        
        return result
    
    def format_for_log(self, category, error_type, context=None):
        """
        Formata mensagem para log JSON
        
        Args:
            category (str): Categoria do erro
            error_type (str): Tipo do erro
            context (dict): Contexto adicional
            
        Returns:
            dict: Mensagem formatada para log
        """
        message = self.get_message(category, error_type)
        
        result = {
            'category': category,
            'error_type': error_type,
            'title': message['title'],
            'message': message['message'],
            'severity': message['type']
        }
        
        if context:
            result['context'] = context
        
        return result


# Instância global
error_messages = ErrorMessagesHelper()


def get_error_message(category, error_type):
    """Atalho para obter mensagem"""
    return error_messages.get_message(category, error_type)


def format_error_for_frontend(category, error_type, extra_data=None):
    """Atalho para formatar para frontend"""
    return error_messages.format_for_frontend(category, error_type, extra_data)


def format_error_for_log(category, error_type, context=None):
    """Atalho para formatar para log"""
    return error_messages.format_for_log(category, error_type, context)

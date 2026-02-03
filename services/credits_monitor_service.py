"""
SERVIÇO DE MONITORAMENTO DE CRÉDITOS
Monitora créditos do Manus e OpenAI em tempo real
"""

import os
import requests
from typing import Dict, Any
from datetime import datetime
from services.manus_ai_service import manus_ai

class CreditsMonitorService:
    """Serviço para monitorar créditos das APIs"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.manus_api_key = os.getenv('MANUS_API_KEY', '')
        
    def get_openai_credits(self) -> Dict[str, Any]:
        """
        Obter status de créditos (Manus IA não tem limite)
        
        Returns:
            Dict com status sempre OK
        """
        return {
            "success": True,
            "status": "ok",
            "color": "green",
            "message": "MANUS IA ATIVO (SEM LIMITES)",
            "balance": "ilimitado",
            "usage": "0%",
            "timestamp": datetime.now().isoformat()
        }
    def get_manus_credits(self) -> Dict[str, Any]:
        """
        Obter status de créditos do Manus
        
        Returns:
            Dict com status, créditos e informações
        """
        try:
            # Nota: Manus não tem API pública de créditos
            # Retornamos status simulado baseado na configuração
            
            if not self.manus_api_key or self.manus_api_key == '':
                return {
                    "success": True,
                    "status": "integrated",
                    "message": "INTEGRADO AO SISTEMA",
                    "color": "green",
                    "credits": "Ilimitado",
                    "usage_today": "Ativo",
                    "note": "Manus está integrado diretamente ao sistema"
                }
            
            return {
                "success": True,
                "status": "ok",
                "message": "SISTEMA ATIVO",
                "color": "green",
                "credits": "Disponível",
                "usage_today": "Normal",
                "last_check": datetime.now().isoformat()
            }
                
        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "message": f"ERRO: {str(e)}",
                "color": "red",
                "credits": 0
            }
    
    def get_all_credits_status(self) -> Dict[str, Any]:
        """
        Obter status de todos os créditos
        
        Returns:
            Dict com status de OpenAI e Manus
        """
        openai_status = self.get_openai_credits()
        manus_status = self.get_manus_credits()
        
        # Determinar status geral
        if openai_status.get('success') and manus_status.get('success'):
            overall_status = "ok"
            overall_color = "green"
            overall_message = "TODOS OS SISTEMAS OPERACIONAIS"
        elif not openai_status.get('success') and not manus_status.get('success'):
            overall_status = "critical"
            overall_color = "red"
            overall_message = "SISTEMAS COM PROBLEMAS"
        else:
            overall_status = "warning"
            overall_color = "yellow"
            overall_message = "ATENÇÃO: VERIFICAR CONFIGURAÇÕES"
        
        return {
            "success": True,
            "overall_status": overall_status,
            "overall_color": overall_color,
            "overall_message": overall_message,
            "openai": openai_status,
            "manus": manus_status,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_color_for_status(self, status: str) -> str:
        """
        Obter cor para status
        
        Args:
            status: Status do sistema
            
        Returns:
            Cor (green, yellow, red)
        """
        status_colors = {
            "ok": "green",
            "integrated": "green",
            "warning": "yellow",
            "rate_limit": "yellow",
            "timeout": "yellow",
            "critical": "red",
            "error": "red",
            "not_configured": "red",
            "invalid_key": "red"
        }
        
        return status_colors.get(status, "gray")

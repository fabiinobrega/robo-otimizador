#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Velyra Alert System - Sistema de Alertas Automáticos
Envia alertas e notificações sobre eventos importantes nas campanhas
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class VelyraAlertSystem:
    """
    Sistema de alertas automáticos para campanhas
    Envia notificações sobre eventos importantes
    """
    
    def __init__(self, db_path: str = "nexora.db"):
        self.db_path = db_path
        
        # Tipos de alertas
        self.alert_types = {
            "critical": {
                "name": "Crítico",
                "emoji": "🚨",
                "priority": 1
            },
            "warning": {
                "name": "Aviso",
                "emoji": "⚠️",
                "priority": 2
            },
            "info": {
                "name": "Informação",
                "emoji": "ℹ️",
                "priority": 3
            },
            "success": {
                "name": "Sucesso",
                "emoji": "✅",
                "priority": 4
            }
        }
    
    def _get_db(self):
        """Retorna conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_alert(self, alert_type: str, title: str, message: str, 
                    campaign_id: Optional[int] = None, data: Optional[Dict] = None):
        """Cria um novo alerta"""
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO alerts (type, title, message, campaign_id, data, created_at, read)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            alert_type,
            title,
            message,
            campaign_id,
            json.dumps(data) if data else None,
            datetime.now().isoformat(),
            False
        ))
        
        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Log do alerta
        emoji = self.alert_types.get(alert_type, {}).get('emoji', '📢')
        print(f"{emoji} ALERTA: {title} - {message}")
        
        return alert_id
    
    def get_unread_alerts(self, limit: int = 50) -> List[Dict]:
        """Retorna alertas não lidos"""
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM alerts 
            WHERE read = 0 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        alerts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return alerts
    
    def mark_as_read(self, alert_id: int):
        """Marca alerta como lido"""
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE alerts 
            SET read = 1 
            WHERE id = ?
        """, (alert_id,))
        
        conn.commit()
        conn.close()
    
    # Alertas específicos
    
    def alert_high_cpa(self, campaign_id: int, cpa: float, threshold: float):
        """Alerta de CPA alto"""
        return self.create_alert(
            "critical",
            "CPA Muito Alto",
            f"Campanha {campaign_id}: CPA de R$ {cpa:.2f} excede o limite de R$ {threshold:.2f}",
            campaign_id,
            {"cpa": cpa, "threshold": threshold}
        )
    
    def alert_low_ctr(self, campaign_id: int, ctr: float, threshold: float):
        """Alerta de CTR baixo"""
        return self.create_alert(
            "warning",
            "CTR Baixo",
            f"Campanha {campaign_id}: CTR de {ctr:.2f}% está abaixo do mínimo de {threshold:.2f}%",
            campaign_id,
            {"ctr": ctr, "threshold": threshold}
        )
    
    def alert_budget_exhaustion(self, campaign_id: int, utilization: float):
        """Alerta de budget acabando"""
        return self.create_alert(
            "critical",
            "Budget Quase Esgotado",
            f"Campanha {campaign_id}: {utilization*100:.1f}% do budget já foi utilizado",
            campaign_id,
            {"utilization": utilization}
        )
    
    def alert_campaign_paused(self, campaign_id: int, reason: str):
        """Alerta de campanha pausada"""
        return self.create_alert(
            "warning",
            "Campanha Pausada",
            f"Campanha {campaign_id} foi pausada automaticamente. Motivo: {reason}",
            campaign_id,
            {"reason": reason}
        )
    
    def alert_optimization_applied(self, campaign_id: int, optimization: str):
        """Alerta de otimização aplicada"""
        return self.create_alert(
            "info",
            "Otimização Aplicada",
            f"Campanha {campaign_id}: {optimization}",
            campaign_id,
            {"optimization": optimization}
        )
    
    def alert_goal_reached(self, campaign_id: int, goal_type: str, value: float):
        """Alerta de meta atingida"""
        return self.create_alert(
            "success",
            "Meta Atingida! 🎉",
            f"Campanha {campaign_id} atingiu a meta de {goal_type}: {value}",
            campaign_id,
            {"goal_type": goal_type, "value": value}
        )
    
    def alert_low_roas(self, campaign_id: int, roas: float, threshold: float):
        """Alerta de ROAS baixo"""
        return self.create_alert(
            "critical",
            "ROAS Muito Baixo",
            f"Campanha {campaign_id}: ROAS de {roas:.2f}x está abaixo do mínimo de {threshold:.2f}x",
            campaign_id,
            {"roas": roas, "threshold": threshold}
        )
    
    def alert_high_frequency(self, campaign_id: int, frequency: float):
        """Alerta de frequência alta"""
        return self.create_alert(
            "warning",
            "Frequência Alta",
            f"Campanha {campaign_id}: Frequência de {frequency:.2f} pode causar fadiga de anúncio",
            campaign_id,
            {"frequency": frequency}
        )
    
    def alert_conversion_spike(self, campaign_id: int, conversions: int, increase: float):
        """Alerta de pico de conversões"""
        return self.create_alert(
            "success",
            "Pico de Conversões! 📈",
            f"Campanha {campaign_id}: {conversions} conversões (aumento de {increase:.1f}%)",
            campaign_id,
            {"conversions": conversions, "increase": increase}
        )


# Instância global do sistema de alertas
alert_system = VelyraAlertSystem()

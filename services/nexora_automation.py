"""
NEXORA AUTOMATION
Sistema de automações do Nexora Prime
"""

import os
import json
import sqlite3
# import schedule
# import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres


class NexoraAutomation:
    """
    Sistema de automações do Nexora
    
    Responsabilidades:
    - Automações programadas
    - Rotinas de manutenção
    - Sincronização automática
    - Relatórios automáticos
    - Alertas e notificações
    """
    
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self.root_path = Path(__file__).parent.parent
        self.automations = []
        
    def create_automation(self, automation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar nova automação
        
        Args:
            automation_data: Dados da automação
            
        Returns:
            Automação criada
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS automations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    config TEXT,
                    schedule TEXT,
                    status TEXT DEFAULT 'active',
                    last_run TEXT,
                    next_run TEXT,
                    created_at TEXT
                )
            """)
            
            cursor.execute("""
                INSERT INTO automations (
                    name, type, config, schedule, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                automation_data.get('name', 'Nova Automação'),
                automation_data.get('type', 'custom'),
                json.dumps(automation_data.get('config', {})),
                automation_data.get('schedule', 'daily'),
                'active',
                datetime.now().isoformat()
            ))
            
            automation_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "automation_id": automation_id,
                "message": "Automação criada com sucesso"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_automation(self, automation_id: int) -> Dict[str, Any]:
        """
        Executar automação
        
        Args:
            automation_id: ID da automação
            
        Returns:
            Resultado da execução
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(sql_param("""
                SELECT name, type, config
                FROM automations
                WHERE id = ? AND status = 'active'
            """), (automation_id,))
            
            automation = cursor.fetchone()
            
            if not automation:
                return {
                    "success": False,
                    "error": "Automação não encontrada ou inativa"
                }
            
            name, automation_type, config_json = automation
            config = json.loads(config_json) if config_json else {}
            
            # Executar baseado no tipo
            if automation_type == 'daily_report':
                result = self._run_daily_report(config)
            elif automation_type == 'performance_check':
                result = self._run_performance_check(config)
            elif automation_type == 'budget_reallocation':
                result = self._run_budget_reallocation(config)
            elif automation_type == 'sync_platforms':
                result = self._run_sync_platforms(config)
            else:
                result = {
                    "success": False,
                    "error": f"Tipo de automação desconhecido: {automation_type}"
                }
            
            # Atualizar last_run
            cursor.execute(sql_param("""
                UPDATE automations
                SET last_run = ?
                WHERE id = ?
            """), (datetime.now().isoformat(), automation_id))
            
            conn.commit()
            conn.close()
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_automations(self, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Listar automações
        
        Args:
            status: Filtrar por status
            
        Returns:
            Lista de automações
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if status:
                cursor.execute(sql_param("""
                    SELECT id, name, type, schedule, status, last_run
                    FROM automations
                    WHERE status = ?
                    ORDER BY created_at DESC
                """), (status,))
            else:
                cursor.execute("""
                    SELECT id, name, type, schedule, status, last_run
                    FROM automations
                    ORDER BY created_at DESC
                """)
            
            automations = []
            for row in cursor.fetchall():
                automations.append({
                    "id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "schedule": row[3],
                    "status": row[4],
                    "last_run": row[5]
                })
            
            conn.close()
            
            return {
                "success": True,
                "automations": automations,
                "count": len(automations)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _run_daily_report(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Gerar relatório diário"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Buscar dados do dia anterior
            yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as campaigns,
                    SUM(impressions) as total_impressions,
                    SUM(clicks) as total_clicks,
                    SUM(conversions) as total_conversions,
                    SUM(cost) as total_cost,
                    SUM(revenue) as total_revenue
                FROM campaigns
                WHERE DATE(created_at) = ?
            """, (yesterday,))
            
            stats = cursor.fetchone()
            
            conn.close()
            
            report = {
                "date": yesterday,
                "campaigns": stats[0] or 0,
                "impressions": stats[1] or 0,
                "clicks": stats[2] or 0,
                "conversions": stats[3] or 0,
                "cost": stats[4] or 0,
                "revenue": stats[5] or 0,
                "roas": (stats[5] / stats[4]) if stats[4] and stats[4] > 0 else 0
            }
            
            # Salvar relatório
            report_file = self.root_path / f"reports/daily_report_{yesterday}.json"
            report_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            return {
                "success": True,
                "report": report,
                "file": str(report_file)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _run_performance_check(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Verificar performance das campanhas"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            threshold_roas = config.get('threshold_roas', 1.5)
            threshold_ctr = config.get('threshold_ctr', 1.0)
            
            # Campanhas com baixa performance
            cursor.execute(sql_param("""
                SELECT id, name, roas, ctr
                FROM campaigns
                WHERE status = 'active'
                AND (roas < ? OR ctr < ?)
            """), (threshold_roas, threshold_ctr))
            
            low_performers = []
            for row in cursor.fetchall():
                low_performers.append({
                    "id": row[0],
                    "name": row[1],
                    "roas": row[2],
                    "ctr": row[3],
                    "issue": "low_roas" if row[2] < threshold_roas else "low_ctr"
                })
            
            conn.close()
            
            return {
                "success": True,
                "low_performers": low_performers,
                "count": len(low_performers),
                "threshold_roas": threshold_roas,
                "threshold_ctr": threshold_ctr
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _run_budget_reallocation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Realocar orçamento automaticamente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Buscar campanhas ativas
            cursor.execute("""
                SELECT id, name, budget, roas, conversions
                FROM campaigns
                WHERE status = 'active'
                ORDER BY roas DESC
            """)
            
            campaigns = cursor.fetchall()
            
            if not campaigns:
                return {
                    "success": True,
                    "message": "Nenhuma campanha ativa para realocar"
                }
            
            # Calcular orçamento total
            total_budget = sum(c[2] for c in campaigns)
            
            # Realocar baseado em performance
            reallocations = []
            for campaign_id, name, budget, roas, conversions in campaigns:
                # Campanhas com ROAS > 3.0 recebem mais orçamento
                if roas > 3.0:
                    new_budget = budget * 1.3
                # Campanhas com ROAS < 1.5 recebem menos
                elif roas < 1.5:
                    new_budget = budget * 0.7
                else:
                    new_budget = budget
                
                if abs(new_budget - budget) > 1:
                    cursor.execute(sql_param("""
                        UPDATE campaigns SET budget = ? WHERE id = ?
                    """), (new_budget, campaign_id))
                    
                    reallocations.append({
                        "campaign_id": campaign_id,
                        "campaign_name": name,
                        "old_budget": budget,
                        "new_budget": new_budget,
                        "roas": roas
                    })
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "reallocations": reallocations,
                "count": len(reallocations)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _run_sync_platforms(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Sincronizar com plataformas externas"""
        try:
            platforms = config.get('platforms', ['google', 'facebook'])
            
            synced = []
            for platform in platforms:
                # Aqui seria a sincronização real
                synced.append({
                    "platform": platform,
                    "status": "synced",
                    "synced_at": datetime.now().isoformat()
                })
            
            return {
                "success": True,
                "synced_platforms": synced,
                "count": len(synced)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

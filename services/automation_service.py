"""
Automation Service
Sistema de automação e regras para campanhas
"""
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any
# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres



class AutomationService:
    """Serviço para gerenciar automações e regras de campanhas"""
    
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
    
    def get_db(self):
        """Conectar ao banco de dados"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar nova regra de automação"""
        db = self.get_db()
        
        try:
            cursor = db.execute("""
                INSERT INTO automation_rules 
                (name, rule_type, conditions, actions, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                rule_data.get('name'),
                rule_data.get('rule_type'),
                rule_data.get('conditions'),
                rule_data.get('actions'),
                rule_data.get('is_active', True),
                datetime.now().isoformat()
            ))
            db.commit()
            
            return {
                'success': True,
                'rule_id': cursor.lastrowid,
                'message': 'Regra criada com sucesso'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao criar regra: {str(e)}'
            }
        finally:
            db.close()
    
    def execute_rules(self) -> Dict[str, Any]:
        """Executar todas as regras ativas"""
        db = self.get_db()
        executed = []
        
        try:
            rules = db.execute("""
                SELECT * FROM automation_rules 
                WHERE is_active = 1
            """).fetchall()
            
            for rule in rules:
                rule_dict = dict(rule)
                result = self._execute_single_rule(rule_dict, db)
                executed.append(result)
            
            db.commit()
        
        except Exception as e:
            print(f"Erro ao executar regras: {e}")
        finally:
            db.close()
        
        return {
            'executed_rules': executed,
            'total': len(executed),
            'timestamp': datetime.now().isoformat()
        }
    
    def _execute_single_rule(self, rule: Dict, db) -> Dict[str, Any]:
        """Executar uma regra específica"""
        rule_type = rule.get('rule_type')
        
        if rule_type == 'auto_pause_low_performance':
            return self._auto_pause_low_performance(db)
        
        elif rule_type == 'auto_increase_budget':
            return self._auto_increase_budget(db)
        
        elif rule_type == 'auto_reactivate':
            return self._auto_reactivate_campaigns(db)
        
        elif rule_type == 'alert_high_spend':
            return self._alert_high_spend(db)
        
        return {'rule_type': rule_type, 'status': 'not_implemented'}
    
    def _auto_pause_low_performance(self, db) -> Dict[str, Any]:
        """Auto-pausar campanhas com baixo desempenho"""
        affected = 0
        
        try:
            # Buscar campanhas ativas com ROAS < 1
            campaigns = db.execute("""
                SELECT c.id, c.name, m.roas, m.spend
                FROM campaigns c
                JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE c.status = 'Active' 
                AND m.roas < 1.0 
                AND m.spend > 50
            """).fetchall()
            
            for campaign in campaigns:
                db.execute(sql_param("")"
                    UPDATE campaigns 
                    SET status = 'Paused', updated_at = ?
                    WHERE id = ?
                """, (datetime.now().isoformat(), campaign['id']))
                
                # Registrar log
                db.execute("""
                    INSERT INTO activity_logs (action, details)
                    VALUES (?, ?)
                """, (
                    '[Automação] Campanha Pausada',
                    f"Campanha '{campaign['name']}' pausada automaticamente por baixo ROAS"
                ))
                
                affected += 1
        
        except Exception as e:
            print(f"Erro ao pausar campanhas: {e}")
        
        return {
            'rule_type': 'auto_pause_low_performance',
            'campaigns_affected': affected,
            'status': 'executed'
        }
    
    def _auto_increase_budget(self, db) -> Dict[str, Any]:
        """Aumentar budget de campanhas performando bem"""
        affected = 0
        
        try:
            # Buscar campanhas com alto ROAS
            campaigns = db.execute("""
                SELECT c.id, c.name, c.budget, m.roas, m.conversions
                FROM campaigns c
                JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE c.status = 'Active' 
                AND m.roas > 3.0 
                AND m.conversions > 10
            """).fetchall()
            
            for campaign in campaigns:
                new_budget = campaign['budget'] * 1.15  # Aumentar 15%
                
                db.execute(sql_param("")"
                    UPDATE campaigns 
                    SET budget = ?, updated_at = ?
                    WHERE id = ?
                """, (new_budget, datetime.now().isoformat(), campaign['id']))
                
                # Registrar log
                db.execute("""
                    INSERT INTO activity_logs (action, details)
                    VALUES (?, ?)
                """, (
                    '[Automação] Budget Aumentado',
                    f"Budget da campanha '{campaign['name']}' aumentado de R$ {campaign['budget']:.2f} para R$ {new_budget:.2f}"
                ))
                
                affected += 1
        
        except Exception as e:
            print(f"Erro ao aumentar budget: {e}")
        
        return {
            'rule_type': 'auto_increase_budget',
            'campaigns_affected': affected,
            'status': 'executed'
        }
    
    def _auto_reactivate_campaigns(self, db) -> Dict[str, Any]:
        """Reativar campanhas que foram pausadas mas melhoraram"""
        affected = 0
        
        try:
            # Buscar campanhas pausadas recentemente
            campaigns = db.execute("""
                SELECT c.id, c.name, m.roas
                FROM campaigns c
                JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE c.status = 'Paused' 
                AND m.roas > 2.0
            """).fetchall()
            
            for campaign in campaigns:
                db.execute(sql_param("")"
                    UPDATE campaigns 
                    SET status = 'Active', updated_at = ?
                    WHERE id = ?
                """, (datetime.now().isoformat(), campaign['id']))
                
                # Registrar log
                db.execute("""
                    INSERT INTO activity_logs (action, details)
                    VALUES (?, ?)
                """, (
                    '[Automação] Campanha Reativada',
                    f"Campanha '{campaign['name']}' reativada automaticamente por melhora no ROAS"
                ))
                
                affected += 1
        
        except Exception as e:
            print(f"Erro ao reativar campanhas: {e}")
        
        return {
            'rule_type': 'auto_reactivate',
            'campaigns_affected': affected,
            'status': 'executed'
        }
    
    def _alert_high_spend(self, db) -> Dict[str, Any]:
        """Alertar sobre gastos altos"""
        alerts = 0
        
        try:
            # Buscar campanhas com gasto > 80% do budget
            campaigns = db.execute("""
                SELECT c.id, c.name, c.budget, m.spend
                FROM campaigns c
                JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE c.status = 'Active' 
                AND m.spend > (c.budget * 0.8)
            """).fetchall()
            
            for campaign in campaigns:
                # Registrar alerta
                db.execute("""
                    INSERT INTO activity_logs (action, details)
                    VALUES (?, ?)
                """, (
                    '[Alerta] Gasto Alto',
                    f"Campanha '{campaign['name']}' já gastou {(campaign['spend']/campaign['budget']*100):.1f}% do budget"
                ))
                
                alerts += 1
        
        except Exception as e:
            print(f"Erro ao gerar alertas: {e}")
        
        return {
            'rule_type': 'alert_high_spend',
            'alerts_generated': alerts,
            'status': 'executed'
        }
    
    def get_available_rule_templates(self) -> List[Dict[str, Any]]:
        """Retornar templates de regras disponíveis"""
        return [
            {
                'id': 'auto_pause_low_performance',
                'name': 'Auto-Pausar Campanhas de Baixo Desempenho',
                'description': 'Pausa automaticamente campanhas com ROAS < 1.0',
                'category': 'performance'
            },
            {
                'id': 'auto_increase_budget',
                'name': 'Aumentar Budget de Campanhas Performando Bem',
                'description': 'Aumenta o budget em 15% para campanhas com ROAS > 3.0',
                'category': 'optimization'
            },
            {
                'id': 'auto_reactivate',
                'name': 'Reativar Campanhas Melhoradas',
                'description': 'Reativa campanhas pausadas que melhoraram o ROAS',
                'category': 'recovery'
            },
            {
                'id': 'alert_high_spend',
                'name': 'Alertar Sobre Gastos Altos',
                'description': 'Gera alertas quando o gasto ultrapassa 80% do budget',
                'category': 'monitoring'
            },
            {
                'id': 'schedule_reports',
                'name': 'Agendar Relatórios Automáticos',
                'description': 'Envia relatórios de performance por email',
                'category': 'reporting'
            }
        ]
    
    def get_rule_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obter histórico de execução de regras"""
        db = self.get_db()
        
        try:
            logs = db.execute(sql_param("")"
                SELECT * FROM activity_logs
                WHERE action LIKE '[Automação]%' OR action LIKE '[Alerta]%'
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,)).fetchall()
            
            return [dict(log) for log in logs]
        
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []
        finally:
            db.close()


# Instância do serviço
automation_service = AutomationService()

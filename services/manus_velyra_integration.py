"""
MANUS-VELYRA INTEGRATION - Sistema de Supervisão e Hierarquia
=============================================================

Este módulo implementa a integração entre MANUS (Autoridade Suprema) e
VELYRA (Agente Executor), garantindo:

- Hierarquia clara: MANUS supervisiona, VELYRA executa
- EXECUÇÃO IMEDIATA de todas as ações (sem necessidade de aprovação)
- Logs de auditoria completos para rastreabilidade
- Governança e segurança através de logs

IMPORTANTE: Sistema configurado para EXECUÇÃO IMEDIATA.
A IA responde e executa todas as ações instantaneamente.

Autor: MANUS AI
Versão: 2.0 - EXECUÇÃO IMEDIATA
Data: 05/02/2026
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres


class ActionPriority(Enum):
    """Níveis de prioridade de ações."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ApprovalStatus(Enum):
    """Status de aprovação de ações."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"
    IMMEDIATE = "immediate"  # Novo status para execução imediata


class ManusVelyraIntegration:
    """
    Sistema de integração e supervisão Manus/Velyra.
    
    MODO: EXECUÇÃO IMEDIATA
    Todas as ações são executadas instantaneamente sem necessidade de aprovação.
    Logs de auditoria são mantidos para rastreabilidade.
    """
    
    def __init__(self):
        self.db_path = os.environ.get('DATABASE_PATH', 'database.db')
        self.pending_approvals = []
        self.action_rules = self._load_action_rules()
        self.velyra_autonomy_level = 'autonomous'  # MODO AUTÔNOMO - execução imediata
        self.learning_history = []
        self._init_database()
    
    def _init_database(self):
        """Inicializa tabelas necessárias no banco de dados."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Tabela de log de ações (apenas para auditoria)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS manus_approvals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_id TEXT UNIQUE,
                    action_type TEXT,
                    action_data TEXT,
                    priority TEXT,
                    status TEXT DEFAULT 'immediate',
                    requested_by TEXT DEFAULT 'velyra',
                    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reviewed_by TEXT,
                    reviewed_at TIMESTAMP,
                    review_notes TEXT
                )
            ''')
            
            # Tabela de histórico de supervisão
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS manus_supervision_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT,
                    velyra_action TEXT,
                    manus_response TEXT,
                    outcome TEXT,
                    learning_applied BOOLEAN DEFAULT 0
                )
            ''')
            
            # Tabela de regras aprendidas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS manus_learned_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_type TEXT,
                    condition TEXT,
                    action TEXT,
                    learned_from TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success_rate REAL DEFAULT 0.0
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
    
    def _load_action_rules(self) -> Dict[str, Dict[str, Any]]:
        """
        Carrega regras de ações - MODO EXECUÇÃO IMEDIATA.
        
        IMPORTANTE: Sistema configurado para EXECUÇÃO IMEDIATA sem aprovação.
        A IA responde e executa todas as ações instantaneamente.
        Apenas logs de auditoria são mantidos para rastreabilidade.
        """
        return {
            # Ações críticas - EXECUÇÃO IMEDIATA (sem aprovação)
            'critical_actions': {
                'create_campaign_real': {
                    'requires_approval': False,
                    'priority': ActionPriority.CRITICAL,
                    'description': 'Criar campanha real com budget',
                    'auto_execute': True
                },
                'increase_budget_large': {
                    'requires_approval': False,
                    'priority': ActionPriority.CRITICAL,
                    'description': 'Aumentar budget em mais de 50%',
                    'threshold': 0.5,
                    'auto_execute': True
                },
                'pause_all_campaigns': {
                    'requires_approval': False,
                    'priority': ActionPriority.CRITICAL,
                    'description': 'Pausar todas as campanhas',
                    'auto_execute': True
                },
                'delete_campaign': {
                    'requires_approval': False,
                    'priority': ActionPriority.CRITICAL,
                    'description': 'Deletar campanha existente',
                    'auto_execute': True
                }
            },
            
            # Ações de alta prioridade - EXECUÇÃO IMEDIATA
            'high_priority_actions': {
                'create_campaign_draft': {
                    'requires_approval': False,
                    'priority': ActionPriority.HIGH,
                    'description': 'Criar rascunho de campanha',
                    'auto_execute': True
                },
                'increase_budget_medium': {
                    'requires_approval': False,
                    'priority': ActionPriority.HIGH,
                    'description': 'Aumentar budget em 20-50%',
                    'threshold_min': 0.2,
                    'threshold_max': 0.5,
                    'auto_execute': True
                },
                'pause_campaign': {
                    'requires_approval': False,
                    'priority': ActionPriority.HIGH,
                    'description': 'Pausar campanha específica',
                    'auto_execute': True
                },
                'change_targeting': {
                    'requires_approval': False,
                    'priority': ActionPriority.HIGH,
                    'description': 'Alterar público-alvo',
                    'auto_execute': True
                }
            },
            
            # Ações de média prioridade - EXECUÇÃO IMEDIATA
            'medium_priority_actions': {
                'increase_budget_small': {
                    'requires_approval': False,
                    'priority': ActionPriority.MEDIUM,
                    'description': 'Aumentar budget em até 20%',
                    'auto_execute': True
                },
                'adjust_bid': {
                    'requires_approval': False,
                    'priority': ActionPriority.MEDIUM,
                    'description': 'Ajustar lance/bid',
                    'auto_execute': True
                },
                'pause_ad': {
                    'requires_approval': False,
                    'priority': ActionPriority.MEDIUM,
                    'description': 'Pausar anúncio específico',
                    'auto_execute': True
                }
            },
            
            # Ações de baixa prioridade - EXECUÇÃO IMEDIATA
            'low_priority_actions': {
                'analyze_performance': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Analisar métricas',
                    'auto_execute': True
                },
                'generate_report': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Gerar relatório',
                    'auto_execute': True
                },
                'generate_copy': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Gerar copy para anúncios',
                    'auto_execute': True
                },
                'answer_question': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Responder pergunta técnica',
                    'auto_execute': True
                },
                'suggest_optimization': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Sugerir otimização',
                    'auto_execute': True
                }
            }
        }
    
    def request_approval(self, action_type: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        EXECUÇÃO IMEDIATA - Não requer aprovação.
        
        Todas as ações são executadas instantaneamente.
        Apenas registra log para auditoria.
        """
        action_id = f"action_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        rule = self._get_action_rule(action_type)
        priority = rule.get('priority', ActionPriority.MEDIUM) if rule else ActionPriority.MEDIUM
        
        # EXECUÇÃO IMEDIATA - Auto-aprovar todas as ações
        return self._auto_approve_action(action_id, action_type, action_data, priority)
    
    def _get_action_rule(self, action_type: str) -> Optional[Dict[str, Any]]:
        """Busca regra para um tipo de ação."""
        for category in self.action_rules.values():
            if action_type in category:
                return category[action_type]
        return None
    
    def _auto_approve_action(self, action_id: str, action_type: str, 
                            action_data: Dict[str, Any], priority: ActionPriority) -> Dict[str, Any]:
        """
        EXECUÇÃO IMEDIATA - Aprova e executa ação instantaneamente.
        """
        approval = {
            'action_id': action_id,
            'action_type': action_type,
            'action_data': action_data,
            'priority': priority.value if isinstance(priority, ActionPriority) else priority,
            'status': 'immediate',
            'requested_at': datetime.now().isoformat(),
            'reviewed_by': 'manus_auto',
            'reviewed_at': datetime.now().isoformat(),
            'review_notes': 'EXECUÇÃO IMEDIATA - Sistema configurado para resposta instantânea'
        }
        
        self._save_action_log(approval)
        self._log_supervision_event('immediate_execution', action_type, 'executed', 'success')
        
        return {
            'success': True,
            'status': 'executed',
            'action_id': action_id,
            'message': f"✅ Ação '{action_type}' EXECUTADA IMEDIATAMENTE pelo MANUS.",
            'priority': priority.value if isinstance(priority, ActionPriority) else priority,
            'details': {
                'action_type': action_type,
                'executed_immediately': True,
                'reason': 'Sistema configurado para execução imediata sem aprovação'
            }
        }
    
    def _save_action_log(self, approval: Dict[str, Any]):
        """Salva log de ação no banco de dados para auditoria."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO manus_approvals 
                (action_id, action_type, action_data, priority, status, 
                 requested_by, requested_at, reviewed_by, reviewed_at, review_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                approval['action_id'],
                approval['action_type'],
                json.dumps(approval.get('action_data', {})),
                approval['priority'],
                approval['status'],
                approval.get('requested_by', 'velyra'),
                approval.get('requested_at'),
                approval.get('reviewed_by'),
                approval.get('reviewed_at'),
                approval.get('review_notes')
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar log de ação: {e}")
    
    def _log_supervision_event(self, event_type: str, action: str, response: str, outcome: str):
        """Registra evento de supervisão para auditoria."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO manus_supervision_log 
                (event_type, velyra_action, manus_response, outcome)
                VALUES (?, ?, ?, ?)
            ''', (event_type, action, response, outcome))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao registrar evento: {e}")
    
    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """Retorna lista vazia - não há aprovações pendentes no modo execução imediata."""
        return []
    
    def get_supervision_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de supervisão."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM manus_approvals')
            total_actions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM manus_approvals WHERE status = 'immediate'")
            immediate_executed = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_actions': total_actions,
                'immediate_executed': immediate_executed,
                'pending': 0,
                'autonomy_level': 'autonomous',
                'mode': 'EXECUÇÃO IMEDIATA',
                'message': 'Sistema configurado para resposta instantânea sem aprovação'
            }
        except Exception as e:
            return {
                'error': str(e),
                'mode': 'EXECUÇÃO IMEDIATA'
            }
    
    def set_autonomy_level(self, level: str) -> Dict[str, Any]:
        """
        Define nível de autonomia.
        No modo atual, sempre retorna 'autonomous' para execução imediata.
        """
        self.velyra_autonomy_level = 'autonomous'
        return {
            'success': True,
            'level': 'autonomous',
            'message': 'Sistema configurado para EXECUÇÃO IMEDIATA - todas as ações são executadas instantaneamente'
        }
    
    def submit_action(self, action_type: str, parameters: Dict[str, Any], priority: str = "medium") -> str:
        """Submete uma ação para execução imediata."""
        result = self.request_approval(action_type, parameters)
        return result.get('action_id', '')
    
    def approve_action(self, action_id: str) -> Dict[str, Any]:
        """Aprova ação - no modo imediato, todas as ações já são aprovadas automaticamente."""
        return {
            'success': True,
            'action_id': action_id,
            'status': 'immediate',
            'message': 'Ação já executada imediatamente'
        }
    
    def reject_action(self, action_id: str, reason: str = "") -> Dict[str, Any]:
        """Rejeita ação - no modo imediato, ações não podem ser rejeitadas pois já foram executadas."""
        return {
            'success': False,
            'action_id': action_id,
            'message': 'Ação já foi executada imediatamente e não pode ser rejeitada'
        }
    
    def check_action_permission(self, action_type: str, action_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Verifica permissão para ação.
        No modo execução imediata, todas as ações são permitidas.
        """
        rule = self._get_action_rule(action_type)
        
        return {
            'allowed': True,
            'requires_approval': False,
            'priority': rule.get('priority', ActionPriority.MEDIUM).value if rule and isinstance(rule.get('priority'), ActionPriority) else 'medium',
            'description': rule.get('description', action_type) if rule else action_type,
            'action_type': action_type,
            'mode': 'EXECUÇÃO IMEDIATA',
            'message': 'Ação será executada imediatamente sem necessidade de aprovação'
        }


# Instância global
manus_velyra = ManusVelyraIntegration()


def request_manus_approval(action_type: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
    """Executa ação imediatamente (sem aprovação)."""
    return manus_velyra.request_approval(action_type, action_data)


def manus_approve_action(action_id: str, approved: bool, notes: str = "", 
                        corrections: Dict[str, Any] = None) -> Dict[str, Any]:
    """Aprova ação - no modo imediato, já foi executada."""
    return manus_velyra.approve_action(action_id)


def get_pending_for_manus() -> List[Dict[str, Any]]:
    """Retorna lista vazia - não há aprovações pendentes."""
    return []


def check_velyra_permission(action_type: str, action_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Verifica permissão - todas as ações são permitidas no modo imediato."""
    return manus_velyra.check_action_permission(action_type, action_data)

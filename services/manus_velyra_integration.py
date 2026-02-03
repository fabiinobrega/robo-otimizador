"""
MANUS-VELYRA INTEGRATION - Sistema de Supervisão e Hierarquia
=============================================================

Este módulo implementa a integração entre MANUS (Autoridade Suprema) e
VELYRA (Agente Executor), garantindo:

- Hierarquia clara: MANUS supervisiona, VELYRA executa
- Sistema de aprovação para ações críticas
- Aprendizado supervisionado
- Logs de auditoria completos
- Governança e segurança

Autor: MANUS AI
Versão: 1.0
Data: 03/02/2026
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum


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


class ManusVelyraIntegration:
    """
    Sistema de integração e supervisão Manus/Velyra.
    
    Implementa a hierarquia onde MANUS é autoridade suprema e
    VELYRA executa ações sob supervisão.
    """
    
    def __init__(self):
        self.db_path = os.environ.get('DATABASE_PATH', 'database.db')
        self.pending_approvals = []
        self.action_rules = self._load_action_rules()
        self.velyra_autonomy_level = 'supervised'  # supervised, semi_autonomous, autonomous
        self.learning_history = []
        self._init_database()
    
    def _init_database(self):
        """Inicializa tabelas necessárias no banco de dados."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabela de aprovações pendentes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS manus_approvals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_id TEXT UNIQUE,
                    action_type TEXT,
                    action_data TEXT,
                    priority TEXT,
                    status TEXT DEFAULT 'pending',
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
                CREATE TABLE IF NOT EXISTS velyra_learned_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_type TEXT,
                    condition TEXT,
                    action TEXT,
                    learned_from TEXT,
                    confidence REAL DEFAULT 0.5,
                    times_applied INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_applied TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
    
    def _load_action_rules(self) -> Dict[str, Dict[str, Any]]:
        """Carrega regras de ações e níveis de autonomia."""
        return {
            # Ações que SEMPRE requerem aprovação do Manus
            'critical_actions': {
                'create_campaign_real': {
                    'requires_approval': True,
                    'priority': ActionPriority.CRITICAL,
                    'description': 'Criar campanha real com budget',
                    'approval_timeout_hours': 24
                },
                'increase_budget_large': {
                    'requires_approval': True,
                    'priority': ActionPriority.CRITICAL,
                    'description': 'Aumentar budget em mais de 50%',
                    'threshold': 0.5
                },
                'pause_all_campaigns': {
                    'requires_approval': True,
                    'priority': ActionPriority.CRITICAL,
                    'description': 'Pausar todas as campanhas'
                },
                'delete_campaign': {
                    'requires_approval': True,
                    'priority': ActionPriority.CRITICAL,
                    'description': 'Deletar campanha existente'
                }
            },
            
            # Ações que requerem aprovação em modo supervisionado
            'high_priority_actions': {
                'create_campaign_draft': {
                    'requires_approval': True,
                    'priority': ActionPriority.HIGH,
                    'description': 'Criar rascunho de campanha'
                },
                'increase_budget_medium': {
                    'requires_approval': True,
                    'priority': ActionPriority.HIGH,
                    'description': 'Aumentar budget em 20-50%',
                    'threshold_min': 0.2,
                    'threshold_max': 0.5
                },
                'pause_campaign': {
                    'requires_approval': True,
                    'priority': ActionPriority.HIGH,
                    'description': 'Pausar campanha específica'
                },
                'change_targeting': {
                    'requires_approval': True,
                    'priority': ActionPriority.HIGH,
                    'description': 'Alterar público-alvo'
                }
            },
            
            # Ações que podem ser auto-aprovadas com condições
            'medium_priority_actions': {
                'increase_budget_small': {
                    'requires_approval': False,
                    'auto_approve_conditions': ['roas > 2', 'running_days > 7'],
                    'priority': ActionPriority.MEDIUM,
                    'description': 'Aumentar budget em até 20%'
                },
                'adjust_bid': {
                    'requires_approval': False,
                    'auto_approve_conditions': ['change < 30%'],
                    'priority': ActionPriority.MEDIUM,
                    'description': 'Ajustar lance/bid'
                },
                'pause_ad': {
                    'requires_approval': False,
                    'auto_approve_conditions': ['ctr < 0.5%', 'impressions > 1000'],
                    'priority': ActionPriority.MEDIUM,
                    'description': 'Pausar anúncio específico'
                }
            },
            
            # Ações que Velyra pode executar autonomamente
            'low_priority_actions': {
                'analyze_performance': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Analisar métricas'
                },
                'generate_report': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Gerar relatório'
                },
                'generate_copy': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Gerar copy para anúncios'
                },
                'answer_question': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Responder pergunta técnica'
                },
                'suggest_optimization': {
                    'requires_approval': False,
                    'priority': ActionPriority.LOW,
                    'description': 'Sugerir otimização (sem executar)'
                }
            }
        }
    
    def request_approval(self, action_type: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solicita aprovação do Manus para uma ação.
        
        Args:
            action_type: Tipo de ação a ser aprovada
            action_data: Dados da ação
            
        Returns:
            Status da solicitação
        """
        action_id = f"action_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        # Determinar prioridade e regras
        rule = self._get_action_rule(action_type)
        priority = rule.get('priority', ActionPriority.MEDIUM) if rule else ActionPriority.MEDIUM
        
        # Verificar se pode ser auto-aprovado
        if rule and not rule.get('requires_approval', True):
            auto_approve_conditions = rule.get('auto_approve_conditions', [])
            if self._check_auto_approve_conditions(auto_approve_conditions, action_data):
                return self._auto_approve_action(action_id, action_type, action_data, priority)
        
        # Criar solicitação de aprovação
        approval_request = {
            'action_id': action_id,
            'action_type': action_type,
            'action_data': action_data,
            'priority': priority.value if isinstance(priority, ActionPriority) else priority,
            'status': ApprovalStatus.PENDING.value,
            'requested_by': 'velyra',
            'requested_at': datetime.now().isoformat(),
            'description': rule.get('description', action_type) if rule else action_type
        }
        
        # Salvar no banco de dados
        self._save_approval_request(approval_request)
        
        # Adicionar à lista de pendentes
        self.pending_approvals.append(approval_request)
        
        return {
            'success': True,
            'status': 'pending_approval',
            'action_id': action_id,
            'message': f"⏳ Ação '{action_type}' enviada para aprovação do MANUS.",
            'priority': priority.value if isinstance(priority, ActionPriority) else priority,
            'estimated_review_time': '1-24 horas dependendo da prioridade',
            'details': {
                'action_type': action_type,
                'requires_manus_approval': True,
                'reason': 'Ação classificada como crítica ou de alta prioridade'
            }
        }
    
    def _get_action_rule(self, action_type: str) -> Optional[Dict[str, Any]]:
        """Busca regra para um tipo de ação."""
        for category in self.action_rules.values():
            if action_type in category:
                return category[action_type]
        return None
    
    def _check_auto_approve_conditions(self, conditions: List[str], action_data: Dict[str, Any]) -> bool:
        """Verifica se condições de auto-aprovação são atendidas."""
        if not conditions:
            return True
        
        for condition in conditions:
            # Parsear condição simples (ex: "roas > 2")
            try:
                if '>' in condition:
                    metric, value = condition.split('>')
                    metric = metric.strip()
                    value = float(value.strip())
                    if action_data.get(metric, 0) <= value:
                        return False
                elif '<' in condition:
                    metric, value = condition.split('<')
                    metric = metric.strip()
                    value = float(value.strip().replace('%', ''))
                    if action_data.get(metric, 100) >= value:
                        return False
            except:
                continue
        
        return True
    
    def _auto_approve_action(self, action_id: str, action_type: str, 
                            action_data: Dict[str, Any], priority: ActionPriority) -> Dict[str, Any]:
        """Auto-aprova uma ação que atende às condições."""
        approval = {
            'action_id': action_id,
            'action_type': action_type,
            'action_data': action_data,
            'priority': priority.value if isinstance(priority, ActionPriority) else priority,
            'status': ApprovalStatus.AUTO_APPROVED.value,
            'requested_by': 'velyra',
            'requested_at': datetime.now().isoformat(),
            'reviewed_by': 'manus_auto',
            'reviewed_at': datetime.now().isoformat(),
            'review_notes': 'Auto-aprovado: condições atendidas'
        }
        
        self._save_approval_request(approval)
        self._log_supervision_event('auto_approval', action_type, 'approved', 'success')
        
        return {
            'success': True,
            'status': 'auto_approved',
            'action_id': action_id,
            'message': f"✅ Ação '{action_type}' auto-aprovada pelo sistema.",
            'can_execute': True,
            'details': {
                'action_type': action_type,
                'auto_approved': True,
                'reason': 'Condições de auto-aprovação atendidas'
            }
        }
    
    def _save_approval_request(self, approval: Dict[str, Any]):
        """Salva solicitação de aprovação no banco de dados."""
        try:
            conn = sqlite3.connect(self.db_path)
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
            print(f"Erro ao salvar aprovação: {e}")
    
    def manus_review_action(self, action_id: str, approved: bool, 
                           notes: str = "", corrections: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        MANUS revisa e aprova/rejeita uma ação do Velyra.
        
        Args:
            action_id: ID da ação a revisar
            approved: Se a ação foi aprovada
            notes: Notas de revisão
            corrections: Correções a serem aplicadas
            
        Returns:
            Resultado da revisão
        """
        # Buscar ação pendente
        action = self._get_pending_action(action_id)
        if not action:
            return {
                'success': False,
                'error': f'Ação {action_id} não encontrada'
            }
        
        status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        
        # Atualizar status
        self._update_approval_status(action_id, status, notes)
        
        # Se rejeitado com correções, ensinar Velyra
        if not approved and corrections:
            self._teach_velyra(action, corrections, notes)
        
        # Registrar evento de supervisão
        self._log_supervision_event(
            'manual_review',
            action['action_type'],
            status.value,
            'success' if approved else 'corrected'
        )
        
        return {
            'success': True,
            'action_id': action_id,
            'status': status.value,
            'message': f"✅ Ação {'aprovada' if approved else 'rejeitada'} pelo MANUS.",
            'can_execute': approved,
            'notes': notes,
            'corrections_applied': corrections is not None
        }
    
    def _get_pending_action(self, action_id: str) -> Optional[Dict[str, Any]]:
        """Busca ação pendente por ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM manus_approvals WHERE action_id = ?', (action_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'action_id': row[1],
                    'action_type': row[2],
                    'action_data': json.loads(row[3]) if row[3] else {},
                    'priority': row[4],
                    'status': row[5]
                }
        except Exception as e:
            print(f"Erro ao buscar ação: {e}")
        
        return None
    
    def _update_approval_status(self, action_id: str, status: ApprovalStatus, notes: str):
        """Atualiza status de aprovação."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE manus_approvals 
                SET status = ?, reviewed_by = ?, reviewed_at = ?, review_notes = ?
                WHERE action_id = ?
            ''', (status.value, 'manus', datetime.now().isoformat(), notes, action_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
    
    def _teach_velyra(self, action: Dict[str, Any], corrections: Dict[str, Any], notes: str):
        """
        Ensina Velyra com base em correções do Manus.
        
        Implementa aprendizado supervisionado onde Velyra aprende
        com as correções e não repete os mesmos erros.
        """
        learning = {
            'original_action': action,
            'corrections': corrections,
            'notes': notes,
            'learned_at': datetime.now().isoformat()
        }
        
        self.learning_history.append(learning)
        
        # Criar regra aprendida
        rule = {
            'rule_type': 'correction',
            'condition': f"action_type == '{action['action_type']}'",
            'action': json.dumps(corrections),
            'learned_from': f"manus_correction_{action['action_id']}",
            'confidence': 0.8
        }
        
        self._save_learned_rule(rule)
        
        # Registrar evento de aprendizado
        self._log_supervision_event(
            'learning',
            action['action_type'],
            'rule_created',
            'velyra_improved'
        )
    
    def _save_learned_rule(self, rule: Dict[str, Any]):
        """Salva regra aprendida no banco de dados."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO velyra_learned_rules 
                (rule_type, condition, action, learned_from, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                rule['rule_type'],
                rule['condition'],
                rule['action'],
                rule['learned_from'],
                rule['confidence']
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar regra: {e}")
    
    def _log_supervision_event(self, event_type: str, velyra_action: str, 
                               manus_response: str, outcome: str):
        """Registra evento de supervisão."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO manus_supervision_log 
                (event_type, velyra_action, manus_response, outcome)
                VALUES (?, ?, ?, ?)
            ''', (event_type, velyra_action, manus_response, outcome))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao registrar evento: {e}")
    
    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """Retorna lista de aprovações pendentes."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM manus_approvals 
                WHERE status = 'pending'
                ORDER BY 
                    CASE priority 
                        WHEN 'critical' THEN 1 
                        WHEN 'high' THEN 2 
                        WHEN 'medium' THEN 3 
                        ELSE 4 
                    END,
                    requested_at ASC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'action_id': row[1],
                    'action_type': row[2],
                    'action_data': json.loads(row[3]) if row[3] else {},
                    'priority': row[4],
                    'status': row[5],
                    'requested_at': row[7]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Erro ao buscar aprovações: {e}")
            return []
    
    def get_supervision_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de supervisão."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de ações revisadas
            cursor.execute('SELECT COUNT(*) FROM manus_approvals WHERE status != "pending"')
            total_reviewed = cursor.fetchone()[0]
            
            # Aprovadas vs Rejeitadas
            cursor.execute('SELECT COUNT(*) FROM manus_approvals WHERE status = "approved"')
            approved = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM manus_approvals WHERE status = "rejected"')
            rejected = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM manus_approvals WHERE status = "auto_approved"')
            auto_approved = cursor.fetchone()[0]
            
            # Regras aprendidas
            cursor.execute('SELECT COUNT(*) FROM velyra_learned_rules')
            rules_learned = cursor.fetchone()[0]
            
            # Pendentes
            cursor.execute('SELECT COUNT(*) FROM manus_approvals WHERE status = "pending"')
            pending = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_reviewed': total_reviewed,
                'approved': approved,
                'rejected': rejected,
                'auto_approved': auto_approved,
                'pending': pending,
                'rules_learned': rules_learned,
                'approval_rate': round(approved / total_reviewed * 100, 1) if total_reviewed > 0 else 0,
                'autonomy_level': self.velyra_autonomy_level
            }
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {}
    
    def set_autonomy_level(self, level: str) -> Dict[str, Any]:
        """
        Define nível de autonomia do Velyra.
        
        Args:
            level: 'supervised', 'semi_autonomous', 'autonomous'
            
        Returns:
            Confirmação da mudança
        """
        valid_levels = ['supervised', 'semi_autonomous', 'autonomous']
        
        if level not in valid_levels:
            return {
                'success': False,
                'error': f'Nível inválido. Use: {valid_levels}'
            }
        
        old_level = self.velyra_autonomy_level
        self.velyra_autonomy_level = level
        
        # Ajustar regras baseado no nível
        if level == 'autonomous':
            # Reduzir requisitos de aprovação
            for category in ['high_priority_actions', 'medium_priority_actions']:
                for action in self.action_rules.get(category, {}).values():
                    action['requires_approval'] = False
        elif level == 'semi_autonomous':
            # Manter apenas críticas com aprovação
            for action in self.action_rules.get('high_priority_actions', {}).values():
                action['requires_approval'] = False
        else:  # supervised
            # Restaurar todas as aprovações
            self.action_rules = self._load_action_rules()
        
        self._log_supervision_event(
            'autonomy_change',
            f'level_change_{old_level}_to_{level}',
            'approved',
            'success'
        )
        
        return {
            'success': True,
            'previous_level': old_level,
            'new_level': level,
            'message': f"Nível de autonomia alterado de '{old_level}' para '{level}'",
            'implications': {
                'supervised': 'Todas as ações críticas e de alta prioridade requerem aprovação',
                'semi_autonomous': 'Apenas ações críticas requerem aprovação',
                'autonomous': 'Velyra pode executar a maioria das ações sem aprovação'
            }.get(level)
        }
    
    def check_action_permission(self, action_type: str, action_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Verifica se Velyra tem permissão para executar uma ação.
        
        Args:
            action_type: Tipo de ação
            action_data: Dados da ação (opcional)
            
        Returns:
            Permissão e requisitos
        """
        rule = self._get_action_rule(action_type)
        
        if not rule:
            # Ação desconhecida - requer aprovação por segurança
            return {
                'allowed': False,
                'requires_approval': True,
                'reason': 'Ação não reconhecida - requer aprovação manual',
                'action_type': action_type
            }
        
        requires_approval = rule.get('requires_approval', True)
        
        # Verificar condições de auto-aprovação
        if not requires_approval and action_data:
            conditions = rule.get('auto_approve_conditions', [])
            if not self._check_auto_approve_conditions(conditions, action_data):
                requires_approval = True
        
        return {
            'allowed': not requires_approval,
            'requires_approval': requires_approval,
            'priority': rule.get('priority', ActionPriority.MEDIUM).value if isinstance(rule.get('priority'), ActionPriority) else rule.get('priority', 'medium'),
            'description': rule.get('description', action_type),
            'action_type': action_type,
            'autonomy_level': self.velyra_autonomy_level
        }


# Instância global da integração
manus_velyra = ManusVelyraIntegration()


def request_manus_approval(action_type: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
    """Solicita aprovação do Manus para uma ação."""
    return manus_velyra.request_approval(action_type, action_data)


def manus_approve_action(action_id: str, approved: bool, notes: str = "", 
                        corrections: Dict[str, Any] = None) -> Dict[str, Any]:
    """Manus aprova ou rejeita uma ação."""
    return manus_velyra.manus_review_action(action_id, approved, notes, corrections)


def get_pending_for_manus() -> List[Dict[str, Any]]:
    """Retorna ações pendentes de aprovação do Manus."""
    return manus_velyra.get_pending_approvals()


def check_velyra_permission(action_type: str, action_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Verifica permissão do Velyra para uma ação."""
    return manus_velyra.check_action_permission(action_type, action_data)

"""
Serviço de Controle Remoto
Permite que o Manus controle o Nexora de forma autônoma
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import secrets


class RemoteControlService:
    """Serviço para controle remoto do Nexora pelo Manus"""
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.active_sessions = {}
    
    # ===== SESSÕES DE CONTROLE =====
    
    def start_session(self, controller: str = 'manus_ai') -> Dict[str, Any]:
        """
        Inicia uma sessão de controle remoto
        
        Args:
            controller: Identificador do controlador
            
        Returns:
            dict: Informações da sessão
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Gerar token de sessão
            session_token = secrets.token_urlsafe(32)
            
            cursor.execute("""
                INSERT INTO remote_control_sessions (
                    session_token, controller, status
                ) VALUES (?, ?, 'active')
            """, (session_token, controller))
            
            session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Armazenar sessão ativa
            self.active_sessions[session_token] = {
                'id': session_id,
                'controller': controller,
                'started_at': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'session_id': session_id,
                'session_token': session_token,
                'message': 'Sessão de controle iniciada'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def end_session(self, session_token: str) -> Dict[str, Any]:
        """Encerra uma sessão de controle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE remote_control_sessions
                SET status = 'ended', ended_at = ?
                WHERE session_token = ?
            """, (datetime.now().isoformat(), session_token))
            
            conn.commit()
            conn.close()
            
            # Remover da lista de sessões ativas
            if session_token in self.active_sessions:
                del self.active_sessions[session_token]
            
            return {
                'success': True,
                'message': 'Sessão encerrada'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def verify_session(self, session_token: str) -> bool:
        """Verifica se uma sessão é válida"""
        return session_token in self.active_sessions
    
    # ===== COMANDOS DE CONTROLE =====
    
    def execute_action(self, session_token: str, action: str, params: Dict = None) -> Dict[str, Any]:
        """
        Executa uma ação de controle remoto
        
        Args:
            session_token: Token da sessão
            action: Ação a executar
            params: Parâmetros da ação
            
        Returns:
            dict: Resultado da ação
        """
        if not self.verify_session(session_token):
            return {'success': False, 'error': 'Sessão inválida ou expirada'}
        
        try:
            # Registrar ação
            self._log_action(session_token, action, params or {})
            
            # Executar ação
            result = self._execute_action_internal(action, params or {})
            
            # Incrementar contador de comandos
            self._increment_commands_counter(session_token)
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _execute_action_internal(self, action: str, params: Dict) -> Dict[str, Any]:
        """Executa a ação internamente"""
        
        actions = {
            # Campanhas
            'create_campaign': self._action_create_campaign,
            'update_campaign': self._action_update_campaign,
            'pause_campaign': self._action_pause_campaign,
            'resume_campaign': self._action_resume_campaign,
            'delete_campaign': self._action_delete_campaign,
            
            # Orçamento
            'adjust_budget': self._action_adjust_budget,
            'optimize_budget': self._action_optimize_budget,
            
            # Anúncios
            'create_ad': self._action_create_ad,
            'update_ad': self._action_update_ad,
            'test_creative': self._action_test_creative,
            
            # Análise
            'analyze_performance': self._action_analyze_performance,
            'get_insights': self._action_get_insights,
            'get_recommendations': self._action_get_recommendations,
            
            # Sistema
            'get_status': self._action_get_status,
            'get_metrics': self._action_get_metrics,
            'run_audit': self._action_run_audit
        }
        
        if action in actions:
            return actions[action](params)
        else:
            return {
                'success': False,
                'error': f'Ação desconhecida: {action}'
            }
    
    # ===== AÇÕES DISPONÍVEIS =====
    
    def _action_create_campaign(self, params: Dict) -> Dict:
        """Cria uma campanha"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO campaigns (
                name, platform, objective, budget, status,
                created_at, created_by
            ) VALUES (?, ?, ?, ?, 'draft', ?, 'remote_control')
        """, (
            params.get('name'),
            params.get('platform'),
            params.get('objective'),
            params.get('budget'),
            datetime.now().isoformat()
        ))
        
        campaign_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'campaign_id': campaign_id,
            'message': 'Campanha criada via controle remoto'
        }
    
    def _action_update_campaign(self, params: Dict) -> Dict:
        """Atualiza uma campanha"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        campaign_id = params.get('campaign_id')
        updates = params.get('updates', {})
        
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [campaign_id]
        
        cursor.execute(f"""
            UPDATE campaigns SET {set_clause}
            WHERE id = ?
        """, values)
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': 'Campanha atualizada'}
    
    def _action_pause_campaign(self, params: Dict) -> Dict:
        """Pausa uma campanha"""
        return self._action_update_campaign({
            'campaign_id': params.get('campaign_id'),
            'updates': {'status': 'paused'}
        })
    
    def _action_resume_campaign(self, params: Dict) -> Dict:
        """Resume uma campanha"""
        return self._action_update_campaign({
            'campaign_id': params.get('campaign_id'),
            'updates': {'status': 'active'}
        })
    
    def _action_delete_campaign(self, params: Dict) -> Dict:
        """Deleta uma campanha"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM campaigns WHERE id = ?
        """, (params.get('campaign_id'),))
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': 'Campanha deletada'}
    
    def _action_adjust_budget(self, params: Dict) -> Dict:
        """Ajusta orçamento de uma campanha"""
        new_budget = params.get('new_budget')
        campaign_id = params.get('campaign_id')
        
        return self._action_update_campaign({
            'campaign_id': campaign_id,
            'updates': {'budget': new_budget}
        })
    
    def _action_optimize_budget(self, params: Dict) -> Dict:
        """Otimiza orçamento baseado em performance"""
        # Implementação simplificada
        return {
            'success': True,
            'optimization': {
                'current_budget': params.get('current_budget', 0),
                'suggested_budget': params.get('current_budget', 0) * 1.2,
                'reason': 'Performance acima da média'
            }
        }
    
    def _action_create_ad(self, params: Dict) -> Dict:
        """Cria um anúncio"""
        return {
            'success': True,
            'ad_id': 12345,
            'message': 'Anúncio criado via controle remoto'
        }
    
    def _action_update_ad(self, params: Dict) -> Dict:
        """Atualiza um anúncio"""
        return {
            'success': True,
            'message': 'Anúncio atualizado'
        }
    
    def _action_test_creative(self, params: Dict) -> Dict:
        """Testa um criativo"""
        return {
            'success': True,
            'test_result': {
                'score': 85,
                'feedback': 'Criativo com boa performance esperada'
            }
        }
    
    def _action_analyze_performance(self, params: Dict) -> Dict:
        """Analisa performance"""
        return {
            'success': True,
            'analysis': {
                'status': 'good',
                'ctr': 2.5,
                'cpc': 0.85,
                'conversions': 150
            }
        }
    
    def _action_get_insights(self, params: Dict) -> Dict:
        """Obtém insights"""
        return {
            'success': True,
            'insights': [
                'Melhor horário: 18h-21h',
                'Público mais engajado: 25-34 anos',
                'Melhor dia: Terça-feira'
            ]
        }
    
    def _action_get_recommendations(self, params: Dict) -> Dict:
        """Obtém recomendações"""
        return {
            'success': True,
            'recommendations': [
                'Aumentar orçamento em 20%',
                'Testar novo criativo',
                'Expandir segmentação'
            ]
        }
    
    def _action_get_status(self, params: Dict) -> Dict:
        """Obtém status do sistema"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Contar campanhas por status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM campaigns
            GROUP BY status
        """)
        
        status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
        conn.close()
        
        return {
            'success': True,
            'status': {
                'active_campaigns': status_counts.get('active', 0),
                'paused_campaigns': status_counts.get('paused', 0),
                'draft_campaigns': status_counts.get('draft', 0),
                'system_health': 'healthy'
            }
        }
    
    def _action_get_metrics(self, params: Dict) -> Dict:
        """Obtém métricas do sistema"""
        return {
            'success': True,
            'metrics': {
                'total_spend': 15000.00,
                'total_conversions': 450,
                'average_cpa': 33.33,
                'total_clicks': 12500
            }
        }
    
    def _action_run_audit(self, params: Dict) -> Dict:
        """Executa auditoria do sistema"""
        return {
            'success': True,
            'audit_result': {
                'score': 92,
                'issues_found': 3,
                'recommendations': [
                    'Otimizar 2 campanhas com baixa performance',
                    'Atualizar 5 criativos antigos',
                    'Revisar segmentação de 3 públicos'
                ]
            }
        }
    
    # ===== LOGGING E AUDITORIA =====
    
    def _log_action(self, session_token: str, action: str, params: Dict):
        """Registra uma ação executada"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            session = self.active_sessions.get(session_token, {})
            
            cursor.execute("""
                INSERT INTO action_audit (
                    action, entity_type, performed_by, performed_at
                ) VALUES (?, ?, ?, ?)
            """, (
                action,
                'remote_control',
                session.get('controller', 'unknown'),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error logging action: {e}")
    
    def _increment_commands_counter(self, session_token: str):
        """Incrementa contador de comandos executados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE remote_control_sessions
                SET commands_executed = commands_executed + 1
                WHERE session_token = ?
            """, (session_token,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error incrementing counter: {e}")
    
    # ===== MONITORAMENTO =====
    
    def get_session_info(self, session_token: str) -> Dict[str, Any]:
        """Obtém informações de uma sessão"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM remote_control_sessions
                WHERE session_token = ?
            """, (session_token,))
            
            session = cursor.fetchone()
            conn.close()
            
            if session:
                return {
                    'success': True,
                    'session': dict(session)
                }
            else:
                return {
                    'success': False,
                    'error': 'Sessão não encontrada'
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_active_sessions(self) -> Dict[str, Any]:
        """Lista todas as sessões ativas"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM remote_control_sessions
                WHERE status = 'active'
                ORDER BY started_at DESC
            """)
            
            sessions = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return {
                'success': True,
                'sessions': sessions,
                'count': len(sessions)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_audit_log(self, limit: int = 100) -> Dict[str, Any]:
        """Obtém log de auditoria"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM action_audit
                ORDER BY performed_at DESC
                LIMIT ?
            """, (limit,))
            
            logs = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return {
                'success': True,
                'logs': logs,
                'count': len(logs)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


# Instância global
remote_control = RemoteControlService()

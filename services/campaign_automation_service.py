"""
Serviço de Automação de Campanhas
Automação completa com sistema de autorização de gastos
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random


class CampaignAutomationService:
    """Serviço para automação completa de campanhas com autorização"""
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        
        # Configurações de automação
        self.auto_optimization_enabled = True
        self.auto_pause_enabled = True
        self.auto_budget_adjustment_enabled = True
        
        # Limites de segurança
        self.max_budget_increase_percent = 50  # Máximo 50% de aumento sem autorização
        self.max_single_transaction = 1000.00  # R$ 1000 por transação sem autorização
        self.min_performance_score = 40  # Score mínimo para manter campanha ativa
    
    # ===== AUTORIZAÇÃO DE GASTOS =====
    
    def request_spend_authorization(
        self,
        action: str,
        amount: float,
        campaign_id: int = None,
        notes: str = None
    ) -> Dict[str, Any]:
        """
        Solicita autorização para gastar dinheiro
        
        Args:
            action: Ação que requer autorização
            amount: Valor em reais
            campaign_id: ID da campanha (opcional)
            notes: Notas adicionais
            
        Returns:
            dict: Resultado da solicitação
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO spend_authorizations (
                    campaign_id, action, amount, currency, status, notes
                ) VALUES (?, ?, ?, 'BRL', 'pending', ?)
            """, (campaign_id, action, amount, notes))
            
            auth_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Verificar se precisa de autorização manual
            needs_approval = self._needs_manual_approval(action, amount)
            
            if not needs_approval:
                # Auto-aprovar
                return self.approve_spend_authorization(auth_id, 'auto_approved')
            
            return {
                'success': True,
                'authorization_id': auth_id,
                'status': 'pending',
                'needs_approval': True,
                'message': f'Autorização necessária para {action} de R$ {amount:.2f}'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _needs_manual_approval(self, action: str, amount: float) -> bool:
        """Verifica se uma ação precisa de aprovação manual"""
        
        # Auto-aprovar criação de campanhas com orçamento baixo (< R$200)
        if action == 'create_campaign' and amount < 200.00:
            return False
        
        # Ações que sempre precisam de aprovação (exceto create_campaign com budget baixo)
        high_risk_actions = [
            'create_campaign',
            'delete_campaign',
            'major_budget_increase'
        ]
        
        if action in high_risk_actions:
            return True
        
        # Valores acima do limite precisam de aprovação
        if amount > self.max_single_transaction:
            return True
        
        return False
    
    def approve_spend_authorization(
        self,
        auth_id: int,
        approved_by: str = 'user'
    ) -> Dict[str, Any]:
        """Aprova uma autorização de gasto"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE spend_authorizations
                SET status = 'approved',
                    responded_at = ?,
                    response_by = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), approved_by, auth_id))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': 'Autorização aprovada'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def reject_spend_authorization(
        self,
        auth_id: int,
        rejected_by: str = 'user',
        reason: str = None
    ) -> Dict[str, Any]:
        """Rejeita uma autorização de gasto"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE spend_authorizations
                SET status = 'rejected',
                    responded_at = ?,
                    response_by = ?,
                    notes = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), rejected_by, reason, auth_id))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': 'Autorização rejeitada'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_pending_authorizations(self) -> Dict[str, Any]:
        """Obtém todas as autorizações pendentes"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT a.*, c.name as campaign_name
                FROM spend_authorizations a
                LEFT JOIN campaigns c ON a.campaign_id = c.id
                WHERE a.status = 'pending'
                ORDER BY a.requested_at DESC
            """)
            
            authorizations = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return {
                'success': True,
                'authorizations': authorizations,
                'count': len(authorizations)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== AUTOMAÇÃO DE CAMPANHAS =====
    
    def auto_optimize_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """
        Otimiza automaticamente uma campanha
        
        Args:
            campaign_id: ID da campanha
            
        Returns:
            dict: Resultado da otimização
        """
        if not self.auto_optimization_enabled:
            return {
                'success': False,
                'error': 'Auto-otimização desabilitada'
            }
        
        try:
            # Analisar performance
            performance = self._analyze_campaign_performance(campaign_id)
            
            if not performance['success']:
                return performance
            
            actions_taken = []
            
            # Otimizar orçamento
            if performance['score'] >= 80:
                budget_result = self._auto_adjust_budget(campaign_id, 'increase', 20)
                if budget_result['success']:
                    actions_taken.append('Orçamento aumentado em 20%')
            
            elif performance['score'] < 40:
                budget_result = self._auto_adjust_budget(campaign_id, 'decrease', 30)
                if budget_result['success']:
                    actions_taken.append('Orçamento reduzido em 30%')
            
            # Pausar se performance muito ruim
            if performance['score'] < 20 and self.auto_pause_enabled:
                pause_result = self._auto_pause_campaign(campaign_id)
                if pause_result['success']:
                    actions_taken.append('Campanha pausada por baixa performance')
            
            # Otimizar segmentação
            if performance['ctr'] < 1.0:
                actions_taken.append('Recomendação: Revisar segmentação')
            
            # Otimizar criativos
            if performance['cpc'] > 2.0:
                actions_taken.append('Recomendação: Testar novos criativos')
            
            return {
                'success': True,
                'campaign_id': campaign_id,
                'performance_score': performance['score'],
                'actions_taken': actions_taken,
                'recommendations': performance.get('recommendations', [])
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _analyze_campaign_performance(self, campaign_id: int) -> Dict[str, Any]:
        """Analisa performance de uma campanha"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Obter métricas dos últimos 7 dias
            cursor.execute("""
                SELECT * FROM campaign_metrics
                WHERE campaign_id = ?
                ORDER BY date DESC
                LIMIT 7
            """, (campaign_id,))
            
            metrics = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            if not metrics:
                return {
                    'success': True,
                    'score': 50,
                    'ctr': 0,
                    'cpc': 0,
                    'conversions': 0,
                    'recommendations': ['Dados insuficientes para análise']
                }
            
            # Calcular métricas agregadas
            total_impressions = sum(m.get('impressions', 0) for m in metrics)
            total_clicks = sum(m.get('clicks', 0) for m in metrics)
            total_conversions = sum(m.get('conversions', 0) for m in metrics)
            total_spend = sum(m.get('spend', 0) for m in metrics)
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
            cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
            
            # Calcular score de performance
            score = 0
            if ctr > 2.0:
                score += 35
            elif ctr > 1.0:
                score += 20
            
            if cpc < 1.0:
                score += 35
            elif cpc < 2.0:
                score += 20
            
            if cpa < 50.0:
                score += 30
            elif cpa < 100.0:
                score += 15
            
            # Gerar recomendações
            recommendations = []
            if ctr < 1.0:
                recommendations.append('CTR baixo - melhorar criativos')
            if cpc > 2.0:
                recommendations.append('CPC alto - otimizar lances')
            if cpa > 100.0:
                recommendations.append('CPA alto - revisar funil')
            
            return {
                'success': True,
                'score': score,
                'ctr': round(ctr, 2),
                'cpc': round(cpc, 2),
                'cpa': round(cpa, 2),
                'conversions': total_conversions,
                'recommendations': recommendations
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _auto_adjust_budget(
        self,
        campaign_id: int,
        direction: str,
        percent: float
    ) -> Dict[str, Any]:
        """Ajusta orçamento automaticamente"""
        if not self.auto_budget_adjustment_enabled:
            return {'success': False, 'error': 'Ajuste automático desabilitado'}
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Obter orçamento atual
            cursor.execute("SELECT budget FROM campaigns WHERE id = ?", (campaign_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return {'success': False, 'error': 'Campanha não encontrada'}
            
            current_budget = row['budget']
            
            # Calcular novo orçamento
            if direction == 'increase':
                new_budget = current_budget * (1 + percent / 100)
                amount_change = new_budget - current_budget
            else:
                new_budget = current_budget * (1 - percent / 100)
                amount_change = current_budget - new_budget
            
            # Verificar se precisa de autorização
            if amount_change > self.max_single_transaction:
                conn.close()
                return self.request_spend_authorization(
                    action=f'budget_{direction}',
                    amount=amount_change,
                    campaign_id=campaign_id,
                    notes=f'Ajuste automático de {percent}%'
                )
            
            # Atualizar orçamento
            cursor.execute("""
                UPDATE campaigns
                SET budget = ?
                WHERE id = ?
            """, (new_budget, campaign_id))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'old_budget': current_budget,
                'new_budget': new_budget,
                'change_percent': percent
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _auto_pause_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """Pausa automaticamente uma campanha"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE campaigns
                SET status = 'paused'
                WHERE id = ?
            """, (campaign_id,))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': 'Campanha pausada automaticamente'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== OTIMIZAÇÃO EM LOTE =====
    
    def optimize_all_campaigns(self) -> Dict[str, Any]:
        """Otimiza todas as campanhas ativas"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id FROM campaigns
                WHERE status = 'active'
            """)
            
            campaigns = cursor.fetchall()
            conn.close()
            
            results = []
            
            for campaign in campaigns:
                result = self.auto_optimize_campaign(campaign['id'])
                results.append({
                    'campaign_id': campaign['id'],
                    'result': result
                })
            
            return {
                'success': True,
                'campaigns_optimized': len(results),
                'results': results
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== AGENDAMENTO DE AÇÕES =====
    
    def schedule_campaign_action(
        self,
        campaign_id: int,
        action: str,
        scheduled_time: str,
        params: Dict = None
    ) -> Dict[str, Any]:
        """Agenda uma ação para ser executada no futuro"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO scheduled_actions (
                    campaign_id, action, params, scheduled_time, status
                ) VALUES (?, ?, ?, ?, 'pending')
            """, (
                campaign_id,
                action,
                json.dumps(params or {}),
                scheduled_time
            ))
            
            action_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'action_id': action_id,
                'message': f'Ação agendada para {scheduled_time}'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== RELATÓRIOS =====
    
    def get_automation_report(self, days: int = 7) -> Dict[str, Any]:
        """Gera relatório de automação"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Contar autorizações
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM spend_authorizations
                WHERE requested_at >= ?
                GROUP BY status
            """, (start_date,))
            
            auth_stats = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Contar ações de auditoria
            cursor.execute("""
                SELECT action, COUNT(*) as count
                FROM action_audit
                WHERE performed_at >= ?
                GROUP BY action
            """, (start_date,))
            
            action_stats = {row['action']: row['count'] for row in cursor.fetchall()}
            
            conn.close()
            
            return {
                'success': True,
                'period_days': days,
                'authorization_stats': auth_stats,
                'action_stats': action_stats,
                'total_authorizations': sum(auth_stats.values()),
                'total_actions': sum(action_stats.values())
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


# Instância global
campaign_automation = CampaignAutomationService()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Velyra Campaign Monitor - Sistema de Monitoramento 24/7
Monitora campanhas continuamente e toma ações corretivas automaticamente
"""

import sqlite3
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading

# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres


class VelyraCampaignMonitor:
    """
    Sistema de monitoramento 24/7 de campanhas
    Monitora métricas, detecta problemas e toma ações corretivas
    """
    
    def __init__(self, db_path: str = "nexora.db"):
        self.db_path = db_path
        self.running = False
        self.thread = None
        
        # Thresholds de alerta
        self.thresholds = {
            "cpa_max": 50,  # CPA máximo aceitável (R$)
            "ctr_min": 0.5,  # CTR mínimo aceitável (%)
            "roas_min": 1.5,  # ROAS mínimo aceitável
            "budget_utilization_min": 0.7,  # Utilização mínima de budget (70%)
            "budget_utilization_max": 0.95,  # Utilização máxima de budget (95%)
        }
        
        # Ações corretivas automáticas
        self.auto_actions = {
            "high_cpa": True,  # Pausar anúncios com CPA alto
            "low_ctr": True,  # Pausar anúncios com CTR baixo
            "low_roas": True,  # Reduzir budget de campanhas com ROAS baixo
            "budget_exhaustion": True,  # Aumentar budget se acabando
        }
    
    def _get_db(self):
        """Retorna conexão com o banco de dados"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        return conn
    
    def start(self):
        """Inicia o monitor em background"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            print("✅ Velyra Campaign Monitor iniciado - Monitoramento 24/7 ativo")
    
    def stop(self):
        """Para o monitor"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("⏹️ Velyra Campaign Monitor parado")
    
    def _run_loop(self):
        """Loop principal do monitor"""
        while self.running:
            try:
                self.monitor_all_campaigns()
                time.sleep(300)  # Verifica a cada 5 minutos
            except Exception as e:
                print(f"❌ Erro no monitor: {e}")
                time.sleep(60)
    
    def monitor_all_campaigns(self):
        """Monitora todas as campanhas ativas"""
        campaigns = self.get_active_campaigns()
        
        for campaign in campaigns:
            try:
                # Busca métricas da campanha
                metrics = self.get_campaign_metrics(campaign['id'])
                
                # Verifica problemas
                issues = self.detect_issues(campaign, metrics)
                
                # Toma ações corretivas se necessário
                if issues:
                    self.take_corrective_actions(campaign, issues)
                    self.log_monitoring_event(campaign['id'], issues)
                
            except Exception as e:
                print(f"❌ Erro ao monitorar campanha {campaign['id']}: {e}")
    
    def get_active_campaigns(self) -> List[Dict]:
        """Retorna lista de campanhas ativas"""
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM campaigns 
            WHERE status = 'active' 
            ORDER BY created_at DESC
        """)
        
        campaigns = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return campaigns
    
    def get_campaign_metrics(self, campaign_id: int) -> Dict:
        """Busca métricas da campanha"""
        # Aqui você integraria com as APIs do Google Ads, Meta Ads, etc.
        # Por enquanto, retorna métricas simuladas
        
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM campaign_metrics 
            WHERE campaign_id = ? 
            ORDER BY date DESC 
            LIMIT 1
        """, (campaign_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        
        # Retorna métricas padrão se não houver dados
        return {
            "impressions": 0,
            "clicks": 0,
            "conversions": 0,
            "spend": 0,
            "revenue": 0,
            "ctr": 0,
            "cpa": 0,
            "roas": 0,
        }
    
    def detect_issues(self, campaign: Dict, metrics: Dict) -> List[Dict]:
        """Detecta problemas na campanha"""
        issues = []
        
        # Verifica CPA alto
        if metrics.get('cpa', 0) > self.thresholds['cpa_max']:
            issues.append({
                "type": "high_cpa",
                "severity": "high",
                "message": f"CPA muito alto: R$ {metrics['cpa']:.2f} (máx: R$ {self.thresholds['cpa_max']})",
                "metric": "cpa",
                "current_value": metrics['cpa'],
                "threshold": self.thresholds['cpa_max']
            })
        
        # Verifica CTR baixo
        if metrics.get('ctr', 0) < self.thresholds['ctr_min']:
            issues.append({
                "type": "low_ctr",
                "severity": "medium",
                "message": f"CTR muito baixo: {metrics['ctr']:.2f}% (mín: {self.thresholds['ctr_min']}%)",
                "metric": "ctr",
                "current_value": metrics['ctr'],
                "threshold": self.thresholds['ctr_min']
            })
        
        # Verifica ROAS baixo
        if metrics.get('roas', 0) < self.thresholds['roas_min']:
            issues.append({
                "type": "low_roas",
                "severity": "high",
                "message": f"ROAS muito baixo: {metrics['roas']:.2f}x (mín: {self.thresholds['roas_min']}x)",
                "metric": "roas",
                "current_value": metrics['roas'],
                "threshold": self.thresholds['roas_min']
            })
        
        # Verifica utilização de budget
        budget = float(campaign.get('budget', 0))
        spend = float(metrics.get('spend', 0))
        
        if budget > 0:
            utilization = spend / budget
            
            if utilization > self.thresholds['budget_utilization_max']:
                issues.append({
                    "type": "budget_exhaustion",
                    "severity": "high",
                    "message": f"Budget quase esgotado: {utilization*100:.1f}% utilizado",
                    "metric": "budget_utilization",
                    "current_value": utilization,
                    "threshold": self.thresholds['budget_utilization_max']
                })
        
        return issues
    
    def take_corrective_actions(self, campaign: Dict, issues: List[Dict]):
        """Toma ações corretivas baseado nos problemas detectados"""
        for issue in issues:
            issue_type = issue['type']
            
            if issue_type == "high_cpa" and self.auto_actions.get('high_cpa'):
                self.reduce_budget(campaign['id'], 0.8)  # Reduz 20%
                print(f"⚠️ Campanha {campaign['id']}: Budget reduzido devido a CPA alto")
            
            elif issue_type == "low_ctr" and self.auto_actions.get('low_ctr'):
                self.pause_low_performing_ads(campaign['id'])
                print(f"⚠️ Campanha {campaign['id']}: Anúncios com CTR baixo pausados")
            
            elif issue_type == "low_roas" and self.auto_actions.get('low_roas'):
                self.reduce_budget(campaign['id'], 0.7)  # Reduz 30%
                print(f"⚠️ Campanha {campaign['id']}: Budget reduzido devido a ROAS baixo")
            
            elif issue_type == "budget_exhaustion" and self.auto_actions.get('budget_exhaustion'):
                self.request_budget_increase(campaign['id'], 1.2)  # Aumenta 20%
                print(f"📈 Campanha {campaign['id']}: Solicitação de aumento de budget")
    
    def reduce_budget(self, campaign_id: int, multiplier: float):
        """Reduz o budget da campanha"""
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE campaigns 
            SET budget = budget * ?,
                last_optimized = ?
            WHERE id = ?
        """, (multiplier, datetime.now().isoformat(), campaign_id))
        
        conn.commit()
        conn.close()
    
    def pause_low_performing_ads(self, campaign_id: int):
        """Pausa anúncios com performance baixa"""
        # Aqui você integraria com as APIs para pausar anúncios específicos
        pass
    
    def request_budget_increase(self, campaign_id: int, multiplier: float):
        """Solicita aumento de budget (requer aprovação)"""
        from services.velyra_auto_executor import auto_executor
        
        # Cria ação pendente para aprovação
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT budget FROM campaigns WHERE id = ?
        """, (campaign_id,))
        
        row = cursor.fetchone()
        current_budget = float(row['budget']) if row else 0
        new_budget = current_budget * multiplier
        
        cursor.execute("""
            INSERT INTO velyra_actions (action_type, parameters, status, priority, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            'increase_budget',
            json.dumps({
                'campaign_id': campaign_id,
                'current_budget': current_budget,
                'new_budget': new_budget,
                'reason': 'Budget quase esgotado'
            }),
            'pending',
            'high',
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def log_monitoring_event(self, campaign_id: int, issues: List[Dict]):
        """Registra evento de monitoramento"""
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO monitoring_log (campaign_id, issues, timestamp)
            VALUES (?, ?, ?)
        """, (campaign_id, json.dumps(issues), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()


# Instância global do monitor
campaign_monitor = VelyraCampaignMonitor()

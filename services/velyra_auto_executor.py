#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Velyra Auto Executor - Sistema de Auto-Aprovação e Execução Automática
Processa ações pendentes e executa automaticamente após aprovação
"""

import sqlite3
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import threading

class VelyraAutoExecutor:
    """
    Sistema de auto-aprovação e execução automática de ações do Velyra Prime
    """
    
    def __init__(self, db_path: str = "nexora.db"):
        self.db_path = db_path
        self.running = False
        self.thread = None
        
        # Configurações de auto-aprovação por tipo de ação
        self.auto_approve_config = {
            "create_campaign": {"enabled": True, "max_budget": 500},  # Auto-aprova até R$ 500
            "generate_copy": {"enabled": True},
            "analyze_performance": {"enabled": True},
            "optimize_campaign": {"enabled": True, "max_budget_change": 0.3},  # Até 30% de mudança
            "pause_campaign": {"enabled": False},  # Requer aprovação manual
            "delete_campaign": {"enabled": False},  # Requer aprovação manual
        }
    
    def _get_db(self):
        """Retorna conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def start(self):
        """Inicia o executor em background"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            print("✅ Velyra Auto Executor iniciado")
    
    def stop(self):
        """Para o executor"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("⏹️ Velyra Auto Executor parado")
    
    def _run_loop(self):
        """Loop principal do executor"""
        while self.running:
            try:
                self.process_pending_actions()
                time.sleep(5)  # Verifica a cada 5 segundos
            except Exception as e:
                print(f"❌ Erro no executor: {e}")
                time.sleep(10)
    
    def process_pending_actions(self):
        """Processa todas as ações pendentes"""
        pending_actions = self.get_pending_actions()
        
        for action in pending_actions:
            try:
                # Verifica se pode auto-aprovar
                if self.can_auto_approve(action):
                    self.approve_action(action['id'])
                    self.execute_action(action)
                    print(f"✅ Ação {action['id']} auto-aprovada e executada: {action['action_type']}")
            except Exception as e:
                print(f"❌ Erro ao processar ação {action['id']}: {e}")
    
    def get_pending_actions(self) -> List[Dict]:
        """Retorna lista de ações pendentes"""
        conn = self._get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM velyra_actions 
            WHERE status = 'pending' 
            ORDER BY created_at ASC
            LIMIT 50
        """)
        
        actions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return actions
    
    def can_auto_approve(self, action: Dict) -> bool:
        """Verifica se a ação pode ser auto-aprovada"""
        action_type = action.get('action_type')
        
        # Verifica se o tipo de ação está configurado para auto-aprovação
        config = self.auto_approve_config.get(action_type, {})
        if not config.get('enabled', False):
            return False
        
        # Verifica restrições específicas por tipo
        try:
            params = json.loads(action.get('parameters', '{}'))
            
            if action_type == "create_campaign":
                budget = float(params.get('budget', 0))
                max_budget = config.get('max_budget', 500)
                return budget <= max_budget
            
            elif action_type == "optimize_campaign":
                budget_change = float(params.get('budget_change_percent', 0))
                max_change = config.get('max_budget_change', 0.3)
                return abs(budget_change) <= max_change
            
            # Outros tipos: auto-aprova se enabled=True
            return True
            
        except Exception as e:
            print(f"⚠️ Erro ao verificar auto-aprovação: {e}")
            return False
    
    def approve_action(self, action_id: int):
        """Aprova uma ação"""
        conn = self._get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE velyra_actions 
            SET status = 'approved', 
                approved_at = ?,
                approved_by = 'AUTO_EXECUTOR'
            WHERE id = ?
        """, (datetime.now().isoformat(), action_id))
        
        conn.commit()
        conn.close()
    
    def execute_action(self, action: Dict):
        """Executa uma ação aprovada"""
        action_type = action.get('action_type')
        parameters = json.loads(action.get('parameters', '{}'))
        
        try:
            # Importa os executores necessários
            from services.velyra_action_engine import VelyraActionEngine
            
            engine = VelyraActionEngine()
            
            # Executa a ação baseado no tipo
            if action_type == "create_campaign":
                result = engine.create_campaign(parameters)
            elif action_type == "generate_copy":
                result = engine.generate_ad_copy(parameters)
            elif action_type == "analyze_performance":
                result = engine.analyze_campaign_performance(parameters)
            elif action_type == "optimize_campaign":
                result = engine.optimize_campaign(parameters)
            else:
                result = {"error": f"Tipo de ação desconhecido: {action_type}"}
            
            # Atualiza status da ação
            self.mark_action_completed(action['id'], result)
            
        except Exception as e:
            self.mark_action_failed(action['id'], str(e))
            raise
    
    def mark_action_completed(self, action_id: int, result: Dict):
        """Marca ação como concluída"""
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE velyra_actions 
            SET status = 'completed',
                completed_at = ?,
                result = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), json.dumps(result), action_id))
        
        conn.commit()
        conn.close()
    
    def mark_action_failed(self, action_id: int, error: str):
        """Marca ação como falha"""
        conn = self._get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE velyra_actions 
            SET status = 'failed',
                completed_at = ?,
                result = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), json.dumps({"error": error}), action_id))
        
        conn.commit()
        conn.close()


# Instância global do executor
auto_executor = VelyraAutoExecutor()

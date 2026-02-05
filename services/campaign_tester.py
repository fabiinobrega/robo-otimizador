from functools import wraps
"""
NEXORA Operator v11.7 - Campaign Tester Service
Serviço de teste e aquecimento de campanhas com ajustes automáticos
"""

import sqlite3
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional
import time
# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres


class CampaignTester:
    """
    Testador e aquecedor de campanhas com monitoramento inteligente
    """
    

def handle_errors(func):
    """Decorador para tratamento automático de erros"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Erro em {func.__name__}: {str(e)}")
            return None
    return wrapper


    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.warming_stages = [
            {
                'stage': 1,
                'name': 'Início (0-2h)',
                'duration_hours': 2,
                'budget_multiplier': 0.3,  # 30% do orçamento
                'min_impressions': 100,
                'actions': ['monitor_delivery', 'check_approval']
            },
            {
                'stage': 2,
                'name': 'Aquecimento Inicial (2-6h)',
                'duration_hours': 4,
                'budget_multiplier': 0.5,  # 50% do orçamento
                'min_impressions': 500,
                'actions': ['optimize_audience', 'test_creatives']
            },
            {
                'stage': 3,
                'name': 'Aquecimento Médio (6-12h)',
                'duration_hours': 6,
                'budget_multiplier': 0.75,  # 75% do orçamento
                'min_impressions': 1000,
                'actions': ['adjust_bids', 'expand_audience']
            },
            {
                'stage': 4,
                'name': 'Aquecimento Final (12-24h)',
                'duration_hours': 12,
                'budget_multiplier': 1.0,  # 100% do orçamento
                'min_impressions': 2000,
                'actions': ['full_optimization', 'scale_budget']
            },
            {
                'stage': 5,
                'name': 'Campanha Aquecida (24h+)',
                'duration_hours': None,
                'budget_multiplier': 1.0,
                'min_impressions': 5000,
                'actions': ['continuous_optimization']
            }
        ]
    
    def create_test_campaign(self, campaign_data: Dict) -> Dict:
        """
        Cria uma campanha de teste com configurações otimizadas
        """
        conn = get_db_connection()
        c = conn.cursor()
        
        # Criar campanha de teste
        test_campaign = {
            'name': f"[TESTE] {campaign_data.get('name', 'Nova Campanha')}",
            'status': 'testing',
            'platform': campaign_data.get('platform', 'facebook'),
            'objective': campaign_data.get('objective', 'conversions'),
            'daily_budget': campaign_data.get('daily_budget', 50),
            'target_audience': campaign_data.get('target_audience', {}),
            'creatives': campaign_data.get('creatives', []),
            'start_date': datetime.now().isoformat(),
            'warming_stage': 1,
            'auto_adjust': True,
            'test_mode': True
        }
        
        c.execute(sql_param('''
            INSERT INTO campaigns (name, status, platform, objective, daily_budget, 
                                 target_audience, creatives, created_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''), (
            test_campaign['name'],
            test_campaign['status'],
            test_campaign['platform'],
            test_campaign['objective'],
            test_campaign['daily_budget'],
            json.dumps(test_campaign['target_audience']),
            json.dumps(test_campaign['creatives']),
            test_campaign['start_date'],
            json.dumps({
                'warming_stage': 1,
                'auto_adjust': True,
                'test_mode': True,
                'initial_budget': test_campaign['daily_budget']
            })
        ))
        
        campaign_id = c.lastrowid
        
        # Criar registro de aquecimento
        c.execute(sql_param('''
            INSERT INTO campaign_warming (campaign_id, stage, started_at, status)
            VALUES (?, ?, ?, ?)
        '''), (campaign_id, 1, datetime.now().isoformat(), 'active'))
        
        conn.commit()
        conn.close()
        
        # Gerar relatório inicial
        report = self.generate_stage_report(campaign_id, 1, 'started')
        
        return {
            'success': True,
            'campaign_id': campaign_id,
            'campaign': test_campaign,
            'report': report
        }
    
    def monitor_campaign(self, campaign_id: int) -> Dict:
        """
        Monitora campanha em tempo real e faz ajustes automáticos
        """
        conn = get_db_connection()
        c = conn.cursor()
        
        # Buscar campanha
        c.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
        campaign = c.fetchone()
        
        if not campaign:
            return {'success': False, 'error': 'Campanha não encontrada'}
        
        # Buscar métricas atuais
        c.execute(sql_param('''
            SELECT * FROM campaign_metrics 
            WHERE campaign_id = ? 
            ORDER BY timestamp DESC LIMIT 1
        '''), (campaign_id,))
        metrics = c.fetchone()
        
        # Determinar estágio atual
        metadata = json.loads(campaign[12]) if campaign[12] else {}
        current_stage = metadata.get('warming_stage', 1)
        
        # Calcular tempo desde início
        start_time = datetime.fromisoformat(campaign[8])
        hours_running = (datetime.now() - start_time).total_seconds() / 3600
        
        # Verificar se deve avançar para próximo estágio
        stage_info = self.warming_stages[current_stage - 1]
        should_advance = False
        
        if stage_info['duration_hours'] and hours_running >= stage_info['duration_hours']:
            should_advance = True
        
        # Fazer ajustes automáticos
        adjustments = self.auto_adjust_campaign(campaign_id, current_stage, metrics)
        
        # Avançar estágio se necessário
        if should_advance and current_stage < len(self.warming_stages):
            new_stage = current_stage + 1
            self.advance_warming_stage(campaign_id, new_stage)
            current_stage = new_stage
        
        # Gerar relatório
        report = self.generate_stage_report(campaign_id, current_stage, 'monitoring')
        
        conn.close()
        
        return {
            'success': True,
            'campaign_id': campaign_id,
            'current_stage': current_stage,
            'hours_running': round(hours_running, 2),
            'adjustments': adjustments,
            'report': report
        }
    
    def auto_adjust_campaign(self, campaign_id: int, stage: int, metrics: Optional[tuple]) -> List[Dict]:
        """
        Faz ajustes automáticos baseados no estágio e métricas
        """
        adjustments = []
        conn = get_db_connection()
        c = conn.cursor()
        
        # Buscar campanha
        c.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
        campaign = c.fetchone()
        
        if not campaign or not metrics:
            conn.close()
            return adjustments
        
        # Extrair métricas
        impressions = metrics[3] if len(metrics) > 3 else 0
        clicks = metrics[4] if len(metrics) > 4 else 0
        ctr = metrics[5] if len(metrics) > 5 else 0
        cpc = metrics[6] if len(metrics) > 6 else 0
        conversions = metrics[7] if len(metrics) > 7 else 0
        
        stage_info = self.warming_stages[stage - 1]
        
        # Ajuste 1: Orçamento baseado no estágio
        metadata = json.loads(campaign[12]) if campaign[12] else {}
        initial_budget = metadata.get('initial_budget', campaign[5])
        target_budget = initial_budget * stage_info['budget_multiplier']
        
        if campaign[5] != target_budget:
            c.execute('UPDATE campaigns SET daily_budget = ? WHERE id = ?', 
                     (target_budget, campaign_id))
            adjustments.append({
                'type': 'budget',
                'action': 'adjusted',
                'from': campaign[5],
                'to': target_budget,
                'reason': f'Estágio {stage} - {stage_info["name"]}'
            })
        
        # Ajuste 2: CTR muito baixo (< 1%)
        if ctr < 1.0 and impressions > 100:
            adjustments.append({
                'type': 'creative',
                'action': 'test_new_creative',
                'reason': f'CTR baixo ({ctr}%)',
                'recommendation': 'Testar novos criativos mais chamativos'
            })
        
        # Ajuste 3: CPC muito alto
        avg_cpc = 2.0  # Benchmark
        if cpc > avg_cpc * 1.5 and clicks > 10:
            adjustments.append({
                'type': 'bid',
                'action': 'lower_bid',
                'reason': f'CPC alto (R$ {cpc:.2f})',
                'recommendation': 'Reduzir lance em 20%'
            })
        
        # Ajuste 4: Sem impressões suficientes
        if impressions < stage_info['min_impressions']:
            adjustments.append({
                'type': 'audience',
                'action': 'expand_audience',
                'reason': f'Poucas impressões ({impressions})',
                'recommendation': 'Expandir público-alvo'
            })
        
        # Ajuste 5: Conversões baixas (estágios avançados)
        if stage >= 3 and clicks > 50 and conversions == 0:
            adjustments.append({
                'type': 'landing_page',
                'action': 'check_landing_page',
                'reason': 'Sem conversões após 50 cliques',
                'recommendation': 'Verificar landing page e pixel'
            })
        
        # Registrar ajustes
        for adj in adjustments:
            c.execute(sql_param('''
                INSERT INTO campaign_adjustments 
                (campaign_id, adjustment_type, action, reason, timestamp)
                VALUES (?, ?, ?, ?, ?)
            '''), (
                campaign_id,
                adj['type'],
                adj['action'],
                adj['reason'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        
        return adjustments
    
    def advance_warming_stage(self, campaign_id: int, new_stage: int):
        """
        Avança campanha para próximo estágio de aquecimento
        """
        conn = get_db_connection()
        c = conn.cursor()
        
        # Atualizar metadata da campanha
        c.execute('SELECT metadata FROM campaigns WHERE id = ?', (campaign_id,))
        result = c.fetchone()
        metadata = json.loads(result[0]) if result and result[0] else {}
        metadata['warming_stage'] = new_stage
        
        c.execute('UPDATE campaigns SET metadata = ? WHERE id = ?', 
                 (json.dumps(metadata), campaign_id))
        
        # Finalizar estágio anterior
        c.execute(sql_param('''
            UPDATE campaign_warming 
            SET status = 'completed', completed_at = ?
            WHERE campaign_id = ? AND stage = ?
        '''), (datetime.now().isoformat(), campaign_id, new_stage - 1))
        
        # Criar novo estágio
        c.execute(sql_param('''
            INSERT INTO campaign_warming (campaign_id, stage, started_at, status)
            VALUES (?, ?, ?, ?)
        '''), (campaign_id, new_stage, datetime.now().isoformat(), 'active'))
        
        conn.commit()
        conn.close()
        
        # Gerar relatório de transição
        report = self.generate_stage_report(campaign_id, new_stage, 'advanced')
        
        return report
    
    def generate_stage_report(self, campaign_id: int, stage: int, event_type: str) -> Dict:
        """
        Gera relatório curto do estágio atual
        """
        conn = get_db_connection()
        c = conn.cursor()
        
        # Buscar campanha
        c.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
        campaign = c.fetchone()
        
        # Buscar métricas
        c.execute(sql_param('''
            SELECT * FROM campaign_metrics 
            WHERE campaign_id = ? 
            ORDER BY timestamp DESC LIMIT 1
        '''), (campaign_id,))
        metrics = c.fetchone()
        
        # Buscar ajustes recentes
        c.execute(sql_param('''
            SELECT * FROM campaign_adjustments 
            WHERE campaign_id = ? 
            ORDER BY timestamp DESC LIMIT 5
        '''), (campaign_id,))
        recent_adjustments = c.fetchall()
        
        conn.close()
        
        stage_info = self.warming_stages[stage - 1]
        
        report = {
            'campaign_id': campaign_id,
            'campaign_name': campaign[1] if campaign else 'N/A',
            'timestamp': datetime.now().isoformat(),
            'event': event_type,
            'stage': {
                'number': stage,
                'name': stage_info['name'],
                'budget_level': f"{int(stage_info['budget_multiplier'] * 100)}%"
            },
            'metrics': {},
            'adjustments': [],
            'recommendations': [],
            'status': 'healthy'
        }
        
        if metrics:
            impressions = metrics[3] if len(metrics) > 3 else 0
            clicks = metrics[4] if len(metrics) > 4 else 0
            ctr = metrics[5] if len(metrics) > 5 else 0
            cpc = metrics[6] if len(metrics) > 6 else 0
            conversions = metrics[7] if len(metrics) > 7 else 0
            
            report['metrics'] = {
                'impressions': impressions,
                'clicks': clicks,
                'ctr': f"{ctr}%",
                'cpc': f"R$ {cpc:.2f}",
                'conversions': conversions
            }
            
            # Avaliar saúde da campanha
            if ctr < 1.0:
                report['status'] = 'needs_attention'
                report['recommendations'].append('CTR baixo - considere novos criativos')
            
            if impressions < stage_info['min_impressions']:
                report['status'] = 'needs_attention'
                report['recommendations'].append('Poucas impressões - expandir público')
        
        if recent_adjustments:
            report['adjustments'] = [
                {
                    'type': adj[2],
                    'action': adj[3],
                    'reason': adj[4]
                }
                for adj in recent_adjustments
            ]
        
        # Mensagens personalizadas por evento
        if event_type == 'started':
            report['message'] = f"🚀 Campanha iniciada! Estágio 1: Monitoramento inicial (0-2h)"
        elif event_type == 'advanced':
            report['message'] = f"📈 Avançou para Estágio {stage}: {stage_info['name']}"
        elif event_type == 'monitoring':
            report['message'] = f"👀 Monitorando Estágio {stage}: {stage_info['name']}"
        
        return report
    
    def get_campaign_warming_status(self, campaign_id: int) -> Dict:
        """
        Retorna status completo do aquecimento da campanha
        """
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
        campaign = c.fetchone()
        
        if not campaign:
            conn.close()
            return {'success': False, 'error': 'Campanha não encontrada'}
        
        # Buscar histórico de aquecimento
        c.execute(sql_param('''
            SELECT * FROM campaign_warming 
            WHERE campaign_id = ? 
            ORDER BY stage ASC
        '''), (campaign_id,))
        warming_history = c.fetchall()
        
        # Buscar todos os ajustes
        c.execute(sql_param('''
            SELECT * FROM campaign_adjustments 
            WHERE campaign_id = ? 
            ORDER BY timestamp DESC
        '''), (campaign_id,))
        all_adjustments = c.fetchall()
        
        conn.close()
        
        metadata = json.loads(campaign[12]) if campaign[12] else {}
        current_stage = metadata.get('warming_stage', 1)
        
        return {
            'success': True,
            'campaign_id': campaign_id,
            'campaign_name': campaign[1],
            'current_stage': current_stage,
            'stage_name': self.warming_stages[current_stage - 1]['name'],
            'warming_history': [
                {
                    'stage': w[2],
                    'started_at': w[3],
                    'completed_at': w[4],
                    'status': w[5]
                }
                for w in warming_history
            ],
            'total_adjustments': len(all_adjustments),
            'recent_adjustments': [
                {
                    'type': adj[2],
                    'action': adj[3],
                    'reason': adj[4],
                    'timestamp': adj[5]
                }
                for adj in all_adjustments[:10]
            ]
        }
    
    def stop_test(self, campaign_id: int, reason: str = 'manual_stop') -> Dict:
        """
        Para teste de campanha
        """
        conn = get_db_connection()
        c = conn.cursor()
        
        # Atualizar status da campanha
        c.execute('UPDATE campaigns SET status = ? WHERE id = ?', 
                 ('paused', campaign_id))
        
        # Finalizar aquecimento ativo
        c.execute(sql_param('''
            UPDATE campaign_warming 
            SET status = 'stopped', completed_at = ?
            WHERE campaign_id = ? AND status = 'active'
        '''), (datetime.now().isoformat(), campaign_id))
        
        # Registrar motivo
        c.execute(sql_param('''
            INSERT INTO campaign_adjustments 
            (campaign_id, adjustment_type, action, reason, timestamp)
            VALUES (?, ?, ?, ?, ?)
        '''), (
            campaign_id,
            'test',
            'stopped',
            reason,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'campaign_id': campaign_id,
            'message': 'Teste de campanha parado',
            'reason': reason
        }


# Função auxiliar para criar tabelas necessárias
def create_warming_tables():
    """
    Cria tabelas necessárias para aquecimento de campanhas
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # Tabela de aquecimento
    c.execute(sql_param('''
        CREATE TABLE IF NOT EXISTS campaign_warming (
            id SERIAL PRIMARY KEY,
            campaign_id INTEGER NOT NULL,
            stage INTEGER NOT NULL,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    '''))
    
    # Tabela de ajustes
    c.execute(sql_param('''
        CREATE TABLE IF NOT EXISTS campaign_adjustments (
            id SERIAL PRIMARY KEY,
            campaign_id INTEGER NOT NULL,
            adjustment_type TEXT NOT NULL,
            action TEXT NOT NULL,
            reason TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    '''))
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # Criar tabelas
    create_warming_tables()
    print("✅ Tabelas de aquecimento criadas!")

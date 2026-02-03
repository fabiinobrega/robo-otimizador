"""
Sistema de Vendas Real - NEXORA PRIME
Implementa CRM, Lead Scoring, Funil de Vendas e Automação
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres



class SalesSystem:
    """Sistema completo de vendas com CRM e automação"""
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self._init_tables()
    
    def _init_tables(self):
        """Inicializar tabelas do sistema de vendas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Tabela de Leads
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                company TEXT,
                position TEXT,
                industry TEXT,
                budget REAL,
                source TEXT,
                status TEXT DEFAULT 'new',
                score INTEGER DEFAULT 0,
                stage TEXT DEFAULT 'awareness',
                assigned_to INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_contact TIMESTAMP,
                next_follow_up TIMESTAMP,
                notes TEXT,
                metadata TEXT
            )
        ''')
        
        # Tabela de Atividades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                outcome TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        
        # Tabela de Oportunidades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                probability INTEGER DEFAULT 50,
                stage TEXT DEFAULT 'qualification',
                expected_close_date DATE,
                actual_close_date DATE,
                status TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        
        # Tabela de Follow-ups Automáticos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automated_followups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                sequence_step INTEGER DEFAULT 1,
                message_template TEXT,
                scheduled_for TIMESTAMP,
                sent_at TIMESTAMP,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_lead(self, lead_data: Dict) -> Dict:
        """Criar novo lead no CRM"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Calcular score inicial
        score = self._calculate_lead_score(lead_data)
        
        cursor.execute('''
            INSERT INTO leads (
                name, email, phone, company, position, industry,
                budget, source, score, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            lead_data.get('name'),
            lead_data.get('email'),
            lead_data.get('phone'),
            lead_data.get('company'),
            lead_data.get('position'),
            lead_data.get('industry'),
            lead_data.get('budget', 0),
            lead_data.get('source', 'website'),
            score,
            json.dumps(lead_data.get('metadata', {}))
        ))
        
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Criar sequência de follow-up automático
        self._create_followup_sequence(lead_id)
        
        # Classificar lead
        if score >= 80:
            classification = 'Hot Lead'
        elif score >= 60:
            classification = 'Warm Lead'
        else:
            classification = 'Cold Lead'
        
        return {
            'id': lead_id,
            'score': score,
            'classification': classification,
            'status': 'created',
            'message': f'Lead criado com sucesso! Score: {score}/100 ({classification})'
        }
    
    def _calculate_lead_score(self, lead_data: Dict) -> int:
        """Calcular score do lead (0-100)"""
        score = 0
        
        # Orçamento (30 pontos)
        budget = lead_data.get('budget', 0)
        if budget >= 50000:
            score += 30
        elif budget >= 20000:
            score += 20
        elif budget >= 10000:
            score += 10
        
        # Cargo (25 pontos)
        position = lead_data.get('position', '').lower()
        if any(x in position for x in ['ceo', 'diretor', 'founder']):
            score += 25
        elif any(x in position for x in ['gerente', 'manager', 'head']):
            score += 15
        elif any(x in position for x in ['coordenador', 'analista']):
            score += 5
        
        # Empresa (20 pontos)
        company = lead_data.get('company', '')
        if company:
            score += 20
        
        # Indústria (15 pontos)
        industry = lead_data.get('industry', '').lower()
        target_industries = ['tecnologia', 'e-commerce', 'saas', 'varejo']
        if any(x in industry for x in target_industries):
            score += 15
        
        # Fonte (10 pontos)
        source = lead_data.get('source', '').lower()
        if source in ['indicação', 'referral']:
            score += 10
        elif source in ['linkedin', 'google ads']:
            score += 7
        elif source in ['website', 'landing page']:
            score += 5
        
        return min(score, 100)
    
    def _create_followup_sequence(self, lead_id: int):
        """Criar sequência automática de follow-up"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sequência de 5 follow-ups
        sequences = [
            {
                'step': 1,
                'delay_hours': 0,
                'template': 'Olá {name}! Obrigado pelo interesse. Vamos agendar uma conversa?'
            },
            {
                'step': 2,
                'delay_hours': 24,
                'template': 'Oi {name}, vi que você se interessou por {topic}. Posso te ajudar?'
            },
            {
                'step': 3,
                'delay_hours': 72,
                'template': '{name}, preparei uma proposta personalizada para {company}. Quando podemos conversar?'
            },
            {
                'step': 4,
                'delay_hours': 168,  # 1 semana
                'template': 'Última chance! Oferta especial para {company} válida até amanhã.'
            },
            {
                'step': 5,
                'delay_hours': 336,  # 2 semanas
                'template': '{name}, ainda tem interesse? Estou à disposição para ajudar.'
            }
        ]
        
        for seq in sequences:
            scheduled_for = datetime.now() + timedelta(hours=seq['delay_hours'])
            cursor.execute('''
                INSERT INTO automated_followups (
                    lead_id, sequence_step, message_template, scheduled_for
                ) VALUES (?, ?, ?, ?)
            ''', (lead_id, seq['step'], seq['template'], scheduled_for))
        
        conn.commit()
        conn.close()
    
    def get_sales_funnel(self) -> Dict:
        """Obter estatísticas do funil de vendas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Leads por estágio
        cursor.execute('''
            SELECT stage, COUNT(*) as count
            FROM leads
            GROUP BY stage
        ''')
        stages = dict(cursor.fetchall())
        
        # Oportunidades por estágio
        cursor.execute('''
            SELECT stage, COUNT(*) as count, SUM(value) as total_value
            FROM opportunities
            WHERE status = 'open'
            GROUP BY stage
        ''')
        opportunities = {}
        for row in cursor.fetchall():
            opportunities[row[0]] = {
                'count': row[1],
                'value': row[2] or 0
            }
        
        # Taxa de conversão
        cursor.execute('SELECT COUNT(*) FROM leads')
        total_leads = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM opportunities WHERE status = "won"')
        won_deals = cursor.fetchone()[0]
        
        conversion_rate = (won_deals / total_leads * 100) if total_leads > 0 else 0
        
        conn.close()
        
        return {
            'stages': {
                'awareness': stages.get('awareness', 0),
                'interest': stages.get('interest', 0),
                'consideration': stages.get('consideration', 0),
                'decision': stages.get('decision', 0),
                'purchase': stages.get('purchase', 0)
            },
            'opportunities': opportunities,
            'metrics': {
                'total_leads': total_leads,
                'won_deals': won_deals,
                'conversion_rate': round(conversion_rate, 2)
            }
        }
    
    def get_lead_by_id(self, lead_id: int) -> Optional[Dict]:
        """Obter lead por ID"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM leads WHERE id = ?', (lead_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        lead = dict(row)
        
        # Obter atividades
        cursor.execute('''
            SELECT * FROM activities
            WHERE lead_id = ?
            ORDER BY created_at DESC
        ''', (lead_id,))
        lead['activities'] = [dict(r) for r in cursor.fetchall()]
        
        # Obter oportunidades
        cursor.execute('''
            SELECT * FROM opportunities
            WHERE lead_id = ?
            ORDER BY created_at DESC
        ''', (lead_id,))
        lead['opportunities'] = [dict(r) for r in cursor.fetchall()]
        
        conn.close()
        return lead
    
    def update_lead_stage(self, lead_id: int, new_stage: str) -> Dict:
        """Atualizar estágio do lead no funil"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE leads
            SET stage = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_stage, lead_id))
        
        # Registrar atividade
        cursor.execute('''
            INSERT INTO activities (lead_id, type, description)
            VALUES (?, 'stage_change', ?)
        ''', (lead_id, f'Movido para estágio: {new_stage}'))
        
        conn.commit()
        conn.close()
        
        return {'status': 'updated', 'new_stage': new_stage}
    
    def create_opportunity(self, opportunity_data: Dict) -> Dict:
        """Criar nova oportunidade"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO opportunities (
                lead_id, name, value, probability, stage, expected_close_date
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            opportunity_data.get('lead_id'),
            opportunity_data.get('name'),
            opportunity_data.get('value'),
            opportunity_data.get('probability', 50),
            opportunity_data.get('stage', 'qualification'),
            opportunity_data.get('expected_close_date')
        ))
        
        opp_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': opp_id,
            'status': 'created',
            'message': 'Oportunidade criada com sucesso!'
        }
    
    def get_pending_followups(self) -> List[Dict]:
        """Obter follow-ups pendentes"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.*, l.name, l.email, l.company
            FROM automated_followups f
            JOIN leads l ON f.lead_id = l.id
            WHERE f.status = 'pending'
            AND f.scheduled_for <= datetime('now')
            ORDER BY f.scheduled_for ASC
        ''')
        
        followups = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return followups
    
    def mark_followup_sent(self, followup_id: int) -> Dict:
        """Marcar follow-up como enviado"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE automated_followups
            SET status = 'sent', sent_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (followup_id,))
        
        conn.commit()
        conn.close()
        
        return {'status': 'sent'}
    
    def predict_conversion(self, lead_id: int) -> Dict:
        """Prever probabilidade de conversão do lead"""
        lead = self.get_lead_by_id(lead_id)
        
        if not lead:
            return {'error': 'Lead not found'}
        
        # Fatores de conversão
        score = lead['score']
        stage = lead['stage']
        activities_count = len(lead['activities'])
        opportunities_count = len(lead['opportunities'])
        
        # Cálculo de probabilidade
        probability = score  # Base: score do lead
        
        # Ajustes por estágio
        stage_multipliers = {
            'awareness': 0.5,
            'interest': 0.7,
            'consideration': 0.85,
            'decision': 0.95,
            'purchase': 1.0
        }
        probability *= stage_multipliers.get(stage, 0.5)
        
        # Ajuste por engajamento
        if activities_count > 5:
            probability *= 1.2
        elif activities_count > 2:
            probability *= 1.1
        
        # Ajuste por oportunidades
        if opportunities_count > 0:
            probability *= 1.15
        
        # Limitar entre 0-100
        probability = min(max(probability, 0), 100)
        
        # Tempo estimado para conversão
        days_to_convert = int((100 - probability) / 2)  # Quanto menor a prob, mais tempo
        
        # Classificação
        if probability >= 70:
            classification = 'Alta'
        elif probability >= 40:
            classification = 'Média'
        else:
            classification = 'Baixa'
        
        return {
            'lead_id': lead_id,
            'probability': round(probability, 2),
            'classification': classification,
            'days_to_convert': days_to_convert,
            'recommendation': self._get_conversion_recommendation(probability)
        }
    
    def _get_conversion_recommendation(self, probability: float) -> str:
        """Obter recomendação baseada na probabilidade"""
        if probability >= 80:
            return 'Lead quente! Priorize contato imediato e faça proposta.'
        elif probability >= 60:
            return 'Lead morno. Continue nutrição e agende demonstração.'
        elif probability >= 40:
            return 'Lead frio. Envie conteúdo educativo e mantenha contato.'
        else:
            return 'Lead muito frio. Considere remarketing ou pausar follow-up.'
    
    def get_sales_dashboard(self) -> Dict:
        """Obter dados para dashboard de vendas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de leads
        cursor.execute('SELECT COUNT(*) FROM leads')
        total_leads = cursor.fetchone()[0]
        
        # Leads por status
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM leads
            GROUP BY status
        ''')
        leads_by_status = dict(cursor.fetchall())
        
        # Oportunidades abertas
        cursor.execute('''
            SELECT COUNT(*), SUM(value)
            FROM opportunities
            WHERE status = 'open'
        ''')
        open_opps = cursor.fetchone()
        
        # Oportunidades ganhas (este mês)
        cursor.execute('''
            SELECT COUNT(*), SUM(value)
            FROM opportunities
            WHERE status = 'won'
            AND strftime('%Y-%m', actual_close_date) = strftime('%Y-%m', 'now')
        ''')
        won_opps = cursor.fetchone()
        
        # Taxa de conversão
        cursor.execute('SELECT COUNT(*) FROM opportunities WHERE status = "won"')
        total_won = cursor.fetchone()[0]
        conversion_rate = (total_won / total_leads * 100) if total_leads > 0 else 0
        
        # Ticket médio
        cursor.execute('SELECT AVG(value) FROM opportunities WHERE status = "won"')
        avg_ticket = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_leads': total_leads,
            'leads_by_status': leads_by_status,
            'open_opportunities': {
                'count': open_opps[0] or 0,
                'value': open_opps[1] or 0
            },
            'won_this_month': {
                'count': won_opps[0] or 0,
                'value': won_opps[1] or 0
            },
            'metrics': {
                'conversion_rate': round(conversion_rate, 2),
                'average_ticket': round(avg_ticket, 2)
            }
        }


# Exemplo de uso
if __name__ == '__main__':
    sales = SalesSystem()
    
    # Criar lead
    lead = sales.create_lead({
        'name': 'João Silva',
        'email': 'joao@empresa.com',
        'phone': '(11) 99999-9999',
        'company': 'Tech Corp',
        'position': 'CEO',
        'industry': 'Tecnologia',
        'budget': 50000,
        'source': 'LinkedIn'
    })
    print(f"Lead criado: {lead}")
    
    # Obter funil
    funnel = sales.get_sales_funnel()
    print(f"Funil: {funnel}")
    
    # Prever conversão
    prediction = sales.predict_conversion(lead['id'])
    print(f"Previsão: {prediction}")
    
    # Dashboard
    dashboard = sales.get_sales_dashboard()
    print(f"Dashboard: {dashboard}")

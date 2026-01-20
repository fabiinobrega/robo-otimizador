#!/usr/bin/env python3
"""
Script para popular banco de dados do Nexora Prime com dados mockados consistentes
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from database import get_db_connection

def seed_database():
    """Popular banco de dados com dados mockados"""
    
    print("🚀 Iniciando população do banco de dados...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Limpar dados antigos
        print("🗑️  Limpando dados antigos...")
        cursor.execute("DELETE FROM campaign_metrics")
        cursor.execute("DELETE FROM campaigns")
        cursor.execute("DELETE FROM users WHERE email != 'admin@nexora.com'")
        conn.commit()
        print("✅ Dados antigos removidos")
        
        # 2. Criar usuário de teste
        print("👤 Criando usuário de teste...")
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, created_at)
            VALUES ('Usuário Teste', 'teste@nexora.com', 'hashed_password', NOW())
            ON CONFLICT (email) DO NOTHING
        """)
        conn.commit()
        
        # Buscar user_id
        cursor.execute("SELECT id FROM users WHERE email = 'teste@nexora.com'")
        user_id = cursor.fetchone()[0]
        print(f"✅ Usuário criado (ID: {user_id})")
        
        # 3. Criar campanhas mockadas
        print("📊 Criando campanhas mockadas...")
        
        campaigns_data = [
            {
                'name': 'Campanha Black Friday 2024',
                'platform': 'Facebook',
                'status': 'Active',
                'daily_budget': 150.00,
                'total_budget': 4500.00,
                'start_date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
                'end_date': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
                'objective': 'Conversões - Vendas e leads'
            },
            {
                'name': 'Google Ads - Sapatos Esportivos',
                'platform': 'Google',
                'status': 'Active',
                'daily_budget': 100.00,
                'total_budget': 3000.00,
                'start_date': (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
                'end_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
                'objective': 'Tráfego - Visitas ao site'
            },
            {
                'name': 'TikTok - Lançamento Produto',
                'platform': 'TikTok',
                'status': 'Paused',
                'daily_budget': 80.00,
                'total_budget': 2400.00,
                'start_date': (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
                'end_date': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
                'objective': 'Reconhecimento - Alcance'
            },
            {
                'name': 'Pinterest - Decoração Casa',
                'platform': 'Pinterest',
                'status': 'Active',
                'daily_budget': 60.00,
                'total_budget': 1800.00,
                'start_date': (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
                'end_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
                'objective': 'Conversões - Vendas e leads'
            },
            {
                'name': 'LinkedIn - B2B Software',
                'platform': 'LinkedIn',
                'status': 'Draft',
                'daily_budget': 200.00,
                'total_budget': 6000.00,
                'start_date': datetime.now().strftime('%Y-%m-%d'),
                'end_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'objective': 'Geração de Leads - B2B'
            }
        ]
        
        campaign_ids = []
        for campaign in campaigns_data:
            cursor.execute("""
                INSERT INTO campaigns (
                    user_id, name, platform, status, daily_budget, total_budget,
                    start_date, end_date, objective, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id
            """, (
                user_id, campaign['name'], campaign['platform'], campaign['status'],
                campaign['daily_budget'], campaign['total_budget'], campaign['start_date'],
                campaign['end_date'], campaign['objective']
            ))
            campaign_id = cursor.fetchone()[0]
            campaign_ids.append((campaign_id, campaign['status']))
            print(f"  ✅ {campaign['name']} (ID: {campaign_id})")
        
        conn.commit()
        print(f"✅ {len(campaigns_data)} campanhas criadas")
        
        # 4. Criar métricas para campanhas ativas
        print("📈 Criando métricas para campanhas ativas...")
        
        metrics_count = 0
        for campaign_id, status in campaign_ids:
            if status == 'Active':
                # Gerar métricas dos últimos 7 dias
                for days_ago in range(7):
                    date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
                    
                    impressions = random.randint(5000, 15000)
                    clicks = random.randint(100, 500)
                    conversions = random.randint(10, 50)
                    spend = random.uniform(80, 150)
                    revenue = spend * random.uniform(1.5, 3.5)
                    
                    cursor.execute("""
                        INSERT INTO campaign_metrics (
                            campaign_id, date, impressions, clicks, conversions,
                            spend, revenue, created_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                    """, (
                        campaign_id, date, impressions, clicks, conversions,
                        spend, revenue
                    ))
                    metrics_count += 1
        
        conn.commit()
        print(f"✅ {metrics_count} métricas criadas")
        
        # 5. Verificar dados
        print("\n📊 Verificando dados inseridos...")
        
        cursor.execute("SELECT COUNT(*) FROM campaigns")
        total_campaigns = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM campaigns WHERE status = 'Active'")
        active_campaigns = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM campaign_metrics")
        total_metrics = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(spend) FROM campaign_metrics")
        total_spend = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(revenue) FROM campaign_metrics")
        total_revenue = cursor.fetchone()[0] or 0
        
        print(f"  📊 Total de Campanhas: {total_campaigns}")
        print(f"  ✅ Campanhas Ativas: {active_campaigns}")
        print(f"  📈 Total de Métricas: {total_metrics}")
        print(f"  💰 Investimento Total: R$ {total_spend:.2f}")
        print(f"  💵 Receita Total: R$ {total_revenue:.2f}")
        print(f"  📊 ROAS: {(total_revenue / total_spend if total_spend > 0 else 0):.2f}x")
        
        print("\n🎉 Banco de dados populado com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro ao popular banco de dados: {str(e)}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_database()

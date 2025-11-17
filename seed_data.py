"""
Seed Data - Popular banco de dados com dados de exemplo
"""
import sqlite3
import json
from datetime import datetime, timedelta
import random


def seed_database(db_path='database.db'):
    """Popular banco de dados com dados de exemplo"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🌱 Iniciando seed do banco de dados...")
    
    # 1. Criar campanhas de exemplo
    campaigns = [
        {
            'name': 'Campanha Black Friday 2024',
            'platform': 'Facebook',
            'status': 'Active',
            'budget': 500.00,
            'start_date': (datetime.now() - timedelta(days=5)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=25)).isoformat(),
            'objective': 'Conversões',
            'product_url': 'https://exemplo.com/produto1'
        },
        {
            'name': 'Google Ads - Sapatos Esportivos',
            'platform': 'Google',
            'status': 'Active',
            'budget': 300.00,
            'start_date': (datetime.now() - timedelta(days=10)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=20)).isoformat(),
            'objective': 'Tráfego',
            'product_url': 'https://exemplo.com/sapatos'
        },
        {
            'name': 'TikTok - Lançamento Produto',
            'platform': 'TikTok',
            'status': 'Paused',
            'budget': 200.00,
            'start_date': (datetime.now() - timedelta(days=3)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=27)).isoformat(),
            'objective': 'Reconhecimento',
            'product_url': 'https://exemplo.com/lancamento'
        },
        {
            'name': 'Pinterest - Decoração Casa',
            'platform': 'Pinterest',
            'status': 'Active',
            'budget': 150.00,
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=30)).isoformat(),
            'objective': 'Tráfego',
            'product_url': 'https://exemplo.com/decoracao'
        },
        {
            'name': 'LinkedIn - B2B Software',
            'platform': 'LinkedIn',
            'status': 'Draft',
            'budget': 1000.00,
            'start_date': (datetime.now() + timedelta(days=5)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=35)).isoformat(),
            'objective': 'Leads',
            'product_url': 'https://exemplo.com/software'
        }
    ]
    
    campaign_ids = []
    for campaign in campaigns:
        cursor.execute("""
            INSERT INTO campaigns (name, platform, status, budget, start_date, end_date, objective, product_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            campaign['name'],
            campaign['platform'],
            campaign['status'],
            campaign['budget'],
            campaign['start_date'],
            campaign['end_date'],
            campaign['objective'],
            campaign['product_url'],
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        campaign_ids.append(cursor.lastrowid)
    
    print(f"✅ {len(campaigns)} campanhas criadas")
    
    # 2. Adicionar métricas para campanhas ativas
    for campaign_id in campaign_ids[:4]:  # Apenas para as 4 primeiras
        impressions = random.randint(5000, 50000)
        clicks = int(impressions * random.uniform(0.01, 0.05))
        conversions = int(clicks * random.uniform(0.02, 0.10))
        spend = random.uniform(50, 400)
        revenue = spend * random.uniform(1.5, 4.0)
        
        cursor.execute("""
            INSERT INTO campaign_metrics (campaign_id, impressions, clicks, conversions, spend, revenue, ctr, cpc, cpa, roas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            campaign_id,
            impressions,
            clicks,
            conversions,
            spend,
            revenue,
            round((clicks / impressions * 100), 2),
            round((spend / clicks), 2) if clicks > 0 else 0,
            round((spend / conversions), 2) if conversions > 0 else 0,
            round((revenue / spend), 2) if spend > 0 else 0,
        ))
    
    print(f"✅ Métricas adicionadas para campanhas ativas")
    
    # 3. Adicionar logs de atividade
    activities = [
        ('Campanha Criada', 'Campanha Black Friday 2024 criada com sucesso'),
        ('Otimização Automática', 'Budget da campanha Google Ads aumentado em 15%'),
        ('[Velyra Prime] Monitoramento', '5 campanhas monitoradas, 0 problemas detectados'),
        ('Upload de Mídia', 'Imagem banner_black_friday.jpg enviada'),
        ('[Automação] Campanha Pausada', 'Campanha TikTok pausada por baixo ROAS'),
        ('Teste A/B Criado', 'Teste de título criado com 3 variações'),
        ('[Velyra Prime] Otimização', 'Campanha Pinterest otimizada automaticamente'),
        ('Relatório Gerado', 'Relatório semanal de performance gerado'),
    ]
    
    for i, (action, details) in enumerate(activities):
        timestamp = (datetime.now() - timedelta(hours=i*2)).isoformat()
        cursor.execute("""
            INSERT INTO activity_logs (timestamp, action, details)
            VALUES (?, ?, ?)
        """, (timestamp, action, details))
    
    print(f"✅ {len(activities)} logs de atividade criados")
    
    # 4. Adicionar arquivos de mídia de exemplo
    media_files = [
        ('banner_black_friday.jpg', '/static/uploads/banner_black_friday.jpg', 'image'),
        ('video_produto.mp4', '/static/uploads/video_produto.mp4', 'video'),
        ('logo_marca.png', '/static/uploads/logo_marca.png', 'image'),
    ]
    
    for filename, url, filetype in media_files:
        cursor.execute("""
            INSERT INTO media_files (filename, url, filetype, uploaded_at)
            VALUES (?, ?, ?, ?)
        """, (filename, url, filetype, datetime.now().isoformat()))
    
    print(f"✅ {len(media_files)} arquivos de mídia adicionados")
    
    # 5. Criar regras de automação
    rules = [
        {
            'name': 'Auto-Pausar Campanhas de Baixo Desempenho',
            'rule_type': 'auto_pause_low_performance',
            'conditions': json.dumps({'roas': '<1.0', 'spend': '>50'}),
            'actions': json.dumps({'action': 'pause_campaign'}),
            'is_active': True
        },
        {
            'name': 'Aumentar Budget de Campanhas Performando Bem',
            'rule_type': 'auto_increase_budget',
            'conditions': json.dumps({'roas': '>3.0', 'conversions': '>10'}),
            'actions': json.dumps({'action': 'increase_budget', 'percentage': 15}),
            'is_active': True
        }
    ]
    
    for rule in rules:
        cursor.execute("""
            INSERT INTO automation_rules (name, rule_type, conditions, actions, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            rule['name'],
            rule['rule_type'],
            rule['conditions'],
            rule['actions'],
            rule['is_active'],
            datetime.now().isoformat()
        ))
    
    print(f"✅ {len(rules)} regras de automação criadas")
    
    # 6. Adicionar notificações
    notifications = [
        {
            'title': 'Campanha Otimizada',
            'message': 'O Velyra Prime otimizou sua campanha do Google Ads',
            'type': 'success',
            'is_read': False
        },
        {
            'title': 'Alerta de Orçamento',
            'message': 'Campanha Black Friday já gastou 80% do orçamento',
            'type': 'warning',
            'is_read': False
        },
        {
            'title': 'Novo Relatório Disponível',
            'message': 'Relatório semanal de performance está pronto',
            'type': 'info',
            'is_read': True
        }
    ]
    
    for notif in notifications:
        cursor.execute("""
            INSERT INTO notifications (title, message, type, is_read, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            notif['title'],
            notif['message'],
            notif['type'],
            notif['is_read'],
            datetime.now().isoformat()
        ))
    
    print(f"✅ {len(notifications)} notificações criadas")
    
    # 7. Configurar status do Velyra Prime
    cursor.execute("""
        INSERT INTO operator_status (status, last_check, health_data, updated_at)
        VALUES (?, ?, ?, ?)
    """, (
        'active',
        datetime.now().isoformat(),
        json.dumps({
            'database': 'ok',
            'openai_api': 'configured',
            'campaigns_monitored': len(campaign_ids),
            'last_optimization': datetime.now().isoformat()
        }),
        datetime.now().isoformat()
    ))
    
    print(f"✅ Status do Velyra Prime configurado")
    
    # 8. Adicionar chaves de API (vazias para o usuário configurar)
    api_services = ['OpenAI', 'Facebook Ads', 'Google Ads', 'TikTok Ads', 'Pinterest Ads', 'LinkedIn Ads']
    for service in api_services:
        cursor.execute("""
            INSERT INTO api_keys (service_name, api_key, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (service, '', False, datetime.now().isoformat(), datetime.now().isoformat()))
    
    print(f"✅ {len(api_services)} serviços de API configurados")
    
    conn.commit()
    conn.close()
    
    print("✅ Seed concluído com sucesso!")
    print(f"\n📊 Resumo:")
    print(f"   - {len(campaigns)} campanhas")
    print(f"   - {len(activities)} logs de atividade")
    print(f"   - {len(media_files)} arquivos de mídia")
    print(f"   - {len(rules)} regras de automação")
    print(f"   - {len(notifications)} notificações")
    print(f"   - {len(api_services)} integrações de API")


if __name__ == '__main__':
    seed_database()

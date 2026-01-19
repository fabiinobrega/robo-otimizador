-- Seed Data para NEXORA PRIME
-- Dados realistas para testes

-- Inserir campanhas com dados realistas
INSERT INTO campaigns (name, platform, status, budget, objective, product_url, created_at) VALUES
('Black Friday 2024', 'Facebook', 'Active', 2500.00, 'Conversões', 'https://exemplo.com/black-friday', datetime('now', '-15 days')),
('Remarketing Q4', 'Google', 'Active', 1800.00, 'Remarketing', 'https://exemplo.com/remarketing', datetime('now', '-10 days')),
('Lançamento Produto X', 'Instagram', 'Active', 3200.00, 'Awareness', 'https://exemplo.com/produto-x', datetime('now', '-7 days')),
('Google Ads - Sapatos Esportivos', 'Google', 'Active', 1500.00, 'Conversões', 'https://exemplo.com/sapatos', datetime('now', '-5 days')),
('TikTok - Lançamento Produto', 'TikTok', 'Paused', 800.00, 'Engagement', 'https://exemplo.com/tiktok', datetime('now', '-3 days')),
('Pinterest - Decoração Casa', 'Pinterest', 'Active', 1200.00, 'Traffic', 'https://exemplo.com/decoracao', datetime('now', '-2 days')),
('LinkedIn - B2B Software', 'LinkedIn', 'Draft', 0.00, 'Leads', 'https://exemplo.com/b2b', datetime('now', '-1 day'));

-- Inserir métricas realistas para as campanhas
INSERT INTO campaign_metrics (campaign_id, impressions, clicks, conversions, spend, revenue, ctr, cpc, cpa, roas) VALUES
(1, 125000, 3800, 156, 2450.00, 9800.00, 3.04, 0.64, 15.71, 4.00),
(2, 98000, 2950, 180, 1750.00, 7200.00, 3.01, 0.59, 9.72, 4.11),
(3, 156000, 4200, 245, 3150.00, 11500.00, 2.69, 0.75, 12.86, 3.65),
(4, 87000, 2100, 98, 1480.00, 5650.00, 2.41, 0.70, 15.10, 3.82),
(5, 45000, 1200, 45, 750.00, 1720.00, 2.67, 0.63, 16.67, 2.29),
(6, 62000, 1850, 112, 1150.00, 3080.00, 2.98, 0.62, 10.27, 2.68),
(7, 0, 0, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00);

-- Inserir logs de atividade
INSERT INTO activity_logs (action, details, timestamp) VALUES
('campaign_created', 'Campanha "Black Friday 2024" criada', datetime('now', '-15 days')),
('campaign_published', 'Campanha "Black Friday 2024" publicada no Facebook', datetime('now', '-15 days', '+2 hours')),
('campaign_optimized', 'Velyra Prime otimizou lances da campanha "Black Friday 2024"', datetime('now', '-12 minutes')),
('campaign_created', 'Campanha "Remarketing Q4" criada', datetime('now', '-10 days')),
('campaign_published', 'Campanha "Remarketing Q4" publicada no Google Ads', datetime('now', '-10 days', '+1 hour')),
('campaign_created', 'Campanha "Lançamento Produto X" criada', datetime('now', '-7 days')),
('campaign_paused', 'Campanha "TikTok - Lançamento Produto" pausada automaticamente (ROAS < 2.5)', datetime('now', '-1 day')),
('campaign_scaled', 'Velyra Prime aumentou orçamento da campanha "Black Friday 2024" em 15%', datetime('now', '-5 hours'));

-- Inserir notificações
INSERT INTO notifications (title, message, type, is_read, campaign_id) VALUES
('🎉 Campanha com alto desempenho!', 'A campanha "Black Friday 2024" está com ROAS de 4.00x', 'success', 0, 1),
('⚠️ Campanha pausada', 'A campanha "TikTok - Lançamento Produto" foi pausada automaticamente devido a baixo ROAS', 'warning', 0, 5),
('📈 Orçamento aumentado', 'Velyra Prime aumentou o orçamento da campanha "Remarketing Q4" em 10%', 'info', 1, 2),
('✅ Otimização concluída', 'Velyra Prime otimizou 47 campanhas hoje', 'success', 1, NULL);

-- Inserir API keys (sem valores reais)
INSERT INTO api_keys (service_name, api_key, is_active, last_tested) VALUES
('meta_ads', NULL, 0, NULL),
('google_ads', NULL, 0, NULL),
('openai', NULL, 0, NULL),
('similarweb', NULL, 0, NULL);

-- Inserir status do operador
INSERT INTO operator_status (status, health_data) VALUES
('active', '{"cpu": 45, "memory": 62, "uptime": "15d 7h 23m"}');

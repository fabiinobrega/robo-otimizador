-- Script para corrigir dados inconsistentes entre Dashboard e Campanhas
-- Garante que os dados mockados sejam consistentes

-- Limpar dados antigos
DELETE FROM campaigns WHERE id IN (1, 2, 3, 4, 5);

-- Inserir campanhas mockadas consistentes
INSERT INTO campaigns (id, name, platform, status, budget, start_date, end_date, created_at, updated_at) VALUES
(1, 'Campanha LinkedIn B2B', 'LinkedIn', 'Active', 500.00, '2024-11-01', '2024-11-30', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Campanha Pinterest Produtos', 'Pinterest', 'Active', 300.00, '2024-11-01', '2024-11-30', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Campanha TikTok Viral', 'TikTok', 'Active', 400.00, '2024-11-01', '2024-11-30', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 'Campanha Google Search', 'Google', 'Paused', 200.00, '2024-10-15', '2024-10-31', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 'Campanha Facebook Retargeting', 'Facebook', 'Paused', 150.00, '2024-10-01', '2024-10-31', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Inserir métricas mockadas para as campanhas ativas
INSERT INTO campaign_metrics (campaign_id, date, impressions, clicks, ctr, cpc, conversions, cost, created_at) VALUES
-- Campanha 1 (LinkedIn)
(1, '2024-11-15', 5000, 250, 5.0, 2.00, 25, 500.00, CURRENT_TIMESTAMP),
-- Campanha 2 (Pinterest)
(2, '2024-11-15', 8000, 320, 4.0, 0.94, 32, 300.00, CURRENT_TIMESTAMP),
-- Campanha 3 (TikTok)
(3, '2024-11-15', 12000, 480, 4.0, 0.83, 48, 400.00, CURRENT_TIMESTAMP);

-- Verificar dados inseridos
SELECT 'Campanhas Ativas:' as info, COUNT(*) as count FROM campaigns WHERE status = 'Active';
SELECT 'Campanhas Pausadas:' as info, COUNT(*) as count FROM campaigns WHERE status = 'Paused';
SELECT 'Total de Campanhas:' as info, COUNT(*) as count FROM campaigns;

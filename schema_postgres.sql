-- Main Campaigns Table
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    platform TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Draft',
    budget REAL NOT NULL,
    start_date TEXT,
    end_date TEXT,
    objective TEXT,
    product_url TEXT,
    meta_campaign_id TEXT,
    google_campaign_id TEXT,
    last_publish_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaign Creatives (Images, Videos, Headlines, Descriptions)
CREATE TABLE IF NOT EXISTS campaign_creatives (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    asset_url TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Keywords (Google Ads)
CREATE TABLE IF NOT EXISTS campaign_keywords (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    match_type TEXT DEFAULT 'broad',
    source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Audiences (Meta Ads)
CREATE TABLE IF NOT EXISTS campaign_audiences (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    audience_type TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Segmentation (Advanced Targeting)
CREATE TABLE IF NOT EXISTS campaign_segmentation (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    target_country TEXT,
    target_cities TEXT,
    min_age INTEGER,
    max_age INTEGER,
    interests TEXT,
    keywords TEXT,
    exclude_audiences TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Budget Optimization
CREATE TABLE IF NOT EXISTS campaign_budget_config (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    is_daily_budget BOOLEAN DEFAULT 1,
    bid_strategy TEXT DEFAULT 'maximize_conversions',
    budget_optimization TEXT DEFAULT 'campaign',
    ad_rotation TEXT DEFAULT 'optimize',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Copy & Headlines
CREATE TABLE IF NOT EXISTS campaign_copy (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    headline_1 TEXT,
    headline_2 TEXT,
    description_1 TEXT,
    call_to_action TEXT,
    copy_sentiment TEXT DEFAULT 'neutral',
    negative_keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Media Files (Uploads)
CREATE TABLE IF NOT EXISTS media_files (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    url TEXT NOT NULL,
    filetype TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activity Logs
CREATE TABLE IF NOT EXISTS activity_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action TEXT NOT NULL,
    details TEXT
);

-- AI Analysis Results (Cache)
CREATE TABLE IF NOT EXISTS ai_analyses (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER,
    analysis_type TEXT,
    result_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Competitor Analysis Cache
CREATE TABLE IF NOT EXISTS competitor_analyses (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL,
    analysis_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaign Performance Metrics
CREATE TABLE IF NOT EXISTS campaign_metrics (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    spend REAL DEFAULT 0,
    revenue REAL DEFAULT 0,
    ctr REAL DEFAULT 0,
    cpc REAL DEFAULT 0,
    cpa REAL DEFAULT 0,
    roas REAL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- A/B Testing
CREATE TABLE IF NOT EXISTS ab_tests (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    test_name TEXT NOT NULL,
    test_type TEXT NOT NULL,
    status TEXT DEFAULT 'running',
    winner_variation_id INTEGER,
    confidence_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- A/B Test Variations
CREATE TABLE IF NOT EXISTS ab_test_variations (
    id SERIAL PRIMARY KEY,
    test_id INTEGER NOT NULL,
    variation_name TEXT NOT NULL,
    content_json TEXT NOT NULL,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES ab_tests (id) ON DELETE CASCADE
);

-- Automation Rules
CREATE TABLE IF NOT EXISTS automation_rules (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    conditions TEXT,
    actions TEXT,
    is_active BOOLEAN DEFAULT 1,
    last_executed TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automation Rule Executions
CREATE TABLE IF NOT EXISTS automation_executions (
    id SERIAL PRIMARY KEY,
    rule_id INTEGER NOT NULL,
    campaign_id INTEGER,
    action_taken TEXT,
    result TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rule_id) REFERENCES automation_rules (id) ON DELETE CASCADE,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info',
    is_read BOOLEAN DEFAULT 0,
    campaign_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Reports
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    report_name TEXT NOT NULL,
    report_type TEXT NOT NULL,
    date_range_start TEXT,
    date_range_end TEXT,
    data_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API Keys and Integrations
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    service_name TEXT NOT NULL UNIQUE,
    api_key TEXT,
    is_active BOOLEAN DEFAULT 1,
    last_tested TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Manus Operator Status
CREATE TABLE IF NOT EXISTS operator_status (
    id SERIAL PRIMARY KEY,
    status TEXT DEFAULT 'active',
    last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    health_data TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Messages (Manus Operator)
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    sender TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_platform ON campaigns(platform);
CREATE INDEX IF NOT EXISTS idx_campaign_creatives_campaign_id ON campaign_creatives(campaign_id);
CREATE INDEX IF NOT EXISTS idx_campaign_keywords_campaign_id ON campaign_keywords(campaign_id);
CREATE INDEX IF NOT EXISTS idx_campaign_audiences_campaign_id ON campaign_audiences(campaign_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON activity_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_media_files_uploaded_at ON media_files(uploaded_at);
CREATE INDEX IF NOT EXISTS idx_ab_tests_campaign_id ON ab_tests(campaign_id);
CREATE INDEX IF NOT EXISTS idx_automation_rules_active ON automation_rules(is_active);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(is_read);


-- Tabela para histórico de aprendizado da IA
CREATE TABLE IF NOT EXISTS ai_learning_history (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER,
    timestamp TEXT NOT NULL,
    results TEXT,
    patterns TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para modelos treinados
CREATE TABLE IF NOT EXISTS ai_models (
    id SERIAL PRIMARY KEY,
    model_name TEXT NOT NULL,
    version TEXT NOT NULL,
    metrics TEXT,
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active'
);

-- Tabela para experimentos A/B
CREATE TABLE IF NOT EXISTS ab_experiments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    variants TEXT,
    results TEXT,
    winner_id INTEGER,
    status TEXT DEFAULT 'running',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== TABELAS DE INTEGRAÇÃO COM API MANUS =====

-- Tokens de autenticação OAuth2
CREATE TABLE IF NOT EXISTS manus_api_tokens (
    id INTEGER PRIMARY KEY,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Estados OAuth para validação CSRF
CREATE TABLE IF NOT EXISTS oauth_states (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);

-- Logs de sincronização
CREATE TABLE IF NOT EXISTS manus_sync_logs (
    id SERIAL PRIMARY KEY,
    sync_type TEXT NOT NULL,
    pushed INTEGER DEFAULT 0,
    pulled INTEGER DEFAULT 0,
    errors TEXT,
    synced_at TEXT NOT NULL
);

-- Webhooks registrados
CREATE TABLE IF NOT EXISTS manus_webhooks (
    id SERIAL PRIMARY KEY,
    event TEXT NOT NULL,
    url TEXT NOT NULL,
    webhook_id TEXT,
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Adicionar coluna de sincronização nas campanhas existentes (removido IF NOT EXISTS para compatibilidade)
-- ALTER TABLE campaigns ADD COLUMN synced_with_manus INTEGER DEFAULT 0;
-- ALTER TABLE campaigns ADD COLUMN manus_id TEXT;
-- ALTER TABLE campaigns ADD COLUMN last_synced_at TEXT;


-- ===== TABELA DE AUTOMAÇÕES NEXORA =====

-- Tabela principal de automações
CREATE TABLE IF NOT EXISTS automations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    config TEXT,
    schedule TEXT,
    status TEXT DEFAULT 'active',
    last_run TEXT,
    next_run TEXT,
    run_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para busca por status
CREATE INDEX IF NOT EXISTS idx_automations_status ON automations(status);
CREATE INDEX IF NOT EXISTS idx_automations_type ON automations(type);



-- ===== TABELA DE SERVIÇOS DE API =====

-- Tabela para armazenar integrações com serviços externos
CREATE TABLE IF NOT EXISTS api_services (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    api_key TEXT,
    api_secret TEXT,
    endpoint_url TEXT,
    status TEXT DEFAULT 'inactive',
    is_connected BOOLEAN DEFAULT 0,
    last_sync TEXT,
    config_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para busca por status
CREATE INDEX IF NOT EXISTS idx_api_services_status ON api_services(status);
CREATE INDEX IF NOT EXISTS idx_api_services_name ON api_services(name);

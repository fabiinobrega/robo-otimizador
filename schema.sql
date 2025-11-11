-- Main Campaigns Table
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Campaign Creatives (Images, Videos, Headlines, Descriptions)
CREATE TABLE IF NOT EXISTS campaign_creatives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    asset_url TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Keywords (Google Ads)
CREATE TABLE IF NOT EXISTS campaign_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    match_type TEXT DEFAULT 'broad',
    source TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Audiences (Meta Ads)
CREATE TABLE IF NOT EXISTS campaign_audiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    audience_type TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Segmentation (Advanced Targeting)
CREATE TABLE IF NOT EXISTS campaign_segmentation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    target_country TEXT,
    target_cities TEXT,
    min_age INTEGER,
    max_age INTEGER,
    interests TEXT,
    keywords TEXT,
    exclude_audiences TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Budget Optimization
CREATE TABLE IF NOT EXISTS campaign_budget_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    is_daily_budget BOOLEAN DEFAULT 1,
    bid_strategy TEXT DEFAULT 'maximize_conversions',
    budget_optimization TEXT DEFAULT 'campaign',
    ad_rotation TEXT DEFAULT 'optimize',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Campaign Copy & Headlines
CREATE TABLE IF NOT EXISTS campaign_copy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    headline_1 TEXT,
    headline_2 TEXT,
    description_1 TEXT,
    call_to_action TEXT,
    copy_sentiment TEXT DEFAULT 'neutral',
    negative_keywords TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Media Files (Uploads)
CREATE TABLE IF NOT EXISTS media_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    url TEXT NOT NULL,
    filetype TEXT NOT NULL,
    uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Activity Logs
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    action TEXT NOT NULL,
    details TEXT
);

-- AI Analysis Results (Cache)
CREATE TABLE IF NOT EXISTS ai_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    analysis_type TEXT,
    result_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Competitor Analysis Cache
CREATE TABLE IF NOT EXISTS competitor_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    analysis_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Campaign Performance Metrics
CREATE TABLE IF NOT EXISTS campaign_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- A/B Testing
CREATE TABLE IF NOT EXISTS ab_tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    test_name TEXT NOT NULL,
    test_type TEXT NOT NULL,
    status TEXT DEFAULT 'running',
    winner_variation_id INTEGER,
    confidence_level TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- A/B Test Variations
CREATE TABLE IF NOT EXISTS ab_test_variations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    variation_name TEXT NOT NULL,
    content_json TEXT NOT NULL,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES ab_tests (id) ON DELETE CASCADE
);

-- Automation Rules
CREATE TABLE IF NOT EXISTS automation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    conditions TEXT,
    actions TEXT,
    is_active BOOLEAN DEFAULT 1,
    last_executed TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Automation Rule Executions
CREATE TABLE IF NOT EXISTS automation_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id INTEGER NOT NULL,
    campaign_id INTEGER,
    action_taken TEXT,
    result TEXT,
    executed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rule_id) REFERENCES automation_rules (id) ON DELETE CASCADE,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info',
    is_read BOOLEAN DEFAULT 0,
    campaign_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE
);

-- Reports
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_name TEXT NOT NULL,
    report_type TEXT NOT NULL,
    date_range_start TEXT,
    date_range_end TEXT,
    data_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- API Keys and Integrations
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL UNIQUE,
    api_key TEXT,
    is_active BOOLEAN DEFAULT 1,
    last_tested TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Manus Operator Status
CREATE TABLE IF NOT EXISTS operator_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT DEFAULT 'active',
    last_check TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    health_data TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Chat Messages (Manus Operator)
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    timestamp TEXT NOT NULL,
    results TEXT,
    patterns TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para modelos treinados
CREATE TABLE IF NOT EXISTS ai_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    version TEXT NOT NULL,
    metrics TEXT,
    trained_at TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active'
);

-- Tabela para experimentos A/B
CREATE TABLE IF NOT EXISTS ab_experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    variants TEXT,
    results TEXT,
    winner_id INTEGER,
    status TEXT DEFAULT 'running',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

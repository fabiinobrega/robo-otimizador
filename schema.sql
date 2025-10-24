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

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_platform ON campaigns(platform);
CREATE INDEX IF NOT EXISTS idx_campaign_creatives_campaign_id ON campaign_creatives(campaign_id);
CREATE INDEX IF NOT EXISTS idx_campaign_keywords_campaign_id ON campaign_keywords(campaign_id);
CREATE INDEX IF NOT EXISTS idx_campaign_audiences_campaign_id ON campaign_audiences(campaign_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON activity_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_media_files_uploaded_at ON media_files(uploaded_at);


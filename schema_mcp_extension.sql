-- ═══════════════════════════════════════════════════════════════════════════════
-- EXTENSÃO DO SCHEMA PARA INTEGRAÇÃO MCP (Model Context Protocol)
-- Adiciona tabelas para comunicação bidirecional Manus ↔ Nexora
-- ═══════════════════════════════════════════════════════════════════════════════

-- Tabela de comandos MCP
CREATE TABLE IF NOT EXISTS mcp_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT NOT NULL,
    params TEXT,  -- JSON
    status TEXT DEFAULT 'pending',  -- pending, executing, completed, failed
    result TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_at TIMESTAMP,
    created_by TEXT DEFAULT 'manus_ai'
);

-- Tabela de eventos MCP
CREATE TABLE IF NOT EXISTS mcp_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    data TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed INTEGER DEFAULT 0
);

-- Tabela de webhooks
CREATE TABLE IF NOT EXISTS webhooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,  -- campaign_created, campaign_updated, etc
    url TEXT NOT NULL,
    secret TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_triggered TIMESTAMP
);

-- Tabela de telemetria
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric TEXT NOT NULL,
    value TEXT,
    tags TEXT,  -- JSON
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de logs de sincronização
CREATE TABLE IF NOT EXISTS sync_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_type TEXT NOT NULL,  -- campaigns, ads, reports
    direction TEXT NOT NULL,  -- push, pull, both
    items_pushed INTEGER DEFAULT 0,
    items_pulled INTEGER DEFAULT 0,
    errors TEXT,  -- JSON array
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status TEXT DEFAULT 'pending'  -- pending, running, completed, failed
);

-- Tabela de autorizações de gastos
CREATE TABLE IF NOT EXISTS spend_authorizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    action TEXT NOT NULL,  -- create_campaign, increase_budget, etc
    amount REAL,
    currency TEXT DEFAULT 'BRL',
    status TEXT DEFAULT 'pending',  -- pending, approved, rejected
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP,
    requested_by TEXT DEFAULT 'manus_ai',
    response_by TEXT,
    notes TEXT,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Tabela de sessões de controle remoto
CREATE TABLE IF NOT EXISTS remote_control_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_token TEXT UNIQUE NOT NULL,
    controller TEXT NOT NULL,  -- manus_ai, user, etc
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    commands_executed INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active'  -- active, ended, expired
);

-- Tabela de auditoria de ações
CREATE TABLE IF NOT EXISTS action_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    entity_type TEXT,  -- campaign, ad, budget, etc
    entity_id INTEGER,
    old_value TEXT,  -- JSON
    new_value TEXT,  -- JSON
    performed_by TEXT,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_mcp_commands_status ON mcp_commands(status);
CREATE INDEX IF NOT EXISTS idx_mcp_commands_created_at ON mcp_commands(created_at);
CREATE INDEX IF NOT EXISTS idx_mcp_events_type ON mcp_events(event_type);
CREATE INDEX IF NOT EXISTS idx_mcp_events_processed ON mcp_events(processed);
CREATE INDEX IF NOT EXISTS idx_webhooks_event ON webhooks(event);
CREATE INDEX IF NOT EXISTS idx_webhooks_active ON webhooks(active);
CREATE INDEX IF NOT EXISTS idx_telemetry_metric ON telemetry(metric);
CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp ON telemetry(timestamp);
CREATE INDEX IF NOT EXISTS idx_spend_auth_status ON spend_authorizations(status);
CREATE INDEX IF NOT EXISTS idx_spend_auth_campaign ON spend_authorizations(campaign_id);
CREATE INDEX IF NOT EXISTS idx_remote_sessions_status ON remote_control_sessions(status);
CREATE INDEX IF NOT EXISTS idx_action_audit_entity ON action_audit(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_action_audit_performed_at ON action_audit(performed_at);

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIM DA EXTENSÃO MCP
-- ═══════════════════════════════════════════════════════════════════════════════

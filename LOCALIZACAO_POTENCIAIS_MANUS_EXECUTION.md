# LOCALIZAÇÃO DE POTENCIAIS MANUS EXECUTION

## Áreas de Execução para Manus

### Execução de Campanhas (Prioridade: ALTA)

**Descrição:** Aplicar campanhas no Google Ads e Facebook Ads

**Rotas Relacionadas:** 2

- `POST /api/campaign/publish` → `api_campaign_publish()`
- `POST /api/ad/publish` → `api_ad_publish()`

### Sincronização de Dados (Prioridade: ALTA)

**Descrição:** Sincronizar dados entre Nexora e plataformas externas

**Rotas Relacionadas:** 2

- `'POST' /api/manus/sync/campaigns` → `api_manus_sync_campaigns()`
- `'POST' /api/manus/sync/ads` → `api_manus_sync_ads()`

### Automação (Prioridade: MÉDIA)

**Descrição:** Executar automações e rotinas

**Rotas Relacionadas:** 11

- `GET /automation` → `automation()`
- `GET /api/automation/rules` → `api_automation_rules()`
- `POST /api/automation/execute` → `api_automation_execute()`
- `GET /api/automation/history` → `api_automation_history()`
- `POST /api/automation/authorize/request` → `api_automation_authorize_request()`

### Manipulação de Estrutura (Prioridade: ALTA)

**Descrição:** Criar/editar arquivos, APIs e banco de dados

**Rotas Relacionadas:** 0



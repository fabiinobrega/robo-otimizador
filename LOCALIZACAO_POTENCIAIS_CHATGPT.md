# LOCALIZAÇÃO DE POTENCIAIS CHATGPT

## Áreas Estratégicas para ChatGPT

### Copywriting (Prioridade: ALTA)

**Descrição:** Geração de headlines, descrições e copy de anúncios

**Rotas Relacionadas:** 14

- `POST /api/dco/generate-segmentation` → `api_dco_generate_segmentation()`
- `POST /api/dco/generate` → `api_dco_generate()`
- `POST /api/dco/generate-copy` → `api_dco_generate_copy()`
- `POST /api/reports/generate` → `api_report_generate()`
- `GET /generate-perfect-ad` → `generate_perfect_ad()`

### Estratégia de Campanhas (Prioridade: ALTA)

**Descrição:** Criação de estratégias de marketing e planejamento

**Rotas Relacionadas:** 19

- `POST /api/campaign/create` → `api_campaign_create()`
- `GET /api/campaign/list` → `api_campaign_list()`
- `GET /api/campaign/read/<int:campaign_id>` → `api_campaign_read()`
- `PUT /api/campaign/update/<int:campaign_id>` → `api_campaign_update()`
- `DELETE /api/campaign/delete/<int:campaign_id>` → `api_campaign_delete()`

### Análise e Otimização (Prioridade: MÉDIA)

**Descrição:** Análise de performance e recomendações

**Rotas Relacionadas:** 13

- `POST /api/analyze-landing-page` → `api_analyze_landing_page()`
- `POST /api/operator/optimize` → `api_operator_optimize()`
- `GET /api/ab-test/analyze/<int:test_id>` → `api_ab_test_analyze()`
- `POST /api/landing/analyze` → `api_landing_analyze()`
- `POST /api/automation/optimize/<int:campaign_id>` → `api_automation_optimize_campaign()`

### Persona e Segmentação (Prioridade: MÉDIA)

**Descrição:** Análise de público e criação de personas

**Rotas Relacionadas:** 2

- `POST /api/dco/generate-segmentation` → `api_dco_generate_segmentation()`
- `GET /segmentation` → `segmentation()`


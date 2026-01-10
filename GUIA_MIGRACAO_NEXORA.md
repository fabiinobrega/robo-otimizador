# Guia de Migração para NEXORA Premium Design

## Visão Geral

Este guia orienta a migração das páginas existentes do NEXORA Operator v11.7 para o novo design system premium, inspirado em Stripe, Linear e Notion.

## Arquitetura do Novo Design

### Arquivos Principais

1. **`static/css/nexora-premium-theme.css`** - Design system completo com variáveis CSS
2. **`templates/base_nexora.html`** - Template base com sidebar e topbar
3. **`templates/components/nexora_components.html`** - Componentes reutilizáveis

### Estrutura de Páginas

Todas as novas páginas devem seguir este padrão:

```html
{% extends "base_nexora.html" %}

{% block title %}Título da Página - NEXORA{% endblock %}

{% block content %}
<!-- Page Header -->
<div class="nexora-page-header">
    <h1 class="nexora-page-title">Título da Página</h1>
    <p class="nexora-page-subtitle">Descrição breve</p>
</div>

<!-- Conteúdo da página -->
{% endblock %}
```

## Componentes Disponíveis

### 1. Cards de Estatísticas

```html
<div class="nexora-stat-card">
    <div class="nexora-stat-label">Label</div>
    <div class="nexora-stat-value">Valor</div>
    <div class="nexora-stat-change positive">
        <i class="fas fa-arrow-up"></i> 12%
    </div>
</div>
```

### 2. Cards Padrão

```html
<div class="nexora-card">
    <!-- Conteúdo -->
</div>
```

### 3. Botões

```html
<!-- Primary -->
<button class="btn-nexora btn-nexora-primary">
    <i class="fas fa-plus"></i>
    Texto
</button>

<!-- Secondary -->
<button class="btn-nexora btn-nexora-secondary">
    Texto
</button>
```

### 4. Formulários

```html
<div class="form-group-nexora">
    <label class="form-label-nexora">Label</label>
    <input type="text" class="form-input-nexora" placeholder="Placeholder" />
</div>
```

### 5. Toast Notifications

```javascript
NEXORA.showToast('Título', 'Mensagem', 'success'); // success, error, warning, info
```

### 6. Empty States

```html
<div class="nexora-empty-state">
    <div class="nexora-empty-state-icon"><i class="fas fa-icon"></i></div>
    <div class="nexora-empty-state-title">Título</div>
    <div class="nexora-empty-state-message">Mensagem</div>
</div>
```

### 7. Loading Spinner

```html
<div class="nexora-spinner"></div>
```

## Paleta de Cores

### Backgrounds
- `var(--bg-primary)` - #0A0A0A (fundo principal)
- `var(--bg-secondary)` - #141414 (cards, modais)
- `var(--bg-tertiary)` - #1A1A1A (elementos elevados)

### Fills (inputs, botões)
- `var(--fill-primary)` - #1F1F1F
- `var(--fill-secondary)` - #292929
- `var(--fill-tertiary)` - #333333

### Texto
- `var(--text-primary)` - #F5F5F5 (texto principal)
- `var(--text-secondary)` - #A3A3A3 (texto secundário)
- `var(--text-tertiary)` - #737373 (desabilitado/placeholder)

### Bordas
- `var(--border-primary)` - #262626
- `var(--border-secondary)` - #363636
- `var(--border-focus)` - #525252

### Accents
- `var(--accent-primary)` - #4f46e5 (ações principais)
- `var(--accent-success)` - #22c55e (sucesso)
- `var(--accent-warning)` - #f97316 (avisos)
- `var(--accent-danger)` - #ef4444 (erros)
- `var(--accent-info)` - #3b82f6 (informações)

## Tipografia

### Tamanhos
- `var(--text-xs)` - 0.75rem (12px)
- `var(--text-sm)` - 0.875rem (14px)
- `var(--text-base)` - 1rem (16px)
- `var(--text-lg)` - 1.125rem (18px)
- `var(--text-xl)` - 1.25rem (20px)
- `var(--text-2xl)` - 1.5rem (24px)
- `var(--text-3xl)` - 1.875rem (30px)

### Font Family
- `var(--font-family-sans)` - 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif

## Espaçamento

- `var(--spacing-1)` - 0.25rem (4px)
- `var(--spacing-2)` - 0.5rem (8px)
- `var(--spacing-3)` - 0.75rem (12px)
- `var(--spacing-4)` - 1rem (16px)
- `var(--spacing-5)` - 1.25rem (20px)
- `var(--spacing-6)` - 1.5rem (24px)
- `var(--spacing-8)` - 2rem (32px)

## Bordas e Raios

- `var(--radius-sm)` - 0.25rem (4px)
- `var(--radius-md)` - 0.375rem (6px)
- `var(--radius-lg)` - 0.5rem (8px)
- `var(--radius-xl)` - 0.75rem (12px)

## Sombras

- `var(--shadow-sm)` - Sombra pequena
- `var(--shadow-md)` - Sombra média
- `var(--shadow-lg)` - Sombra grande
- `var(--shadow-xl)` - Sombra extra grande

## Transições

- `var(--transition-fast)` - 150ms
- `var(--transition-base)` - 200ms
- `var(--transition-slow)` - 300ms

## Utilitários JavaScript

### NEXORA Object

```javascript
// Formatação de moeda
NEXORA.formatCurrency(1234.56); // "R$ 1.234,56"

// Formatação de número
NEXORA.formatNumber(1234); // "1.234"

// Formatação de porcentagem
NEXORA.formatPercentage(12.34); // "12.34%"

// Toast notification
NEXORA.showToast('Título', 'Mensagem', 'success');
```

## Checklist de Migração por Página

Para cada página antiga, siga este checklist:

- [ ] Criar novo arquivo `{nome}_nexora.html`
- [ ] Estender `base_nexora.html`
- [ ] Adicionar page header com título e subtítulo
- [ ] Substituir cards antigos por `nexora-card`
- [ ] Substituir botões por `btn-nexora`
- [ ] Substituir inputs por `form-input-nexora`
- [ ] Adicionar estados de loading
- [ ] Adicionar estados vazios
- [ ] Implementar toasts para feedback
- [ ] Testar responsividade
- [ ] Testar funcionalidades existentes

## Páginas Já Migradas

1. ✅ `dashboard_nexora.html` - Dashboard CEO View
2. ✅ `campaigns_nexora.html` - Lista de Campanhas
3. ✅ `create_campaign_nexora.html` - Criar Campanha (wizard)

## Páginas Pendentes de Migração

1. ⏳ `reports_dashboard.html` → `reports_nexora.html`
2. ⏳ `segmentation.html` → `segmentation_nexora.html`
3. ⏳ `media_library.html` → `media_library_nexora.html`
4. ⏳ `velyra_prime.html` → `velyra_prime_nexora.html`
5. ⏳ `ai_copywriter.html` → `ai_copywriter_nexora.html`
6. ⏳ `funnel_builder.html` → `funnel_builder_nexora.html`
7. ⏳ `landing_page_builder.html` → `landing_page_builder_nexora.html`
8. ⏳ `dco_builder.html` → `dco_builder_nexora.html`
9. ⏳ `ab_testing.html` → `ab_testing_nexora.html`
10. ⏳ `automation.html` → `automation_nexora.html`
11. ⏳ `competitor_spy.html` → `competitor_spy_nexora.html`
12. ⏳ `integrations.html` → `integrations_nexora.html`
13. ⏳ `settings.html` → `settings_nexora.html`
14. ⏳ `create_perfect_ad_v2.html` → `create_perfect_ad_nexora.html`

## Atualização de Rotas no Backend

Após migrar uma página, atualize as rotas no `main.py`:

```python
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_nexora.html')
```

## Testes

Antes de considerar uma página migrada, teste:

1. ✅ Carregamento de dados da API
2. ✅ Funcionalidades interativas (botões, formulários)
3. ✅ Responsividade (mobile, tablet, desktop)
4. ✅ Estados de loading
5. ✅ Estados vazios
6. ✅ Mensagens de erro/sucesso
7. ✅ Navegação entre páginas

## Boas Práticas

1. **Consistência**: Use sempre as classes do design system
2. **Acessibilidade**: Mantenha ARIA labels e navegação por teclado
3. **Performance**: Lazy load imagens e dados pesados
4. **Feedback**: Sempre forneça feedback visual para ações do usuário
5. **Simplicidade**: Máximo 2 cliques para qualquer ação

## Suporte

Para dúvidas sobre a migração, consulte:
- `NEXORA_BRAND_IDENTITY.md` - Identidade da marca
- `nexora-premium-theme.css` - Design system completo
- `base_nexora.html` - Template base
- Páginas já migradas como referência

---

**Última atualização:** 24 de Novembro de 2024

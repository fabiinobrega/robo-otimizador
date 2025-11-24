# 📘 GUIA DE MIGRAÇÃO PREMIUM - NEXORA PRIME v11.7

**Data:** 24/11/2024  
**Versão:** 1.0  
**Objetivo:** Migrar todas as páginas do NEXORA PRIME para o novo Design System Premium

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Arquivos Criados](#arquivos-criados)
3. [Páginas Modelo Completas](#páginas-modelo-completas)
4. [Padrões de Conversão](#padrões-de-conversão)
5. [Componentes Premium](#componentes-premium)
6. [Páginas Restantes (11 páginas)](#páginas-restantes)
7. [Checklist de Migração](#checklist-de-migração)
8. [Exemplos de Código](#exemplos-de-código)

---

## 🎯 VISÃO GERAL

### O Que Foi Criado

**Design System Premium Completo:**
- ✅ `nexora_design_system_premium.css` (600+ linhas)
- ✅ `nexora_components_premium.css` (800+ linhas)
- ✅ `nexora_components.html` (showcase visual)

**3 Páginas Modelo Reconstruídas:**
1. ✅ `dashboard_premium.html` - Dashboard com métricas e gráficos
2. ✅ `create_campaign_premium.html` - Wizard em 5 passos
3. ✅ `reports_premium.html` - Analytics e relatórios

### Melhorias Implementadas

**Design:**
- Paleta de cores premium (50+ variáveis)
- Tipografia enterprise (Inter)
- Espaçamentos generosos (24px-48px)
- Gradientes vibrantes
- Sombras realistas e coloridas
- Micro-animações suaves

**UX:**
- Cards interativos com hover
- Loading states (spinners + skeleton)
- Estados vazios com ícones grandes
- Badges com dot indicators
- Breadcrumbs premium
- Alertas contextuais

---

## 📁 ARQUIVOS CRIADOS

### 1. Design System

```
/static/css/nexora_design_system_premium.css
```

**Contém:**
- Paleta de cores (50+ variáveis)
- Tipografia (11 tamanhos + 9 pesos)
- Espaçamentos (24 variáveis)
- Bordas e arredondamentos
- Sombras (10 variáveis)
- Transições e animações
- Z-index system
- Grid 12 colunas
- Breakpoints responsivos
- Reset CSS

### 2. Componentes

```
/static/css/nexora_components_premium.css
```

**Contém:**
- Botões (6 variantes + 4 tamanhos)
- Cards (5 variantes)
- Formulários (inputs, selects, textareas)
- Badges e Tags (7 cores)
- Alertas (4 tipos)
- Tabelas (striped, bordered, hover)
- Modais (4 tamanhos)
- Tooltips
- Breadcrumbs
- Loading states

### 3. Showcase

```
/nexora_components.html
```

**Contém:**
- Exemplos visuais de todos os componentes
- Paleta de cores visualizada
- Documentação interativa

---

## ✅ PÁGINAS MODELO COMPLETAS

### 1. Dashboard Premium

**Arquivo:** `templates/dashboard_premium.html`

**Componentes usados:**
- Breadcrumbs premium
- 4 cards de métricas com gradientes
- Skeleton loading
- Animação de contagem de números
- 2 gráficos (Chart.js)
- Tabela premium de campanhas
- Timeline de atividades
- Seção de ações rápidas

**Características:**
- Grid responsivo (2fr 1fr)
- Hover effects suaves
- Badges com dot indicators
- Estados vazios com ícones
- Formatação de tempo relativo

### 2. Criar Campanha Premium

**Arquivo:** `templates/create_campaign_premium.html`

**Componentes usados:**
- Wizard em 5 passos
- Progress indicators visuais
- Layout 2 colunas (conteúdo + sidebar)
- 4 cards de plataformas interativos
- Formulários premium
- Alertas da IA Velyra
- Navegação entre passos

**Características:**
- Gradientes diferentes por passo
- Hover effects nos cards
- Validação visual
- Transições suaves
- Resumo final

### 3. Relatórios & Analytics Premium

**Arquivo:** `templates/reports_premium.html`

**Componentes usados:**
- 5 KPIs premium com gradientes
- Date range picker
- 2 gráficos principais
- Top 5 campanhas com ranking
- Funil de conversão
- Tabela detalhada
- Botões de exportação

**Características:**
- Grid responsivo
- Sombras coloridas
- Barras de progresso
- Ranking visual
- Cores semânticas

---

## 🔄 PADRÕES DE CONVERSÃO

### Bootstrap → Nexora Premium

#### 1. Classes de Layout

**ANTES (Bootstrap):**
```html
<div class="container">
    <div class="row">
        <div class="col-md-6">...</div>
        <div class="col-md-6">...</div>
    </div>
</div>
```

**DEPOIS (Nexora Premium):**
```html
<div style="max-width: var(--nexora-container-xl); margin: 0 auto; padding: var(--nexora-spacing-6);">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--nexora-spacing-6);">
        <div>...</div>
        <div>...</div>
    </div>
</div>
```

#### 2. Botões

**ANTES (Bootstrap):**
```html
<button class="btn btn-primary">Clique Aqui</button>
<button class="btn btn-outline-secondary">Cancelar</button>
```

**DEPOIS (Nexora Premium):**
```html
<button class="nexora-btn nexora-btn-primary">Clique Aqui</button>
<button class="nexora-btn nexora-btn-outlined">Cancelar</button>
```

#### 3. Cards

**ANTES (Bootstrap):**
```html
<div class="card">
    <div class="card-header">Título</div>
    <div class="card-body">Conteúdo</div>
    <div class="card-footer">Rodapé</div>
</div>
```

**DEPOIS (Nexora Premium):**
```html
<div class="nexora-card">
    <div class="nexora-card-header">
        <h3 class="nexora-card-title">Título</h3>
    </div>
    <div class="nexora-card-body">Conteúdo</div>
    <div class="nexora-card-footer">Rodapé</div>
</div>
```

#### 4. Formulários

**ANTES (Bootstrap):**
```html
<div class="mb-3">
    <label class="form-label">Nome</label>
    <input type="text" class="form-control">
</div>
```

**DEPOIS (Nexora Premium):**
```html
<div class="nexora-form-group">
    <label class="nexora-label">Nome</label>
    <input type="text" class="nexora-input">
</div>
```

#### 5. Badges

**ANTES (Bootstrap):**
```html
<span class="badge bg-success">Ativo</span>
<span class="badge bg-warning">Pendente</span>
```

**DEPOIS (Nexora Premium):**
```html
<span class="nexora-badge nexora-badge-success nexora-badge-dot">Ativo</span>
<span class="nexora-badge nexora-badge-warning nexora-badge-dot">Pendente</span>
```

#### 6. Alertas

**ANTES (Bootstrap):**
```html
<div class="alert alert-success">
    <strong>Sucesso!</strong> Operação concluída.
</div>
```

**DEPOIS (Nexora Premium):**
```html
<div class="nexora-alert nexora-alert-success">
    <div class="nexora-alert-content">
        <div class="nexora-alert-title">Sucesso!</div>
        <div class="nexora-alert-description">Operação concluída.</div>
    </div>
</div>
```

#### 7. Tabelas

**ANTES (Bootstrap):**
```html
<table class="table table-hover">
    <thead>
        <tr><th>Coluna</th></tr>
    </thead>
    <tbody>
        <tr><td>Valor</td></tr>
    </tbody>
</table>
```

**DEPOIS (Nexora Premium):**
```html
<div class="nexora-table-container">
    <table class="nexora-table">
        <thead>
            <tr><th>Coluna</th></tr>
        </thead>
        <tbody>
            <tr><td>Valor</td></tr>
        </tbody>
    </table>
</div>
```

#### 8. Breadcrumbs

**ANTES (Bootstrap):**
```html
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        <li class="breadcrumb-item active">Página</li>
    </ol>
</nav>
```

**DEPOIS (Nexora Premium):**
```html
<nav class="nexora-breadcrumb">
    <div class="nexora-breadcrumb-item">
        <a href="/">Home</a>
    </div>
    <span class="nexora-breadcrumb-separator">/</span>
    <div class="nexora-breadcrumb-item active">Página</div>
</nav>
```

---

## 🎨 COMPONENTES PREMIUM

### 1. Cards com Gradientes

```html
<div class="nexora-card" style="background: var(--nexora-gradient-primary-soft); border: 2px solid var(--nexora-primary-200);">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div style="flex: 1;">
            <p style="font-size: var(--nexora-text-sm); font-weight: var(--nexora-font-semibold); color: var(--nexora-gray-600); text-transform: uppercase; letter-spacing: var(--nexora-tracking-wider); margin-bottom: var(--nexora-spacing-2);">
                Título
            </p>
            <h2 style="font-size: var(--nexora-text-4xl); font-weight: var(--nexora-font-extrabold); color: var(--nexora-gray-900); margin-bottom: var(--nexora-spacing-3);">
                1.234
            </h2>
            <span class="nexora-badge nexora-badge-success nexora-badge-dot">
                <i class="fas fa-arrow-up"></i> +12%
            </span>
        </div>
        <div style="width: 64px; height: 64px; background: var(--nexora-gradient-primary); border-radius: var(--nexora-radius-2xl); display: flex; align-items: center; justify-content: center; box-shadow: var(--nexora-shadow-primary);">
            <i class="fas fa-chart-line" style="font-size: 28px; color: var(--nexora-white);"></i>
        </div>
    </div>
</div>
```

### 2. Skeleton Loading

```html
<div class="nexora-skeleton" style="width: 100px; height: 40px;"></div>
<div class="nexora-skeleton nexora-skeleton-text"></div>
<div class="nexora-skeleton nexora-skeleton-title"></div>
```

### 3. Estados Vazios

```html
<div style="text-align: center; padding: var(--nexora-spacing-8); color: var(--nexora-gray-500);">
    <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: var(--nexora-spacing-4); opacity: 0.3;"></i>
    <p>Nenhum item encontrado</p>
</div>
```

### 4. Spinner

```html
<div class="nexora-spinner"></div>
<div class="nexora-spinner nexora-spinner-sm"></div>
<div class="nexora-spinner nexora-spinner-lg"></div>
```

### 5. Modal

```html
<div class="nexora-modal-backdrop">
    <div class="nexora-modal nexora-modal-md">
        <div class="nexora-modal-header">
            <h3 class="nexora-modal-title">Título</h3>
            <button class="nexora-modal-close">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="nexora-modal-body">
            Conteúdo
        </div>
        <div class="nexora-modal-footer">
            <button class="nexora-btn nexora-btn-ghost">Cancelar</button>
            <button class="nexora-btn nexora-btn-primary">Confirmar</button>
        </div>
    </div>
</div>
```

---

## 📄 PÁGINAS RESTANTES (11 páginas)

### Prioridade ALTA (4 páginas)

#### 1. **Segmentação** (`segmentation.html`)

**Componentes a usar:**
- Breadcrumbs premium
- Cards de segmentos com gradientes
- Formulário de criação de segmento
- Tabela de segmentos existentes
- Badges de status

**Padrão de conversão:**
```
Bootstrap cards → nexora-card
Bootstrap forms → nexora-form-group + nexora-input
Bootstrap badges → nexora-badge nexora-badge-dot
```

#### 2. **Biblioteca de Mídia** (`media-library.html`)

**Componentes a usar:**
- Grid de imagens responsivo
- Cards de mídia com hover
- Modal de preview
- Botões de upload
- Filtros e busca

**Padrão de conversão:**
```
Bootstrap grid → CSS Grid com gap
Bootstrap modal → nexora-modal-backdrop + nexora-modal
Bootstrap buttons → nexora-btn nexora-btn-primary
```

#### 3. **Integrações** (`integrations.html`)

**Componentes a usar:**
- Cards de integrações com logos
- Badges de status (conectado/desconectado)
- Botões de ação
- Alertas de configuração

**Padrão de conversão:**
```
Bootstrap cards → nexora-card nexora-card-interactive
Bootstrap badges → nexora-badge nexora-badge-success/danger
Bootstrap alerts → nexora-alert nexora-alert-info
```

#### 4. **Configurações** (`settings.html`)

**Componentes a usar:**
- Tabs laterais
- Formulários de configuração
- Switches e checkboxes premium
- Botões de salvar

**Padrão de conversão:**
```
Bootstrap nav-tabs → Custom tabs com nexora-btn-ghost
Bootstrap forms → nexora-form-group
Bootstrap switches → nexora-checkbox styled
```

### Prioridade MÉDIA (4 páginas)

#### 5. **Inteligência Artificial** (`ai-assistant.html`)

**Componentes a usar:**
- Chat interface
- Cards de sugestões da IA
- Loading states
- Badges de confiança

**Padrão de conversão:**
```
Chat messages → nexora-card com gradientes
Loading → nexora-spinner
Badges → nexora-badge nexora-badge-primary
```

#### 6. **Plataformas** (`platforms.html`)

**Componentes a usar:**
- Grid de plataformas
- Cards interativos
- Badges de status
- Botões de conexão

**Padrão de conversão:**
```
Platform cards → nexora-card nexora-card-interactive
Status badges → nexora-badge nexora-badge-dot
Connect buttons → nexora-btn nexora-btn-primary
```

#### 7. **Onboarding** (`onboarding.html`)

**Componentes a usar:**
- Wizard steps
- Progress bar
- Cards de boas-vindas
- Botões de navegação

**Padrão de conversão:**
```
Steps → Wizard steps (ver create_campaign_premium.html)
Progress → Custom progress bar com gradientes
Cards → nexora-card com gradientes
```

#### 8. **Chat IA** (`operator-chat.html`)

**Componentes a usar:**
- Interface de chat
- Bubbles de mensagem
- Input de texto
- Botões de ação rápida

**Padrão de conversão:**
```
Chat bubbles → nexora-card com border-radius-2xl
Input → nexora-input com ícone
Quick actions → nexora-btn nexora-btn-ghost
```

### Prioridade BAIXA (3 páginas)

#### 9. **Builder de Funis** (`funnel-builder.html`)

**Componentes a usar:**
- Canvas de arrastar e soltar
- Cards de etapas
- Conectores visuais
- Sidebar de componentes

**Padrão de conversão:**
```
Funnel steps → nexora-card com hover effects
Connectors → SVG lines com gradientes
Sidebar → nexora-card com overflow-y
```

#### 10. **Builder de DCO** (`dco-builder.html`)

**Componentes a usar:**
- Editor visual
- Preview de variações
- Formulários de configuração
- Botões de ação

**Padrão de conversão:**
```
Editor → Custom com nexora-card
Previews → Grid de nexora-card
Forms → nexora-form-group
```

#### 11. **Builder de Landing Pages** (`landing-builder.html`)

**Componentes a usar:**
- Editor de blocos
- Sidebar de componentes
- Preview responsivo
- Botões de publicação

**Padrão de conversão:**
```
Blocks → nexora-card draggable
Sidebar → nexora-card com scroll
Preview → iframe com border-radius
```

---

## ✅ CHECKLIST DE MIGRAÇÃO

### Para Cada Página:

- [ ] **1. Criar arquivo `[nome]_premium.html`**
- [ ] **2. Adicionar imports do Design System:**
  ```html
  <link rel="stylesheet" href="/static/css/nexora_design_system_premium.css">
  <link rel="stylesheet" href="/static/css/nexora_components_premium.css">
  ```
- [ ] **3. Converter breadcrumbs:**
  - Bootstrap breadcrumb → nexora-breadcrumb
- [ ] **4. Converter header:**
  - Adicionar ícone com gradiente
  - Adicionar subtítulo
  - Adicionar botões de ação
- [ ] **5. Converter cards:**
  - Bootstrap card → nexora-card
  - Adicionar gradientes quando apropriado
  - Adicionar hover effects
- [ ] **6. Converter formulários:**
  - form-control → nexora-input
  - form-label → nexora-label
  - form-group → nexora-form-group
- [ ] **7. Converter botões:**
  - btn btn-primary → nexora-btn nexora-btn-primary
  - btn btn-outline → nexora-btn nexora-btn-outlined
- [ ] **8. Converter badges:**
  - badge bg-success → nexora-badge nexora-badge-success nexora-badge-dot
- [ ] **9. Converter tabelas:**
  - table → nexora-table-container + nexora-table
- [ ] **10. Converter alertas:**
  - alert → nexora-alert
- [ ] **11. Adicionar loading states:**
  - Spinner ou skeleton loading
- [ ] **12. Adicionar estados vazios:**
  - Ícone grande + mensagem
- [ ] **13. Testar responsividade:**
  - Mobile, tablet, desktop
- [ ] **14. Testar interatividade:**
  - Hover effects, clicks, transições
- [ ] **15. Validar acessibilidade:**
  - Contraste, ARIA labels

---

## 💻 EXEMPLOS DE CÓDIGO

### Exemplo 1: Página Completa Básica

```html
{% extends "base_premium.html" %}

{% block title %}Título da Página - NEXORA PRIME{% endblock %}

{% block content %}
<!-- Breadcrumbs -->
<nav class="nexora-breadcrumb" style="margin-bottom: var(--nexora-spacing-6);">
    <div class="nexora-breadcrumb-item">
        <a href="/"><i class="fas fa-home"></i> Dashboard</a>
    </div>
    <span class="nexora-breadcrumb-separator">/</span>
    <div class="nexora-breadcrumb-item active">
        Título da Página
    </div>
</nav>

<!-- Header -->
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--nexora-spacing-8);">
    <div>
        <h1 style="margin-bottom: var(--nexora-spacing-2); display: flex; align-items: center; gap: var(--nexora-spacing-3);">
            <i class="fas fa-icon" style="background: var(--nexora-gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>
            Título da Página
        </h1>
        <p style="color: var(--nexora-gray-600); margin: 0;">Descrição da página</p>
    </div>
    
    <div style="display: flex; gap: var(--nexora-spacing-3);">
        <button class="nexora-btn nexora-btn-outlined">Ação Secundária</button>
        <button class="nexora-btn nexora-btn-primary">Ação Principal</button>
    </div>
</div>

<!-- Content -->
<div class="nexora-card">
    <div class="nexora-card-header">
        <h3 class="nexora-card-title">Título do Card</h3>
    </div>
    <div class="nexora-card-body">
        Conteúdo aqui
    </div>
</div>
{% endblock %}
```

### Exemplo 2: Grid de Cards

```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: var(--nexora-spacing-6);">
    <div class="nexora-card nexora-card-interactive">
        <div class="nexora-card-body">
            <h4>Card 1</h4>
            <p>Conteúdo</p>
        </div>
    </div>
    
    <div class="nexora-card nexora-card-interactive">
        <div class="nexora-card-body">
            <h4>Card 2</h4>
            <p>Conteúdo</p>
        </div>
    </div>
    
    <div class="nexora-card nexora-card-interactive">
        <div class="nexora-card-body">
            <h4>Card 3</h4>
            <p>Conteúdo</p>
        </div>
    </div>
</div>
```

### Exemplo 3: Formulário Completo

```html
<form class="nexora-card">
    <div class="nexora-card-header">
        <h3 class="nexora-card-title">Formulário</h3>
    </div>
    <div class="nexora-card-body">
        <div class="nexora-form-group">
            <label class="nexora-label nexora-label-required">Nome</label>
            <input type="text" class="nexora-input" placeholder="Digite seu nome" required>
        </div>
        
        <div class="nexora-form-group">
            <label class="nexora-label">Email</label>
            <input type="email" class="nexora-input" placeholder="seu@email.com">
            <span class="nexora-helper-text">Nunca compartilharemos seu email.</span>
        </div>
        
        <div class="nexora-form-group">
            <label class="nexora-label">Categoria</label>
            <select class="nexora-select">
                <option>Opção 1</option>
                <option>Opção 2</option>
            </select>
        </div>
        
        <div class="nexora-form-group">
            <label class="nexora-label">Mensagem</label>
            <textarea class="nexora-textarea" rows="4"></textarea>
        </div>
    </div>
    <div class="nexora-card-footer">
        <button type="button" class="nexora-btn nexora-btn-ghost">Cancelar</button>
        <button type="submit" class="nexora-btn nexora-btn-primary">Enviar</button>
    </div>
</form>
```

### Exemplo 4: Tabela com Ações

```html
<div class="nexora-card">
    <div class="nexora-card-header">
        <h3 class="nexora-card-title">Lista de Itens</h3>
        <button class="nexora-btn nexora-btn-primary nexora-btn-sm">Adicionar</button>
    </div>
    <div class="nexora-card-body" style="padding: 0;">
        <div class="nexora-table-container" style="box-shadow: none;">
            <table class="nexora-table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Status</th>
                        <th>Data</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Item 1</strong></td>
                        <td><span class="nexora-badge nexora-badge-success nexora-badge-dot">Ativo</span></td>
                        <td>24/11/2024</td>
                        <td>
                            <button class="nexora-btn nexora-btn-ghost nexora-btn-sm">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="nexora-btn nexora-btn-ghost nexora-btn-sm">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
```

---

## 🎨 VARIÁVEIS CSS MAIS USADAS

### Cores
```css
var(--nexora-primary-600)     /* Azul principal */
var(--nexora-secondary-600)   /* Roxo secundário */
var(--nexora-success)         /* Verde sucesso */
var(--nexora-warning)         /* Amarelo aviso */
var(--nexora-danger)          /* Vermelho erro */
var(--nexora-gray-600)        /* Cinza texto */
var(--nexora-white)           /* Branco */
```

### Gradientes
```css
var(--nexora-gradient-primary)         /* Azul → Roxo */
var(--nexora-gradient-primary-soft)    /* Azul suave */
var(--nexora-gradient-secondary)       /* Roxo → Azul */
var(--nexora-gradient-energy)          /* Ciano → Verde */
```

### Espaçamentos
```css
var(--nexora-spacing-2)   /* 8px */
var(--nexora-spacing-4)   /* 16px */
var(--nexora-spacing-6)   /* 24px */
var(--nexora-spacing-8)   /* 32px */
var(--nexora-spacing-10)  /* 40px */
```

### Tipografia
```css
var(--nexora-text-sm)     /* 14px */
var(--nexora-text-base)   /* 16px */
var(--nexora-text-lg)     /* 18px */
var(--nexora-text-xl)     /* 20px */
var(--nexora-text-2xl)    /* 24px */
var(--nexora-text-4xl)    /* 36px */
```

### Sombras
```css
var(--nexora-shadow-sm)       /* Sombra pequena */
var(--nexora-shadow-md)       /* Sombra média */
var(--nexora-shadow-lg)       /* Sombra grande */
var(--nexora-shadow-primary)  /* Sombra azul */
```

### Bordas
```css
var(--nexora-radius-lg)   /* 12px */
var(--nexora-radius-xl)   /* 16px */
var(--nexora-radius-2xl)  /* 20px */
var(--nexora-radius-full) /* 9999px (círculo) */
```

---

## 🚀 PRÓXIMOS PASSOS

1. **Migrar páginas de prioridade ALTA** (4 páginas)
2. **Testar e validar** cada página migrada
3. **Migrar páginas de prioridade MÉDIA** (4 páginas)
4. **Migrar páginas de prioridade BAIXA** (3 páginas)
5. **Criar arquivo `base_premium.html`** (template base)
6. **Atualizar rotas** para usar páginas premium
7. **Remover arquivos antigos** após validação
8. **Documentar mudanças** no CHANGELOG

---

## 📞 SUPORTE

Para dúvidas ou problemas durante a migração:

1. Consulte as **3 páginas modelo** criadas
2. Veja o **showcase de componentes** em `nexora_components.html`
3. Revise este guia de migração
4. Consulte a **AUDITORIA_DE_DESIGN.md** para contexto

---

**Última atualização:** 24/11/2024  
**Versão:** 1.0  
**Autor:** Manus AI Agent

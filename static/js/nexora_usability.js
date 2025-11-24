// ═══════════════════════════════════════════════════════════════════
// NEXORA PRIME v11.7 - USABILITY ENHANCEMENTS
// ═══════════════════════════════════════════════════════════════════
// Melhorias de usabilidade em 200%
// Data: 24/11/2024
// ═══════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════
// 1. DARK MODE (Modo Claro/Escuro)
// ═══════════════════════════════════════════════════════════════════

class DarkModeManager {
    constructor() {
        this.darkMode = localStorage.getItem('nexora-dark-mode') === 'true';
        this.init();
    }
    
    init() {
        // Apply saved preference
        if (this.darkMode) {
            document.documentElement.classList.add('dark-mode');
        }
        
        // Create toggle button
        this.createToggleButton();
        
        // Listen for system preference changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('nexora-dark-mode')) {
                this.toggle(e.matches);
            }
        });
    }
    
    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'nexora-dark-mode-toggle';
        button.innerHTML = this.darkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        button.title = this.darkMode ? 'Modo Claro' : 'Modo Escuro';
        button.onclick = () => this.toggle();
        
        // Add to page
        document.body.appendChild(button);
    }
    
    toggle(force = null) {
        this.darkMode = force !== null ? force : !this.darkMode;
        
        if (this.darkMode) {
            document.documentElement.classList.add('dark-mode');
        } else {
            document.documentElement.classList.remove('dark-mode');
        }
        
        // Save preference
        localStorage.setItem('nexora-dark-mode', this.darkMode);
        
        // Update button
        const button = document.querySelector('.nexora-dark-mode-toggle');
        if (button) {
            button.innerHTML = this.darkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            button.title = this.darkMode ? 'Modo Claro' : 'Modo Escuro';
        }
        
        // Dispatch event
        window.dispatchEvent(new CustomEvent('darkModeChanged', { detail: { darkMode: this.darkMode } }));
    }
}

// ═══════════════════════════════════════════════════════════════════
// 2. SIDEBAR INTELIGENTE (Navegação Lateral)
// ═══════════════════════════════════════════════════════════════════

class SmartSidebar {
    constructor() {
        this.collapsed = localStorage.getItem('nexora-sidebar-collapsed') === 'true';
        this.init();
    }
    
    init() {
        // Apply saved state
        if (this.collapsed) {
            document.body.classList.add('sidebar-collapsed');
        }
        
        // Create toggle button
        this.createToggleButton();
        
        // Auto-collapse on mobile
        if (window.innerWidth < 768) {
            this.collapse(true);
        }
        
        // Listen for resize
        window.addEventListener('resize', () => {
            if (window.innerWidth < 768 && !this.collapsed) {
                this.collapse(true);
            }
        });
    }
    
    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'nexora-sidebar-toggle';
        button.innerHTML = '<i class="fas fa-bars"></i>';
        button.title = 'Toggle Sidebar';
        button.onclick = () => this.toggle();
        
        // Add to page
        const sidebar = document.querySelector('.sidebar, .nexora-sidebar');
        if (sidebar) {
            sidebar.insertBefore(button, sidebar.firstChild);
        }
    }
    
    toggle() {
        this.collapse(!this.collapsed);
    }
    
    collapse(force = null) {
        this.collapsed = force !== null ? force : !this.collapsed;
        
        if (this.collapsed) {
            document.body.classList.add('sidebar-collapsed');
        } else {
            document.body.classList.remove('sidebar-collapsed');
        }
        
        // Save preference
        localStorage.setItem('nexora-sidebar-collapsed', this.collapsed);
        
        // Dispatch event
        window.dispatchEvent(new CustomEvent('sidebarChanged', { detail: { collapsed: this.collapsed } }));
    }
}

// ═══════════════════════════════════════════════════════════════════
// 3. BUSCA GLOBAL (Global Search)
// ═══════════════════════════════════════════════════════════════════

class GlobalSearch {
    constructor() {
        this.isOpen = false;
        this.init();
    }
    
    init() {
        // Create search modal
        this.createModal();
        
        // Listen for keyboard shortcut (Ctrl+K or Cmd+K)
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.toggle();
            }
            
            // Close on Escape
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }
    
    createModal() {
        const modal = document.createElement('div');
        modal.className = 'nexora-global-search-modal';
        modal.innerHTML = `
            <div class="nexora-global-search-backdrop"></div>
            <div class="nexora-global-search-content">
                <div class="nexora-global-search-header">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Buscar campanhas, relatórios, configurações..." class="nexora-global-search-input" autofocus>
                    <kbd>ESC</kbd>
                </div>
                <div class="nexora-global-search-results">
                    <div class="nexora-global-search-empty">
                        <i class="fas fa-search"></i>
                        <p>Digite para buscar...</p>
                    </div>
                </div>
                <div class="nexora-global-search-footer">
                    <div>
                        <kbd>↑</kbd> <kbd>↓</kbd> Navegar
                    </div>
                    <div>
                        <kbd>↵</kbd> Selecionar
                    </div>
                    <div>
                        <kbd>ESC</kbd> Fechar
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add event listeners
        const backdrop = modal.querySelector('.nexora-global-search-backdrop');
        backdrop.onclick = () => this.close();
        
        const input = modal.querySelector('.nexora-global-search-input');
        input.addEventListener('input', (e) => this.search(e.target.value));
        
        // Keyboard navigation
        input.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.navigateResults(1);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.navigateResults(-1);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                this.selectResult();
            }
        });
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        this.isOpen = true;
        const modal = document.querySelector('.nexora-global-search-modal');
        modal.classList.add('active');
        
        // Focus input
        setTimeout(() => {
            const input = modal.querySelector('.nexora-global-search-input');
            input.focus();
        }, 100);
    }
    
    close() {
        this.isOpen = false;
        const modal = document.querySelector('.nexora-global-search-modal');
        modal.classList.remove('active');
        
        // Clear input
        const input = modal.querySelector('.nexora-global-search-input');
        input.value = '';
        
        // Clear results
        this.clearResults();
    }
    
    async search(query) {
        if (!query || query.length < 2) {
            this.clearResults();
            return;
        }
        
        // Show loading
        this.showLoading();
        
        try {
            // Simulate API call (replace with actual API)
            await new Promise(resolve => setTimeout(resolve, 300));
            
            const results = this.mockSearch(query);
            this.displayResults(results);
        } catch (error) {
            console.error('Search error:', error);
            this.showError();
        }
    }
    
    mockSearch(query) {
        // Mock search results (replace with actual API call)
        const allItems = [
            { type: 'campaign', title: 'Black Friday 2024', url: '/campaigns/1', icon: 'fa-bullhorn' },
            { type: 'campaign', title: 'Remarketing Q4', url: '/campaigns/2', icon: 'fa-bullhorn' },
            { type: 'report', title: 'Relatório Mensal', url: '/reports/monthly', icon: 'fa-chart-bar' },
            { type: 'report', title: 'Performance por Plataforma', url: '/reports/platform', icon: 'fa-chart-bar' },
            { type: 'page', title: 'Configurações', url: '/settings', icon: 'fa-cog' },
            { type: 'page', title: 'Integrações', url: '/integrations', icon: 'fa-plug' },
            { type: 'page', title: 'Biblioteca de Mídia', url: '/media-library', icon: 'fa-images' },
        ];
        
        return allItems.filter(item => 
            item.title.toLowerCase().includes(query.toLowerCase())
        ).slice(0, 8);
    }
    
    displayResults(results) {
        const container = document.querySelector('.nexora-global-search-results');
        
        if (results.length === 0) {
            container.innerHTML = `
                <div class="nexora-global-search-empty">
                    <i class="fas fa-search"></i>
                    <p>Nenhum resultado encontrado</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = results.map((result, index) => `
            <a href="${result.url}" class="nexora-global-search-result ${index === 0 ? 'active' : ''}" data-index="${index}">
                <i class="fas ${result.icon}"></i>
                <div>
                    <div class="nexora-global-search-result-title">${result.title}</div>
                    <div class="nexora-global-search-result-type">${result.type}</div>
                </div>
                <i class="fas fa-arrow-right"></i>
            </a>
        `).join('');
        
        // Add click listeners
        container.querySelectorAll('.nexora-global-search-result').forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                window.location.href = el.getAttribute('href');
                this.close();
            });
        });
    }
    
    clearResults() {
        const container = document.querySelector('.nexora-global-search-results');
        container.innerHTML = `
            <div class="nexora-global-search-empty">
                <i class="fas fa-search"></i>
                <p>Digite para buscar...</p>
            </div>
        `;
    }
    
    showLoading() {
        const container = document.querySelector('.nexora-global-search-results');
        container.innerHTML = `
            <div class="nexora-global-search-loading">
                <div class="nexora-spinner"></div>
                <p>Buscando...</p>
            </div>
        `;
    }
    
    showError() {
        const container = document.querySelector('.nexora-global-search-results');
        container.innerHTML = `
            <div class="nexora-global-search-empty">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Erro ao buscar. Tente novamente.</p>
            </div>
        `;
    }
    
    navigateResults(direction) {
        const results = document.querySelectorAll('.nexora-global-search-result');
        if (results.length === 0) return;
        
        const activeIndex = Array.from(results).findIndex(el => el.classList.contains('active'));
        let newIndex = activeIndex + direction;
        
        if (newIndex < 0) newIndex = results.length - 1;
        if (newIndex >= results.length) newIndex = 0;
        
        results[activeIndex]?.classList.remove('active');
        results[newIndex]?.classList.add('active');
        results[newIndex]?.scrollIntoView({ block: 'nearest' });
    }
    
    selectResult() {
        const activeResult = document.querySelector('.nexora-global-search-result.active');
        if (activeResult) {
            window.location.href = activeResult.getAttribute('href');
            this.close();
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// 4. TOAST NOTIFICATIONS (Notificações)
// ═══════════════════════════════════════════════════════════════════

class ToastManager {
    constructor() {
        this.container = null;
        this.init();
    }
    
    init() {
        // Create container
        this.container = document.createElement('div');
        this.container.className = 'nexora-toast-container';
        document.body.appendChild(this.container);
    }
    
    show(message, type = 'info', duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `nexora-toast nexora-toast-${type}`;
        
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        
        toast.innerHTML = `
            <i class="fas ${icons[type]}"></i>
            <span>${message}</span>
            <button class="nexora-toast-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        this.container.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.add('active'), 10);
        
        // Close button
        const closeBtn = toast.querySelector('.nexora-toast-close');
        closeBtn.onclick = () => this.hide(toast);
        
        // Auto hide
        if (duration > 0) {
            setTimeout(() => this.hide(toast), duration);
        }
        
        return toast;
    }
    
    hide(toast) {
        toast.classList.remove('active');
        setTimeout(() => toast.remove(), 300);
    }
    
    success(message, duration) {
        return this.show(message, 'success', duration);
    }
    
    error(message, duration) {
        return this.show(message, 'error', duration);
    }
    
    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }
    
    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

// ═══════════════════════════════════════════════════════════════════
// 5. KEYBOARD SHORTCUTS (Atalhos de Teclado)
// ═══════════════════════════════════════════════════════════════════

class KeyboardShortcuts {
    constructor() {
        this.shortcuts = {
            'ctrl+k': () => window.globalSearch?.toggle(),
            'ctrl+b': () => window.smartSidebar?.toggle(),
            'ctrl+d': () => window.darkMode?.toggle(),
            'ctrl+n': () => window.location.href = '/campaigns/create',
            'ctrl+h': () => window.location.href = '/',
            'ctrl+/': () => this.showHelp(),
            'esc': () => this.closeModals()
        };
        
        this.init();
    }
    
    init() {
        document.addEventListener('keydown', (e) => {
            const key = this.getKeyCombo(e);
            const handler = this.shortcuts[key];
            
            if (handler) {
                e.preventDefault();
                handler();
            }
        });
    }
    
    getKeyCombo(e) {
        const parts = [];
        
        if (e.ctrlKey || e.metaKey) parts.push('ctrl');
        if (e.shiftKey) parts.push('shift');
        if (e.altKey) parts.push('alt');
        
        const key = e.key.toLowerCase();
        if (key !== 'control' && key !== 'shift' && key !== 'alt' && key !== 'meta') {
            parts.push(key);
        }
        
        return parts.join('+');
    }
    
    showHelp() {
        const modal = document.createElement('div');
        modal.className = 'nexora-modal-backdrop active';
        modal.innerHTML = `
            <div class="nexora-modal nexora-modal-md">
                <div class="nexora-modal-header">
                    <h3 class="nexora-modal-title">Atalhos de Teclado</h3>
                    <button class="nexora-modal-close" onclick="this.closest('.nexora-modal-backdrop').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="nexora-modal-body">
                    <table class="nexora-table">
                        <tbody>
                            <tr>
                                <td><kbd>Ctrl</kbd> + <kbd>K</kbd></td>
                                <td>Busca Global</td>
                            </tr>
                            <tr>
                                <td><kbd>Ctrl</kbd> + <kbd>B</kbd></td>
                                <td>Toggle Sidebar</td>
                            </tr>
                            <tr>
                                <td><kbd>Ctrl</kbd> + <kbd>D</kbd></td>
                                <td>Modo Escuro</td>
                            </tr>
                            <tr>
                                <td><kbd>Ctrl</kbd> + <kbd>N</kbd></td>
                                <td>Nova Campanha</td>
                            </tr>
                            <tr>
                                <td><kbd>Ctrl</kbd> + <kbd>H</kbd></td>
                                <td>Ir para Home</td>
                            </tr>
                            <tr>
                                <td><kbd>Ctrl</kbd> + <kbd>/</kbd></td>
                                <td>Mostrar Ajuda</td>
                            </tr>
                            <tr>
                                <td><kbd>ESC</kbd></td>
                                <td>Fechar Modais</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close on backdrop click
        modal.querySelector('.nexora-modal-backdrop').onclick = (e) => {
            if (e.target === modal) modal.remove();
        };
    }
    
    closeModals() {
        document.querySelectorAll('.nexora-modal-backdrop.active').forEach(modal => {
            modal.remove();
        });
    }
}

// ═══════════════════════════════════════════════════════════════════
// 6. AUTO-SAVE (Salvamento Automático)
// ═══════════════════════════════════════════════════════════════════

class AutoSave {
    constructor(formSelector, saveCallback, interval = 30000) {
        this.form = document.querySelector(formSelector);
        this.saveCallback = saveCallback;
        this.interval = interval;
        this.timer = null;
        this.lastSaved = null;
        
        if (this.form) {
            this.init();
        }
    }
    
    init() {
        // Listen for changes
        this.form.addEventListener('input', () => {
            this.scheduleAutoSave();
        });
        
        // Show last saved time
        this.createStatusIndicator();
    }
    
    scheduleAutoSave() {
        clearTimeout(this.timer);
        this.timer = setTimeout(() => {
            this.save();
        }, this.interval);
        
        this.updateStatus('Salvando...');
    }
    
    async save() {
        try {
            const formData = new FormData(this.form);
            const data = Object.fromEntries(formData);
            
            await this.saveCallback(data);
            
            this.lastSaved = new Date();
            this.updateStatus(`Salvo às ${this.lastSaved.toLocaleTimeString()}`);
            
            window.toast?.success('Alterações salvas automaticamente', 2000);
        } catch (error) {
            console.error('Auto-save error:', error);
            this.updateStatus('Erro ao salvar');
            window.toast?.error('Erro ao salvar automaticamente', 3000);
        }
    }
    
    createStatusIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'nexora-autosave-status';
        indicator.innerHTML = '<i class="fas fa-check-circle"></i> <span>Todas as alterações salvas</span>';
        
        this.form.insertBefore(indicator, this.form.firstChild);
    }
    
    updateStatus(message) {
        const indicator = this.form.querySelector('.nexora-autosave-status span');
        if (indicator) {
            indicator.textContent = message;
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// 7. QUICK ACTIONS (Ações Rápidas em Hover)
// ═══════════════════════════════════════════════════════════════════

class QuickActions {
    constructor() {
        this.init();
    }
    
    init() {
        // Add quick actions to cards
        document.querySelectorAll('.nexora-card[data-quick-actions]').forEach(card => {
            this.addQuickActions(card);
        });
    }
    
    addQuickActions(card) {
        const actions = card.getAttribute('data-quick-actions').split(',');
        
        const container = document.createElement('div');
        container.className = 'nexora-quick-actions';
        
        actions.forEach(action => {
            const button = document.createElement('button');
            button.className = 'nexora-quick-action-btn';
            button.title = action;
            
            const icons = {
                edit: 'fa-edit',
                delete: 'fa-trash',
                duplicate: 'fa-copy',
                share: 'fa-share',
                download: 'fa-download',
                view: 'fa-eye'
            };
            
            button.innerHTML = `<i class="fas ${icons[action] || 'fa-ellipsis-h'}"></i>`;
            button.onclick = (e) => {
                e.stopPropagation();
                this.handleAction(action, card);
            };
            
            container.appendChild(button);
        });
        
        card.appendChild(container);
    }
    
    handleAction(action, card) {
        const id = card.getAttribute('data-id');
        
        switch (action) {
            case 'edit':
                window.location.href = `/edit/${id}`;
                break;
            case 'delete':
                if (confirm('Tem certeza que deseja excluir?')) {
                    this.delete(id);
                }
                break;
            case 'duplicate':
                this.duplicate(id);
                break;
            case 'share':
                this.share(id);
                break;
            case 'download':
                this.download(id);
                break;
            case 'view':
                window.location.href = `/view/${id}`;
                break;
        }
    }
    
    async delete(id) {
        try {
            await fetch(`/api/delete/${id}`, { method: 'DELETE' });
            window.toast?.success('Item excluído com sucesso');
            location.reload();
        } catch (error) {
            window.toast?.error('Erro ao excluir item');
        }
    }
    
    async duplicate(id) {
        try {
            await fetch(`/api/duplicate/${id}`, { method: 'POST' });
            window.toast?.success('Item duplicado com sucesso');
            location.reload();
        } catch (error) {
            window.toast?.error('Erro ao duplicar item');
        }
    }
    
    share(id) {
        const url = `${window.location.origin}/share/${id}`;
        navigator.clipboard.writeText(url);
        window.toast?.success('Link copiado para a área de transferência');
    }
    
    async download(id) {
        try {
            window.location.href = `/api/download/${id}`;
            window.toast?.success('Download iniciado');
        } catch (error) {
            window.toast?.error('Erro ao baixar item');
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// INITIALIZE ALL FEATURES
// ═══════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    window.darkMode = new DarkModeManager();
    window.smartSidebar = new SmartSidebar();
    window.globalSearch = new GlobalSearch();
    window.toast = new ToastManager();
    window.keyboardShortcuts = new KeyboardShortcuts();
    window.quickActions = new QuickActions();
    
    console.log('✅ NEXORA Usability Enhancements Loaded');
    
    // Show welcome toast
    setTimeout(() => {
        window.toast?.info('Pressione Ctrl+/ para ver os atalhos de teclado', 5000);
    }, 1000);
});

// ═══════════════════════════════════════════════════════════════════
// 8. AI INSIGHTS (Gráficos com IA)
// ═══════════════════════════════════════════════════════════════════

class AIInsights {
    constructor() {
        this.init();
    }
    
    init() {
        // Add AI insights to charts
        document.querySelectorAll('[data-chart-id]').forEach(chart => {
            this.addInsights(chart);
        });
    }
    
    async addInsights(chartElement) {
        const chartId = chartElement.getAttribute('data-chart-id');
        
        // Create insights container
        const container = document.createElement('div');
        container.className = 'nexora-ai-insights';
        container.innerHTML = `
            <div class="nexora-ai-insights-header">
                <i class="fas fa-robot"></i>
                <span>Insights da IA Velyra</span>
                <div class="nexora-spinner nexora-spinner-sm"></div>
            </div>
            <div class="nexora-ai-insights-content">
                <div class="nexora-skeleton nexora-skeleton-text"></div>
                <div class="nexora-skeleton nexora-skeleton-text"></div>
                <div class="nexora-skeleton nexora-skeleton-text"></div>
            </div>
        `;
        
        chartElement.parentElement.appendChild(container);
        
        // Fetch insights
        try {
            const insights = await this.fetchInsights(chartId);
            this.displayInsights(container, insights);
        } catch (error) {
            console.error('Error fetching insights:', error);
            this.showError(container);
        }
    }
    
    async fetchInsights(chartId) {
        // Simulate API call (replace with actual API)
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Mock insights
        return [
            {
                type: 'positive',
                icon: 'fa-arrow-up',
                text: 'Suas campanhas tiveram um aumento de 28% no ROI este mês.'
            },
            {
                type: 'warning',
                icon: 'fa-exclamation-triangle',
                text: 'O CPA está 15% acima da média. Considere otimizar a segmentação.'
            },
            {
                type: 'info',
                icon: 'fa-lightbulb',
                text: 'Facebook Ads está performando melhor que Instagram. Considere realocar orçamento.'
            }
        ];
    }
    
    displayInsights(container, insights) {
        const header = container.querySelector('.nexora-ai-insights-header');
        header.querySelector('.nexora-spinner').remove();
        
        const content = container.querySelector('.nexora-ai-insights-content');
        content.innerHTML = insights.map(insight => `
            <div class="nexora-ai-insight nexora-ai-insight-${insight.type}">
                <i class="fas ${insight.icon}"></i>
                <span>${insight.text}</span>
            </div>
        `).join('');
    }
    
    showError(container) {
        const content = container.querySelector('.nexora-ai-insights-content');
        content.innerHTML = `
            <div class="nexora-ai-insight nexora-ai-insight-error">
                <i class="fas fa-exclamation-circle"></i>
                <span>Erro ao carregar insights. Tente novamente.</span>
            </div>
        `;
    }
}

// ═══════════════════════════════════════════════════════════════════
// 9. DRAG AND DROP (Arrastar e Soltar)
// ═══════════════════════════════════════════════════════════════════

class DragAndDrop {
    constructor(containerSelector) {
        this.container = document.querySelector(containerSelector);
        this.draggedElement = null;
        
        if (this.container) {
            this.init();
        }
    }
    
    init() {
        // Make items draggable
        this.container.querySelectorAll('[data-draggable="true"]').forEach(item => {
            this.makeDraggable(item);
        });
        
        // Make container droppable
        this.makeDroppable(this.container);
    }
    
    makeDraggable(element) {
        element.setAttribute('draggable', 'true');
        element.classList.add('nexora-draggable');
        
        element.addEventListener('dragstart', (e) => {
            this.draggedElement = element;
            element.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', element.innerHTML);
        });
        
        element.addEventListener('dragend', (e) => {
            element.classList.remove('dragging');
            this.draggedElement = null;
        });
    }
    
    makeDroppable(container) {
        container.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            
            const afterElement = this.getDragAfterElement(container, e.clientY);
            if (afterElement == null) {
                container.appendChild(this.draggedElement);
            } else {
                container.insertBefore(this.draggedElement, afterElement);
            }
        });
        
        container.addEventListener('drop', (e) => {
            e.preventDefault();
            this.onDrop(this.draggedElement);
        });
    }
    
    getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.nexora-draggable:not(.dragging)')];
        
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }
    
    onDrop(element) {
        // Save new order
        const items = [...this.container.querySelectorAll('[data-draggable="true"]')];
        const order = items.map((item, index) => ({
            id: item.getAttribute('data-id'),
            order: index
        }));
        
        // Send to API
        this.saveOrder(order);
        
        // Show toast
        window.toast?.success('Ordem atualizada com sucesso');
    }
    
    async saveOrder(order) {
        try {
            await fetch('/api/update-order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ order })
            });
        } catch (error) {
            console.error('Error saving order:', error);
            window.toast?.error('Erro ao salvar ordem');
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// 10. ONBOARDING (Fluxo Guiado de Criação)
// ═══════════════════════════════════════════════════════════════════

class OnboardingFlow {
    constructor() {
        this.steps = [];
        this.currentStep = 0;
        this.completed = localStorage.getItem('nexora-onboarding-completed') === 'true';
        
        if (!this.completed) {
            this.init();
        }
    }
    
    init() {
        // Define onboarding steps
        this.steps = [
            {
                target: '.nexora-sidebar',
                title: 'Bem-vindo ao NEXORA PRIME!',
                description: 'Esta é a barra lateral de navegação. Aqui você encontra todas as funcionalidades.',
                position: 'right'
            },
            {
                target: '.nexora-dark-mode-toggle',
                title: 'Modo Escuro',
                description: 'Clique aqui para alternar entre modo claro e escuro.',
                position: 'left'
            },
            {
                target: '[href="/campaigns/create"]',
                title: 'Criar Campanha',
                description: 'Comece criando sua primeira campanha. O wizard guiado vai te ajudar em cada passo.',
                position: 'right'
            },
            {
                target: '[href="/reports"]',
                title: 'Relatórios',
                description: 'Acompanhe o desempenho das suas campanhas em tempo real.',
                position: 'right'
            },
            {
                target: 'body',
                title: 'Atalhos de Teclado',
                description: 'Pressione Ctrl+/ para ver todos os atalhos disponíveis. Ctrl+K abre a busca global.',
                position: 'center'
            }
        ];
        
        // Show first step after a delay
        setTimeout(() => this.show(), 1000);
    }
    
    show() {
        if (this.currentStep >= this.steps.length) {
            this.complete();
            return;
        }
        
        const step = this.steps[this.currentStep];
        
        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'nexora-onboarding-overlay';
        
        // Create spotlight
        const spotlight = document.createElement('div');
        spotlight.className = 'nexora-onboarding-spotlight';
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = `nexora-onboarding-tooltip nexora-onboarding-tooltip-${step.position}`;
        tooltip.innerHTML = `
            <div class="nexora-onboarding-tooltip-header">
                <h4>${step.title}</h4>
                <button class="nexora-onboarding-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="nexora-onboarding-tooltip-body">
                <p>${step.description}</p>
            </div>
            <div class="nexora-onboarding-tooltip-footer">
                <div class="nexora-onboarding-progress">
                    ${this.currentStep + 1} de ${this.steps.length}
                </div>
                <div class="nexora-onboarding-actions">
                    ${this.currentStep > 0 ? '<button class="nexora-btn nexora-btn-ghost nexora-btn-sm nexora-onboarding-prev">Anterior</button>' : ''}
                    <button class="nexora-btn nexora-btn-primary nexora-btn-sm nexora-onboarding-next">
                        ${this.currentStep === this.steps.length - 1 ? 'Concluir' : 'Próximo'}
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(overlay);
        document.body.appendChild(spotlight);
        document.body.appendChild(tooltip);
        
        // Position spotlight and tooltip
        if (step.target !== 'body') {
            const target = document.querySelector(step.target);
            if (target) {
                const rect = target.getBoundingClientRect();
                
                spotlight.style.top = `${rect.top - 10}px`;
                spotlight.style.left = `${rect.left - 10}px`;
                spotlight.style.width = `${rect.width + 20}px`;
                spotlight.style.height = `${rect.height + 20}px`;
                
                this.positionTooltip(tooltip, rect, step.position);
            }
        } else {
            spotlight.style.display = 'none';
            tooltip.style.top = '50%';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translate(-50%, -50%)';
        }
        
        // Add event listeners
        tooltip.querySelector('.nexora-onboarding-close').onclick = () => this.skip();
        tooltip.querySelector('.nexora-onboarding-next').onclick = () => this.next();
        
        const prevBtn = tooltip.querySelector('.nexora-onboarding-prev');
        if (prevBtn) {
            prevBtn.onclick = () => this.prev();
        }
        
        overlay.onclick = () => this.skip();
    }
    
    positionTooltip(tooltip, targetRect, position) {
        const tooltipRect = tooltip.getBoundingClientRect();
        
        switch (position) {
            case 'right':
                tooltip.style.top = `${targetRect.top + targetRect.height / 2 - tooltipRect.height / 2}px`;
                tooltip.style.left = `${targetRect.right + 20}px`;
                break;
            case 'left':
                tooltip.style.top = `${targetRect.top + targetRect.height / 2 - tooltipRect.height / 2}px`;
                tooltip.style.left = `${targetRect.left - tooltipRect.width - 20}px`;
                break;
            case 'top':
                tooltip.style.top = `${targetRect.top - tooltipRect.height - 20}px`;
                tooltip.style.left = `${targetRect.left + targetRect.width / 2 - tooltipRect.width / 2}px`;
                break;
            case 'bottom':
                tooltip.style.top = `${targetRect.bottom + 20}px`;
                tooltip.style.left = `${targetRect.left + targetRect.width / 2 - tooltipRect.width / 2}px`;
                break;
        }
    }
    
    hide() {
        document.querySelector('.nexora-onboarding-overlay')?.remove();
        document.querySelector('.nexora-onboarding-spotlight')?.remove();
        document.querySelector('.nexora-onboarding-tooltip')?.remove();
    }
    
    next() {
        this.hide();
        this.currentStep++;
        this.show();
    }
    
    prev() {
        this.hide();
        this.currentStep--;
        this.show();
    }
    
    skip() {
        this.hide();
        this.complete();
    }
    
    complete() {
        this.hide();
        localStorage.setItem('nexora-onboarding-completed', 'true');
        window.toast?.success('Onboarding concluído! Explore o NEXORA PRIME.', 5000);
    }
    
    reset() {
        localStorage.removeItem('nexora-onboarding-completed');
        this.completed = false;
        this.currentStep = 0;
        this.init();
    }
}

// ═══════════════════════════════════════════════════════════════════
// UPDATE INITIALIZATION
// ═══════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    window.darkMode = new DarkModeManager();
    window.smartSidebar = new SmartSidebar();
    window.globalSearch = new GlobalSearch();
    window.toast = new ToastManager();
    window.keyboardShortcuts = new KeyboardShortcuts();
    window.quickActions = new QuickActions();
    window.aiInsights = new AIInsights();
    window.dragAndDrop = new DragAndDrop('[data-sortable="true"]');
    window.onboarding = new OnboardingFlow();
    
    console.log('✅ NEXORA Usability Enhancements Loaded (10/10 features)');
    
    // Show welcome toast
    setTimeout(() => {
        window.toast?.info('Pressione Ctrl+/ para ver os atalhos de teclado', 5000);
    }, 1000);
});

/**
 * UX Enhancements - NEXORA PRIME v11.7
 * Lazy loading, loading states, mobile optimizations
 */

// ========== LAZY LOADING DE IMAGENS ==========

class LazyLoader {
    constructor() {
        this.images = document.querySelectorAll('img[loading="lazy"]');
        this.imageObserver = null;
        this.init();
    }
    
    init() {
        if ('IntersectionObserver' in window) {
            this.imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        observer.unobserve(img);
                    }
                });
            });
            
            this.images.forEach(img => this.imageObserver.observe(img));
        } else {
            // Fallback para navegadores antigos
            this.images.forEach(img => this.loadImage(img));
        }
    }
    
    loadImage(img) {
        const src = img.dataset.src || img.src;
        if (src) {
            img.src = src;
            img.onload = () => {
                img.classList.add('loaded');
            };
        }
    }
}

// ========== LOADING STATES ==========

class LoadingManager {
    constructor() {
        this.overlay = null;
        this.createOverlay();
    }
    
    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'loading-overlay';
        this.overlay.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner-large"></div>
                <p>Carregando...</p>
            </div>
        `;
        document.body.appendChild(this.overlay);
    }
    
    show(message = 'Carregando...') {
        if (this.overlay) {
            this.overlay.querySelector('p').textContent = message;
            this.overlay.classList.add('active');
        }
    }
    
    hide() {
        if (this.overlay) {
            this.overlay.classList.remove('active');
        }
    }
    
    // Loading state para botões
    setButtonLoading(button, loading = true) {
        if (loading) {
            button.classList.add('btn-loading');
            button.disabled = true;
            button.dataset.originalText = button.textContent;
        } else {
            button.classList.remove('btn-loading');
            button.disabled = false;
            if (button.dataset.originalText) {
                button.textContent = button.dataset.originalText;
            }
        }
    }
    
    // Loading state para formulários
    setFormLoading(form, loading = true) {
        const inputs = form.querySelectorAll('input, select, textarea, button');
        inputs.forEach(input => {
            input.disabled = loading;
        });
        
        const submitBtn = form.querySelector('[type="submit"]');
        if (submitBtn) {
            this.setButtonLoading(submitBtn, loading);
        }
    }
}

// ========== MOBILE OPTIMIZATIONS ==========

class MobileOptimizer {
    constructor() {
        this.isMobile = window.innerWidth <= 768;
        this.sidebar = document.querySelector('.sidebar');
        this.sidebarOverlay = null;
        this.init();
    }
    
    init() {
        this.createSidebarOverlay();
        this.setupMobileMenu();
        this.setupTouchOptimizations();
        this.setupResponsiveImages();
        
        // Atualizar em resize
        window.addEventListener('resize', () => {
            this.isMobile = window.innerWidth <= 768;
        });
    }
    
    createSidebarOverlay() {
        if (!this.sidebar) return;
        
        this.sidebarOverlay = document.createElement('div');
        this.sidebarOverlay.className = 'sidebar-overlay';
        document.body.appendChild(this.sidebarOverlay);
        
        this.sidebarOverlay.addEventListener('click', () => {
            this.closeSidebar();
        });
    }
    
    setupMobileMenu() {
        // Botão de menu mobile
        const menuBtn = document.querySelector('.mobile-menu-btn');
        if (menuBtn) {
            menuBtn.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }
        
        // Fechar sidebar ao clicar em link (mobile)
        if (this.sidebar) {
            const links = this.sidebar.querySelectorAll('a');
            links.forEach(link => {
                link.addEventListener('click', () => {
                    if (this.isMobile) {
                        this.closeSidebar();
                    }
                });
            });
        }
    }
    
    toggleSidebar() {
        if (!this.sidebar || !this.sidebarOverlay) return;
        
        this.sidebar.classList.toggle('active');
        this.sidebarOverlay.classList.toggle('active');
        document.body.style.overflow = this.sidebar.classList.contains('active') ? 'hidden' : '';
    }
    
    closeSidebar() {
        if (!this.sidebar || !this.sidebarOverlay) return;
        
        this.sidebar.classList.remove('active');
        this.sidebarOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    setupTouchOptimizations() {
        // Prevenir zoom duplo-toque em iOS
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (e) => {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
        
        // Smooth scrolling para âncoras
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    setupResponsiveImages() {
        // Detectar suporte a WebP
        const supportsWebP = () => {
            const canvas = document.createElement('canvas');
            if (canvas.getContext && canvas.getContext('2d')) {
                return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
            }
            return false;
        };
        
        if (supportsWebP()) {
            document.documentElement.classList.add('webp');
        } else {
            document.documentElement.classList.add('no-webp');
        }
    }
}

// ========== SKELETON LOADING ==========

class SkeletonLoader {
    static createSkeleton(type = 'card') {
        const templates = {
            card: `
                <div class="skeleton-card">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text" style="width: 80%"></div>
                </div>
            `,
            list: `
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text" style="width: 90%"></div>
            `,
            table: `
                <div class="skeleton skeleton-text" style="height: 40px; margin-bottom: 16px;"></div>
                <div class="skeleton skeleton-text" style="height: 40px; margin-bottom: 16px;"></div>
                <div class="skeleton skeleton-text" style="height: 40px;"></div>
            `
        };
        
        return templates[type] || templates.card;
    }
    
    static showSkeleton(container, type = 'card', count = 3) {
        container.innerHTML = '';
        for (let i = 0; i < count; i++) {
            container.innerHTML += this.createSkeleton(type);
        }
    }
    
    static hideSkeleton(container, content) {
        container.innerHTML = content;
    }
}

// ========== PERFORMANCE OPTIMIZATIONS ==========

class PerformanceOptimizer {
    constructor() {
        this.init();
    }
    
    init() {
        // Debounce para eventos de scroll e resize
        this.setupDebounce();
        
        // Lazy load de componentes pesados
        this.lazyLoadComponents();
        
        // Prefetch de páginas importantes
        this.prefetchPages();
    }
    
    setupDebounce() {
        // Debounce helper
        const debounce = (func, wait) => {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        };
        
        // Aplicar debounce em eventos de scroll
        const scrollHandler = debounce(() => {
            // Lógica de scroll
        }, 100);
        
        window.addEventListener('scroll', scrollHandler);
        
        // Aplicar debounce em eventos de resize
        const resizeHandler = debounce(() => {
            // Lógica de resize
        }, 250);
        
        window.addEventListener('resize', resizeHandler);
    }
    
    lazyLoadComponents() {
        // Lazy load de gráficos e componentes pesados
        const heavyComponents = document.querySelectorAll('[data-lazy-component]');
        
        if ('IntersectionObserver' in window) {
            const componentObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const component = entry.target;
                        const componentType = component.dataset.lazyComponent;
                        this.loadComponent(component, componentType);
                        componentObserver.unobserve(component);
                    }
                });
            });
            
            heavyComponents.forEach(component => componentObserver.observe(component));
        }
    }
    
    loadComponent(element, type) {
        // Carregar componente baseado no tipo
        switch(type) {
            case 'chart':
                // Carregar biblioteca de gráficos
                break;
            case 'map':
                // Carregar mapa
                break;
            default:
                break;
        }
    }
    
    prefetchPages() {
        // Prefetch de páginas importantes
        const importantLinks = document.querySelectorAll('a[data-prefetch]');
        
        if ('IntersectionObserver' in window) {
            const linkObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const link = entry.target;
                        const href = link.getAttribute('href');
                        this.prefetch(href);
                        linkObserver.unobserve(link);
                    }
                });
            });
            
            importantLinks.forEach(link => linkObserver.observe(link));
        }
    }
    
    prefetch(url) {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;
        document.head.appendChild(link);
    }
}

// ========== INICIALIZAÇÃO ==========

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar lazy loader
    window.lazyLoader = new LazyLoader();
    
    // Inicializar loading manager
    window.loadingManager = new LoadingManager();
    
    // Inicializar mobile optimizer
    window.mobileOptimizer = new MobileOptimizer();
    
    // Inicializar performance optimizer
    window.performanceOptimizer = new PerformanceOptimizer();
    
    console.log('✅ UX Enhancements initialized');
});

// ========== EXPORTAR PARA USO GLOBAL ==========

window.UX = {
    LazyLoader,
    LoadingManager,
    MobileOptimizer,
    SkeletonLoader,
    PerformanceOptimizer
};

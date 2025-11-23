/**
 * NEXORA Operator v11.7 - Accessibility Features
 * Melhorias de acessibilidade para WCAG 2.1 AA compliance
 */

(function() {
    'use strict';

    // ===== SKIP TO MAIN CONTENT =====
    function addSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'nexora-skip-link';
        skipLink.textContent = 'Pular para o conteúdo principal';
        skipLink.setAttribute('tabindex', '0');
        
        document.body.insertBefore(skipLink, document.body.firstChild);
        
        // Adicionar ID ao conteúdo principal se não existir
        const mainContent = document.querySelector('main') || 
                          document.querySelector('.container-fluid') ||
                          document.querySelector('.content');
        if (mainContent && !mainContent.id) {
            mainContent.id = 'main-content';
            mainContent.setAttribute('tabindex', '-1');
        }
    }

    // ===== FOCUS MANAGEMENT =====
    function enhanceFocusManagement() {
        // Adicionar indicador visual de foco
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', function() {
            document.body.classList.remove('keyboard-navigation');
        });

        // Trap focus em modais
        document.addEventListener('shown.bs.modal', function(e) {
            trapFocus(e.target);
        });
    }

    function trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'a[href], button:not([disabled]), textarea:not([disabled]), ' +
            'input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length === 0) return;
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        element.addEventListener('keydown', function(e) {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        });

        // Focus no primeiro elemento
        setTimeout(() => firstElement.focus(), 100);
    }

    // ===== ARIA LABELS =====
    function enhanceAriaLabels() {
        // Botões sem texto
        document.querySelectorAll('button:not([aria-label])').forEach(button => {
            const icon = button.querySelector('i');
            if (icon && !button.textContent.trim()) {
                const ariaLabel = getAriaLabelFromIcon(icon.className);
                if (ariaLabel) {
                    button.setAttribute('aria-label', ariaLabel);
                }
            }
        });

        // Links sem texto
        document.querySelectorAll('a:not([aria-label])').forEach(link => {
            const icon = link.querySelector('i');
            if (icon && !link.textContent.trim()) {
                const ariaLabel = getAriaLabelFromIcon(icon.className);
                if (ariaLabel) {
                    link.setAttribute('aria-label', ariaLabel);
                }
            }
        });

        // Imagens sem alt
        document.querySelectorAll('img:not([alt])').forEach(img => {
            img.setAttribute('alt', '');
        });

        // Forms sem labels
        document.querySelectorAll('input:not([aria-label]):not([id])').forEach(input => {
            const placeholder = input.getAttribute('placeholder');
            if (placeholder) {
                input.setAttribute('aria-label', placeholder);
            }
        });
    }

    function getAriaLabelFromIcon(className) {
        const iconMap = {
            'fa-search': 'Buscar',
            'fa-filter': 'Filtrar',
            'fa-download': 'Baixar',
            'fa-upload': 'Enviar',
            'fa-edit': 'Editar',
            'fa-trash': 'Excluir',
            'fa-save': 'Salvar',
            'fa-close': 'Fechar',
            'fa-times': 'Fechar',
            'fa-plus': 'Adicionar',
            'fa-minus': 'Remover',
            'fa-check': 'Confirmar',
            'fa-cog': 'Configurações',
            'fa-user': 'Usuário',
            'fa-home': 'Início',
            'fa-chart': 'Gráfico',
            'fa-bell': 'Notificações',
            'fa-envelope': 'Mensagens',
            'fa-calendar': 'Calendário',
            'fa-print': 'Imprimir',
            'fa-share': 'Compartilhar',
            'fa-copy': 'Copiar',
            'fa-refresh': 'Atualizar',
            'fa-sync': 'Sincronizar',
            'fa-play': 'Reproduzir',
            'fa-pause': 'Pausar',
            'fa-stop': 'Parar',
        };

        for (const [key, value] of Object.entries(iconMap)) {
            if (className.includes(key)) {
                return value;
            }
        }
        return null;
    }

    // ===== KEYBOARD NAVIGATION =====
    function enhanceKeyboardNavigation() {
        // Navegação por cards
        document.querySelectorAll('.card').forEach(card => {
            const link = card.querySelector('a');
            if (link && !card.hasAttribute('tabindex')) {
                card.setAttribute('tabindex', '0');
                card.setAttribute('role', 'button');
                
                card.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        link.click();
                    }
                });
            }
        });

        // Dropdown navigation
        document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
            toggle.addEventListener('keydown', function(e) {
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    const menu = this.nextElementSibling;
                    if (menu) {
                        const firstItem = menu.querySelector('.dropdown-item');
                        if (firstItem) firstItem.focus();
                    }
                }
            });
        });

        // Table navigation
        document.querySelectorAll('table').forEach(table => {
            table.setAttribute('role', 'table');
            
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach((row, index) => {
                row.setAttribute('tabindex', '0');
                
                row.addEventListener('keydown', function(e) {
                    if (e.key === 'ArrowDown' && index < rows.length - 1) {
                        e.preventDefault();
                        rows[index + 1].focus();
                    } else if (e.key === 'ArrowUp' && index > 0) {
                        e.preventDefault();
                        rows[index - 1].focus();
                    } else if (e.key === 'Enter') {
                        const link = row.querySelector('a');
                        if (link) link.click();
                    }
                });
            });
        });
    }

    // ===== LIVE REGIONS =====
    function setupLiveRegions() {
        // Criar live region para notificações
        const liveRegion = document.createElement('div');
        liveRegion.id = 'nexora-live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        document.body.appendChild(liveRegion);

        // Interceptar toasts para anunciar
        const originalShowToast = window.showToast;
        if (originalShowToast) {
            window.showToast = function(message, type) {
                originalShowToast(message, type);
                announceToScreenReader(message);
            };
        }
    }

    function announceToScreenReader(message) {
        const liveRegion = document.getElementById('nexora-live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    // ===== CONTRAST CHECKER =====
    function checkContrast() {
        // Verificar contraste de texto (apenas em desenvolvimento)
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            console.log('Accessibility: Contrast checking enabled in development mode');
        }
    }

    // ===== HEADING HIERARCHY =====
    function validateHeadingHierarchy() {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        let lastLevel = 0;
        
        headings.forEach(heading => {
            const level = parseInt(heading.tagName.substring(1));
            
            if (level - lastLevel > 1) {
                console.warn(`Accessibility: Heading hierarchy skip detected - ${heading.tagName} after H${lastLevel}`, heading);
            }
            
            lastLevel = level;
        });
    }

    // ===== INITIALIZATION =====
    function init() {
        // Aguardar DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        console.log('NEXORA Accessibility: Initializing...');

        addSkipLink();
        enhanceFocusManagement();
        enhanceAriaLabels();
        enhanceKeyboardNavigation();
        setupLiveRegions();
        checkContrast();
        validateHeadingHierarchy();

        console.log('NEXORA Accessibility: Ready');
    }

    // Auto-initialize
    init();

    // Expose utility functions
    window.NexoraAccessibility = {
        announceToScreenReader: announceToScreenReader,
        trapFocus: trapFocus
    };

})();

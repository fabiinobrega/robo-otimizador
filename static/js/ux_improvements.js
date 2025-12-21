/**
 * UX Improvements - Melhorias de Experiência do Usuário
 * Corrige os 4 problemas de UX identificados
 */

// ============================================================================
// PROBLEMA 1: Feedback Visual em Ações Críticas
// ============================================================================

/**
 * Mostra loading em botões durante ações
 */
function showButtonLoading(buttonElement, loadingText = 'Processando...') {
    const originalText = buttonElement.innerHTML;
    buttonElement.dataset.originalText = originalText;
    buttonElement.disabled = true;
    buttonElement.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>${loadingText}`;
}

/**
 * Remove loading dos botões
 */
function hideButtonLoading(buttonElement) {
    const originalText = buttonElement.dataset.originalText || 'Continuar';
    buttonElement.disabled = false;
    buttonElement.innerHTML = originalText;
}

/**
 * Mostra toast de notificação
 */
function showToast(title, message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toastId = `toast-${Date.now()}`;
    const iconMap = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    };
    
    const colorMap = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    };
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${colorMap[type]} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <strong>${iconMap[type]} ${title}</strong><br>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
    toast.show();
    
    // Remove do DOM após fechar
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

/**
 * Cria container de toasts se não existir
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// ============================================================================
// PROBLEMA 2: Estados de Loading
// ============================================================================

/**
 * Mostra overlay de loading global
 */
function showGlobalLoading(message = 'Carregando...') {
    let overlay = document.getElementById('globalLoadingOverlay');
    
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'globalLoadingOverlay';
        overlay.innerHTML = `
            <div class="loading-overlay">
                <div class="loading-content">
                    <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;"></div>
                    <p class="loading-message">${message}</p>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    } else {
        overlay.querySelector('.loading-message').textContent = message;
        overlay.style.display = 'flex';
    }
}

/**
 * Esconde overlay de loading global
 */
function hideGlobalLoading() {
    const overlay = document.getElementById('globalLoadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// ============================================================================
// PROBLEMA 3: Indicadores de Progresso
// ============================================================================

/**
 * Atualiza barra de progresso
 */
function updateProgressBar(progressBarId, percentage, label = '') {
    const progressBar = document.getElementById(progressBarId);
    if (progressBar) {
        progressBar.style.width = `${percentage}%`;
        progressBar.setAttribute('aria-valuenow', percentage);
        if (label) {
            progressBar.textContent = label;
        }
    }
}

/**
 * Cria indicador de progresso de etapas
 */
function createStepIndicator(steps, currentStep) {
    const container = document.createElement('div');
    container.className = 'step-progress mb-4';
    
    steps.forEach((step, index) => {
        const stepNumber = index + 1;
        const isActive = stepNumber === currentStep;
        const isCompleted = stepNumber < currentStep;
        
        const stepElement = document.createElement('div');
        stepElement.className = `step-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`;
        stepElement.innerHTML = `
            <div class="step-circle">${stepNumber}</div>
            <div class="step-label">${step}</div>
        `;
        
        container.appendChild(stepElement);
    });
    
    return container;
}

// ============================================================================
// PROBLEMA 4: Validação de Campos com Feedback Visual
// ============================================================================

/**
 * Valida campo e mostra feedback visual
 */
function validateField(fieldId, validationFn, errorMessage) {
    const field = document.getElementById(fieldId);
    if (!field) return true;
    
    const value = field.value.trim();
    const isValid = validationFn(value);
    
    // Remove feedback anterior
    field.classList.remove('is-valid', 'is-invalid');
    const feedbackElement = field.nextElementSibling;
    if (feedbackElement && feedbackElement.classList.contains('invalid-feedback')) {
        feedbackElement.remove();
    }
    
    if (!isValid) {
        field.classList.add('is-invalid');
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = errorMessage;
        field.parentNode.insertBefore(feedback, field.nextSibling);
        return false;
    } else {
        field.classList.add('is-valid');
        return true;
    }
}

/**
 * Valida formulário completo
 */
function validateForm(formId, validations) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let allValid = true;
    
    validations.forEach(validation => {
        const isValid = validateField(
            validation.fieldId,
            validation.validationFn,
            validation.errorMessage
        );
        if (!isValid) allValid = false;
    });
    
    return allValid;
}

// ============================================================================
// Confirmação de Sucesso/Falha
// ============================================================================

/**
 * Mostra modal de confirmação
 */
function showConfirmation(title, message, type = 'success', onConfirm = null) {
    const modalId = 'confirmationModal';
    let modal = document.getElementById(modalId);
    
    if (!modal) {
        modal = document.createElement('div');
        modal.id = modalId;
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="confirmationTitle"></h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body" id="confirmationMessage"></div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        <button type="button" class="btn btn-primary" id="confirmationBtn">OK</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
    
    const iconMap = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    };
    
    document.getElementById('confirmationTitle').textContent = `${iconMap[type]} ${title}`;
    document.getElementById('confirmationMessage').textContent = message;
    
    const confirmBtn = document.getElementById('confirmationBtn');
    if (onConfirm) {
        confirmBtn.onclick = () => {
            onConfirm();
            bootstrap.Modal.getInstance(modal).hide();
        };
    }
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

// ============================================================================
// CSS para Loading Overlay
// ============================================================================

// Adicionar estilos dinamicamente
const style = document.createElement('style');
style.textContent = `
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9998;
}

.loading-content {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.loading-message {
    margin: 0;
    font-size: 1.1rem;
    color: #333;
}

#globalLoadingOverlay {
    display: none;
}

.step-progress {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.step-item {
    flex: 1;
    text-align: center;
    position: relative;
}

.step-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #e9ecef;
    color: #6c757d;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.5rem;
    font-weight: bold;
    border: 2px solid #dee2e6;
}

.step-item.active .step-circle {
    background: #0d6efd;
    color: white;
    border-color: #0d6efd;
}

.step-item.completed .step-circle {
    background: #198754;
    color: white;
    border-color: #198754;
}

.step-label {
    font-size: 0.875rem;
    color: #6c757d;
}

.step-item.active .step-label {
    color: #0d6efd;
    font-weight: 600;
}
`;
document.head.appendChild(style);

// ============================================================================
// Exportar funções globalmente
// ============================================================================

window.UX = {
    showButtonLoading,
    hideButtonLoading,
    showToast,
    showGlobalLoading,
    hideGlobalLoading,
    updateProgressBar,
    createStepIndicator,
    validateField,
    validateForm,
    showConfirmation
};

/**
 * ================================================================
 * NEXORA PRIME - AD CREATOR ENGINE
 * Sistema de Criação de Anúncios Mais Avançado
 * ================================================================
 */

class AdCreatorEngine {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 6;
        this.formData = {};
        this.uploadedFiles = [];
        this.analysisResults = {};
        
        this.init();
    }

    init() {
        console.log('🚀 Ad Creator Engine inicializado');
        this.setupEventListeners();
        this.updateSummary();
    }

    setupEventListeners() {
        // Mode selector
        document.querySelectorAll('.mode-option').forEach(option => {
            option.addEventListener('click', (e) => {
                document.querySelectorAll('.mode-option').forEach(opt => opt.classList.remove('active'));
                e.currentTarget.classList.add('active');
                document.getElementById('operationMode').value = e.currentTarget.dataset.mode;
                this.updateSummary();
            });
        });

        // Upload area
        const uploadArea = document.getElementById('uploadArea');
        const mediaFiles = document.getElementById('mediaFiles');

        uploadArea.addEventListener('click', () => mediaFiles.click());

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            this.handleFiles(e.dataTransfer.files);
        });

        mediaFiles.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });

        // Form inputs
        const formInputs = [
            'salesPageUrl', 'platform', 'budgetType', 'budgetAmount',
            'country', 'language'
        ];

        formInputs.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.addEventListener('change', () => this.updateSummary());
                element.addEventListener('input', () => this.updateSummary());
            }
        });

        // Step 1 Next button
        document.getElementById('btnStep1Next')?.addEventListener('click', () => {
            this.validateAndProceed();
        });
    }

    handleFiles(files) {
        const uploadedFilesDiv = document.getElementById('uploadedFiles');
        
        Array.from(files).forEach(file => {
            // Validar tamanho (50MB)
            if (file.size > 50 * 1024 * 1024) {
                this.showToast('Arquivo muito grande: ' + file.name, 'error');
                return;
            }

            // Validar tipo
            if (!file.type.startsWith('image/') && !file.type.startsWith('video/')) {
                this.showToast('Tipo de arquivo inválido: ' + file.name, 'error');
                return;
            }

            this.uploadedFiles.push(file);

            // Criar preview
            const fileCard = document.createElement('div');
            fileCard.className = 'file-preview';
            fileCard.innerHTML = `
                <div class="d-flex align-items-center justify-content-between p-3 mb-2" 
                     style="background: var(--nexora-gray-800); border-radius: 8px;">
                    <div class="d-flex align-items-center gap-3">
                        <i class="fas ${file.type.startsWith('image/') ? 'fa-image' : 'fa-video'}" 
                           style="font-size: 1.5rem; color: var(--nexora-primary);"></i>
                        <div>
                            <div style="color: var(--nexora-white); font-weight: 600;">${file.name}</div>
                            <div style="color: var(--nexora-gray-400); font-size: 0.875rem;">
                                ${this.formatFileSize(file.size)}
                            </div>
                        </div>
                    </div>
                    <button class="btn btn-sm btn-secondary" onclick="adCreator.removeFile('${file.name}')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            uploadedFilesDiv.appendChild(fileCard);
        });

        this.updateSummary();
    }

    removeFile(fileName) {
        this.uploadedFiles = this.uploadedFiles.filter(f => f.name !== fileName);
        this.renderUploadedFiles();
        this.updateSummary();
    }

    renderUploadedFiles() {
        const uploadedFilesDiv = document.getElementById('uploadedFiles');
        uploadedFilesDiv.innerHTML = '';
        this.uploadedFiles.forEach(file => {
            // Re-render files (simplified for now)
            const fileCard = document.createElement('div');
            fileCard.innerHTML = `
                <div class="d-flex align-items-center justify-content-between p-3 mb-2" 
                     style="background: var(--nexora-gray-800); border-radius: 8px;">
                    <div class="d-flex align-items-center gap-3">
                        <i class="fas ${file.type.startsWith('image/') ? 'fa-image' : 'fa-video'}" 
                           style="font-size: 1.5rem; color: var(--nexora-primary);"></i>
                        <div>
                            <div style="color: var(--nexora-white); font-weight: 600;">${file.name}</div>
                            <div style="color: var(--nexora-gray-400); font-size: 0.875rem;">
                                ${this.formatFileSize(file.size)}
                            </div>
                        </div>
                    </div>
                    <button class="btn btn-sm btn-secondary" onclick="adCreator.removeFile('${file.name}')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            uploadedFilesDiv.appendChild(fileCard);
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    updateSummary() {
        const summaryContent = document.getElementById('summaryContent');
        
        const salesPageUrl = document.getElementById('salesPageUrl')?.value;
        const platform = document.getElementById('platform')?.value;
        const budgetType = document.getElementById('budgetType')?.value;
        const budgetAmount = document.getElementById('budgetAmount')?.value;
        const country = document.getElementById('country')?.value;
        const language = document.getElementById('language')?.value;
        const mode = document.getElementById('operationMode')?.value;

        if (!salesPageUrl && !platform) {
            summaryContent.innerHTML = `
                <p class="text-gray-400 text-center py-4">
                    <i class="fas fa-info-circle"></i><br>
                    Preencha os campos para ver o resumo
                </p>
            `;
            return;
        }

        const platformNames = {
            'meta': 'Meta Ads (Facebook/Instagram)',
            'google': 'Google Ads'
        };

        const countryNames = {
            'BR': 'Brasil',
            'US': 'Estados Unidos',
            'PT': 'Portugal',
            'ES': 'Espanha',
            'MX': 'México'
        };

        const modeNames = {
            'normal': '⭕ Modo Normal',
            'turbo': '🔥 Modo Escala Agressiva'
        };

        summaryContent.innerHTML = `
            <div class="summary-item">
                <div class="summary-label">Plataforma</div>
                <div class="summary-value">${platformNames[platform] || '-'}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Orçamento</div>
                <div class="summary-value">
                    R$ ${budgetAmount || '0'} ${budgetType === 'daily' ? '/dia' : 'total'}
                </div>
            </div>
            <div class="summary-item">
                <div class="summary-label">País</div>
                <div class="summary-value">${countryNames[country] || '-'}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Modo</div>
                <div class="summary-value">${modeNames[mode] || '-'}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Mídias</div>
                <div class="summary-value">${this.uploadedFiles.length} arquivo(s)</div>
            </div>
        `;
    }

    validateAndProceed() {
        // Validar campos obrigatórios
        const salesPageUrl = document.getElementById('salesPageUrl').value;
        const platform = document.getElementById('platform').value;
        const budgetAmount = document.getElementById('budgetAmount').value;
        const country = document.getElementById('country').value;
        const language = document.getElementById('language').value;

        // Limpar erros anteriores
        document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

        if (!salesPageUrl) {
            document.getElementById('salesPageUrl').classList.add('is-invalid');
            this.showToast('Por favor, insira a URL da página de vendas', 'error');
            document.getElementById('salesPageUrl').focus();
            return;
        }

        if (!platform || platform === '') {
            document.getElementById('platform').classList.add('is-invalid');
            this.showToast('Por favor, selecione uma plataforma', 'error');
            document.getElementById('platform').focus();
            return;
        }

        if (!budgetAmount || budgetAmount < 10) {
            this.showToast('Orçamento mínimo: R$ 10,00', 'error');
            return;
        }

        // Salvar dados
        this.formData = {
            salesPageUrl,
            platform,
            budgetType: document.getElementById('budgetType').value,
            budgetAmount: parseFloat(budgetAmount),
            country,
            language,
            operationMode: document.getElementById('operationMode').value,
            uploadedFiles: this.uploadedFiles.length
        };

        // Iniciar análise IA
        this.startAIAnalysis();
    }

    async startAIAnalysis() {
        // Avançar para step 2
        this.goToStep(2);

        // Mostrar AI status
        this.showAIStatus('analyzing', 'IA Analisando...', 'Velyra + Manus analisando seu produto e mercado...');

        // Criar progresso visual
        const analysisProgress = document.getElementById('analysisProgress');
        analysisProgress.innerHTML = `
            <div class="analysis-step" id="analysis-product">
                <div class="d-flex align-items-center gap-3 mb-3">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div>
                        <div style="color: var(--nexora-white); font-weight: 600;">
                            Analisando Produto
                        </div>
                        <div style="color: var(--nexora-gray-400); font-size: 0.875rem;">
                            Extraindo informações da página de vendas...
                        </div>
                    </div>
                </div>
            </div>
        `;

        try {
            // Chamar API de análise
            const response = await fetch('/api/ad-creator/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.formData)
            });

            if (!response.ok) {
                throw new Error('Erro na análise');
            }

            const result = await response.json();
            this.analysisResults = result;

            // Atualizar progresso
            this.updateAnalysisProgress(result);

        } catch (error) {
            console.error('Erro na análise:', error);
            this.showToast('Erro ao analisar. Tente novamente.', 'error');
            this.goToStep(1);
        }
    }

    updateAnalysisProgress(result) {
        const analysisProgress = document.getElementById('analysisProgress');
        
        // Simular progresso por enquanto (será implementado completamente na próxima sessão)
        analysisProgress.innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle"></i>
                Análise concluída! Próximas etapas serão implementadas na continuação.
            </div>
        `;

        this.hideAIStatus();
    }

    goToStep(step) {
        // Atualizar wizard visual
        document.querySelectorAll('.wizard-step').forEach((el, index) => {
            el.classList.remove('active', 'completed');
            if (index + 1 < step) {
                el.classList.add('completed');
            } else if (index + 1 === step) {
                el.classList.add('active');
            }
        });

        // Esconder todos os steps
        document.querySelectorAll('.wizard-content').forEach(el => {
            el.style.display = 'none';
        });

        // Mostrar step atual
        const currentStepEl = document.getElementById(`step-${step}`);
        if (currentStepEl) {
            currentStepEl.style.display = 'block';
        }

        this.currentStep = step;
    }

    showAIStatus(type, title, message) {
        const aiStatus = document.getElementById('aiStatus');
        const aiStatusTitle = document.getElementById('aiStatusTitle');
        const aiStatusMessage = document.getElementById('aiStatusMessage');

        aiStatusTitle.textContent = title;
        aiStatusMessage.textContent = message;
        aiStatus.style.display = 'flex';
    }

    hideAIStatus() {
        const aiStatus = document.getElementById('aiStatus');
        aiStatus.style.display = 'none';
    }

    showToast(message, type = 'info') {
        // Usar sistema de toast do NEXORA se disponível
        if (window.NEXORA && window.NEXORA.showToast) {
            window.NEXORA.showToast(message, type);
            return;
        }

        // Fallback: implementação própria
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : 'success'}`;
        toast.style.cssText = `
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 99999;
            min-width: 300px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease-out;
        `;
        toast.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
            ${message}
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Inicializar quando o DOM estiver pronto
let adCreator;
document.addEventListener('DOMContentLoaded', () => {
    adCreator = new AdCreatorEngine();
});

// Adicionar estilos do summary
const summaryStyles = document.createElement('style');
summaryStyles.textContent = `
    .summary-item {
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--nexora-gray-800);
    }
    .summary-item:last-child {
        border-bottom: none;
    }
    .summary-label {
        font-size: 0.8125rem;
        color: var(--nexora-gray-400);
        margin-bottom: 0.25rem;
    }
    .summary-value {
        font-size: 0.9375rem;
        font-weight: 600;
        color: var(--nexora-white);
    }
`;
document.head.appendChild(summaryStyles);

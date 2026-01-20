/**
 * ================================================================
 * NEXORA PRIME - AD CREATOR ENGINE v2.0
 * Sistema de Criação de Anúncios Mais Avançado
 * CORREÇÃO COMPLETA: Inicialização, Toast, Wizard
 * ================================================================
 */

(function() {
    'use strict';
    
    console.log('📦 Ad Creator Engine v2.0 - Script carregado');

    class AdCreatorEngine {
        constructor() {
            console.log('🔧 AdCreatorEngine constructor iniciado');
            this.currentStep = 1;
            this.totalSteps = 6;
            this.formData = {};
            this.uploadedFiles = [];
            this.analysisResults = {};
            this.initialized = false;
            
            this.init();
        }

        init() {
            console.log('🚀 Ad Creator Engine init() chamado');
            
            // Verificar se elementos existem
            const platform = document.getElementById('platform');
            const btnNext = document.getElementById('btnStep1Next');
            
            console.log('📋 Elementos encontrados:', {
                platform: !!platform,
                btnNext: !!btnNext,
                salesPageUrl: !!document.getElementById('salesPageUrl')
            });
            
            if (!platform) {
                console.error('❌ Elemento platform não encontrado!');
                return;
            }
            
            this.setupEventListeners();
            this.updateSummary();
            this.ensureToastContainer();
            this.initialized = true;
            
            console.log('✅ Ad Creator Engine inicializado com sucesso!');
        }

        ensureToastContainer() {
            // Garantir que existe um container de toast
            let toastContainer = document.getElementById('nexora-toast-container');
            if (!toastContainer) {
                toastContainer = document.createElement('div');
                toastContainer.id = 'nexora-toast-container';
                toastContainer.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 999999;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    pointer-events: none;
                `;
                document.body.appendChild(toastContainer);
                console.log('🍞 Toast container criado');
            }
        }

        setupEventListeners() {
            console.log('🎯 Configurando event listeners...');
            
            // Mode selector
            document.querySelectorAll('.mode-option').forEach(option => {
                option.addEventListener('click', (e) => {
                    console.log('🔘 Mode option clicado:', e.currentTarget.dataset.mode);
                    document.querySelectorAll('.mode-option').forEach(opt => opt.classList.remove('active'));
                    e.currentTarget.classList.add('active');
                    const operationMode = document.getElementById('operationMode');
                    if (operationMode) {
                        operationMode.value = e.currentTarget.dataset.mode;
                    }
                    this.updateSummary();
                });
            });

            // Upload area
            const uploadArea = document.getElementById('uploadArea');
            const mediaFiles = document.getElementById('mediaFiles');

            if (uploadArea && mediaFiles) {
                uploadArea.addEventListener('click', () => {
                    console.log('📁 Upload area clicado');
                    mediaFiles.click();
                });

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
                    console.log('📥 Arquivos dropados:', e.dataTransfer.files.length);
                    this.handleFiles(e.dataTransfer.files);
                });

                mediaFiles.addEventListener('change', (e) => {
                    console.log('📂 Arquivos selecionados:', e.target.files.length);
                    this.handleFiles(e.target.files);
                });
            }

            // Form inputs - com logging
            const formInputs = [
                'salesPageUrl', 'platform', 'budgetType', 'budgetAmount',
                'country', 'language'
            ];

            formInputs.forEach(id => {
                const element = document.getElementById(id);
                if (element) {
                    element.addEventListener('change', (e) => {
                        console.log(`📝 Campo ${id} alterado:`, e.target.value);
                        this.updateSummary();
                    });
                    element.addEventListener('input', () => this.updateSummary());
                } else {
                    console.warn(`⚠️ Elemento ${id} não encontrado`);
                }
            });

            // Step 1 Next button - CRÍTICO
            const btnStep1Next = document.getElementById('btnStep1Next');
            if (btnStep1Next) {
                btnStep1Next.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('🚀 Botão "Iniciar Análise IA" clicado');
                    this.validateAndProceed();
                });
                console.log('✅ Event listener do botão btnStep1Next configurado');
            } else {
                console.error('❌ Botão btnStep1Next não encontrado!');
            }
        }

        handleFiles(files) {
            const uploadedFilesDiv = document.getElementById('uploadedFiles');
            if (!uploadedFilesDiv) {
                console.error('❌ uploadedFiles div não encontrado');
                return;
            }
            
            Array.from(files).forEach(file => {
                console.log('📄 Processando arquivo:', file.name, file.size, file.type);
                
                // Validar tamanho (50MB)
                if (file.size > 50 * 1024 * 1024) {
                    this.showToast('Arquivo muito grande: ' + file.name + ' (máx. 50MB)', 'error');
                    return;
                }

                // Validar tipo
                if (!file.type.startsWith('image/') && !file.type.startsWith('video/')) {
                    this.showToast('Tipo de arquivo inválido: ' + file.name, 'error');
                    return;
                }

                this.uploadedFiles.push(file);
                console.log('✅ Arquivo adicionado:', file.name);

                // Criar preview
                const fileCard = document.createElement('div');
                fileCard.className = 'file-preview';
                fileCard.innerHTML = `
                    <div class="d-flex align-items-center justify-content-between p-3 mb-2" 
                         style="background: var(--nexora-gray-800, #1f2937); border-radius: 8px; border: 1px solid var(--nexora-gray-700, #374151);">
                        <div class="d-flex align-items-center gap-3">
                            <i class="fas ${file.type.startsWith('image/') ? 'fa-image' : 'fa-video'}" 
                               style="font-size: 1.5rem; color: var(--nexora-primary, #6366f1);"></i>
                            <div>
                                <div style="color: var(--nexora-white, #fff); font-weight: 600;">${file.name}</div>
                                <div style="color: var(--nexora-gray-400, #9ca3af); font-size: 0.875rem;">
                                    ${this.formatFileSize(file.size)}
                                </div>
                            </div>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" onclick="window.adCreatorEngine.removeFile('${file.name}')">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `;
                uploadedFilesDiv.appendChild(fileCard);
            });

            this.updateSummary();
            
            if (this.uploadedFiles.length > 0) {
                this.showToast(`${this.uploadedFiles.length} arquivo(s) carregado(s)`, 'success');
            }
        }

        removeFile(fileName) {
            console.log('🗑️ Removendo arquivo:', fileName);
            this.uploadedFiles = this.uploadedFiles.filter(f => f.name !== fileName);
            this.renderUploadedFiles();
            this.updateSummary();
        }

        renderUploadedFiles() {
            const uploadedFilesDiv = document.getElementById('uploadedFiles');
            if (!uploadedFilesDiv) return;
            
            uploadedFilesDiv.innerHTML = '';
            this.uploadedFiles.forEach(file => {
                const fileCard = document.createElement('div');
                fileCard.innerHTML = `
                    <div class="d-flex align-items-center justify-content-between p-3 mb-2" 
                         style="background: var(--nexora-gray-800, #1f2937); border-radius: 8px; border: 1px solid var(--nexora-gray-700, #374151);">
                        <div class="d-flex align-items-center gap-3">
                            <i class="fas ${file.type.startsWith('image/') ? 'fa-image' : 'fa-video'}" 
                               style="font-size: 1.5rem; color: var(--nexora-primary, #6366f1);"></i>
                            <div>
                                <div style="color: var(--nexora-white, #fff); font-weight: 600;">${file.name}</div>
                                <div style="color: var(--nexora-gray-400, #9ca3af); font-size: 0.875rem;">
                                    ${this.formatFileSize(file.size)}
                                </div>
                            </div>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" onclick="window.adCreatorEngine.removeFile('${file.name}')">
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
            if (!summaryContent) return;
            
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
            console.log('🔍 Iniciando validação...');
            
            // Validar campos obrigatórios
            const salesPageUrl = document.getElementById('salesPageUrl')?.value?.trim();
            const platform = document.getElementById('platform')?.value;
            const budgetAmount = document.getElementById('budgetAmount')?.value;
            const country = document.getElementById('country')?.value;
            const language = document.getElementById('language')?.value;

            console.log('📋 Valores do formulário:', {
                salesPageUrl,
                platform,
                budgetAmount,
                country,
                language
            });

            // Limpar erros anteriores
            document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

            // Validação 1: URL da página de vendas
            if (!salesPageUrl) {
                const urlInput = document.getElementById('salesPageUrl');
                if (urlInput) {
                    urlInput.classList.add('is-invalid');
                    urlInput.focus();
                }
                this.showToast('Por favor, insira a URL da página de vendas', 'error');
                console.log('❌ Validação falhou: URL vazia');
                return false;
            }

            // Validação 2: Plataforma
            if (!platform || platform === '') {
                const platformSelect = document.getElementById('platform');
                if (platformSelect) {
                    platformSelect.classList.add('is-invalid');
                    platformSelect.focus();
                }
                this.showToast('Por favor, selecione uma plataforma', 'error');
                console.log('❌ Validação falhou: Plataforma não selecionada');
                return false;
            }

            // Validação 3: Orçamento
            if (!budgetAmount || parseFloat(budgetAmount) < 10) {
                const budgetInput = document.getElementById('budgetAmount');
                if (budgetInput) {
                    budgetInput.classList.add('is-invalid');
                    budgetInput.focus();
                }
                this.showToast('Orçamento mínimo: R$ 10,00', 'error');
                console.log('❌ Validação falhou: Orçamento inválido');
                return false;
            }

            console.log('✅ Validação passou! Salvando dados...');

            // Salvar dados
            this.formData = {
                salesPageUrl,
                platform,
                budgetType: document.getElementById('budgetType')?.value || 'daily',
                budgetAmount: parseFloat(budgetAmount),
                country: country || 'BR',
                language: language || 'pt-BR',
                operationMode: document.getElementById('operationMode')?.value || 'normal',
                uploadedFiles: this.uploadedFiles.length
            };

            console.log('💾 Dados salvos:', this.formData);
            
            // Mostrar toast de sucesso
            this.showToast('Configuração validada! Iniciando análise...', 'success');

            // Iniciar análise
            this.startAIAnalysis();
            return true;
        }

        async startAIAnalysis() {
            console.log('🤖 Iniciando análise IA...');
            
            // Avançar para step 2
            this.goToStep(2);

            // Mostrar AI status
            this.showAIStatus('analyzing', 'IA Analisando...', 'Velyra + Manus analisando seu produto e mercado...');

            // Criar progresso visual
            const analysisProgress = document.getElementById('analysisProgress');
            if (analysisProgress) {
                analysisProgress.innerHTML = `
                    <div class="analysis-step" id="analysis-product">
                        <div class="d-flex align-items-center gap-3 mb-3">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <div>
                                <div style="color: var(--nexora-white, #fff); font-weight: 600;">
                                    Analisando Produto
                                </div>
                                <div style="color: var(--nexora-gray-400, #9ca3af); font-size: 0.875rem;">
                                    Extraindo informações da página de vendas...
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }

            try {
                console.log('📡 Chamando API /api/ad-creator/analyze...');
                
                // Chamar API de análise
                const response = await fetch('/api/ad-creator/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.formData)
                });

                console.log('📥 Resposta recebida:', response.status);

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('❌ Erro na resposta:', errorText);
                    throw new Error('Erro na análise: ' + response.status);
                }

                const result = await response.json();
                console.log('✅ Resultado da análise:', result);
                
                this.analysisResults = result;

                // Atualizar progresso
                this.updateAnalysisProgress(result);

            } catch (error) {
                console.error('❌ Erro na análise:', error);
                this.showToast('Erro ao analisar. Tente novamente.', 'error');
                this.goToStep(1);
            }
        }

        updateAnalysisProgress(result) {
            const analysisProgress = document.getElementById('analysisProgress');
            if (!analysisProgress) return;
            
            analysisProgress.innerHTML = `
                <div class="alert alert-success" style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); color: #22c55e;">
                    <i class="fas fa-check-circle me-2"></i>
                    Análise concluída com sucesso!
                </div>
                <div class="mt-3 p-3" style="background: var(--nexora-gray-800, #1f2937); border-radius: 8px;">
                    <h5 style="color: var(--nexora-white, #fff);">Resultado da Análise</h5>
                    <pre style="color: var(--nexora-gray-300, #d1d5db); font-size: 0.875rem; white-space: pre-wrap;">${JSON.stringify(result, null, 2)}</pre>
                </div>
            `;

            this.hideAIStatus();
            this.showToast('Análise concluída! Revise os resultados.', 'success');
        }

        goToStep(step) {
            console.log('📍 Navegando para step:', step);
            
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
                console.log('✅ Step', step, 'exibido');
            } else {
                console.warn('⚠️ Elemento step-' + step + ' não encontrado');
            }

            this.currentStep = step;
        }

        showAIStatus(type, title, message) {
            const aiStatus = document.getElementById('aiStatus');
            const aiStatusTitle = document.getElementById('aiStatusTitle');
            const aiStatusMessage = document.getElementById('aiStatusMessage');

            if (aiStatusTitle) aiStatusTitle.textContent = title;
            if (aiStatusMessage) aiStatusMessage.textContent = message;
            if (aiStatus) aiStatus.style.display = 'flex';
        }

        hideAIStatus() {
            const aiStatus = document.getElementById('aiStatus');
            if (aiStatus) aiStatus.style.display = 'none';
        }

        showToast(message, type = 'info') {
            console.log('🍞 Toast:', type, '-', message);
            
            // Garantir container existe
            this.ensureToastContainer();
            
            const container = document.getElementById('nexora-toast-container');
            if (!container) {
                console.error('❌ Toast container não encontrado');
                alert(message); // Fallback
                return;
            }

            // Criar toast
            const toast = document.createElement('div');
            toast.className = 'nexora-toast';
            
            const bgColor = type === 'error' ? 'rgba(239, 68, 68, 0.95)' : 
                           type === 'success' ? 'rgba(34, 197, 94, 0.95)' : 
                           'rgba(59, 130, 246, 0.95)';
            
            const icon = type === 'error' ? 'fa-exclamation-circle' : 
                        type === 'success' ? 'fa-check-circle' : 
                        'fa-info-circle';
            
            toast.style.cssText = `
                background: ${bgColor};
                color: white;
                padding: 16px 24px;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                display: flex;
                align-items: center;
                gap: 12px;
                min-width: 320px;
                max-width: 450px;
                font-size: 14px;
                font-weight: 500;
                pointer-events: auto;
                animation: toastSlideIn 0.4s ease-out;
                backdrop-filter: blur(10px);
            `;
            
            toast.innerHTML = `
                <i class="fas ${icon}" style="font-size: 20px;"></i>
                <span>${message}</span>
            `;
            
            container.appendChild(toast);

            // Remover após 4 segundos
            setTimeout(() => {
                toast.style.animation = 'toastSlideOut 0.4s ease-in forwards';
                setTimeout(() => toast.remove(), 400);
            }, 4000);
        }
    }

    // Adicionar estilos globais
    const styles = document.createElement('style');
    styles.textContent = `
        @keyframes toastSlideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes toastSlideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        .summary-item {
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--nexora-gray-800, #1f2937);
        }
        .summary-item:last-child {
            border-bottom: none;
        }
        .summary-label {
            font-size: 0.8125rem;
            color: var(--nexora-gray-400, #9ca3af);
            margin-bottom: 0.25rem;
        }
        .summary-value {
            font-size: 0.9375rem;
            font-weight: 600;
            color: var(--nexora-white, #fff);
        }
        
        .is-invalid {
            border-color: #ef4444 !important;
            box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2) !important;
        }
        
        .upload-area.drag-over {
            border-color: var(--nexora-primary, #6366f1) !important;
            background: rgba(99, 102, 241, 0.1) !important;
        }
    `;
    document.head.appendChild(styles);

    // ================================================================
    // INICIALIZAÇÃO ROBUSTA
    // ================================================================
    function initializeEngine() {
        console.log('🎯 Tentando inicializar Ad Creator Engine...');
        
        // Verificar se já foi inicializado
        if (window.adCreatorEngine && window.adCreatorEngine.initialized) {
            console.log('⚠️ Engine já inicializado, ignorando');
            return;
        }
        
        // Verificar se elementos existem
        const platform = document.getElementById('platform');
        if (!platform) {
            console.log('⏳ Elementos ainda não disponíveis, aguardando...');
            return false;
        }
        
        // Criar instância
        window.adCreatorEngine = new AdCreatorEngine();
        window.adCreator = window.adCreatorEngine; // Alias para compatibilidade
        
        console.log('🎉 Ad Creator Engine v2.0 pronto!');
        return true;
    }

    // Tentar inicializar imediatamente se DOM já estiver pronto
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        console.log('📄 DOM já está pronto, inicializando...');
        setTimeout(initializeEngine, 0);
    }
    
    // Também escutar DOMContentLoaded como fallback
    document.addEventListener('DOMContentLoaded', () => {
        console.log('📄 DOMContentLoaded disparado');
        initializeEngine();
    });
    
    // Fallback final: tentar após 500ms
    setTimeout(() => {
        if (!window.adCreatorEngine || !window.adCreatorEngine.initialized) {
            console.log('⏰ Fallback timeout - tentando inicializar...');
            initializeEngine();
        }
    }, 500);
    
    // Fallback extra: tentar após 1s
    setTimeout(() => {
        if (!window.adCreatorEngine || !window.adCreatorEngine.initialized) {
            console.log('⏰ Fallback extra timeout - tentando inicializar...');
            initializeEngine();
        }
    }, 1000);

})();

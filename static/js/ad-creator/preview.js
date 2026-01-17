/**
 * FASE 8: Pré-visualização Obrigatória de Anúncios
 * 
 * Permite visualizar e editar TODOS os campos dos anúncios antes da execução.
 */

class AdPreviewManager {
    constructor() {
        this.ads = [];
        this.selectedAdIndex = 0;
        this.editMode = false;
    }

    /**
     * Inicializar pré-visualização com anúncios criados
     */
    init(ads) {
        this.ads = ads;
        this.render();
        this.attachEventListeners();
    }

    /**
     * Renderizar interface de pré-visualização
     */
    render() {
        const container = document.getElementById('preview-container');
        if (!container) return;

        container.innerHTML = `
            <div class="preview-wrapper">
                <!-- Lista de anúncios -->
                <div class="ads-list">
                    <h3>Anúncios Criados (${this.ads.length})</h3>
                    <div class="ads-grid">
                        ${this.ads.map((ad, index) => this.renderAdCard(ad, index)).join('')}
                    </div>
                </div>

                <!-- Preview detalhado -->
                <div class="ad-detail-preview">
                    ${this.renderDetailedPreview()}
                </div>

                <!-- Ações -->
                <div class="preview-actions">
                    <button class="btn-secondary" onclick="adPreview.goBack()">
                        ← Voltar
                    </button>
                    <button class="btn-primary" onclick="adPreview.approveAndExecute()">
                        ✓ Aprovar e Executar
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Renderizar card de anúncio na lista
     */
    renderAdCard(ad, index) {
        const isSelected = index === this.selectedAdIndex;
        
        return `
            <div class="ad-card ${isSelected ? 'selected' : ''}" 
                 onclick="adPreview.selectAd(${index})">
                <div class="ad-card-header">
                    <span class="ad-number">#${index + 1}</span>
                    <span class="ad-status">${ad.status}</span>
                </div>
                <div class="ad-card-preview">
                    ${ad.creative.type === 'image' ? 
                        `<img src="${ad.creative.url || '/static/img/placeholder.jpg'}" alt="Creative">` :
                        `<div class="video-placeholder">📹 Vídeo</div>`
                    }
                </div>
                <div class="ad-card-copy">
                    <strong>${ad.copy.headline}</strong>
                    <p>${ad.copy.primary_text.substring(0, 50)}...</p>
                </div>
                <div class="ad-card-actions">
                    <button class="btn-icon" onclick="adPreview.editAd(${index}); event.stopPropagation();">
                        ✏️ Editar
                    </button>
                    <button class="btn-icon" onclick="adPreview.duplicateAd(${index}); event.stopPropagation();">
                        📋 Duplicar
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Renderizar preview detalhado do anúncio selecionado
     */
    renderDetailedPreview() {
        if (this.ads.length === 0) {
            return '<p>Nenhum anúncio criado ainda.</p>';
        }

        const ad = this.ads[this.selectedAdIndex];
        
        return `
            <div class="detailed-preview">
                <h3>Preview: ${ad.name}</h3>
                
                <!-- Preview visual do anúncio -->
                <div class="ad-preview-mockup">
                    ${this.renderAdMockup(ad)}
                </div>

                <!-- Campos editáveis -->
                <div class="ad-fields-editor">
                    <h4>Editar Campos</h4>
                    
                    <div class="form-group">
                        <label>Headline</label>
                        <input type="text" 
                               id="edit-headline-${this.selectedAdIndex}"
                               value="${ad.copy.headline}"
                               maxlength="40"
                               ${!this.editMode ? 'disabled' : ''}>
                        <small>${ad.copy.headline.length}/40 caracteres</small>
                    </div>

                    <div class="form-group">
                        <label>Texto Principal</label>
                        <textarea id="edit-primary-text-${this.selectedAdIndex}"
                                  rows="4"
                                  maxlength="125"
                                  ${!this.editMode ? 'disabled' : ''}>${ad.copy.primary_text}</textarea>
                        <small>${ad.copy.primary_text.length}/125 caracteres</small>
                    </div>

                    <div class="form-group">
                        <label>Descrição</label>
                        <input type="text"
                               id="edit-description-${this.selectedAdIndex}"
                               value="${ad.copy.description}"
                               maxlength="30"
                               ${!this.editMode ? 'disabled' : ''}>
                        <small>${ad.copy.description.length}/30 caracteres</small>
                    </div>

                    <div class="form-group">
                        <label>Call to Action</label>
                        <select id="edit-cta-${this.selectedAdIndex}"
                                ${!this.editMode ? 'disabled' : ''}>
                            <option value="SHOP_NOW" ${ad.copy.call_to_action === 'SHOP_NOW' ? 'selected' : ''}>Comprar Agora</option>
                            <option value="LEARN_MORE" ${ad.copy.call_to_action === 'LEARN_MORE' ? 'selected' : ''}>Saiba Mais</option>
                            <option value="SIGN_UP" ${ad.copy.call_to_action === 'SIGN_UP' ? 'selected' : ''}>Cadastre-se</option>
                            <option value="DOWNLOAD" ${ad.copy.call_to_action === 'DOWNLOAD' ? 'selected' : ''}>Baixar</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Criativo</label>
                        <div class="creative-selector">
                            <img src="${ad.creative.url || '/static/img/placeholder.jpg'}" 
                                 alt="Current Creative"
                                 style="max-width: 200px;">
                            ${this.editMode ? `
                                <button class="btn-secondary" onclick="adPreview.changeCreative(${this.selectedAdIndex})">
                                    🖼️ Trocar Imagem
                                </button>
                            ` : ''}
                        </div>
                    </div>

                    <div class="editor-actions">
                        ${!this.editMode ? `
                            <button class="btn-primary" onclick="adPreview.enableEditMode()">
                                ✏️ Habilitar Edição
                            </button>
                        ` : `
                            <button class="btn-success" onclick="adPreview.saveChanges()">
                                ✓ Salvar Alterações
                            </button>
                            <button class="btn-secondary" onclick="adPreview.cancelEdit()">
                                ✗ Cancelar
                            </button>
                        `}
                    </div>
                </div>

                <!-- Métricas estimadas -->
                <div class="ad-estimated-metrics">
                    <h4>Métricas Estimadas</h4>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <span class="metric-label">Alcance</span>
                            <span class="metric-value">${ad.estimated_reach.toLocaleString()}</span>
                        </div>
                        <div class="metric-card">
                            <span class="metric-label">CPA Estimado</span>
                            <span class="metric-value">R$ ${ad.estimated_cpa.toFixed(2)}</span>
                        </div>
                        <div class="metric-card">
                            <span class="metric-label">CTR Esperado</span>
                            <span class="metric-value">2.5%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Renderizar mockup visual do anúncio
     */
    renderAdMockup(ad) {
        // Mockup estilo Facebook/Instagram
        return `
            <div class="ad-mockup facebook-style">
                <div class="mockup-header">
                    <div class="mockup-profile">
                        <div class="profile-pic"></div>
                        <div class="profile-info">
                            <strong>Sua Empresa</strong>
                            <span>Patrocinado</span>
                        </div>
                    </div>
                </div>
                <div class="mockup-body">
                    <p>${ad.copy.primary_text}</p>
                </div>
                <div class="mockup-media">
                    <img src="${ad.creative.url || '/static/img/placeholder.jpg'}" alt="Ad Creative">
                </div>
                <div class="mockup-footer">
                    <strong>${ad.copy.headline}</strong>
                    <p>${ad.copy.description}</p>
                    <button class="mockup-cta">${this.formatCTA(ad.copy.call_to_action)}</button>
                </div>
            </div>
        `;
    }

    /**
     * Formatar CTA para exibição
     */
    formatCTA(cta) {
        const ctaMap = {
            'SHOP_NOW': 'Comprar Agora',
            'LEARN_MORE': 'Saiba Mais',
            'SIGN_UP': 'Cadastre-se',
            'DOWNLOAD': 'Baixar'
        };
        return ctaMap[cta] || cta;
    }

    /**
     * Selecionar um anúncio para visualização
     */
    selectAd(index) {
        this.selectedAdIndex = index;
        this.editMode = false;
        this.render();
    }

    /**
     * Habilitar modo de edição
     */
    enableEditMode() {
        this.editMode = true;
        this.render();
        showToast('Modo de edição ativado. Altere os campos desejados.', 'info');
    }

    /**
     * Salvar alterações do anúncio
     */
    saveChanges() {
        const ad = this.ads[this.selectedAdIndex];
        
        // Coletar valores dos campos
        ad.copy.headline = document.getElementById(`edit-headline-${this.selectedAdIndex}`).value;
        ad.copy.primary_text = document.getElementById(`edit-primary-text-${this.selectedAdIndex}`).value;
        ad.copy.description = document.getElementById(`edit-description-${this.selectedAdIndex}`).value;
        ad.copy.call_to_action = document.getElementById(`edit-cta-${this.selectedAdIndex}`).value;
        
        this.editMode = false;
        this.render();
        showToast('Alterações salvas com sucesso!', 'success');
    }

    /**
     * Cancelar edição
     */
    cancelEdit() {
        this.editMode = false;
        this.render();
        showToast('Edição cancelada', 'info');
    }

    /**
     * Editar anúncio específico
     */
    editAd(index) {
        this.selectAd(index);
        this.enableEditMode();
    }

    /**
     * Duplicar anúncio
     */
    duplicateAd(index) {
        const original = this.ads[index];
        const duplicate = JSON.parse(JSON.stringify(original));
        duplicate.id = `ad_${this.ads.length + 1}_duplicate`;
        duplicate.name = `${original.name} (Cópia)`;
        
        this.ads.push(duplicate);
        this.render();
        showToast('Anúncio duplicado com sucesso!', 'success');
    }

    /**
     * Trocar criativo do anúncio
     */
    changeCreative(index) {
        // Abrir seletor de arquivo
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*,video/*';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                // Simular upload e atualizar URL
                const reader = new FileReader();
                reader.onload = (event) => {
                    this.ads[index].creative.url = event.target.result;
                    this.render();
                    showToast('Criativo atualizado!', 'success');
                };
                reader.readAsDataURL(file);
            }
        };
        input.click();
    }

    /**
     * Voltar para etapa anterior
     */
    goBack() {
        if (confirm('Tem certeza que deseja voltar? As alterações não salvas serão perdidas.')) {
            // Voltar para wizard
            window.location.reload();
        }
    }

    /**
     * Aprovar e executar campanha
     */
    async approveAndExecute() {
        if (!confirm(`Confirma a execução de ${this.ads.length} anúncios?`)) {
            return;
        }

        showToast('Executando campanha...', 'info');

        try {
            const response = await fetch('/api/ad-creator/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ads: this.ads
                })
            });

            const result = await response.json();

            if (result.success) {
                showToast('Campanha executada com sucesso!', 'success');
                // Redirecionar para dashboard de monitoramento
                setTimeout(() => {
                    window.location.href = '/campaigns';
                }, 2000);
            } else {
                showToast(`Erro: ${result.error}`, 'error');
            }
        } catch (error) {
            console.error('Erro ao executar campanha:', error);
            showToast('Erro ao executar campanha', 'error');
        }
    }

    /**
     * Anexar event listeners
     */
    attachEventListeners() {
        // Event listeners já são anexados via onclick inline
        // Adicionar listeners adicionais se necessário
    }
}

// Instância global
const adPreview = new AdPreviewManager();

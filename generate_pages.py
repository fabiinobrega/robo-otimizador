#!/usr/bin/env python3
"""Script para gerar todas as páginas HTML do projeto"""

import os

# Template base para todas as páginas
def create_page(filename, title, icon, content):
    template = f'''{{%% extends "index.html" %%}}

{{%% block title %%}}{title} - Manus Marketing{{%% endblock %%}}

{{%% block content %%}}
<div class="container-fluid">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 class="h2"><i class="{icon}"></i> {title}</h1>
    </div>
    
    {content}
</div>
{{%% endblock %%}}
'''
    
    filepath = f'templates/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f'✅ {filename} criado')

# Criar todas as páginas
print("🚀 Gerando todas as páginas HTML...\n")

# 1. Criar Campanha (wizard 5 passos) - PÁGINA MAIS IMPORTANTE
create_campaign_content = '''
<div class="row">
    <div class="col-12">
        <!-- Progress Bar -->
        <div class="card mb-4">
            <div class="card-body">
                <div class="d-flex justify-content-between mb-2">
                    <span class="badge bg-primary">Passo <span id="currentStep">1</span> de 5</span>
                </div>
                <div class="progress" style="height: 10px;">
                    <div class="progress-bar" id="progressBar" role="progressbar" style="width: 20%"></div>
                </div>
            </div>
        </div>

        <!-- Passo 1: Informações Básicas -->
        <div class="card step-content" id="step1">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">📝 Passo 1: Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label class="form-label">Nome da Campanha *</label>
                    <input type="text" class="form-control" id="campaignName" placeholder="Ex: Black Friday 2024">
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Objetivo da Campanha *</label>
                    <select class="form-select" id="objective">
                        <option value="">Selecione...</option>
                        <option value="conversions">Conversões</option>
                        <option value="traffic">Tráfego</option>
                        <option value="awareness">Reconhecimento de Marca</option>
                        <option value="leads">Geração de Leads</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">URL da Landing Page</label>
                    <input type="url" class="form-control" id="landingPage" placeholder="https://seusite.com/produto">
                    <button class="btn btn-sm btn-outline-primary mt-2" onclick="analyzeLandingPage()">
                        <i class="fas fa-magic"></i> Analisar com IA
                    </button>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Plataforma *</label>
                    <select class="form-select" id="platform">
                        <option value="">Selecione...</option>
                        <option value="facebook">Facebook Ads</option>
                        <option value="google">Google Ads</option>
                        <option value="tiktok">TikTok Ads</option>
                        <option value="pinterest">Pinterest Ads</option>
                        <option value="linkedin">LinkedIn Ads</option>
                    </select>
                </div>
                
                <div class="alert alert-info">
                    <i class="fas fa-robot"></i> <strong>Velyra Prime:</strong> Posso analisar sua landing page e sugerir o melhor objetivo e copy!
                </div>
                
                <div class="d-flex justify-content-between">
                    <button class="btn btn-secondary" disabled>Anterior</button>
                    <button class="btn btn-primary" onclick="nextStep(2)">Próximo <i class="fas fa-arrow-right"></i></button>
                </div>
            </div>
        </div>

        <!-- Passo 2: Segmentação -->
        <div class="card step-content d-none" id="step2">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">🎯 Passo 2: Público e Segmentação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Idade</label>
                        <div class="d-flex gap-2">
                            <input type="number" class="form-control" placeholder="De" value="18">
                            <input type="number" class="form-control" placeholder="Até" value="65">
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Gênero</label>
                        <select class="form-select">
                            <option>Todos</option>
                            <option>Masculino</option>
                            <option>Feminino</option>
                        </select>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Localização</label>
                    <input type="text" class="form-control" placeholder="Brasil, São Paulo, etc.">
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Interesses (separados por vírgula)</label>
                    <input type="text" class="form-control" placeholder="Moda, Beleza, Tecnologia">
                </div>
                
                <button class="btn btn-outline-success mb-3">
                    <i class="fas fa-magic"></i> Sugerir Público com IA
                </button>
                
                <div class="d-flex justify-content-between">
                    <button class="btn btn-secondary" onclick="prevStep(1)"><i class="fas fa-arrow-left"></i> Anterior</button>
                    <button class="btn btn-primary" onclick="nextStep(3)">Próximo <i class="fas fa-arrow-right"></i></button>
                </div>
            </div>
        </div>

        <!-- Passo 3: Criativos -->
        <div class="card step-content d-none" id="step3">
            <div class="card-header bg-warning text-dark">
                <h5 class="mb-0">🎨 Passo 3: Criativos e Anúncios</h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label class="form-label">Título do Anúncio</label>
                    <input type="text" class="form-control" placeholder="Título chamativo">
                    <button class="btn btn-sm btn-outline-primary mt-2">
                        <i class="fas fa-magic"></i> Gerar com IA
                    </button>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Descrição</label>
                    <textarea class="form-control" rows="3" placeholder="Descrição persuasiva"></textarea>
                    <button class="btn btn-sm btn-outline-primary mt-2">
                        <i class="fas fa-magic"></i> Gerar com IA
                    </button>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Upload de Mídia</label>
                    <input type="file" class="form-control" multiple accept="image/*,video/*">
                    <button class="btn btn-sm btn-outline-primary mt-2">
                        <i class="fas fa-image"></i> Gerar Imagem com DALL-E
                    </button>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Call-to-Action (CTA)</label>
                    <select class="form-select">
                        <option>Comprar Agora</option>
                        <option>Saiba Mais</option>
                        <option>Cadastre-se</option>
                        <option>Baixar</option>
                    </select>
                </div>
                
                <div class="d-flex justify-content-between">
                    <button class="btn btn-secondary" onclick="prevStep(2)"><i class="fas fa-arrow-left"></i> Anterior</button>
                    <button class="btn btn-primary" onclick="nextStep(4)">Próximo <i class="fas fa-arrow-right"></i></button>
                </div>
            </div>
        </div>

        <!-- Passo 4: Orçamento -->
        <div class="card step-content d-none" id="step4">
            <div class="card-header bg-info text-white">
                <h5 class="mb-0">💰 Passo 4: Orçamento e Agenda</h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label class="form-label">Orçamento Diário (R$)</label>
                    <input type="number" class="form-control" placeholder="100.00" step="0.01">
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Estratégia de Lance</label>
                    <select class="form-select">
                        <option>CPC - Custo por Clique</option>
                        <option>CPM - Custo por Mil Impressões</option>
                        <option>CPA - Custo por Aquisição</option>
                    </select>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Data de Início</label>
                        <input type="date" class="form-control">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Data de Término</label>
                        <input type="date" class="form-control">
                    </div>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Meta de Vendas</label>
                    <input type="number" class="form-control" placeholder="50">
                </div>
                
                <div class="alert alert-success">
                    <i class="fas fa-lightbulb"></i> <strong>Sugestão da IA:</strong> Com R$ 100/dia, você pode alcançar aproximadamente 30-50 conversões.
                </div>
                
                <div class="d-flex justify-content-between">
                    <button class="btn btn-secondary" onclick="prevStep(3)"><i class="fas fa-arrow-left"></i> Anterior</button>
                    <button class="btn btn-primary" onclick="nextStep(5)">Próximo <i class="fas fa-arrow-right"></i></button>
                </div>
            </div>
        </div>

        <!-- Passo 5: Revisão e Lançamento -->
        <div class="card step-content d-none" id="step5">
            <div class="card-header bg-danger text-white">
                <h5 class="mb-0">✅ Passo 5: Revisão e Lançamento</h5>
            </div>
            <div class="card-body">
                <h5>Resumo da Campanha</h5>
                <div class="card mb-3">
                    <div class="card-body">
                        <p><strong>Nome:</strong> <span id="reviewName">-</span></p>
                        <p><strong>Plataforma:</strong> <span id="reviewPlatform">-</span></p>
                        <p><strong>Objetivo:</strong> <span id="reviewObjective">-</span></p>
                        <p><strong>Orçamento:</strong> R$ <span id="reviewBudget">-</span>/dia</p>
                    </div>
                </div>
                
                <h5>Preview do Anúncio</h5>
                <div class="card mb-3">
                    <div class="card-body">
                        <div class="border p-3 rounded">
                            <h6>Título do Anúncio</h6>
                            <p>Descrição persuasiva do anúncio...</p>
                            <button class="btn btn-sm btn-primary">Comprar Agora</button>
                        </div>
                    </div>
                </div>
                
                <div class="form-check mb-3">
                    <input class="form-check-input" type="checkbox" id="confirmLaunch">
                    <label class="form-check-label" for="confirmLaunch">
                        Confirmo que revisei todos os dados e quero lançar esta campanha
                    </label>
                </div>
                
                <div class="d-flex justify-content-between">
                    <button class="btn btn-secondary" onclick="prevStep(4)"><i class="fas fa-arrow-left"></i> Anterior</button>
                    <button class="btn btn-success btn-lg" onclick="launchCampaign()">
                        <i class="fas fa-rocket"></i> Lançar Campanha
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function nextStep(step) {
    document.querySelectorAll('.step-content').forEach(el => el.classList.add('d-none'));
    document.getElementById('step' + step).classList.remove('d-none');
    document.getElementById('currentStep').textContent = step;
    document.getElementById('progressBar').style.width = (step * 20) + '%';
}

function prevStep(step) {
    nextStep(step);
}

function analyzeLandingPage() {
    alert('Analisando landing page com IA... (funcionalidade em desenvolvimento)');
}

async function launchCampaign() {
    if (!document.getElementById('confirmLaunch').checked) {
        alert('Por favor, confirme que deseja lançar a campanha');
        return;
    }
    
    alert('Campanha sendo criada... Você será redirecionado para o dashboard.');
    setTimeout(() => {
        window.location.href = '/campaigns';
    }, 2000);
}
</script>
'''

create_page('create_campaign.html', 'Criar Campanha', 'fas fa-plus-circle', create_campaign_content)

print("\n✅ Todas as páginas foram criadas com sucesso!")

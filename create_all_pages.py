#!/usr/bin/env python3
"""Criar todas as páginas HTML com sintaxe Jinja2 correta"""

def write_template(filename, title, icon, content):
    """Escrever template com sintaxe correta"""
    template_content = f"""{{{{ extends "index.html" }}}}

{{{{ block title }}}}{title} - Manus Marketing{{{{ endblock }}}}

{{{{ block content }}}}
<div class="container-fluid">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 class="h2"><i class="{icon}"></i> {title}</h1>
    </div>
    
    {content}
</div>
{{{{ endblock }}}}
"""
    # Substituir {{ e }} por {% e %}
    template_content = template_content.replace('{{{{', '{%').replace('}}}}', '%}')
    
    with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
        f.write(template_content)
    print(f'✅ {filename}')

# Definir todas as páginas
pages = [
    ('create_campaign.html', 'Criar Campanha', 'fas fa-plus-circle', '''
<div class="card">
    <div class="card-body">
        <h5>Wizard de Criação de Campanha</h5>
        <p>Crie campanhas completas em 5 passos com auxílio da IA</p>
        <a href="/create-campaign" class="btn btn-primary">Iniciar Wizard</a>
    </div>
</div>
'''),
    
    ('campaigns.html', 'Minhas Campanhas', 'fas fa-list', '''
<div class="card">
    <div class="card-body p-0">
        <table class="table mb-0">
            <thead>
                <tr><th>Campanha</th><th>Status</th><th>Ações</th></tr>
            </thead>
            <tbody id="campaignsList">
                <tr><td colspan="3" class="text-center">Carregando...</td></tr>
            </tbody>
        </table>
    </div>
</div>
<script>
fetch('/api/campaigns').then(r=>r.json()).then(d=>{
    document.getElementById('campaignsList').innerHTML = d.campaigns ? 
        d.campaigns.map(c=>`<tr><td>${c.name}</td><td>${c.status}</td><td><a href="/campaigns/${c.id}">Ver</a></td></tr>`).join('') :
        '<tr><td colspan="3" class="text-center">Nenhuma campanha</td></tr>';
});
</script>
'''),
    
    ('competitor_spy.html', 'Espionagem', 'fas fa-user-secret', '''
<div class="card">
    <div class="card-body">
        <input type="url" class="form-control mb-3" placeholder="URL do concorrente">
        <button class="btn btn-primary">Espionar</button>
    </div>
</div>
'''),
    
    ('media_library.html', 'Biblioteca de Mídia', 'fas fa-photo-video', '''
<div class="card">
    <div class="card-body">
        <input type="file" class="form-control mb-3" multiple>
        <button class="btn btn-primary">Upload</button>
    </div>
</div>
'''),
    
    ('reports_dashboard.html', 'Relatórios', 'fas fa-file-alt', '''
<div class="card">
    <div class="card-body">
        <h5>Relatórios de Performance</h5>
        <button class="btn btn-success">Exportar PDF</button>
    </div>
</div>
'''),
    
    ('settings.html', 'Configurações', 'fas fa-cog', '''
<div class="card">
    <div class="card-body">
        <h5>Configurações do Sistema</h5>
        <button class="btn btn-primary">Salvar</button>
    </div>
</div>
'''),
    
    ('segmentation.html', 'Segmentação', 'fas fa-users', '''
<div class="card">
    <div class="card-body">
        <h5>Segmentação Avançada</h5>
        <button class="btn btn-primary">Criar Público</button>
    </div>
</div>
'''),
    
    ('funnel_builder.html', 'Funil', 'fas fa-filter', '''
<div class="card">
    <div class="card-body">
        <h5>Construtor de Funil</h5>
        <button class="btn btn-primary">Criar Funil</button>
    </div>
</div>
'''),
    
    ('dco_builder.html', 'DCO Builder', 'fas fa-layer-group', '''
<div class="card">
    <div class="card-body">
        <h5>Dynamic Creative Optimization</h5>
        <button class="btn btn-primary">Gerar Variações</button>
    </div>
</div>
'''),
    
    ('landing_page_builder.html', 'Landing Pages', 'fas fa-pager', '''
<div class="card">
    <div class="card-body">
        <h5>Landing Page Builder</h5>
        <button class="btn btn-primary">Criar Landing Page</button>
    </div>
</div>
'''),
    
    ('notifications.html', 'Notificações', 'fas fa-bell', '''
<div class="card">
    <div class="card-body">
        <h5>Central de Notificações</h5>
        <p>Nenhuma notificação nova</p>
    </div>
</div>
'''),
    
    ('subscriptions.html', 'Assinatura', 'fas fa-credit-card', '''
<div class="card">
    <div class="card-body">
        <h5>Plano Atual: Gratuito</h5>
        <button class="btn btn-primary">Upgrade</button>
    </div>
</div>
'''),
    
    ('affiliates.html', 'Afiliados', 'fas fa-handshake', '''
<div class="card">
    <div class="card-body">
        <h5>Programa de Afiliados</h5>
        <p>Ganhe comissões indicando</p>
    </div>
</div>
'''),
    
    ('developer_api.html', 'API', 'fas fa-code', '''
<div class="card">
    <div class="card-body">
        <h5>Documentação da API</h5>
        <code>GET /api/campaigns</code>
    </div>
</div>
'''),
]

print("🚀 Criando todas as páginas...\n")
for page in pages:
    write_template(*page)

print("\n✅ Todas as páginas criadas com sucesso!")

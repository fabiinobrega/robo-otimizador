# NEXORA - Guia de Instalação e Ativação

## 📦 Conteúdo do Pacote

Este pacote contém a transformação completa do NEXORA Operator v11.7 em um SaaS de nível mundial.

### Arquivos Incluídos

#### Documentação
- `NEXORA_BRAND_IDENTITY.md` - Identidade completa da marca
- `GUIA_MIGRACAO_NEXORA.md` - Guia de migração das páginas
- `ESTRUTURA_SAAS.md` - Estrutura SaaS preparada
- `RELATORIO_TRANSFORMACAO_NEXORA.md` - Relatório completo
- `README_NEXORA_INSTALLATION.md` - Este arquivo

#### Design System
- `static/css/nexora-premium-theme.css` - Design system completo

#### Templates
- `templates/base_nexora.html` - Template base
- `templates/dashboard_nexora.html` - Dashboard CEO View
- `templates/campaigns_nexora.html` - Lista de campanhas
- `templates/create_campaign_nexora.html` - Wizard de criação
- `templates/reports_nexora.html` - Relatórios de performance

#### Componentes
- `templates/components/nexora_components.html` - Componentes reutilizáveis

---

## 🚀 Instalação Rápida

### Opção 1: Via Git (Recomendado)

Se você já tem o repositório clonado:

```bash
# 1. Navegue até o diretório do projeto
cd /caminho/para/robo-otimizador

# 2. Faça pull das alterações
git pull origin main

# 3. Reinicie o servidor
# (Se estiver usando Render, o deploy será automático)
```

### Opção 2: Manual

Se você baixou o ZIP:

```bash
# 1. Extraia o arquivo nexora_transformation.zip

# 2. Copie os arquivos para o projeto
cp -r nexora_transformation/* /caminho/para/robo-otimizador/

# 3. Reinicie o servidor
```

---

## 🔧 Ativação das Novas Páginas

### Passo 1: Atualizar Rotas no main.py

Abra o arquivo `main.py` e atualize as rotas para usar os novos templates:

```python
# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_nexora.html')

# Campanhas
@app.route('/campaigns')
def campaigns():
    return render_template('campaigns_nexora.html')

# Criar Campanha
@app.route('/create-campaign')
def create_campaign():
    return render_template('create_campaign_nexora.html')

# Relatórios
@app.route('/reports')
def reports():
    return render_template('reports_nexora.html')
```

### Passo 2: Testar Localmente

```bash
# 1. Ative o ambiente virtual (se estiver usando)
source venv/bin/activate

# 2. Instale dependências (se necessário)
pip install -r requirements.txt

# 3. Execute o servidor
python main.py

# 4. Acesse http://localhost:5000
```

### Passo 3: Verificar Funcionalidades

Teste cada página:
- ✅ Dashboard carrega com métricas
- ✅ Campanhas lista e filtra corretamente
- ✅ Criar campanha navega pelo wizard
- ✅ Relatórios exibe gráficos
- ✅ Busca global funciona (Ctrl+K)
- ✅ Toasts aparecem nas ações

---

## 🎨 Personalização

### Alterar Cores

Edite `static/css/nexora-premium-theme.css`:

```css
:root {
    --accent-primary: #4f46e5; /* Cor principal */
    --accent-success: #22c55e; /* Verde de sucesso */
    /* ... outras cores */
}
```

### Alterar Logo

No arquivo `templates/base_nexora.html`, localize:

```html
<span class="nexora-logo-icon">
    <i class="fas fa-bolt"></i>
</span>
NEXORA
```

Substitua o ícone ou adicione uma imagem.

---

## 📱 Responsividade

O design é totalmente responsivo. Teste em:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

---

## 🔍 Troubleshooting

### Problema: Estilos não carregam

**Solução:**
```bash
# Limpe o cache do navegador
# Ou force reload: Ctrl+Shift+R (Windows/Linux) ou Cmd+Shift+R (Mac)
```

### Problema: Gráficos não aparecem

**Solução:**
Verifique se o Chart.js está carregando:
```html
<!-- Deve estar no <head> do base_nexora.html -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.umd.js"></script>
```

### Problema: API retorna erro

**Solução:**
Verifique se os endpoints da API estão funcionando:
```bash
curl http://localhost:5000/api/dashboard/metrics
curl http://localhost:5000/api/campaigns
```

---

## 🚢 Deploy

### Render (Automático)

Se você está usando Render com auto-deploy:
1. Faça push para o GitHub
2. Render detectará e fará deploy automaticamente
3. Aguarde 2-3 minutos
4. Acesse sua URL do Render

### Heroku

```bash
git push heroku main
```

### Servidor Próprio

```bash
# 1. Faça SSH no servidor
ssh user@seu-servidor.com

# 2. Navegue até o projeto
cd /caminho/para/robo-otimizador

# 3. Faça pull
git pull origin main

# 4. Reinicie o serviço
sudo systemctl restart nexora
```

---

## 📊 Migração das Páginas Restantes

Para migrar as outras páginas, siga o `GUIA_MIGRACAO_NEXORA.md`.

### Páginas Prioritárias (próxima fase)
1. Velyra Prime
2. Funil Builder
3. Landing Page Builder
4. DCO Builder
5. Segmentação

---

## 🔐 Ativação do SaaS (Futuro)

Quando estiver pronto para ativar o modelo SaaS, consulte `ESTRUTURA_SAAS.md`.

**Checklist:**
- [ ] Configurar Stripe
- [ ] Criar produtos e preços
- [ ] Descomentar rotas de billing
- [ ] Ativar middleware de limites
- [ ] Testar fluxo completo

---

## 📞 Suporte

### Documentação
- `NEXORA_BRAND_IDENTITY.md` - Identidade da marca
- `GUIA_MIGRACAO_NEXORA.md` - Guia de migração
- `ESTRUTURA_SAAS.md` - Estrutura SaaS
- `RELATORIO_TRANSFORMACAO_NEXORA.md` - Relatório completo

### Referências
- Páginas de exemplo em `templates/*_nexora.html`
- Componentes em `templates/components/nexora_components.html`
- Design system em `static/css/nexora-premium-theme.css`

---

## ✅ Checklist de Ativação

- [ ] Arquivos copiados para o projeto
- [ ] Rotas atualizadas no main.py
- [ ] Servidor reiniciado
- [ ] Dashboard testado
- [ ] Campanhas testadas
- [ ] Criar Campanha testado
- [ ] Relatórios testados
- [ ] Busca global testada (Ctrl+K)
- [ ] Responsividade verificada
- [ ] Deploy realizado

---

## 🎉 Resultado Esperado

Após a instalação, você terá:
- ✅ Design de classe mundial (Stripe/Linear/Notion)
- ✅ 4 páginas críticas redesenhadas
- ✅ Componentes reutilizáveis
- ✅ Busca global funcional
- ✅ Estrutura SaaS preparada
- ✅ Documentação completa

**O NEXORA agora parece, funciona e se sente como um produto SaaS premium.**

---

**Versão:** 1.0  
**Data:** 24 de Novembro de 2024  
**Criado por:** Manus AI

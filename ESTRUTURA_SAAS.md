# Estrutura SaaS para NEXORA (Preparação Futura)

## Visão Geral

Este documento descreve a estrutura preparatória para transformar o NEXORA em um SaaS multi-usuário com planos de assinatura. **IMPORTANTE:** Esta estrutura está preparada mas NÃO ATIVADA. Nenhuma cobrança será realizada.

## Arquitetura de Planos (Preparada, Não Ativa)

### Planos Propostos

#### 1. **Starter** - R$ 297/mês
- 5 campanhas ativas
- 1 usuário
- Suporte por email
- Integrações básicas (Facebook, Google)
- 10.000 impressões/mês
- Relatórios básicos

#### 2. **Growth** - R$ 797/mês
- 20 campanhas ativas
- 3 usuários
- Suporte prioritário
- Todas as integrações
- 100.000 impressões/mês
- Relatórios avançados
- A/B Testing
- Automação básica

#### 3. **Scale** - R$ 1.997/mês
- Campanhas ilimitadas
- 10 usuários
- Suporte dedicado
- Todas as funcionalidades
- Impressões ilimitadas
- Relatórios personalizados
- Automação avançada
- API access
- White label

#### 4. **Enterprise** - Sob consulta
- Tudo do Scale +
- Usuários ilimitados
- Gerente de conta dedicado
- SLA garantido
- Onboarding personalizado
- Treinamento da equipe
- Integrações customizadas

## Estrutura de Banco de Dados (Preparada)

### Tabela: `organizations`
```sql
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT DEFAULT 'starter',
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: `users`
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'member',
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);
```

### Tabela: `subscriptions`
```sql
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    plan TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    stripe_subscription_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);
```

### Tabela: `usage_metrics`
```sql
CREATE TABLE usage_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    metric_name TEXT NOT NULL,
    metric_value INTEGER DEFAULT 0,
    period TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);
```

## Limites por Plano (Configuração)

```python
PLAN_LIMITS = {
    'starter': {
        'campaigns': 5,
        'users': 1,
        'impressions': 10000,
        'features': ['basic_reports', 'facebook', 'google']
    },
    'growth': {
        'campaigns': 20,
        'users': 3,
        'impressions': 100000,
        'features': ['advanced_reports', 'ab_testing', 'automation_basic', 'all_integrations']
    },
    'scale': {
        'campaigns': -1,  # unlimited
        'users': 10,
        'impressions': -1,  # unlimited
        'features': ['all']
    },
    'enterprise': {
        'campaigns': -1,
        'users': -1,
        'impressions': -1,
        'features': ['all', 'white_label', 'api_access', 'custom_integrations']
    }
}
```

## Middleware de Verificação (Preparado, Não Ativo)

```python
def check_plan_limit(organization_id, resource_type):
    """
    Verifica se a organização atingiu o limite do plano.
    NOTA: Esta função está preparada mas não será ativada até o lançamento SaaS.
    """
    # TODO: Implementar quando ativar SaaS
    return True  # Sempre permite por enquanto

def check_feature_access(organization_id, feature_name):
    """
    Verifica se a organização tem acesso a uma funcionalidade.
    NOTA: Esta função está preparada mas não será ativada até o lançamento SaaS.
    """
    # TODO: Implementar quando ativar SaaS
    return True  # Sempre permite por enquanto
```

## Página de Planos (Preparada, Oculta)

### Rota (comentada no main.py)
```python
# @app.route('/pricing')
# def pricing():
#     return render_template('pricing_nexora.html')
```

## Integração com Stripe (Preparada, Não Configurada)

### Variáveis de Ambiente (não configuradas)
```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Endpoints (preparados, comentados)
```python
# @app.route('/api/create-checkout-session', methods=['POST'])
# def create_checkout_session():
#     # TODO: Implementar quando ativar SaaS
#     pass

# @app.route('/api/stripe-webhook', methods=['POST'])
# def stripe_webhook():
#     # TODO: Implementar quando ativar SaaS
#     pass
```

## Onboarding Multi-Usuário (Preparado)

### Fluxo de Cadastro
1. Usuário acessa `/signup`
2. Preenche dados da organização
3. Escolhe plano (mas não paga ainda)
4. Cria conta de admin
5. Acessa dashboard

### Página de Signup (preparada, não ativa)
```python
# @app.route('/signup')
# def signup():
#     return render_template('signup_nexora.html')
```

## Sistema de Permissões (Preparado)

### Roles
- **Owner**: Acesso total, gerencia assinatura
- **Admin**: Acesso total, exceto gerenciar assinatura
- **Member**: Acesso limitado às suas campanhas
- **Viewer**: Apenas visualização

### Decorador de Permissão (preparado)
```python
def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # TODO: Implementar verificação quando ativar SaaS
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

## Dashboard de Billing (Preparado, Oculto)

### Funcionalidades Planejadas
- Visualizar plano atual
- Histórico de faturas
- Atualizar método de pagamento
- Upgrade/downgrade de plano
- Cancelar assinatura

### Rota (comentada)
```python
# @app.route('/billing')
# def billing():
#     return render_template('billing_nexora.html')
```

## Métricas de Uso (Preparadas)

### Tracking Automático
```python
def track_usage(organization_id, metric_name, value=1):
    """
    Registra uso de recursos para billing futuro.
    NOTA: Dados coletados mas não usados para cobrança ainda.
    """
    # TODO: Implementar quando ativar SaaS
    pass
```

### Métricas Rastreadas
- Campanhas criadas
- Impressões servidas
- API calls
- Usuários ativos
- Relatórios gerados

## Notificações de Limite (Preparadas)

### Avisos Planejados
- 80% do limite de campanhas atingido
- 90% do limite de impressões atingido
- Limite de usuários atingido
- Sugestão de upgrade

## Migração de Dados (Planejada)

### Quando Ativar SaaS
1. Criar organização padrão para usuários existentes
2. Associar campanhas existentes à organização
3. Definir plano inicial (ex: Growth por 3 meses grátis)
4. Notificar usuários sobre mudanças

## Checklist de Ativação SaaS

Quando decidir ativar o modelo SaaS, siga este checklist:

- [ ] Configurar Stripe (chaves de produção)
- [ ] Criar produtos e preços no Stripe
- [ ] Descomentar rotas de billing
- [ ] Ativar middleware de verificação de limites
- [ ] Criar páginas de pricing e signup
- [ ] Implementar fluxo de checkout
- [ ] Configurar webhooks do Stripe
- [ ] Testar fluxo completo de assinatura
- [ ] Preparar comunicação para usuários existentes
- [ ] Definir período de transição/trial
- [ ] Configurar sistema de suporte para billing
- [ ] Preparar FAQs sobre planos
- [ ] Configurar analytics de conversão

## Observações Importantes

1. **Nenhuma Cobrança Ativa**: Todo o código de cobrança está comentado ou retorna `True` (permitindo acesso total).

2. **Estrutura Preparada**: Banco de dados e código estão prontos para ativação rápida quando necessário.

3. **Sem Impacto Atual**: Usuários atuais não verão nenhuma menção a planos ou limites.

4. **Transição Suave**: Quando ativar, será possível migrar usuários existentes gradualmente.

5. **Flexibilidade**: Estrutura permite ajustar planos e preços antes do lançamento.

## Próximos Passos (Quando Ativar)

1. Definir preços finais e features de cada plano
2. Criar conta Stripe e configurar produtos
3. Implementar páginas de pricing e signup
4. Testar fluxo completo em ambiente de staging
5. Preparar comunicação de lançamento
6. Oferecer período de trial para usuários existentes
7. Lançar gradualmente (beta fechado → beta aberto → público)

---

**Status:** PREPARADO, NÃO ATIVO
**Última atualização:** 24 de Novembro de 2024

# Requisitos de Negócio - Duração da Campanha

## Objetivo

Adicionar ao fluxo "CRIAR ANÚNCIO PERFEITO" a definição obrigatória de **DURAÇÃO DA CAMPANHA** (em dias), integrando orçamento total, cálculo de orçamento diário e execução real em Facebook Ads e Google Ads.

## Requisitos Funcionais

### RF01: Campos Obrigatórios

A criação de anúncios DEVE exigir:
- **Orçamento Total** (já existente) - Valor total a ser investido na campanha
- **Duração da Campanha** (NOVO, obrigatório) - Período em dias que a campanha deve rodar

### RF02: Lógica de Cálculo

O sistema deve calcular automaticamente:

```
orçamento_diario = orçamento_total / duracao_dias
```

**Exemplo 1:**
- Orçamento Total: R$ 1.000,00
- Duração: 10 dias
- **Orçamento Diário: R$ 100,00/dia**

**Exemplo 2:**
- Orçamento Total: R$ 500,00
- Duração: 7 dias
- **Orçamento Diário: R$ 71,43/dia**

### RF03: Validações Mínimas

O sistema DEVE validar:
- `duracao_dias >= 1` (mínimo 1 dia)
- `duracao_dias` não pode ser nulo ou vazio
- `duracao_dias` deve ser um número inteiro positivo

### RF04: Cálculo de Datas

O sistema deve calcular automaticamente:
- **Data de Início:** Data atual (hoje)
- **Data de Término:** Data atual + duração em dias

**Exemplo:**
- Hoje: 2025-01-15
- Duração: 10 dias
- **Data de Início:** 2025-01-15
- **Data de Término:** 2025-01-25

## Regras de Negócio

### RN01: Orçamento Mínimo por Dia

- Facebook Ads exige mínimo de **R$ 20,00/dia**
- Google Ads exige mínimo de **R$ 10,00/dia**

O sistema deve validar:
```
orçamento_diario >= 20.00  # Para Facebook
orçamento_diario >= 10.00  # Para Google
```

### RN02: Duração Máxima Recomendada

- Duração máxima recomendada: **90 dias**
- Campanhas acima de 90 dias devem exibir aviso (não bloquear)

### RN03: Ajuste Automático de Estratégia

O GPT deve ajustar a estratégia conforme a duração:

**Campanhas Curtas (1-7 dias):**
- Foco em conversões rápidas
- Criativos diretos e urgentes
- Testes A/B limitados

**Campanhas Médias (8-30 dias):**
- Estratégia balanceada
- Testes A/B completos
- Otimização contínua

**Campanhas Longas (31+ dias):**
- Estratégia de longo prazo
- Múltiplos testes A/B
- Otimização agressiva

## Fluxo de Dados

```
[Usuário]
    ↓
    Preenche: orçamento_total, duracao_dias
    ↓
[Frontend]
    ↓
    Calcula: orçamento_diario = orçamento_total / duracao_dias
    Exibe em tempo real
    ↓
[Validação Frontend]
    ↓
    Valida: duracao_dias >= 1, orçamento_diario >= 20
    ↓
[Backend - PreExecutionValidator]
    ↓
    Valida: presença e valores mínimos
    ↓
[GPT - OpenAIStrategicBrain]
    ↓
    Recebe: orçamento_total, duracao_dias, orçamento_diario
    Ajusta estratégia conforme duração
    ↓
[Manus - ManusTechnicalExecutor]
    ↓
    Recebe: orçamento_diario, data_inicio, data_termino
    Cria campanha no Facebook/Google Ads
    ↓
[Facebook/Google Ads]
    ↓
    Campanha criada com:
    - daily_budget (em centavos)
    - start_time (ISO 8601)
    - end_time (ISO 8601)
```

## Mensagens de Erro

### Erro 1: Duração não definida
```
❌ Defina por quantos dias a campanha deve rodar para calcular o orçamento diário.
```

### Erro 2: Duração inválida
```
❌ A duração da campanha deve ser de pelo menos 1 dia.
```

### Erro 3: Orçamento diário muito baixo
```
❌ Com este orçamento e duração, o orçamento diário seria R$ X,XX, mas o mínimo para Facebook Ads é R$ 20,00/dia. Aumente o orçamento total ou reduza a duração.
```

## Impacto nas Integrações

### Facebook Ads API

Campos a serem configurados:
```python
{
    "daily_budget": int(orçamento_diario * 100),  # Em centavos
    "start_time": datetime.now().isoformat(),
    "end_time": (datetime.now() + timedelta(days=duracao_dias)).isoformat()
}
```

### Google Ads API

Campos a serem configurados:
```python
{
    "budget": {
        "amount_micros": int(orçamento_diario * 1000000),  # Em micros
        "delivery_method": "STANDARD"
    },
    "start_date": datetime.now().strftime("%Y%m%d"),
    "end_date": (datetime.now() + timedelta(days=duracao_dias)).strftime("%Y%m%d")
}
```

## Prioridade

**ALTA** - Implementação obrigatória para lançamento do fluxo completo.

## Dependências

- `PreExecutionValidator` (existente - requer atualização)
- `OpenAIStrategicBrain` (existente - requer atualização)
- `ManusTechnicalExecutor` (existente - requer atualização)
- `create_campaign.html` (existente - requer atualização)

## Critérios de Aceitação

- [ ] Campo "Duração da campanha (em dias)" é obrigatório
- [ ] Orçamento diário é calculado automaticamente em tempo real
- [ ] Sistema bloqueia criação sem duração definida
- [ ] Facebook Ads aceita a campanha com start_time e end_time
- [ ] Google Ads aceita a campanha com start_date e end_date
- [ ] Testes unitários com 100% de aprovação
- [ ] UX clara com tooltips e feedback visual

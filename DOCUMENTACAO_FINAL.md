# DOCUMENTAÇÃO FINAL - NEXORA PRIME v11.9 (Build Integração IA)

## 1. Visão Geral

Esta documentação descreve a arquitetura e o uso da integração de Inteligência Artificial (IA) no sistema NEXORA PRIME, envolvendo OpenAI (ChatGPT) e Manus.

## 2. Arquitetura da IA

A arquitetura é baseada em uma divisão de responsabilidades:

- **ChatGPT (Cérebro Estratégico):** Responsável por tarefas que exigem raciocínio, criatividade e conhecimento de marketing, como criação de estratégias, copywriting e análise de dados.
- **Manus (Braço de Execução):** Responsável por tarefas técnicas e operacionais, como aplicar configurações, interagir com APIs externas, manipular o banco de dados e modificar a estrutura do sistema.
- **Orchestrator (Coordenador):** Um módulo central que traduz as decisões estratégicas do ChatGPT em comandos executáveis para o Manus, garantindo um fluxo de trabalho coeso.

## 3. Guia de Uso

### 3.1. Dashboard de IA (`/ai-dashboard`)

O Dashboard de IA é o ponto central para interagir com as funcionalidades de inteligência artificial. Ele fornece:

- **Status em Tempo Real:** Verifica se todos os componentes da IA (ChatGPT, Manus, Orchestrator) estão operacionais.
- **Ações Rápidas:** Atalhos para as principais funcionalidades, como criar campanhas, gerar copy e analisar performance.
- **Criação de Campanhas com IA:** Um modal que guia o usuário na criação de uma campanha completa, desde a definição do objetivo até a implementação.

### 3.2. Fluxo de Criação de Campanha

1. Acesse o Dashboard de IA.
2. Clique em "Criar Campanha com IA".
3. Preencha o formulário com os detalhes da campanha (nome, produto, objetivo, orçamento, etc.).
4. Clique em "Criar com IA".
5. O Orchestrator iniciará o fluxo:
   - O ChatGPT criará a estratégia e o copy.
   - O Manus aplicará a campanha no sistema Nexora.
   - O Manus sincronizará a campanha com as plataformas de anúncios (Google Ads, Facebook Ads).
6. O resultado e o log de execução serão exibidos na tela.

### 3.3. Endpoints da API

A integração expõe uma série de endpoints para uso programático. Consulte o `RELATORIO_INTEGRACAO_GPT_MANUS_NEXORA.md` para a lista completa de novas rotas.

## 4. Configuração

### 4.1. Chave da API da OpenAI

A chave da API da OpenAI deve ser configurada no arquivo `.env` na raiz do projeto:

```
OPENAI_API_KEY=sk-...
```

### 4.2. Credenciais do Facebook Ads

As credenciais do Facebook Ads também devem ser configuradas no arquivo `.env`:

```
FACEBOOK_APP_ID=SEU_APP_ID
FACEBOOK_APP_SECRET=SEU_APP_SECRET
FACEBOOK_ACCESS_TOKEN=SEU_ACCESS_TOKEN
```

## 5. Testes

Os testes foram criados na pasta `/tests` e podem ser executados individualmente:

```bash
python3.11 tests/test_openai_endpoints.py
python3.11 tests/test_manus_endpoints.py
python3.11 tests/test_orchestration.py
```

**Nota:** Os testes do Manus apresentaram falhas relacionadas ao acesso ao banco de dados, que devem ser investigadas em um ambiente com as permissões corretas.

## 6. Conclusão

Esta integração transforma o NEXORA PRIME em uma plataforma de marketing autônoma e inteligente, capaz de otimizar processos e potencializar resultados de resultados.

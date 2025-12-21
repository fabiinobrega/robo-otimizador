'''
# 📖 GUIA DE CONFIGURAÇÃO DAS CHAVES STRIPE
## NEXORA PRIME - Integração de Pagamentos

**Data:** 19 de Dezembro de 2025
**Autor:** Manus AI

---

## 1. Introdução

Este guia fornece as instruções passo a passo para obter e configurar suas chaves de API da Stripe, necessárias para ativar o sistema de pagamentos no **NEXORA PRIME**. 

É crucial seguir estes passos para garantir que os pagamentos sejam processados de forma segura em seus ambientes de **teste** e **produção**.

**Atenção:** As chaves fornecidas anteriormente (`mk_*`) não são chaves padrão da Stripe e não funcionarão. Por favor, siga os passos abaixo para gerar as chaves corretas.

## 2. Obtendo as Chaves de API no Dashboard da Stripe

Você precisará de duas chaves: a **Chave Secreta** (`sk_...`) e o **Segredo do Webhook** (`whsec_...`).

### Passo 1: Acesse o Dashboard da Stripe

1.  Faça login na sua conta Stripe: [https://dashboard.stripe.com/](https://dashboard.stripe.com/)

### Passo 2: Obtenha a Chave Secreta (Secret Key)

1.  No menu à esquerda, navegue até **Desenvolvedores > Chaves de API**.
2.  Nesta página, você verá a **Chave publicável** (`pk_...`) e a **Chave secreta** (`sk_...`).
3.  **Importante:** Certifique-se de que o seletor "Visualizar dados de teste" está **ativado** para obter as chaves de teste (`sk_test_...`).
4.  Clique em **Revelar chave de teste** para ver e copiar sua **Chave Secreta de Teste**. Ela começará com `sk_test_`.

    > **Segurança:** Nunca compartilhe sua chave secreta publicamente. Trate-a como uma senha.

### Passo 3: Obtenha o Segredo do Webhook (Webhook Secret)

1.  No menu à esquerda, navegue até **Desenvolvedores > Webhooks**.
2.  Clique em **Adicionar um endpoint**.
3.  No campo **URL do endpoint**, você precisará inserir a URL pública onde sua aplicação NEXORA PRIME está rodando, seguida de `/api/payments/webhook`. 
    *   *Exemplo para desenvolvimento local (usando uma ferramenta como ngrok):* `https://sua-url-publica.ngrok.io/api/payments/webhook`
    *   *Exemplo para produção:* `https://sua-app.com/api/payments/webhook`
4.  Clique em **+ Selecionar eventos** e adicione os seguintes eventos:
    *   `payment_intent.succeeded`
    *   `payment_intent.payment_failed`
    *   `charge.refunded`
5.  Clique em **Adicionar eventos** e, em seguida, em **Adicionar endpoint**.
6.  Após a criação do endpoint, você será redirecionado para a página de detalhes. Na seção **Segredo de assinatura**, clique em **Revelar**.
7.  Copie o valor. Ele começará com `whsec_`.

## 3. Configurando as Chaves no NEXORA PRIME

Agora que você tem as duas chaves, precisa configurá-las no arquivo `.env` do seu projeto.

1.  Abra o arquivo `.env` na raiz do seu projeto `robo-otimizador`.
2.  Localize as seguintes linhas:

    ```
    STRIPE_SECRET_KEY=mk_1Sft3lCDfzMBjtj2lam9D52q
    STRIPE_WEBHOOK_SECRET=mk_1SfYlkCDfzMBjtj2r6kGTO94
    ```

3.  Substitua os valores `mk_*` pelas chaves que você acabou de copiar do Dashboard da Stripe.

    *   **STRIPE_SECRET_KEY:** Cole a sua **Chave Secreta** (`sk_test_...`).
    *   **STRIPE_WEBHOOK_SECRET:** Cole o seu **Segredo do Webhook** (`whsec_...`).

4.  O resultado deve ser semelhante a este:

    ```
    STRIPE_SECRET_KEY=sk_test_SUA_CHAVE_AQUI
    STRIPE_WEBHOOK_SECRET=whsec_yyyyyyyyyyyyyyyyyyyyyyyy
    ```

5.  Salve o arquivo `.env` e reinicie sua aplicação NEXORA PRIME para que as novas configurações sejam carregadas.

## 4. Modo de Produção (Live)

Quando estiver pronto para aceitar pagamentos reais, o processo é o mesmo, mas com uma diferença crucial:

1.  No Dashboard da Stripe, **desative** o seletor "Visualizar dados de teste".
2.  Repita os **Passos 2 e 3** para obter sua **Chave Secreta de Produção** (`sk_live_...`) e seu **Segredo do Webhook de Produção**.
3.  Atualize o arquivo `.env` com as chaves de produção antes de implantar sua aplicação no ambiente de produção.

---

**Suporte:** Se encontrar qualquer dificuldade, consulte a documentação oficial da Stripe ou entre em contato com o suporte da plataforma.
'''

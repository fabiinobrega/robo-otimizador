"""
🔥 TRANSFERÊNCIA TOTAL DE CONHECIMENTO - FASES 7 E 8
MÉTRICAS E DECISÃO + EXECUÇÃO REAL DE CAMPANHAS

Este módulo contém TODO o conhecimento que Manus transfere para Velyra
sobre análise de métricas e execução de campanhas reais.

REGRAS:
- NÃO resumir
- NÃO simplificar
- EXPLICAR O PORQUÊ de cada decisão
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FASE 7: MÉTRICAS E DECISÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FASE_7_METRICAS = {
    "titulo": "Métricas e Tomada de Decisão",
    "objetivo": "Velyra deve tomar decisões baseadas em DADOS, não intuição",
    
    "conteudo": {
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1. MÉTRICAS CERTAS POR FASE
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "metricas_por_fase": {
            "conceito": """
            Cada fase da campanha exige foco em métricas DIFERENTES.
            
            Olhar para a métrica errada = decisão errada.
            """,
            
            "fase_teste": {
                "objetivo": "Validar se a campanha tem potencial",
                "duracao": "3-7 dias",
                "orcamento": "R$50-200/dia",
                "metricas_primarias": {
                    "ctr": {
                        "o_que_e": "Taxa de cliques",
                        "benchmark": ">1% aceitável, >2% bom",
                        "por_que": "Indica se criativo chama atenção"
                    },
                    "cpc": {
                        "o_que_e": "Custo por clique",
                        "benchmark": "Depende do nicho (R$0.50-R$5)",
                        "por_que": "Indica eficiência do tráfego"
                    },
                    "hook_rate": {
                        "o_que_e": "% que assiste 3s do vídeo",
                        "benchmark": ">30% bom",
                        "por_que": "Indica se o gancho funciona"
                    }
                },
                "decisao": {
                    "escalar": "CTR >1.5%, CPC dentro do esperado, sinais de conversão",
                    "otimizar": "CTR ok mas CPA alto, ou CTR baixo mas conversões ok",
                    "matar": "CTR <0.5%, zero conversões após 500 cliques"
                }
            },
            
            "fase_otimizacao": {
                "objetivo": "Melhorar performance e encontrar vencedores",
                "duracao": "7-14 dias",
                "orcamento": "R$100-500/dia",
                "metricas_primarias": {
                    "cpa": {
                        "o_que_e": "Custo por aquisição/conversão",
                        "benchmark": "Deve ser < LTV do cliente",
                        "por_que": "Indica se campanha é lucrativa"
                    },
                    "roas": {
                        "o_que_e": "Retorno sobre investimento em ads",
                        "benchmark": ">2x bom, >3x excelente",
                        "por_que": "Indica lucro direto"
                    },
                    "taxa_conversao": {
                        "o_que_e": "% de cliques que convertem",
                        "benchmark": ">2% bom para e-commerce",
                        "por_que": "Indica qualidade do tráfego + landing"
                    }
                },
                "decisao": {
                    "escalar": "CPA estável, ROAS >2x, volume crescente",
                    "otimizar": "CPA flutuando, ROAS entre 1.5-2x",
                    "matar": "CPA subindo, ROAS <1.5x por 5+ dias"
                }
            },
            
            "fase_escala": {
                "objetivo": "Maximizar volume mantendo lucratividade",
                "duracao": "Contínuo",
                "orcamento": "R$500+/dia",
                "metricas_primarias": {
                    "volume_conversoes": {
                        "o_que_e": "Número absoluto de conversões",
                        "benchmark": "Crescendo ou estável",
                        "por_que": "Indica capacidade de escala"
                    },
                    "roas_marginal": {
                        "o_que_e": "ROAS do investimento adicional",
                        "benchmark": "Deve manter >1.5x",
                        "por_que": "Indica se escala é sustentável"
                    },
                    "frequencia": {
                        "o_que_e": "Quantas vezes cada pessoa viu o anúncio",
                        "benchmark": "<3 ideal, >5 saturado",
                        "por_que": "Indica saturação de público"
                    }
                },
                "decisao": {
                    "continuar": "ROAS estável, frequência <3, volume crescendo",
                    "pausar_escala": "ROAS caindo, frequência >3",
                    "renovar": "Frequência >5, CTR caindo"
                }
            }
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2. LEITURA DE DADOS INICIAIS
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "leitura_dados_iniciais": {
            "conceito": """
            Os primeiros dados são os mais difíceis de interpretar.
            Pouco volume = alta variância = decisões arriscadas.
            
            Regra: Espere significância antes de decidir.
            """,
            
            "minimos_para_decisao": {
                "impressoes": {
                    "minimo": 1000,
                    "por_que": "Menos que isso, CTR não é confiável"
                },
                "cliques": {
                    "minimo": 100,
                    "por_que": "Menos que isso, taxa de conversão não é confiável"
                },
                "conversoes": {
                    "minimo": 20,
                    "por_que": "Menos que isso, CPA não é confiável"
                },
                "dias": {
                    "minimo": 3,
                    "por_que": "Variação diária é normal, precisa de tendência"
                }
            },
            
            "como_interpretar": {
                "dia_1": {
                    "o_que_olhar": "Impressões, CTR inicial",
                    "o_que_nao_fazer": "Tomar decisões definitivas",
                    "acao": "Observar e anotar"
                },
                "dia_2_3": {
                    "o_que_olhar": "Tendência de CTR, primeiros cliques",
                    "o_que_nao_fazer": "Matar campanha sem dados suficientes",
                    "acao": "Ajustes menores se necessário"
                },
                "dia_4_7": {
                    "o_que_olhar": "CPA, taxa de conversão, ROAS",
                    "o_que_nao_fazer": "Escalar sem validar",
                    "acao": "Decisão de continuar/pausar/otimizar"
                }
            },
            
            "armadilhas": [
                {
                    "armadilha": "Matar campanha no dia 1",
                    "por_que_errado": "Dados insuficientes para conclusão",
                    "o_que_fazer": "Esperar mínimo 3 dias ou 100 cliques"
                },
                {
                    "armadilha": "Escalar no dia 2 porque 'está bom'",
                    "por_que_errado": "Pode ser variância, não tendência",
                    "o_que_fazer": "Esperar confirmação por 3+ dias"
                },
                {
                    "armadilha": "Ignorar sinais de alerta",
                    "por_que_errado": "Problemas pequenos viram grandes",
                    "o_que_fazer": "Anotar e monitorar de perto"
                }
            ]
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 3. QUANDO ESCALAR
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "quando_escalar": {
            "pre_requisitos": [
                "ROAS consistente >2x por 5+ dias",
                "CPA estável (variação <20%)",
                "Volume de conversões crescendo ou estável",
                "Frequência <3",
                "Criativos não saturados (CTR estável)"
            ],
            
            "tipos_escala": {
                "vertical": {
                    "o_que_e": "Aumentar orçamento da mesma campanha",
                    "como_fazer": "Aumentar 20-30% a cada 3 dias",
                    "risco": "CPA pode subir se aumentar muito rápido",
                    "quando_usar": "Campanha validada, público grande"
                },
                "horizontal": {
                    "o_que_e": "Criar novas campanhas/conjuntos",
                    "como_fazer": "Duplicar vencedor para novos públicos",
                    "risco": "Pode canibalizar campanha original",
                    "quando_usar": "Quando vertical atinge limite"
                }
            },
            
            "sinais_para_escalar": {
                "verde": [
                    "ROAS >2.5x consistente",
                    "CPA abaixo do target",
                    "Frequência <2",
                    "CTR estável ou subindo"
                ],
                "amarelo": [
                    "ROAS entre 2-2.5x",
                    "CPA no target",
                    "Frequência entre 2-3",
                    "CTR estável"
                ],
                "vermelho": [
                    "ROAS <2x",
                    "CPA acima do target",
                    "Frequência >3",
                    "CTR caindo"
                ]
            },
            
            "principio_manus": """
            Escale DEVAGAR.
            
            Aumentar 20-30% a cada 3 dias é seguro.
            Dobrar orçamento de uma vez é arriscado.
            
            Paciência na escala = lucro sustentável.
            """
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 4. QUANDO CORTAR
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "quando_cortar": {
            "sinais_para_pausar": {
                "imediato": [
                    "Zero conversões após 500+ cliques",
                    "CPA 3x acima do target por 3+ dias",
                    "CTR <0.3% (criativo não funciona)",
                    "Erro na campanha (link quebrado, etc)"
                ],
                "apos_analise": [
                    "ROAS <1.5x por 5+ dias",
                    "CPA subindo consistentemente",
                    "Frequência >5 (público esgotado)",
                    "Custo por resultado inviável"
                ]
            },
            
            "como_cortar": {
                "pausar_vs_deletar": {
                    "pausar": "Quando pode voltar depois (sazonal, teste)",
                    "deletar": "Quando definitivamente não funciona"
                },
                "o_que_salvar": [
                    "Dados de público (para exclusão futura)",
                    "Aprendizados (o que não funcionou)",
                    "Criativos (podem funcionar em outro contexto)"
                ]
            },
            
            "erro_comum": """
            O erro mais comum é NÃO cortar.
            
            Empreendedores se apegam a campanhas que não funcionam.
            "Talvez amanhã melhore..."
            
            Não melhora. Corte e teste outra coisa.
            
            Dinheiro gasto em campanha ruim = dinheiro que poderia
            estar em campanha boa.
            """
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 5. QUANDO INSISTIR
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "quando_insistir": {
            "sinais_de_potencial": [
                "CTR bom mas CPA alto (problema pode ser landing)",
                "Conversões esporádicas (pode precisar de mais volume)",
                "Público engajado (comentários, compartilhamentos)",
                "Métricas melhorando dia a dia"
            ],
            
            "o_que_testar_antes_de_desistir": {
                "se_ctr_baixo": [
                    "Novos criativos (ângulos diferentes)",
                    "Novos públicos",
                    "Novos formatos (imagem → vídeo)"
                ],
                "se_ctr_bom_conversao_baixa": [
                    "Landing page (velocidade, copy, oferta)",
                    "Alinhamento criativo-landing",
                    "Público mais qualificado"
                ],
                "se_cpa_alto": [
                    "Reduzir público (mais específico)",
                    "Testar ofertas diferentes",
                    "Otimizar para evento mais próximo da compra"
                ]
            },
            
            "limite_de_insistencia": """
            Insista enquanto houver HIPÓTESE clara do que testar.
            
            Se você já testou:
            - 5+ criativos diferentes
            - 3+ públicos diferentes
            - 2+ ofertas diferentes
            - Landing page otimizada
            
            E ainda não funciona... é hora de pivotar.
            
            Não é fracasso, é aprendizado.
            """
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 6. COMO PROTEGER MARGEM
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "proteger_margem": {
            "conceito": """
            Faturamento alto ≠ Lucro alto.
            
            Você pode faturar R$100k e ter prejuízo.
            Você pode faturar R$30k e ter lucro.
            
            O que importa é a MARGEM.
            """,
            
            "calculo_margem": {
                "formula": "(Receita - Custos) / Receita × 100",
                "custos_incluir": [
                    "Custo do produto/serviço",
                    "Custo de ads",
                    "Custo de ferramentas",
                    "Custo de equipe",
                    "Impostos",
                    "Taxas de pagamento"
                ],
                "exemplo": """
                Receita: R$ 100.000
                Custo produto: R$ 30.000
                Custo ads: R$ 25.000
                Outros custos: R$ 15.000
                Total custos: R$ 70.000
                Lucro: R$ 30.000
                Margem: 30%
                """
            },
            
            "como_proteger": {
                "definir_cpa_maximo": {
                    "como": "CPA máximo = Margem do produto × % aceitável para aquisição",
                    "exemplo": "Produto de R$200 com margem 50% = R$100 de margem. CPA máximo = R$50 (50% da margem)"
                },
                "definir_roas_minimo": {
                    "como": "ROAS mínimo = 1 / Margem do produto",
                    "exemplo": "Margem 50% = ROAS mínimo 2x. Margem 33% = ROAS mínimo 3x"
                },
                "monitorar_diariamente": {
                    "metricas": ["CPA", "ROAS", "Custo total", "Receita total"],
                    "acao": "Pausar campanhas que ultrapassam limites"
                }
            },
            
            "principio_manus": """
            Defina seus limites ANTES de começar.
            
            CPA máximo: R$ ___
            ROAS mínimo: ___x
            Orçamento máximo diário: R$ ___
            
            Se ultrapassar, PAUSE. Sem exceções.
            Emoção não paga as contas.
            """
        }
    },
    
    "validacao": {
        "perguntas_velyra_deve_responder": [
            "Quais métricas olhar em cada fase da campanha?",
            "Quanto tempo esperar antes de tomar decisões?",
            "Quais são os pré-requisitos para escalar?",
            "Quando pausar uma campanha imediatamente?",
            "Como calcular CPA máximo e ROAS mínimo?",
            "O que testar antes de desistir de uma campanha?"
        ],
        
        "criterio_aprovacao": """
        Velyra deve demonstrar:
        1. Conhecimento das métricas certas por fase
        2. Paciência para esperar dados suficientes
        3. Critérios claros para escalar
        4. Disciplina para cortar quando necessário
        5. Capacidade de proteger margem
        6. Tomada de decisão baseada em dados
        """
    }
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FASE 8: EXECUÇÃO REAL DE CAMPANHAS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FASE_8_EXECUCAO = {
    "titulo": "Execução Real de Campanhas",
    "objetivo": "Velyra deve executar campanhas reais com metodologia profissional",
    
    "conteudo": {
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1. PRÉ-REQUISITOS ANTES DE CRIAR
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "pre_requisitos": {
            "aviso": """
            ⚠️ ANTES de criar QUALQUER anúncio, você DEVE:
            
            1. Espionar concorrentes
            2. Analisar mercado
            3. Mapear criativos vencedores
            4. Identificar brechas
            5. Definir estratégia completa
            
            Criar anúncio sem isso = jogar dinheiro fora.
            """,
            
            "checklist_pre_campanha": {
                "pesquisa_mercado": [
                    "Tamanho do mercado definido",
                    "Público-alvo mapeado (avatar)",
                    "Dores e desejos identificados",
                    "Objeções listadas"
                ],
                "analise_concorrencia": [
                    "Top 5 concorrentes identificados",
                    "Criativos deles analisados",
                    "Ofertas deles mapeadas",
                    "Pontos fracos identificados"
                ],
                "oferta_definida": [
                    "Promessa clara",
                    "Mecanismo único",
                    "Provas reunidas",
                    "Garantia definida",
                    "Preço e condições"
                ],
                "assets_prontos": [
                    "Landing page funcionando",
                    "Criativos produzidos",
                    "Copy escrita",
                    "Tracking configurado"
                ]
            }
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2. ESPIONAGEM DE CONCORRENTES
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "espionagem_concorrentes": {
            "por_que": """
            Seus concorrentes já gastaram dinheiro testando.
            Eles já descobriram o que funciona e o que não funciona.
            
            Espionar = aprender com o dinheiro dos outros.
            """,
            
            "ferramentas": {
                "meta_ad_library": {
                    "url": "https://www.facebook.com/ads/library",
                    "o_que_ver": [
                        "Anúncios ativos dos concorrentes",
                        "Há quanto tempo estão rodando",
                        "Formatos que usam",
                        "Copy e criativos"
                    ],
                    "dica": "Anúncio rodando há muito tempo = provavelmente funciona"
                },
                "similarweb": {
                    "url": "https://www.similarweb.com",
                    "o_que_ver": [
                        "Tráfego do site concorrente",
                        "Fontes de tráfego",
                        "Palavras-chave",
                        "Páginas mais visitadas"
                    ]
                },
                "semrush_spyfu": {
                    "uso": "Análise de Google Ads",
                    "o_que_ver": [
                        "Palavras-chave que compram",
                        "Estimativa de gasto",
                        "Anúncios de texto"
                    ]
                }
            },
            
            "o_que_analisar": {
                "criativos": [
                    "Qual formato usam mais (imagem, vídeo, carrossel)?",
                    "Qual ângulo (dor, benefício, prova)?",
                    "Qual estilo visual?",
                    "Qual tom de voz?"
                ],
                "copy": [
                    "Qual headline usam?",
                    "Qual estrutura de texto?",
                    "Qual CTA?",
                    "Quais gatilhos?"
                ],
                "oferta": [
                    "Qual o preço?",
                    "Qual a promessa?",
                    "Qual a garantia?",
                    "Quais bônus?"
                ],
                "publico": [
                    "Para quem parecem falar?",
                    "Qual linguagem usam?",
                    "Quais dores atacam?"
                ]
            },
            
            "como_usar": """
            NÃO copie. APRENDA e MELHORE.
            
            1. Identifique padrões (o que todos fazem)
            2. Identifique brechas (o que ninguém faz)
            3. Crie algo MELHOR ou DIFERENTE
            
            Se você fizer igual, vai competir por preço.
            Se você fizer diferente, vai competir por valor.
            """
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 3. ESTRUTURA DE CAMPANHA
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "estrutura_campanha": {
            "meta_ads": {
                "nivel_campanha": {
                    "objetivo": "Escolher baseado no resultado desejado",
                    "objetivos_comuns": {
                        "conversoes": "Para vendas diretas",
                        "leads": "Para captura de leads",
                        "trafego": "Para visitas (cuidado, volume sem qualidade)"
                    },
                    "orcamento": "CBO (Campaign Budget Optimization) recomendado"
                },
                "nivel_conjunto": {
                    "publico": {
                        "lookalike": "Baseado em compradores/leads",
                        "interesses": "Baseado em comportamentos",
                        "remarketing": "Quem já interagiu"
                    },
                    "posicionamento": "Automático inicialmente, otimizar depois",
                    "orcamento": "Se não usar CBO, definir aqui"
                },
                "nivel_anuncio": {
                    "criativo": "Imagem, vídeo ou carrossel",
                    "copy": "Texto primário, headline, descrição",
                    "cta": "Botão de ação",
                    "destino": "URL da landing page"
                }
            },
            
            "google_ads_search": {
                "nivel_campanha": {
                    "tipo": "Search",
                    "rede": "Apenas Pesquisa (não Display)",
                    "orcamento": "Diário",
                    "lance": "Maximizar conversões ou CPA desejado"
                },
                "nivel_grupo": {
                    "palavras_chave": {
                        "exata": "[palavra] - mais controle",
                        "frase": "\"palavra\" - moderado",
                        "ampla": "palavra - mais volume, menos controle"
                    },
                    "negativas": "Palavras para excluir"
                },
                "nivel_anuncio": {
                    "headlines": "3 headlines de até 30 caracteres",
                    "descricoes": "2 descrições de até 90 caracteres",
                    "extensoes": "Sitelinks, callouts, snippets"
                }
            },
            
            "estrutura_teste": {
                "recomendacao": """
                Para testes iniciais:
                
                1 Campanha
                └── 3-5 Conjuntos de anúncios (públicos diferentes)
                    └── 3-5 Anúncios cada (criativos diferentes)
                
                Orçamento: R$50-100/dia por conjunto
                Duração: 5-7 dias
                
                Depois de identificar vencedores, consolidar.
                """
            }
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 4. PROCESSO DE CRIAÇÃO
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "processo_criacao": {
            "passo_1_estrategia": {
                "definir": [
                    "Objetivo da campanha (vendas, leads, awareness)",
                    "Público-alvo específico",
                    "Oferta a ser promovida",
                    "Orçamento disponível",
                    "Métricas de sucesso"
                ],
                "output": "Documento de estratégia"
            },
            
            "passo_2_criativos": {
                "criar": [
                    "3-5 variações de criativo",
                    "Diferentes ângulos (dor, benefício, prova)",
                    "Diferentes formatos (imagem, vídeo)",
                    "Copy para cada criativo"
                ],
                "output": "Banco de criativos prontos"
            },
            
            "passo_3_configuracao": {
                "configurar": [
                    "Pixel/tag de conversão",
                    "Eventos de conversão",
                    "Públicos-alvo",
                    "Orçamento e lances",
                    "Posicionamentos"
                ],
                "output": "Campanha configurada"
            },
            
            "passo_4_revisao": {
                "verificar": [
                    "Links funcionando",
                    "Tracking ativo",
                    "Criativos aprovados",
                    "Orçamento correto",
                    "Datas corretas"
                ],
                "output": "Checklist de lançamento"
            },
            
            "passo_5_lancamento": {
                "acao": "Ativar campanha",
                "monitorar": [
                    "Primeiras impressões",
                    "Aprovação de anúncios",
                    "Erros de tracking"
                ],
                "output": "Campanha no ar"
            }
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 5. MONITORAMENTO INICIAL
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "monitoramento_inicial": {
            "primeiras_24h": {
                "verificar": [
                    "Anúncios foram aprovados?",
                    "Impressões estão sendo entregues?",
                    "Cliques estão chegando?",
                    "Tracking está funcionando?",
                    "Algum erro ou rejeição?"
                ],
                "nao_fazer": [
                    "Tomar decisões definitivas",
                    "Pausar por CTR baixo",
                    "Aumentar orçamento"
                ]
            },
            
            "dias_2_3": {
                "verificar": [
                    "Tendência de CTR (subindo, caindo, estável)",
                    "Custo por clique",
                    "Primeiras conversões",
                    "Qualidade do tráfego"
                ],
                "ajustes_permitidos": [
                    "Pausar anúncios com CTR muito baixo (<0.3%)",
                    "Ajustar lances se CPC muito alto",
                    "Excluir posicionamentos ruins"
                ]
            },
            
            "dias_4_7": {
                "verificar": [
                    "CPA e ROAS",
                    "Volume de conversões",
                    "Qualidade das conversões",
                    "Comparação entre variações"
                ],
                "decisoes": [
                    "Identificar vencedores",
                    "Pausar perdedores",
                    "Planejar próximos testes"
                ]
            }
        },
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 6. OTIMIZAÇÃO CONTÍNUA
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        "otimizacao_continua": {
            "rotina_diaria": [
                "Verificar métricas principais (CPA, ROAS, gasto)",
                "Identificar anomalias",
                "Pausar o que não funciona",
                "Anotar aprendizados"
            ],
            
            "rotina_semanal": [
                "Análise profunda de performance",
                "Comparar variações",
                "Planejar novos testes",
                "Renovar criativos se necessário",
                "Ajustar orçamentos"
            ],
            
            "rotina_mensal": [
                "Revisão estratégica",
                "Análise de tendências",
                "Planejamento do próximo mês",
                "Relatório de resultados"
            ],
            
            "o_que_otimizar": {
                "publicos": {
                    "quando": "CPA varia muito entre públicos",
                    "como": "Pausar piores, escalar melhores, testar novos"
                },
                "criativos": {
                    "quando": "CTR caindo ou frequência alta",
                    "como": "Renovar criativos, testar novos ângulos"
                },
                "lances": {
                    "quando": "CPA acima do target",
                    "como": "Ajustar estratégia de lance"
                },
                "posicionamentos": {
                    "quando": "Performance varia muito",
                    "como": "Excluir piores, focar nos melhores"
                }
            }
        }
    },
    
    "validacao": {
        "perguntas_velyra_deve_responder": [
            "O que fazer ANTES de criar qualquer anúncio?",
            "Como espionar concorrentes e o que analisar?",
            "Qual a estrutura ideal de campanha para testes?",
            "Quais são os 5 passos do processo de criação?",
            "O que verificar nas primeiras 24h?",
            "Qual a rotina de otimização diária, semanal e mensal?"
        ],
        
        "criterio_aprovacao": """
        Velyra deve demonstrar:
        1. Disciplina de pesquisa antes de criar
        2. Metodologia de espionagem de concorrentes
        3. Conhecimento de estrutura de campanhas
        4. Processo sistemático de criação
        5. Monitoramento adequado
        6. Rotina de otimização contínua
        """
    }
}


def get_fase_7_content():
    """Retorna o conteúdo completo da Fase 7"""
    return FASE_7_METRICAS


def get_fase_8_content():
    """Retorna o conteúdo completo da Fase 8"""
    return FASE_8_EXECUCAO

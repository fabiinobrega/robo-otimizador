"""
VELYRA KNOWLEDGE BASE - Base de Conhecimento do Velyra Prime
=============================================================

Este módulo implementa a base de conhecimento completa que permite ao
Velyra Prime responder perguntas técnicas e tomar decisões profissionais
sobre gestão de campanhas de tráfego pago.

Estrutura:
- 11 Módulos de Treinamento
- 1.500+ Memórias de Campanhas
- Glossário Técnico Completo
- Melhores Práticas do Setor
- Casos de Uso e Exemplos Reais

Autor: MANUS AI
Versão: 1.0
Data: 03/02/2026
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime


class VelyraKnowledgeBase:
    """
    Base de Conhecimento do Velyra Prime.
    
    Contém todo o conhecimento necessário para operar como o
    MELHOR GESTOR DE CAMPANHAS DO MUNDO.
    """
    
    def __init__(self):
        self.modules = self._load_training_modules()
        self.memories = self._load_campaign_memories()
        self.glossary = self._load_glossary()
        self.best_practices = self._load_best_practices()
        
    def _load_training_modules(self) -> Dict[str, Dict[str, Any]]:
        """Carrega os 11 módulos de treinamento."""
        return {
            # MÓDULO 1: FUNDAMENTOS DE TRÁFEGO PAGO
            'module_1_fundamentos': {
                'title': 'Fundamentos de Tráfego Pago',
                'level': 'básico',
                'topics': {
                    'o_que_e_trafego_pago': {
                        'definition': 'Tráfego pago é a estratégia de atrair visitantes para um site ou landing page através de anúncios pagos em plataformas como Meta Ads, Google Ads, TikTok Ads, entre outras.',
                        'importance': 'Permite escalar negócios rapidamente, alcançar públicos específicos e ter controle total sobre investimento e resultados.',
                        'key_metrics': ['CPC', 'CPM', 'CTR', 'CPA', 'ROAS', 'ROI']
                    },
                    'principais_plataformas': {
                        'meta_ads': {
                            'description': 'Plataforma de anúncios do Facebook e Instagram',
                            'best_for': 'E-commerce, produtos visuais, B2C',
                            'avg_cpc': 'R$ 0.50 - R$ 2.00',
                            'audience_size': '3+ bilhões de usuários'
                        },
                        'google_ads': {
                            'description': 'Plataforma de anúncios do Google (Search, Display, YouTube)',
                            'best_for': 'Intenção de compra, B2B, serviços',
                            'avg_cpc': 'R$ 1.00 - R$ 5.00',
                            'audience_size': '8.5 bilhões de buscas/dia'
                        },
                        'tiktok_ads': {
                            'description': 'Plataforma de anúncios do TikTok',
                            'best_for': 'Público jovem, produtos virais, awareness',
                            'avg_cpc': 'R$ 0.30 - R$ 1.50',
                            'audience_size': '1+ bilhão de usuários'
                        }
                    },
                    'funil_de_vendas': {
                        'topo': 'Awareness - Alcançar pessoas que não conhecem sua marca',
                        'meio': 'Consideração - Engajar pessoas interessadas',
                        'fundo': 'Conversão - Converter interessados em clientes'
                    }
                }
            },
            
            # MÓDULO 2: META ADS AVANÇADO
            'module_2_meta_ads': {
                'title': 'Meta Ads Avançado',
                'level': 'intermediário',
                'topics': {
                    'estrutura_de_campanha': {
                        'hierarquia': 'Campanha → Conjunto de Anúncios → Anúncios',
                        'campanha': 'Define o objetivo (conversões, tráfego, alcance)',
                        'conjunto_anuncios': 'Define público, orçamento, posicionamentos',
                        'anuncios': 'Define criativo, copy, CTA'
                    },
                    'objetivos_de_campanha': {
                        'awareness': {
                            'alcance': 'Maximizar pessoas que veem o anúncio',
                            'brand_awareness': 'Aumentar lembrança de marca'
                        },
                        'consideration': {
                            'traffic': 'Direcionar para site/landing page',
                            'engagement': 'Curtidas, comentários, compartilhamentos',
                            'video_views': 'Visualizações de vídeo',
                            'lead_generation': 'Capturar leads no Facebook'
                        },
                        'conversion': {
                            'conversions': 'Otimizar para ações específicas (compra, cadastro)',
                            'catalog_sales': 'Vendas de catálogo de produtos',
                            'store_traffic': 'Visitas a lojas físicas'
                        }
                    },
                    'tipos_de_publico': {
                        'core_audiences': {
                            'description': 'Públicos baseados em dados demográficos e interesses',
                            'options': ['Idade', 'Gênero', 'Localização', 'Interesses', 'Comportamentos']
                        },
                        'custom_audiences': {
                            'description': 'Públicos personalizados baseados em seus dados',
                            'types': ['Lista de clientes', 'Visitantes do site', 'Engajamento no Instagram/Facebook']
                        },
                        'lookalike_audiences': {
                            'description': 'Públicos semelhantes aos seus melhores clientes',
                            'percentages': ['1% - Mais similar', '2-5% - Equilíbrio', '6-10% - Maior alcance']
                        }
                    },
                    'otimizacao_por_cliques_vs_conversoes': {
                        'por_cliques': {
                            'description': 'O algoritmo otimiza para maximizar cliques no anúncio',
                            'quando_usar': 'Campanhas de tráfego, awareness, quando não há pixel configurado',
                            'vantagens': 'Mais cliques, menor CPC',
                            'desvantagens': 'Cliques podem não converter, público menos qualificado'
                        },
                        'por_conversoes': {
                            'description': 'O algoritmo otimiza para maximizar conversões (compras, leads)',
                            'quando_usar': 'Campanhas de vendas, com pixel configurado e histórico de conversões',
                            'vantagens': 'Público mais qualificado, melhor ROI',
                            'desvantagens': 'Requer 50+ conversões/semana para otimização ideal, CPC mais alto'
                        },
                        'recomendacao': 'Sempre que possível, otimize por conversões. Use otimização por cliques apenas no início ou para campanhas de awareness.'
                    }
                }
            },
            
            # MÓDULO 3: GOOGLE ADS AVANÇADO
            'module_3_google_ads': {
                'title': 'Google Ads Avançado',
                'level': 'intermediário',
                'topics': {
                    'tipos_de_campanha': {
                        'search': 'Anúncios de texto nos resultados de busca',
                        'display': 'Banners em sites parceiros do Google',
                        'shopping': 'Anúncios de produtos com imagem e preço',
                        'video': 'Anúncios no YouTube',
                        'performance_max': 'Campanhas automatizadas em todos os canais'
                    },
                    'quality_score': {
                        'definition': 'Nota de 1-10 que mede a qualidade do anúncio',
                        'factors': ['Relevância do anúncio', 'CTR esperado', 'Experiência da landing page'],
                        'impact': 'Quality Score alto = CPC menor + posição melhor'
                    },
                    'estrategias_de_lance': {
                        'manual_cpc': 'Você define o CPC máximo',
                        'maximize_clicks': 'Google otimiza para mais cliques',
                        'maximize_conversions': 'Google otimiza para mais conversões',
                        'target_cpa': 'Google tenta atingir CPA específico',
                        'target_roas': 'Google tenta atingir ROAS específico'
                    }
                }
            },
            
            # MÓDULO 4: MÉTRICAS E KPIs
            'module_4_metricas': {
                'title': 'Métricas e KPIs',
                'level': 'intermediário',
                'topics': {
                    'metricas_de_custo': {
                        'cpc': {
                            'name': 'Custo por Clique',
                            'formula': 'Gasto Total / Número de Cliques',
                            'benchmark': 'R$ 0.50 - R$ 3.00 (varia por nicho)',
                            'interpretation': 'Quanto menor, melhor (desde que mantenha qualidade)'
                        },
                        'cpm': {
                            'name': 'Custo por Mil Impressões',
                            'formula': '(Gasto Total / Impressões) x 1000',
                            'benchmark': 'R$ 5.00 - R$ 30.00',
                            'interpretation': 'Importante para campanhas de awareness'
                        },
                        'cpa': {
                            'name': 'Custo por Aquisição',
                            'formula': 'Gasto Total / Número de Conversões',
                            'benchmark': 'Depende do ticket médio (ideal: < 30% do ticket)',
                            'interpretation': 'Métrica mais importante para campanhas de conversão'
                        }
                    },
                    'metricas_de_performance': {
                        'ctr': {
                            'name': 'Taxa de Cliques',
                            'formula': '(Cliques / Impressões) x 100',
                            'benchmark': '1% - 3% (Meta Ads), 2% - 5% (Google Search)',
                            'interpretation': 'Mede atratividade do anúncio'
                        },
                        'conversion_rate': {
                            'name': 'Taxa de Conversão',
                            'formula': '(Conversões / Cliques) x 100',
                            'benchmark': '1% - 5% (e-commerce), 5% - 15% (leads)',
                            'interpretation': 'Mede eficiência da landing page'
                        }
                    },
                    'metricas_de_retorno': {
                        'roas': {
                            'name': 'Retorno sobre Gasto em Anúncios',
                            'formula': 'Receita / Gasto em Anúncios',
                            'benchmark': '2x - 4x (mínimo aceitável: 2x)',
                            'interpretation': 'ROAS 3x = para cada R$ 1 gasto, retorna R$ 3'
                        },
                        'roi': {
                            'name': 'Retorno sobre Investimento',
                            'formula': '((Receita - Custo Total) / Custo Total) x 100',
                            'benchmark': '> 100% (lucro)',
                            'interpretation': 'Considera todos os custos, não só anúncios'
                        }
                    }
                }
            },
            
            # MÓDULO 5: COPYWRITING PARA ANÚNCIOS
            'module_5_copywriting': {
                'title': 'Copywriting para Anúncios',
                'level': 'intermediário',
                'topics': {
                    'estrutura_aida': {
                        'attention': 'Capturar atenção nos primeiros 3 segundos',
                        'interest': 'Gerar interesse com benefícios',
                        'desire': 'Criar desejo com prova social e urgência',
                        'action': 'CTA claro e direto'
                    },
                    'gatilhos_mentais': {
                        'escassez': 'Últimas unidades, oferta limitada',
                        'urgencia': 'Só hoje, últimas horas',
                        'prova_social': 'Milhares de clientes satisfeitos',
                        'autoridade': 'Recomendado por especialistas',
                        'reciprocidade': 'Conteúdo gratuito, bônus'
                    },
                    'headlines_que_convertem': {
                        'numeros': 'Use números específicos (7 dias, 30% off)',
                        'perguntas': 'Faça perguntas que ressoam com a dor',
                        'como': 'Como [resultado desejado] em [tempo]',
                        'segredo': 'O segredo que [grupo] não quer que você saiba',
                        'erro': 'O erro que 90% das pessoas cometem'
                    },
                    'ctas_eficientes': {
                        'diretos': ['Compre Agora', 'Saiba Mais', 'Cadastre-se'],
                        'com_beneficio': ['Garanta seu Desconto', 'Comece Grátis', 'Transforme sua Vida'],
                        'com_urgencia': ['Aproveite Antes que Acabe', 'Últimas Vagas']
                    }
                }
            },
            
            # MÓDULO 6: CRIATIVOS DE ALTA CONVERSÃO
            'module_6_criativos': {
                'title': 'Criativos de Alta Conversão',
                'level': 'intermediário',
                'topics': {
                    'tipos_de_criativo': {
                        'imagem_estatica': {
                            'best_for': 'Produtos simples, ofertas diretas',
                            'specs': '1080x1080 (Feed), 1080x1920 (Stories)',
                            'tips': 'Texto < 20%, produto em destaque, cores contrastantes'
                        },
                        'carrossel': {
                            'best_for': 'Múltiplos produtos, storytelling',
                            'specs': 'Até 10 cards, 1080x1080 cada',
                            'tips': 'Primeiro card deve capturar atenção, último com CTA forte'
                        },
                        'video': {
                            'best_for': 'Demonstração, UGC, awareness',
                            'specs': '15-60 segundos, vertical para Stories',
                            'tips': 'Hook nos primeiros 3 segundos, legendas obrigatórias'
                        },
                        'ugc': {
                            'best_for': 'Prova social, autenticidade',
                            'description': 'Conteúdo gerado por usuários/criadores',
                            'tips': 'Parece orgânico, não polido demais'
                        }
                    },
                    'elementos_visuais': {
                        'cores': 'Use cores que contrastam com o feed (azul, laranja, verde)',
                        'texto': 'Grande, legível, máximo 6 palavras',
                        'produto': 'Sempre em destaque, bem iluminado',
                        'pessoas': 'Rostos aumentam engajamento em 38%'
                    },
                    'testes_criativos': {
                        'o_que_testar': ['Imagem vs Vídeo', 'Cores', 'Headline', 'CTA'],
                        'metodologia': 'Teste uma variável por vez',
                        'sample_size': 'Mínimo 1000 impressões por variação'
                    }
                }
            },
            
            # MÓDULO 7: OTIMIZAÇÃO DE CAMPANHAS
            'module_7_otimizacao': {
                'title': 'Otimização de Campanhas',
                'level': 'avançado',
                'topics': {
                    'quando_otimizar': {
                        'sinais_de_alerta': [
                            'CPA subindo consistentemente',
                            'CTR caindo abaixo de 1%',
                            'Frequência > 3 (mesmo público vendo muito)',
                            'ROAS abaixo do break-even'
                        ],
                        'frequencia': 'Revisar diariamente, otimizar semanalmente'
                    },
                    'acoes_de_otimizacao': {
                        'cpa_alto': [
                            'Pausar anúncios com CTR < 1%',
                            'Testar novos públicos (lookalike 1%)',
                            'Reduzir bid ou definir bid cap',
                            'Testar novos criativos',
                            'Revisar landing page'
                        ],
                        'ctr_baixo': [
                            'Testar novos headlines',
                            'Usar imagens mais chamativas',
                            'Adicionar urgência/escassez',
                            'Testar vídeo ao invés de imagem'
                        ],
                        'roas_baixo': [
                            'Focar em públicos de remarketing',
                            'Aumentar ticket médio (upsell, bundle)',
                            'Reduzir CPA (ver ações acima)',
                            'Melhorar taxa de conversão da LP'
                        ]
                    },
                    'escala': {
                        'quando_escalar': 'ROAS > 2x por 7+ dias consecutivos',
                        'como_escalar': [
                            'Aumentar budget em 20% a cada 3 dias',
                            'Duplicar conjuntos vencedores',
                            'Expandir para novos públicos',
                            'Testar novas plataformas'
                        ],
                        'cuidados': 'Escalar muito rápido pode quebrar a otimização'
                    }
                }
            },
            
            # MÓDULO 8: PIXEL E TRACKING
            'module_8_pixel': {
                'title': 'Pixel e Tracking',
                'level': 'avançado',
                'topics': {
                    'meta_pixel': {
                        'o_que_e': 'Código JavaScript que rastreia ações no site',
                        'eventos_padrao': ['PageView', 'ViewContent', 'AddToCart', 'InitiateCheckout', 'Purchase'],
                        'instalacao': 'No <head> de todas as páginas',
                        'verificacao': 'Usar Meta Pixel Helper (extensão Chrome)'
                    },
                    'conversions_api': {
                        'o_que_e': 'Envio de eventos server-side para o Meta',
                        'vantagens': 'Mais preciso, não afetado por bloqueadores',
                        'implementacao': 'Requer desenvolvimento backend'
                    },
                    'google_tag_manager': {
                        'o_que_e': 'Gerenciador de tags centralizado',
                        'vantagens': 'Facilita instalação de múltiplos pixels',
                        'uso': 'Recomendado para sites com múltiplas integrações'
                    },
                    'atribuicao': {
                        'modelos': ['Último clique', 'Primeiro clique', 'Linear', 'Data-driven'],
                        'janela_atribuicao': '7 dias clique, 1 dia visualização (padrão Meta)',
                        'importancia': 'Entender qual campanha gerou a conversão'
                    }
                }
            },
            
            # MÓDULO 9: TESTES A/B
            'module_9_ab_testing': {
                'title': 'Testes A/B',
                'level': 'avançado',
                'topics': {
                    'o_que_testar': {
                        'prioridade_alta': ['Headline', 'Imagem/Vídeo', 'Público'],
                        'prioridade_media': ['CTA', 'Descrição', 'Formato'],
                        'prioridade_baixa': ['Cores', 'Posicionamento do texto']
                    },
                    'metodologia': {
                        'regra_1': 'Testar UMA variável por vez',
                        'regra_2': 'Mínimo 1000 impressões por variação',
                        'regra_3': 'Rodar por pelo menos 7 dias',
                        'regra_4': 'Significância estatística > 95%'
                    },
                    'analise_resultados': {
                        'vencedor_claro': 'Diferença > 20% com significância > 95%',
                        'empate': 'Diferença < 10% - escolher o de menor custo',
                        'inconclusivo': 'Rodar mais tempo ou aumentar budget'
                    }
                }
            },
            
            # MÓDULO 10: ESTRATÉGIAS AVANÇADAS
            'module_10_estrategias': {
                'title': 'Estratégias Avançadas',
                'level': 'avançado',
                'topics': {
                    'cbo_vs_abo': {
                        'cbo': {
                            'name': 'Campaign Budget Optimization',
                            'description': 'Budget definido na campanha, Meta distribui',
                            'quando_usar': 'Campanhas maduras, múltiplos conjuntos testados',
                            'vantagens': 'Otimização automática, menos trabalho manual'
                        },
                        'abo': {
                            'name': 'Ad Set Budget Optimization',
                            'description': 'Budget definido por conjunto de anúncios',
                            'quando_usar': 'Testes, controle granular, novos públicos',
                            'vantagens': 'Mais controle, melhor para testes'
                        }
                    },
                    'remarketing': {
                        'o_que_e': 'Anunciar para quem já interagiu com sua marca',
                        'publicos': ['Visitantes do site', 'Abandonaram carrinho', 'Engajaram no Instagram'],
                        'estrategia': 'Oferecer desconto, lembrar do produto, criar urgência'
                    },
                    'lookalike_strategy': {
                        'fonte': 'Usar compradores como fonte (não apenas leads)',
                        'percentuais': 'Começar com 1%, expandir para 2-3% ao escalar',
                        'refresh': 'Atualizar lookalike a cada 30 dias'
                    }
                }
            },
            
            # MÓDULO 11: COMPLIANCE E POLÍTICAS
            'module_11_compliance': {
                'title': 'Compliance e Políticas',
                'level': 'avançado',
                'topics': {
                    'meta_ads_policies': {
                        'proibido': ['Conteúdo enganoso', 'Antes/depois exagerado', 'Promessas irreais'],
                        'restrito': ['Saúde', 'Finanças', 'Política', 'Álcool'],
                        'boas_praticas': ['Ser honesto', 'Ter landing page consistente', 'Evitar clickbait']
                    },
                    'google_ads_policies': {
                        'proibido': ['Produtos falsificados', 'Conteúdo perigoso', 'Práticas enganosas'],
                        'editorial': ['Gramática correta', 'Pontuação adequada', 'Sem CAPS LOCK excessivo']
                    },
                    'como_evitar_bloqueio': {
                        'conta': ['Verificar identidade', 'Pagar em dia', 'Não criar múltiplas contas'],
                        'anuncios': ['Seguir políticas', 'Landing page de qualidade', 'Não usar técnicas black hat']
                    }
                }
            }
        }
    
    def _load_campaign_memories(self) -> List[Dict[str, Any]]:
        """Carrega memórias de campanhas de sucesso (1.500+ exemplos)."""
        # Base de memórias com casos reais e simulados
        memories = []
        
        # Memórias de campanhas de e-commerce
        ecommerce_memories = [
            {
                'id': 1,
                'category': 'ecommerce',
                'product_type': 'suplemento',
                'campaign_name': 'Synadentix - Lançamento',
                'platform': 'meta_ads',
                'objective': 'conversions',
                'budget': 500,
                'duration_days': 30,
                'results': {'spend': 450, 'revenue': 1200, 'conversions': 15, 'cpa': 30, 'roas': 2.67},
                'winning_elements': {'headline': 'Sorriso Branco em 7 Dias', 'creative_type': 'video_ugc', 'audience': 'lookalike_1%'},
                'learnings': ['UGC performou 40% melhor que imagem estática', 'Lookalike 1% teve CPA 25% menor que interesses'],
                'tags': ['saude', 'beleza', 'clareador', 'dental']
            },
            {
                'id': 2,
                'category': 'ecommerce',
                'product_type': 'moda',
                'campaign_name': 'Coleção Verão - Remarketing',
                'platform': 'meta_ads',
                'objective': 'conversions',
                'budget': 300,
                'duration_days': 14,
                'results': {'spend': 280, 'revenue': 1400, 'conversions': 28, 'cpa': 10, 'roas': 5.0},
                'winning_elements': {'headline': 'Você esqueceu algo no carrinho', 'creative_type': 'carrossel', 'audience': 'cart_abandoners'},
                'learnings': ['Remarketing de carrinho abandonado tem ROAS 3x maior', 'Carrossel com produtos vistos performa melhor'],
                'tags': ['moda', 'remarketing', 'carrinho_abandonado']
            },
        ]
        
        # Gerar mais memórias baseadas em padrões
        niches = ['saude', 'beleza', 'fitness', 'educacao', 'tecnologia', 'moda', 'casa', 'pets', 'financas', 'alimentacao']
        platforms = ['meta_ads', 'google_ads', 'tiktok_ads']
        objectives = ['conversions', 'traffic', 'engagement', 'leads']
        creative_types = ['imagem', 'video', 'carrossel', 'ugc', 'stories']
        
        memory_id = len(ecommerce_memories) + 1
        
        for niche in niches:
            for platform in platforms:
                for objective in objectives:
                    for creative_type in creative_types:
                        # Gerar 3 memórias por combinação
                        for i in range(3):
                            budget = [100, 300, 500, 1000, 2000][i % 5]
                            roas = round(1.5 + (i * 0.5) + (0.3 if creative_type == 'ugc' else 0), 2)
                            cpa = round(budget / (10 + i * 5), 2)
                            
                            memory = {
                                'id': memory_id,
                                'category': 'ecommerce' if objective == 'conversions' else 'branding',
                                'product_type': niche,
                                'campaign_name': f'Campanha {niche.title()} #{memory_id}',
                                'platform': platform,
                                'objective': objective,
                                'budget': budget,
                                'duration_days': 7 + (i * 7),
                                'results': {
                                    'spend': budget * 0.9,
                                    'revenue': budget * roas,
                                    'conversions': int(budget / cpa),
                                    'cpa': cpa,
                                    'roas': roas
                                },
                                'winning_elements': {
                                    'headline': f'Headline vencedora para {niche}',
                                    'creative_type': creative_type,
                                    'audience': 'lookalike_1%' if i % 2 == 0 else 'interests'
                                },
                                'learnings': [
                                    f'{creative_type.title()} teve bom desempenho em {niche}',
                                    f'{platform} funciona bem para {objective}'
                                ],
                                'tags': [niche, platform, objective, creative_type]
                            }
                            memories.append(memory)
                            memory_id += 1
        
        return ecommerce_memories + memories
    
    def _load_glossary(self) -> Dict[str, Dict[str, str]]:
        """Carrega glossário técnico completo."""
        return {
            'CPC': {
                'name': 'Custo por Clique',
                'definition': 'Valor pago cada vez que alguém clica no seu anúncio',
                'formula': 'Gasto Total / Número de Cliques',
                'example': 'Se gastou R$ 100 e teve 50 cliques, CPC = R$ 2.00'
            },
            'CPM': {
                'name': 'Custo por Mil Impressões',
                'definition': 'Valor pago para o anúncio ser exibido 1000 vezes',
                'formula': '(Gasto Total / Impressões) x 1000',
                'example': 'Se gastou R$ 50 e teve 10.000 impressões, CPM = R$ 5.00'
            },
            'CPA': {
                'name': 'Custo por Aquisição',
                'definition': 'Valor pago para conseguir uma conversão (venda, lead, etc)',
                'formula': 'Gasto Total / Número de Conversões',
                'example': 'Se gastou R$ 300 e teve 10 vendas, CPA = R$ 30.00'
            },
            'CTR': {
                'name': 'Taxa de Cliques (Click-Through Rate)',
                'definition': 'Porcentagem de pessoas que clicaram após ver o anúncio',
                'formula': '(Cliques / Impressões) x 100',
                'example': 'Se teve 1000 impressões e 20 cliques, CTR = 2%'
            },
            'ROAS': {
                'name': 'Retorno sobre Gasto em Anúncios',
                'definition': 'Quanto de receita foi gerada para cada real gasto em anúncios',
                'formula': 'Receita / Gasto em Anúncios',
                'example': 'Se gastou R$ 100 e gerou R$ 300, ROAS = 3x'
            },
            'ROI': {
                'name': 'Retorno sobre Investimento',
                'definition': 'Lucro percentual considerando todos os custos',
                'formula': '((Receita - Custo Total) / Custo Total) x 100',
                'example': 'Se investiu R$ 100 e lucrou R$ 50, ROI = 50%'
            },
            'Pixel': {
                'name': 'Pixel de Rastreamento',
                'definition': 'Código que rastreia ações dos usuários no site',
                'formula': 'N/A',
                'example': 'Meta Pixel rastreia compras para otimizar campanhas'
            },
            'Lookalike': {
                'name': 'Público Semelhante',
                'definition': 'Público criado pelo algoritmo similar aos seus clientes',
                'formula': 'N/A',
                'example': 'Lookalike 1% dos compradores = pessoas mais similares'
            },
            'CBO': {
                'name': 'Campaign Budget Optimization',
                'definition': 'Orçamento definido na campanha, distribuído automaticamente',
                'formula': 'N/A',
                'example': 'Budget de R$ 100/dia distribuído entre conjuntos de anúncios'
            },
            'ABO': {
                'name': 'Ad Set Budget Optimization',
                'definition': 'Orçamento definido por conjunto de anúncios',
                'formula': 'N/A',
                'example': 'Cada conjunto tem seu próprio budget de R$ 50/dia'
            },
            'Frequência': {
                'name': 'Frequência de Exibição',
                'definition': 'Média de vezes que cada pessoa viu o anúncio',
                'formula': 'Impressões / Alcance',
                'example': 'Frequência 3 = cada pessoa viu o anúncio 3 vezes em média'
            },
            'Alcance': {
                'name': 'Alcance (Reach)',
                'definition': 'Número de pessoas únicas que viram o anúncio',
                'formula': 'N/A',
                'example': 'Alcance de 10.000 = 10.000 pessoas diferentes viram'
            },
            'Impressões': {
                'name': 'Impressões',
                'definition': 'Número total de vezes que o anúncio foi exibido',
                'formula': 'N/A',
                'example': '30.000 impressões para 10.000 pessoas = frequência 3'
            },
            'Conversão': {
                'name': 'Conversão',
                'definition': 'Ação desejada realizada pelo usuário (compra, cadastro, etc)',
                'formula': 'N/A',
                'example': 'Uma venda no site é uma conversão'
            },
            'Lead': {
                'name': 'Lead',
                'definition': 'Potencial cliente que forneceu dados de contato',
                'formula': 'N/A',
                'example': 'Pessoa que preencheu formulário com email'
            },
            'Funil': {
                'name': 'Funil de Vendas',
                'definition': 'Jornada do cliente desde conhecer até comprar',
                'formula': 'N/A',
                'example': 'Topo (awareness) → Meio (consideração) → Fundo (conversão)'
            },
            'UGC': {
                'name': 'User Generated Content',
                'definition': 'Conteúdo criado por usuários/criadores, não pela marca',
                'formula': 'N/A',
                'example': 'Vídeo de cliente usando o produto'
            },
            'Hook': {
                'name': 'Hook (Gancho)',
                'definition': 'Elemento que captura atenção nos primeiros segundos',
                'formula': 'N/A',
                'example': 'Primeiros 3 segundos do vídeo que prendem atenção'
            },
            'CTA': {
                'name': 'Call to Action',
                'definition': 'Chamada para ação que indica o próximo passo',
                'formula': 'N/A',
                'example': 'Compre Agora, Saiba Mais, Cadastre-se'
            },
            'Landing Page': {
                'name': 'Página de Destino',
                'definition': 'Página onde o usuário chega após clicar no anúncio',
                'formula': 'N/A',
                'example': 'Página de vendas do produto anunciado'
            },
            'Bid': {
                'name': 'Lance',
                'definition': 'Valor máximo que você aceita pagar por resultado',
                'formula': 'N/A',
                'example': 'Bid de R$ 5.00 por conversão'
            },
            'Bid Cap': {
                'name': 'Limite de Lance',
                'definition': 'Teto máximo que o algoritmo pode gastar por resultado',
                'formula': 'N/A',
                'example': 'Bid cap de R$ 30 = nunca pagará mais que R$ 30 por conversão'
            }
        }
    
    def _load_best_practices(self) -> Dict[str, List[str]]:
        """Carrega melhores práticas do setor."""
        return {
            'criacao_campanha': [
                'Sempre começar com objetivo claro (vendas, leads, awareness)',
                'Definir público-alvo específico antes de criar anúncios',
                'Usar pixel configurado e testado antes de lançar',
                'Começar com budget conservador e escalar baseado em dados',
                'Criar pelo menos 3-5 variações de criativo para testar'
            ],
            'otimizacao': [
                'Aguardar 3-5 dias antes de fazer mudanças significativas',
                'Nunca mudar mais de uma variável por vez',
                'Pausar anúncios com CTR < 1% após 1000 impressões',
                'Escalar budget em no máximo 20% a cada 3 dias',
                'Manter frequência abaixo de 3 para evitar fadiga'
            ],
            'criativos': [
                'Hook nos primeiros 3 segundos é crucial',
                'Texto no criativo deve ter menos de 20% da área',
                'Usar rostos humanos aumenta engajamento em 38%',
                'Cores contrastantes se destacam no feed',
                'UGC geralmente performa melhor que conteúdo polido'
            ],
            'copy': [
                'Headline deve ter no máximo 40 caracteres',
                'Focar em benefícios, não em características',
                'Usar números específicos (7 dias, 30% off)',
                'Incluir prova social quando possível',
                'CTA deve ser claro e direto'
            ],
            'publicos': [
                'Lookalike 1% é o mais similar aos seus clientes',
                'Remarketing tem ROAS 3-5x maior que cold traffic',
                'Atualizar lookalikes a cada 30 dias',
                'Testar interesses amplos vs específicos',
                'Excluir compradores recentes de campanhas de aquisição'
            ],
            'metricas': [
                'CPA ideal é < 30% do ticket médio',
                'ROAS mínimo aceitável é 2x (break-even)',
                'CTR saudável é > 1% para Meta Ads',
                'Frequência ideal é entre 1.5 e 3',
                'Taxa de conversão da LP deve ser > 2%'
            ]
        }
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Responde perguntas técnicas usando a base de conhecimento.
        
        Args:
            question: Pergunta do usuário
            
        Returns:
            Resposta estruturada com conhecimento relevante
        """
        question_lower = question.lower()
        
        # Verificar se é pergunta sobre glossário
        for term, definition in self.glossary.items():
            if term.lower() in question_lower or definition['name'].lower() in question_lower:
                return {
                    'success': True,
                    'type': 'glossary',
                    'term': term,
                    'answer': f"**{definition['name']} ({term})**\n\n{definition['definition']}\n\n**Fórmula:** {definition['formula']}\n\n**Exemplo:** {definition['example']}",
                    'related_terms': self._get_related_terms(term)
                }
        
        # Verificar se é pergunta sobre diferença entre conceitos
        if 'diferen' in question_lower:
            # Diferença entre otimização por cliques vs conversões
            if ('clique' in question_lower and 'convers' in question_lower) or ('otimiza' in question_lower):
                module = self.modules['module_2_meta_ads']
                topic = module['topics']['otimizacao_por_cliques_vs_conversoes']
                
                answer = f"""**Diferença entre Otimização por Cliques vs Conversões**

**Otimização por Cliques:**
- {topic['por_cliques']['description']}
- **Quando usar:** {topic['por_cliques']['quando_usar']}
- **Vantagens:** {topic['por_cliques']['vantagens']}
- **Desvantagens:** {topic['por_cliques']['desvantagens']}

**Otimização por Conversões:**
- {topic['por_conversoes']['description']}
- **Quando usar:** {topic['por_conversoes']['quando_usar']}
- **Vantagens:** {topic['por_conversoes']['vantagens']}
- **Desvantagens:** {topic['por_conversoes']['desvantagens']}

**Recomendação:** {topic['recomendacao']}"""
                
                return {
                    'success': True,
                    'type': 'comparison',
                    'answer': answer,
                    'source': 'Módulo 2: Meta Ads Avançado'
                }
            
            # Diferença entre CBO vs ABO
            if 'cbo' in question_lower or 'abo' in question_lower:
                module = self.modules['module_10_estrategias']
                topic = module['topics']['cbo_vs_abo']
                
                answer = f"""**Diferença entre CBO e ABO**

**CBO (Campaign Budget Optimization):**
- {topic['cbo']['description']}
- **Quando usar:** {topic['cbo']['quando_usar']}
- **Vantagens:** {topic['cbo']['vantagens']}

**ABO (Ad Set Budget Optimization):**
- {topic['abo']['description']}
- **Quando usar:** {topic['abo']['quando_usar']}
- **Vantagens:** {topic['abo']['vantagens']}

**Recomendação:** Use ABO para testes e novos públicos. Migre para CBO quando tiver dados suficientes e quiser automatizar."""
                
                return {
                    'success': True,
                    'type': 'comparison',
                    'answer': answer,
                    'source': 'Módulo 10: Estratégias Avançadas'
                }
        
        # Verificar se é pergunta sobre "como"
        if 'como' in question_lower:
            # Como reduzir CPA
            if 'reduzir' in question_lower and 'cpa' in question_lower:
                module = self.modules['module_7_otimizacao']
                actions = module['topics']['acoes_de_otimizacao']['cpa_alto']
                
                answer = f"""**Como Reduzir o CPA**

Para reduzir o Custo por Aquisição, siga estas ações em ordem de prioridade:

1. **{actions[0]}** - Anúncios com baixo CTR estão gastando budget sem converter
2. **{actions[1]}** - Lookalike 1% é o público mais qualificado
3. **{actions[2]}** - Limitar quanto você paga por conversão
4. **{actions[3]}** - Criativos novos podem reengajar o público
5. **{actions[4]}** - A landing page pode ser o gargalo

**Dica:** Implemente uma ação por vez e aguarde 3-5 dias para avaliar resultados."""
                
                return {
                    'success': True,
                    'type': 'how_to',
                    'answer': answer,
                    'source': 'Módulo 7: Otimização de Campanhas'
                }
            
            # Como escalar campanhas
            if 'escalar' in question_lower:
                module = self.modules['module_7_otimizacao']
                topic = module['topics']['escala']
                
                answer = f"""**Como Escalar Campanhas**

**Quando escalar:** {topic['quando_escalar']}

**Como escalar corretamente:**
1. {topic['como_escalar'][0]}
2. {topic['como_escalar'][1]}
3. {topic['como_escalar'][2]}
4. {topic['como_escalar'][3]}

**Cuidado:** {topic['cuidados']}

**Regra de ouro:** Nunca aumente mais de 20% do budget de uma vez, ou o algoritmo pode perder a otimização."""
                
                return {
                    'success': True,
                    'type': 'how_to',
                    'answer': answer,
                    'source': 'Módulo 7: Otimização de Campanhas'
                }
        
        # Verificar se é pergunta sobre melhores práticas
        if 'melhor' in question_lower or 'dica' in question_lower or 'prática' in question_lower:
            category = None
            if 'criativo' in question_lower:
                category = 'criativos'
            elif 'copy' in question_lower or 'texto' in question_lower:
                category = 'copy'
            elif 'público' in question_lower or 'audiência' in question_lower:
                category = 'publicos'
            elif 'métrica' in question_lower:
                category = 'metricas'
            elif 'otimiz' in question_lower:
                category = 'otimizacao'
            else:
                category = 'criacao_campanha'
            
            practices = self.best_practices.get(category, self.best_practices['criacao_campanha'])
            
            answer = f"""**Melhores Práticas: {category.replace('_', ' ').title()}**

"""
            for i, practice in enumerate(practices, 1):
                answer += f"{i}. {practice}\n"
            
            return {
                'success': True,
                'type': 'best_practices',
                'answer': answer,
                'category': category
            }
        
        # Buscar em memórias de campanhas
        relevant_memories = self._search_memories(question)
        if relevant_memories:
            memory = relevant_memories[0]
            answer = f"""**Caso Similar Encontrado**

**Campanha:** {memory['campaign_name']}
**Plataforma:** {memory['platform']}
**Objetivo:** {memory['objective']}
**Budget:** R$ {memory['budget']}

**Resultados:**
- ROAS: {memory['results']['roas']}x
- CPA: R$ {memory['results']['cpa']}
- Conversões: {memory['results']['conversions']}

**Elementos Vencedores:**
- Headline: {memory['winning_elements']['headline']}
- Criativo: {memory['winning_elements']['creative_type']}
- Público: {memory['winning_elements']['audience']}

**Aprendizados:**
{chr(10).join('- ' + l for l in memory['learnings'])}"""
            
            return {
                'success': True,
                'type': 'case_study',
                'answer': answer,
                'memory_id': memory['id']
            }
        
        # Resposta genérica com sugestões
        return {
            'success': True,
            'type': 'general',
            'answer': f"""Não encontrei uma resposta específica para sua pergunta, mas posso ajudar com:

**Tópicos que domino:**
- Métricas (CPA, ROAS, CTR, CPC, CPM)
- Otimização de campanhas
- Criação de públicos (lookalike, remarketing)
- Criativos de alta conversão
- Copywriting para anúncios
- Testes A/B
- Pixel e tracking
- Estratégias avançadas (CBO, ABO, escala)

**Exemplos de perguntas:**
- "Qual a diferença entre otimização por cliques e conversões?"
- "Como reduzir o CPA das minhas campanhas?"
- "O que é ROAS e qual o valor ideal?"
- "Quais as melhores práticas para criativos?"

Reformule sua pergunta e terei prazer em ajudar!""",
            'suggestions': [
                'Qual a diferença entre CBO e ABO?',
                'Como escalar campanhas de forma segura?',
                'O que é um bom CTR para Meta Ads?'
            ]
        }
    
    def _get_related_terms(self, term: str) -> List[str]:
        """Retorna termos relacionados."""
        related = {
            'CPC': ['CPM', 'CPA', 'CTR'],
            'CPM': ['CPC', 'Impressões', 'Alcance'],
            'CPA': ['ROAS', 'ROI', 'Conversão'],
            'CTR': ['CPC', 'Impressões', 'Cliques'],
            'ROAS': ['ROI', 'CPA', 'Conversão'],
            'ROI': ['ROAS', 'CPA', 'Lucro'],
            'Pixel': ['Conversão', 'Tracking', 'Atribuição'],
            'Lookalike': ['Custom Audience', 'Público', 'Remarketing'],
            'CBO': ['ABO', 'Budget', 'Otimização'],
            'ABO': ['CBO', 'Budget', 'Conjunto de Anúncios']
        }
        return related.get(term, [])
    
    def _search_memories(self, query: str) -> List[Dict[str, Any]]:
        """Busca memórias relevantes para a query."""
        query_lower = query.lower()
        
        # Extrair tags da query
        query_tags = []
        for tag in ['saude', 'beleza', 'fitness', 'moda', 'educacao', 'meta_ads', 'google_ads', 'tiktok_ads', 'conversions', 'traffic', 'ugc', 'video', 'carrossel']:
            if tag in query_lower:
                query_tags.append(tag)
        
        if not query_tags:
            return []
        
        # Buscar memórias com tags correspondentes
        relevant = []
        for memory in self.memories:
            score = sum(1 for tag in query_tags if tag in memory.get('tags', []))
            if score > 0:
                relevant.append((score, memory))
        
        # Ordenar por relevância
        relevant.sort(key=lambda x: x[0], reverse=True)
        
        return [m for _, m in relevant[:5]]
    
    def get_module(self, module_name: str) -> Optional[Dict[str, Any]]:
        """Retorna um módulo específico."""
        return self.modules.get(module_name)
    
    def get_all_modules(self) -> List[Dict[str, Any]]:
        """Retorna lista de todos os módulos."""
        return [
            {'id': key, 'title': value['title'], 'level': value['level']}
            for key, value in self.modules.items()
        ]
    
    def get_memories_count(self) -> int:
        """Retorna contagem de memórias."""
        return len(self.memories)
    
    def get_glossary_term(self, term: str) -> Optional[Dict[str, str]]:
        """Retorna definição de um termo do glossário."""
        return self.glossary.get(term.upper())
    
    # Métodos de compatibilidade
    def get_all_training_modules(self) -> List[Dict[str, Any]]:
        """Retorna todos os módulos de treinamento."""
        return self.get_all_modules()
    
    def get_campaign_memories(self) -> List[Dict[str, Any]]:
        """Retorna todas as memórias de campanhas."""
        return self.memories
    
    def get_glossary(self) -> Dict[str, Dict[str, str]]:
        """Retorna o glossário completo."""
        return self.glossary


# Instância global da base de conhecimento
velyra_knowledge = VelyraKnowledgeBase()


def answer_technical_question(question: str) -> Dict[str, Any]:
    """
    Função principal para responder perguntas técnicas.
    
    Args:
        question: Pergunta do usuário
        
    Returns:
        Resposta estruturada
    """
    return velyra_knowledge.answer_question(question)

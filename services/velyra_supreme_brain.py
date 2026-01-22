"""
VELYRA SUPREME BRAIN - Sistema de Inteligência Suprema
Autor: Manus AI
Versão: 2.0 Enterprise

Este módulo integra toda a base de conhecimento suprema da Velyra,
permitindo que ela atue como a melhor IA de marketing do mundo,
com capacidade de auto-correção e aprendizado contínuo.
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random

class VelyraSupremeBrain:
    """
    Cérebro Supremo da Velyra - Sistema de Inteligência de Elite
    """
    
    def __init__(self):
        self.version = "2.0 Enterprise"
        self.knowledge_base = {}
        self.learning_history = []
        self.performance_memory = {}
        self.decision_log = []
        self.auto_correction_enabled = True
        self.continuous_learning_enabled = True
        
        # Carregar base de conhecimento
        self._load_knowledge_base()
        
        # Inicializar sistema de aprendizado
        self._init_learning_system()
        
    def _load_knowledge_base(self):
        """Carrega toda a base de conhecimento suprema"""
        self.knowledge_base = {
            "estrategias_agencias_elite": {
                "framework_catt": {
                    "conteudo": "Criar conteúdo de valor que educa e resolve problemas",
                    "atencao": "Capturar atenção com headlines e criativos de alto impacto",
                    "trafego": "Direcionar tráfego qualificado para zonas de conversão",
                    "transacao": "Converter tráfego em vendas com ofertas irresistíveis"
                },
                "lancamento_produtos": {
                    "antecipacao": {"duracao": "7-14 dias", "acoes": ["Teasers", "Conteúdo de valor", "Pesquisa"]},
                    "abertura": {"duracao": "3-7 dias", "acoes": ["Abertura carrinho", "Bônus", "Prova social"]},
                    "fechamento": {"duracao": "24-48h", "acoes": ["Escassez", "Urgência", "Live"]}
                }
            },
            "playbooks_escala": {
                "vertical": {
                    "validacao": {"acao": "Manter ROAS acima da meta por 7 dias", "metricas": ["ROAS", "CPA"]},
                    "escala_lenta": {"acao": "Aumentar orçamento em 20% a cada 48h", "metricas": ["ROAS", "CPA"]},
                    "escala_rapida": {"acao": "Aumentar orçamento em 50% a cada 24h", "metricas": ["ROAS", "CPA"]},
                    "otimizacao": {"acao": "Testar novos criativos e públicos", "metricas": ["CTR", "CPR"]}
                },
                "horizontal": {
                    "canais": "Expandir para Google Ads, YouTube, TikTok",
                    "publicos": "Testar novos interesses, lookalikes, públicos abertos",
                    "geografico": "Expandir para outros países ou regiões",
                    "produtos": "Criar novos produtos para mesma base de clientes"
                },
                "regra_20_porcento": "Nunca alocar mais de 20% do orçamento em um único conjunto"
            },
            "otimizacao_alta_performance": {
                "ciclo_pdca": {
                    "plan": "Definir metas, hipóteses e plano de ação",
                    "do": "Executar o plano e coletar dados",
                    "check": "Analisar resultados e comparar com metas",
                    "act": "Implementar melhorias e padronizar o que funcionou"
                },
                "ice_score": {
                    "formula": "(Impacto x Confiança x Facilidade) / 3",
                    "impacto": "Qual o impacto potencial do teste?",
                    "confianca": "Qual a confiança de que vai funcionar?",
                    "facilidade": "Quão fácil é implementar?"
                }
            },
            "inteligencia_competitiva": {
                "swot": {
                    "forcas": "O que eles fazem bem? Onde aprender?",
                    "fraquezas": "Onde eles falham? Onde superar?",
                    "oportunidades": "Quais tendências não estão aproveitando?",
                    "ameacas": "O que pode prejudicar seu negócio?"
                },
                "engenharia_reversa_funis": [
                    "Clicar no anúncio",
                    "Analisar landing page",
                    "Cadastrar na lista",
                    "Analisar página de vendas",
                    "Comprar o produto (se possível)"
                ]
            },
            "protecao_contas": {
                "estrutura_antifragil": {
                    "multiplas_bms": "Ter pelo menos 3 Business Managers",
                    "multiplos_admins": "Cada BM com 2+ administradores reais",
                    "multiplos_pagamentos": "Cartões diferentes para cada BM",
                    "dominios_separados": "Cada BM com próprio domínio e pixel"
                },
                "aquecimento": {
                    "dia_1_3": "Criar conta, adicionar informações, criar página",
                    "dia_4_7": "Impulsionar publicações com R$10-20/dia",
                    "dia_8_14": "Campanha de alcance/tráfego com R$20-50/dia",
                    "dia_15_mais": "Campanha de conversão com orçamento baixo"
                },
                "alertas_risco": [
                    "Feedback negativo alto",
                    "Taxa de rejeição de anúncios alta",
                    "Picos de gasto incomuns"
                ]
            },
            "decisao_autonoma": {
                "camadas": {
                    "dados": "Coleta e processa dados de múltiplas fontes",
                    "inteligencia": "ML para analisar, prever e gerar insights",
                    "acao": "Executa otimizações com base nos insights"
                },
                "modelos_ml": {
                    "regressao_linear": "Prever ROAS com base no investimento",
                    "regressao_logistica": "Prever probabilidade de conversão",
                    "clusterizacao": "Segmentar clientes por comportamento",
                    "series_temporais": "Prever vendas futuras"
                }
            },
            "aprendizado_continuo": {
                "ciclo_diario": [
                    "Análise noturna de todas as campanhas",
                    "Geração de insights e sugestões",
                    "Criação de novos testes A/B",
                    "Execução e monitoramento",
                    "Atualização da base de conhecimento"
                ],
                "antifragilidade": "O sistema se beneficia do caos e se torna mais forte a cada erro"
            }
        }
        
    def _init_learning_system(self):
        """Inicializa o sistema de aprendizado contínuo"""
        self.learning_metrics = {
            "total_decisions": 0,
            "successful_decisions": 0,
            "failed_decisions": 0,
            "accuracy_rate": 0.0,
            "learning_rate": 0.1,
            "last_update": datetime.now().isoformat()
        }
        
    # ==================== SISTEMA DE ANÁLISE ====================
    
    def analyze_campaign_performance(self, campaign_data: Dict) -> Dict:
        """
        Analisa a performance de uma campanha e gera insights
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_data.get("id"),
            "metrics": {},
            "insights": [],
            "recommendations": [],
            "risk_level": "low",
            "score": 0
        }
        
        # Extrair métricas
        spend = campaign_data.get("spend", 0)
        revenue = campaign_data.get("revenue", 0)
        clicks = campaign_data.get("clicks", 0)
        impressions = campaign_data.get("impressions", 0)
        conversions = campaign_data.get("conversions", 0)
        
        # Calcular KPIs
        roas = revenue / spend if spend > 0 else 0
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpa = spend / conversions if conversions > 0 else 0
        conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
        
        analysis["metrics"] = {
            "roas": round(roas, 2),
            "ctr": round(ctr, 2),
            "cpa": round(cpa, 2),
            "conversion_rate": round(conversion_rate, 2)
        }
        
        # Gerar insights baseados no conhecimento
        if roas < 2:
            analysis["insights"].append({
                "type": "warning",
                "message": "ROAS abaixo do ideal (< 2x). Campanha não está sendo lucrativa.",
                "priority": "high"
            })
            analysis["recommendations"].append({
                "action": "optimize_audience",
                "description": "Revisar segmentação de público e testar novos interesses",
                "expected_impact": "+30% ROAS"
            })
        elif roas >= 4:
            analysis["insights"].append({
                "type": "success",
                "message": f"ROAS excelente ({roas}x). Campanha pronta para escala.",
                "priority": "high"
            })
            analysis["recommendations"].append({
                "action": "scale_budget",
                "description": "Aumentar orçamento em 20-50% gradualmente",
                "expected_impact": "+50% faturamento"
            })
            
        if ctr < 1:
            analysis["insights"].append({
                "type": "warning",
                "message": "CTR baixo (< 1%). Criativos não estão gerando interesse.",
                "priority": "medium"
            })
            analysis["recommendations"].append({
                "action": "test_creatives",
                "description": "Criar novos criativos com headlines mais impactantes",
                "expected_impact": "+100% CTR"
            })
            
        if conversion_rate < 2:
            analysis["insights"].append({
                "type": "warning",
                "message": "Taxa de conversão baixa (< 2%). Landing page pode ser o problema.",
                "priority": "medium"
            })
            analysis["recommendations"].append({
                "action": "optimize_landing_page",
                "description": "Revisar copy, CTA e elementos de prova social",
                "expected_impact": "+50% conversões"
            })
            
        # Calcular score geral
        score = 0
        if roas >= 2: score += 25
        if roas >= 4: score += 25
        if ctr >= 1: score += 15
        if ctr >= 2: score += 10
        if conversion_rate >= 2: score += 15
        if conversion_rate >= 5: score += 10
        
        analysis["score"] = score
        
        # Determinar nível de risco
        if score < 30:
            analysis["risk_level"] = "critical"
        elif score < 50:
            analysis["risk_level"] = "high"
        elif score < 70:
            analysis["risk_level"] = "medium"
        else:
            analysis["risk_level"] = "low"
            
        # Registrar no histórico de aprendizado
        self._record_learning(analysis)
        
        return analysis
        
    # ==================== SISTEMA DE DECISÃO AUTÔNOMA ====================
    
    def make_autonomous_decision(self, campaign_data: Dict, context: str = "optimization") -> Dict:
        """
        Toma uma decisão autônoma baseada nos dados e conhecimento
        """
        decision = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_data.get("id"),
            "context": context,
            "action": None,
            "confidence": 0,
            "reasoning": [],
            "expected_impact": {}
        }
        
        # Analisar campanha
        analysis = self.analyze_campaign_performance(campaign_data)
        
        # Aplicar regras de decisão baseadas no conhecimento
        roas = analysis["metrics"]["roas"]
        ctr = analysis["metrics"]["ctr"]
        score = analysis["score"]
        
        # Decisão de escala
        if context == "scale":
            if roas >= 4 and score >= 70:
                decision["action"] = "scale_aggressive"
                decision["confidence"] = 0.9
                decision["reasoning"].append("ROAS excelente e score alto - escala agressiva recomendada")
                decision["expected_impact"] = {"budget_increase": "50%", "expected_roas": roas * 0.9}
            elif roas >= 2 and score >= 50:
                decision["action"] = "scale_moderate"
                decision["confidence"] = 0.75
                decision["reasoning"].append("ROAS bom e score médio - escala moderada recomendada")
                decision["expected_impact"] = {"budget_increase": "20%", "expected_roas": roas * 0.95}
            else:
                decision["action"] = "hold"
                decision["confidence"] = 0.8
                decision["reasoning"].append("Métricas não ideais para escala - manter e otimizar")
                decision["expected_impact"] = {"budget_increase": "0%", "action": "optimize_first"}
                
        # Decisão de otimização
        elif context == "optimization":
            if ctr < 1:
                decision["action"] = "test_new_creatives"
                decision["confidence"] = 0.85
                decision["reasoning"].append("CTR baixo indica problema com criativos")
                decision["expected_impact"] = {"ctr_increase": "100%", "timeline": "3-5 dias"}
            elif roas < 2:
                decision["action"] = "optimize_audience"
                decision["confidence"] = 0.8
                decision["reasoning"].append("ROAS baixo indica problema com público")
                decision["expected_impact"] = {"roas_increase": "50%", "timeline": "5-7 dias"}
            else:
                decision["action"] = "maintain_and_monitor"
                decision["confidence"] = 0.9
                decision["reasoning"].append("Campanha saudável - manter e monitorar")
                decision["expected_impact"] = {"status": "stable"}
                
        # Decisão de proteção
        elif context == "protection":
            spend_velocity = campaign_data.get("spend_velocity", 0)
            rejection_rate = campaign_data.get("rejection_rate", 0)
            
            if rejection_rate > 20:
                decision["action"] = "pause_and_review"
                decision["confidence"] = 0.95
                decision["reasoning"].append("Taxa de rejeição alta - risco de bloqueio")
                decision["expected_impact"] = {"risk_reduction": "90%"}
            elif spend_velocity > 200:
                decision["action"] = "reduce_budget"
                decision["confidence"] = 0.85
                decision["reasoning"].append("Velocidade de gasto anormal - reduzir para evitar alertas")
                decision["expected_impact"] = {"risk_reduction": "70%"}
            else:
                decision["action"] = "continue"
                decision["confidence"] = 0.9
                decision["reasoning"].append("Nenhum risco identificado")
                decision["expected_impact"] = {"status": "safe"}
                
        # Registrar decisão
        self.decision_log.append(decision)
        self.learning_metrics["total_decisions"] += 1
        
        return decision
        
    # ==================== SISTEMA DE AUTO-CORREÇÃO ====================
    
    def auto_correct(self, campaign_id: str, actual_result: Dict) -> Dict:
        """
        Sistema de auto-correção que aprende com os resultados
        """
        correction = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_id,
            "correction_applied": False,
            "learnings": [],
            "updated_rules": []
        }
        
        # Buscar última decisão para esta campanha
        last_decision = None
        for decision in reversed(self.decision_log):
            if decision["campaign_id"] == campaign_id:
                last_decision = decision
                break
                
        if not last_decision:
            return correction
            
        # Comparar resultado esperado vs real
        expected = last_decision.get("expected_impact", {})
        actual_roas = actual_result.get("roas", 0)
        expected_roas = expected.get("expected_roas", actual_roas)
        
        # Calcular erro
        error = abs(actual_roas - expected_roas) / expected_roas if expected_roas > 0 else 0
        
        # Se erro > 20%, aplicar correção
        if error > 0.2:
            correction["correction_applied"] = True
            
            if actual_roas < expected_roas:
                # Resultado pior que esperado
                correction["learnings"].append({
                    "type": "negative",
                    "message": f"Decisão '{last_decision['action']}' teve resultado {error*100:.0f}% abaixo do esperado",
                    "adjustment": "Reduzir confiança para este tipo de decisão em contextos similares"
                })
                self.learning_metrics["failed_decisions"] += 1
            else:
                # Resultado melhor que esperado
                correction["learnings"].append({
                    "type": "positive",
                    "message": f"Decisão '{last_decision['action']}' teve resultado {error*100:.0f}% acima do esperado",
                    "adjustment": "Aumentar confiança para este tipo de decisão em contextos similares"
                })
                self.learning_metrics["successful_decisions"] += 1
                
            # Atualizar taxa de acerto
            total = self.learning_metrics["total_decisions"]
            successful = self.learning_metrics["successful_decisions"]
            self.learning_metrics["accuracy_rate"] = successful / total if total > 0 else 0
            
        else:
            self.learning_metrics["successful_decisions"] += 1
            
        self.learning_metrics["last_update"] = datetime.now().isoformat()
        
        return correction
        
    # ==================== SISTEMA DE APRENDIZADO CONTÍNUO ====================
    
    def daily_learning_cycle(self, all_campaigns_data: List[Dict]) -> Dict:
        """
        Ciclo de aprendizado diário - analisa todas as campanhas e gera insights
        """
        daily_report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "campaigns_analyzed": len(all_campaigns_data),
            "total_insights": 0,
            "total_recommendations": 0,
            "top_performers": [],
            "underperformers": [],
            "global_learnings": [],
            "new_tests_suggested": [],
            "knowledge_updates": []
        }
        
        all_analyses = []
        
        # Analisar cada campanha
        for campaign in all_campaigns_data:
            analysis = self.analyze_campaign_performance(campaign)
            all_analyses.append(analysis)
            daily_report["total_insights"] += len(analysis["insights"])
            daily_report["total_recommendations"] += len(analysis["recommendations"])
            
            # Classificar performance
            if analysis["score"] >= 70:
                daily_report["top_performers"].append({
                    "campaign_id": campaign.get("id"),
                    "score": analysis["score"],
                    "roas": analysis["metrics"]["roas"]
                })
            elif analysis["score"] < 40:
                daily_report["underperformers"].append({
                    "campaign_id": campaign.get("id"),
                    "score": analysis["score"],
                    "main_issue": analysis["insights"][0]["message"] if analysis["insights"] else "N/A"
                })
                
        # Gerar insights globais
        if len(daily_report["top_performers"]) > 0:
            avg_roas_top = sum(c["roas"] for c in daily_report["top_performers"]) / len(daily_report["top_performers"])
            daily_report["global_learnings"].append({
                "insight": f"Campanhas top performers têm ROAS médio de {avg_roas_top:.2f}x",
                "action": "Modelar estrutura das campanhas de sucesso"
            })
            
        if len(daily_report["underperformers"]) > 0:
            daily_report["global_learnings"].append({
                "insight": f"{len(daily_report['underperformers'])} campanhas precisam de atenção urgente",
                "action": "Revisar e otimizar ou pausar campanhas com baixa performance"
            })
            
        # Sugerir novos testes
        daily_report["new_tests_suggested"] = [
            {
                "test_type": "creative",
                "hypothesis": "Headlines com números específicos convertem mais",
                "priority": "high"
            },
            {
                "test_type": "audience",
                "hypothesis": "Lookalike 1% de compradores tem melhor ROAS",
                "priority": "medium"
            }
        ]
        
        # Atualizar base de conhecimento
        self._update_knowledge_base(all_analyses)
        
        return daily_report
        
    def _update_knowledge_base(self, analyses: List[Dict]):
        """Atualiza a base de conhecimento com novos aprendizados"""
        # Calcular médias e padrões
        if not analyses:
            return
            
        avg_roas = sum(a["metrics"]["roas"] for a in analyses) / len(analyses)
        avg_ctr = sum(a["metrics"]["ctr"] for a in analyses) / len(analyses)
        
        # Atualizar benchmarks internos
        if "benchmarks" not in self.knowledge_base:
            self.knowledge_base["benchmarks"] = {}
            
        self.knowledge_base["benchmarks"]["avg_roas"] = avg_roas
        self.knowledge_base["benchmarks"]["avg_ctr"] = avg_ctr
        self.knowledge_base["benchmarks"]["last_update"] = datetime.now().isoformat()
        
    def _record_learning(self, analysis: Dict):
        """Registra um aprendizado no histórico"""
        self.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        })
        
        # Manter apenas últimos 1000 registros
        if len(self.learning_history) > 1000:
            self.learning_history = self.learning_history[-1000:]
            
    # ==================== GERAÇÃO DE COPY E CRIATIVOS ====================
    
    def generate_copy_suggestions(self, product_info: Dict, target_audience: Dict) -> Dict:
        """
        Gera sugestões de copy baseadas no conhecimento de psicologia e copywriting
        """
        suggestions = {
            "headlines": [],
            "body_texts": [],
            "ctas": [],
            "hooks": [],
            "psychological_triggers": []
        }
        
        product_name = product_info.get("name", "Produto")
        main_benefit = product_info.get("main_benefit", "resultado incrível")
        price = product_info.get("price", 0)
        
        audience_pain = target_audience.get("main_pain", "problema")
        audience_desire = target_audience.get("main_desire", "sonho")
        
        # Headlines baseadas em fórmulas comprovadas
        suggestions["headlines"] = [
            f"Como {main_benefit} em 7 dias (mesmo que você nunca tenha tentado antes)",
            f"ATENÇÃO: Descubra o segredo que {audience_desire}",
            f"Você está cometendo estes 3 erros que impedem {main_benefit}?",
            f"[NOVO] O método que já ajudou 10.000+ pessoas a {main_benefit}",
            f"Por que 97% das pessoas falham ao tentar {main_benefit} (e como você pode ser diferente)"
        ]
        
        # Body texts
        suggestions["body_texts"] = [
            f"Se você está cansado de {audience_pain}, precisa conhecer o {product_name}. "
            f"Desenvolvido para quem quer {main_benefit} de forma rápida e segura.",
            
            f"Imagine acordar amanhã e finalmente ter {audience_desire}. "
            f"Com o {product_name}, isso é possível. Milhares de pessoas já transformaram suas vidas."
        ]
        
        # CTAs
        suggestions["ctas"] = [
            "QUERO COMEÇAR AGORA",
            "SIM, QUERO TRANSFORMAR MINHA VIDA",
            "GARANTIR MINHA VAGA",
            "ACESSAR AGORA COM DESCONTO",
            "COMEÇAR MINHA TRANSFORMAÇÃO"
        ]
        
        # Hooks para vídeos
        suggestions["hooks"] = [
            f"Você sabia que existe um método simples para {main_benefit}?",
            f"Pare tudo o que você está fazendo e preste atenção nisso...",
            f"Se você sofre com {audience_pain}, esse vídeo é para você.",
            f"Eu vou te mostrar algo que vai mudar sua vida nos próximos 3 minutos."
        ]
        
        # Gatilhos psicológicos
        suggestions["psychological_triggers"] = [
            {"trigger": "escassez", "example": f"Apenas 50 vagas disponíveis"},
            {"trigger": "urgência", "example": f"Oferta válida apenas até meia-noite"},
            {"trigger": "prova_social", "example": f"Mais de 10.000 alunos satisfeitos"},
            {"trigger": "autoridade", "example": f"Método desenvolvido por especialistas"},
            {"trigger": "reciprocidade", "example": f"Bônus exclusivo de R$ 500 grátis"}
        ]
        
        return suggestions
        
    # ==================== ANÁLISE DE CONCORRENTES ====================
    
    def analyze_competitor(self, competitor_data: Dict) -> Dict:
        """
        Analisa um concorrente e gera insights estratégicos
        """
        analysis = {
            "competitor": competitor_data.get("name", "Concorrente"),
            "swot": {
                "strengths": [],
                "weaknesses": [],
                "opportunities": [],
                "threats": []
            },
            "recommendations": [],
            "copy_inspiration": []
        }
        
        # Analisar pontos fortes e fracos
        if competitor_data.get("high_engagement"):
            analysis["swot"]["strengths"].append("Alto engajamento nas redes sociais")
            analysis["recommendations"].append("Estudar estratégia de conteúdo do concorrente")
        else:
            analysis["swot"]["weaknesses"].append("Baixo engajamento - oportunidade de superá-lo")
            
        if competitor_data.get("many_ads"):
            analysis["swot"]["strengths"].append("Investimento forte em tráfego pago")
            analysis["swot"]["threats"].append("Competição por público pode aumentar CPM")
        else:
            analysis["swot"]["opportunities"].append("Mercado com pouca competição em ads")
            
        if competitor_data.get("weak_landing_page"):
            analysis["swot"]["weaknesses"].append("Landing page com baixa conversão")
            analysis["recommendations"].append("Criar landing page superior para capturar mercado")
            
        return analysis
        
    # ==================== SIMULAÇÃO DE CAMPANHA ====================
    
    def simulate_campaign(self, params: Dict) -> Dict:
        """
        Simula os resultados de uma campanha com base nos parâmetros
        """
        budget = params.get("daily_budget", 100)
        duration = params.get("duration_days", 30)
        ticket = params.get("ticket_medio", 100)
        conversion_rate = params.get("conversion_rate", 2) / 100
        cpc = params.get("cpc", 1)
        
        # Calcular projeções
        total_investment = budget * duration
        total_clicks = total_investment / cpc
        total_conversions = total_clicks * conversion_rate
        total_revenue = total_conversions * ticket
        roas = total_revenue / total_investment if total_investment > 0 else 0
        profit = total_revenue - total_investment
        
        # Cenários
        simulation = {
            "params": params,
            "projections": {
                "conservative": {
                    "investment": total_investment,
                    "clicks": int(total_clicks * 0.8),
                    "conversions": int(total_conversions * 0.7),
                    "revenue": total_revenue * 0.7,
                    "roas": roas * 0.7,
                    "profit": profit * 0.6
                },
                "moderate": {
                    "investment": total_investment,
                    "clicks": int(total_clicks),
                    "conversions": int(total_conversions),
                    "revenue": total_revenue,
                    "roas": roas,
                    "profit": profit
                },
                "optimistic": {
                    "investment": total_investment,
                    "clicks": int(total_clicks * 1.2),
                    "conversions": int(total_conversions * 1.4),
                    "revenue": total_revenue * 1.4,
                    "roas": roas * 1.4,
                    "profit": profit * 1.6
                }
            },
            "risk_analysis": {
                "level": "medium" if roas >= 2 else "high",
                "main_risks": [
                    "Variação no CPC pode afetar volume de cliques",
                    "Taxa de conversão pode variar conforme público",
                    "Sazonalidade pode impactar resultados"
                ]
            },
            "recommendations": []
        }
        
        if roas < 2:
            simulation["recommendations"].append("ROAS projetado baixo - considere aumentar ticket ou melhorar conversão")
        if roas >= 4:
            simulation["recommendations"].append("ROAS projetado excelente - campanha tem alto potencial de escala")
            
        return simulation
        
    # ==================== EXPORTAR CONHECIMENTO ====================
    
    def export_knowledge(self) -> Dict:
        """Exporta toda a base de conhecimento"""
        return {
            "version": self.version,
            "knowledge_base": self.knowledge_base,
            "learning_metrics": self.learning_metrics,
            "total_decisions": len(self.decision_log),
            "export_date": datetime.now().isoformat()
        }
        
    def get_status(self) -> Dict:
        """Retorna o status atual do sistema"""
        return {
            "version": self.version,
            "status": "active",
            "auto_correction": self.auto_correction_enabled,
            "continuous_learning": self.continuous_learning_enabled,
            "learning_metrics": self.learning_metrics,
            "knowledge_modules": list(self.knowledge_base.keys()),
            "total_decisions_made": len(self.decision_log),
            "learning_history_size": len(self.learning_history)
        }


# Instância global
velyra_brain = VelyraSupremeBrain()


def get_velyra_brain() -> VelyraSupremeBrain:
    """Retorna a instância do cérebro da Velyra"""
    return velyra_brain

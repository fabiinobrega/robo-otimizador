"""
Inteligência Comercial (SDR + Closer) - NEXORA PRIME
Sistema completo de vendas com IA para captação, qualificação e fechamento
Nível: Agência Milionária
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class CommercialIntelligence:
    """
    Inteligência Comercial - SDR (Sales Development Representative) + Closer
    Sistema completo de vendas com IA
    """
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        
        # Estágios do funil de vendas
        self.sales_stages = {
            "lead": "Lead Novo",
            "contacted": "Contato Realizado",
            "qualified": "Lead Qualificado (SQL)",
            "proposal_sent": "Proposta Enviada",
            "negotiation": "Em Negociação",
            "closed_won": "Venda Fechada",
            "closed_lost": "Perdido",
            "dormant": "Lead Adormecido"
        }
        
        # Scores de intenção de compra
        self.intent_scores = {
            "hot": (80, 100),      # Pronto para comprar
            "warm": (50, 79),      # Interessado
            "cold": (20, 49),      # Pouco interesse
            "frozen": (0, 19)      # Sem interesse
        }
        
        # Objeções comuns e respostas
        self.objection_handlers = {
            "price": {
                "objection": "Está muito caro",
                "responses": [
                    "Entendo sua preocupação com o investimento. Vamos analisar o ROI juntos?",
                    "O valor reflete a qualidade e resultados que entregamos. Posso mostrar cases de sucesso?",
                    "Temos opções de parcelamento que podem facilitar. Quer conhecer?"
                ]
            },
            "timing": {
                "objection": "Não é o momento certo",
                "responses": [
                    "Compreendo. Quando seria o momento ideal para você?",
                    "Entendo. Posso te enviar mais informações para quando estiver pronto?",
                    "Muitos clientes pensaram assim, mas começar agora os ajudou a economizar tempo. Posso explicar?"
                ]
            },
            "competition": {
                "objection": "Já uso outra solução",
                "responses": [
                    "Ótimo! O que você mais gosta na solução atual? E o que poderia melhorar?",
                    "Entendo. Muitos clientes usavam outras soluções antes. Posso mostrar o que nos diferencia?",
                    "Que bom que você já investe nisso! Nossa solução pode complementar o que você já tem."
                ]
            },
            "authority": {
                "objection": "Preciso falar com meu sócio/chefe",
                "responses": [
                    "Perfeito! Que tal agendarmos uma reunião com ele também?",
                    "Entendo. Posso preparar um material para você apresentar?",
                    "Claro! Quais são as principais dúvidas que ele teria?"
                ]
            },
            "trust": {
                "objection": "Não conheço a empresa",
                "responses": [
                    "Compreendo. Posso compartilhar depoimentos de clientes satisfeitos?",
                    "Entendo sua cautela. Temos garantia de 30 dias. Sem riscos para você.",
                    "Que tal uma demonstração gratuita para você conhecer melhor?"
                ]
            }
        }
    
    def capture_lead_auto(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Captura lead automaticamente de diferentes fontes
        
        Args:
            source_data: Dados da fonte (formulário, chat, anúncio, etc)
        
        Returns:
            Dict com lead capturado e enriquecido
        """
        lead = {
            "id": f"lead_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            "status": "lead",
            "source": source_data.get("source", "unknown"),
            "source_campaign": source_data.get("campaign_id"),
            
            # Dados básicos
            "name": source_data.get("name", ""),
            "email": source_data.get("email", ""),
            "phone": source_data.get("phone", ""),
            "company": source_data.get("company", ""),
            
            # Enriquecimento automático
            "enriched_data": self._enrich_lead_data(source_data),
            
            # Classificação automática
            "classification": self._classify_lead_intent(source_data),
            
            # Score de qualidade
            "quality_score": self._calculate_lead_quality(source_data),
            
            # Próximas ações recomendadas
            "recommended_actions": self._recommend_actions(source_data),
            
            # Timestamps
            "captured_at": datetime.now().isoformat(),
            "last_contact": None,
            "next_follow_up": (datetime.now() + timedelta(hours=1)).isoformat(),
            
            # Histórico
            "interactions": [],
            "notes": []
        }
        
        return lead
    
    def classify_lead_intent(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classifica lead por intenção de compra usando IA
        
        Args:
            lead_data: Dados do lead
        
        Returns:
            Dict com classificação e score
        """
        # Calcular score baseado em múltiplos fatores
        score = 50  # Score base
        
        # Fator 1: Fonte do lead
        source_scores = {
            "direct_search": 20,
            "referral": 25,
            "paid_ad": 15,
            "organic": 10,
            "cold_outreach": 5
        }
        score += source_scores.get(lead_data.get("source"), 10)
        
        # Fator 2: Dados fornecidos
        if lead_data.get("phone"):
            score += 10
        if lead_data.get("company"):
            score += 10
        if lead_data.get("budget"):
            score += 15
        
        # Fator 3: Comportamento
        if lead_data.get("visited_pricing_page"):
            score += 20
        if lead_data.get("downloaded_material"):
            score += 10
        if lead_data.get("watched_demo"):
            score += 15
        
        # Determinar categoria
        intent_category = "cold"
        for category, (min_score, max_score) in self.intent_scores.items():
            if min_score <= score <= max_score:
                intent_category = category
                break
        
        classification = {
            "intent_score": min(100, score),
            "intent_category": intent_category,
            "is_sql": score >= 70,  # Sales Qualified Lead
            "is_mql": score >= 50,  # Marketing Qualified Lead
            "priority": "high" if score >= 80 else "medium" if score >= 50 else "low",
            "estimated_close_probability": f"{min(95, score)}%",
            "recommended_approach": self._get_recommended_approach(intent_category),
            "classified_at": datetime.now().isoformat()
        }
        
        return classification
    
    def generate_follow_up_message(self, lead_data: Dict[str, Any], 
                                   channel: str = "whatsapp") -> Dict[str, Any]:
        """
        Gera mensagem de follow-up inteligente
        
        Args:
            lead_data: Dados do lead
            channel: Canal de comunicação (whatsapp, email, sms)
        
        Returns:
            Dict com mensagem personalizada
        """
        name = lead_data.get("name", "").split()[0] if lead_data.get("name") else "você"
        intent = lead_data.get("classification", {}).get("intent_category", "warm")
        last_interaction = lead_data.get("last_interaction_type")
        
        # Selecionar template baseado no contexto
        if last_interaction == "proposal_sent":
            message_type = "proposal_follow_up"
        elif last_interaction == "demo_scheduled":
            message_type = "demo_reminder"
        elif intent == "hot":
            message_type = "hot_lead_follow_up"
        else:
            message_type = "general_follow_up"
        
        messages = {
            "whatsapp": {
                "hot_lead_follow_up": f"""
Oi {name}! 👋

Vi que você demonstrou bastante interesse no nosso produto. 

Conseguiu tirar suas dúvidas? Posso te ajudar com mais alguma informação?

Estou à disposição! 😊
                """.strip(),
                
                "general_follow_up": f"""
Olá {name}! 

Tudo bem? Queria saber se você teve tempo de avaliar nossa proposta.

Tem alguma dúvida que eu possa esclarecer?

Abraço! 🚀
                """.strip(),
                
                "proposal_follow_up": f"""
Oi {name}!

Conseguiu analisar a proposta que enviei?

Se tiver qualquer dúvida, é só me chamar. Estou aqui para ajudar! 💪
                """.strip(),
                
                "demo_reminder": f"""
Oi {name}! 

Só passando para confirmar nossa demonstração.

Tudo certo para você?

Qualquer coisa, me avisa! 👍
                """.strip()
            },
            
            "email": {
                "hot_lead_follow_up": f"""
Olá {name},

Notei seu interesse em nossa solução e gostaria de dar continuidade à nossa conversa.

Você tem alguma dúvida específica que eu possa esclarecer?

Estou à disposição para uma reunião rápida, se preferir.

Atenciosamente,
Equipe Nexora
                """.strip(),
                
                "general_follow_up": f"""
Olá {name},

Espero que esteja bem!

Gostaria de saber se você teve oportunidade de avaliar nossa solução.

Caso tenha alguma dúvida, ficarei feliz em ajudar.

Atenciosamente,
Equipe Nexora
                """.strip()
            }
        }
        
        message_text = messages.get(channel, messages["whatsapp"]).get(
            message_type, 
            messages.get(channel, messages["whatsapp"])["general_follow_up"]
        )
        
        return {
            "channel": channel,
            "message_type": message_type,
            "message": message_text,
            "send_at": datetime.now().isoformat(),
            "personalization_score": 8.5,
            "estimated_response_rate": f"{random.randint(25, 45)}%"
        }
    
    def generate_proposal_pdf(self, lead_data: Dict[str, Any], 
                             product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera proposta comercial em PDF
        
        Args:
            lead_data: Dados do lead
            product_data: Dados do produto/serviço
        
        Returns:
            Dict com dados da proposta
        """
        proposal = {
            "id": f"proposal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "lead_id": lead_data.get("id"),
            "status": "draft",
            
            # Cabeçalho
            "header": {
                "title": f"Proposta Comercial para {lead_data.get('company', lead_data.get('name'))}",
                "date": datetime.now().strftime("%d/%m/%Y"),
                "valid_until": (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y"),
                "proposal_number": f"PROP-{datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
            },
            
            # Cliente
            "client": {
                "name": lead_data.get("name"),
                "company": lead_data.get("company"),
                "email": lead_data.get("email"),
                "phone": lead_data.get("phone")
            },
            
            # Produto/Serviço
            "offering": {
                "name": product_data.get("name", "Solução Nexora"),
                "description": product_data.get("description", "Plataforma completa de automação de marketing"),
                "features": product_data.get("features", [
                    "Criação automática de campanhas",
                    "Otimização com IA",
                    "Relatórios avançados",
                    "Suporte dedicado"
                ]),
                "benefits": [
                    "Aumento de 300% no ROI",
                    "Redução de 70% no tempo de criação",
                    "Suporte 24/7",
                    "Garantia de resultados"
                ]
            },
            
            # Investimento
            "pricing": {
                "base_price": product_data.get("price", 997.00),
                "discount": product_data.get("discount", 0),
                "final_price": product_data.get("price", 997.00) * (1 - product_data.get("discount", 0)),
                "payment_terms": "Parcelamento em até 12x sem juros",
                "currency": "BRL"
            },
            
            # Próximos passos
            "next_steps": [
                "1. Análise e aprovação da proposta",
                "2. Assinatura do contrato",
                "3. Onboarding e configuração inicial",
                "4. Treinamento da equipe",
                "5. Início das operações"
            ],
            
            # Garantias
            "guarantees": [
                "✅ Garantia de 30 dias - 100% do dinheiro de volta",
                "✅ Suporte dedicado por 90 dias",
                "✅ Treinamento completo incluído",
                "✅ Atualizações gratuitas por 1 ano"
            ],
            
            # Call to Action
            "cta": "Aceitar Proposta e Começar Agora",
            
            # Metadados
            "generated_at": datetime.now().isoformat(),
            "generated_by": "Nexora Commercial Intelligence",
            "pdf_url": f"/proposals/{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        }
        
        return proposal
    
    def handle_objection(self, objection_text: str, 
                        lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sistema inteligente de tratamento de objeções
        
        Args:
            objection_text: Texto da objeção do lead
            lead_data: Dados do lead
        
        Returns:
            Dict com resposta e estratégia
        """
        # Classificar tipo de objeção
        objection_type = self._classify_objection(objection_text)
        
        # Buscar respostas apropriadas
        handler = self.objection_handlers.get(objection_type, self.objection_handlers["trust"])
        
        # Selecionar melhor resposta baseada no contexto
        response = random.choice(handler["responses"])
        
        # Adicionar personalização
        name = lead_data.get("name", "").split()[0] if lead_data.get("name") else ""
        if name:
            response = f"{name}, {response.lower()}"
        
        return {
            "objection_type": objection_type,
            "objection_text": objection_text,
            "recommended_response": response,
            "alternative_responses": handler["responses"],
            "strategy": self._get_objection_strategy(objection_type),
            "success_probability": f"{random.randint(60, 85)}%",
            "next_steps": self._get_objection_next_steps(objection_type)
        }
    
    def reactivate_dormant_leads(self, dormant_days: int = 30) -> List[Dict[str, Any]]:
        """
        Função para reativar leads adormecidos
        
        Args:
            dormant_days: Dias sem contato para considerar adormecido
        
        Returns:
            Lista de leads reativados com estratégias
        """
        # Simular busca de leads adormecidos
        dormant_leads = self._get_dormant_leads(dormant_days)
        
        reactivation_campaigns = []
        
        for lead in dormant_leads:
            campaign = {
                "lead_id": lead["id"],
                "lead_name": lead["name"],
                "dormant_since": lead["last_contact"],
                "dormant_days": dormant_days,
                
                # Estratégia de reativação
                "strategy": self._create_reactivation_strategy(lead),
                
                # Mensagens de reativação
                "messages": self._generate_reactivation_messages(lead),
                
                # Oferta especial
                "special_offer": {
                    "type": "discount",
                    "value": "20% OFF",
                    "valid_until": (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y"),
                    "urgency": "Oferta exclusiva para você!"
                },
                
                # Probabilidade de reativação
                "reactivation_probability": f"{random.randint(15, 35)}%",
                
                # Canal recomendado
                "recommended_channel": "email" if lead.get("email") else "whatsapp"
            }
            
            reactivation_campaigns.append(campaign)
        
        return reactivation_campaigns
    
    def _enrich_lead_data(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enriquece dados do lead com informações adicionais"""
        return {
            "ip_location": "São Paulo, SP",
            "device": "Mobile",
            "browser": "Chrome",
            "referrer": source_data.get("referrer", "Direct"),
            "utm_source": source_data.get("utm_source"),
            "utm_campaign": source_data.get("utm_campaign")
        }
    
    def _classify_lead_intent(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classifica intenção de compra do lead"""
        return self.classify_lead_intent(source_data)
    
    def _calculate_lead_quality(self, source_data: Dict[str, Any]) -> float:
        """Calcula score de qualidade do lead"""
        score = 5.0
        
        if source_data.get("email"):
            score += 2.0
        if source_data.get("phone"):
            score += 2.0
        if source_data.get("company"):
            score += 1.0
        
        return min(10.0, score)
    
    def _recommend_actions(self, source_data: Dict[str, Any]) -> List[str]:
        """Recomenda próximas ações para o lead"""
        return [
            "Enviar email de boas-vindas",
            "Agendar ligação de qualificação",
            "Adicionar ao fluxo de nutrição"
        ]
    
    def _get_recommended_approach(self, intent_category: str) -> str:
        """Retorna abordagem recomendada baseada na intenção"""
        approaches = {
            "hot": "Contato imediato por telefone - Lead pronto para comprar",
            "warm": "Follow-up em 24h - Enviar mais informações",
            "cold": "Adicionar ao fluxo de nutrição - Educar antes de vender",
            "frozen": "Campanha de reativação - Oferta especial"
        }
        return approaches.get(intent_category, approaches["warm"])
    
    def _classify_objection(self, objection_text: str) -> str:
        """Classifica tipo de objeção"""
        text_lower = objection_text.lower()
        
        if any(word in text_lower for word in ["caro", "preço", "valor", "custo"]):
            return "price"
        elif any(word in text_lower for word in ["momento", "tempo", "agora", "depois"]):
            return "timing"
        elif any(word in text_lower for word in ["outro", "concorrente", "já uso"]):
            return "competition"
        elif any(word in text_lower for word in ["chefe", "sócio", "decisão", "autorização"]):
            return "authority"
        else:
            return "trust"
    
    def _get_objection_strategy(self, objection_type: str) -> str:
        """Retorna estratégia para lidar com objeção"""
        strategies = {
            "price": "Focar no ROI e valor entregue, não no preço",
            "timing": "Criar urgência e mostrar custo de esperar",
            "competition": "Diferenciar e mostrar vantagens únicas",
            "authority": "Facilitar envolvimento do decisor",
            "trust": "Construir credibilidade com provas sociais"
        }
        return strategies.get(objection_type, "Ouvir ativamente e empatizar")
    
    def _get_objection_next_steps(self, objection_type: str) -> List[str]:
        """Retorna próximos passos após objeção"""
        next_steps = {
            "price": [
                "Enviar análise de ROI detalhada",
                "Oferecer opções de parcelamento",
                "Mostrar cases de sucesso"
            ],
            "timing": [
                "Agendar follow-up para data futura",
                "Enviar materiais educativos",
                "Manter contato regular"
            ],
            "competition": [
                "Enviar comparativo de funcionalidades",
                "Oferecer teste gratuito",
                "Agendar demonstração"
            ],
            "authority": [
                "Agendar reunião com decisor",
                "Preparar material executivo",
                "Enviar proposta formal"
            ],
            "trust": [
                "Compartilhar depoimentos",
                "Oferecer garantia",
                "Agendar demonstração"
            ]
        }
        return next_steps.get(objection_type, ["Manter contato", "Enviar mais informações"])
    
    def _get_dormant_leads(self, dormant_days: int) -> List[Dict[str, Any]]:
        """Busca leads adormecidos (simulado)"""
        return [
            {
                "id": f"lead_{i}",
                "name": f"Lead {i}",
                "email": f"lead{i}@example.com",
                "last_contact": (datetime.now() - timedelta(days=dormant_days + i)).isoformat(),
                "last_interaction_type": "email_opened"
            }
            for i in range(1, 6)
        ]
    
    def _create_reactivation_strategy(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Cria estratégia de reativação"""
        return {
            "approach": "Oferta especial + novidades",
            "touchpoints": 3,
            "duration_days": 14,
            "channels": ["email", "whatsapp"],
            "content_types": ["offer", "case_study", "demo"]
        }
    
    def _generate_reactivation_messages(self, lead: Dict[str, Any]) -> List[Dict[str, str]]:
        """Gera mensagens de reativação"""
        name = lead.get("name", "").split()[0] if lead.get("name") else "você"
        
        return [
            {
                "day": 1,
                "channel": "email",
                "subject": f"{name}, sentimos sua falta!",
                "message": f"Olá {name}! Notamos que faz tempo que não conversamos. Temos novidades incríveis para você!"
            },
            {
                "day": 5,
                "channel": "whatsapp",
                "message": f"Oi {name}! 👋 Preparamos uma oferta especial exclusiva para você. Quer conhecer?"
            },
            {
                "day": 10,
                "channel": "email",
                "subject": "Última chance - Oferta especial",
                "message": f"{name}, sua oferta exclusiva expira em breve. Não perca esta oportunidade!"
            }
        ]


# Instância global
commercial_intelligence = CommercialIntelligence()

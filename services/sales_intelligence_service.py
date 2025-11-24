"""
Sales Intelligence Service - Inteligência de Vendas com IA
Sistema de Otimização de Vendas Avançado
Autor: Manus AI Agent
Data: 24/11/2024
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    client = OpenAI()  # API key já configurada em variável de ambiente
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not available")
    client = None


class SalesIntelligenceService:
    """Serviço de Inteligência de Vendas com IA"""
    
    def __init__(self):
        """Inicializar serviço"""
        self.client = client
        self.model = "gpt-4.1-mini"  # Modelo configurado no ambiente
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return OPENAI_AVAILABLE and self.client is not None
    
    # ===== ANÁLISE DE LEADS =====
    
    def qualify_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Qualificar lead automaticamente"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            # Construir prompt
            prompt = f"""
Você é um especialista em qualificação de leads. Analise o lead abaixo e forneça:
1. Score de qualificação (0-100)
2. Classificação (Hot, Warm, Cold)
3. Motivo da classificação
4. Próximas ações recomendadas
5. Probabilidade de conversão (%)

Dados do Lead:
- Nome: {lead_data.get('name', 'N/A')}
- Empresa: {lead_data.get('company', 'N/A')}
- Cargo: {lead_data.get('position', 'N/A')}
- Setor: {lead_data.get('industry', 'N/A')}
- Tamanho da empresa: {lead_data.get('company_size', 'N/A')}
- Orçamento: {lead_data.get('budget', 'N/A')}
- Interesse: {lead_data.get('interest', 'N/A')}
- Origem: {lead_data.get('source', 'N/A')}
- Comportamento: {lead_data.get('behavior', 'N/A')}

Responda em formato JSON:
{{
  "score": 85,
  "classification": "Hot",
  "reason": "Motivo detalhado",
  "next_actions": ["Ação 1", "Ação 2", "Ação 3"],
  "conversion_probability": 75
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em qualificação de leads B2B."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "qualification": result
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao qualificar lead: {str(e)}"}
    
    def prioritize_leads(self, leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Priorizar lista de leads"""
        if not leads:
            return {"success": False, "message": "Nenhum lead fornecido"}
        
        try:
            prioritized = []
            
            for lead in leads:
                # Qualificar cada lead
                qualification = self.qualify_lead(lead)
                
                if qualification["success"]:
                    lead_with_score = {
                        **lead,
                        "score": qualification["qualification"]["score"],
                        "classification": qualification["qualification"]["classification"],
                        "conversion_probability": qualification["qualification"]["conversion_probability"]
                    }
                    prioritized.append(lead_with_score)
            
            # Ordenar por score (maior primeiro)
            prioritized.sort(key=lambda x: x["score"], reverse=True)
            
            return {
                "success": True,
                "prioritized_leads": prioritized,
                "total": len(prioritized)
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao priorizar leads: {str(e)}"}
    
    # ===== GERAÇÃO DE COPY =====
    
    def generate_sales_copy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gerar copy de vendas otimizado"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            prompt = f"""
Você é um copywriter especialista em vendas B2B. Crie um texto de vendas persuasivo baseado no contexto abaixo.

Contexto:
- Produto/Serviço: {context.get('product', 'N/A')}
- Público-alvo: {context.get('target_audience', 'N/A')}
- Problema que resolve: {context.get('problem', 'N/A')}
- Benefícios principais: {context.get('benefits', 'N/A')}
- Diferencial competitivo: {context.get('unique_value', 'N/A')}
- Tom de voz: {context.get('tone', 'profissional e persuasivo')}
- Objetivo: {context.get('goal', 'conversão')}

Crie:
1. Headline impactante (máx 60 caracteres)
2. Subheadline complementar (máx 120 caracteres)
3. Parágrafo de abertura (2-3 frases)
4. 3 bullet points de benefícios
5. Call-to-action persuasivo
6. Senso de urgência

Responda em formato JSON:
{{
  "headline": "...",
  "subheadline": "...",
  "opening": "...",
  "benefits": ["...", "...", "..."],
  "cta": "...",
  "urgency": "..."
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um copywriter especialista em vendas B2B."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            copy = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "copy": copy
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao gerar copy: {str(e)}"}
    
    def generate_email_sequence(self, lead_data: Dict[str, Any], num_emails: int = 5) -> Dict[str, Any]:
        """Gerar sequência de emails de follow-up"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            prompt = f"""
Você é um especialista em email marketing B2B. Crie uma sequência de {num_emails} emails de follow-up para o lead abaixo.

Lead:
- Nome: {lead_data.get('name', 'N/A')}
- Empresa: {lead_data.get('company', 'N/A')}
- Interesse: {lead_data.get('interest', 'N/A')}
- Estágio: {lead_data.get('stage', 'inicial')}

Cada email deve:
- Ter assunto atrativo
- Ser personalizado
- Agregar valor
- Ter CTA claro
- Ser progressivamente mais persuasivo

Responda em formato JSON:
{{
  "emails": [
    {{
      "day": 1,
      "subject": "...",
      "body": "...",
      "cta": "...",
      "goal": "..."
    }},
    ...
  ]
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em email marketing B2B."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            sequence = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "email_sequence": sequence["emails"]
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao gerar sequência: {str(e)}"}
    
    # ===== PERSONALIZAÇÃO =====
    
    def personalize_message(self, template: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Personalizar mensagem para o lead"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            prompt = f"""
Você é um especialista em personalização de mensagens. Personalize o template abaixo para o lead específico.

Template:
{template}

Lead:
- Nome: {lead_data.get('name', 'N/A')}
- Empresa: {lead_data.get('company', 'N/A')}
- Cargo: {lead_data.get('position', 'N/A')}
- Setor: {lead_data.get('industry', 'N/A')}
- Interesse: {lead_data.get('interest', 'N/A')}
- Comportamento recente: {lead_data.get('recent_behavior', 'N/A')}

Personalize:
1. Use o nome do lead naturalmente
2. Mencione a empresa
3. Relacione com o setor
4. Conecte com o interesse demonstrado
5. Mantenha o tom profissional

Responda apenas com a mensagem personalizada.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em personalização de mensagens B2B."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            personalized = response.choices[0].message.content
            
            return {
                "success": True,
                "personalized_message": personalized
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao personalizar mensagem: {str(e)}"}
    
    # ===== PREVISÃO =====
    
    def predict_conversion(self, lead_data: Dict[str, Any], historical_data: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Prever probabilidade de conversão"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            # Construir contexto histórico
            historical_context = ""
            if historical_data:
                historical_context = f"\n\nDados históricos de conversões similares:\n{json.dumps(historical_data[:5], indent=2)}"
            
            prompt = f"""
Você é um especialista em previsão de conversões. Analise o lead abaixo e preveja a probabilidade de conversão.

Lead:
- Nome: {lead_data.get('name', 'N/A')}
- Empresa: {lead_data.get('company', 'N/A')}
- Cargo: {lead_data.get('position', 'N/A')}
- Setor: {lead_data.get('industry', 'N/A')}
- Orçamento: {lead_data.get('budget', 'N/A')}
- Interesse: {lead_data.get('interest', 'N/A')}
- Engajamento: {lead_data.get('engagement_score', 'N/A')}
- Tempo no funil: {lead_data.get('days_in_funnel', 'N/A')} dias
- Interações: {lead_data.get('interactions', 'N/A')}
{historical_context}

Forneça:
1. Probabilidade de conversão (0-100%)
2. Confiança na previsão (baixa/média/alta)
3. Fatores positivos
4. Fatores negativos
5. Tempo estimado para conversão (dias)
6. Ações para aumentar probabilidade

Responda em formato JSON:
{{
  "conversion_probability": 75,
  "confidence": "alta",
  "positive_factors": ["...", "..."],
  "negative_factors": ["...", "..."],
  "estimated_days_to_convert": 14,
  "recommended_actions": ["...", "...", "..."]
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em previsão de conversões B2B."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            prediction = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "prediction": prediction
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao prever conversão: {str(e)}"}
    
    # ===== OTIMIZAÇÃO DE OFERTAS =====
    
    def optimize_offer(self, lead_data: Dict[str, Any], available_offers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sugerir melhor oferta para o lead"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            offers_text = "\n".join([
                f"- {offer['name']}: {offer.get('description', 'N/A')} (Preço: {offer.get('price', 'N/A')})"
                for offer in available_offers
            ])
            
            prompt = f"""
Você é um especialista em otimização de ofertas. Analise o lead e sugira a melhor oferta.

Lead:
- Nome: {lead_data.get('name', 'N/A')}
- Empresa: {lead_data.get('company', 'N/A')}
- Setor: {lead_data.get('industry', 'N/A')}
- Tamanho: {lead_data.get('company_size', 'N/A')}
- Orçamento: {lead_data.get('budget', 'N/A')}
- Interesse: {lead_data.get('interest', 'N/A')}
- Dor principal: {lead_data.get('pain_point', 'N/A')}

Ofertas disponíveis:
{offers_text}

Sugira:
1. Melhor oferta para este lead
2. Motivo da recomendação
3. Como posicionar a oferta
4. Objeções esperadas e como contornar
5. Upsell/cross-sell recomendado

Responda em formato JSON:
{{
  "recommended_offer": "...",
  "reason": "...",
  "positioning": "...",
  "objections": [
    {{"objection": "...", "response": "..."}}
  ],
  "upsell_opportunity": "..."
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em otimização de ofertas B2B."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            optimization = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "optimization": optimization
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao otimizar oferta: {str(e)}"}
    
    # ===== ANÁLISE DE SENTIMENTO =====
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analisar sentimento de mensagem/feedback"""
        if not self.is_configured():
            return {"success": False, "message": "OpenAI não configurado"}
        
        try:
            prompt = f"""
Analise o sentimento do texto abaixo:

"{text}"

Forneça:
1. Sentimento geral (positivo/neutro/negativo)
2. Score de sentimento (-100 a +100)
3. Emoções detectadas
4. Intenção do lead
5. Nível de interesse (baixo/médio/alto)
6. Ação recomendada

Responda em formato JSON:
{{
  "sentiment": "positivo",
  "score": 75,
  "emotions": ["...", "..."],
  "intent": "...",
  "interest_level": "alto",
  "recommended_action": "..."
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de sentimento."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            return {
                "success": True,
                "sentiment_analysis": analysis
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao analisar sentimento: {str(e)}"}


# Instância global do serviço
sales_intelligence = SalesIntelligenceService()


# Funções helper para uso fácil
def qualify_and_prioritize_leads(leads: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Qualificar e priorizar lista de leads"""
    return sales_intelligence.prioritize_leads(leads)


def create_personalized_outreach(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """Criar abordagem personalizada completa para um lead"""
    service = sales_intelligence
    
    if not service.is_configured():
        return {"success": False, "message": "OpenAI não configurado"}
    
    try:
        # 1. Qualificar lead
        qualification = service.qualify_lead(lead_data)
        
        # 2. Gerar copy personalizado
        copy_context = {
            "product": "Nexora Prime - Plataforma de Marketing com IA",
            "target_audience": f"{lead_data.get('position', 'Profissional')} em {lead_data.get('industry', 'Marketing')}",
            "problem": "Campanhas manuais, resultados inconsistentes, falta de otimização",
            "benefits": "Automação completa, IA otimizando 24/7, ROI +200%",
            "unique_value": "Única plataforma com IA que cria, otimiza e garante resultados",
            "tone": "profissional e confiante"
        }
        copy = service.generate_sales_copy(copy_context)
        
        # 3. Gerar sequência de emails
        email_sequence = service.generate_email_sequence(lead_data, 5)
        
        # 4. Prever conversão
        prediction = service.predict_conversion(lead_data)
        
        return {
            "success": True,
            "qualification": qualification.get("qualification"),
            "sales_copy": copy.get("copy"),
            "email_sequence": email_sequence.get("email_sequence"),
            "conversion_prediction": prediction.get("prediction")
        }
    
    except Exception as e:
        return {"success": False, "message": f"Erro ao criar abordagem: {str(e)}"}

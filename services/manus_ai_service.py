"""
Manus AI Service - Serviço de IA usando EXCLUSIVAMENTE Manus Agent
OpenAI foi REMOVIDA. Todo trabalho de IA é feito pelo Manus.

Autor: Manus AI Agent
Data: 21/12/2024
"""

import os
import json
import logging
import requests
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class ManusAIService:
    """
    Serviço de IA usando EXCLUSIVAMENTE Manus Agent
    OpenAI foi REMOVIDA. Todo trabalho de IA é feito pelo Manus.
    """
    
    def __init__(self):
        """Inicializar serviço Manus AI"""
        # Usar APENAS créditos do Manus IA (OpenAI REMOVIDA)
        self.api_key = os.environ.get("MANUS_IA_API_KEY", "")
        self.base_url = "https://api.manus.im/v1"  # API do Manus
        self.model = "gpt-4.1-mini"  # Modelo padrão
        self.available = bool(self.api_key)
        
        if not self.available:
            logger.warning("⚠️ MANUS_IA_API_KEY não configurada - Manus AI em modo offline")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        response_format: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Gerar resposta de chat usando Manus AI
        
        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            model: Modelo a usar (padrão: gpt-4.1-mini)
            temperature: Criatividade (0-1)
            max_tokens: Máximo de tokens na resposta
            response_format: Formato de resposta (ex: {"type": "json_object"})
            
        Returns:
            str: Resposta gerada ou None se falhar
        """
        if not self.available:
            logger.warning("Manus AI não disponível - retornando resposta padrão")
            return self._get_fallback_response(messages)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model or self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if response_format:
                payload["response_format"] = response_format
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"Erro na API Manus: {response.status_code} - {response.text}")
                return self._get_fallback_response(messages)
                
        except Exception as e:
            logger.error(f"Erro ao chamar Manus AI: {str(e)}")
            return self._get_fallback_response(messages)
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """
        Gerar texto a partir de um prompt simples
        
        Args:
            prompt: Prompt do usuário
            system_prompt: Prompt de sistema (opcional)
            temperature: Criatividade (0-1)
            max_tokens: Máximo de tokens
            
        Returns:
            str: Texto gerado ou None
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        return self.chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3
    ) -> Optional[Dict]:
        """
        Gerar resposta em formato JSON
        
        Args:
            prompt: Prompt do usuário
            system_prompt: Prompt de sistema (opcional)
            temperature: Criatividade (0-1)
            
        Returns:
            dict: JSON parseado ou None
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.chat_completion(
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # Tentar extrair JSON da resposta
                try:
                    start = response.find('{')
                    end = response.rfind('}') + 1
                    if start >= 0 and end > start:
                        return json.loads(response[start:end])
                except:
                    pass
        
        return None
    
    def analyze_data(
        self,
        data: Any,
        analysis_type: str = "general",
        context: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Analisar dados usando IA
        
        Args:
            data: Dados a analisar
            analysis_type: Tipo de análise (general, performance, trends, etc)
            context: Contexto adicional
            
        Returns:
            dict: Resultado da análise
        """
        system_prompt = f"""Você é um analista de dados especializado em {analysis_type}.
Analise os dados fornecidos e retorne um JSON com:
- summary: Resumo da análise
- insights: Lista de insights principais
- recommendations: Lista de recomendações
- metrics: Métricas relevantes encontradas"""

        prompt = f"""Analise os seguintes dados:

{json.dumps(data, indent=2, ensure_ascii=False) if isinstance(data, (dict, list)) else str(data)}

{f'Contexto adicional: {context}' if context else ''}

Retorne a análise em formato JSON."""

        return self.generate_json(prompt, system_prompt)
    
    def generate_ad_copy(
        self,
        product: str,
        target_audience: str,
        platform: str = "facebook",
        tone: str = "persuasivo"
    ) -> Optional[Dict]:
        """
        Gerar copy para anúncios
        
        Args:
            product: Produto/serviço
            target_audience: Público-alvo
            platform: Plataforma (facebook, google, instagram)
            tone: Tom da comunicação
            
        Returns:
            dict: Copy gerado com headline, body, cta
        """
        system_prompt = f"""Você é um copywriter especialista em {platform} Ads.
Crie copies persuasivos e de alta conversão.
Retorne sempre em formato JSON com: headline, body, cta, variations (lista de 3 variações)."""

        prompt = f"""Crie um anúncio para {platform} com as seguintes especificações:

Produto/Serviço: {product}
Público-alvo: {target_audience}
Tom: {tone}

Retorne em JSON com headline, body, cta e 3 variações."""

        return self.generate_json(prompt, system_prompt)
    
    def create_campaign_strategy(
        self,
        product: str,
        budget: float,
        objective: str,
        duration_days: int
    ) -> Optional[Dict]:
        """
        Criar estratégia de campanha
        
        Args:
            product: Produto/serviço
            budget: Orçamento total
            objective: Objetivo da campanha
            duration_days: Duração em dias
            
        Returns:
            dict: Estratégia completa
        """
        system_prompt = """Você é um estrategista de marketing digital especialista em Facebook e Google Ads.
Crie estratégias de campanha detalhadas e otimizadas para conversão.
Retorne sempre em formato JSON."""

        prompt = f"""Crie uma estratégia de campanha com:

Produto: {product}
Orçamento Total: R$ {budget:.2f}
Objetivo: {objective}
Duração: {duration_days} dias
Orçamento Diário: R$ {budget/duration_days:.2f}

Retorne um JSON com:
- campaign_name: Nome sugerido
- daily_budget: Orçamento diário
- targeting: Segmentação recomendada
- ad_sets: Lista de conjuntos de anúncios
- schedule: Cronograma de veiculação
- kpis: KPIs esperados
- optimization_tips: Dicas de otimização"""

        return self.generate_json(prompt, system_prompt)
    
    def _get_fallback_response(self, messages: List[Dict]) -> str:
        """
        Retornar resposta padrão quando IA não está disponível
        
        Args:
            messages: Mensagens originais
            
        Returns:
            str: Resposta padrão
        """
        last_message = messages[-1]["content"] if messages else ""
        
        # Detectar tipo de requisição e retornar resposta apropriada
        if "json" in last_message.lower() or "análise" in last_message.lower():
            return json.dumps({
                "status": "offline",
                "message": "IA temporariamente indisponível. Configure OPENAI_API_KEY para habilitar.",
                "data": {}
            })
        
        return "Sistema de IA temporariamente indisponível. Por favor, configure a OPENAI_API_KEY nas variáveis de ambiente."


# Instância global do serviço
manus_ai = ManusAIService()


# Funções de conveniência para uso direto
def chat(messages: List[Dict], **kwargs) -> Optional[str]:
    """Atalho para chat_completion"""
    return manus_ai.chat_completion(messages, **kwargs)


def generate(prompt: str, **kwargs) -> Optional[str]:
    """Atalho para generate_text"""
    return manus_ai.generate_text(prompt, **kwargs)


def analyze(data: Any, **kwargs) -> Optional[Dict]:
    """Atalho para analyze_data"""
    return manus_ai.analyze_data(data, **kwargs)


def generate_copy(product: str, audience: str, **kwargs) -> Optional[Dict]:
    """Atalho para generate_ad_copy"""
    return manus_ai.generate_ad_copy(product, audience, **kwargs)


def create_strategy(product: str, budget: float, objective: str, days: int) -> Optional[Dict]:
    """Atalho para create_campaign_strategy"""
    return manus_ai.create_campaign_strategy(product, budget, objective, days)

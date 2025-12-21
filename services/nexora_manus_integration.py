"""
NEXORA + MANUS - Sistema Integrado de IA Comercial
Sistema completo de geração automática de campanhas e vendas

Autor: Manus AI Agent
Data: 25/11/2024
Atualizado: 21/12/2024 - Migrado para Manus AI Service
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Importar Manus AI Service (substitui OpenAI)
from services.manus_ai_service import manus_ai


class NexoraPrimeAI:
    """
    Nexora Prime - IA Principal de Vendas
    Responsável por estratégia, análise e decisões de alto nível
    """
    
    def __init__(self):
        self.name = "Nexora Prime"
        self.role = "Chief Sales AI"
        
    def analyze_product_for_campaign(self, product_url: str, product_info: Dict) -> Dict:
        """
        Analisa produto e cria estratégia de campanha completa
        """
        prompt = f"""
        Você é Nexora Prime, a IA mais avançada de estratégia de vendas.
        
        Analise este produto e crie uma estratégia de campanha COMPLETA:
        
        Produto: {product_info.get('name', 'Produto')}
        URL: {product_url}
        Descrição: {product_info.get('description', '')}
        Preço: {product_info.get('price', 'N/A')}
        Categoria: {product_info.get('category', 'N/A')}
        
        Crie uma análise PROFUNDA incluindo:
        
        1. PERSONA DO CLIENTE IDEAL
           - Demografia detalhada
           - Psicografia (valores, medos, desejos)
           - Comportamento de compra
           - Objeções principais
        
        2. ANÁLISE DE CONCORRÊNCIA
           - Principais concorrentes
           - Diferenciação
           - Vantagens competitivas
        
        3. ÂNGULOS DE VENDA (mínimo 5)
           - Ângulo emocional
           - Ângulo racional
           - Ângulo de urgência
           - Ângulo de autoridade
           - Ângulo de prova social
        
        4. ESTRATÉGIA DE FUNIL
           - Topo de funil (awareness)
           - Meio de funil (consideration)
           - Fundo de funil (conversion)
        
        5. ORÇAMENTO RECOMENDADO
           - Budget total
           - Distribuição por plataforma
           - CPA esperado
           - ROAS projetado
        
        Retorne em formato JSON.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é Nexora Prime, especialista em estratégia de vendas.",
            temperature=0.7
        )
        
        if result:
            result["timestamp"] = datetime.now().isoformat()
            return result
        
        return self._fallback_analysis(product_info)
    
    def _fallback_analysis(self, product_info: Dict) -> Dict:
        """Análise básica quando IA não está disponível"""
        return {
            "persona": {
                "age_range": "25-45",
                "interests": ["tecnologia", "inovação"],
                "pain_points": ["falta de tempo", "busca por qualidade"]
            },
            "sales_angles": [
                "Economia de tempo",
                "Melhor custo-benefício",
                "Qualidade premium",
                "Prova social",
                "Urgência limitada"
            ],
            "budget_recommendation": {
                "total": 5000,
                "facebook": 2000,
                "google": 2000,
                "tiktok": 1000
            },
            "expected_roas": 3.5,
            "timestamp": datetime.now().isoformat()
        }


class ManusExecutorAI:
    """
    Manus IA - Executor Operacional
    Responsável por execução, criação de assets e otimização
    """
    
    def __init__(self):
        self.name = "Manus"
        self.role = "Operational Executor AI"
    
    def generate_ad_copy(self, strategy: Dict, platform: str, format_type: str) -> Dict:
        """
        Gera copy de anúncio baseado na estratégia
        Aplica modelos AIDA, PAS, BAB
        """
        prompt = f"""
        Você é Manus, especialista em copywriting de alta conversão.
        
        Crie um anúncio PERFEITO para {platform} usando os 3 modelos:
        
        ESTRATÉGIA:
        {json.dumps(strategy, indent=2)}
        
        FORMATO: {format_type}
        
        Crie 3 variações usando:
        1. Modelo AIDA (Attention, Interest, Desire, Action)
        2. Modelo PAS (Problem, Agitate, Solution)
        3. Modelo BAB (Before, After, Bridge)
        
        Para cada variação, inclua:
        - Headline (máx 40 caracteres)
        - Primary Text (máx 125 caracteres)
        - Description (máx 90 caracteres)
        - Call-to-Action
        - Hashtags (se aplicável)
        
        IMPORTANTE:
        - Use gatilhos emocionais
        - Crie senso de urgência
        - Inclua prova social
        - CTA claro e direto
        - Linguagem persuasiva mas natural
        
        Retorne em formato JSON.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é Manus, especialista em copywriting de alta conversão.",
            temperature=0.8
        )
        
        if result:
            return result
        
        return self._fallback_copy(platform, format_type)
    
    def _fallback_copy(self, platform: str, format_type: str) -> Dict:
        """Copy básico quando IA não está disponível"""
        return {
            "variations": [
                {
                    "model": "AIDA",
                    "headline": "Transforme Seu Negócio Hoje",
                    "primary_text": "Descubra a solução que milhares de empresas já usam para crescer 300% mais rápido. Resultados em 30 dias.",
                    "description": "Comece grátis. Sem cartão de crédito.",
                    "cta": "Começar Agora",
                    "hashtags": ["#crescimento", "#sucesso", "#transformacao"]
                },
                {
                    "model": "PAS",
                    "headline": "Cansado de Perder Vendas?",
                    "primary_text": "Você está perdendo dinheiro todos os dias. Enquanto seus concorrentes crescem, você fica para trás. Mude isso agora.",
                    "description": "Solução comprovada. Resultados garantidos.",
                    "cta": "Quero Crescer",
                    "hashtags": ["#vendas", "#crescimento", "#sucesso"]
                },
                {
                    "model": "BAB",
                    "headline": "Antes vs Depois",
                    "primary_text": "Antes: vendas estagnadas. Depois: crescimento de 300%. A ponte? Nossa solução testada por 10.000+ empresas.",
                    "description": "Junte-se aos vencedores hoje.",
                    "cta": "Ver Resultados",
                    "hashtags": ["#transformacao", "#resultados", "#sucesso"]
                }
            ]
        }
    
    def generate_creative_prompts(self, strategy: Dict, copy: Dict) -> List[str]:
        """
        Gera prompts para criação de imagens/vídeos
        """
        prompt = f"""
        Você é Manus, especialista em criativos de alta conversão.
        
        Baseado nesta estratégia e copy, crie 5 prompts para geração de imagens/vídeos:
        
        ESTRATÉGIA: {json.dumps(strategy, indent=2)}
        COPY: {json.dumps(copy, indent=2)}
        
        Cada prompt deve:
        - Ser visual e específico
        - Incluir estilo (fotográfico, ilustração, 3D, etc)
        - Incluir cores dominantes
        - Incluir mood/emoção
        - Ser otimizado para conversão
        
        Retorne apenas os 5 prompts, um por linha.
        """
        
        result = manus_ai.generate_text(
            prompt=prompt,
            system_prompt="Você é Manus, especialista em criativos.",
            temperature=0.9
        )
        
        if result:
            prompts = [p.strip() for p in result.strip().split('\n') if p.strip()]
            return prompts[:5] if len(prompts) >= 5 else prompts + self._fallback_creative_prompts()[:5-len(prompts)]
        
        return self._fallback_creative_prompts()
    
    def _fallback_creative_prompts(self) -> List[str]:
        """Prompts básicos quando IA não está disponível"""
        return [
            "Fotografia profissional de produto em fundo branco minimalista, iluminação suave, alta qualidade, estilo e-commerce premium",
            "Pessoa sorridente usando o produto em ambiente moderno, cores vibrantes, estilo lifestyle, sensação de sucesso e satisfação",
            "Comparação antes/depois em split screen, lado esquerdo escuro e triste, lado direito brilhante e colorido, transformação visual",
            "Infográfico moderno mostrando benefícios do produto, ícones flat design, cores azul e laranja, estilo corporativo profissional",
            "Cena de unboxing com mãos abrindo embalagem premium, confete dourado, fundo gradiente, sensação de exclusividade e luxo"
        ]
    
    def optimize_campaign_performance(self, campaign_data: Dict) -> Dict:
        """
        Analisa dados de campanha e sugere otimizações
        """
        prompt = f"""
        Você é Manus, especialista em otimização de campanhas.
        
        Analise estes dados de campanha e sugira otimizações:
        
        DADOS DA CAMPANHA:
        {json.dumps(campaign_data, indent=2)}
        
        Forneça:
        1. Diagnóstico do desempenho atual
        2. Problemas identificados
        3. Otimizações recomendadas (mínimo 5)
        4. Previsão de melhoria com cada otimização
        5. Priorização das ações
        
        Retorne em formato JSON.
        """
        
        result = manus_ai.generate_json(
            prompt=prompt,
            system_prompt="Você é Manus, especialista em otimização de campanhas.",
            temperature=0.5
        )
        
        if result:
            return result
        
        return {
            "diagnosis": "Análise não disponível",
            "issues": [],
            "optimizations": [
                {"action": "Aumentar orçamento em horários de pico", "impact": "alto"},
                {"action": "Testar novos criativos", "impact": "médio"},
                {"action": "Refinar segmentação", "impact": "alto"}
            ],
            "priority": ["segmentação", "criativos", "orçamento"]
        }


class NexoraManusOrchestrator:
    """
    Orquestrador que coordena Nexora Prime e Manus
    """
    
    def __init__(self):
        self.nexora = NexoraPrimeAI()
        self.manus = ManusExecutorAI()
    
    def create_full_campaign(self, product_url: str, product_info: Dict, budget: float = 5000) -> Dict:
        """
        Cria campanha completa do zero
        """
        # 1. Nexora Prime analisa e cria estratégia
        strategy = self.nexora.analyze_product_for_campaign(product_url, product_info)
        
        # 2. Manus gera copies para cada plataforma
        copies = {
            "facebook": self.manus.generate_ad_copy(strategy, "facebook", "feed"),
            "instagram": self.manus.generate_ad_copy(strategy, "instagram", "stories"),
            "google": self.manus.generate_ad_copy(strategy, "google", "search")
        }
        
        # 3. Manus gera prompts de criativos
        creative_prompts = self.manus.generate_creative_prompts(strategy, copies["facebook"])
        
        return {
            "strategy": strategy,
            "copies": copies,
            "creative_prompts": creative_prompts,
            "budget": budget,
            "created_at": datetime.now().isoformat(),
            "status": "ready_to_launch"
        }
    
    def optimize_existing_campaign(self, campaign_id: str, campaign_data: Dict) -> Dict:
        """
        Otimiza campanha existente
        """
        optimizations = self.manus.optimize_campaign_performance(campaign_data)
        
        return {
            "campaign_id": campaign_id,
            "optimizations": optimizations,
            "analyzed_at": datetime.now().isoformat()
        }


# Instâncias globais
nexora_prime = NexoraPrimeAI()
manus_executor = ManusExecutorAI()
orchestrator = NexoraManusOrchestrator()

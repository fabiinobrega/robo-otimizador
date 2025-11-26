"""
NEXORA + MANUS - Sistema Integrado de IA Comercial
Sistema completo de geração automática de campanhas e vendas

Autor: Manus AI Agent
Data: 25/11/2024
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Importar OpenAI para IA
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except ImportError:
    client = None


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
        if not client:
            return self._fallback_analysis(product_info)
            
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
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você é Nexora Prime, especialista em estratégia de vendas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis = response.choices[0].message.content
            
            # Tentar parsear JSON
            try:
                return json.loads(analysis)
            except:
                return {
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"Erro na análise Nexora Prime: {e}")
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
            "expected_roas": 3.5
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
        if not client:
            return self._fallback_copy(platform, format_type)
        
        # Selecionar modelo de copy
        models = {
            "AIDA": "Attention, Interest, Desire, Action",
            "PAS": "Problem, Agitate, Solution",
            "BAB": "Before, After, Bridge"
        }
        
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
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você é Manus, especialista em copywriting de alta conversão."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            
            copy_result = response.choices[0].message.content
            
            try:
                return json.loads(copy_result)
            except:
                return {
                    "variations": [
                        {
                            "model": "AIDA",
                            "headline": "Transforme Seu Negócio Hoje",
                            "primary_text": copy_result[:125],
                            "description": "Resultados garantidos em 30 dias",
                            "cta": "Começar Agora"
                        }
                    ]
                }
                
        except Exception as e:
            print(f"Erro na geração de copy: {e}")
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
        if not client:
            return self._fallback_creative_prompts()
        
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
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você é Manus, especialista em criativos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=500
            )
            
            prompts = response.choices[0].message.content.strip().split('\n')
            return [p.strip() for p in prompts if p.strip()]
            
        except Exception as e:
            print(f"Erro na geração de prompts: {e}")
            return self._fallback_creative_prompts()
    
    def _fallback_creative_prompts(self) -> List[str]:
        """Prompts básicos quando IA não está disponível"""
        return [
            "Fotografia profissional de produto em fundo minimalista branco, iluminação suave, alta qualidade, 8K",
            "Pessoa feliz usando o produto, ambiente moderno e clean, cores vibrantes, estilo lifestyle",
            "Antes e depois dramático, split screen, transformação visível, cores contrastantes",
            "Infográfico moderno mostrando benefícios, ícones minimalistas, paleta azul e verde",
            "Vídeo curto de 15s mostrando produto em ação, transições suaves, música energética"
        ]


class CampaignPerformancePredictor:
    """
    Preditor de Performance de Campanhas
    Usa IA para prever conversões e sugerir ajustes
    """
    
    def __init__(self):
        self.name = "Performance Predictor"
    
    def predict_campaign_performance(self, campaign_data: Dict) -> Dict:
        """
        Prevê performance da campanha antes de lançar
        """
        if not client:
            return self._fallback_prediction(campaign_data)
        
        prompt = f"""
        Você é um especialista em previsão de performance de campanhas.
        
        Analise esta campanha e preveja:
        
        CAMPANHA:
        {json.dumps(campaign_data, indent=2)}
        
        Preveja:
        1. CTR esperado (%)
        2. Taxa de conversão esperada (%)
        3. CPA esperado (R$)
        4. ROAS esperado (x)
        5. Impressões estimadas
        6. Cliques estimados
        7. Conversões estimadas
        8. Receita estimada (R$)
        
        Também forneça:
        - Nível de confiança (0-100%)
        - Fatores de risco
        - Recomendações de otimização
        
        Retorne em formato JSON.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em previsão de performance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            prediction = response.choices[0].message.content
            
            try:
                return json.loads(prediction)
            except:
                return self._fallback_prediction(campaign_data)
                
        except Exception as e:
            print(f"Erro na previsão: {e}")
            return self._fallback_prediction(campaign_data)
    
    def _fallback_prediction(self, campaign_data: Dict) -> Dict:
        """Previsão básica quando IA não está disponível"""
        budget = campaign_data.get('budget', 1000)
        
        return {
            "predictions": {
                "ctr": 1.5,
                "conversion_rate": 2.0,
                "cpa": 50,
                "roas": 3.5,
                "impressions": int(budget * 100),
                "clicks": int(budget * 1.5),
                "conversions": int(budget / 50),
                "revenue": int(budget * 3.5)
            },
            "confidence": 75,
            "risk_factors": [
                "Campanha nova sem histórico",
                "Mercado competitivo"
            ],
            "recommendations": [
                "Iniciar com budget menor para teste",
                "Criar múltiplas variações de copy",
                "Monitorar métricas nas primeiras 48h"
            ]
        }
    
    def suggest_optimizations(self, campaign_id: int, current_metrics: Dict) -> List[Dict]:
        """
        Sugere otimizações baseadas em métricas atuais
        """
        if not client:
            return self._fallback_optimizations(current_metrics)
        
        prompt = f"""
        Você é um especialista em otimização de campanhas.
        
        Analise estas métricas e sugira otimizações ESPECÍFICAS:
        
        MÉTRICAS ATUAIS:
        {json.dumps(current_metrics, indent=2)}
        
        Para cada otimização, forneça:
        - Ação específica
        - Impacto esperado (%)
        - Prioridade (Alta/Média/Baixa)
        - Tempo para implementar
        - Risco (Baixo/Médio/Alto)
        
        Retorne em formato JSON (lista de otimizações).
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em otimização."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1000
            )
            
            optimizations = response.choices[0].message.content
            
            try:
                return json.loads(optimizations)
            except:
                return self._fallback_optimizations(current_metrics)
                
        except Exception as e:
            print(f"Erro nas otimizações: {e}")
            return self._fallback_optimizations(current_metrics)
    
    def _fallback_optimizations(self, metrics: Dict) -> List[Dict]:
        """Otimizações básicas quando IA não está disponível"""
        ctr = metrics.get('ctr', 0)
        roas = metrics.get('roas', 0)
        
        optimizations = []
        
        if ctr < 1.0:
            optimizations.append({
                "action": "Melhorar criativos e headlines",
                "expected_impact": "+50%",
                "priority": "Alta",
                "time_to_implement": "2 horas",
                "risk": "Baixo"
            })
        
        if roas < 2.0:
            optimizations.append({
                "action": "Refinar targeting e audiências",
                "expected_impact": "+30%",
                "priority": "Alta",
                "time_to_implement": "1 hora",
                "risk": "Médio"
            })
        
        return optimizations


# Instâncias globais
nexora_prime = NexoraPrimeAI()
manus_executor = ManusExecutorAI()
performance_predictor = CampaignPerformancePredictor()


def create_complete_campaign(product_url: str, product_info: Dict, platforms: List[str]) -> Dict:
    """
    Função principal: cria campanha completa do zero
    Integra Nexora Prime + Manus para resultado perfeito
    """
    
    print(f"🚀 Iniciando criação de campanha completa...")
    print(f"📊 Nexora Prime analisando produto...")
    
    # 1. Nexora Prime analisa e cria estratégia
    strategy = nexora_prime.analyze_product_for_campaign(product_url, product_info)
    
    print(f"✅ Estratégia criada!")
    print(f"✍️ Manus gerando copy...")
    
    # 2. Manus gera copy para cada plataforma
    campaign_assets = {}
    
    for platform in platforms:
        # Gerar copy
        copy = manus_executor.generate_ad_copy(strategy, platform, "feed")
        
        # Gerar prompts de criativos
        creative_prompts = manus_executor.generate_creative_prompts(strategy, copy)
        
        campaign_assets[platform] = {
            "copy": copy,
            "creative_prompts": creative_prompts
        }
    
    print(f"✅ Copy e criativos gerados!")
    print(f"🔮 Prevendo performance...")
    
    # 3. Prever performance
    campaign_data = {
        "product": product_info,
        "strategy": strategy,
        "platforms": platforms,
        "budget": strategy.get('budget_recommendation', {}).get('total', 5000)
    }
    
    prediction = performance_predictor.predict_campaign_performance(campaign_data)
    
    print(f"✅ Previsão completa!")
    
    # 4. Retornar tudo
    return {
        "success": True,
        "strategy": strategy,
        "assets": campaign_assets,
        "prediction": prediction,
        "created_at": datetime.now().isoformat(),
        "created_by": "Nexora Prime + Manus AI"
    }


# Exportar funções principais
__all__ = [
    'nexora_prime',
    'manus_executor',
    'performance_predictor',
    'create_complete_campaign'
]

"""
OpenAI Strategic Brain - Cérebro Estratégico
OpenAI é usado APENAS para PENSAR: estratégia, copywriting, criativos
NÃO executa nada técnico
"""

import os
import json
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

# Importar OpenAI com verificação
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = bool(os.environ.get("OPENAI_API_KEY"))
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAIStrategicBrain:
    """
    Cérebro estratégico que usa OpenAI APENAS para pensar
    Não executa nada técnico - isso é trabalho do Manus
    """
    
    def __init__(self):
        if OPENAI_AVAILABLE:
            self.client = OpenAI()
        else:
            self.client = None
            print("⚠️ OPENAI_API_KEY não configurada - OpenAIStrategicBrain desabilitado")
    
    def create_campaign_strategy(self, spy_report, product, objective, total_budget, duration_days):
        """
        Cria estratégia de campanha baseada na espionagem
        
        Args:
            spy_report (dict): Relatório de espionagem
            product (str): Produto/serviço
            objective (str): Objetivo de vendas
            total_budget (float): Orçamento total
            duration_days (int): Duração em dias
            
        Returns:
            dict: Estratégia completa
        """
        daily_budget = total_budget / duration_days
        
        # Determinar tipo de campanha por duração
        if duration_days <= 7:
            campaign_type = "CURTA (1-7 dias) - Foco em conversões rápidas"
        elif duration_days <= 30:
            campaign_type = "MÉDIA (8-30 dias) - Estratégia balanceada"
        else:
            campaign_type = "LONGA (31+ dias) - Estratégia de longo prazo"
        
        try:
            prompt = f"""
Você é um estrategista de marketing digital de elite.

Com base nesta análise de concorrência:
{spy_report.get('analysis', 'Análise não disponível')}

Crie uma ESTRATÉGIA COMPLETA para:
- Produto: {product}
- Objetivo: {objective}
- Orçamento Total: R$ {total_budget:.2f}
- Duração: {duration_days} dias
- Orçamento Diário: R$ {daily_budget:.2f}/dia
- Tipo de Campanha: {campaign_type}

A estratégia deve incluir:

1. POSICIONAMENTO:
   - Como se diferenciar dos concorrentes?
   - Qual o ângulo único?
   - Qual a proposta de valor?

2. FUNIL DE VENDAS:
   - Topo: Como atrair atenção?
   - Meio: Como nutrir interesse?
   - Fundo: Como converter?

3. MENSAGEM PRINCIPAL:
   - Qual a mensagem central?
   - Quais os 3 benefícios principais?
   - Qual a prova social a usar?

4. SEGMENTAÇÃO:
   - Público primário
   - Público secundário
   - Interesses e comportamentos

5. ALOCAÇÃO DE ORÇAMENTO:
   - % para topo de funil
   - % para meio de funil
   - % para fundo de funil

Seja específico, prático e focado em resultados.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um estrategista de marketing com 15 anos de experiência em campanhas de alta performance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            strategy_text = response.choices[0].message.content
            
            return {
                'timestamp': datetime.now().isoformat(),
                'product': product,
                'objective': objective,
                'budget': budget,
                'strategy': strategy_text,
                'based_on_spy': True
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar estratégia: {e}")
            raise
    
    def generate_ad_copy(self, strategy, spy_recommendations):
        """
        Gera copy de anúncio baseado na estratégia
        
        Args:
            strategy (dict): Estratégia criada
            spy_recommendations (list): Recomendações da espionagem
            
        Returns:
            dict: Copy completo do anúncio
        """
        try:
            recommendations_text = '\n'.join(spy_recommendations)
            
            prompt = f"""
Com base nesta estratégia:
{strategy['strategy']}

E nestas recomendações competitivas:
{recommendations_text}

Crie um COPY COMPLETO DE ANÚNCIO com:

1. HEADLINE (3 variações):
   - Variação A: [headline impactante]
   - Variação B: [headline com benefício]
   - Variação C: [headline com pergunta]

2. TEXTO PRINCIPAL (150-200 palavras):
   - Gancho inicial
   - Problema que resolve
   - Solução oferecida
   - Benefícios principais
   - Prova social
   - Urgência/escassez

3. CALL-TO-ACTION (3 variações):
   - CTA A: [direto]
   - CTA B: [com benefício]
   - CTA C: [com urgência]

4. DESCRIÇÃO DO CRIATIVO:
   - Que tipo de imagem/vídeo usar?
   - Cores sugeridas
   - Elementos visuais importantes
   - Emoção a transmitir

5. PROMESSA PRINCIPAL:
   - Qual a promessa central do anúncio?

Seja persuasivo, claro e focado em conversão.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um copywriter especialista em anúncios de alta conversão."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=1500
            )
            
            copy_text = response.choices[0].message.content
            
            # Extrair headlines
            headlines = self._extract_headlines(copy_text)
            
            # Extrair CTAs
            ctas = self._extract_ctas(copy_text)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'full_copy': copy_text,
                'headlines': headlines,
                'ctas': ctas,
                'ready_for_manus': True
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar copy: {e}")
            raise
    
    def optimize_copy_for_platform(self, copy, platform):
        """
        Otimiza copy para plataforma específica
        
        Args:
            copy (dict): Copy gerado
            platform (str): Plataforma (facebook, google, etc)
            
        Returns:
            dict: Copy otimizado
        """
        try:
            platform_rules = {
                'facebook': 'Texto mais conversacional, emojis permitidos, foco em storytelling',
                'google': 'Texto mais direto, foco em palavras-chave, sem emojis',
                'instagram': 'Texto curto, muitos emojis, hashtags relevantes',
                'linkedin': 'Texto profissional, foco em valor de negócio, sem emojis'
            }
            
            rule = platform_rules.get(platform, platform_rules['facebook'])
            
            prompt = f"""
Adapte este copy para {platform.upper()}:

{copy['full_copy']}

Regras da plataforma:
{rule}

Mantenha a essência, mas adapte o tom e formato.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Você é especialista em anúncios para {platform}."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            optimized_copy = response.choices[0].message.content
            
            return {
                **copy,
                'platform': platform,
                'optimized_copy': optimized_copy
            }
            
        except Exception as e:
            logger.error(f"Erro ao otimizar copy: {e}")
            return copy
    
    def create_differentiation_angle(self, product, competitors_analysis):
        """
        Cria ângulo de diferenciação único
        
        Args:
            product (str): Produto/serviço
            competitors_analysis (str): Análise de concorrentes
            
        Returns:
            dict: Ângulo de diferenciação
        """
        try:
            prompt = f"""
Produto: {product}

Análise de concorrentes:
{competitors_analysis}

Crie 3 ÂNGULOS DE DIFERENCIAÇÃO ÚNICOS que:
1. Não sejam usados pelos concorrentes
2. Sejam genuínos e verdadeiros
3. Sejam relevantes para o público
4. Sejam fáceis de comunicar

Para cada ângulo, explique:
- O ângulo
- Por que funciona
- Como comunicar
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é especialista em posicionamento de marca e diferenciação competitiva."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=1000
            )
            
            return {
                'product': product,
                'differentiation_angles': response.choices[0].message.content
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar diferenciação: {e}")
            raise
    
    def _extract_headlines(self, copy_text):
        """Extrai headlines do copy"""
        headlines = []
        lines = copy_text.split('\n')
        
        for line in lines:
            if 'Variação A:' in line or 'Variação B:' in line or 'Variação C:' in line:
                headline = line.split(':', 1)[1].strip()
                headlines.append(headline)
        
        return headlines if headlines else ['Headline padrão']
    
    def _extract_ctas(self, copy_text):
        """Extrai CTAs do copy"""
        ctas = []
        lines = copy_text.split('\n')
        
        for line in lines:
            if 'CTA A:' in line or 'CTA B:' in line or 'CTA C:' in line:
                cta = line.split(':', 1)[1].strip()
                ctas.append(cta)
        
        return ctas if ctas else ['Saiba Mais']

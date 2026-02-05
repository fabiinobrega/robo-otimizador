"""
MANUS CAMPAIGN CREATOR
Criador de campanhas completas usando EXCLUSIVAMENTE Manus AI
OpenAI foi REMOVIDA conforme solicitação do usuário.
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

# Importar Manus AI Service (ÚNICO provedor de IA)
from services.manus_ai_service import manus_ai


class OpenAICampaignCreator:
    """
    Criador de campanhas baseado em Manus AI (nome mantido para compatibilidade)
    
    Responsabilidades:
    - Criação de campanhas estruturadas
    - Geração de copy persuasivo
    - Criação de headlines e descrições
    - Argumentos de venda
    - Scripts e storytelling
    
    NOTA: Usa APENAS Manus AI. OpenAI foi removida.
    """
    
    def __init__(self):
        self.manus_ai = manus_ai
        
    def generate_campaign_copy(self, campaign_data: Dict[str, Any], platform: str = "google") -> Dict[str, Any]:
        """
        Gerar copy completo para campanha usando Manus AI
        """
        platform_specs = self._get_platform_specs(platform)
        
        prompt = f"""
        Como copywriter especializado em {platform.upper()}, crie copy completo para esta campanha:
        
        **Campanha:**
        - Produto: {campaign_data.get('product', 'Não informado')}
        - Objetivo: {campaign_data.get('objective', 'Conversões')}
        - Público: {campaign_data.get('audience', 'Geral')}
        - Proposta de Valor: {campaign_data.get('value_proposition', 'Não informada')}
        - Tom de Voz: {campaign_data.get('tone', 'Profissional')}
        
        **Especificações {platform.upper()}:**
        {json.dumps(platform_specs, indent=2)}
        
        Crie 5 variações completas de anúncio, cada uma com:
        1. Headline principal (respeitando limite de caracteres)
        2. Headline secundária (se aplicável)
        3. Descrição longa
        4. Descrição curta
        5. Call-to-action
        6. Palavras-chave de destaque
        7. Gatilhos mentais usados
        8. Público-alvo sugerido
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um copywriter e criador de conteúdo de marketing de classe mundial. Sempre responda em formato JSON estruturado e em português."
            )
            
            if result:
                return {
                    "success": True,
                    "platform": platform,
                    "variations": result,
                    "generated_at": datetime.now().isoformat(),
                    "engine": "Manus AI"
                }
        except Exception as e:
            pass
            
        return {
            "success": False,
            "error": "Manus AI temporariamente indisponível",
            "engine": "Manus AI"
        }
    
    def generate_headlines(self, product_data: Dict[str, Any], count: int = 10) -> Dict[str, Any]:
        """
        Gerar headlines persuasivas usando Manus AI
        """
        prompt = f"""
        Como copywriter especializado, crie {count} headlines persuasivas para:
        
        **Produto/Serviço:** {product_data.get('name', 'Não informado')}
        **Benefício Principal:** {product_data.get('main_benefit', 'Não informado')}
        **Diferencial:** {product_data.get('unique_selling_point', 'Não informado')}
        **Público:** {product_data.get('target_audience', 'Geral')}
        
        Crie headlines que:
        1. Sejam curtas e impactantes (máx 30 caracteres)
        2. Usem gatilhos mentais (urgência, escassez, prova social)
        3. Destaquem benefícios, não features
        4. Criem curiosidade
        5. Sejam específicas e mensuráveis quando possível
        
        Para cada headline, forneça:
        - Texto da headline
        - Gatilho mental usado
        - Pontuação de impacto (0-10)
        - Contexto ideal de uso
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um copywriter especializado em headlines de alta conversão."
            )
            
            if result:
                return {
                    "success": True,
                    "headlines": result,
                    "count": count,
                    "generated_at": datetime.now().isoformat(),
                    "engine": "Manus AI"
                }
        except Exception as e:
            pass
            
        return {
            "success": False,
            "error": "Manus AI temporariamente indisponível",
            "engine": "Manus AI"
        }
    
    def generate_sales_argument(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerar argumento de venda completo usando Manus AI
        """
        prompt = f"""
        Como especialista em vendas, crie um argumento de venda completo para:
        
        **Produto:** {product_data.get('name', 'Não informado')}
        **Preço:** R$ {product_data.get('price', 0)}
        **Benefícios:** {', '.join(product_data.get('benefits', []))}
        **Público:** {product_data.get('target_audience', 'Geral')}
        **Objeções Comuns:** {', '.join(product_data.get('objections', []))}
        
        Crie um argumento com:
        1. Hook de abertura (gancho emocional)
        2. Identificação do problema
        3. Agravamento do problema
        4. Apresentação da solução
        5. Explicação de como funciona
        6. Prova social e credibilidade
        7. Benefícios transformacionais
        8. Comparação com alternativas
        9. Garantias e redução de risco
        10. Call-to-action urgente
        11. Respostas para objeções
        12. Fechamento poderoso
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um especialista em vendas e persuasão."
            )
            
            if result:
                return {
                    "success": True,
                    "argument": result,
                    "generated_at": datetime.now().isoformat(),
                    "engine": "Manus AI"
                }
        except Exception as e:
            pass
            
        return {
            "success": False,
            "error": "Manus AI temporariamente indisponível",
            "engine": "Manus AI"
        }
    
    def generate_storytelling(self, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerar storytelling da marca usando Manus AI
        """
        prompt = f"""
        Como especialista em storytelling, crie uma narrativa envolvente para:
        
        **Marca:** {brand_data.get('name', 'Não informado')}
        **Missão:** {brand_data.get('mission', 'Não informada')}
        **Valores:** {', '.join(brand_data.get('values', []))}
        **História:** {brand_data.get('history', 'Não informada')}
        **Impacto:** {brand_data.get('impact', 'Não informado')}
        
        Crie um storytelling com:
        1. Origem da marca (jornada do herói)
        2. Desafios enfrentados
        3. Momento de transformação
        4. Missão e propósito
        5. Impacto no mundo
        6. Visão de futuro
        7. Convite para fazer parte
        
        Versões:
        - Versão longa (500 palavras)
        - Versão média (200 palavras)
        - Versão curta (50 palavras)
        - Versão elevator pitch (25 palavras)
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um especialista em storytelling e branding."
            )
            
            if result:
                return {
                    "success": True,
                    "storytelling": result,
                    "generated_at": datetime.now().isoformat(),
                    "engine": "Manus AI"
                }
        except Exception as e:
            pass
            
        return {
            "success": False,
            "error": "Manus AI temporariamente indisponível",
            "engine": "Manus AI"
        }
    
    def generate_video_script(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerar script de vídeo usando Manus AI
        """
        prompt = f"""
        Como roteirista de vídeos de marketing, crie um script para:
        
        **Tipo:** {video_data.get('type', 'Vídeo explicativo')}
        **Duração:** {video_data.get('duration', 60)} segundos
        **Produto:** {video_data.get('product', 'Não informado')}
        **Objetivo:** {video_data.get('objective', 'Conversão')}
        **Plataforma:** {video_data.get('platform', 'YouTube')}
        
        Crie um script com:
        1. Hook dos primeiros 3 segundos
        2. Estrutura cena por cena
        3. Texto narrado
        4. Ações visuais
        5. Trilha sonora sugerida
        6. Texto na tela
        7. Call-to-action final
        8. Timing de cada cena
        
        Retorne em formato JSON estruturado.
        """
        
        try:
            result = self.manus_ai.generate_json(
                prompt=prompt,
                system_prompt="Você é um roteirista especializado em vídeos de marketing."
            )
            
            if result:
                return {
                    "success": True,
                    "script": result,
                    "generated_at": datetime.now().isoformat(),
                    "engine": "Manus AI"
                }
        except Exception as e:
            pass
            
        return {
            "success": False,
            "error": "Manus AI temporariamente indisponível",
            "engine": "Manus AI"
        }
    
    def _get_platform_specs(self, platform: str) -> Dict[str, Any]:
        """Obter especificações da plataforma"""
        specs = {
            "google": {
                "headline_max": 30,
                "description_max": 90,
                "path_max": 15
            },
            "facebook": {
                "headline_max": 40,
                "description_max": 125,
                "text_max": 125
            },
            "instagram": {
                "caption_max": 2200,
                "hashtags_max": 30
            },
            "linkedin": {
                "headline_max": 200,
                "description_max": 600
            }
        }
        
        return specs.get(platform, specs["google"])


# Instância global para compatibilidade
campaign_creator = OpenAICampaignCreator()

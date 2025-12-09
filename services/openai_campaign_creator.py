"""
OPENAI CAMPAIGN CREATOR
Criador de campanhas completas usando ChatGPT
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

class OpenAICampaignCreator:
    """
    Criador de campanhas baseado em ChatGPT
    
    Responsabilidades:
    - Criação de campanhas estruturadas
    - Geração de copy persuasivo
    - Criação de headlines e descrições
    - Argumentos de venda
    - Scripts e storytelling
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-4"
        
    def generate_campaign_copy(self, campaign_data: Dict[str, Any], platform: str = "google") -> Dict[str, Any]:
        """
        Gerar copy completo para campanha
        
        Args:
            campaign_data: Dados da campanha
            platform: Plataforma (google, facebook, etc)
            
        Returns:
            Copy completo
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
            response = self._call_gpt(prompt)
            copy_variations = self._parse_json_response(response)
            
            return {
                "success": True,
                "platform": platform,
                "variations": copy_variations,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_headlines(self, product_data: Dict[str, Any], count: int = 10) -> Dict[str, Any]:
        """
        Gerar headlines persuasivas
        
        Args:
            product_data: Dados do produto
            count: Quantidade de headlines
            
        Returns:
            Headlines geradas
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
            response = self._call_gpt(prompt)
            headlines = self._parse_json_response(response)
            
            return {
                "success": True,
                "headlines": headlines,
                "count": len(headlines.get('headlines', [])) if isinstance(headlines, dict) else count,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_sales_argument(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerar argumento de venda completo
        
        Args:
            product_data: Dados do produto
            
        Returns:
            Argumento de venda
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
            response = self._call_gpt(prompt)
            argument = self._parse_json_response(response)
            
            return {
                "success": True,
                "argument": argument,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_storytelling(self, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerar storytelling da marca
        
        Args:
            brand_data: Dados da marca
            
        Returns:
            Storytelling completo
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
            response = self._call_gpt(prompt)
            storytelling = self._parse_json_response(response)
            
            return {
                "success": True,
                "storytelling": storytelling,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_video_script(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerar script de vídeo
        
        Args:
            video_data: Dados do vídeo
            
        Returns:
            Script completo
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
            response = self._call_gpt(prompt)
            script = self._parse_json_response(response)
            
            return {
                "success": True,
                "script": script,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
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
    
    def _call_gpt(self, prompt: str, temperature: float = 0.8) -> str:
        """Chamar API do ChatGPT"""
        if not self.api_key:
            return json.dumps({"error": "API key not configured"})
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Você é um copywriter e criador de conteúdo de marketing de classe mundial. Sempre responda em formato JSON estruturado e em português."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return json.dumps({"error": f"API returned status {response.status_code}"})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse resposta JSON do GPT"""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except:
            return {"response": response}

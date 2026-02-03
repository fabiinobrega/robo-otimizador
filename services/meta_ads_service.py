"""
Meta Ads Service - Integração Completa com Facebook/Instagram Ads API
Criação e gerenciamento de campanhas no Meta Ads
Autor: Manus AI Agent
Data: 03/02/2026
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class MetaAdsService:
    """Serviço completo de integração com Meta Ads (Facebook/Instagram)"""
    
    def __init__(self):
        """Inicializar serviço com credenciais"""
        # Credenciais Meta Ads
        self.access_token = os.environ.get("META_ACCESS_TOKEN", "")
        self.app_id = os.environ.get("META_APP_ID", "")
        self.app_secret = os.environ.get("META_APP_SECRET", "")
        self.ad_account_id = os.environ.get("META_AD_ACCOUNT_ID", "")
        self.pixel_id = os.environ.get("META_PIXEL_ID", "865226839589725")  # Pixel do usuário
        
        # URLs da API
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        
        # Cache de dados
        self.campaigns_cache = []
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return bool(self.access_token and self.ad_account_id)
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict[str, Any]:
        """
        Fazer requisição à API do Meta
        
        Args:
            method: GET, POST, PUT, DELETE
            endpoint: Endpoint da API
            data: Dados para POST/PUT
            params: Parâmetros de query
        
        Returns:
            Resposta da API
        """
        url = f"{self.base_url}/{endpoint}"
        
        # Adicionar access_token aos parâmetros
        if params is None:
            params = {}
        params["access_token"] = self.access_token
        
        try:
            if method == "GET":
                response = requests.get(url, params=params)
            elif method == "POST":
                response = requests.post(url, json=data, params=params)
            elif method == "PUT":
                response = requests.put(url, json=data, params=params)
            elif method == "DELETE":
                response = requests.delete(url, params=params)
            else:
                return {"success": False, "error": f"Método {method} não suportado"}
            
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Erro na API: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Erro: {str(e)}"}
    
    # ===== CRIAÇÃO DE CAMPANHAS =====
    
    def create_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar campanha no Meta Ads
        
        Args:
            campaign_config: Configuração da campanha
                - name: Nome da campanha
                - objective: Objetivo (CONVERSIONS, TRAFFIC, REACH, etc.)
                - status: Status (PAUSED, ACTIVE)
                - special_ad_categories: Categorias especiais (opcional)
        
        Returns:
            Resultado com campaign_id
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        # Preparar dados da campanha
        campaign_data = {
            "name": campaign_config.get("name", "Nova Campanha"),
            "objective": campaign_config.get("objective", "OUTCOME_TRAFFIC"),
            "status": campaign_config.get("status", "PAUSED"),
            "special_ad_categories": campaign_config.get("special_ad_categories", [])
        }
        
        # Criar campanha
        endpoint = f"act_{self.ad_account_id}/campaigns"
        result = self._make_request("POST", endpoint, data=campaign_data)
        
        if result.get("success"):
            campaign_id = result["data"].get("id")
            return {
                "success": True,
                "campaign_id": campaign_id,
                "message": "Campanha criada com sucesso"
            }
        else:
            return result
    
    def create_ad_set(self, campaign_id: str, ad_set_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar conjunto de anúncios (Ad Set)
        
        Args:
            campaign_id: ID da campanha
            ad_set_config: Configuração do ad set
                - name: Nome do ad set
                - optimization_goal: Meta de otimização (LINK_CLICKS, CONVERSIONS, etc.)
                - billing_event: Evento de cobrança (IMPRESSIONS, LINK_CLICKS, etc.)
                - bid_amount: Lance em centavos
                - daily_budget: Orçamento diário em centavos
                - targeting: Segmentação (geo_locations, age_min, age_max, genders, interests, etc.)
                - start_time: Data/hora de início
                - end_time: Data/hora de término (opcional)
        
        Returns:
            Resultado com ad_set_id
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        # Preparar dados do ad set
        ad_set_data = {
            "name": ad_set_config.get("name", "Novo Ad Set"),
            "campaign_id": campaign_id,
            "optimization_goal": ad_set_config.get("optimization_goal", "LINK_CLICKS"),
            "billing_event": ad_set_config.get("billing_event", "IMPRESSIONS"),
            "bid_amount": ad_set_config.get("bid_amount", 100),  # $1.00 em centavos
            "daily_budget": ad_set_config.get("daily_budget", 1000),  # $10.00 em centavos
            "targeting": ad_set_config.get("targeting", {
                "geo_locations": {"countries": ["US"]},
                "age_min": 25,
                "age_max": 65
            }),
            "status": ad_set_config.get("status", "PAUSED"),
            "start_time": ad_set_config.get("start_time", datetime.now().isoformat())
        }
        
        # Adicionar end_time se fornecido
        if ad_set_config.get("end_time"):
            ad_set_data["end_time"] = ad_set_config["end_time"]
        
        # Criar ad set
        endpoint = f"act_{self.ad_account_id}/adsets"
        result = self._make_request("POST", endpoint, data=ad_set_data)
        
        if result.get("success"):
            ad_set_id = result["data"].get("id")
            return {
                "success": True,
                "ad_set_id": ad_set_id,
                "message": "Ad Set criado com sucesso"
            }
        else:
            return result
    
    def create_ad_creative(self, creative_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar criativo de anúncio
        
        Args:
            creative_config: Configuração do criativo
                - name: Nome do criativo
                - object_story_spec: Especificação da história (link, imagem, vídeo, etc.)
                    - page_id: ID da página do Facebook
                    - link_data: Dados do link (link, message, name, description, picture)
        
        Returns:
            Resultado com creative_id
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        # Preparar dados do criativo
        creative_data = {
            "name": creative_config.get("name", "Novo Criativo"),
            "object_story_spec": creative_config.get("object_story_spec", {})
        }
        
        # Criar criativo
        endpoint = f"act_{self.ad_account_id}/adcreatives"
        result = self._make_request("POST", endpoint, data=creative_data)
        
        if result.get("success"):
            creative_id = result["data"].get("id")
            return {
                "success": True,
                "creative_id": creative_id,
                "message": "Criativo criado com sucesso"
            }
        else:
            return result
    
    def create_ad(self, ad_set_id: str, creative_id: str, ad_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar anúncio
        
        Args:
            ad_set_id: ID do ad set
            creative_id: ID do criativo
            ad_config: Configuração do anúncio
                - name: Nome do anúncio
                - status: Status (PAUSED, ACTIVE)
        
        Returns:
            Resultado com ad_id
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        # Preparar dados do anúncio
        ad_data = {
            "name": ad_config.get("name", "Novo Anúncio"),
            "adset_id": ad_set_id,
            "creative": {"creative_id": creative_id},
            "status": ad_config.get("status", "PAUSED")
        }
        
        # Criar anúncio
        endpoint = f"act_{self.ad_account_id}/ads"
        result = self._make_request("POST", endpoint, data=ad_data)
        
        if result.get("success"):
            ad_id = result["data"].get("id")
            return {
                "success": True,
                "ad_id": ad_id,
                "message": "Anúncio criado com sucesso"
            }
        else:
            return result
    
    # ===== CRIAÇÃO COMPLETA DE CAMPANHA =====
    
    def create_complete_campaign(self, full_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar campanha completa (Campaign + Ad Set + Creative + Ad)
        
        Args:
            full_config: Configuração completa
                - campaign: Configuração da campanha
                - ad_set: Configuração do ad set
                - creative: Configuração do criativo
                - ad: Configuração do anúncio
        
        Returns:
            Resultado com todos os IDs
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        try:
            # 1. Criar campanha
            campaign_result = self.create_campaign(full_config.get("campaign", {}))
            if not campaign_result.get("success"):
                return campaign_result
            
            campaign_id = campaign_result["campaign_id"]
            
            # 2. Criar ad set
            ad_set_result = self.create_ad_set(campaign_id, full_config.get("ad_set", {}))
            if not ad_set_result.get("success"):
                return ad_set_result
            
            ad_set_id = ad_set_result["ad_set_id"]
            
            # 3. Criar criativo
            creative_result = self.create_ad_creative(full_config.get("creative", {}))
            if not creative_result.get("success"):
                return creative_result
            
            creative_id = creative_result["creative_id"]
            
            # 4. Criar anúncio
            ad_result = self.create_ad(ad_set_id, creative_id, full_config.get("ad", {}))
            if not ad_result.get("success"):
                return ad_result
            
            ad_id = ad_result["ad_id"]
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "ad_set_id": ad_set_id,
                "creative_id": creative_id,
                "ad_id": ad_id,
                "message": "Campanha completa criada com sucesso!"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao criar campanha completa: {str(e)}"
            }
    
    # ===== GERENCIAMENTO DE CAMPANHAS =====
    
    def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Obter detalhes de uma campanha"""
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        endpoint = f"{campaign_id}"
        params = {"fields": "id,name,objective,status,created_time,updated_time"}
        result = self._make_request("GET", endpoint, params=params)
        
        return result
    
    def update_campaign_status(self, campaign_id: str, status: str) -> Dict[str, Any]:
        """
        Atualizar status de uma campanha
        
        Args:
            campaign_id: ID da campanha
            status: Novo status (ACTIVE, PAUSED, DELETED)
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        endpoint = f"{campaign_id}"
        data = {"status": status}
        result = self._make_request("POST", endpoint, data=data)
        
        if result.get("success"):
            return {
                "success": True,
                "message": f"Status da campanha atualizado para {status}"
            }
        else:
            return result
    
    def get_campaign_insights(self, campaign_id: str, date_preset: str = "last_7d") -> Dict[str, Any]:
        """
        Obter insights (métricas) de uma campanha
        
        Args:
            campaign_id: ID da campanha
            date_preset: Período (today, yesterday, last_7d, last_30d, etc.)
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        endpoint = f"{campaign_id}/insights"
        params = {
            "date_preset": date_preset,
            "fields": "impressions,clicks,spend,ctr,cpc,cpm,reach,frequency,conversions,cost_per_conversion"
        }
        result = self._make_request("GET", endpoint, params=params)
        
        if result.get("success"):
            insights = result["data"].get("data", [])
            if insights:
                return {
                    "success": True,
                    "insights": insights[0],
                    "period": date_preset
                }
            else:
                return {
                    "success": True,
                    "insights": {},
                    "message": "Nenhum dado disponível para o período"
                }
        else:
            return result
    
    # ===== UPLOAD DE IMAGENS =====
    
    def upload_image(self, image_path: str, image_name: str = None) -> Dict[str, Any]:
        """
        Fazer upload de imagem para usar em anúncios
        
        Args:
            image_path: Caminho local da imagem
            image_name: Nome da imagem (opcional)
        
        Returns:
            Resultado com image_hash
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        try:
            # Ler arquivo de imagem
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                
                # Fazer upload
                url = f"{self.base_url}/act_{self.ad_account_id}/adimages"
                params = {"access_token": self.access_token}
                
                if image_name:
                    params["name"] = image_name
                
                response = requests.post(url, files=files, params=params)
                response.raise_for_status()
                
                data = response.json()
                images = data.get("images", {})
                
                if images:
                    # Pegar primeiro hash
                    image_hash = list(images.values())[0].get("hash")
                    return {
                        "success": True,
                        "image_hash": image_hash,
                        "message": "Imagem enviada com sucesso"
                    }
                else:
                    return {
                        "success": False,
                        "error": "Nenhuma imagem retornada"
                    }
        
        except FileNotFoundError:
            return {"success": False, "error": f"Arquivo não encontrado: {image_path}"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Erro no upload: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Erro: {str(e)}"}
    
    # ===== PIXEL DO FACEBOOK =====
    
    def get_pixel_stats(self, pixel_id: str = None) -> Dict[str, Any]:
        """
        Obter estatísticas do Pixel do Facebook
        
        Args:
            pixel_id: ID do pixel (usa o configurado se não fornecido)
        """
        if not self.is_configured():
            return {"success": False, "error": "Meta Ads não configurado"}
        
        pixel_id = pixel_id or self.pixel_id
        
        if not pixel_id:
            return {"success": False, "error": "Pixel ID não configurado"}
        
        endpoint = f"{pixel_id}"
        params = {"fields": "id,name,code,is_unavailable,last_fired_time"}
        result = self._make_request("GET", endpoint, params=params)
        
        return result


# Instância global do serviço
meta_ads_service = MetaAdsService()


# Funções de conveniência
def create_meta_campaign(config: Dict[str, Any]) -> Dict[str, Any]:
    """Criar campanha completa no Meta Ads"""
    return meta_ads_service.create_complete_campaign(config)


def get_campaign_performance(campaign_id: str) -> Dict[str, Any]:
    """Obter performance de uma campanha"""
    return meta_ads_service.get_campaign_insights(campaign_id)


def update_campaign_status(campaign_id: str, status: str) -> Dict[str, Any]:
    """Atualizar status de campanha"""
    return meta_ads_service.update_campaign_status(campaign_id, status)

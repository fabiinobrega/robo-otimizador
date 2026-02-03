"""
Velyra Campaign Creator - Criação Automática de Campanhas
Integra Velyra Prime com Google Ads, Meta Ads e ClickBank
Autor: Manus AI Agent
Data: 03/02/2026
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# Importar serviços
try:
    from services.google_ads_service import google_ads_service, create_complete_search_campaign
    GOOGLE_ADS_AVAILABLE = True
except ImportError:
    GOOGLE_ADS_AVAILABLE = False
    google_ads_service = None

try:
    from services.facebook_ads_service_complete import facebook_ads_service
    META_ADS_AVAILABLE = True
except ImportError:
    META_ADS_AVAILABLE = False
    facebook_ads_service = None

try:
    from services.clickbank_service import clickbank_service
    CLICKBANK_AVAILABLE = True
except ImportError:
    CLICKBANK_AVAILABLE = False
    clickbank_service = None

try:
    from services.velyra_training_system import velyra_training
    VELYRA_AVAILABLE = True
except ImportError:
    VELYRA_AVAILABLE = False
    velyra_training = None


class VelyraCampaignCreator:
    """
    Criador Automático de Campanhas pela Velyra Prime
    
    Permite que a Velyra Prime crie campanhas completas via chat,
    integrando com Google Ads, Meta Ads e ClickBank.
    """
    
    def __init__(self):
        """Inicializar criador de campanhas"""
        self.google_ads = google_ads_service
        self.meta_ads = facebook_ads_service
        self.clickbank = clickbank_service
        self.velyra = velyra_training
    
    def check_permissions(self) -> Dict[str, Any]:
        """
        Verificar se Velyra tem permissão para criar campanhas
        
        Returns:
            Status de permissão
        """
        if not VELYRA_AVAILABLE or not self.velyra:
            return {
                "allowed": False,
                "message": "Sistema de treinamento Velyra não disponível"
            }
        
        return self.velyra.check_execution_permission()
    
    def create_google_ads_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar campanha Google Ads via Velyra
        
        Args:
            campaign_config: Configuração da campanha
                - name: Nome da campanha
                - budget: Orçamento diário
                - keywords: Lista de palavras-chave
                - ad: Dados do anúncio (headlines, descriptions, url)
        
        Returns:
            Resultado da criação
        """
        # Verificar permissão
        permission = self.check_permissions()
        if not permission.get("allowed"):
            return {
                "success": False,
                "error": "Velyra não autorizada",
                "message": permission.get("message")
            }
        
        # Verificar se Google Ads está disponível
        if not GOOGLE_ADS_AVAILABLE or not self.google_ads:
            return {
                "success": False,
                "error": "Google Ads não disponível",
                "message": "Serviço Google Ads não está configurado"
            }
        
        # Verificar se está configurado
        if not self.google_ads.is_configured():
            return {
                "success": False,
                "error": "Google Ads não configurado",
                "message": "Configure as credenciais do Google Ads"
            }
        
        try:
            # Criar campanha completa
            result = create_complete_search_campaign(campaign_config)
            
            if result.get("success"):
                # Registrar aprendizado da Velyra
                if VELYRA_AVAILABLE and self.velyra:
                    self.velyra.record_learning(
                        campaign_id=result.get("campaign_id"),
                        metrics={"platform": "google_ads", "created_at": datetime.now().isoformat()},
                        insights=["Campanha Google Ads criada com sucesso via Velyra Prime"]
                    )
            
            return result
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao criar campanha: {str(e)}"
            }
    
    def create_meta_ads_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar campanha Meta Ads (Facebook/Instagram) via Velyra
        
        Args:
            campaign_config: Configuração da campanha
        
        Returns:
            Resultado da criação
        """
        # Verificar permissão
        permission = self.check_permissions()
        if not permission.get("allowed"):
            return {
                "success": False,
                "error": "Velyra não autorizada",
                "message": permission.get("message")
            }
        
        # Verificar se Meta Ads está disponível
        if not META_ADS_AVAILABLE or not self.meta_ads:
            return {
                "success": False,
                "error": "Meta Ads não disponível",
                "message": "Serviço Meta Ads não está configurado"
            }
        
        try:
            # Criar campanha (implementar quando Meta Ads service estiver pronto)
            return {
                "success": False,
                "error": "Funcionalidade em desenvolvimento",
                "message": "Criação de campanhas Meta Ads será implementada em breve"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao criar campanha: {str(e)}"
            }
    
    def create_synadentix_campaign(self, platform: str = "google_ads", budget: float = 100.0) -> Dict[str, Any]:
        """
        Criar campanha Synadentix completa
        
        Args:
            platform: Plataforma (google_ads ou meta_ads)
            budget: Orçamento em R$
        
        Returns:
            Resultado da criação
        """
        # Verificar permissão
        permission = self.check_permissions()
        if not permission.get("allowed"):
            return {
                "success": False,
                "error": "Velyra não autorizada",
                "message": permission.get("message")
            }
        
        if platform == "google_ads":
            # Configuração da campanha Synadentix para Google Ads
            campaign_config = {
                "name": "Synadentix - Google Ads Search",
                "channel_type": "SEARCH",
                "daily_budget": budget / 3,  # Dividir por 3 dias
                "keywords": [
                    {"text": "buy dental supplement", "match_type": "PHRASE"},
                    {"text": "best oral health supplement", "match_type": "PHRASE"},
                    {"text": "gum disease supplement", "match_type": "PHRASE"},
                    {"text": "tooth decay supplement", "match_type": "PHRASE"},
                    {"text": "natural teeth strengthening supplement", "match_type": "PHRASE"}
                ],
                "ad_group": {
                    "name": "Synadentix - High Intent Keywords",
                    "cpc_bid": 0.60  # $0.60 CPC
                },
                "ad": {
                    "headlines": [
                        "Stop Tooth Decay Naturally",
                        "NASA-Grade Dental Formula",
                        "90-Day Money-Back Guarantee"
                    ],
                    "descriptions": [
                        "Rebuild teeth & gums naturally. Clinically proven ingredients. Order now!",
                        "Join 127,000+ customers. Free shipping. Made in USA. FDA-approved facility."
                    ],
                    "final_url": f"https://synadentix-official.shop"
                }
            }
            
            result = self.create_google_ads_campaign(campaign_config)
            
            # Adicionar link ClickBank se disponível
            if result.get("success") and CLICKBANK_AVAILABLE and self.clickbank:
                campaign_id = result.get("campaign_id")
                clickbank_link = self.clickbank.generate_affiliate_link("synadentix", f"camp_{campaign_id}")
                result["clickbank_link"] = clickbank_link
                result["affiliate_id"] = "fabiinobre"
            
            return result
        
        elif platform == "meta_ads":
            return {
                "success": False,
                "error": "Meta Ads em desenvolvimento",
                "message": "Use Google Ads por enquanto"
            }
        
        else:
            return {
                "success": False,
                "error": "Plataforma inválida",
                "message": f"Plataforma '{platform}' não suportada. Use 'google_ads' ou 'meta_ads'."
            }
    
    def get_campaign_status(self, campaign_id: int, platform: str = "google_ads") -> Dict[str, Any]:
        """
        Obter status de uma campanha
        
        Args:
            campaign_id: ID da campanha
            platform: Plataforma
        
        Returns:
            Status da campanha
        """
        if platform == "google_ads":
            if not GOOGLE_ADS_AVAILABLE or not self.google_ads:
                return {"success": False, "error": "Google Ads não disponível"}
            
            return self.google_ads.get_campaign_performance(campaign_id)
        
        elif platform == "meta_ads":
            return {"success": False, "error": "Meta Ads em desenvolvimento"}
        
        else:
            return {"success": False, "error": "Plataforma inválida"}
    
    def get_available_platforms(self) -> Dict[str, bool]:
        """
        Verificar quais plataformas estão disponíveis
        
        Returns:
            Status de cada plataforma
        """
        return {
            "google_ads": GOOGLE_ADS_AVAILABLE and (self.google_ads.is_configured() if self.google_ads else False),
            "meta_ads": META_ADS_AVAILABLE and (self.meta_ads is not None),
            "clickbank": CLICKBANK_AVAILABLE and (self.clickbank is not None),
            "velyra_authorized": self.check_permissions().get("allowed", False)
        }


# Instância global do criador de campanhas
velyra_campaign_creator = VelyraCampaignCreator()


# Funções de conveniência para uso nas APIs
def create_campaign_via_velyra(platform: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Criar campanha via Velyra Prime"""
    creator = velyra_campaign_creator
    
    if platform == "google_ads":
        return creator.create_google_ads_campaign(config)
    elif platform == "meta_ads":
        return creator.create_meta_ads_campaign(config)
    else:
        return {"success": False, "error": f"Plataforma '{platform}' não suportada"}


def create_synadentix_campaign(platform: str = "google_ads", budget: float = 100.0) -> Dict[str, Any]:
    """Criar campanha Synadentix completa"""
    return velyra_campaign_creator.create_synadentix_campaign(platform, budget)


def check_velyra_status() -> Dict[str, Any]:
    """Verificar status da Velyra e plataformas disponíveis"""
    creator = velyra_campaign_creator
    platforms = creator.get_available_platforms()
    permission = creator.check_permissions()
    
    return {
        "velyra_authorized": permission.get("allowed", False),
        "velyra_status": permission.get("message", ""),
        "platforms": platforms
    }

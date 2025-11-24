"""
Google Ads Service - Integração Completa
Sistema de Otimização de Vendas Avançado
Autor: Manus AI Agent
Data: 24/11/2024
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    GOOGLE_ADS_SDK_AVAILABLE = True
except ImportError:
    GOOGLE_ADS_SDK_AVAILABLE = False
    print("Warning: Google Ads SDK not installed. Run: pip install google-ads")


class GoogleAdsService:
    """Serviço completo de integração com Google Ads API"""
    
    def __init__(self):
        """Inicializar serviço com credenciais"""
        self.developer_token = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")
        self.client_id = os.environ.get("GOOGLE_ADS_CLIENT_ID", "")
        self.client_secret = os.environ.get("GOOGLE_ADS_CLIENT_SECRET", "")
        self.refresh_token = os.environ.get("GOOGLE_ADS_REFRESH_TOKEN", "")
        self.customer_id = os.environ.get("GOOGLE_ADS_CUSTOMER_ID", "")
        self.login_customer_id = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "")
        
        self.client = None
        
        if GOOGLE_ADS_SDK_AVAILABLE and self.developer_token:
            self._initialize_client()
    
    def _initialize_client(self):
        """Inicializar Google Ads Client"""
        try:
            # Criar configuração
            config = {
                "developer_token": self.developer_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "login_customer_id": self.login_customer_id,
                "use_proto_plus": True,
            }
            
            self.client = GoogleAdsClient.load_from_dict(config)
            print("✅ Google Ads API inicializada com sucesso")
        except Exception as e:
            print(f"❌ Erro ao inicializar Google Ads API: {e}")
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return bool(
            self.developer_token and 
            self.client_id and 
            self.client_secret and 
            self.refresh_token and 
            self.customer_id and 
            GOOGLE_ADS_SDK_AVAILABLE
        )
    
    # ===== CAMPANHAS =====
    
    def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar campanha no Google Ads"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            campaign_service = self.client.get_service("CampaignService")
            campaign_operation = self.client.get_type("CampaignOperation")
            
            campaign = campaign_operation.create
            campaign.name = campaign_data.get("name")
            campaign.status = self.client.enums.CampaignStatusEnum.PAUSED
            
            # Configurar tipo e objetivo
            advertising_channel_type = campaign_data.get("channel_type", "SEARCH")
            if advertising_channel_type == "SEARCH":
                campaign.advertising_channel_type = self.client.enums.AdvertisingChannelTypeEnum.SEARCH
            elif advertising_channel_type == "DISPLAY":
                campaign.advertising_channel_type = self.client.enums.AdvertisingChannelTypeEnum.DISPLAY
            elif advertising_channel_type == "VIDEO":
                campaign.advertising_channel_type = self.client.enums.AdvertisingChannelTypeEnum.VIDEO
            
            # Configurar orçamento
            campaign.campaign_budget = self._create_budget(campaign_data.get("daily_budget", 50.0))
            
            # Configurar estratégia de lance
            campaign.manual_cpc.enhanced_cpc_enabled = True
            
            # Datas de início e fim
            start_date = campaign_data.get("start_date", datetime.now().strftime("%Y%m%d"))
            campaign.start_date = start_date
            
            if campaign_data.get("end_date"):
                campaign.end_date = campaign_data["end_date"]
            
            # Criar campanha
            response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            
            campaign_resource_name = response.results[0].resource_name
            campaign_id = campaign_resource_name.split("/")[-1]
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "resource_name": campaign_resource_name,
                "message": "Campanha criada com sucesso"
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar campanha: {str(e)}"}
    
    def _create_budget(self, daily_amount: float) -> str:
        """Criar orçamento de campanha"""
        try:
            budget_service = self.client.get_service("CampaignBudgetService")
            budget_operation = self.client.get_type("CampaignBudgetOperation")
            
            budget = budget_operation.create
            budget.name = f"Budget {datetime.now().strftime('%Y%m%d%H%M%S')}"
            budget.amount_micros = int(daily_amount * 1_000_000)  # converter para micros
            budget.delivery_method = self.client.enums.BudgetDeliveryMethodEnum.STANDARD
            
            response = budget_service.mutate_campaign_budgets(
                customer_id=self.customer_id,
                operations=[budget_operation]
            )
            
            return response.results[0].resource_name
        except Exception as e:
            raise Exception(f"Erro ao criar orçamento: {str(e)}")
    
    def create_ad_group(self, campaign_id: str, ad_group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar grupo de anúncios"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            ad_group_service = self.client.get_service("AdGroupService")
            ad_group_operation = self.client.get_type("AdGroupOperation")
            
            ad_group = ad_group_operation.create
            ad_group.name = ad_group_data.get("name")
            ad_group.campaign = f"customers/{self.customer_id}/campaigns/{campaign_id}"
            ad_group.status = self.client.enums.AdGroupStatusEnum.ENABLED
            ad_group.type_ = self.client.enums.AdGroupTypeEnum.SEARCH_STANDARD
            
            # Configurar lance
            ad_group.cpc_bid_micros = int(ad_group_data.get("cpc_bid", 1.0) * 1_000_000)
            
            # Criar grupo de anúncios
            response = ad_group_service.mutate_ad_groups(
                customer_id=self.customer_id,
                operations=[ad_group_operation]
            )
            
            ad_group_resource_name = response.results[0].resource_name
            ad_group_id = ad_group_resource_name.split("/")[-1]
            
            return {
                "success": True,
                "ad_group_id": ad_group_id,
                "resource_name": ad_group_resource_name,
                "message": "Grupo de anúncios criado com sucesso"
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar grupo de anúncios: {str(e)}"}
    
    def create_text_ad(self, ad_group_id: str, ad_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar anúncio de texto responsivo"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            ad_group_ad_service = self.client.get_service("AdGroupAdService")
            ad_group_ad_operation = self.client.get_type("AdGroupAdOperation")
            
            ad_group_ad = ad_group_ad_operation.create
            ad_group_ad.ad_group = f"customers/{self.customer_id}/adGroups/{ad_group_id}"
            ad_group_ad.status = self.client.enums.AdGroupAdStatusEnum.PAUSED
            
            # Criar anúncio de texto responsivo
            ad = ad_group_ad.ad
            ad.final_urls.append(ad_data.get("final_url"))
            
            # Headlines (mínimo 3, máximo 15)
            headlines = ad_data.get("headlines", [])
            for headline in headlines[:15]:
                headline_asset = self.client.get_type("AdTextAsset")
                headline_asset.text = headline
                ad.responsive_search_ad.headlines.append(headline_asset)
            
            # Descriptions (mínimo 2, máximo 4)
            descriptions = ad_data.get("descriptions", [])
            for description in descriptions[:4]:
                description_asset = self.client.get_type("AdTextAsset")
                description_asset.text = description
                ad.responsive_search_ad.descriptions.append(description_asset)
            
            # Path (opcional)
            if ad_data.get("path1"):
                ad.responsive_search_ad.path1 = ad_data["path1"]
            if ad_data.get("path2"):
                ad.responsive_search_ad.path2 = ad_data["path2"]
            
            # Criar anúncio
            response = ad_group_ad_service.mutate_ad_group_ads(
                customer_id=self.customer_id,
                operations=[ad_group_ad_operation]
            )
            
            ad_resource_name = response.results[0].resource_name
            
            return {
                "success": True,
                "ad_resource_name": ad_resource_name,
                "message": "Anúncio criado com sucesso"
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar anúncio: {str(e)}"}
    
    def add_keywords(self, ad_group_id: str, keywords: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Adicionar palavras-chave ao grupo de anúncios"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            ad_group_criterion_service = self.client.get_service("AdGroupCriterionService")
            operations = []
            
            for keyword_data in keywords:
                operation = self.client.get_type("AdGroupCriterionOperation")
                criterion = operation.create
                
                criterion.ad_group = f"customers/{self.customer_id}/adGroups/{ad_group_id}"
                criterion.status = self.client.enums.AdGroupCriterionStatusEnum.ENABLED
                criterion.keyword.text = keyword_data.get("text")
                
                # Tipo de correspondência
                match_type = keyword_data.get("match_type", "BROAD")
                if match_type == "EXACT":
                    criterion.keyword.match_type = self.client.enums.KeywordMatchTypeEnum.EXACT
                elif match_type == "PHRASE":
                    criterion.keyword.match_type = self.client.enums.KeywordMatchTypeEnum.PHRASE
                else:
                    criterion.keyword.match_type = self.client.enums.KeywordMatchTypeEnum.BROAD
                
                # Lance personalizado (opcional)
                if keyword_data.get("cpc_bid"):
                    criterion.cpc_bid_micros = int(keyword_data["cpc_bid"] * 1_000_000)
                
                operations.append(operation)
            
            # Adicionar palavras-chave
            response = ad_group_criterion_service.mutate_ad_group_criteria(
                customer_id=self.customer_id,
                operations=operations
            )
            
            return {
                "success": True,
                "keywords_added": len(response.results),
                "message": f"{len(response.results)} palavras-chave adicionadas"
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao adicionar palavras-chave: {str(e)}"}
    
    # ===== GERENCIAMENTO =====
    
    def update_campaign_status(self, campaign_id: str, status: str) -> Dict[str, Any]:
        """Atualizar status da campanha"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            campaign_service = self.client.get_service("CampaignService")
            campaign_operation = self.client.get_type("CampaignOperation")
            
            campaign = campaign_operation.update
            campaign.resource_name = f"customers/{self.customer_id}/campaigns/{campaign_id}"
            
            # Mapear status
            status_map = {
                "enabled": self.client.enums.CampaignStatusEnum.ENABLED,
                "paused": self.client.enums.CampaignStatusEnum.PAUSED,
                "removed": self.client.enums.CampaignStatusEnum.REMOVED,
            }
            
            campaign.status = status_map.get(status, self.client.enums.CampaignStatusEnum.PAUSED)
            
            # Especificar campos a atualizar
            field_mask = self.client.get_type("FieldMask")
            field_mask.paths.append("status")
            campaign_operation.update_mask.CopyFrom(field_mask)
            
            # Atualizar campanha
            response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            
            return {
                "success": True,
                "message": f"Status da campanha atualizado para {status}"
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao atualizar status: {str(e)}"}
    
    def update_budget(self, campaign_id: str, daily_budget: float) -> Dict[str, Any]:
        """Atualizar orçamento diário da campanha"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            # Primeiro, obter o budget resource name da campanha
            query = f"""
                SELECT campaign.campaign_budget
                FROM campaign
                WHERE campaign.id = {campaign_id}
            """
            
            ga_service = self.client.get_service("GoogleAdsService")
            response = ga_service.search(customer_id=self.customer_id, query=query)
            
            budget_resource_name = None
            for row in response:
                budget_resource_name = row.campaign.campaign_budget
                break
            
            if not budget_resource_name:
                return {"success": False, "message": "Orçamento não encontrado"}
            
            # Atualizar orçamento
            budget_service = self.client.get_service("CampaignBudgetService")
            budget_operation = self.client.get_type("CampaignBudgetOperation")
            
            budget = budget_operation.update
            budget.resource_name = budget_resource_name
            budget.amount_micros = int(daily_budget * 1_000_000)
            
            field_mask = self.client.get_type("FieldMask")
            field_mask.paths.append("amount_micros")
            budget_operation.update_mask.CopyFrom(field_mask)
            
            budget_service.mutate_campaign_budgets(
                customer_id=self.customer_id,
                operations=[budget_operation]
            )
            
            return {
                "success": True,
                "message": f"Orçamento atualizado para R$ {daily_budget:.2f}/dia"
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao atualizar orçamento: {str(e)}"}
    
    # ===== MÉTRICAS =====
    
    def get_campaign_metrics(self, campaign_id: str, days: int = 30) -> Dict[str, Any]:
        """Obter métricas da campanha"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            # Calcular período
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            query = f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.conversions,
                    metrics.cost_micros,
                    metrics.conversions_value,
                    metrics.ctr,
                    metrics.average_cpc,
                    metrics.average_cpm
                FROM campaign
                WHERE campaign.id = {campaign_id}
                AND segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' 
                AND '{end_date.strftime('%Y-%m-%d')}'
            """
            
            ga_service = self.client.get_service("GoogleAdsService")
            response = ga_service.search(customer_id=self.customer_id, query=query)
            
            # Agregar métricas
            total_impressions = 0
            total_clicks = 0
            total_conversions = 0
            total_cost = 0
            total_revenue = 0
            
            for row in response:
                total_impressions += row.metrics.impressions
                total_clicks += row.metrics.clicks
                total_conversions += row.metrics.conversions
                total_cost += row.metrics.cost_micros / 1_000_000
                total_revenue += row.metrics.conversions_value
            
            # Calcular métricas derivadas
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
            cpa = (total_cost / total_conversions) if total_conversions > 0 else 0
            roas = (total_revenue / total_cost) if total_cost > 0 else 0
            
            return {
                "success": True,
                "metrics": {
                    "impressions": int(total_impressions),
                    "clicks": int(total_clicks),
                    "conversions": int(total_conversions),
                    "spend": round(total_cost, 2),
                    "revenue": round(total_revenue, 2),
                    "ctr": round(ctr, 2),
                    "cpc": round(cpc, 2),
                    "cpa": round(cpa, 2),
                    "roas": round(roas, 2),
                }
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao obter métricas: {str(e)}"}
    
    def get_all_campaigns(self) -> Dict[str, Any]:
        """Listar todas as campanhas"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            query = """
                SELECT
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    campaign.advertising_channel_type
                FROM campaign
                WHERE campaign.status != 'REMOVED'
                ORDER BY campaign.name
            """
            
            ga_service = self.client.get_service("GoogleAdsService")
            response = ga_service.search(customer_id=self.customer_id, query=query)
            
            campaigns_list = []
            for row in response:
                campaigns_list.append({
                    "id": row.campaign.id,
                    "name": row.campaign.name,
                    "status": row.campaign.status.name,
                    "type": row.campaign.advertising_channel_type.name,
                })
            
            return {
                "success": True,
                "campaigns": campaigns_list,
                "total": len(campaigns_list)
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar campanhas: {str(e)}"}
    
    # ===== OTIMIZAÇÃO =====
    
    def optimize_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Otimizar campanha baseado em performance"""
        if not self.is_configured():
            return {"success": False, "message": "Google Ads não configurado"}
        
        try:
            # Obter métricas dos últimos 7 dias
            metrics_result = self.get_campaign_metrics(campaign_id, 7)
            
            if not metrics_result["success"]:
                return metrics_result
            
            metrics = metrics_result["metrics"]
            actions = []
            
            # Regra 1: ROAS muito baixo - pausar campanha
            if metrics["roas"] < 1.0 and metrics["spend"] > 50:
                self.update_campaign_status(campaign_id, "paused")
                actions.append("Campanha pausada (ROAS < 1.0)")
            
            # Regra 2: ROAS alto - aumentar orçamento
            elif metrics["roas"] > 3.0:
                # Obter orçamento atual
                query = f"""
                    SELECT campaign.campaign_budget
                    FROM campaign
                    WHERE campaign.id = {campaign_id}
                """
                
                ga_service = self.client.get_service("GoogleAdsService")
                response = ga_service.search(customer_id=self.customer_id, query=query)
                
                for row in response:
                    # Aumentar orçamento em 15%
                    current_budget = metrics["spend"] / 7  # média diária
                    new_budget = current_budget * 1.15
                    self.update_budget(campaign_id, new_budget)
                    actions.append(f"Orçamento aumentado em 15% (ROAS > 3.0)")
                    break
            
            # Regra 3: CTR muito baixo - sugerir novas palavras-chave
            if metrics["ctr"] < 1.0:
                actions.append("CTR baixo - considere adicionar novas palavras-chave")
            
            # Regra 4: CPA muito alto - reduzir orçamento
            if metrics["cpa"] > 100:
                current_budget = metrics["spend"] / 7
                new_budget = current_budget * 0.85  # -15%
                self.update_budget(campaign_id, new_budget)
                actions.append(f"Orçamento reduzido em 15% (CPA > R$ 100)")
            
            return {
                "success": True,
                "actions": actions,
                "metrics": metrics
            }
        
        except GoogleAdsException as e:
            return {"success": False, "message": f"Erro Google Ads: {e.error.message}"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao otimizar campanha: {str(e)}"}


# Instância global do serviço
google_ads_service = GoogleAdsService()


# Função helper para uso fácil
def create_complete_search_campaign(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """Criar campanha de pesquisa completa"""
    service = google_ads_service
    
    if not service.is_configured():
        return {"success": False, "message": "Google Ads não configurado. Configure as variáveis de ambiente."}
    
    try:
        # 1. Criar campanha
        campaign_result = service.create_campaign(campaign_data)
        if not campaign_result["success"]:
            return campaign_result
        
        campaign_id = campaign_result["campaign_id"]
        
        # 2. Criar grupo de anúncios
        ad_group_data = campaign_data.get("ad_group", {})
        ad_group_result = service.create_ad_group(campaign_id, ad_group_data)
        if not ad_group_result["success"]:
            return ad_group_result
        
        ad_group_id = ad_group_result["ad_group_id"]
        
        # 3. Adicionar palavras-chave
        if campaign_data.get("keywords"):
            keywords_result = service.add_keywords(ad_group_id, campaign_data["keywords"])
            if not keywords_result["success"]:
                return keywords_result
        
        # 4. Criar anúncio
        ad_data = campaign_data.get("ad", {})
        ad_result = service.create_text_ad(ad_group_id, ad_data)
        if not ad_result["success"]:
            return ad_result
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "ad_group_id": ad_group_id,
            "message": "Campanha de pesquisa criada com sucesso!"
        }
    
    except Exception as e:
        return {"success": False, "message": f"Erro ao criar campanha completa: {str(e)}"}

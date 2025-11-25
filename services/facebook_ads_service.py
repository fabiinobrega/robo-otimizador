"""
Facebook Ads Service - Integração Completa
Sistema de Otimização de Vendas Avançado
Autor: Manus AI Agent
Data: 24/11/2024
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

try:
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.ad import Ad
    from facebook_business.adobjects.adcreative import AdCreative
    from facebook_business.adobjects.adimage import AdImage
    FACEBOOK_SDK_AVAILABLE = True
except ImportError:
    FACEBOOK_SDK_AVAILABLE = False
    print("Warning: Facebook Business SDK not installed. Run: pip install facebook-business")


class FacebookAdsService:
    """Serviço completo de integração com Facebook Marketing API"""
    
    def __init__(self):
        """Inicializar serviço com credenciais"""
        self.app_id = os.environ.get("FACEBOOK_APP_ID", "")
        self.app_secret = os.environ.get("FACEBOOK_APP_SECRET", "")
        self.access_token = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")
        self.ad_account_id = os.environ.get("FACEBOOK_AD_ACCOUNT_ID", "")
        
        self.api = None
        self.ad_account = None
        
        if FACEBOOK_SDK_AVAILABLE and self.access_token:
            self._initialize_api()
    
    def _initialize_api(self):
        """Inicializar Facebook Ads API"""
        try:
            FacebookAdsApi.init(
                app_id=self.app_id,
                app_secret=self.app_secret,
                access_token=self.access_token
            )
            self.api = FacebookAdsApi.get_default_api()
            self.ad_account = AdAccount(f"act_{self.ad_account_id}")
            print("✅ Facebook Ads API inicializada com sucesso")
        except Exception as e:
            print(f"❌ Erro ao inicializar Facebook Ads API: {e}")
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return bool(self.access_token and self.ad_account_id and FACEBOOK_SDK_AVAILABLE)
    
    # ===== CAMPANHAS =====
    
    def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar campanha no Facebook Ads"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            campaign = Campaign(parent_id=self.ad_account.get_id_assured())
            
            # Mapear objetivo
            objective_map = {
                "conversions": Campaign.Objective.conversions,
                "traffic": Campaign.Objective.link_clicks,
                "awareness": Campaign.Objective.brand_awareness,
                "engagement": Campaign.Objective.post_engagement,
                "leads": Campaign.Objective.lead_generation,
            }
            
            objective = objective_map.get(campaign_data.get("objective", "conversions"))
            
            # Criar campanha
            campaign.update({
                Campaign.Field.name: campaign_data.get("name"),
                Campaign.Field.objective: objective,
                Campaign.Field.status: Campaign.Status.paused,  # Criar pausada
                Campaign.Field.special_ad_categories: [],
            })
            
            campaign.remote_create()
            
            return {
                "success": True,
                "campaign_id": campaign.get_id(),
                "message": "Campanha criada com sucesso"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar campanha: {str(e)}"}
    
    def create_adset(self, campaign_id: str, adset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar conjunto de anúncios"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            adset = AdSet(parent_id=self.ad_account.get_id_assured())
            
            # Configurar targeting
            targeting = {
                "geo_locations": {
                    "countries": [adset_data.get("country", "BR")]
                },
                "age_min": adset_data.get("min_age", 18),
                "age_max": adset_data.get("max_age", 65),
            }
            
            # Adicionar interesses se fornecidos
            if adset_data.get("interests"):
                targeting["interests"] = adset_data["interests"]
            
            # Criar adset
            adset.update({
                AdSet.Field.name: adset_data.get("name"),
                AdSet.Field.campaign_id: campaign_id,
                AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
                AdSet.Field.optimization_goal: AdSet.OptimizationGoal.link_clicks,
                AdSet.Field.bid_amount: int(adset_data.get("bid_amount", 100)),  # centavos
                AdSet.Field.daily_budget: int(adset_data.get("daily_budget", 1000)),  # centavos
                AdSet.Field.targeting: targeting,
                AdSet.Field.status: AdSet.Status.paused,
            })
            
            adset.remote_create()
            
            return {
                "success": True,
                "adset_id": adset.get_id(),
                "message": "Conjunto de anúncios criado com sucesso"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar adset: {str(e)}"}
    
    def create_ad_creative(self, creative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar criativo de anúncio"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            creative = AdCreative(parent_id=self.ad_account.get_id_assured())
            
            # Configurar objeto de link
            object_story_spec = {
                "page_id": creative_data.get("page_id"),
                "link_data": {
                    "message": creative_data.get("message"),
                    "link": creative_data.get("link"),
                    "caption": creative_data.get("caption", ""),
                    "name": creative_data.get("headline"),
                    "description": creative_data.get("description"),
                    "call_to_action": {
                        "type": creative_data.get("cta_type", "LEARN_MORE")
                    }
                }
            }
            
            # Adicionar imagem se fornecida
            if creative_data.get("image_hash"):
                object_story_spec["link_data"]["image_hash"] = creative_data["image_hash"]
            
            creative.update({
                AdCreative.Field.name: creative_data.get("name"),
                AdCreative.Field.object_story_spec: object_story_spec,
            })
            
            creative.remote_create()
            
            return {
                "success": True,
                "creative_id": creative.get_id(),
                "message": "Criativo criado com sucesso"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar criativo: {str(e)}"}
    
    def create_ad(self, adset_id: str, creative_id: str, ad_name: str) -> Dict[str, Any]:
        """Criar anúncio"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            ad = Ad(parent_id=self.ad_account.get_id_assured())
            
            ad.update({
                Ad.Field.name: ad_name,
                Ad.Field.adset_id: adset_id,
                Ad.Field.creative: {"creative_id": creative_id},
                Ad.Field.status: Ad.Status.paused,
            })
            
            ad.remote_create()
            
            return {
                "success": True,
                "ad_id": ad.get_id(),
                "message": "Anúncio criado com sucesso"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao criar anúncio: {str(e)}"}
    
    def upload_image(self, image_path: str) -> Dict[str, Any]:
        """Fazer upload de imagem"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            image = AdImage(parent_id=self.ad_account.get_id_assured())
            image[AdImage.Field.filename] = image_path
            image.remote_create()
            
            return {
                "success": True,
                "image_hash": image[AdImage.Field.hash],
                "message": "Imagem enviada com sucesso"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao enviar imagem: {str(e)}"}
    
    # ===== GERENCIAMENTO =====
    
    def update_campaign_status(self, campaign_id: str, status: str) -> Dict[str, Any]:
        """Atualizar status da campanha"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            campaign = Campaign(campaign_id)
            
            status_map = {
                "active": Campaign.Status.active,
                "paused": Campaign.Status.paused,
                "deleted": Campaign.Status.deleted,
            }
            
            campaign.update({
                Campaign.Field.status: status_map.get(status, Campaign.Status.paused)
            })
            
            campaign.remote_update()
            
            return {
                "success": True,
                "message": f"Status da campanha atualizado para {status}"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao atualizar status: {str(e)}"}
    
    def update_budget(self, adset_id: str, daily_budget: float) -> Dict[str, Any]:
        """Atualizar orçamento diário"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            adset = AdSet(adset_id)
            adset.update({
                AdSet.Field.daily_budget: int(daily_budget * 100)  # converter para centavos
            })
            adset.remote_update()
            
            return {
                "success": True,
                "message": f"Orçamento atualizado para R$ {daily_budget:.2f}/dia"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao atualizar orçamento: {str(e)}"}
    
    # ===== MÉTRICAS =====
    
    def get_campaign_insights(self, campaign_id: str, date_preset: str = "last_30d") -> Dict[str, Any]:
        """Obter métricas da campanha"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            campaign = Campaign(campaign_id)
            
            insights = campaign.get_insights(
                fields=[
                    'impressions',
                    'clicks',
                    'spend',
                    'actions',
                    'action_values',
                    'ctr',
                    'cpc',
                    'cpp',
                    'cpm',
                ],
                params={
                    'date_preset': date_preset,
                }
            )
            
            if not insights:
                return {"success": False, "message": "Nenhuma métrica disponível"}
            
            insight = insights[0]
            
            # Processar ações (conversões)
            conversions = 0
            revenue = 0.0
            
            if 'actions' in insight:
                for action in insight['actions']:
                    if action['action_type'] == 'purchase':
                        conversions = int(action['value'])
            
            if 'action_values' in insight:
                for action_value in insight['action_values']:
                    if action_value['action_type'] == 'purchase':
                        revenue = float(action_value['value'])
            
            # Calcular métricas
            impressions = int(insight.get('impressions', 0))
            clicks = int(insight.get('clicks', 0))
            spend = float(insight.get('spend', 0))
            ctr = float(insight.get('ctr', 0))
            cpc = float(insight.get('cpc', 0))
            cpm = float(insight.get('cpm', 0))
            
            roas = (revenue / spend) if spend > 0 else 0
            cpa = (spend / conversions) if conversions > 0 else 0
            
            return {
                "success": True,
                "metrics": {
                    "impressions": impressions,
                    "clicks": clicks,
                    "conversions": conversions,
                    "spend": spend,
                    "revenue": revenue,
                    "ctr": ctr,
                    "cpc": cpc,
                    "cpm": cpm,
                    "cpa": cpa,
                    "roas": roas,
                }
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao obter métricas: {str(e)}"}
    
    def get_all_campaigns(self) -> Dict[str, Any]:
        """Listar todas as campanhas"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            campaigns = self.ad_account.get_campaigns(
                fields=[
                    Campaign.Field.id,
                    Campaign.Field.name,
                    Campaign.Field.status,
                    Campaign.Field.objective,
                    Campaign.Field.created_time,
                ]
            )
            
            campaigns_list = []
            for campaign in campaigns:
                campaigns_list.append({
                    "id": campaign.get_id(),
                    "name": campaign[Campaign.Field.name],
                    "status": campaign[Campaign.Field.status],
                    "objective": campaign[Campaign.Field.objective],
                    "created_at": campaign[Campaign.Field.created_time],
                })
            
            return {
                "success": True,
                "campaigns": campaigns_list,
                "total": len(campaigns_list)
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar campanhas: {str(e)}"}
    
    # ===== OTIMIZAÇÃO =====
    
    def optimize_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Otimizar campanha baseado em performance"""
        if not self.is_configured():
            return {"success": False, "message": "Facebook Ads não configurado"}
        
        try:
            # Obter métricas
            insights_result = self.get_campaign_insights(campaign_id, "last_7d")
            
            if not insights_result["success"]:
                return insights_result
            
            metrics = insights_result["metrics"]
            actions = []
            
            # Regra 1: ROAS muito baixo - pausar campanha
            if metrics["roas"] < 1.0 and metrics["spend"] > 50:
                self.update_campaign_status(campaign_id, "paused")
                actions.append("Campanha pausada (ROAS < 1.0)")
            
            # Regra 2: ROAS alto - aumentar orçamento
            elif metrics["roas"] > 3.0:
                # Obter adsets da campanha
                campaign = Campaign(campaign_id)
                adsets = campaign.get_ad_sets()
                
                for adset in adsets:
                    current_budget = float(adset.get(AdSet.Field.daily_budget, 0)) / 100
                    new_budget = current_budget * 1.15  # +15%
                    self.update_budget(adset.get_id(), new_budget)
                    actions.append(f"Orçamento aumentado em 15% (ROAS > 3.0)")
            
            # Regra 3: CTR muito baixo - sugerir novos criativos
            if metrics["ctr"] < 0.5:
                actions.append("CTR baixo - considere criar novos criativos")
            
            # Regra 4: CPA muito alto - reduzir orçamento
            if metrics["cpa"] > 100:
                campaign = Campaign(campaign_id)
                adsets = campaign.get_ad_sets()
                
                for adset in adsets:
                    current_budget = float(adset.get(AdSet.Field.daily_budget, 0)) / 100
                    new_budget = current_budget * 0.85  # -15%
                    self.update_budget(adset.get_id(), new_budget)
                    actions.append(f"Orçamento reduzido em 15% (CPA > R$ 100)")
            
            return {
                "success": True,
                "actions": actions,
                "metrics": metrics
            }
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao otimizar campanha: {str(e)}"}


# Instância global do serviço
facebook_ads_service = FacebookAdsService()


# Função helper para uso fácil
def create_complete_campaign(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """Criar campanha completa com adset, criativo e anúncio"""
    service = facebook_ads_service
    
    if not service.is_configured():
        return {"success": False, "message": "Facebook Ads não configurado. Configure as variáveis de ambiente."}
    
    try:
        # 1. Criar campanha
        campaign_result = service.create_campaign(campaign_data)
        if not campaign_result["success"]:
            return campaign_result
        
        campaign_id = campaign_result["campaign_id"]
        
        # 2. Criar adset
        adset_result = service.create_adset(campaign_id, campaign_data.get("adset", {}))
        if not adset_result["success"]:
            return adset_result
        
        adset_id = adset_result["adset_id"]
        
        # 3. Upload de imagem (se fornecida)
        image_hash = None
        if campaign_data.get("image_path"):
            image_result = service.upload_image(campaign_data["image_path"])
            if image_result["success"]:
                image_hash = image_result["image_hash"]
        
        # 4. Criar criativo
        creative_data = campaign_data.get("creative", {})
        if image_hash:
            creative_data["image_hash"] = image_hash
        
        creative_result = service.create_ad_creative(creative_data)
        if not creative_result["success"]:
            return creative_result
        
        creative_id = creative_result["creative_id"]
        
        # 5. Criar anúncio
        ad_result = service.create_ad(adset_id, creative_id, campaign_data.get("name"))
        if not ad_result["success"]:
            return ad_result
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "adset_id": adset_id,
            "creative_id": creative_id,
            "ad_id": ad_result["ad_id"],
            "message": "Campanha completa criada com sucesso!"
        }
    
    except Exception as e:
        return {"success": False, "message": f"Erro ao criar campanha completa: {str(e)}"}

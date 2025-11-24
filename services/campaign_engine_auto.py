"""
Motor de Campanhas Automáticas - NEXORA PRIME
Criação de campanhas Meta e Google com 1 clique
Nível: Agência Milionária
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class CampaignEngineAuto:
    """
    Motor automático para criação e gerenciamento de campanhas
    Cria campanhas completas com 1 clique em Meta Ads e Google Ads
    """
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        
        self.campaign_objectives = {
            "meta": {
                "awareness": "BRAND_AWARENESS",
                "traffic": "LINK_CLICKS",
                "engagement": "POST_ENGAGEMENT",
                "leads": "LEAD_GENERATION",
                "sales": "CONVERSIONS"
            },
            "google": {
                "awareness": "BRAND_AWARENESS",
                "traffic": "WEBSITE_TRAFFIC",
                "engagement": "VIDEO_VIEWS",
                "leads": "LEAD_GENERATION",
                "sales": "SALES"
            }
        }
        
        self.optimization_strategies = [
            "maximize_conversions",
            "target_cpa",
            "target_roas",
            "maximize_clicks",
            "manual_bidding"
        ]
    
    def create_campaign_one_click(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria campanha completa com 1 clique
        
        Args:
            params: Parâmetros da campanha
                - platform: str (meta ou google)
                - name: str
                - objective: str
                - budget_daily: float
                - product: str
                - audience: str
                - duration_days: int
        
        Returns:
            Dict com campanha completa criada
        """
        platform = params.get("platform", "meta")
        name = params.get("name", f"Campanha {datetime.now().strftime('%Y%m%d')}")
        objective = params.get("objective", "sales")
        budget_daily = params.get("budget_daily", 100.0)
        product = params.get("product", "produto")
        audience = params.get("audience", "público geral")
        duration_days = params.get("duration_days", 7)
        
        # Criar estrutura da campanha
        campaign = {
            "id": f"camp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            "name": name,
            "platform": platform,
            "objective": objective,
            "status": "draft",
            
            # Orçamento
            "budget": {
                "daily": budget_daily,
                "total": budget_daily * duration_days,
                "currency": "BRL"
            },
            
            # Datas
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=duration_days)).isoformat(),
            "duration_days": duration_days,
            
            # Configurações
            "settings": self._generate_campaign_settings(platform, objective, budget_daily),
            
            # Conjuntos de anúncios
            "ad_sets": self._create_ad_sets(platform, objective, audience, budget_daily),
            
            # Anúncios
            "ads": [],  # Serão criados pelo creative_intelligence
            
            # Otimização
            "optimization": self._generate_optimization_config(platform, objective, budget_daily),
            
            # Segmentação
            "targeting": self._generate_targeting(platform, audience),
            
            # Rastreamento
            "tracking": self._generate_tracking_config(platform, objective),
            
            # Métricas estimadas
            "estimated_metrics": self._calculate_estimated_metrics(
                platform, objective, budget_daily, duration_days
            ),
            
            # Status de aprovação
            "approval_status": "pending_approval",
            "requires_budget_approval": budget_daily * duration_days > 500,
            
            # Metadados
            "created_at": datetime.now().isoformat(),
            "created_by": "Nexora Campaign Engine",
            "auto_created": True
        }
        
        return campaign
    
    def create_meta_campaign_auto(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cria campanha Meta Ads automaticamente"""
        params["platform"] = "meta"
        campaign = self.create_campaign_one_click(params)
        
        # Adicionar configurações específicas do Meta
        campaign["meta_specific"] = {
            "campaign_objective": self.campaign_objectives["meta"][params.get("objective", "sales")],
            "buying_type": "AUCTION",
            "special_ad_categories": [],
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "optimization_goal": "CONVERSIONS" if params.get("objective") == "sales" else "LINK_CLICKS",
            "billing_event": "IMPRESSIONS",
            "promoted_object": {
                "pixel_id": "PIXEL_ID_HERE",
                "custom_event_type": "PURCHASE"
            }
        }
        
        return campaign
    
    def create_google_campaign_auto(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cria campanha Google Ads automaticamente"""
        params["platform"] = "google"
        campaign = self.create_campaign_one_click(params)
        
        # Adicionar configurações específicas do Google
        campaign["google_specific"] = {
            "campaign_type": "SEARCH" if params.get("objective") in ["traffic", "sales"] else "DISPLAY",
            "network_settings": {
                "target_google_search": True,
                "target_search_network": True,
                "target_content_network": False,
                "target_partner_search_network": False
            },
            "bidding_strategy_type": "TARGET_CPA" if params.get("objective") == "sales" else "MAXIMIZE_CLICKS",
            "ad_rotation_mode": "OPTIMIZE",
            "conversion_action": "PURCHASE",
            "tracking_template": "{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign={campaignid}"
        }
        
        return campaign
    
    def auto_adjust_budget(self, campaign_id: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ajusta orçamento automaticamente baseado em performance"""
        
        current_budget = performance_data.get("current_budget", 100.0)
        roas = performance_data.get("roas", 0)
        cpa = performance_data.get("cpa", 0)
        target_cpa = performance_data.get("target_cpa", 50.0)
        
        adjustment = {
            "campaign_id": campaign_id,
            "current_budget": current_budget,
            "action": "maintain",
            "new_budget": current_budget,
            "reason": "",
            "confidence": 0.0
        }
        
        # Lógica de ajuste inteligente
        if roas > 3.0:
            # Performance excelente - aumentar orçamento
            increase = min(0.30, (roas - 3.0) * 0.10)  # Max 30% de aumento
            adjustment["new_budget"] = current_budget * (1 + increase)
            adjustment["action"] = "increase"
            adjustment["reason"] = f"ROAS excelente ({roas}x) - escalando campanha"
            adjustment["confidence"] = 0.9
            
        elif roas > 2.0:
            # Performance boa - aumentar moderadamente
            adjustment["new_budget"] = current_budget * 1.15
            adjustment["action"] = "increase"
            adjustment["reason"] = f"ROAS bom ({roas}x) - aumentando gradualmente"
            adjustment["confidence"] = 0.7
            
        elif roas < 1.0 and cpa > target_cpa * 1.5:
            # Performance ruim - reduzir orçamento
            adjustment["new_budget"] = current_budget * 0.70
            adjustment["action"] = "decrease"
            adjustment["reason"] = f"ROAS baixo ({roas}x) e CPA alto - reduzindo investimento"
            adjustment["confidence"] = 0.8
            
        elif cpa > target_cpa * 2.0:
            # CPA muito alto - pausar campanha
            adjustment["new_budget"] = 0
            adjustment["action"] = "pause"
            adjustment["reason"] = f"CPA crítico (R$ {cpa}) - pausando para análise"
            adjustment["confidence"] = 0.95
        
        else:
            # Performance OK - manter
            adjustment["reason"] = "Performance dentro do esperado"
            adjustment["confidence"] = 0.6
        
        adjustment["timestamp"] = datetime.now().isoformat()
        adjustment["requires_approval"] = adjustment["action"] in ["increase", "pause"]
        
        return adjustment
    
    def auto_pause_campaign(self, campaign_id: str, reason: str) -> Dict[str, Any]:
        """Pausa campanha automaticamente"""
        return {
            "campaign_id": campaign_id,
            "action": "pause",
            "reason": reason,
            "paused_at": datetime.now().isoformat(),
            "can_resume": True,
            "requires_approval_to_resume": True
        }
    
    def auto_activate_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Ativa campanha automaticamente"""
        return {
            "campaign_id": campaign_id,
            "action": "activate",
            "activated_at": datetime.now().isoformat(),
            "status": "active"
        }
    
    def create_ab_test_campaigns(self, base_params: Dict[str, Any], 
                                 num_variations: int = 3) -> List[Dict[str, Any]]:
        """Cria múltiplas campanhas para teste A/B"""
        campaigns = []
        
        for i in range(num_variations):
            params = base_params.copy()
            params["name"] = f"{base_params.get('name', 'Campanha')} - Variação {i+1}"
            
            # Variar orçamento
            if i == 0:
                params["budget_daily"] = base_params.get("budget_daily", 100.0)
            elif i == 1:
                params["budget_daily"] = base_params.get("budget_daily", 100.0) * 1.5
            else:
                params["budget_daily"] = base_params.get("budget_daily", 100.0) * 0.75
            
            campaign = self.create_campaign_one_click(params)
            campaign["ab_test_group"] = f"test_{datetime.now().strftime('%Y%m%d')}"
            campaign["variation_number"] = i + 1
            
            campaigns.append(campaign)
        
        return campaigns
    
    def _generate_campaign_settings(self, platform: str, objective: str, 
                                    budget_daily: float) -> Dict[str, Any]:
        """Gera configurações da campanha"""
        return {
            "attribution_window": "7_day_click_1_day_view",
            "optimization_event": "PURCHASE" if objective == "sales" else "LINK_CLICK",
            "bid_cap": budget_daily * 0.10,  # 10% do orçamento diário
            "cost_per_result_goal": budget_daily * 0.05,
            "delivery_type": "standard",
            "pacing_type": "standard",
            "auto_optimization": True,
            "auto_pause_low_performance": True,
            "auto_increase_high_performance": True
        }
    
    def _create_ad_sets(self, platform: str, objective: str, audience: str, 
                       budget_daily: float) -> List[Dict[str, Any]]:
        """Cria conjuntos de anúncios"""
        ad_sets = []
        
        # Criar 2-3 ad sets para teste
        num_ad_sets = 2 if budget_daily < 200 else 3
        
        for i in range(num_ad_sets):
            ad_set = {
                "id": f"adset_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i+1}",
                "name": f"Ad Set {i+1} - {audience}",
                "status": "active",
                "budget_daily": budget_daily / num_ad_sets,
                "optimization_goal": "CONVERSIONS" if objective == "sales" else "LINK_CLICKS",
                "billing_event": "IMPRESSIONS",
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "targeting": self._generate_targeting(platform, audience),
                "placements": self._generate_placements(platform),
                "schedule": {
                    "start_time": datetime.now().isoformat(),
                    "end_time": None  # Sem data de término
                }
            }
            ad_sets.append(ad_set)
        
        return ad_sets
    
    def _generate_optimization_config(self, platform: str, objective: str, 
                                     budget_daily: float) -> Dict[str, Any]:
        """Gera configuração de otimização"""
        return {
            "strategy": "maximize_conversions" if objective == "sales" else "maximize_clicks",
            "learning_phase_budget": budget_daily * 7,  # 7 dias de learning
            "auto_rules": [
                {
                    "name": "Pausar se CPA > R$ 100",
                    "condition": "cpa > 100",
                    "action": "pause",
                    "enabled": True
                },
                {
                    "name": "Aumentar orçamento se ROAS > 3x",
                    "condition": "roas > 3",
                    "action": "increase_budget_20",
                    "enabled": True
                },
                {
                    "name": "Reduzir orçamento se ROAS < 1x",
                    "condition": "roas < 1",
                    "action": "decrease_budget_30",
                    "enabled": True
                }
            ],
            "performance_thresholds": {
                "min_roas": 1.5,
                "max_cpa": 100.0,
                "min_ctr": 1.0,
                "min_conversion_rate": 2.0
            }
        }
    
    def _generate_targeting(self, platform: str, audience: str) -> Dict[str, Any]:
        """Gera configuração de segmentação"""
        return {
            "age_min": 18,
            "age_max": 65,
            "genders": ["male", "female"],
            "locations": [
                {"country": "BR", "name": "Brasil"}
            ],
            "interests": self._extract_interests(audience),
            "behaviors": [],
            "demographics": {
                "education": [],
                "work": [],
                "relationship": []
            },
            "custom_audiences": [],
            "lookalike_audiences": [],
            "exclusions": []
        }
    
    def _generate_placements(self, platform: str) -> List[str]:
        """Gera placements automáticos"""
        if platform == "meta":
            return [
                "facebook_feed",
                "instagram_feed",
                "facebook_stories",
                "instagram_stories",
                "facebook_reels",
                "instagram_reels"
            ]
        elif platform == "google":
            return [
                "google_search",
                "search_partners",
                "display_network"
            ]
        return []
    
    def _generate_tracking_config(self, platform: str, objective: str) -> Dict[str, Any]:
        """Gera configuração de rastreamento"""
        return {
            "pixel_id": "PIXEL_ID_HERE",
            "conversion_events": ["PageView", "AddToCart", "InitiateCheckout", "Purchase"],
            "custom_conversions": [],
            "utm_parameters": {
                "utm_source": platform,
                "utm_medium": "cpc",
                "utm_campaign": "{campaign_name}",
                "utm_content": "{ad_name}",
                "utm_term": "{keyword}"
            },
            "server_side_tracking": True,
            "enhanced_conversions": True
        }
    
    def _calculate_estimated_metrics(self, platform: str, objective: str, 
                                    budget_daily: float, duration_days: int) -> Dict[str, Any]:
        """Calcula métricas estimadas da campanha"""
        total_budget = budget_daily * duration_days
        
        # Estimativas baseadas em benchmarks da indústria
        cpm = random.uniform(15, 35)  # CPM médio no Brasil
        impressions = (total_budget / cpm) * 1000
        ctr = random.uniform(1.5, 4.5)  # CTR médio
        clicks = impressions * (ctr / 100)
        cpc = total_budget / clicks if clicks > 0 else 0
        
        conversion_rate = random.uniform(2.0, 5.0) if objective == "sales" else random.uniform(5.0, 10.0)
        conversions = clicks * (conversion_rate / 100)
        cpa = total_budget / conversions if conversions > 0 else 0
        
        # Estimativa de receita (para objetivos de vendas)
        avg_order_value = random.uniform(150, 500)
        revenue = conversions * avg_order_value if objective == "sales" else 0
        roas = revenue / total_budget if total_budget > 0 and objective == "sales" else 0
        
        return {
            "budget_total": round(total_budget, 2),
            "impressions": int(impressions),
            "clicks": int(clicks),
            "ctr": round(ctr, 2),
            "cpc": round(cpc, 2),
            "cpm": round(cpm, 2),
            "conversions": int(conversions),
            "conversion_rate": round(conversion_rate, 2),
            "cpa": round(cpa, 2),
            "revenue": round(revenue, 2) if objective == "sales" else 0,
            "roas": round(roas, 2) if objective == "sales" else 0,
            "profit": round(revenue - total_budget, 2) if objective == "sales" else 0
        }
    
    def _extract_interests(self, audience: str) -> List[str]:
        """Extrai interesses do texto de audiência"""
        # Implementação simplificada - em produção usaria NLP
        keywords = audience.lower().split()
        interests = []
        
        interest_map = {
            "empreendedor": ["Entrepreneurship", "Business", "Startups"],
            "marketing": ["Marketing", "Digital Marketing", "Advertising"],
            "vendas": ["Sales", "Business Development"],
            "tecnologia": ["Technology", "Software", "Innovation"],
            "fitness": ["Fitness", "Health", "Wellness"],
            "moda": ["Fashion", "Style", "Beauty"]
        }
        
        for keyword in keywords:
            if keyword in interest_map:
                interests.extend(interest_map[keyword])
        
        return interests if interests else ["Business", "Marketing"]


# Instância global
campaign_engine = CampaignEngineAuto()

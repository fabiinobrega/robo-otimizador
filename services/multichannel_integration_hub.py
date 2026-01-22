"""
MULTI-CHANNEL INTEGRATION HUB - Hub de Integração Multicanal
Sistema unificado de integração com todas as plataformas de anúncios
Versão: 1.0 - Expansão Avançada
"""

import os
import json
import asyncio
import logging
import hashlib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Platform(Enum):
    """Plataformas suportadas"""
    META = "meta"  # Facebook + Instagram
    GOOGLE = "google"  # Google Ads + YouTube
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    PINTEREST = "pinterest"
    SNAPCHAT = "snapchat"
    MICROSOFT = "microsoft"  # Bing Ads


class ConnectionStatus(Enum):
    """Status de conexão"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    EXPIRED = "expired"
    ERROR = "error"
    PENDING = "pending"


class SyncStatus(Enum):
    """Status de sincronização"""
    SYNCED = "synced"
    SYNCING = "syncing"
    PENDING = "pending"
    ERROR = "error"


@dataclass
class PlatformCredentials:
    """Credenciais de plataforma"""
    platform: Platform
    access_token: str
    refresh_token: Optional[str]
    account_id: str
    expires_at: Optional[datetime]
    scopes: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at


@dataclass
class PlatformConnection:
    """Conexão com plataforma"""
    id: str
    platform: Platform
    status: ConnectionStatus
    credentials: Optional[PlatformCredentials]
    account_name: str
    account_id: str
    connected_at: datetime
    last_sync: Optional[datetime]
    sync_status: SyncStatus
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "platform": self.platform.value,
            "status": self.status.value,
            "account_name": self.account_name,
            "account_id": self.account_id,
            "connected_at": self.connected_at.isoformat(),
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "sync_status": self.sync_status.value,
            "error_message": self.error_message
        }


@dataclass
class UnifiedCampaign:
    """Campanha unificada (cross-platform)"""
    id: str
    name: str
    platforms: List[Platform]
    platform_campaigns: Dict[str, str]  # platform -> campaign_id
    status: str
    budget: float
    budget_type: str  # daily, lifetime
    objective: str
    start_date: datetime
    end_date: Optional[datetime]
    metrics: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "platforms": [p.value for p in self.platforms],
            "platform_campaigns": self.platform_campaigns,
            "status": self.status,
            "budget": self.budget,
            "budget_type": self.budget_type,
            "objective": self.objective,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "metrics": self.metrics,
            "created_at": self.created_at.isoformat()
        }


class BasePlatformAdapter(ABC):
    """Adaptador base para plataformas"""
    
    def __init__(self, credentials: PlatformCredentials):
        self.credentials = credentials
        
    @abstractmethod
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """Obtém campanhas da plataforma"""
        pass
    
    @abstractmethod
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria campanha na plataforma"""
        pass
    
    @abstractmethod
    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza campanha na plataforma"""
        pass
    
    @abstractmethod
    async def get_metrics(self, campaign_id: str, date_range: tuple) -> Dict[str, Any]:
        """Obtém métricas da campanha"""
        pass
    
    @abstractmethod
    async def pause_campaign(self, campaign_id: str) -> bool:
        """Pausa campanha"""
        pass
    
    @abstractmethod
    async def resume_campaign(self, campaign_id: str) -> bool:
        """Retoma campanha"""
        pass


class MetaAdsAdapter(BasePlatformAdapter):
    """Adaptador para Meta Ads (Facebook + Instagram)"""
    
    def __init__(self, credentials: PlatformCredentials):
        super().__init__(credentials)
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """Obtém campanhas do Meta Ads"""
        # Simulação - em produção, usaria a API real
        return [
            {
                "id": "meta_camp_001",
                "name": "Campanha Facebook - Conversões",
                "status": "ACTIVE",
                "objective": "CONVERSIONS",
                "budget": 100,
                "budget_type": "daily",
                "platform": "meta"
            },
            {
                "id": "meta_camp_002",
                "name": "Campanha Instagram - Awareness",
                "status": "ACTIVE",
                "objective": "BRAND_AWARENESS",
                "budget": 50,
                "budget_type": "daily",
                "platform": "meta"
            }
        ]
    
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria campanha no Meta Ads"""
        campaign_id = hashlib.md5(f"meta_{datetime.now()}".encode()).hexdigest()[:12]
        
        return {
            "id": campaign_id,
            "platform": "meta",
            "name": campaign_data.get("name"),
            "status": "PAUSED",
            "created": True
        }
    
    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza campanha no Meta Ads"""
        return {
            "id": campaign_id,
            "updated": True,
            "changes": updates
        }
    
    async def get_metrics(self, campaign_id: str, date_range: tuple) -> Dict[str, Any]:
        """Obtém métricas do Meta Ads"""
        return {
            "impressions": 150000,
            "clicks": 4500,
            "spend": 450.00,
            "conversions": 120,
            "revenue": 1800.00,
            "ctr": 3.0,
            "cpc": 0.10,
            "cpa": 3.75,
            "roas": 4.0
        }
    
    async def pause_campaign(self, campaign_id: str) -> bool:
        """Pausa campanha no Meta Ads"""
        return True
    
    async def resume_campaign(self, campaign_id: str) -> bool:
        """Retoma campanha no Meta Ads"""
        return True


class GoogleAdsAdapter(BasePlatformAdapter):
    """Adaptador para Google Ads"""
    
    def __init__(self, credentials: PlatformCredentials):
        super().__init__(credentials)
        
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """Obtém campanhas do Google Ads"""
        return [
            {
                "id": "google_camp_001",
                "name": "Campanha Search - Marca",
                "status": "ENABLED",
                "objective": "SEARCH",
                "budget": 80,
                "budget_type": "daily",
                "platform": "google"
            },
            {
                "id": "google_camp_002",
                "name": "Campanha Display - Remarketing",
                "status": "ENABLED",
                "objective": "DISPLAY",
                "budget": 40,
                "budget_type": "daily",
                "platform": "google"
            }
        ]
    
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria campanha no Google Ads"""
        campaign_id = hashlib.md5(f"google_{datetime.now()}".encode()).hexdigest()[:12]
        
        return {
            "id": campaign_id,
            "platform": "google",
            "name": campaign_data.get("name"),
            "status": "PAUSED",
            "created": True
        }
    
    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza campanha no Google Ads"""
        return {
            "id": campaign_id,
            "updated": True,
            "changes": updates
        }
    
    async def get_metrics(self, campaign_id: str, date_range: tuple) -> Dict[str, Any]:
        """Obtém métricas do Google Ads"""
        return {
            "impressions": 200000,
            "clicks": 3000,
            "spend": 600.00,
            "conversions": 90,
            "revenue": 1350.00,
            "ctr": 1.5,
            "cpc": 0.20,
            "cpa": 6.67,
            "roas": 2.25
        }
    
    async def pause_campaign(self, campaign_id: str) -> bool:
        """Pausa campanha no Google Ads"""
        return True
    
    async def resume_campaign(self, campaign_id: str) -> bool:
        """Retoma campanha no Google Ads"""
        return True


class TikTokAdsAdapter(BasePlatformAdapter):
    """Adaptador para TikTok Ads"""
    
    def __init__(self, credentials: PlatformCredentials):
        super().__init__(credentials)
        
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """Obtém campanhas do TikTok Ads"""
        return [
            {
                "id": "tiktok_camp_001",
                "name": "Campanha TikTok - Conversões",
                "status": "ACTIVE",
                "objective": "CONVERSIONS",
                "budget": 60,
                "budget_type": "daily",
                "platform": "tiktok"
            }
        ]
    
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria campanha no TikTok Ads"""
        campaign_id = hashlib.md5(f"tiktok_{datetime.now()}".encode()).hexdigest()[:12]
        
        return {
            "id": campaign_id,
            "platform": "tiktok",
            "name": campaign_data.get("name"),
            "status": "PAUSED",
            "created": True
        }
    
    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza campanha no TikTok Ads"""
        return {
            "id": campaign_id,
            "updated": True,
            "changes": updates
        }
    
    async def get_metrics(self, campaign_id: str, date_range: tuple) -> Dict[str, Any]:
        """Obtém métricas do TikTok Ads"""
        return {
            "impressions": 300000,
            "clicks": 9000,
            "spend": 300.00,
            "conversions": 75,
            "revenue": 1125.00,
            "ctr": 3.0,
            "cpc": 0.033,
            "cpa": 4.00,
            "roas": 3.75
        }
    
    async def pause_campaign(self, campaign_id: str) -> bool:
        """Pausa campanha no TikTok Ads"""
        return True
    
    async def resume_campaign(self, campaign_id: str) -> bool:
        """Retoma campanha no TikTok Ads"""
        return True


class LinkedInAdsAdapter(BasePlatformAdapter):
    """Adaptador para LinkedIn Ads"""
    
    def __init__(self, credentials: PlatformCredentials):
        super().__init__(credentials)
        
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """Obtém campanhas do LinkedIn Ads"""
        return [
            {
                "id": "linkedin_camp_001",
                "name": "Campanha LinkedIn - B2B Leads",
                "status": "ACTIVE",
                "objective": "LEAD_GENERATION",
                "budget": 100,
                "budget_type": "daily",
                "platform": "linkedin"
            }
        ]
    
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria campanha no LinkedIn Ads"""
        campaign_id = hashlib.md5(f"linkedin_{datetime.now()}".encode()).hexdigest()[:12]
        
        return {
            "id": campaign_id,
            "platform": "linkedin",
            "name": campaign_data.get("name"),
            "status": "PAUSED",
            "created": True
        }
    
    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza campanha no LinkedIn Ads"""
        return {
            "id": campaign_id,
            "updated": True,
            "changes": updates
        }
    
    async def get_metrics(self, campaign_id: str, date_range: tuple) -> Dict[str, Any]:
        """Obtém métricas do LinkedIn Ads"""
        return {
            "impressions": 50000,
            "clicks": 500,
            "spend": 500.00,
            "conversions": 25,
            "revenue": 2500.00,
            "ctr": 1.0,
            "cpc": 1.00,
            "cpa": 20.00,
            "roas": 5.0
        }
    
    async def pause_campaign(self, campaign_id: str) -> bool:
        """Pausa campanha no LinkedIn Ads"""
        return True
    
    async def resume_campaign(self, campaign_id: str) -> bool:
        """Retoma campanha no LinkedIn Ads"""
        return True


class MultiChannelIntegrationHub:
    """
    Hub principal de Integração Multicanal
    Gerencia conexões e operações em todas as plataformas
    """
    
    def __init__(self):
        self.connections: Dict[str, PlatformConnection] = {}
        self.adapters: Dict[Platform, BasePlatformAdapter] = {}
        self.unified_campaigns: Dict[str, UnifiedCampaign] = {}
        self.sync_history: List[Dict[str, Any]] = []
        
    def _get_adapter_class(self, platform: Platform) -> type:
        """Obtém classe do adaptador para a plataforma"""
        adapters = {
            Platform.META: MetaAdsAdapter,
            Platform.GOOGLE: GoogleAdsAdapter,
            Platform.TIKTOK: TikTokAdsAdapter,
            Platform.LINKEDIN: LinkedInAdsAdapter
        }
        return adapters.get(platform)
    
    async def connect_platform(
        self,
        platform: Platform,
        credentials_data: Dict[str, Any]
    ) -> PlatformConnection:
        """Conecta uma plataforma"""
        connection_id = hashlib.md5(f"{platform.value}_{datetime.now()}".encode()).hexdigest()[:12]
        
        credentials = PlatformCredentials(
            platform=platform,
            access_token=credentials_data.get("access_token", ""),
            refresh_token=credentials_data.get("refresh_token"),
            account_id=credentials_data.get("account_id", ""),
            expires_at=datetime.now() + timedelta(days=60) if credentials_data.get("access_token") else None,
            scopes=credentials_data.get("scopes", []),
            metadata=credentials_data.get("metadata", {})
        )
        
        connection = PlatformConnection(
            id=connection_id,
            platform=platform,
            status=ConnectionStatus.CONNECTED,
            credentials=credentials,
            account_name=credentials_data.get("account_name", f"{platform.value} Account"),
            account_id=credentials_data.get("account_id", ""),
            connected_at=datetime.now(),
            last_sync=None,
            sync_status=SyncStatus.PENDING
        )
        
        self.connections[connection_id] = connection
        
        # Criar adaptador
        adapter_class = self._get_adapter_class(platform)
        if adapter_class:
            self.adapters[platform] = adapter_class(credentials)
            
        return connection
    
    async def disconnect_platform(self, connection_id: str) -> bool:
        """Desconecta uma plataforma"""
        connection = self.connections.get(connection_id)
        
        if not connection:
            return False
            
        connection.status = ConnectionStatus.DISCONNECTED
        
        if connection.platform in self.adapters:
            del self.adapters[connection.platform]
            
        return True
    
    async def sync_platform(self, connection_id: str) -> Dict[str, Any]:
        """Sincroniza dados de uma plataforma"""
        connection = self.connections.get(connection_id)
        
        if not connection:
            return {"error": "Conexão não encontrada"}
            
        if connection.status != ConnectionStatus.CONNECTED:
            return {"error": "Plataforma não conectada"}
            
        connection.sync_status = SyncStatus.SYNCING
        
        adapter = self.adapters.get(connection.platform)
        
        if not adapter:
            connection.sync_status = SyncStatus.ERROR
            return {"error": "Adaptador não encontrado"}
            
        try:
            # Sincronizar campanhas
            campaigns = await adapter.get_campaigns()
            
            connection.last_sync = datetime.now()
            connection.sync_status = SyncStatus.SYNCED
            
            sync_record = {
                "connection_id": connection_id,
                "platform": connection.platform.value,
                "timestamp": datetime.now().isoformat(),
                "campaigns_synced": len(campaigns),
                "status": "success"
            }
            self.sync_history.append(sync_record)
            
            return {
                "status": "success",
                "campaigns_synced": len(campaigns),
                "last_sync": connection.last_sync.isoformat()
            }
            
        except Exception as e:
            connection.sync_status = SyncStatus.ERROR
            connection.error_message = str(e)
            return {"error": str(e)}
    
    async def sync_all_platforms(self) -> Dict[str, Any]:
        """Sincroniza todas as plataformas conectadas"""
        results = {}
        
        for connection_id, connection in self.connections.items():
            if connection.status == ConnectionStatus.CONNECTED:
                result = await self.sync_platform(connection_id)
                results[connection.platform.value] = result
                
        return results
    
    async def get_all_campaigns(self) -> List[Dict[str, Any]]:
        """Obtém todas as campanhas de todas as plataformas"""
        all_campaigns = []
        
        for platform, adapter in self.adapters.items():
            try:
                campaigns = await adapter.get_campaigns()
                for campaign in campaigns:
                    campaign["platform"] = platform.value
                all_campaigns.extend(campaigns)
            except Exception as e:
                logger.error(f"Erro ao obter campanhas de {platform.value}: {e}")
                
        return all_campaigns
    
    async def get_unified_metrics(
        self,
        date_range: tuple = None
    ) -> Dict[str, Any]:
        """Obtém métricas unificadas de todas as plataformas"""
        if not date_range:
            date_range = (datetime.now() - timedelta(days=7), datetime.now())
            
        unified = {
            "impressions": 0,
            "clicks": 0,
            "spend": 0,
            "conversions": 0,
            "revenue": 0
        }
        
        by_platform = {}
        
        for platform, adapter in self.adapters.items():
            try:
                campaigns = await adapter.get_campaigns()
                platform_metrics = {
                    "impressions": 0,
                    "clicks": 0,
                    "spend": 0,
                    "conversions": 0,
                    "revenue": 0
                }
                
                for campaign in campaigns:
                    metrics = await adapter.get_metrics(campaign["id"], date_range)
                    for key in platform_metrics:
                        platform_metrics[key] += metrics.get(key, 0)
                        unified[key] += metrics.get(key, 0)
                        
                by_platform[platform.value] = platform_metrics
                
            except Exception as e:
                logger.error(f"Erro ao obter métricas de {platform.value}: {e}")
                
        # Calcular métricas derivadas
        unified["ctr"] = round((unified["clicks"] / unified["impressions"] * 100) if unified["impressions"] > 0 else 0, 2)
        unified["cpc"] = round((unified["spend"] / unified["clicks"]) if unified["clicks"] > 0 else 0, 2)
        unified["cpa"] = round((unified["spend"] / unified["conversions"]) if unified["conversions"] > 0 else 0, 2)
        unified["roas"] = round((unified["revenue"] / unified["spend"]) if unified["spend"] > 0 else 0, 2)
        
        return {
            "unified": unified,
            "by_platform": by_platform,
            "date_range": {
                "start": date_range[0].isoformat(),
                "end": date_range[1].isoformat()
            }
        }
    
    async def create_cross_platform_campaign(
        self,
        campaign_data: Dict[str, Any]
    ) -> UnifiedCampaign:
        """Cria campanha em múltiplas plataformas"""
        campaign_id = hashlib.md5(f"unified_{datetime.now()}".encode()).hexdigest()[:12]
        
        platforms = [Platform[p.upper()] for p in campaign_data.get("platforms", ["meta"])]
        platform_campaigns = {}
        
        for platform in platforms:
            adapter = self.adapters.get(platform)
            if adapter:
                result = await adapter.create_campaign(campaign_data)
                platform_campaigns[platform.value] = result["id"]
                
        unified_campaign = UnifiedCampaign(
            id=campaign_id,
            name=campaign_data.get("name", "Nova Campanha"),
            platforms=platforms,
            platform_campaigns=platform_campaigns,
            status="paused",
            budget=campaign_data.get("budget", 0),
            budget_type=campaign_data.get("budget_type", "daily"),
            objective=campaign_data.get("objective", "conversions"),
            start_date=datetime.now(),
            end_date=None,
            metrics={}
        )
        
        self.unified_campaigns[campaign_id] = unified_campaign
        
        return unified_campaign
    
    async def update_cross_platform_campaign(
        self,
        campaign_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Atualiza campanha em todas as plataformas"""
        unified = self.unified_campaigns.get(campaign_id)
        
        if not unified:
            return {"error": "Campanha não encontrada"}
            
        results = {}
        
        for platform in unified.platforms:
            adapter = self.adapters.get(platform)
            if adapter:
                platform_campaign_id = unified.platform_campaigns.get(platform.value)
                if platform_campaign_id:
                    result = await adapter.update_campaign(platform_campaign_id, updates)
                    results[platform.value] = result
                    
        return {"campaign_id": campaign_id, "updates": results}
    
    async def pause_cross_platform_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pausa campanha em todas as plataformas"""
        unified = self.unified_campaigns.get(campaign_id)
        
        if not unified:
            return {"error": "Campanha não encontrada"}
            
        results = {}
        
        for platform in unified.platforms:
            adapter = self.adapters.get(platform)
            if adapter:
                platform_campaign_id = unified.platform_campaigns.get(platform.value)
                if platform_campaign_id:
                    success = await adapter.pause_campaign(platform_campaign_id)
                    results[platform.value] = success
                    
        unified.status = "paused"
        
        return {"campaign_id": campaign_id, "status": "paused", "results": results}
    
    async def resume_cross_platform_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Retoma campanha em todas as plataformas"""
        unified = self.unified_campaigns.get(campaign_id)
        
        if not unified:
            return {"error": "Campanha não encontrada"}
            
        results = {}
        
        for platform in unified.platforms:
            adapter = self.adapters.get(platform)
            if adapter:
                platform_campaign_id = unified.platform_campaigns.get(platform.value)
                if platform_campaign_id:
                    success = await adapter.resume_campaign(platform_campaign_id)
                    results[platform.value] = success
                    
        unified.status = "active"
        
        return {"campaign_id": campaign_id, "status": "active", "results": results}
    
    def get_connections(self) -> List[Dict[str, Any]]:
        """Obtém todas as conexões"""
        return [c.to_dict() for c in self.connections.values()]
    
    def get_connection(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Obtém uma conexão específica"""
        connection = self.connections.get(connection_id)
        return connection.to_dict() if connection else None
    
    def get_unified_campaigns(self) -> List[Dict[str, Any]]:
        """Obtém todas as campanhas unificadas"""
        return [c.to_dict() for c in self.unified_campaigns.values()]
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do hub"""
        connected = [c for c in self.connections.values() if c.status == ConnectionStatus.CONNECTED]
        
        return {
            "total_connections": len(self.connections),
            "connected_platforms": len(connected),
            "platforms": [c.platform.value for c in connected],
            "unified_campaigns": len(self.unified_campaigns),
            "last_sync": max([c.last_sync for c in self.connections.values() if c.last_sync], default=None),
            "sync_history_count": len(self.sync_history)
        }


# Instância global
integration_hub = MultiChannelIntegrationHub()


# Funções de conveniência
async def connect_platform(platform: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
    """Conecta plataforma"""
    connection = await integration_hub.connect_platform(Platform[platform.upper()], credentials)
    return connection.to_dict()

async def disconnect_platform(connection_id: str) -> bool:
    """Desconecta plataforma"""
    return await integration_hub.disconnect_platform(connection_id)

async def sync_platform(connection_id: str) -> Dict[str, Any]:
    """Sincroniza plataforma"""
    return await integration_hub.sync_platform(connection_id)

async def sync_all() -> Dict[str, Any]:
    """Sincroniza todas as plataformas"""
    return await integration_hub.sync_all_platforms()

async def get_all_campaigns() -> List[Dict[str, Any]]:
    """Obtém todas as campanhas"""
    return await integration_hub.get_all_campaigns()

async def get_unified_metrics(start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    """Obtém métricas unificadas"""
    date_range = None
    if start_date and end_date:
        date_range = (datetime.fromisoformat(start_date), datetime.fromisoformat(end_date))
    return await integration_hub.get_unified_metrics(date_range)

async def create_campaign(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """Cria campanha cross-platform"""
    campaign = await integration_hub.create_cross_platform_campaign(campaign_data)
    return campaign.to_dict()

def get_connections() -> List[Dict[str, Any]]:
    """Obtém conexões"""
    return integration_hub.get_connections()

def get_hub_status() -> Dict[str, Any]:
    """Obtém status do hub"""
    return integration_hub.get_status()

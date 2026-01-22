"""
AGENCY MODE - Modo Agência Multi-Conta
Gestão de múltiplos clientes com permissões e dashboards isolados
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import secrets

class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"

class AgencyMode:
    """Sistema de gestão multi-conta para agências."""
    
    def __init__(self):
        self.name = "Agency Mode"
        self.version = "2.0.0"
        
        # Estrutura de dados
        self.agencies = {}
        self.clients = {}
        self.users = {}
        self.permissions = {}
        
        # Permissões por role
        self.role_permissions = {
            UserRole.OWNER: {
                "can_create_clients": True,
                "can_delete_clients": True,
                "can_manage_users": True,
                "can_view_billing": True,
                "can_edit_campaigns": True,
                "can_publish_campaigns": True,
                "can_view_reports": True,
                "can_export_data": True,
                "can_access_api": True,
                "can_manage_settings": True
            },
            UserRole.ADMIN: {
                "can_create_clients": True,
                "can_delete_clients": False,
                "can_manage_users": True,
                "can_view_billing": True,
                "can_edit_campaigns": True,
                "can_publish_campaigns": True,
                "can_view_reports": True,
                "can_export_data": True,
                "can_access_api": True,
                "can_manage_settings": False
            },
            UserRole.MANAGER: {
                "can_create_clients": False,
                "can_delete_clients": False,
                "can_manage_users": False,
                "can_view_billing": False,
                "can_edit_campaigns": True,
                "can_publish_campaigns": True,
                "can_view_reports": True,
                "can_export_data": True,
                "can_access_api": False,
                "can_manage_settings": False
            },
            UserRole.ANALYST: {
                "can_create_clients": False,
                "can_delete_clients": False,
                "can_manage_users": False,
                "can_view_billing": False,
                "can_edit_campaigns": False,
                "can_publish_campaigns": False,
                "can_view_reports": True,
                "can_export_data": True,
                "can_access_api": False,
                "can_manage_settings": False
            },
            UserRole.VIEWER: {
                "can_create_clients": False,
                "can_delete_clients": False,
                "can_manage_users": False,
                "can_view_billing": False,
                "can_edit_campaigns": False,
                "can_publish_campaigns": False,
                "can_view_reports": True,
                "can_export_data": False,
                "can_access_api": False,
                "can_manage_settings": False
            }
        }
        
        # Configurações de white-label
        self.white_label_config = {
            "customizable_elements": [
                "logo",
                "primary_color",
                "secondary_color",
                "company_name",
                "favicon",
                "email_footer",
                "report_header",
                "report_footer"
            ]
        }
    
    def create_agency(self, agency_data: Dict) -> Dict[str, Any]:
        """Cria uma nova agência."""
        
        agency_id = f"agency_{secrets.token_hex(8)}"
        
        agency = {
            "id": agency_id,
            "name": agency_data.get("name", "Nova Agência"),
            "owner_email": agency_data.get("owner_email"),
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "plan": agency_data.get("plan", "starter"),
            "settings": {
                "max_clients": self._get_plan_limits(agency_data.get("plan", "starter"))["max_clients"],
                "max_users": self._get_plan_limits(agency_data.get("plan", "starter"))["max_users"],
                "white_label_enabled": agency_data.get("plan", "starter") in ["professional", "enterprise"]
            },
            "white_label": {
                "logo_url": agency_data.get("logo_url"),
                "primary_color": agency_data.get("primary_color", "#6366F1"),
                "secondary_color": agency_data.get("secondary_color", "#4F46E5"),
                "company_name": agency_data.get("name", "Nova Agência")
            },
            "clients": [],
            "users": []
        }
        
        self.agencies[agency_id] = agency
        
        # Criar usuário owner
        owner_user = self.create_user({
            "agency_id": agency_id,
            "email": agency_data.get("owner_email"),
            "name": agency_data.get("owner_name", "Owner"),
            "role": UserRole.OWNER.value
        })
        
        return {
            "agency_id": agency_id,
            "agency": agency,
            "owner_user": owner_user,
            "message": "Agência criada com sucesso"
        }
    
    def create_client(self, agency_id: str, client_data: Dict) -> Dict[str, Any]:
        """Cria um novo cliente para a agência."""
        
        if agency_id not in self.agencies:
            return {"error": "Agência não encontrada"}
        
        agency = self.agencies[agency_id]
        
        # Verificar limite de clientes
        if len(agency["clients"]) >= agency["settings"]["max_clients"]:
            return {"error": f"Limite de {agency['settings']['max_clients']} clientes atingido"}
        
        client_id = f"client_{secrets.token_hex(8)}"
        
        client = {
            "id": client_id,
            "agency_id": agency_id,
            "name": client_data.get("name", "Novo Cliente"),
            "company": client_data.get("company", ""),
            "email": client_data.get("email"),
            "phone": client_data.get("phone"),
            "niche": client_data.get("niche", "geral"),
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "ad_accounts": client_data.get("ad_accounts", []),
            "settings": {
                "timezone": client_data.get("timezone", "America/Sao_Paulo"),
                "currency": client_data.get("currency", "BRL"),
                "notification_email": client_data.get("email")
            },
            "metrics": {
                "total_spend": 0,
                "total_revenue": 0,
                "total_campaigns": 0,
                "active_campaigns": 0
            }
        }
        
        self.clients[client_id] = client
        agency["clients"].append(client_id)
        
        return {
            "client_id": client_id,
            "client": client,
            "message": "Cliente criado com sucesso"
        }
    
    def create_user(self, user_data: Dict) -> Dict[str, Any]:
        """Cria um novo usuário."""
        
        user_id = f"user_{secrets.token_hex(8)}"
        
        user = {
            "id": user_id,
            "agency_id": user_data.get("agency_id"),
            "email": user_data.get("email"),
            "name": user_data.get("name", "Novo Usuário"),
            "role": user_data.get("role", UserRole.VIEWER.value),
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "assigned_clients": user_data.get("assigned_clients", []),
            "last_login": None,
            "permissions": self._get_role_permissions(user_data.get("role", UserRole.VIEWER.value))
        }
        
        self.users[user_id] = user
        
        # Adicionar à agência
        agency_id = user_data.get("agency_id")
        if agency_id and agency_id in self.agencies:
            self.agencies[agency_id]["users"].append(user_id)
        
        return {
            "user_id": user_id,
            "user": user,
            "message": "Usuário criado com sucesso"
        }
    
    def assign_user_to_client(
        self, 
        user_id: str, 
        client_id: str, 
        permissions: Dict = None
    ) -> Dict[str, Any]:
        """Atribui usuário a um cliente específico."""
        
        if user_id not in self.users:
            return {"error": "Usuário não encontrado"}
        
        if client_id not in self.clients:
            return {"error": "Cliente não encontrado"}
        
        user = self.users[user_id]
        
        if client_id not in user["assigned_clients"]:
            user["assigned_clients"].append(client_id)
        
        # Salvar permissões específicas se fornecidas
        if permissions:
            permission_key = f"{user_id}_{client_id}"
            self.permissions[permission_key] = permissions
        
        return {
            "user_id": user_id,
            "client_id": client_id,
            "message": "Usuário atribuído ao cliente com sucesso"
        }
    
    def get_client_dashboard(self, client_id: str, user_id: str = None) -> Dict[str, Any]:
        """Obtém dashboard isolado de um cliente."""
        
        if client_id not in self.clients:
            return {"error": "Cliente não encontrado"}
        
        client = self.clients[client_id]
        
        # Verificar permissão se user_id fornecido
        if user_id:
            if not self._check_client_access(user_id, client_id):
                return {"error": "Acesso negado a este cliente"}
        
        # Gerar dados do dashboard
        dashboard = {
            "client_id": client_id,
            "client_name": client["name"],
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_spend": client["metrics"]["total_spend"],
                "total_revenue": client["metrics"]["total_revenue"],
                "roas": round(
                    client["metrics"]["total_revenue"] / client["metrics"]["total_spend"], 2
                ) if client["metrics"]["total_spend"] > 0 else 0,
                "active_campaigns": client["metrics"]["active_campaigns"],
                "total_campaigns": client["metrics"]["total_campaigns"]
            },
            "performance": {
                "today": self._get_performance_data(client_id, "today"),
                "yesterday": self._get_performance_data(client_id, "yesterday"),
                "last_7_days": self._get_performance_data(client_id, "7d"),
                "last_30_days": self._get_performance_data(client_id, "30d")
            },
            "top_campaigns": self._get_top_campaigns(client_id),
            "alerts": self._get_client_alerts(client_id),
            "recommendations": self._get_client_recommendations(client_id)
        }
        
        return dashboard
    
    def get_agency_overview(self, agency_id: str) -> Dict[str, Any]:
        """Obtém visão geral da agência com todos os clientes."""
        
        if agency_id not in self.agencies:
            return {"error": "Agência não encontrada"}
        
        agency = self.agencies[agency_id]
        
        # Agregar métricas de todos os clientes
        total_spend = 0
        total_revenue = 0
        total_campaigns = 0
        active_campaigns = 0
        
        client_summaries = []
        for client_id in agency["clients"]:
            if client_id in self.clients:
                client = self.clients[client_id]
                total_spend += client["metrics"]["total_spend"]
                total_revenue += client["metrics"]["total_revenue"]
                total_campaigns += client["metrics"]["total_campaigns"]
                active_campaigns += client["metrics"]["active_campaigns"]
                
                client_summaries.append({
                    "id": client_id,
                    "name": client["name"],
                    "spend": client["metrics"]["total_spend"],
                    "revenue": client["metrics"]["total_revenue"],
                    "roas": round(
                        client["metrics"]["total_revenue"] / client["metrics"]["total_spend"], 2
                    ) if client["metrics"]["total_spend"] > 0 else 0,
                    "status": client["status"]
                })
        
        return {
            "agency_id": agency_id,
            "agency_name": agency["name"],
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_clients": len(agency["clients"]),
                "total_users": len(agency["users"]),
                "total_spend": round(total_spend, 2),
                "total_revenue": round(total_revenue, 2),
                "overall_roas": round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
                "total_campaigns": total_campaigns,
                "active_campaigns": active_campaigns
            },
            "clients": sorted(client_summaries, key=lambda x: x["spend"], reverse=True),
            "plan_usage": {
                "clients_used": len(agency["clients"]),
                "clients_limit": agency["settings"]["max_clients"],
                "users_used": len(agency["users"]),
                "users_limit": agency["settings"]["max_users"]
            }
        }
    
    def generate_white_label_report(
        self, 
        agency_id: str, 
        client_id: str,
        report_type: str = "monthly",
        date_range: Dict = None
    ) -> Dict[str, Any]:
        """Gera relatório white-label para cliente."""
        
        if agency_id not in self.agencies:
            return {"error": "Agência não encontrada"}
        
        if client_id not in self.clients:
            return {"error": "Cliente não encontrado"}
        
        agency = self.agencies[agency_id]
        client = self.clients[client_id]
        
        # Verificar se white-label está habilitado
        if not agency["settings"]["white_label_enabled"]:
            return {"error": "White-label não disponível no seu plano"}
        
        # Configurações de branding
        branding = agency["white_label"]
        
        # Gerar relatório
        report = {
            "report_id": f"report_{secrets.token_hex(8)}",
            "generated_at": datetime.now().isoformat(),
            "report_type": report_type,
            "branding": {
                "logo_url": branding["logo_url"],
                "company_name": branding["company_name"],
                "primary_color": branding["primary_color"],
                "secondary_color": branding["secondary_color"]
            },
            "client": {
                "name": client["name"],
                "company": client["company"]
            },
            "period": date_range or {
                "start": (datetime.now() - timedelta(days=30)).isoformat(),
                "end": datetime.now().isoformat()
            },
            "executive_summary": self._generate_executive_summary(client),
            "performance_metrics": {
                "spend": client["metrics"]["total_spend"],
                "revenue": client["metrics"]["total_revenue"],
                "roas": round(
                    client["metrics"]["total_revenue"] / client["metrics"]["total_spend"], 2
                ) if client["metrics"]["total_spend"] > 0 else 0,
                "campaigns": client["metrics"]["total_campaigns"],
                "conversions": 0  # Placeholder
            },
            "campaign_breakdown": self._get_campaign_breakdown(client_id),
            "recommendations": self._generate_report_recommendations(client),
            "next_steps": self._generate_next_steps(client)
        }
        
        return report
    
    def check_permission(
        self, 
        user_id: str, 
        permission: str, 
        client_id: str = None
    ) -> bool:
        """Verifica se usuário tem determinada permissão."""
        
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        
        # Verificar permissão base do role
        base_permission = user["permissions"].get(permission, False)
        
        # Se tem cliente específico, verificar acesso ao cliente
        if client_id and not self._check_client_access(user_id, client_id):
            return False
        
        # Verificar permissões específicas do cliente
        if client_id:
            permission_key = f"{user_id}_{client_id}"
            if permission_key in self.permissions:
                specific_permission = self.permissions[permission_key].get(permission)
                if specific_permission is not None:
                    return specific_permission
        
        return base_permission
    
    def get_user_accessible_clients(self, user_id: str) -> List[Dict]:
        """Obtém lista de clientes acessíveis por um usuário."""
        
        if user_id not in self.users:
            return []
        
        user = self.users[user_id]
        
        # Owner e Admin têm acesso a todos os clientes da agência
        if user["role"] in [UserRole.OWNER.value, UserRole.ADMIN.value]:
            agency_id = user["agency_id"]
            if agency_id in self.agencies:
                return [
                    self.clients[cid] for cid in self.agencies[agency_id]["clients"]
                    if cid in self.clients
                ]
        
        # Outros roles têm acesso apenas aos clientes atribuídos
        return [
            self.clients[cid] for cid in user["assigned_clients"]
            if cid in self.clients
        ]
    
    def update_client_metrics(self, client_id: str, metrics: Dict) -> Dict[str, Any]:
        """Atualiza métricas de um cliente."""
        
        if client_id not in self.clients:
            return {"error": "Cliente não encontrado"}
        
        client = self.clients[client_id]
        
        for key, value in metrics.items():
            if key in client["metrics"]:
                client["metrics"][key] = value
        
        return {
            "client_id": client_id,
            "updated_metrics": client["metrics"],
            "message": "Métricas atualizadas com sucesso"
        }
    
    def _get_plan_limits(self, plan: str) -> Dict:
        """Retorna limites do plano."""
        limits = {
            "starter": {"max_clients": 5, "max_users": 3},
            "professional": {"max_clients": 20, "max_users": 10},
            "enterprise": {"max_clients": 100, "max_users": 50},
            "unlimited": {"max_clients": 9999, "max_users": 9999}
        }
        return limits.get(plan, limits["starter"])
    
    def _get_role_permissions(self, role: str) -> Dict:
        """Retorna permissões de um role."""
        try:
            role_enum = UserRole(role)
            return self.role_permissions.get(role_enum, self.role_permissions[UserRole.VIEWER])
        except:
            return self.role_permissions[UserRole.VIEWER]
    
    def _check_client_access(self, user_id: str, client_id: str) -> bool:
        """Verifica se usuário tem acesso a um cliente."""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        
        # Owner e Admin têm acesso a todos
        if user["role"] in [UserRole.OWNER.value, UserRole.ADMIN.value]:
            return True
        
        return client_id in user["assigned_clients"]
    
    def _get_performance_data(self, client_id: str, period: str) -> Dict:
        """Obtém dados de performance de um período."""
        # Placeholder - em produção, buscaria do banco de dados
        return {
            "spend": 0,
            "revenue": 0,
            "impressions": 0,
            "clicks": 0,
            "conversions": 0,
            "ctr": 0,
            "cpc": 0,
            "cpa": 0,
            "roas": 0
        }
    
    def _get_top_campaigns(self, client_id: str, limit: int = 5) -> List[Dict]:
        """Obtém top campanhas de um cliente."""
        # Placeholder
        return []
    
    def _get_client_alerts(self, client_id: str) -> List[Dict]:
        """Obtém alertas de um cliente."""
        # Placeholder
        return []
    
    def _get_client_recommendations(self, client_id: str) -> List[Dict]:
        """Obtém recomendações para um cliente."""
        return [
            {
                "type": "optimization",
                "priority": "medium",
                "message": "Considere testar novos criativos para melhorar CTR"
            }
        ]
    
    def _generate_executive_summary(self, client: Dict) -> str:
        """Gera resumo executivo para relatório."""
        spend = client["metrics"]["total_spend"]
        revenue = client["metrics"]["total_revenue"]
        roas = round(revenue / spend, 2) if spend > 0 else 0
        
        if roas >= 3:
            performance = "excelente"
        elif roas >= 2:
            performance = "boa"
        elif roas >= 1:
            performance = "satisfatória"
        else:
            performance = "abaixo do esperado"
        
        return f"""
        Durante o período analisado, a conta {client['name']} apresentou performance {performance}.
        O investimento total foi de R$ {spend:,.2f}, gerando R$ {revenue:,.2f} em receita,
        resultando em um ROAS de {roas}x.
        """
    
    def _get_campaign_breakdown(self, client_id: str) -> List[Dict]:
        """Obtém breakdown de campanhas."""
        # Placeholder
        return []
    
    def _generate_report_recommendations(self, client: Dict) -> List[str]:
        """Gera recomendações para relatório."""
        recommendations = []
        
        roas = (
            client["metrics"]["total_revenue"] / client["metrics"]["total_spend"]
            if client["metrics"]["total_spend"] > 0 else 0
        )
        
        if roas < 2:
            recommendations.append("Otimizar públicos-alvo para melhorar ROAS")
            recommendations.append("Testar novos criativos e copies")
        
        if client["metrics"]["active_campaigns"] < 3:
            recommendations.append("Aumentar número de campanhas ativas para diversificar")
        
        recommendations.append("Continuar monitoramento diário das métricas")
        
        return recommendations
    
    def _generate_next_steps(self, client: Dict) -> List[str]:
        """Gera próximos passos para relatório."""
        return [
            "Reunião de alinhamento para discutir resultados",
            "Definir metas para o próximo período",
            "Aprovar novos criativos e campanhas",
            "Revisar orçamento disponível"
        ]


# Instância global
agency_mode = AgencyMode()

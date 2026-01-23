# services/elite_ux_system.py
"""
NEXORA PRIME - Sistema de UX de Elite
4 modos de operação: Iniciante, Profissional, Agência, CEO
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class EliteUXSystem:
    """Sistema de UX adaptativo com 4 modos de operação."""
    
    def __init__(self):
        self.user_modes = {}
        self.mode_configurations = {
            "beginner": {
                "name": "Iniciante",
                "description": "Interface simplificada com guias passo a passo",
                "features": {
                    "guided_wizards": True,
                    "tooltips": True,
                    "simplified_metrics": True,
                    "advanced_settings": False,
                    "bulk_operations": False,
                    "api_access": False,
                    "custom_reports": False,
                    "automation_rules": False
                },
                "dashboard_widgets": ["quick_stats", "simple_chart", "tips", "help_center"],
                "menu_items": ["dashboard", "campaigns", "create_campaign", "help"],
                "max_campaigns": 5,
                "complexity_level": 1
            },
            "professional": {
                "name": "Profissional",
                "description": "Acesso completo a todas as ferramentas de otimização",
                "features": {
                    "guided_wizards": False,
                    "tooltips": True,
                    "simplified_metrics": False,
                    "advanced_settings": True,
                    "bulk_operations": True,
                    "api_access": False,
                    "custom_reports": True,
                    "automation_rules": True
                },
                "dashboard_widgets": ["performance_chart", "campaign_table", "alerts", "ab_tests", "competitor_spy"],
                "menu_items": ["dashboard", "campaigns", "create_campaign", "automation", "ab_testing", "reports", "competitor_spy"],
                "max_campaigns": 50,
                "complexity_level": 2
            },
            "agency": {
                "name": "Agência",
                "description": "Gestão multi-cliente com ferramentas de escala",
                "features": {
                    "guided_wizards": False,
                    "tooltips": False,
                    "simplified_metrics": False,
                    "advanced_settings": True,
                    "bulk_operations": True,
                    "api_access": True,
                    "custom_reports": True,
                    "automation_rules": True,
                    "multi_client": True,
                    "white_label": True,
                    "team_management": True
                },
                "dashboard_widgets": ["client_overview", "performance_matrix", "team_tasks", "revenue_tracker", "alerts"],
                "menu_items": ["dashboard", "clients", "campaigns", "automation", "reports", "team", "billing", "api"],
                "max_campaigns": 500,
                "complexity_level": 3
            },
            "ceo": {
                "name": "CEO",
                "description": "Visão executiva com métricas de alto nível",
                "features": {
                    "guided_wizards": False,
                    "tooltips": False,
                    "simplified_metrics": False,
                    "advanced_settings": False,
                    "bulk_operations": False,
                    "api_access": False,
                    "custom_reports": True,
                    "automation_rules": False,
                    "executive_summary": True,
                    "roi_focus": True,
                    "trend_analysis": True,
                    "forecast": True
                },
                "dashboard_widgets": ["executive_summary", "roi_chart", "trend_analysis", "forecast", "key_decisions"],
                "menu_items": ["ceo_dashboard", "reports", "forecast", "decisions"],
                "max_campaigns": None,
                "complexity_level": 4
            }
        }
    
    def set_user_mode(self, user_id: str, mode: str) -> Dict:
        """Define o modo de operação para um usuário."""
        if mode not in self.mode_configurations:
            return {"success": False, "error": f"Modo inválido. Opções: {list(self.mode_configurations.keys())}"}
        
        self.user_modes[user_id] = {
            "mode": mode,
            "set_at": datetime.now().isoformat(),
            "preferences": {}
        }
        
        return {
            "success": True,
            "user_id": user_id,
            "mode": mode,
            "configuration": self.mode_configurations[mode]
        }
    
    def get_user_mode(self, user_id: str) -> Dict:
        """Retorna o modo atual do usuário."""
        user_config = self.user_modes.get(user_id, {"mode": "beginner"})
        mode = user_config["mode"]
        
        return {
            "user_id": user_id,
            "mode": mode,
            "configuration": self.mode_configurations[mode]
        }
    
    def get_interface_config(self, user_id: str) -> Dict:
        """Retorna a configuração de interface para o usuário."""
        user_config = self.get_user_mode(user_id)
        mode_config = user_config["configuration"]
        
        return {
            "mode": user_config["mode"],
            "mode_name": mode_config["name"],
            "features": mode_config["features"],
            "dashboard_widgets": mode_config["dashboard_widgets"],
            "menu_items": mode_config["menu_items"],
            "complexity_level": mode_config["complexity_level"]
        }
    
    def check_feature_access(self, user_id: str, feature: str) -> bool:
        """Verifica se o usuário tem acesso a uma feature específica."""
        user_config = self.get_user_mode(user_id)
        features = user_config["configuration"]["features"]
        return features.get(feature, False)
    
    def get_contextual_help(self, user_id: str, context: str) -> Dict:
        """Retorna ajuda contextual baseada no modo do usuário."""
        user_config = self.get_user_mode(user_id)
        mode = user_config["mode"]
        
        help_content = {
            "beginner": {
                "campaign_creation": {
                    "title": "Criando sua primeira campanha",
                    "steps": [
                        "1. Escolha um objetivo claro (vendas, leads, tráfego)",
                        "2. Defina seu público-alvo",
                        "3. Configure seu orçamento diário",
                        "4. Crie seu anúncio com imagem e texto",
                        "5. Revise e publique"
                    ],
                    "tips": ["Comece com um orçamento pequeno para testar", "Use imagens de alta qualidade"],
                    "video_tutorial": "/tutorials/first-campaign"
                },
                "dashboard": {
                    "title": "Entendendo seu Dashboard",
                    "explanation": "O dashboard mostra o desempenho geral das suas campanhas.",
                    "key_metrics": ["Gastos", "Cliques", "Conversões"]
                }
            },
            "professional": {
                "campaign_creation": {
                    "title": "Criação Avançada de Campanhas",
                    "advanced_options": ["Segmentação por comportamento", "Remarketing", "Lookalike audiences"],
                    "best_practices": ["Teste múltiplas variações", "Use UTMs para tracking"]
                }
            },
            "agency": {
                "campaign_creation": {
                    "title": "Gestão de Campanhas Multi-Cliente",
                    "workflow": ["Selecione o cliente", "Use templates aprovados", "Configure automações"],
                    "efficiency_tips": ["Use bulk operations", "Configure alertas por cliente"]
                }
            },
            "ceo": {
                "dashboard": {
                    "title": "Visão Executiva",
                    "focus": "ROI e tendências de longo prazo",
                    "key_decisions": ["Alocação de orçamento", "Expansão de canais", "Otimização de ROAS"]
                }
            }
        }
        
        mode_help = help_content.get(mode, {})
        context_help = mode_help.get(context, {
            "title": "Ajuda",
            "message": "Conteúdo de ajuda não disponível para este contexto."
        })
        
        return context_help
    
    def get_onboarding_flow(self, user_id: str) -> List[Dict]:
        """Retorna o fluxo de onboarding baseado no modo do usuário."""
        user_config = self.get_user_mode(user_id)
        mode = user_config["mode"]
        
        flows = {
            "beginner": [
                {"step": 1, "title": "Bem-vindo ao NEXORA!", "action": "watch_intro_video"},
                {"step": 2, "title": "Conecte sua conta de anúncios", "action": "connect_ads"},
                {"step": 3, "title": "Crie sua primeira campanha", "action": "create_campaign"},
                {"step": 4, "title": "Entenda suas métricas", "action": "metrics_tour"},
                {"step": 5, "title": "Configure alertas básicos", "action": "setup_alerts"}
            ],
            "professional": [
                {"step": 1, "title": "Configure suas integrações", "action": "setup_integrations"},
                {"step": 2, "title": "Importe campanhas existentes", "action": "import_campaigns"},
                {"step": 3, "title": "Configure automações", "action": "setup_automation"},
                {"step": 4, "title": "Explore ferramentas avançadas", "action": "advanced_tools_tour"}
            ],
            "agency": [
                {"step": 1, "title": "Configure sua agência", "action": "agency_setup"},
                {"step": 2, "title": "Adicione clientes", "action": "add_clients"},
                {"step": 3, "title": "Configure equipe", "action": "team_setup"},
                {"step": 4, "title": "Personalize white-label", "action": "white_label_setup"}
            ],
            "ceo": [
                {"step": 1, "title": "Visão geral executiva", "action": "executive_overview"},
                {"step": 2, "title": "Configure métricas-chave", "action": "kpi_setup"},
                {"step": 3, "title": "Defina alertas de negócio", "action": "business_alerts"}
            ]
        }
        
        return flows.get(mode, flows["beginner"])
    
    def adapt_complexity(self, user_id: str, user_behavior: Dict) -> Dict:
        """Adapta a complexidade da interface baseado no comportamento do usuário."""
        current_mode = self.get_user_mode(user_id)["mode"]
        
        # Analisar comportamento
        actions_count = user_behavior.get("actions_last_30_days", 0)
        advanced_features_used = user_behavior.get("advanced_features_used", 0)
        error_rate = user_behavior.get("error_rate", 0)
        
        recommendation = None
        
        if current_mode == "beginner":
            if actions_count > 100 and advanced_features_used > 10 and error_rate < 0.1:
                recommendation = "professional"
        elif current_mode == "professional":
            if actions_count > 500 and advanced_features_used > 50:
                recommendation = "agency"
        
        return {
            "current_mode": current_mode,
            "recommended_mode": recommendation,
            "analysis": {
                "actions_count": actions_count,
                "advanced_features_used": advanced_features_used,
                "error_rate": error_rate
            }
        }
    
    def get_available_modes(self) -> List[Dict]:
        """Retorna todos os modos disponíveis."""
        return [
            {
                "id": mode_id,
                "name": config["name"],
                "description": config["description"],
                "complexity_level": config["complexity_level"]
            }
            for mode_id, config in self.mode_configurations.items()
        ]
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de UX."""
        mode_distribution = {}
        for user_config in self.user_modes.values():
            mode = user_config["mode"]
            mode_distribution[mode] = mode_distribution.get(mode, 0) + 1
        
        return {
            "total_users": len(self.user_modes),
            "mode_distribution": mode_distribution,
            "available_modes": list(self.mode_configurations.keys())
        }


# Instâncias globais
elite_ux = EliteUXSystem()
elite_ux_system = elite_ux  # Alias para compatibilidade

# Adicionar método get_mode_config como alias
EliteUXSystem.get_mode_config = lambda self, mode: self.mode_configurations.get(mode)

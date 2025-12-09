"""
ORCHESTRATION ENGINE
Motor de orquestração que conecta GPT (estratégia) → Manus (execução) → Nexora (aplicação)
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from services.openai_strategic_engine import OpenAIStrategicEngine
from services.openai_campaign_creator import OpenAICampaignCreator
from services.openai_optimization_engine import OpenAIOptimizationEngine
from services.manus_executor_bridge import ManusExecutorBridge
from services.nexora_automation import NexoraAutomation

class AIOrchestrator:
    """
    Orquestrador de IA
    
    Fluxo:
    1. GPT cria estratégia/campanha
    2. Orchestrator traduz para formato técnico
    3. Manus executa e aplica no Nexora
    4. Nexora usa e vende
    
    Este é o cérebro que coordena todas as IAs
    """
    
    def __init__(self):
        # Inicializar motores
        self.gpt_strategic = OpenAIStrategicEngine()
        self.gpt_campaign = OpenAICampaignCreator()
        self.gpt_optimization = OpenAIOptimizationEngine()
        self.manus_executor = ManusExecutorBridge()
        self.nexora_automation = NexoraAutomation()
        
        self.execution_log = []
        
    def create_and_deploy_campaign(self, campaign_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar e implementar campanha completa
        
        Fluxo completo:
        1. GPT cria estratégia
        2. GPT gera copy
        3. Orchestrator estrutura
        4. Manus aplica no banco
        5. Manus sincroniza com plataformas
        
        Args:
            campaign_request: Solicitação de campanha
            
        Returns:
            Resultado completo
        """
        try:
            execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self._log(execution_id, "Iniciando criação e deploy de campanha")
            
            # ETAPA 1: GPT cria estratégia
            self._log(execution_id, "GPT: Criando estratégia de marketing")
            strategy_result = self.gpt_strategic.create_marketing_strategy(campaign_request)
            
            if not strategy_result.get('success'):
                return {
                    "success": False,
                    "error": "Falha ao criar estratégia",
                    "details": strategy_result
                }
            
            strategy = strategy_result['strategy']
            self._log(execution_id, "GPT: Estratégia criada com sucesso")
            
            # ETAPA 2: GPT gera copy
            self._log(execution_id, "GPT: Gerando copy de anúncios")
            platform = campaign_request.get('platform', 'google')
            copy_result = self.gpt_campaign.generate_campaign_copy(campaign_request, platform)
            
            if not copy_result.get('success'):
                return {
                    "success": False,
                    "error": "Falha ao gerar copy",
                    "details": copy_result
                }
            
            copy_variations = copy_result['variations']
            self._log(execution_id, f"GPT: {len(copy_variations)} variações de copy geradas")
            
            # ETAPA 3: Orchestrator estrutura dados
            self._log(execution_id, "Orchestrator: Estruturando dados para execução")
            structured_campaign = self._structure_campaign_data(
                campaign_request,
                strategy,
                copy_variations
            )
            
            # ETAPA 4: Manus aplica no banco
            self._log(execution_id, "Manus: Aplicando campanha no sistema")
            apply_result = self.manus_executor.apply_campaign(structured_campaign)
            
            if not apply_result.get('success'):
                return {
                    "success": False,
                    "error": "Falha ao aplicar campanha",
                    "details": apply_result
                }
            
            campaign_id = apply_result['campaign_id']
            self._log(execution_id, f"Manus: Campanha aplicada (ID: {campaign_id})")
            
            # ETAPA 5: Manus sincroniza com plataformas
            sync_results = []
            platforms = campaign_request.get('platforms', ['google'])
            
            for platform in platforms:
                self._log(execution_id, f"Manus: Sincronizando com {platform}")
                
                if platform == 'google':
                    sync_result = self.manus_executor.sync_to_google_ads(campaign_id)
                elif platform == 'facebook':
                    sync_result = self.manus_executor.sync_to_facebook_ads(campaign_id)
                else:
                    sync_result = {"success": False, "error": f"Plataforma desconhecida: {platform}"}
                
                sync_results.append(sync_result)
                
                if sync_result.get('success'):
                    self._log(execution_id, f"Manus: Sincronizado com {platform}")
                else:
                    self._log(execution_id, f"Manus: Falha ao sincronizar com {platform}")
            
            # RESULTADO FINAL
            self._log(execution_id, "Campanha criada e implementada com sucesso!")
            
            return {
                "success": True,
                "execution_id": execution_id,
                "campaign_id": campaign_id,
                "strategy": strategy,
                "copy_variations": copy_variations,
                "sync_results": sync_results,
                "execution_log": self._get_log(execution_id),
                "completed_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_id": execution_id if 'execution_id' in locals() else None
            }
    
    def optimize_and_scale(self, campaign_id: int) -> Dict[str, Any]:
        """
        Otimizar e escalar campanha existente
        
        Fluxo:
        1. GPT analisa performance
        2. GPT recomenda otimizações
        3. Orchestrator decide ações
        4. Manus executa otimizações
        
        Args:
            campaign_id: ID da campanha
            
        Returns:
            Resultado da otimização
        """
        try:
            execution_id = f"optim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self._log(execution_id, "Iniciando otimização e escala")
            
            # Buscar dados da campanha
            # (Aqui seria uma consulta real ao banco)
            campaign_data = {
                "id": campaign_id,
                "name": f"Campanha {campaign_id}",
                "impressions": 10000,
                "clicks": 250,
                "ctr": 2.5,
                "conversions": 15,
                "conversion_rate": 6.0,
                "cost": 500,
                "cpc": 2.0,
                "cpa": 33.33,
                "roas": 3.5
            }
            
            # ETAPA 1: GPT analisa performance
            self._log(execution_id, "GPT: Analisando performance da campanha")
            evaluation_result = self.gpt_optimization.evaluate_campaign(campaign_data)
            
            if not evaluation_result.get('success'):
                return {
                    "success": False,
                    "error": "Falha ao avaliar campanha"
                }
            
            evaluation = evaluation_result['evaluation']
            self._log(execution_id, f"GPT: Avaliação concluída (Nota: {evaluation.get('overall_score', 'N/A')})")
            
            # ETAPA 2: GPT recomenda otimizações
            self._log(execution_id, "GPT: Gerando recomendações de otimização")
            recommendation_result = self.gpt_optimization.suggest_scaling_strategy(campaign_data)
            
            if not recommendation_result.get('success'):
                return {
                    "success": False,
                    "error": "Falha ao gerar recomendações"
                }
            
            recommendations = recommendation_result['strategy']
            self._log(execution_id, "GPT: Recomendações geradas")
            
            # ETAPA 3: Orchestrator decide ações
            self._log(execution_id, "Orchestrator: Decidindo ações a executar")
            actions = self._decide_optimization_actions(evaluation, recommendations)
            
            # ETAPA 4: Manus executa otimizações
            execution_results = []
            for action in actions:
                self._log(execution_id, f"Manus: Executando {action['type']}")
                
                result = self.manus_executor.execute_automation(action)
                execution_results.append(result)
                
                if result.get('success'):
                    self._log(execution_id, f"Manus: {action['type']} executado")
                else:
                    self._log(execution_id, f"Manus: Falha em {action['type']}")
            
            return {
                "success": True,
                "execution_id": execution_id,
                "campaign_id": campaign_id,
                "evaluation": evaluation,
                "recommendations": recommendations,
                "actions_executed": execution_results,
                "execution_log": self._get_log(execution_id),
                "completed_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_complete_funnel(self, funnel_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criar funil de vendas completo
        
        Fluxo:
        1. GPT cria estratégia de funil
        2. GPT gera copy para cada estágio
        3. Orchestrator estrutura funil
        4. Manus cria automações
        5. Manus configura no sistema
        
        Args:
            funnel_request: Solicitação de funil
            
        Returns:
            Funil completo
        """
        try:
            execution_id = f"funnel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self._log(execution_id, "Iniciando criação de funil completo")
            
            # ETAPA 1: GPT cria estratégia de funil
            self._log(execution_id, "GPT: Criando estratégia de funil")
            funnel_result = self.gpt_strategic.create_sales_funnel(funnel_request)
            
            if not funnel_result.get('success'):
                return {
                    "success": False,
                    "error": "Falha ao criar funil"
                }
            
            funnel_strategy = funnel_result['funnel']
            self._log(execution_id, "GPT: Estratégia de funil criada")
            
            # ETAPA 2: GPT gera copy para cada estágio
            stages_copy = []
            for stage in funnel_strategy.get('stages', []):
                self._log(execution_id, f"GPT: Gerando copy para estágio {stage.get('name', 'unknown')}")
                
                copy_result = self.gpt_campaign.generate_campaign_copy({
                    "product": funnel_request.get('product'),
                    "audience": funnel_request.get('audience'),
                    "objective": stage.get('objective', 'awareness')
                })
                
                if copy_result.get('success'):
                    stages_copy.append({
                        "stage": stage.get('name'),
                        "copy": copy_result['variations']
                    })
            
            self._log(execution_id, f"GPT: Copy gerado para {len(stages_copy)} estágios")
            
            # ETAPA 3: Orchestrator estrutura funil
            self._log(execution_id, "Orchestrator: Estruturando funil")
            structured_funnel = {
                "name": funnel_request.get('name', 'Novo Funil'),
                "strategy": funnel_strategy,
                "stages_copy": stages_copy,
                "created_at": datetime.now().isoformat()
            }
            
            # ETAPA 4: Manus cria automações
            self._log(execution_id, "Manus: Criando automações do funil")
            automations = []
            
            for stage in funnel_strategy.get('stages', []):
                automation_result = self.nexora_automation.create_automation({
                    "name": f"Automação - {stage.get('name')}",
                    "type": "funnel_stage",
                    "config": stage
                })
                
                if automation_result.get('success'):
                    automations.append(automation_result)
            
            self._log(execution_id, f"Manus: {len(automations)} automações criadas")
            
            return {
                "success": True,
                "execution_id": execution_id,
                "funnel": structured_funnel,
                "automations": automations,
                "execution_log": self._get_log(execution_id),
                "completed_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _structure_campaign_data(self, request: Dict, strategy: Dict, copy: Dict) -> Dict[str, Any]:
        """Estruturar dados da campanha para execução"""
        return {
            "campaign_name": request.get('name', strategy.get('campaign_name', 'Nova Campanha')),
            "objective": request.get('objective', 'CONVERSIONS'),
            "budget": request.get('budget', strategy.get('budget', 100)),
            "platforms": request.get('platforms', ['google']),
            "targeting": strategy.get('targeting', {}),
            "copy_variations": copy.get('variations', []),
            "strategy": strategy
        }
    
    def _decide_optimization_actions(self, evaluation: Dict, recommendations: Dict) -> List[Dict[str, Any]]:
        """Decidir quais ações executar baseado em avaliação e recomendações"""
        actions = []
        
        # Se ROAS baixo, otimizar orçamento
        if evaluation.get('current_roas', 0) < 2.0:
            actions.append({
                "type": "budget_optimization",
                "config": {
                    "threshold_roas": 1.5
                }
            })
        
        # Se há recomendação de escala, escalar
        if recommendations.get('scalability', 0) > 70:
            actions.append({
                "type": "scale_winners",
                "config": {
                    "threshold_roas": 3.0,
                    "scale_factor": 1.3
                }
            })
        
        # Pausar low performers
        actions.append({
            "type": "pause_low_performers",
            "config": {
                "threshold_roas": 1.0
            }
        })
        
        return actions
    
    def _log(self, execution_id: str, message: str):
        """Adicionar entrada ao log de execução"""
        self.execution_log.append({
            "execution_id": execution_id,
            "timestamp": datetime.now().isoformat(),
            "message": message
        })
    
    def _get_log(self, execution_id: str) -> List[Dict[str, Any]]:
        """Obter log de uma execução específica"""
        return [
            log for log in self.execution_log
            if log['execution_id'] == execution_id
        ]
    
    def get_orchestration_status(self) -> Dict[str, Any]:
        """Obter status geral da orquestração"""
        return {
            "gpt_strategic_available": self.gpt_strategic is not None,
            "gpt_campaign_available": self.gpt_campaign is not None,
            "gpt_optimization_available": self.gpt_optimization is not None,
            "manus_executor_available": self.manus_executor is not None,
            "nexora_automation_available": self.nexora_automation is not None,
            "total_executions": len(set(log['execution_id'] for log in self.execution_log)),
            "last_execution": self.execution_log[-1] if self.execution_log else None
        }

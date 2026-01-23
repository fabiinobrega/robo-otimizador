"""
VELYRA PRIME V2 - Sistema de IA Autônoma Avançada
Motor de inteligência artificial para otimização de campanhas publicitárias
Versão: 2.0 - Expansão Avançada
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
import hashlib

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Tipos de agentes autônomos"""
    OPTIMIZER = "optimizer"
    ANALYST = "analyst"
    CREATIVE = "creative"
    BIDDER = "bidder"
    AUDIENCE = "audience"
    BUDGET = "budget"
    SCHEDULER = "scheduler"
    ANOMALY_DETECTOR = "anomaly_detector"

class ActionPriority(Enum):
    """Prioridade das ações"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class OptimizationStrategy(Enum):
    """Estratégias de otimização"""
    AGGRESSIVE = "aggressive"
    BALANCED = "balanced"
    CONSERVATIVE = "conservative"
    LEARNING = "learning"

@dataclass
class AgentAction:
    """Ação executada por um agente"""
    agent_type: AgentType
    action_name: str
    target_entity: str
    parameters: Dict[str, Any]
    priority: ActionPriority
    timestamp: datetime = field(default_factory=datetime.now)
    result: Optional[Dict[str, Any]] = None
    success: bool = False

@dataclass
class CampaignInsight:
    """Insight gerado pela análise de campanha"""
    campaign_id: str
    insight_type: str
    title: str
    description: str
    impact_score: float  # 0-100
    confidence: float  # 0-1
    recommended_action: str
    estimated_improvement: float  # percentual
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class PredictionResult:
    """Resultado de predição de ML"""
    metric: str
    current_value: float
    predicted_value: float
    confidence_interval: Tuple[float, float]
    time_horizon: str
    factors: List[Dict[str, Any]]

class AutonomousAgent:
    """Agente autônomo base"""
    
    def __init__(self, agent_type: AgentType, config: Dict[str, Any] = None):
        self.agent_type = agent_type
        self.config = config or {}
        self.actions_history: List[AgentAction] = []
        self.is_active = True
        self.learning_rate = 0.01
        self.experience_buffer: List[Dict] = []
        
    async def analyze(self, data: Dict[str, Any]) -> List[CampaignInsight]:
        """Analisa dados e gera insights"""
        raise NotImplementedError
        
    async def decide(self, insights: List[CampaignInsight]) -> List[AgentAction]:
        """Decide ações baseado em insights"""
        raise NotImplementedError
        
    async def execute(self, action: AgentAction) -> AgentAction:
        """Executa uma ação"""
        raise NotImplementedError
        
    async def learn(self, action: AgentAction, outcome: Dict[str, Any]):
        """Aprende com o resultado da ação"""
        self.experience_buffer.append({
            "action": action,
            "outcome": outcome,
            "timestamp": datetime.now()
        })
        # Implementar aprendizado por reforço aqui

class OptimizerAgent(AutonomousAgent):
    """Agente de otimização de campanhas"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.OPTIMIZER, config)
        self.optimization_thresholds = {
            "ctr_min": 0.5,
            "cpc_max": 5.0,
            "roas_min": 2.0,
            "conversion_rate_min": 1.0
        }
        
    async def analyze(self, data: Dict[str, Any]) -> List[CampaignInsight]:
        """Analisa performance de campanhas"""
        insights = []
        campaigns = data.get("campaigns", [])
        
        for campaign in campaigns:
            # Análise de CTR
            ctr = campaign.get("ctr", 0)
            if ctr < self.optimization_thresholds["ctr_min"]:
                insights.append(CampaignInsight(
                    campaign_id=campaign.get("id", ""),
                    insight_type="low_ctr",
                    title="CTR Abaixo do Esperado",
                    description=f"CTR atual ({ctr:.2f}%) está abaixo do mínimo recomendado ({self.optimization_thresholds['ctr_min']}%)",
                    impact_score=85,
                    confidence=0.92,
                    recommended_action="Revisar criativos e segmentação",
                    estimated_improvement=25.0
                ))
            
            # Análise de ROAS
            roas = campaign.get("roas", 0)
            if roas < self.optimization_thresholds["roas_min"]:
                insights.append(CampaignInsight(
                    campaign_id=campaign.get("id", ""),
                    insight_type="low_roas",
                    title="ROAS Precisa de Atenção",
                    description=f"ROAS atual ({roas:.2f}x) está abaixo da meta ({self.optimization_thresholds['roas_min']}x)",
                    impact_score=95,
                    confidence=0.88,
                    recommended_action="Otimizar lances e público-alvo",
                    estimated_improvement=35.0
                ))
            
            # Análise de CPC
            cpc = campaign.get("cpc", 0)
            if cpc > self.optimization_thresholds["cpc_max"]:
                insights.append(CampaignInsight(
                    campaign_id=campaign.get("id", ""),
                    insight_type="high_cpc",
                    title="CPC Elevado",
                    description=f"CPC atual (R$ {cpc:.2f}) está acima do máximo recomendado (R$ {self.optimization_thresholds['cpc_max']:.2f})",
                    impact_score=75,
                    confidence=0.95,
                    recommended_action="Ajustar estratégia de lances",
                    estimated_improvement=20.0
                ))
                
        return insights
    
    async def decide(self, insights: List[CampaignInsight]) -> List[AgentAction]:
        """Decide ações de otimização"""
        actions = []
        
        for insight in insights:
            if insight.impact_score >= 80:
                priority = ActionPriority.HIGH
            elif insight.impact_score >= 60:
                priority = ActionPriority.MEDIUM
            else:
                priority = ActionPriority.LOW
                
            if insight.insight_type == "low_ctr":
                actions.append(AgentAction(
                    agent_type=self.agent_type,
                    action_name="optimize_creatives",
                    target_entity=insight.campaign_id,
                    parameters={
                        "action": "refresh_creatives",
                        "test_new_headlines": True,
                        "test_new_images": True
                    },
                    priority=priority
                ))
            elif insight.insight_type == "low_roas":
                actions.append(AgentAction(
                    agent_type=self.agent_type,
                    action_name="optimize_bidding",
                    target_entity=insight.campaign_id,
                    parameters={
                        "action": "adjust_bids",
                        "strategy": "target_roas",
                        "target_value": self.optimization_thresholds["roas_min"]
                    },
                    priority=priority
                ))
            elif insight.insight_type == "high_cpc":
                actions.append(AgentAction(
                    agent_type=self.agent_type,
                    action_name="reduce_cpc",
                    target_entity=insight.campaign_id,
                    parameters={
                        "action": "lower_bids",
                        "reduction_percentage": 15,
                        "maintain_position": True
                    },
                    priority=priority
                ))
                
        return actions
    
    async def execute(self, action: AgentAction) -> AgentAction:
        """Executa ação de otimização"""
        try:
            logger.info(f"Executando ação: {action.action_name} para {action.target_entity}")
            
            # Simulação de execução - em produção, conectar com APIs reais
            await asyncio.sleep(0.1)
            
            action.result = {
                "status": "success",
                "message": f"Ação {action.action_name} executada com sucesso",
                "changes_applied": action.parameters,
                "execution_time": datetime.now().isoformat()
            }
            action.success = True
            
        except Exception as e:
            action.result = {"status": "error", "message": str(e)}
            action.success = False
            
        self.actions_history.append(action)
        return action

class BidderAgent(AutonomousAgent):
    """Agente de otimização de lances em tempo real"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.BIDDER, config)
        self.bid_strategies = {
            "maximize_conversions": self._maximize_conversions,
            "target_cpa": self._target_cpa,
            "target_roas": self._target_roas,
            "maximize_clicks": self._maximize_clicks
        }
        
    async def _maximize_conversions(self, campaign: Dict) -> float:
        """Calcula lance para maximizar conversões"""
        historical_cpa = campaign.get("cpa", 10)
        conversion_rate = campaign.get("conversion_rate", 2) / 100
        target_conversions = campaign.get("target_conversions", 100)
        
        optimal_bid = historical_cpa * conversion_rate * 1.1
        return min(optimal_bid, campaign.get("max_bid", 50))
    
    async def _target_cpa(self, campaign: Dict) -> float:
        """Calcula lance para atingir CPA alvo"""
        target_cpa = campaign.get("target_cpa", 15)
        current_cpa = campaign.get("cpa", 20)
        
        if current_cpa > target_cpa:
            adjustment = 0.9  # Reduzir lance
        else:
            adjustment = 1.05  # Aumentar lance levemente
            
        return campaign.get("current_bid", 5) * adjustment
    
    async def _target_roas(self, campaign: Dict) -> float:
        """Calcula lance para atingir ROAS alvo"""
        target_roas = campaign.get("target_roas", 3)
        current_roas = campaign.get("roas", 2)
        avg_order_value = campaign.get("avg_order_value", 100)
        
        optimal_bid = avg_order_value / target_roas
        return optimal_bid
    
    async def _maximize_clicks(self, campaign: Dict) -> float:
        """Calcula lance para maximizar cliques"""
        budget = campaign.get("daily_budget", 100)
        avg_cpc = campaign.get("cpc", 2)
        
        return avg_cpc * 0.95  # Ligeiramente abaixo para mais cliques
    
    async def analyze(self, data: Dict[str, Any]) -> List[CampaignInsight]:
        """Analisa oportunidades de otimização de lances"""
        insights = []
        campaigns = data.get("campaigns", [])
        
        for campaign in campaigns:
            bid_strategy = campaign.get("bid_strategy", "maximize_conversions")
            current_performance = campaign.get("performance_score", 50)
            
            if current_performance < 70:
                insights.append(CampaignInsight(
                    campaign_id=campaign.get("id", ""),
                    insight_type="bid_optimization_needed",
                    title="Otimização de Lances Necessária",
                    description=f"Performance atual ({current_performance}%) indica necessidade de ajuste de lances",
                    impact_score=80,
                    confidence=0.85,
                    recommended_action=f"Aplicar estratégia {bid_strategy}",
                    estimated_improvement=15.0
                ))
                
        return insights
    
    async def decide(self, insights: List[CampaignInsight]) -> List[AgentAction]:
        """Decide ajustes de lances"""
        actions = []
        
        for insight in insights:
            actions.append(AgentAction(
                agent_type=self.agent_type,
                action_name="adjust_bid",
                target_entity=insight.campaign_id,
                parameters={
                    "strategy": "dynamic",
                    "adjustment_type": "automatic"
                },
                priority=ActionPriority.HIGH
            ))
            
        return actions
    
    async def execute(self, action: AgentAction) -> AgentAction:
        """Executa ajuste de lance"""
        try:
            logger.info(f"Ajustando lance para campanha: {action.target_entity}")
            await asyncio.sleep(0.05)
            
            action.result = {
                "status": "success",
                "new_bid": random.uniform(1, 10),
                "previous_bid": random.uniform(1, 10),
                "adjustment_reason": "Otimização automática baseada em performance"
            }
            action.success = True
            
        except Exception as e:
            action.result = {"status": "error", "message": str(e)}
            action.success = False
            
        return action

class AudienceAgent(AutonomousAgent):
    """Agente de otimização de público-alvo"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.AUDIENCE, config)
        self.audience_segments = []
        self.lookalike_threshold = 0.7
        
    async def analyze(self, data: Dict[str, Any]) -> List[CampaignInsight]:
        """Analisa performance de públicos"""
        insights = []
        audiences = data.get("audiences", [])
        
        for audience in audiences:
            performance = audience.get("performance_score", 50)
            size = audience.get("size", 0)
            
            if performance < 60 and size > 10000:
                insights.append(CampaignInsight(
                    campaign_id=audience.get("campaign_id", ""),
                    insight_type="audience_refinement",
                    title="Público Precisa de Refinamento",
                    description=f"Público '{audience.get('name', 'Desconhecido')}' tem baixa performance ({performance}%)",
                    impact_score=70,
                    confidence=0.82,
                    recommended_action="Criar segmentação mais específica",
                    estimated_improvement=25.0
                ))
                
        return insights
    
    async def decide(self, insights: List[CampaignInsight]) -> List[AgentAction]:
        """Decide ações de otimização de público"""
        actions = []
        
        for insight in insights:
            actions.append(AgentAction(
                agent_type=self.agent_type,
                action_name="refine_audience",
                target_entity=insight.campaign_id,
                parameters={
                    "action": "create_lookalike",
                    "source": "top_converters",
                    "similarity": self.lookalike_threshold
                },
                priority=ActionPriority.MEDIUM
            ))
            
        return actions
    
    async def execute(self, action: AgentAction) -> AgentAction:
        """Executa refinamento de público"""
        try:
            logger.info(f"Refinando público para: {action.target_entity}")
            await asyncio.sleep(0.1)
            
            action.result = {
                "status": "success",
                "new_audience_id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
                "estimated_reach": random.randint(50000, 500000)
            }
            action.success = True
            
        except Exception as e:
            action.result = {"status": "error", "message": str(e)}
            action.success = False
            
        return action

class AnomalyDetectorAgent(AutonomousAgent):
    """Agente de detecção de anomalias"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.ANOMALY_DETECTOR, config)
        self.sensitivity = 2.0  # Desvios padrão
        self.metrics_baseline: Dict[str, Dict] = {}
        
    async def analyze(self, data: Dict[str, Any]) -> List[CampaignInsight]:
        """Detecta anomalias em métricas"""
        insights = []
        metrics = data.get("metrics", {})
        
        for metric_name, values in metrics.items():
            if isinstance(values, list) and len(values) > 5:
                mean = sum(values) / len(values)
                variance = sum((x - mean) ** 2 for x in values) / len(values)
                std_dev = variance ** 0.5
                
                latest = values[-1]
                z_score = (latest - mean) / std_dev if std_dev > 0 else 0
                
                if abs(z_score) > self.sensitivity:
                    anomaly_type = "spike" if z_score > 0 else "drop"
                    insights.append(CampaignInsight(
                        campaign_id=data.get("campaign_id", ""),
                        insight_type=f"anomaly_{anomaly_type}",
                        title=f"Anomalia Detectada: {metric_name}",
                        description=f"Valor atual ({latest:.2f}) está {abs(z_score):.1f} desvios padrão da média ({mean:.2f})",
                        impact_score=90,
                        confidence=0.95,
                        recommended_action="Investigar causa da anomalia",
                        estimated_improvement=0
                    ))
                    
        return insights
    
    async def decide(self, insights: List[CampaignInsight]) -> List[AgentAction]:
        """Decide ações para anomalias"""
        actions = []
        
        for insight in insights:
            if "spike" in insight.insight_type:
                # Anomalia positiva - investigar e potencialmente escalar
                actions.append(AgentAction(
                    agent_type=self.agent_type,
                    action_name="investigate_positive_anomaly",
                    target_entity=insight.campaign_id,
                    parameters={"action": "analyze_and_scale"},
                    priority=ActionPriority.HIGH
                ))
            else:
                # Anomalia negativa - alerta e possível pausa
                actions.append(AgentAction(
                    agent_type=self.agent_type,
                    action_name="alert_negative_anomaly",
                    target_entity=insight.campaign_id,
                    parameters={"action": "alert_and_monitor"},
                    priority=ActionPriority.CRITICAL
                ))
                
        return actions
    
    async def execute(self, action: AgentAction) -> AgentAction:
        """Executa resposta a anomalia"""
        try:
            logger.info(f"Respondendo a anomalia: {action.action_name}")
            await asyncio.sleep(0.05)
            
            action.result = {
                "status": "success",
                "alert_sent": True,
                "action_taken": action.parameters.get("action")
            }
            action.success = True
            
        except Exception as e:
            action.result = {"status": "error", "message": str(e)}
            action.success = False
            
        return action

class VelyraPrimeV2:
    """
    Motor principal de IA Autônoma - Velyra Prime V2
    Coordena múltiplos agentes para otimização de campanhas
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agents: Dict[AgentType, AutonomousAgent] = {}
        self.is_running = False
        self.optimization_strategy = OptimizationStrategy.BALANCED
        self.actions_queue: List[AgentAction] = []
        self.insights_cache: List[CampaignInsight] = []
        self.performance_history: List[Dict] = []
        self.total_optimizations = 0
        self.total_improvements = 0.0
        
        # Inicializar agentes
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Inicializa todos os agentes autônomos"""
        self.agents[AgentType.OPTIMIZER] = OptimizerAgent(self.config)
        self.agents[AgentType.BIDDER] = BidderAgent(self.config)
        self.agents[AgentType.AUDIENCE] = AudienceAgent(self.config)
        self.agents[AgentType.ANOMALY_DETECTOR] = AnomalyDetectorAgent(self.config)
        
        logger.info(f"Velyra Prime V2 inicializada com {len(self.agents)} agentes")
        
    async def start(self):
        """Inicia o motor de otimização"""
        self.is_running = True
        logger.info("Velyra Prime V2 iniciada")
        
    async def stop(self):
        """Para o motor de otimização"""
        self.is_running = False
        logger.info("Velyra Prime V2 parada")
        
    async def analyze_campaigns(self, campaigns_data: List[Dict]) -> List[CampaignInsight]:
        """Analisa campanhas com todos os agentes"""
        all_insights = []
        
        for agent_type, agent in self.agents.items():
            try:
                insights = await agent.analyze({"campaigns": campaigns_data})
                all_insights.extend(insights)
            except Exception as e:
                logger.error(f"Erro no agente {agent_type}: {e}")
                
        # Ordenar por impacto
        all_insights.sort(key=lambda x: x.impact_score, reverse=True)
        self.insights_cache = all_insights
        
        return all_insights
    
    async def generate_optimization_plan(self, insights: List[CampaignInsight]) -> List[AgentAction]:
        """Gera plano de otimização baseado em insights"""
        all_actions = []
        
        for agent_type, agent in self.agents.items():
            try:
                relevant_insights = [i for i in insights if self._is_relevant_for_agent(i, agent_type)]
                actions = await agent.decide(relevant_insights)
                all_actions.extend(actions)
            except Exception as e:
                logger.error(f"Erro ao gerar ações do agente {agent_type}: {e}")
                
        # Ordenar por prioridade
        all_actions.sort(key=lambda x: x.priority.value)
        self.actions_queue = all_actions
        
        return all_actions
    
    def _is_relevant_for_agent(self, insight: CampaignInsight, agent_type: AgentType) -> bool:
        """Verifica se insight é relevante para o agente"""
        relevance_map = {
            AgentType.OPTIMIZER: ["low_ctr", "low_roas", "high_cpc"],
            AgentType.BIDDER: ["bid_optimization_needed", "high_cpc"],
            AgentType.AUDIENCE: ["audience_refinement", "low_conversion"],
            AgentType.ANOMALY_DETECTOR: ["anomaly_spike", "anomaly_drop"]
        }
        
        return insight.insight_type in relevance_map.get(agent_type, [])
    
    async def execute_optimizations(self, actions: List[AgentAction] = None) -> List[AgentAction]:
        """Executa otimizações planejadas"""
        actions = actions or self.actions_queue
        executed_actions = []
        
        for action in actions:
            agent = self.agents.get(action.agent_type)
            if agent:
                try:
                    result = await agent.execute(action)
                    executed_actions.append(result)
                    
                    if result.success:
                        self.total_optimizations += 1
                        
                except Exception as e:
                    logger.error(f"Erro ao executar ação {action.action_name}: {e}")
                    
        return executed_actions
    
    async def run_optimization_cycle(self, campaigns_data: List[Dict]) -> Dict[str, Any]:
        """Executa um ciclo completo de otimização"""
        cycle_start = datetime.now()
        
        # 1. Análise
        insights = await self.analyze_campaigns(campaigns_data)
        
        # 2. Planejamento
        actions = await self.generate_optimization_plan(insights)
        
        # 3. Execução
        executed = await self.execute_optimizations(actions)
        
        # 4. Registro
        cycle_result = {
            "cycle_id": hashlib.md5(str(cycle_start).encode()).hexdigest()[:8],
            "start_time": cycle_start.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - cycle_start).total_seconds(),
            "insights_generated": len(insights),
            "actions_planned": len(actions),
            "actions_executed": len([a for a in executed if a.success]),
            "actions_failed": len([a for a in executed if not a.success]),
            "top_insights": [
                {
                    "title": i.title,
                    "impact": i.impact_score,
                    "campaign": i.campaign_id
                } for i in insights[:5]
            ]
        }
        
        self.performance_history.append(cycle_result)
        
        return cycle_result
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do sistema"""
        return {
            "is_running": self.is_running,
            "strategy": self.optimization_strategy.value,
            "agents_active": len(self.agents),
            "total_optimizations": self.total_optimizations,
            "pending_actions": len(self.actions_queue),
            "cached_insights": len(self.insights_cache),
            "last_cycle": self.performance_history[-1] if self.performance_history else None
        }
    
    def get_insights_summary(self) -> Dict[str, Any]:
        """Retorna resumo dos insights"""
        if not self.insights_cache:
            return {"total": 0, "by_type": {}, "by_priority": {}}
            
        by_type = {}
        for insight in self.insights_cache:
            by_type[insight.insight_type] = by_type.get(insight.insight_type, 0) + 1
            
        return {
            "total": len(self.insights_cache),
            "by_type": by_type,
            "avg_impact": sum(i.impact_score for i in self.insights_cache) / len(self.insights_cache),
            "high_priority": len([i for i in self.insights_cache if i.impact_score >= 80])
        }


# Instância global
velyra_prime_v2 = VelyraPrimeV2()


# Funções de conveniência para uso nas rotas
async def get_velyra_status() -> Dict[str, Any]:
    """Retorna status da Velyra Prime V2"""
    return velyra_prime_v2.get_status()

async def run_optimization(campaigns: List[Dict]) -> Dict[str, Any]:
    """Executa otimização para campanhas"""
    return await velyra_prime_v2.run_optimization_cycle(campaigns)

async def get_insights() -> List[Dict[str, Any]]:
    """Retorna insights atuais"""
    return [
        {
            "campaign_id": i.campaign_id,
            "type": i.insight_type,
            "title": i.title,
            "description": i.description,
            "impact": i.impact_score,
            "confidence": i.confidence,
            "action": i.recommended_action,
            "improvement": i.estimated_improvement
        }
        for i in velyra_prime_v2.insights_cache
    ]


# Métodos adicionais para compatibilidade com rotas V2
def get_system_status(self=None) -> Dict[str, Any]:
    """Retorna status completo do sistema Velyra Prime V2"""
    return {
        "status": "active",
        "version": "2.0.0",
        "is_running": velyra_prime_v2.is_running,
        "strategy": velyra_prime_v2.optimization_strategy.value,
        "agents": {
            agent_type.value: {
                "status": "active",
                "type": agent_type.value,
                "config": agent.config
            }
            for agent_type, agent in velyra_prime_v2.agents.items()
        },
        "agents_count": len(velyra_prime_v2.agents),
        "total_optimizations": velyra_prime_v2.total_optimizations,
        "pending_actions": len(velyra_prime_v2.actions_queue),
        "cached_insights": len(velyra_prime_v2.insights_cache),
        "last_cycle": velyra_prime_v2.performance_history[-1] if velyra_prime_v2.performance_history else None,
        "capabilities": [
            "campaign_analysis",
            "bid_optimization",
            "audience_refinement",
            "anomaly_detection",
            "performance_prediction",
            "automated_optimization"
        ]
    }

def get_active_agents(self=None) -> Dict[str, Any]:
    """Retorna lista de agentes de IA ativos"""
    return {
        "agents": [
            {
                "id": agent_type.value,
                "name": agent_type.name,
                "type": agent_type.value,
                "status": "active",
                "description": _get_agent_description(agent_type),
                "capabilities": _get_agent_capabilities(agent_type)
            }
            for agent_type in velyra_prime_v2.agents.keys()
        ],
        "total_agents": len(velyra_prime_v2.agents),
        "system_status": "active"
    }

def _get_agent_description(agent_type: AgentType) -> str:
    """Retorna descrição do agente"""
    descriptions = {
        AgentType.OPTIMIZER: "Agente de otimização geral de campanhas",
        AgentType.BIDDER: "Agente de otimização de lances e orçamento",
        AgentType.AUDIENCE: "Agente de refinamento de audiência",
        AgentType.ANOMALY_DETECTOR: "Agente de detecção de anomalias"
    }
    return descriptions.get(agent_type, "Agente de IA")

def _get_agent_capabilities(agent_type: AgentType) -> List[str]:
    """Retorna capacidades do agente"""
    capabilities = {
        AgentType.OPTIMIZER: ["analyze_performance", "suggest_optimizations", "auto_optimize"],
        AgentType.BIDDER: ["bid_analysis", "budget_optimization", "cpc_management"],
        AgentType.AUDIENCE: ["audience_analysis", "segment_refinement", "lookalike_creation"],
        AgentType.ANOMALY_DETECTOR: ["spike_detection", "drop_detection", "trend_analysis"]
    }
    return capabilities.get(agent_type, [])

# Adicionar métodos à classe VelyraPrimeV2
VelyraPrimeV2.get_system_status = get_system_status
VelyraPrimeV2.get_active_agents = get_active_agents

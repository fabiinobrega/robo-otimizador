"""
MANUS CREDIT TRACKER - Controle de Créditos Manus
==================================================

Rastreia e gerencia o consumo de créditos do Manus IA.

Funcionalidades:
- Registrar uso de créditos
- Consultar créditos restantes
- Bloquear operações se sem créditos
- Gerar relatórios de consumo
- Calcular ROI por uso de créditos

Autor: Manus AI
Data: 13 de Janeiro de 2026
"""

import logging
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Tipos de ação que consomem créditos"""
    SIMILARWEB_INSIGHT = "similarweb_insight"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    COPYWRITING = "copywriting"
    CAMPAIGN_OPTIMIZATION = "campaign_optimization"
    MARKET_RESEARCH = "market_research"


class ManusCreditTracker:
    """
    Rastreador de créditos Manus IA.
    
    Gerencia o consumo de créditos e fornece insights sobre uso.
    """
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        self.usage_log = []  # In-memory log (substituir por DB em produção)
        
        # Configurações
        self.credits_per_action = {
            ActionType.SIMILARWEB_INSIGHT: 1,
            ActionType.COMPETITOR_ANALYSIS: 2,
            ActionType.COPYWRITING: 1,
            ActionType.CAMPAIGN_OPTIMIZATION: 3,
            ActionType.MARKET_RESEARCH: 2
        }
        
        logger.info("💳 Manus Credit Tracker inicializado")
    
    def log_credit_usage(
        self,
        action_type: ActionType,
        context: Dict,
        credits_used: Optional[int] = None
    ) -> Dict:
        """
        Registra uso de créditos.
        
        Args:
            action_type: Tipo de ação executada
            context: Contexto da ação (produto, domínio, campanha, etc.)
            credits_used: Créditos usados (se None, usa valor padrão)
            
        Returns:
            Registro criado
        """
        if credits_used is None:
            credits_used = self.credits_per_action.get(action_type, 1)
        
        record = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type.value,
            'credits_used': credits_used,
            'context': context
        }
        
        self.usage_log.append(record)
        
        logger.info(f"💳 Créditos usados: {credits_used} ({action_type.value})")
        
        # TODO: Salvar no banco de dados
        # if self.db:
        #     self._save_to_database(record)
        
        return record
    
    def get_total_credits_used(self, timeframe: Optional[str] = None) -> int:
        """
        Retorna total de créditos usados.
        
        Args:
            timeframe: Período ('today', '7d', '30d', 'all')
            
        Returns:
            Total de créditos
        """
        if timeframe:
            filtered_log = self._filter_by_timeframe(self.usage_log, timeframe)
        else:
            filtered_log = self.usage_log
        
        total = sum(record['credits_used'] for record in filtered_log)
        
        return total
    
    def get_credits_by_action_type(self, timeframe: Optional[str] = None) -> Dict[str, int]:
        """
        Retorna créditos usados por tipo de ação.
        
        Args:
            timeframe: Período ('today', '7d', '30d', 'all')
            
        Returns:
            Dicionário {action_type: credits}
        """
        if timeframe:
            filtered_log = self._filter_by_timeframe(self.usage_log, timeframe)
        else:
            filtered_log = self.usage_log
        
        breakdown = {}
        for record in filtered_log:
            action_type = record['action_type']
            credits = record['credits_used']
            
            if action_type not in breakdown:
                breakdown[action_type] = 0
            
            breakdown[action_type] += credits
        
        return breakdown
    
    def get_usage_report(self, timeframe: str = '30d') -> Dict:
        """
        Gera relatório de uso de créditos.
        
        Args:
            timeframe: Período ('today', '7d', '30d', 'all')
            
        Returns:
            Relatório completo
        """
        filtered_log = self._filter_by_timeframe(self.usage_log, timeframe)
        
        total_credits = sum(record['credits_used'] for record in filtered_log)
        breakdown = self.get_credits_by_action_type(timeframe)
        
        # Top actions
        top_actions = sorted(
            breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Daily average
        if timeframe == 'today':
            days = 1
        elif timeframe == '7d':
            days = 7
        elif timeframe == '30d':
            days = 30
        else:
            days = max(1, len(set(r['timestamp'][:10] for r in filtered_log)))
        
        daily_avg = total_credits / days if days > 0 else 0
        
        return {
            'timeframe': timeframe,
            'total_credits_used': total_credits,
            'daily_average': round(daily_avg, 2),
            'breakdown_by_action': breakdown,
            'top_actions': top_actions,
            'total_actions': len(filtered_log),
            'report_generated_at': datetime.now().isoformat()
        }
    
    def check_credits_available(self, required_credits: int = 1) -> bool:
        """
        Verifica se há créditos disponíveis.
        
        NOTA: Esta é uma implementação simplificada.
        Em produção, deve consultar o saldo real da conta Manus.
        
        Args:
            required_credits: Créditos necessários
            
        Returns:
            True se há créditos suficientes
        """
        # TODO: Implementar consulta real ao saldo Manus
        # Por enquanto, sempre retorna True (modo desenvolvimento)
        
        logger.info(f"💳 Verificando créditos: {required_credits} necessários")
        return True
    
    def get_roi_by_credits(self, timeframe: str = '30d') -> Dict:
        """
        Calcula ROI gerado por uso de créditos Manus.
        
        Args:
            timeframe: Período de análise
            
        Returns:
            Análise de ROI
        """
        filtered_log = self._filter_by_timeframe(self.usage_log, timeframe)
        
        total_credits = sum(record['credits_used'] for record in filtered_log)
        
        # TODO: Calcular ROI real baseado em resultados de campanhas
        # Por enquanto, retorna estimativa
        
        # Estimativa: cada crédito gera R$ 50 em valor
        estimated_value_per_credit = 50.0
        estimated_total_value = total_credits * estimated_value_per_credit
        
        # Custo estimado por crédito: R$ 2
        estimated_cost_per_credit = 2.0
        estimated_total_cost = total_credits * estimated_cost_per_credit
        
        estimated_roi = (estimated_total_value / estimated_total_cost) if estimated_total_cost > 0 else 0
        
        return {
            'timeframe': timeframe,
            'total_credits_used': total_credits,
            'estimated_cost': estimated_total_cost,
            'estimated_value_generated': estimated_total_value,
            'estimated_roi': round(estimated_roi, 2),
            'note': 'Valores estimados - ROI real depende de resultados de campanhas'
        }
    
    def _filter_by_timeframe(self, log: List[Dict], timeframe: str) -> List[Dict]:
        """Filtra log por período de tempo"""
        now = datetime.now()
        
        if timeframe == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeframe == '7d':
            start = now - timedelta(days=7)
        elif timeframe == '30d':
            start = now - timedelta(days=30)
        else:  # 'all'
            return log
        
        filtered = [
            record for record in log
            if datetime.fromisoformat(record['timestamp']) >= start
        ]
        
        return filtered
    
    def _save_to_database(self, record: Dict):
        """Salva registro no banco de dados"""
        # TODO: Implementar persistência em banco
        pass
    
    def get_dashboard_metrics(self) -> Dict:
        """
        Retorna métricas para exibição no CEO Dashboard.
        
        Returns:
            Métricas formatadas para dashboard
        """
        # Créditos usados hoje
        today_credits = self.get_total_credits_used('today')
        
        # Créditos usados últimos 7 dias
        week_credits = self.get_total_credits_used('7d')
        
        # Créditos usados últimos 30 dias
        month_credits = self.get_total_credits_used('30d')
        
        # Breakdown por ação (últimos 30 dias)
        breakdown = self.get_credits_by_action_type('30d')
        
        # ROI estimado
        roi_data = self.get_roi_by_credits('30d')
        
        return {
            'credits_today': today_credits,
            'credits_week': week_credits,
            'credits_month': month_credits,
            'breakdown': breakdown,
            'roi_estimate': roi_data['estimated_roi'],
            'value_generated': roi_data['estimated_value_generated']
        }


# Singleton instance
manus_credit_tracker = ManusCreditTracker()

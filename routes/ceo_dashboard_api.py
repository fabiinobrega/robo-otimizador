"""
🎯 CEO DASHBOARD API - Endpoints para Dashboard Operacional
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fornece dados em tempo real para o CEO Dashboard.

Autor: Manus AI
Data: 05 de Janeiro de 2026
"""

from flask import Blueprint, jsonify, render_template
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

ceo_dashboard_bp = Blueprint('ceo_dashboard', __name__)


@ceo_dashboard_bp.route('/ceo-dashboard')
def ceo_dashboard():
    """Renderiza o CEO Dashboard"""
    return render_template('ceo_dashboard.html')


@ceo_dashboard_bp.route('/api/ceo-dashboard/status')
def get_dashboard_status():
    """
    Retorna status completo do dashboard
    
    Returns:
        JSON com status do Manus, métricas, campanhas e decisões
    """
    try:
        from services.manus_agent import get_agent
        
        agent = get_agent()
        agent_status = agent.get_status()
        
        # Calcular uptime
        uptime_seconds = agent_status.get('uptime_seconds', 0)
        uptime_hours = uptime_seconds // 3600
        uptime_minutes = (uptime_seconds % 3600) // 60
        uptime_str = f"{uptime_hours}h {uptime_minutes}m"
        
        # Status do Manus
        manus_data = {
            'status': 'ATIVO' if agent_status.get('is_active') else 'INATIVO',
            'uptime': uptime_str,
            'last_decision': _get_last_decision(),
            'next_action': _get_next_action(),
            'tasks_completed': agent_status.get('tasks_completed', 0),
            'tasks_failed': agent_status.get('tasks_failed', 0)
        }
        
        # Métricas principais
        metrics_data = {
            'active_campaigns': _get_active_campaigns_count(),
            'roas': _get_average_roas(),
            'spend': _get_today_spend(),
            'revenue': _get_today_revenue()
        }
        
        # Campanhas ativas
        campaigns_data = _get_active_campaigns_list()
        
        # Histórico de decisões
        decisions_data = _get_recent_decisions()
        
        # Metas vs Progresso
        goals_data = _get_goals_progress()
        
        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'manus': manus_data,
            'metrics': metrics_data,
            'campaigns': campaigns_data,
            'decisions': decisions_data,
            'goals': goals_data
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Erro ao buscar status do dashboard: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _get_last_decision() -> str:
    """Retorna a última decisão tomada pelo Manus"""
    # TODO: Buscar do banco de dados
    return "Pausou campanha #12345 (ROAS < 1.2)"


def _get_next_action() -> str:
    """Retorna a próxima ação planejada"""
    # TODO: Buscar da fila de tarefas
    return "Otimização de campanha #12346 em 15min"


def _get_active_campaigns_count() -> int:
    """Retorna número de campanhas ativas"""
    # TODO: Buscar do banco de dados
    return 3


def _get_average_roas() -> float:
    """Retorna ROAS médio das campanhas ativas"""
    # TODO: Calcular do banco de dados
    return 2.5


def _get_today_spend() -> float:
    """Retorna gasto total de hoje"""
    # TODO: Buscar do banco de dados
    return 150.00


def _get_today_revenue() -> float:
    """Retorna receita total de hoje"""
    # TODO: Buscar do banco de dados
    return 375.00


def _get_active_campaigns_list() -> list:
    """Retorna lista de campanhas ativas"""
    # TODO: Buscar do banco de dados
    return [
        {
            'id': 1,
            'name': 'Campanha DURASIL - Conversão',
            'platform': 'Facebook Ads',
            'status': 'ACTIVE',
            'roas': 2.8,
            'spend': 50.00,
            'revenue': 140.00
        },
        {
            'id': 2,
            'name': 'Campanha KIT CAPILAR - Tráfego',
            'platform': 'Facebook Ads',
            'status': 'ACTIVE',
            'roas': 2.3,
            'spend': 75.00,
            'revenue': 172.50
        },
        {
            'id': 3,
            'name': 'Campanha DIURIEFIT - Retargeting',
            'platform': 'Facebook Ads',
            'status': 'PAUSED',
            'roas': 1.1,
            'spend': 25.00,
            'revenue': 27.50
        }
    ]


def _get_recent_decisions() -> list:
    """Retorna histórico recente de decisões"""
    # TODO: Buscar do banco de dados
    now = datetime.now()
    
    return [
        {
            'time': (now - timedelta(minutes=5)).strftime('%H:%M'),
            'action': 'Otimizou campanha #12346',
            'reason': 'CTR caiu para 1.2%, ajustou público-alvo'
        },
        {
            'time': (now - timedelta(minutes=30)).strftime('%H:%M'),
            'action': 'Pausou criativo #789',
            'reason': 'Frequência > 3.0, saturação detectada'
        },
        {
            'time': (now - timedelta(hours=1)).strftime('%H:%M'),
            'action': 'Escalou campanha #12345',
            'reason': 'ROAS estável em 2.8x por 72h, aumentou budget em 20%'
        },
        {
            'time': (now - timedelta(hours=2)).strftime('%H:%M'),
            'action': 'Criou teste A/B #456',
            'reason': 'Testando novo ângulo de copy'
        },
        {
            'time': (now - timedelta(hours=3)).strftime('%H:%M'),
            'action': 'Pausou campanha #12344',
            'reason': 'ROI negativo por 48h consecutivas'
        }
    ]


def _get_goals_progress() -> dict:
    """Retorna progresso das metas"""
    # TODO: Buscar do banco de dados e calcular
    return {
        'sales': {
            'target': 50,
            'current': 30,
            'progress': 60
        },
        'roas': {
            'target': 3.0,
            'current': 2.5,
            'progress': 83
        },
        'revenue': {
            'target': 50000,
            'current': 22500,
            'progress': 45
        }
    }

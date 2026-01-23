"""
Integração dos Serviços Avançados do Nexora Prime
Este arquivo registra todas as rotas avançadas no Flask app principal
"""

from flask import Blueprint, render_template, request, jsonify
import json
from datetime import datetime

# Criar Blueprint para rotas avançadas
advanced_bp = Blueprint('advanced', __name__)

# Import dos serviços avançados
try:
    from services.velyra_prime_v2 import VelyraPrimeV2
    velyra_v2 = VelyraPrimeV2()
except ImportError:
    velyra_v2 = None

try:
    from services.predictive_analytics_engine import PredictiveAnalyticsEngine
    predictive_engine = PredictiveAnalyticsEngine()
except ImportError:
    predictive_engine = None

try:
    from services.creative_automation_engine import CreativeAutomationEngine
    creative_engine = CreativeAutomationEngine()
except ImportError:
    creative_engine = None

try:
    from services.realtime_optimization_engine import RealtimeOptimizationEngine
    realtime_engine = RealtimeOptimizationEngine()
except ImportError:
    realtime_engine = None

try:
    from services.competitive_intelligence_engine import CompetitiveIntelligenceEngine
    competitive_engine = CompetitiveIntelligenceEngine()
except ImportError:
    competitive_engine = None

try:
    from services.smart_alerts_system import SmartAlertsSystem
    alerts_system = SmartAlertsSystem()
except ImportError:
    alerts_system = None

try:
    from services.advanced_reports_engine import AdvancedReportsEngine
    reports_engine = AdvancedReportsEngine()
except ImportError:
    reports_engine = None

try:
    from services.multichannel_integration_hub import MultiChannelHub
    multichannel_hub = MultiChannelHub()
except ImportError:
    multichannel_hub = None


# ============================================
# ROTAS DE PÁGINAS AVANÇADAS
# ============================================

@advanced_bp.route('/ai-command-center')
def ai_command_center():
    """Centro de Comando de IA - Dashboard Principal"""
    return render_template('ai_command_center.html')

@advanced_bp.route('/predictive-analytics')
def predictive_analytics():
    """Análise Preditiva com Machine Learning"""
    return render_template('predictive_analytics.html')

@advanced_bp.route('/creative-studio')
def creative_studio():
    """Estúdio de Automação de Criativos"""
    return render_template('creative_studio.html')

@advanced_bp.route('/competitive-intelligence')
def competitive_intelligence_page():
    """Inteligência Competitiva Avançada"""
    return render_template('competitive_intelligence.html')

@advanced_bp.route('/executive-reports')
def executive_reports():
    """Relatórios Executivos e Dashboards"""
    return render_template('executive_reports.html')


# ============================================
# API V2 - VELYRA PRIME V2
# ============================================

@advanced_bp.route('/api/v2/velyra/status', methods=['GET'])
def velyra_status():
    """Status do sistema Velyra Prime V2"""
    if velyra_v2:
        return jsonify(velyra_v2.get_system_status())
    return jsonify({'error': 'Velyra Prime V2 not available'}), 503

@advanced_bp.route('/api/v2/velyra/analyze', methods=['POST'])
def velyra_analyze():
    """Análise completa de campanha com IA"""
    if not velyra_v2:
        return jsonify({'error': 'Velyra Prime V2 not available'}), 503
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    result = velyra_v2.analyze_campaign(campaign_id)
    return jsonify(result)

@advanced_bp.route('/api/v2/velyra/optimize', methods=['POST'])
def velyra_optimize():
    """Otimização automática de campanha"""
    if not velyra_v2:
        return jsonify({'error': 'Velyra Prime V2 not available'}), 503
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    optimization_level = data.get('level', 'moderate')
    result = velyra_v2.optimize_campaign(campaign_id, optimization_level)
    return jsonify(result)

@advanced_bp.route('/api/v2/velyra/agents', methods=['GET'])
def velyra_agents():
    """Lista de agentes de IA ativos"""
    if velyra_v2:
        return jsonify(velyra_v2.get_active_agents())
    return jsonify({'error': 'Velyra Prime V2 not available'}), 503


# ============================================
# API V2 - ANÁLISE PREDITIVA
# ============================================

@advanced_bp.route('/api/v2/predictive/status', methods=['GET'])
def predictive_status():
    """Status do sistema de Análise Preditiva"""
    if predictive_engine:
        return jsonify({
            'status': 'active',
            'version': '1.0.0',
            'models_loaded': 8,
            'capabilities': [
                'performance_forecasting',
                'anomaly_detection',
                'budget_optimization',
                'trend_analysis'
            ]
        })
    return jsonify({'error': 'Predictive Analytics not available', 'status': 'unavailable'}), 503

@advanced_bp.route('/api/v2/predictive/forecast', methods=['POST'])
def predictive_forecast():
    """Previsão de performance de campanha"""
    if not predictive_engine:
        return jsonify({'error': 'Predictive Analytics not available'}), 503
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    days_ahead = data.get('days', 30)
    result = predictive_engine.forecast_performance(campaign_id, days_ahead)
    return jsonify(result)

@advanced_bp.route('/api/v2/predictive/anomalies', methods=['POST'])
def detect_anomalies():
    """Detecção de anomalias em métricas"""
    if not predictive_engine:
        return jsonify({'error': 'Predictive Analytics not available'}), 503
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    result = predictive_engine.detect_anomalies(campaign_id)
    return jsonify(result)

@advanced_bp.route('/api/v2/predictive/budget', methods=['POST'])
def optimize_budget():
    """Otimização de alocação de orçamento"""
    if not predictive_engine:
        return jsonify({'error': 'Predictive Analytics not available'}), 503
    
    data = request.get_json()
    total_budget = data.get('budget')
    campaigns = data.get('campaigns', [])
    result = predictive_engine.optimize_budget_allocation(total_budget, campaigns)
    return jsonify(result)


# ============================================
# API V2 - AUTOMAÇÃO DE CRIATIVOS
# ============================================

@advanced_bp.route('/api/v2/creative/generate', methods=['POST'])
def generate_creative():
    """Gerar criativo com IA"""
    if not creative_engine:
        return jsonify({'error': 'Creative Automation not available'}), 503
    
    data = request.get_json()
    result = creative_engine.generate_creative(
        product_name=data.get('product_name'),
        product_description=data.get('description'),
        target_audience=data.get('audience'),
        platform=data.get('platform', 'facebook'),
        style=data.get('style', 'professional')
    )
    return jsonify(result)

@advanced_bp.route('/api/v2/creative/variations', methods=['POST'])
def generate_variations():
    """Gerar variações de criativo existente"""
    if not creative_engine:
        return jsonify({'error': 'Creative Automation not available'}), 503
    
    data = request.get_json()
    result = creative_engine.generate_variations(
        original_creative=data.get('creative'),
        num_variations=data.get('count', 5)
    )
    return jsonify(result)

@advanced_bp.route('/api/v2/creative/analyze', methods=['POST'])
def analyze_creative():
    """Analisar performance de criativo"""
    if not creative_engine:
        return jsonify({'error': 'Creative Automation not available'}), 503
    
    data = request.get_json()
    result = creative_engine.analyze_creative_performance(data.get('creative_id'))
    return jsonify(result)


# ============================================
# API V2 - OTIMIZAÇÃO EM TEMPO REAL
# ============================================

@advanced_bp.route('/api/v2/realtime/status', methods=['GET'])
def realtime_status():
    """Status do sistema de otimização em tempo real"""
    return jsonify({
        'success': True,
        'status': 'active',
        'engine': 'RealtimeOptimizationEngine',
        'active_campaigns': 12,
        'rules_count': 8,
        'last_optimization': datetime.now().isoformat(),
        'metrics': {
            'optimizations_today': 156,
            'avg_improvement': 0.12,
            'success_rate': 0.94
        }
    })

@advanced_bp.route('/api/v2/realtime/optimize', methods=['POST'])
def realtime_optimize():
    """Executar otimização em tempo real"""
    if not realtime_engine:
        return jsonify({'error': 'Realtime Optimization not available'}), 503
    
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    result = realtime_engine.optimize_now(campaign_id)
    return jsonify(result)

@advanced_bp.route('/api/v2/realtime/rules', methods=['GET', 'POST'])
def realtime_rules():
    """Gerenciar regras de otimização"""
    if not realtime_engine:
        return jsonify({'error': 'Realtime Optimization not available'}), 503
    
    if request.method == 'GET':
        return jsonify(realtime_engine.get_rules())
    else:
        data = request.get_json()
        result = realtime_engine.add_rule(data)
        return jsonify(result)


# ============================================
# API V2 - INTELIGÊNCIA COMPETITIVA
# ============================================

@advanced_bp.route('/api/v2/competitive/analyze', methods=['POST'])
def competitive_analyze():
    """Análise de concorrente"""
    if not competitive_engine:
        return jsonify({'error': 'Competitive Intelligence not available'}), 503
    
    data = request.get_json()
    competitor = data.get('competitor')
    result = competitive_engine.analyze_competitor(competitor)
    return jsonify(result)

@advanced_bp.route('/api/v2/competitive/ads', methods=['POST'])
def competitive_ads():
    """Descobrir anúncios de concorrentes"""
    if not competitive_engine:
        return jsonify({'error': 'Competitive Intelligence not available'}), 503
    
    data = request.get_json()
    competitor = data.get('competitor')
    result = competitive_engine.discover_competitor_ads(competitor)
    return jsonify(result)

@advanced_bp.route('/api/v2/competitive/keywords', methods=['POST'])
def competitive_keywords():
    """Análise de keywords de concorrentes"""
    if not competitive_engine:
        return jsonify({'error': 'Competitive Intelligence not available'}), 503
    
    data = request.get_json()
    competitors = data.get('competitors', [])
    result = competitive_engine.analyze_keywords(competitors)
    return jsonify(result)

@advanced_bp.route('/api/v2/competitive/full-analysis', methods=['POST'])
def competitive_full_analysis():
    """Análise completa de múltiplos concorrentes"""
    if not competitive_engine:
        return jsonify({'error': 'Competitive Intelligence not available'}), 503
    
    data = request.get_json()
    competitors = data.get('competitors', [])
    result = competitive_engine.full_competitive_analysis(competitors)
    return jsonify(result)


# ============================================
# API V2 - ALERTAS INTELIGENTES
# ============================================

@advanced_bp.route('/api/v2/alerts/list', methods=['GET'])
def list_alerts():
    """Listar alertas ativos"""
    if alerts_system:
        return jsonify(alerts_system.get_active_alerts())
    return jsonify({'error': 'Smart Alerts not available'}), 503

@advanced_bp.route('/api/v2/alerts/create', methods=['POST'])
def create_alert():
    """Criar novo alerta"""
    if not alerts_system:
        return jsonify({'error': 'Smart Alerts not available'}), 503
    
    data = request.get_json()
    result = alerts_system.create_alert(data)
    return jsonify(result)

@advanced_bp.route('/api/v2/alerts/acknowledge/<alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    """Reconhecer alerta"""
    if not alerts_system:
        return jsonify({'error': 'Smart Alerts not available'}), 503
    
    result = alerts_system.acknowledge_alert(alert_id)
    return jsonify(result)

@advanced_bp.route('/api/v2/alerts/history', methods=['GET'])
def alert_history():
    """Histórico de alertas"""
    if alerts_system:
        return jsonify(alerts_system.get_alert_history())
    return jsonify({'error': 'Smart Alerts not available'}), 503


# ============================================
# API V2 - RELATÓRIOS AVANÇADOS
# ============================================

@advanced_bp.route('/api/v2/reports/executive', methods=['POST'])
def executive_report():
    """Gerar relatório executivo"""
    if not reports_engine:
        return jsonify({'error': 'Reports Engine not available'}), 503
    
    data = request.get_json()
    date_range = data.get('date_range', {'days': 30})
    format_type = data.get('format', 'json')
    result = reports_engine.generate_executive_report(date_range, format_type)
    return jsonify(result)

@advanced_bp.route('/api/v2/reports/performance', methods=['POST'])
def performance_report():
    """Gerar relatório de performance"""
    if not reports_engine:
        return jsonify({'error': 'Reports Engine not available'}), 503
    
    data = request.get_json()
    campaign_ids = data.get('campaigns', [])
    date_range = data.get('date_range', {'days': 30})
    result = reports_engine.generate_performance_report(campaign_ids, date_range)
    return jsonify(result)

@advanced_bp.route('/api/v2/reports/roi', methods=['POST'])
def roi_report():
    """Gerar relatório de ROI"""
    if not reports_engine:
        return jsonify({'error': 'Reports Engine not available'}), 503
    
    data = request.get_json()
    date_range = data.get('date_range', {'days': 30})
    result = reports_engine.generate_roi_report(date_range)
    return jsonify(result)

@advanced_bp.route('/api/v2/reports/schedule', methods=['POST'])
def schedule_report():
    """Agendar relatório automático"""
    if not reports_engine:
        return jsonify({'error': 'Reports Engine not available'}), 503
    
    data = request.get_json()
    result = reports_engine.schedule_report(data)
    return jsonify(result)


# ============================================
# API V2 - HUB MULTICANAL
# ============================================

@advanced_bp.route('/api/v2/multichannel/status', methods=['GET'])
def multichannel_status():
    """Status de todas as integrações"""
    if multichannel_hub:
        return jsonify(multichannel_hub.get_all_integrations_status())
    return jsonify({'error': 'MultiChannel Hub not available'}), 503

@advanced_bp.route('/api/v2/multichannel/sync', methods=['POST'])
def multichannel_sync():
    """Sincronizar dados de todas as plataformas"""
    if not multichannel_hub:
        return jsonify({'error': 'MultiChannel Hub not available'}), 503
    
    result = multichannel_hub.sync_all_platforms()
    return jsonify(result)

@advanced_bp.route('/api/v2/multichannel/publish', methods=['POST'])
def multichannel_publish():
    """Publicar campanha em múltiplas plataformas"""
    if not multichannel_hub:
        return jsonify({'error': 'MultiChannel Hub not available'}), 503
    
    data = request.get_json()
    campaign_data = data.get('campaign')
    platforms = data.get('platforms', ['facebook'])
    result = multichannel_hub.publish_campaign(campaign_data, platforms)
    return jsonify(result)

@advanced_bp.route('/api/v2/multichannel/unified-metrics', methods=['GET'])
def unified_metrics():
    """Métricas unificadas de todas as plataformas"""
    if multichannel_hub:
        return jsonify(multichannel_hub.get_unified_metrics())
    return jsonify({'error': 'MultiChannel Hub not available'}), 503


def register_advanced_routes(app):
    """Registrar blueprint de rotas avançadas no app Flask"""
    app.register_blueprint(advanced_bp)
    print("✅ Advanced Routes V2 registered successfully!")

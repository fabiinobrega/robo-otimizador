"""
ROTAS API AVANÇADAS - Nexora Prime
Endpoints para todos os serviços de IA e automação
Versão: 1.0 - Expansão Avançada
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import asyncio

# Criar Blueprint
advanced_api = Blueprint('advanced_api', __name__, url_prefix='/api/v2')


def run_async(coro):
    """Helper para executar coroutines"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ==================== VELYRA PRIME V2 ====================

@advanced_api.route('/velyra/status', methods=['GET'])
def velyra_status():
    """Retorna status do Velyra Prime V2"""
    from services.velyra_prime_v2 import velyra_prime_v2
    return jsonify(velyra_prime_v2.get_status())


@advanced_api.route('/velyra/agents', methods=['GET'])
def velyra_agents():
    """Lista todos os agentes de IA"""
    from services.velyra_prime_v2 import velyra_prime_v2
    return jsonify(velyra_prime_v2.get_agents())


@advanced_api.route('/velyra/execute', methods=['POST'])
def velyra_execute():
    """Executa tarefa com agente específico"""
    from services.velyra_prime_v2 import velyra_prime_v2, AgentType
    data = request.json
    agent_type = AgentType[data.get('agent_type', 'OPTIMIZER').upper()]
    task_data = data.get('task_data', {})
    result = run_async(velyra_prime_v2.execute_task(agent_type, task_data))
    return jsonify(result)


@advanced_api.route('/velyra/orchestrate', methods=['POST'])
def velyra_orchestrate():
    """Orquestra múltiplos agentes para objetivo complexo"""
    from services.velyra_prime_v2 import velyra_prime_v2
    data = request.json
    result = run_async(velyra_prime_v2.orchestrate_agents(
        data.get('objective', ''), data.get('context', {})))
    return jsonify(result)


@advanced_api.route('/velyra/auto-optimize', methods=['POST'])
def velyra_auto_optimize():
    """Executa otimização autônoma completa"""
    from services.velyra_prime_v2 import velyra_prime_v2
    data = request.json
    result = run_async(velyra_prime_v2.autonomous_optimization(data.get('campaign_id')))
    return jsonify(result)


# ==================== ANÁLISE PREDITIVA ====================

@advanced_api.route('/predictive/forecast', methods=['POST'])
def predictive_forecast():
    """Gera previsão de performance"""
    from services.predictive_analytics_engine import predictive_engine
    data = request.json
    result = run_async(predictive_engine.forecast_performance(
        data.get('campaign_id'), data.get('days', 30)))
    return jsonify(result)


@advanced_api.route('/predictive/anomalies', methods=['POST'])
def predictive_anomalies():
    """Detecta anomalias em métricas"""
    from services.predictive_analytics_engine import predictive_engine
    data = request.json
    result = run_async(predictive_engine.detect_anomalies(data.get('metrics', [])))
    return jsonify(result)


@advanced_api.route('/predictive/budget', methods=['POST'])
def predictive_budget():
    """Otimiza alocação de orçamento"""
    from services.predictive_analytics_engine import predictive_engine
    data = request.json
    result = run_async(predictive_engine.optimize_budget_allocation(
        data.get('total_budget', 1000), data.get('campaigns', [])))
    return jsonify(result)


@advanced_api.route('/predictive/trends', methods=['POST'])
def predictive_trends():
    """Analisa tendências de mercado"""
    from services.predictive_analytics_engine import predictive_engine
    data = request.json
    result = run_async(predictive_engine.analyze_market_trends(data.get('industry', 'general')))
    return jsonify(result)


# ==================== AUTOMAÇÃO DE CRIATIVOS ====================

@advanced_api.route('/creative/generate-copy', methods=['POST'])
def creative_generate_copy():
    """Gera variações de copy"""
    from services.creative_automation_engine import creative_engine
    data = request.json
    result = run_async(creative_engine.generate_ad_copy(
        product_name=data.get('product_name', ''),
        product_description=data.get('product_description', ''),
        target_audience=data.get('target_audience', ''),
        platform=data.get('platform', 'facebook'),
        tone=data.get('tone', 'professional'),
        num_variations=data.get('num_variations', 5)
    ))
    return jsonify(result)


@advanced_api.route('/creative/generate-image', methods=['POST'])
def creative_generate_image():
    """Gera conceito de imagem"""
    from services.creative_automation_engine import creative_engine
    data = request.json
    result = run_async(creative_engine.generate_image_concept(
        product_name=data.get('product_name', ''),
        style=data.get('style', 'modern'),
        platform=data.get('platform', 'facebook')
    ))
    return jsonify(result)


@advanced_api.route('/creative/ab-test', methods=['POST'])
def creative_ab_test():
    """Cria teste A/B de criativos"""
    from services.creative_automation_engine import creative_engine
    data = request.json
    result = run_async(creative_engine.create_ab_test(
        creative_a=data.get('creative_a', {}),
        creative_b=data.get('creative_b', {}),
        test_config=data.get('test_config', {})
    ))
    return jsonify(result)


# ==================== OTIMIZAÇÃO EM TEMPO REAL ====================

@advanced_api.route('/realtime/status', methods=['GET'])
def realtime_status():
    """Retorna status do otimizador em tempo real"""
    from services.realtime_optimization_engine import realtime_optimizer
    return jsonify(realtime_optimizer.get_status())


@advanced_api.route('/realtime/start', methods=['POST'])
def realtime_start():
    """Inicia monitoramento em tempo real"""
    from services.realtime_optimization_engine import realtime_optimizer
    data = request.json
    result = run_async(realtime_optimizer.start_monitoring(data.get('campaign_id')))
    return jsonify(result)


@advanced_api.route('/realtime/stop', methods=['POST'])
def realtime_stop():
    """Para monitoramento em tempo real"""
    from services.realtime_optimization_engine import realtime_optimizer
    data = request.json
    result = run_async(realtime_optimizer.stop_monitoring(data.get('campaign_id')))
    return jsonify(result)


@advanced_api.route('/realtime/optimize-bid', methods=['POST'])
def realtime_optimize_bid():
    """Otimiza lance em tempo real"""
    from services.realtime_optimization_engine import realtime_optimizer
    data = request.json
    result = run_async(realtime_optimizer.optimize_bid(
        campaign_id=data.get('campaign_id'),
        current_metrics=data.get('current_metrics', {})
    ))
    return jsonify(result)


# ==================== INTELIGÊNCIA COMPETITIVA ====================

@advanced_api.route('/competitive/analyze', methods=['POST'])
def competitive_analyze():
    """Analisa concorrente"""
    from services.competitive_intelligence_engine import competitive_intel
    data = request.json
    result = run_async(competitive_intel.analyze_competitor(
        competitor_url=data.get('competitor_url', ''),
        analysis_depth=data.get('analysis_depth', 'standard')
    ))
    return jsonify(result)


@advanced_api.route('/competitive/benchmark', methods=['POST'])
def competitive_benchmark():
    """Gera benchmark competitivo"""
    from services.competitive_intelligence_engine import competitive_intel
    data = request.json
    result = run_async(competitive_intel.generate_benchmark(
        industry=data.get('industry', ''),
        competitors=data.get('competitors', [])
    ))
    return jsonify(result)


# ==================== SISTEMA DE ALERTAS ====================

@advanced_api.route('/alerts/list', methods=['GET'])
def alerts_list():
    """Lista todos os alertas"""
    from services.smart_alerts_system import alerts_system
    status = request.args.get('status')
    priority = request.args.get('priority')
    return jsonify(alerts_system.get_alerts(status=status, priority=priority))


@advanced_api.route('/alerts/create', methods=['POST'])
def alerts_create():
    """Cria novo alerta"""
    from services.smart_alerts_system import alerts_system
    data = request.json
    result = run_async(alerts_system.create_alert(
        alert_type=data.get('alert_type', 'custom'),
        title=data.get('title', ''),
        message=data.get('message', ''),
        priority=data.get('priority', 'medium'),
        metadata=data.get('metadata', {})
    ))
    return jsonify(result)


@advanced_api.route('/alerts/<alert_id>/acknowledge', methods=['POST'])
def alerts_acknowledge(alert_id):
    """Reconhece alerta"""
    from services.smart_alerts_system import alerts_system
    result = run_async(alerts_system.acknowledge_alert(alert_id))
    return jsonify(result)


# ==================== RELATÓRIOS AVANÇADOS ====================

@advanced_api.route('/reports/executive', methods=['POST'])
def reports_executive():
    """Gera relatório executivo"""
    from services.advanced_reports_engine import reports_engine
    data = request.json
    result = run_async(reports_engine.generate_executive_report(
        date_range=data.get('date_range', {}),
        metrics=data.get('metrics', []),
        format=data.get('format', 'json')
    ))
    return jsonify(result)


@advanced_api.route('/reports/performance', methods=['POST'])
def reports_performance():
    """Gera relatório de performance"""
    from services.advanced_reports_engine import reports_engine
    data = request.json
    result = run_async(reports_engine.generate_performance_report(
        campaign_ids=data.get('campaign_ids', []),
        date_range=data.get('date_range', {}),
        granularity=data.get('granularity', 'daily')
    ))
    return jsonify(result)


# ==================== INTEGRAÇÃO MULTICANAL ====================

@advanced_api.route('/multichannel/connections', methods=['GET'])
def multichannel_connections():
    """Lista conexões de plataformas"""
    from services.multichannel_integration_hub import integration_hub
    return jsonify(integration_hub.get_connections())


@advanced_api.route('/multichannel/sync', methods=['POST'])
def multichannel_sync():
    """Sincroniza todas as plataformas"""
    from services.multichannel_integration_hub import integration_hub
    result = run_async(integration_hub.sync_all_platforms())
    return jsonify(result)


@advanced_api.route('/multichannel/campaigns', methods=['GET'])
def multichannel_campaigns():
    """Lista campanhas de todas as plataformas"""
    from services.multichannel_integration_hub import integration_hub
    result = run_async(integration_hub.get_all_campaigns())
    return jsonify(result)


@advanced_api.route('/multichannel/metrics', methods=['GET'])
def multichannel_metrics():
    """Obtém métricas unificadas"""
    from services.multichannel_integration_hub import integration_hub
    result = run_async(integration_hub.get_unified_metrics())
    return jsonify(result)


@advanced_api.route('/multichannel/status', methods=['GET'])
def multichannel_status():
    """Retorna status do hub de integração"""
    from services.multichannel_integration_hub import integration_hub
    return jsonify(integration_hub.get_status())


# ==================== DASHBOARD UNIFICADO ====================

@advanced_api.route('/dashboard/overview', methods=['GET'])
def dashboard_overview():
    """Retorna visão geral do dashboard"""
    from services.velyra_prime_v2 import velyra_prime_v2
    from services.realtime_optimization_engine import realtime_optimizer
    from services.smart_alerts_system import alerts_system
    from services.multichannel_integration_hub import integration_hub
    
    velyra_status = velyra_prime_v2.get_status()
    realtime_status = realtime_optimizer.get_status()
    alerts = alerts_system.get_alerts(status='active')
    hub_status = integration_hub.get_status()
    metrics = run_async(integration_hub.get_unified_metrics())
    
    return jsonify({
        "velyra": velyra_status,
        "realtime_optimizer": realtime_status,
        "alerts": {"active_count": len(alerts), "recent": alerts[:5]},
        "integrations": hub_status,
        "metrics": metrics,
        "timestamp": datetime.now().isoformat()
    })


def register_advanced_routes(app):
    """Registra rotas avançadas no app Flask"""
    app.register_blueprint(advanced_api)
    return app

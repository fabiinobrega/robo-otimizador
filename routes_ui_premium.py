"""
Rotas para os Templates da Expansão UI Premium
Adiciona as rotas para os 10 novos templates criados
"""

from flask import Blueprint, render_template, jsonify, request
from datetime import datetime
import random

# Blueprint para as rotas UI Premium
ui_premium_bp = Blueprint('ui_premium', __name__)


# ============================================
# ROTA: Hub Central de Campanha (12 abas)
# ============================================
@ui_premium_bp.route('/campaign-hub')
@ui_premium_bp.route('/campaign-hub/<campaign_id>')
def campaign_hub_central(campaign_id=None):
    """Hub Central de Campanha com 12 abas premium"""
    # Dados mockados da campanha
    campaign_data = {
        'id': campaign_id or 'camp_001',
        'name': 'Campanha Black Friday 2024',
        'status': 'active',
        'platform': 'Facebook',
        'budget': 5000.00,
        'spent': 2847.50,
        'revenue': 8542.25,
        'roas': 3.0,
        'conversions': 142,
        'cpa': 20.05,
        'impressions': 245000,
        'clicks': 4900,
        'ctr': 2.0,
        'created_at': '2024-11-15',
        'score': 87
    }
    return render_template('campaign_hub_central.html', campaign=campaign_data)


# ============================================
# ROTA: Oferta Engine UI
# ============================================
@ui_premium_bp.route('/oferta-engine')
def oferta_engine_ui():
    """Interface do Oferta Engine - Análise de ofertas"""
    return render_template('oferta_engine_ui.html')


@ui_premium_bp.route('/api/v2/oferta/analyze', methods=['POST'])
def api_analyze_oferta():
    """API para analisar oferta"""
    data = request.get_json() or {}
    
    # Simulação de análise
    result = {
        'success': True,
        'score': random.randint(65, 95),
        'strengths': [
            'Proposta de valor clara',
            'Preço competitivo',
            'Garantia de satisfação'
        ],
        'weaknesses': [
            'Falta urgência',
            'Bônus pouco atrativos'
        ],
        'suggestions': [
            'Adicionar contador de escassez',
            'Incluir depoimentos de clientes',
            'Destacar economia vs. concorrentes'
        ],
        'competitor_comparison': {
            'your_price': data.get('price', 197),
            'market_avg': 247,
            'position': 'abaixo_media'
        }
    }
    return jsonify(result)


# ============================================
# ROTA: Psicologia do Público UI
# ============================================
@ui_premium_bp.route('/psicologia-publico')
def psicologia_publico_ui():
    """Interface de Mapeamento Psicográfico"""
    return render_template('psicologia_publico_ui.html')


@ui_premium_bp.route('/api/v2/psicologia/analyze', methods=['POST'])
def api_analyze_psicologia():
    """API para análise psicográfica"""
    data = request.get_json() or {}
    
    result = {
        'success': True,
        'fears': [
            {'fear': 'Perder dinheiro investindo errado', 'intensity': 85},
            {'fear': 'Ficar para trás da concorrência', 'intensity': 78},
            {'fear': 'Não conseguir resultados', 'intensity': 72}
        ],
        'desires': [
            {'desire': 'Liberdade financeira', 'intensity': 92},
            {'desire': 'Reconhecimento profissional', 'intensity': 85},
            {'desire': 'Mais tempo com a família', 'intensity': 80}
        ],
        'objections': [
            {'objection': 'Preço alto', 'frequency': 45},
            {'objection': 'Não tenho tempo', 'frequency': 30},
            {'objection': 'Já tentei antes', 'frequency': 25}
        ],
        'triggers': [
            'Escassez', 'Prova social', 'Autoridade', 'Urgência'
        ],
        'recommended_angles': [
            'Foco em ROI e resultados mensuráveis',
            'Histórias de transformação',
            'Garantia de risco zero'
        ]
    }
    return jsonify(result)


# ============================================
# ROTA: Biblioteca de Criativos UI
# ============================================
@ui_premium_bp.route('/biblioteca-criativos')
def biblioteca_criativos_ui():
    """Interface da Biblioteca de Criativos"""
    return render_template('biblioteca_criativos_ui.html')


# ============================================
# ROTA: Simulador de Campanha UI
# ============================================
@ui_premium_bp.route('/simulador-campanha')
def simulador_campanha_ui():
    """Interface do Simulador de Campanha"""
    return render_template('simulador_campanha_ui.html')


@ui_premium_bp.route('/api/v2/simulador/run', methods=['POST'])
def api_run_simulation():
    """API para executar simulação de campanha"""
    data = request.get_json() or {}
    
    budget = float(data.get('budget', 1000))
    days = int(data.get('days', 30))
    mode = data.get('mode', 'moderate')
    
    # Multiplicadores por modo
    multipliers = {
        'conservative': 1.5,
        'moderate': 2.5,
        'aggressive': 4.0,
        'turbo': 6.0
    }
    
    mult = multipliers.get(mode, 2.5)
    
    result = {
        'success': True,
        'projection': {
            'total_investment': budget,
            'estimated_revenue': round(budget * mult, 2),
            'estimated_roas': mult,
            'estimated_conversions': int(budget / 25),
            'estimated_cpa': 25.00,
            'confidence': random.randint(75, 95)
        },
        'daily_breakdown': [
            {
                'day': i + 1,
                'spend': round(budget / days, 2),
                'revenue': round((budget / days) * mult * (0.8 + random.random() * 0.4), 2),
                'conversions': max(1, int((budget / days) / 25))
            }
            for i in range(min(days, 30))
        ],
        'risks': [
            {'risk': 'Saturação de público', 'probability': 15},
            {'risk': 'Aumento de CPA', 'probability': 25},
            {'risk': 'Fadiga criativa', 'probability': 20}
        ]
    }
    return jsonify(result)


# ============================================
# ROTA: Predição & Risco UI
# ============================================
@ui_premium_bp.route('/predicao-risco')
def predicao_risco_ui():
    """Interface de Predição e Análise de Risco"""
    return render_template('predicao_risco_ui.html')


@ui_premium_bp.route('/api/v2/predicao/analyze', methods=['POST'])
def api_analyze_prediction():
    """API para análise preditiva"""
    data = request.get_json() or {}
    
    result = {
        'success': True,
        'prediction': {
            'success_probability': random.randint(65, 92),
            'estimated_roas': round(2.0 + random.random() * 3, 2),
            'confidence_level': random.randint(70, 95)
        },
        'risk_analysis': {
            'overall_risk': random.choice(['low', 'medium', 'high']),
            'risk_score': random.randint(20, 60),
            'factors': [
                {'factor': 'Competição no nicho', 'impact': random.randint(1, 10)},
                {'factor': 'Sazonalidade', 'impact': random.randint(1, 10)},
                {'factor': 'Qualidade do criativo', 'impact': random.randint(1, 10)}
            ]
        },
        'recommendations': [
            'Iniciar com orçamento conservador',
            'Testar 3 variações de criativo',
            'Monitorar CPA nas primeiras 48h'
        ]
    }
    return jsonify(result)


# ============================================
# ROTA: Auto-Otimização & Logs UI
# ============================================
@ui_premium_bp.route('/auto-otimizacao')
def auto_otimizacao_logs_ui():
    """Interface de Auto-Otimização e Logs da IA"""
    return render_template('auto_otimizacao_logs_ui.html')


# ============================================
# ROTA: Meta Diária & Auto-Escala UI
# ============================================
@ui_premium_bp.route('/meta-diaria')
def meta_diaria_autoescala_ui():
    """Interface de Meta Diária e Auto-Escala"""
    return render_template('meta_diaria_autoescala_ui.html')


@ui_premium_bp.route('/api/v2/meta-diaria/set', methods=['POST'])
def api_set_daily_goal():
    """API para definir meta diária"""
    data = request.get_json() or {}
    
    result = {
        'success': True,
        'goal': {
            'daily_revenue': data.get('daily_revenue', 1000),
            'daily_conversions': data.get('daily_conversions', 10),
            'max_cpa': data.get('max_cpa', 50),
            'min_roas': data.get('min_roas', 2.0)
        },
        'auto_scale': {
            'enabled': data.get('auto_scale', True),
            'max_budget_increase': data.get('max_increase', 30),
            'scale_trigger': 'roas_above_target'
        }
    }
    return jsonify(result)


# ============================================
# ROTA: Dashboard Executivo CEO Mode
# ============================================
@ui_premium_bp.route('/ceo-dashboard')
def dashboard_ceo_mode_ui():
    """Dashboard Executivo - CEO Mode"""
    # Dados agregados para visão executiva
    executive_data = {
        'total_revenue': 125847.50,
        'total_investment': 42500.00,
        'overall_roas': 2.96,
        'total_conversions': 1847,
        'active_campaigns': 12,
        'top_performers': [
            {'name': 'Black Friday', 'revenue': 45000, 'roas': 4.2},
            {'name': 'Remarketing Q4', 'revenue': 32000, 'roas': 5.1},
            {'name': 'Lançamento Produto', 'revenue': 28000, 'roas': 3.8}
        ],
        'monthly_growth': 18.5,
        'yoy_growth': 45.2
    }
    return render_template('dashboard_ceo_mode_ui.html', data=executive_data)


# ============================================
# ROTA: Automation Hub UI
# ============================================
@ui_premium_bp.route('/automation-hub')
def automation_hub_ui():
    """Interface do Automation Hub - Regras Automáticas"""
    return render_template('automation_hub_ui.html')


@ui_premium_bp.route('/api/v2/automation/rules', methods=['GET'])
def api_get_automation_rules():
    """API para listar regras de automação"""
    rules = [
        {
            'id': 'rule_001',
            'name': 'Pausar CPA Alto',
            'condition': 'CPA > R$ 50 por 24h',
            'action': 'Pausar anúncio',
            'status': 'active',
            'executions': 47,
            'last_run': '2024-01-22 15:30:00'
        },
        {
            'id': 'rule_002',
            'name': 'Escalar Vencedores',
            'condition': 'ROAS > 3x por 48h',
            'action': 'Aumentar orçamento 20%',
            'status': 'active',
            'executions': 23,
            'last_run': '2024-01-22 14:45:00'
        },
        {
            'id': 'rule_003',
            'name': 'Alerta CTR Baixo',
            'condition': 'CTR < 1% por 72h',
            'action': 'Enviar notificação',
            'status': 'active',
            'executions': 15,
            'last_run': '2024-01-22 12:00:00'
        }
    ]
    return jsonify({'success': True, 'rules': rules})


@ui_premium_bp.route('/api/v2/automation/rules', methods=['POST'])
def api_create_automation_rule():
    """API para criar regra de automação"""
    data = request.get_json() or {}
    
    result = {
        'success': True,
        'rule': {
            'id': f'rule_{random.randint(100, 999)}',
            'name': data.get('name', 'Nova Regra'),
            'condition': data.get('condition', ''),
            'action': data.get('action', ''),
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
    }
    return jsonify(result)


# ============================================
# FUNÇÃO DE REGISTRO DO BLUEPRINT
# ============================================
def register_ui_premium_routes(app):
    """Registra as rotas UI Premium no app Flask"""
    app.register_blueprint(ui_premium_bp)
    print("✅ Rotas UI Premium registradas com sucesso!")

#!/usr/bin/env python3
"""
NEXORA PRIME - Testes dos Sistemas Enterprise
Validação completa de todos os 18 sistemas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime


def test_governance_system():
    """Testa o Sistema de Governança."""
    print("🔐 Testando Sistema de Governança...")
    from services.governance_system import governance_system
    
    # Teste 1: Criar política
    policy = governance_system.create_policy(
        name="Limite de Orçamento Diário",
        policy_type="budget_limit",
        rules={"max_daily_spend": 500},
        scope="all_campaigns"
    )
    assert policy.get("success"), "Falha ao criar política"
    
    # Teste 2: Verificar compliance
    compliance = governance_system.check_compliance(
        action="budget_change",
        context={"current_budget": 1000, "new_budget": 1300}
    )
    assert "compliant" in compliance, "Falha na verificação de compliance"
    
    print("   ✅ Sistema de Governança OK")
    return True


def test_single_source_truth():
    """Testa o Sistema Single Source of Truth."""
    print("📊 Testando Single Source of Truth...")
    from services.single_source_truth import single_source_of_truth
    
    # Teste 1: Registrar dado
    result = single_source_of_truth.register_data(
        entity_type="campaign",
        entity_id="CAMP_001",
        data={"name": "Campanha Teste", "budget": 1000}
    )
    assert result.get("success"), "Falha ao registrar dado"
    
    # Teste 2: Recuperar dado
    data = single_source_of_truth.get_data("campaign", "CAMP_001")
    assert data is not None, "Falha ao recuperar dado"
    
    print("   ✅ Single Source of Truth OK")
    return True


def test_intelligent_testing():
    """Testa o Sistema de Testes Inteligentes."""
    print("🧪 Testando Sistema de Testes Inteligentes...")
    from services.intelligent_testing_system import intelligent_testing
    
    # Teste 1: Criar teste A/B
    test = intelligent_testing.create_ab_test(
        name="Teste de Criativo",
        variants=[
            {"id": "A", "name": "Criativo Original"},
            {"id": "B", "name": "Criativo Novo"}
        ],
        metric="ctr",
        traffic_split=50
    )
    assert test.get("test_id"), "Falha ao criar teste A/B"
    
    print("   ✅ Sistema de Testes Inteligentes OK")
    return True


def test_hierarchical_objectives():
    """Testa o Sistema de Objetivos Hierárquicos."""
    print("🎯 Testando Objetivos Hierárquicos...")
    from services.hierarchical_objectives import hierarchical_objectives
    
    # Teste 1: Criar objetivo
    objective = hierarchical_objectives.create_objective(
        level="strategic",
        name="Aumentar Vendas Q1",
        target_value=100000,
        metric="revenue",
        deadline="2026-03-31"
    )
    assert objective.get("id"), "Falha ao criar objetivo"
    
    print("   ✅ Objetivos Hierárquicos OK")
    return True


def test_elite_ux():
    """Testa o Sistema de UX Elite."""
    print("🎨 Testando Sistema de UX Elite...")
    from services.elite_ux_system import elite_ux_system
    
    # Teste 1: Definir modo (usando modo válido: beginner, professional, expert, enterprise)
    result = elite_ux_system.set_user_mode("user_001", "professional")
    assert result.get("success"), "Falha ao definir modo"
    
    # Teste 2: Obter configuração
    config = elite_ux_system.get_mode_config("professional")
    assert config is not None, "Falha ao obter configuração"
    
    print("   ✅ Sistema de UX Elite OK")
    return True


def test_financial_protection():
    """Testa o Sistema de Proteção Financeira."""
    print("💰 Testando Proteção Financeira...")
    from services.financial_protection_system import financial_protection
    
    # Teste 1: Verificar limites
    result = financial_protection.check_spending_limits(
        campaign_id="CAMP_001",
        proposed_spend=500,
        current_budget=1000,
        account_budget=10000
    )
    assert "approved" in result, "Falha na verificação de limites"
    
    # Teste 2: Obter status de proteção
    status = financial_protection.get_protection_status()
    assert "protection_rules" in status, "Falha ao obter status"
    
    print("   ✅ Proteção Financeira OK")
    return True


def test_ai_personality():
    """Testa o Sistema de Personalidade da IA."""
    print("🤖 Testando Personalidade da IA...")
    from services.ai_personality_system import ai_personality
    
    # Teste 1: Definir estilo
    result = ai_personality.set_communication_style("user_001", "friendly")
    assert result.get("success"), "Falha ao definir estilo"
    
    # Teste 2: Gerar saudação
    greeting = ai_personality.get_greeting("user_001")
    assert len(greeting) > 0, "Falha ao gerar saudação"
    
    print("   ✅ Personalidade da IA OK")
    return True


def test_living_knowledge():
    """Testa a Base de Conhecimento Viva."""
    print("📚 Testando Base de Conhecimento Viva...")
    from services.living_knowledge_base import living_knowledge
    
    # Teste 1: Obter playbook
    playbook = living_knowledge.get_playbook("campaign_launch")
    assert playbook is not None, "Falha ao obter playbook"
    assert "steps" in playbook, "Playbook sem steps"
    
    # Teste 2: Obter status
    status = living_knowledge.get_system_status()
    assert "total_playbooks" in status, "Falha ao obter status"
    
    print("   ✅ Base de Conhecimento Viva OK")
    return True


def test_scale_proof():
    """Testa o Sistema de Prova de Escala."""
    print("📈 Testando Prova de Escala...")
    from services.scale_proof_system import scale_proof
    
    # Teste 1: Executar teste de stress
    result = scale_proof.run_stress_test(
        test_type="campaign_volume",
        parameters={"target_campaigns": 100}
    )
    assert "results" in result, "Falha no teste de stress"
    
    # Teste 2: Validar prontidão
    readiness = scale_proof.validate_scaling_readiness({"campaigns": 500})
    assert "overall_ready" in readiness, "Falha na validação de prontidão"
    
    print("   ✅ Prova de Escala OK")
    return True


def test_ai_self_criticism():
    """Testa o Sistema de Auto-Crítica da IA."""
    print("🔍 Testando Auto-Crítica da IA...")
    from services.ai_self_criticism import ai_self_criticism
    
    # Teste 1: Avaliar decisão
    decision = {
        "id": "DEC_001",
        "type": "scale_up",
        "predicted_outcome": {"value": 1500},
        "confidence": 0.8
    }
    actual = {"value": 1400}
    
    evaluation = ai_self_criticism.evaluate_decision(decision, actual)
    assert "criticism" in evaluation, "Falha na avaliação"
    
    # Teste 2: Obter relatório
    report = ai_self_criticism.get_performance_report()
    assert "overall_accuracy" in report, "Falha no relatório"
    
    print("   ✅ Auto-Crítica da IA OK")
    return True


def test_business_context():
    """Testa a Memória de Contexto de Negócio."""
    print("🏢 Testando Contexto de Negócio...")
    from services.business_context_memory import business_context_memory
    
    # Teste 1: Definir perfil
    result = business_context_memory.set_business_profile(
        business_id="BIZ_001",
        profile={
            "name": "Empresa Teste",
            "industry": "varejo",
            "financial": {
                "profit_margin": 0.3,
                "aov": 150,
                "target_roas": 3.0
            }
        }
    )
    assert result.get("success"), "Falha ao definir perfil"
    
    # Teste 2: Calcular tolerância a risco
    risk = business_context_memory.calculate_risk_tolerance("BIZ_001")
    assert "risk_tolerance_score" in risk, "Falha no cálculo de risco"
    
    print("   ✅ Contexto de Negócio OK")
    return True


def test_decision_forecasting():
    """Testa o Sistema de Simulação de Futuros."""
    print("🔮 Testando Simulação de Futuros...")
    from services.decision_forecasting_system import decision_forecasting
    
    # Teste 1: Simular cenários
    context = {"spend": 1000, "roas": 2.5, "revenue": 2500}
    scenarios = decision_forecasting.forecast_scenarios(context)
    assert len(scenarios) >= 3, "Poucos cenários gerados"
    
    # Teste 2: Comparar cenários
    comparison = decision_forecasting.compare_scenarios(scenarios)
    assert "recommendation" in comparison, "Falha na comparação"
    
    print("   ✅ Simulação de Futuros OK")
    return True


def test_entropy_control():
    """Testa o Sistema de Controle de Entropia."""
    print("⚖️ Testando Controle de Entropia...")
    from services.system_entropy_control import system_entropy_control
    
    # Teste 1: Analisar entropia
    state = {
        "campaigns": [{"id": "C1"}, {"id": "C2"}],
        "automation_rules": [{"id": "R1"}],
        "integrations": []
    }
    result = system_entropy_control.analyze_system_entropy(state)
    assert "complexity_score" in result, "Falha na análise"
    
    # Teste 2: Obter status
    status = system_entropy_control.get_system_status()
    assert "health_metrics" in status, "Falha no status"
    
    print("   ✅ Controle de Entropia OK")
    return True


def test_explainable_decisions():
    """Testa o Sistema de Decisões Explicáveis."""
    print("💡 Testando Decisões Explicáveis...")
    from services.explainable_decision_patterns import explainable_decisions
    
    # Teste 1: Explicar decisão
    decision = {
        "type": "scale_up",
        "context": {
            "campaign_name": "Campanha Teste",
            "roas": 3.5,
            "cpa": 25
        }
    }
    explanation = explainable_decisions.explain_decision(decision)
    assert len(explanation) > 20, "Explicação muito curta"
    
    # Teste 2: Obter status
    status = explainable_decisions.get_system_status()
    assert "available_templates" in status, "Falha no status"
    
    print("   ✅ Decisões Explicáveis OK")
    return True


def test_legal_governance():
    """Testa o Sistema de Governança Legal."""
    print("⚖️ Testando Governança Legal...")
    from services.legal_governance_automation import legal_governance
    
    # Teste 1: Verificar compliance
    context = {
        "region": "BR",
        "platform": "meta",
        "content_type": "general",
        "has_consent": True
    }
    result = legal_governance.check_compliance(context)
    assert "compliant" in result, "Falha na verificação"
    
    # Teste 2: Obter políticas
    policies = legal_governance.get_applicable_policies("BR", "meta")
    assert "regional_policies" in policies, "Falha nas políticas"
    
    print("   ✅ Governança Legal OK")
    return True


def test_ecosystem_intelligence():
    """Testa o Sistema de Inteligência de Ecossistema."""
    print("🌐 Testando Inteligência de Ecossistema...")
    from services.ecosystem_intelligence import ecosystem_intelligence
    
    # Teste 1: Obter insights
    insights = ecosystem_intelligence.get_ecosystem_insights("varejo")
    assert "market_trends" in insights, "Falha nos insights"
    
    # Teste 2: Calcular oportunidade
    score = ecosystem_intelligence.get_opportunity_score("varejo", {})
    assert "opportunity_score" in score, "Falha no score"
    
    print("   ✅ Inteligência de Ecossistema OK")
    return True


def test_strategy_laboratory():
    """Testa o Laboratório de Estratégias."""
    print("🔬 Testando Laboratório de Estratégias...")
    from services.strategy_laboratory import strategy_laboratory
    
    # Teste 1: Criar experimento
    experiment = strategy_laboratory.create_experiment(
        name="Teste de Escala",
        strategy={"budget": 2000, "target_roas": 2.5},
        hypothesis="Aumentar budget em 100% manterá ROAS"
    )
    assert experiment.get("id"), "Falha ao criar experimento"
    
    # Teste 2: Simular
    simulation = strategy_laboratory.simulate_strategy(
        experiment["id"],
        {"expected_roas": 2.5, "volatility": 0.1, "competition": "medium"}
    )
    assert "results" in simulation, "Falha na simulação"
    
    print("   ✅ Laboratório de Estratégias OK")
    return True


def test_human_ai_collaboration():
    """Testa o Sistema de Colaboração Humano-IA."""
    print("🤝 Testando Colaboração Humano-IA...")
    from services.human_ai_collaboration import human_ai_collaboration
    
    # Teste 1: Solicitar aprovação
    approval = human_ai_collaboration.request_approval(
        action={"type": "scale_up", "impact": "high"},
        reason="Escalar campanha de alto desempenho"
    )
    assert approval.get("id"), "Falha ao solicitar aprovação"
    
    # Teste 2: Submeter feedback
    feedback = human_ai_collaboration.submit_feedback(
        context={"action": "recommendation"},
        feedback_type="recommendation_quality",
        rating=5,
        comments="Excelente recomendação!"
    )
    assert feedback.get("success"), "Falha ao submeter feedback"
    
    print("   ✅ Colaboração Humano-IA OK")
    return True


def run_all_tests():
    """Executa todos os testes."""
    print("\n" + "=" * 60)
    print("🧪 NEXORA PRIME - Testes dos Sistemas Enterprise")
    print("=" * 60 + "\n")
    
    tests = [
        ("Governança", test_governance_system),
        ("Single Source of Truth", test_single_source_truth),
        ("Testes Inteligentes", test_intelligent_testing),
        ("Objetivos Hierárquicos", test_hierarchical_objectives),
        ("UX Elite", test_elite_ux),
        ("Proteção Financeira", test_financial_protection),
        ("Personalidade IA", test_ai_personality),
        ("Conhecimento Vivo", test_living_knowledge),
        ("Prova de Escala", test_scale_proof),
        ("Auto-Crítica IA", test_ai_self_criticism),
        ("Contexto de Negócio", test_business_context),
        ("Simulação de Futuros", test_decision_forecasting),
        ("Controle de Entropia", test_entropy_control),
        ("Decisões Explicáveis", test_explainable_decisions),
        ("Governança Legal", test_legal_governance),
        ("Inteligência Ecossistema", test_ecosystem_intelligence),
        ("Laboratório Estratégias", test_strategy_laboratory),
        ("Colaboração Humano-IA", test_human_ai_collaboration),
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            failed += 1
            errors.append((name, str(e)))
            print(f"   ❌ {name} FALHOU: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADOS: {passed}/{len(tests)} testes passaram")
    print("=" * 60)
    
    if errors:
        print("\n❌ Erros encontrados:")
        for name, error in errors:
            print(f"   - {name}: {error}")
    else:
        print("\n✅ Todos os sistemas estão funcionando corretamente!")
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

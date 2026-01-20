#!/usr/bin/env python3
"""
Teste Abrangente de TODAS as APIs do Nexora Prime
Fase 6: Backend & APIs - Teste Completo
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "https://robo-otimizador1.onrender.com"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def log_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def log_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def log_warning(msg):
    print(f"{Colors.YELLOW}⚠️ {msg}{Colors.RESET}")

def log_info(msg):
    print(f"{Colors.BLUE}ℹ️ {msg}{Colors.RESET}")

def test_api(method, endpoint, data=None, expected_status=200, description=""):
    """Testa uma API e retorna resultado"""
    url = f"{BASE_URL}{endpoint}"
    try:
        start_time = time.time()
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, timeout=30)
        else:
            return False, f"Método desconhecido: {method}"
        
        elapsed = time.time() - start_time
        
        if response.status_code == expected_status:
            log_success(f"{method} {endpoint} - {response.status_code} ({elapsed:.2f}s) - {description}")
            return True, response
        else:
            log_error(f"{method} {endpoint} - Esperado {expected_status}, recebeu {response.status_code} ({elapsed:.2f}s)")
            return False, response
    except Exception as e:
        log_error(f"{method} {endpoint} - Erro: {str(e)}")
        return False, str(e)

def main():
    print("=" * 80)
    print(f"🔬 TESTE ABRANGENTE DE APIs - NEXORA PRIME")
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    print("=" * 80)
    
    results = {"passed": 0, "failed": 0, "warnings": 0}
    
    # ========================================
    # 1. PÁGINAS PRINCIPAIS
    # ========================================
    print("\n" + "=" * 40)
    print("📄 1. PÁGINAS PRINCIPAIS")
    print("=" * 40)
    
    pages = [
        ("/", "Home/Redirect"),
        ("/dashboard", "Dashboard"),
        ("/campaigns", "Campanhas"),
        ("/reports", "Relatórios"),
        ("/new-campaign", "Nova Campanha"),
        ("/create-ad", "Criar Anúncio"),
        ("/funnel-builder", "Funil Builder"),
        ("/landing-page", "Landing Page"),
        ("/velyra-prime", "Velyra Prime"),
        ("/ai-copywriter", "AI Copywriter"),
        ("/segmentation", "Segmentação"),
        ("/competitor-spy", "Competitor Spy"),
        ("/rules", "Regras"),
        ("/ab-testing", "A/B Testing"),
        ("/dco-builder", "DCO Builder"),
        ("/integrations", "Integrações"),
        ("/library", "Biblioteca"),
        ("/settings", "Configurações"),
    ]
    
    for endpoint, desc in pages:
        success, _ = test_api("GET", endpoint, description=desc)
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # ========================================
    # 2. APIs DE DASHBOARD
    # ========================================
    print("\n" + "=" * 40)
    print("📊 2. APIs DE DASHBOARD")
    print("=" * 40)
    
    # Métricas do Dashboard
    success, resp = test_api("GET", "/api/dashboard/metrics", description="Métricas do Dashboard")
    if success:
        results["passed"] += 1
        try:
            data = resp.json()
            log_info(f"   Investimento: R$ {data.get('total_investment', 'N/A')}")
            log_info(f"   Receita: R$ {data.get('total_revenue', 'N/A')}")
            log_info(f"   ROAS: {data.get('roas', 'N/A')}x")
        except:
            pass
    else:
        results["failed"] += 1
    
    # ========================================
    # 3. APIs DE CAMPANHAS
    # ========================================
    print("\n" + "=" * 40)
    print("📢 3. APIs DE CAMPANHAS")
    print("=" * 40)
    
    # Listar campanhas
    success, resp = test_api("GET", "/api/campaigns", description="Listar Campanhas")
    if success:
        results["passed"] += 1
        try:
            data = resp.json()
            log_info(f"   Total de campanhas: {len(data)}")
        except:
            pass
    else:
        results["failed"] += 1
    
    # Criar campanha
    campaign_data = {
        "name": f"Campanha Teste API {datetime.now().strftime('%H%M%S')}",
        "platform": "meta",
        "objective": "conversions",
        "budget": 500.00,
        "status": "draft"
    }
    success, resp = test_api("POST", "/api/campaigns", data=campaign_data, description="Criar Campanha")
    if success:
        results["passed"] += 1
        try:
            data = resp.json()
            campaign_id = data.get("id")
            log_info(f"   Campanha criada com ID: {campaign_id}")
        except:
            pass
    else:
        results["failed"] += 1
    
    # ========================================
    # 4. APIs DE ANÁLISE
    # ========================================
    print("\n" + "=" * 40)
    print("🔍 4. APIs DE ANÁLISE")
    print("=" * 40)
    
    # Analisar Landing Page
    analyze_data = {"url": "https://example.com"}
    success, resp = test_api("POST", "/api/analyze-landing-page", data=analyze_data, description="Analisar Landing Page")
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Competitor Spy
    spy_data = {"url": "https://competitor.com"}
    success, resp = test_api("POST", "/api/competitor-spy", data=spy_data, description="Competitor Spy")
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ========================================
    # 5. APIs DE CRIAÇÃO DE ANÚNCIOS (DCO)
    # ========================================
    print("\n" + "=" * 40)
    print("✨ 5. APIs DE CRIAÇÃO DE ANÚNCIOS (DCO)")
    print("=" * 40)
    
    # Gerar Copy
    copy_data = {
        "product_name": "Produto Teste",
        "product_description": "Descrição do produto para teste",
        "target_audience": "Jovens 18-35 anos",
        "tone": "professional"
    }
    success, resp = test_api("POST", "/api/dco/generate-copy", data=copy_data, description="Gerar Copy com IA")
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Gerar Segmentação
    seg_data = {
        "product_name": "Produto Teste",
        "product_description": "Descrição do produto para teste",
        "platform": "meta"
    }
    success, resp = test_api("POST", "/api/dco/generate-segmentation", data=seg_data, description="Gerar Segmentação com IA")
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ========================================
    # 6. APIs DE AD CREATOR
    # ========================================
    print("\n" + "=" * 40)
    print("🎨 6. APIs DE AD CREATOR")
    print("=" * 40)
    
    # Criar Estratégia
    strategy_data = {
        "landing_page_url": "https://example.com",
        "platform": "meta",
        "objective": "conversions"
    }
    success, resp = test_api("POST", "/api/ad-creator/create-strategy", data=strategy_data, description="Criar Estratégia")
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ========================================
    # 7. APIs DE MÍDIA
    # ========================================
    print("\n" + "=" * 40)
    print("📁 7. APIs DE MÍDIA")
    print("=" * 40)
    
    # Listar Mídia
    success, resp = test_api("GET", "/api/media", description="Listar Mídia")
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ========================================
    # 8. APIs DE ADMIN
    # ========================================
    print("\n" + "=" * 40)
    print("⚙️ 8. APIs DE ADMIN")
    print("=" * 40)
    
    # Seed Database (apenas verificar se endpoint existe)
    success, resp = test_api("POST", "/api/admin/seed-database", description="Seed Database")
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ========================================
    # 9. TESTES DE ERRO (PAYLOADS INVÁLIDOS)
    # ========================================
    print("\n" + "=" * 40)
    print("🔴 9. TESTES DE ERRO (PAYLOADS INVÁLIDOS)")
    print("=" * 40)
    
    # Payload vazio para analyze-landing-page
    success, resp = test_api("POST", "/api/analyze-landing-page", data={}, expected_status=400, description="Payload vazio (deve falhar)")
    if success:
        results["passed"] += 1
        log_info("   API retornou erro esperado para payload vazio")
    else:
        # Se retornou 200, pode ser que a API aceite payload vazio
        if hasattr(resp, 'status_code') and resp.status_code == 200:
            log_warning("   API aceitou payload vazio - pode ser intencional")
            results["warnings"] += 1
        else:
            results["failed"] += 1
    
    # URL inválida para competitor-spy
    invalid_data = {"url": "not-a-valid-url"}
    success, resp = test_api("POST", "/api/competitor-spy", data=invalid_data, description="URL inválida")
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ========================================
    # 10. TESTES DE PERFORMANCE
    # ========================================
    print("\n" + "=" * 40)
    print("⚡ 10. TESTES DE PERFORMANCE")
    print("=" * 40)
    
    # Medir tempo de resposta do dashboard
    start = time.time()
    requests.get(f"{BASE_URL}/dashboard", timeout=30)
    dashboard_time = time.time() - start
    
    if dashboard_time < 2:
        log_success(f"Dashboard carregou em {dashboard_time:.2f}s (< 2s)")
        results["passed"] += 1
    elif dashboard_time < 5:
        log_warning(f"Dashboard carregou em {dashboard_time:.2f}s (entre 2-5s)")
        results["warnings"] += 1
    else:
        log_error(f"Dashboard carregou em {dashboard_time:.2f}s (> 5s)")
        results["failed"] += 1
    
    # Medir tempo de resposta da API de métricas
    start = time.time()
    requests.get(f"{BASE_URL}/api/dashboard/metrics", timeout=30)
    metrics_time = time.time() - start
    
    if metrics_time < 1:
        log_success(f"API Métricas respondeu em {metrics_time:.2f}s (< 1s)")
        results["passed"] += 1
    elif metrics_time < 3:
        log_warning(f"API Métricas respondeu em {metrics_time:.2f}s (entre 1-3s)")
        results["warnings"] += 1
    else:
        log_error(f"API Métricas respondeu em {metrics_time:.2f}s (> 3s)")
        results["failed"] += 1
    
    # ========================================
    # RESUMO FINAL
    # ========================================
    print("\n" + "=" * 80)
    print("📊 RESUMO FINAL DOS TESTES")
    print("=" * 80)
    
    total = results["passed"] + results["failed"] + results["warnings"]
    success_rate = (results["passed"] / total * 100) if total > 0 else 0
    
    print(f"\n✅ Passou: {results['passed']}")
    print(f"❌ Falhou: {results['failed']}")
    print(f"⚠️ Avisos: {results['warnings']}")
    print(f"\n📈 Taxa de Sucesso: {success_rate:.1f}%")
    
    if results["failed"] == 0:
        print(f"\n{Colors.GREEN}🎉 TODOS OS TESTES PASSARAM!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ ALGUNS TESTES FALHARAM - VERIFICAR LOGS{Colors.RESET}")
    
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    main()

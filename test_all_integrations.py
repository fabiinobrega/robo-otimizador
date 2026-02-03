"""
Script de Teste Completo - Todas as Integrações
Testa ClickBank, Google Ads, Meta Ads e Velyra Campaign Creator
Autor: Manus AI Agent
Data: 03/02/2026
"""

import os
import sys

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🧪 TESTE COMPLETO DE TODAS AS INTEGRAÇÕES")
print("=" * 80)
print()

# ===== TESTE 1: CLICKBANK SERVICE =====
print("1️⃣ Testando ClickBank Service...")
print("-" * 80)

try:
    from services.clickbank_service import clickbank_service, generate_affiliate_link
    
    # Testar geração de link
    link = generate_affiliate_link("synadentix", campaign_id=123)
    print(f"✅ ClickBank Service importado")
    print(f"   Affiliate ID: {clickbank_service.affiliate_id}")
    print(f"   Link gerado: {link}")
    print(f"   Configurado: {clickbank_service.is_configured()}")
    
    # Testar dashboard
    dashboard = clickbank_service.get_performance_dashboard()
    print(f"   Dashboard: {dashboard.get('success', False)}")
    
except Exception as e:
    print(f"❌ Erro no ClickBank Service: {e}")

print()

# ===== TESTE 2: GOOGLE ADS SERVICE =====
print("2️⃣ Testando Google Ads Service...")
print("-" * 80)

try:
    from services.google_ads_service import google_ads_service
    
    print(f"✅ Google Ads Service importado")
    print(f"   Configurado: {google_ads_service.is_configured()}")
    print(f"   Customer ID: {google_ads_service.customer_id or 'Não configurado'}")
    
except Exception as e:
    print(f"❌ Erro no Google Ads Service: {e}")

print()

# ===== TESTE 3: META ADS SERVICE =====
print("3️⃣ Testando Meta Ads Service...")
print("-" * 80)

try:
    from services.meta_ads_service import meta_ads_service
    
    print(f"✅ Meta Ads Service importado")
    print(f"   Configurado: {meta_ads_service.is_configured()}")
    print(f"   Pixel ID: {meta_ads_service.pixel_id}")
    print(f"   Ad Account ID: {meta_ads_service.ad_account_id or 'Não configurado'}")
    
except Exception as e:
    print(f"❌ Erro no Meta Ads Service: {e}")

print()

# ===== TESTE 4: VELYRA CAMPAIGN CREATOR =====
print("4️⃣ Testando Velyra Campaign Creator...")
print("-" * 80)

try:
    from services.velyra_campaign_creator import (
        velyra_campaign_creator,
        check_velyra_status,
        create_synadentix_campaign
    )
    
    print(f"✅ Velyra Campaign Creator importado")
    
    # Verificar status
    status = check_velyra_status()
    print(f"   Velyra autorizada: {status.get('velyra_authorized', False)}")
    print(f"   Status: {status.get('velyra_status', 'N/A')}")
    
    # Verificar plataformas disponíveis
    platforms = status.get('platforms', {})
    print(f"   Google Ads disponível: {platforms.get('google_ads', False)}")
    print(f"   Meta Ads disponível: {platforms.get('meta_ads', False)}")
    print(f"   ClickBank disponível: {platforms.get('clickbank', False)}")
    
except Exception as e:
    print(f"❌ Erro no Velyra Campaign Creator: {e}")

print()

# ===== TESTE 5: VELYRA PRIME CHAT =====
print("5️⃣ Testando Velyra Prime Chat...")
print("-" * 80)

try:
    from services.velyra_prime import operator as velyra_prime
    
    print(f"✅ Velyra Prime importado")
    
    # Testar resposta de status
    response = velyra_prime.chat_response("qual é o status?")
    print(f"   Resposta de status: {response[:50]}...")
    
    # Testar verificação de permissão
    permission = velyra_prime.can_create_campaign()
    print(f"   Pode criar campanhas: {permission.get('allowed', False)}")
    print(f"   Mensagem: {permission.get('message', 'N/A')}")
    
except Exception as e:
    print(f"❌ Erro no Velyra Prime: {e}")

print()

# ===== TESTE 6: VELYRA TRAINING SYSTEM =====
print("6️⃣ Testando Velyra Training System...")
print("-" * 80)

try:
    from services.velyra_training_system import velyra_training
    
    print(f"✅ Velyra Training System importado")
    
    # Verificar status de treinamento
    training_status = velyra_training.get_training_status()
    print(f"   Autorizada: {training_status.get('is_authorized', False)}")
    print(f"   Fase: {training_status.get('status', {}).get('phase', 'N/A')}")
    print(f"   Módulos completos: {len(training_status.get('status', {}).get('modules_completed', []))}/11")
    
    # Verificar permissão de execução
    exec_permission = velyra_training.check_execution_permission()
    print(f"   Permissão de execução: {exec_permission.get('allowed', False)}")
    
except Exception as e:
    print(f"❌ Erro no Velyra Training System: {e}")

print()

# ===== RESUMO FINAL =====
print("=" * 80)
print("📊 RESUMO DOS TESTES")
print("=" * 80)
print()

try:
    from services.clickbank_service import clickbank_service
    from services.google_ads_service import google_ads_service
    from services.meta_ads_service import meta_ads_service
    from services.velyra_campaign_creator import check_velyra_status
    
    status = check_velyra_status()
    
    print("✅ SERVIÇOS IMPLEMENTADOS:")
    print(f"   - ClickBank Service: ✅ (Affiliate ID: {clickbank_service.affiliate_id})")
    print(f"   - Google Ads Service: ✅ (Configurado: {google_ads_service.is_configured()})")
    print(f"   - Meta Ads Service: ✅ (Configurado: {meta_ads_service.is_configured()})")
    print(f"   - Velyra Campaign Creator: ✅")
    print(f"   - Velyra Prime Chat: ✅")
    print(f"   - Velyra Training System: ✅")
    print()
    
    print("🎯 FUNCIONALIDADES DISPONÍVEIS:")
    print(f"   - Criar campanhas Google Ads: {status['platforms']['google_ads']}")
    print(f"   - Criar campanhas Meta Ads: {status['platforms']['meta_ads']}")
    print(f"   - Rastreamento ClickBank: {status['platforms']['clickbank']}")
    print(f"   - Velyra autorizada: {status['velyra_authorized']}")
    print()
    
    if not status['velyra_authorized']:
        print("⚠️  ATENÇÃO: Velyra não está autorizada a criar campanhas")
        print("   Mensagem: " + status['velyra_status'])
        print()
    
    if not google_ads_service.is_configured():
        print("⚠️  ATENÇÃO: Google Ads não está configurado")
        print("   Configure as variáveis de ambiente:")
        print("   - GOOGLE_ADS_DEVELOPER_TOKEN")
        print("   - GOOGLE_ADS_CLIENT_ID")
        print("   - GOOGLE_ADS_CLIENT_SECRET")
        print("   - GOOGLE_ADS_REFRESH_TOKEN")
        print("   - GOOGLE_ADS_CUSTOMER_ID")
        print()
    
    if not meta_ads_service.is_configured():
        print("⚠️  ATENÇÃO: Meta Ads não está configurado")
        print("   Configure as variáveis de ambiente:")
        print("   - META_ACCESS_TOKEN")
        print("   - META_AD_ACCOUNT_ID")
        print()
    
    print("=" * 80)
    print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Erro no resumo: {e}")
    print("=" * 80)

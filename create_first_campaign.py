#!/usr/bin/env python3
"""
Script para criar a primeira campanha real no Facebook Ads
Modo Assistido - Humano no Loop
"""

import os
import json
import requests
from datetime import datetime, timedelta

# Configurações da conta
ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
AD_ACCOUNT_ID = 'act_851930913002539'
PAGE_ID = '110733095359498'

# API Base URL
API_VERSION = 'v18.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

def create_campaign(name, objective='OUTCOME_TRAFFIC', status='PAUSED'):
    """
    Cria uma campanha no Facebook Ads
    
    Args:
        name: Nome da campanha
        objective: Objetivo da campanha (LINK_CLICKS, CONVERSIONS, etc.)
        status: Status inicial (PAUSED para revisão humana)
    
    Returns:
        dict: Resposta da API com ID da campanha
    """
    url = f'{BASE_URL}/{AD_ACCOUNT_ID}/campaigns'
    
    params = {
        'name': name,
        'objective': objective,
        'status': status,
        'special_ad_categories': '[]',  # Sem categorias especiais
        'is_adset_budget_sharing_enabled': 'false',  # Budget no nível do ad set
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(url, data=params)
    return response.json()

def create_ad_set(campaign_id, name, daily_budget, targeting, start_time, end_time, status='PAUSED'):
    """
    Cria um conjunto de anúncios (Ad Set)
    
    Args:
        campaign_id: ID da campanha
        name: Nome do conjunto
        daily_budget: Orçamento diário em centavos (ex: 5000 = R$ 50)
        targeting: Dicionário com segmentação
        start_time: Data/hora de início
        end_time: Data/hora de término
        status: Status inicial
    
    Returns:
        dict: Resposta da API com ID do ad set
    """
    url = f'{BASE_URL}/{AD_ACCOUNT_ID}/adsets'
    
    params = {
        'name': name,
        'campaign_id': campaign_id,
        'daily_budget': daily_budget,
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'LINK_CLICKS',
        'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
        'targeting': json.dumps(targeting),
        'start_time': start_time,
        'end_time': end_time,
        'status': status,
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(url, data=params)
    return response.json()

def create_ad_creative(name, message, link, image_hash=None):
    """
    Cria um criativo de anúncio
    
    Args:
        name: Nome do criativo
        message: Texto principal do anúncio
        link: URL de destino
        image_hash: Hash da imagem (opcional)
    
    Returns:
        dict: Resposta da API com ID do criativo
    """
    url = f'{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives'
    
    object_story_spec = {
        'page_id': PAGE_ID,
        'link_data': {
            'message': message,
            'link': link,
            'name': name,
            'call_to_action': {
                'type': 'LEARN_MORE'
            }
        }
    }
    
    if image_hash:
        object_story_spec['link_data']['image_hash'] = image_hash
    
    params = {
        'name': name,
        'object_story_spec': json.dumps(object_story_spec),
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(url, data=params)
    return response.json()

def create_ad(name, adset_id, creative_id, status='PAUSED'):
    """
    Cria um anúncio
    
    Args:
        name: Nome do anúncio
        adset_id: ID do conjunto de anúncios
        creative_id: ID do criativo
        status: Status inicial
    
    Returns:
        dict: Resposta da API com ID do anúncio
    """
    url = f'{BASE_URL}/{AD_ACCOUNT_ID}/ads'
    
    params = {
        'name': name,
        'adset_id': adset_id,
        'creative': json.dumps({'creative_id': creative_id}),
        'status': status,
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(url, data=params)
    return response.json()

def create_first_campaign_guided():
    """
    Fluxo guiado para criar a primeira campanha
    Modo Assistido - Todos os anúncios ficam PAUSADOS para revisão humana
    """
    print("🚀 CRIANDO PRIMEIRA CAMPANHA - MODO ASSISTIDO")
    print("=" * 60)
    
    # Configurações da campanha de teste
    campaign_name = f"Nexora Prime - Teste {datetime.now().strftime('%Y-%m-%d')}"
    daily_budget = 3000  # R$ 30/dia (em centavos)
    duration_days = 3
    
    # Datas
    start_time = datetime.now().isoformat()
    end_time = (datetime.now() + timedelta(days=duration_days)).isoformat()
    
    # Segmentação simples (Brasil, interesses básicos)
    targeting = {
        'geo_locations': {
            'countries': ['BR']
        },
        'age_min': 25,
        'age_max': 55,
        'interests': [
            {'id': '6003139266461', 'name': 'Marketing'},  # Marketing
            {'id': '6003020834693', 'name': 'Empreendedorismo'}  # Empreendedorismo
        ]
    }
    
    print(f"\n📋 Configurações:")
    print(f"   Nome: {campaign_name}")
    print(f"   Orçamento Diário: R$ {daily_budget/100:.2f}")
    print(f"   Duração: {duration_days} dias")
    print(f"   Início: {start_time}")
    print(f"   Término: {end_time}")
    print(f"   Segmentação: Brasil, 25-55 anos, Interesses: Marketing e Empreendedorismo")
    
    # Passo 1: Criar Campanha
    print(f"\n1️⃣ Criando campanha...")
    campaign_result = create_campaign(
        name=campaign_name,
        objective='OUTCOME_TRAFFIC',
        status='PAUSED'  # Pausada para revisão
    )
    
    if 'error' in campaign_result:
        print(f"   ❌ Erro: {campaign_result['error']['message']}")
        return campaign_result
    
    campaign_id = campaign_result['id']
    print(f"   ✅ Campanha criada: {campaign_id}")
    
    # Passo 2: Criar Ad Set
    print(f"\n2️⃣ Criando conjunto de anúncios...")
    adset_result = create_ad_set(
        campaign_id=campaign_id,
        name=f"{campaign_name} - Ad Set 1",
        daily_budget=daily_budget,
        targeting=targeting,
        start_time=start_time,
        end_time=end_time,
        status='PAUSED'
    )
    
    if 'error' in adset_result:
        print(f"   ❌ Erro: {adset_result['error']['message']}")
        return adset_result
    
    adset_id = adset_result['id']
    print(f"   ✅ Ad Set criado: {adset_id}")
    
    # Passo 3: Criar Criativo
    print(f"\n3️⃣ Criando criativo do anúncio...")
    creative_result = create_ad_creative(
        name=f"{campaign_name} - Criativo 1",
        message="🚀 Transforme seu marketing com IA! Descubra como o Nexora Prime pode automatizar suas campanhas e aumentar seus resultados.",
        link="https://nexoraprime.com"
    )
    
    if 'error' in creative_result:
        print(f"   ❌ Erro: {creative_result['error']['message']}")
        return creative_result
    
    creative_id = creative_result['id']
    print(f"   ✅ Criativo criado: {creative_id}")
    
    # Passo 4: Criar Anúncio
    print(f"\n4️⃣ Criando anúncio...")
    ad_result = create_ad(
        name=f"{campaign_name} - Anúncio 1",
        adset_id=adset_id,
        creative_id=creative_id,
        status='PAUSED'
    )
    
    if 'error' in ad_result:
        print(f"   ❌ Erro: {ad_result['error']['message']}")
        return ad_result
    
    ad_id = ad_result['id']
    print(f"   ✅ Anúncio criado: {ad_id}")
    
    # Resumo
    print(f"\n" + "=" * 60)
    print(f"✅ CAMPANHA CRIADA COM SUCESSO!")
    print(f"=" * 60)
    print(f"\n📊 IDs criados:")
    print(f"   Campanha: {campaign_id}")
    print(f"   Ad Set: {adset_id}")
    print(f"   Criativo: {creative_id}")
    print(f"   Anúncio: {ad_id}")
    
    print(f"\n⚠️  IMPORTANTE:")
    print(f"   - Todos os anúncios estão PAUSADOS")
    print(f"   - Revise no Facebook Ads Manager")
    print(f"   - Ative manualmente quando estiver pronto")
    print(f"   - URL: https://business.facebook.com/adsmanager/manage/campaigns?act={AD_ACCOUNT_ID.replace('act_', '')}")
    
    return {
        'success': True,
        'campaign_id': campaign_id,
        'adset_id': adset_id,
        'creative_id': creative_id,
        'ad_id': ad_id
    }

if __name__ == '__main__':
    result = create_first_campaign_guided()
    
    # Salvar resultado em arquivo
    with open('/home/ubuntu/first_campaign_result.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Resultado salvo em: /home/ubuntu/first_campaign_result.json")

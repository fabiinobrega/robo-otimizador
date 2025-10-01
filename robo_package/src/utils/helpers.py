#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_currency(value: float, currency: str = "BRL") -> str:
    """Formatar valor monetário"""
    if currency == "BRL":
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    elif currency == "USD":
        return f"${value:,.2f}"
    else:
        return f"{value:,.2f} {currency}"

def format_percentage(value: float) -> str:
    """Formatar porcentagem"""
    return f"{value:.1f}%"

def format_number(value: int) -> str:
    """Formatar número com separadores"""
    return f"{value:,}".replace(",", ".")

def generate_campaign_id() -> str:
    """Gerar ID único para campanha"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = secrets.token_hex(4)
    return f"CAMP_{timestamp}_{random_part.upper()}"

def validate_email(email: str) -> bool:
    """Validar formato de email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def hash_password(password: str) -> str:
    """Hash de senha com salt"""
    salt = secrets.token_hex(32)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{password_hash.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    """Verificar senha"""
    try:
        salt, password_hash = hashed.split(':')
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() == password_hash
    except:
        return False

def sanitize_filename(filename: str) -> str:
    """Sanitizar nome de arquivo"""
    import re
    # Remove caracteres especiais
    filename = re.sub(r'[^\w\s-.]', '', filename)
    # Remove espaços múltiplos
    filename = re.sub(r'\s+', '_', filename)
    return filename

def get_file_extension(filename: str) -> str:
    """Obter extensão do arquivo"""
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename: str, allowed_extensions: List[str]) -> bool:
    """Verificar se arquivo é permitido"""
    return get_file_extension(filename) in allowed_extensions

def calculate_campaign_metrics(impressions: int, clicks: int, conversions: int, cost: float) -> Dict[str, float]:
    """Calcular métricas de campanha"""
    ctr = (clicks / impressions * 100) if impressions > 0 else 0
    cpc = (cost / clicks) if clicks > 0 else 0
    conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
    cpa = (cost / conversions) if conversions > 0 else 0
    
    return {
        'ctr': round(ctr, 2),
        'cpc': round(cpc, 2),
        'conversion_rate': round(conversion_rate, 2),
        'cpa': round(cpa, 2)
    }

def estimate_campaign_performance(budget: float, platform: str, objective: str) -> Dict[str, Any]:
    """Estimar performance de campanha"""
    # Benchmarks por plataforma
    benchmarks = {
        'Facebook': {
            'Vendas': {'ctr': 3.5, 'cpc': 1.2, 'conversion_rate': 2.8},
            'Leads': {'ctr': 4.2, 'cpc': 0.8, 'conversion_rate': 5.5},
            'Trafego': {'ctr': 5.1, 'cpc': 0.6, 'conversion_rate': 1.2}
        },
        'Google': {
            'Vendas': {'ctr': 2.8, 'cpc': 1.8, 'conversion_rate': 3.2},
            'Leads': {'ctr': 3.5, 'cpc': 1.2, 'conversion_rate': 6.1},
            'Trafego': {'ctr': 4.2, 'cpc': 0.9, 'conversion_rate': 1.8}
        }
    }
    
    bench = benchmarks.get(platform, {}).get(objetivo, {'ctr': 3.0, 'cpc': 1.0, 'conversion_rate': 2.0})
    
    clicks = int(budget / bench['cpc'])
    impressions = int(clicks / (bench['ctr'] / 100))
    conversions = int(clicks * (bench['conversion_rate'] / 100))
    
    return {
        'impressions': impressions,
        'clicks': clicks,
        'conversions': conversions,
        'ctr': bench['ctr'],
        'cpc': bench['cpc'],
        'conversion_rate': bench['conversion_rate'],
        'estimated_cost': budget
    }

def generate_copy_variations(base_copy: str, variations: int = 3) -> List[str]:
    """Gerar variações de copy"""
    # Simulação de variações (em produção, usaria IA)
    variations_list = [base_copy]
    
    # Variações simples para demonstração
    if "incrível" in base_copy.lower():
        variations_list.append(base_copy.replace("incrível", "fantástico"))
    if "agora" in base_copy.lower():
        variations_list.append(base_copy.replace("agora", "hoje mesmo"))
    if "!" in base_copy:
        variations_list.append(base_copy.replace("!", "."))
    
    return variations_list[:variations + 1]

def validate_campaign_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validar dados de campanha"""
    errors = []
    warnings = []
    
    # Validações obrigatórias
    required_fields = ['nome', 'objetivo', 'orcamento_diario', 'publico_alvo']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Campo '{field}' é obrigatório")
    
    # Validações de valor
    if data.get('orcamento_diario', 0) < 10:
        errors.append("Orçamento diário deve ser pelo menos R$ 10,00")
    
    if data.get('idade_min', 0) < 18:
        warnings.append("Idade mínima recomendada é 18 anos")
    
    if data.get('idade_max', 0) > 65:
        warnings.append("Idade máxima recomendada é 65 anos")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def log_user_action(user_id: int, action: str, details: str = None):
    """Registrar ação do usuário"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'user_id': user_id,
        'action': action,
        'details': details
    }
    logger.info(f"User Action: {json.dumps(log_entry)}")

def get_platform_limits(platform: str) -> Dict[str, Any]:
    """Obter limites da plataforma"""
    limits = {
        'Facebook': {
            'min_budget': 10.0,
            'max_budget': 10000.0,
            'min_age': 13,
            'max_age': 65,
            'max_copy_length': 125,
            'max_headline_length': 40
        },
        'Google': {
            'min_budget': 5.0,
            'max_budget': 50000.0,
            'min_age': 18,
            'max_age': 65,
            'max_copy_length': 90,
            'max_headline_length': 30
        }
    }
    return limits.get(platform, {})

def format_datetime(dt: datetime, format_type: str = 'default') -> str:
    """Formatar data e hora"""
    formats = {
        'default': '%d/%m/%Y %H:%M',
        'date_only': '%d/%m/%Y',
        'time_only': '%H:%M',
        'iso': '%Y-%m-%dT%H:%M:%S',
        'friendly': '%d de %B de %Y às %H:%M'
    }
    
    if format_type == 'friendly':
        months = {
            1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
            5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
            9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
        }
        return f"{dt.day} de {months[dt.month]} de {dt.year} às {dt.strftime('%H:%M')}"
    
    return dt.strftime(formats.get(format_type, formats['default']))

def get_color_by_status(status: str) -> str:
    """Obter cor por status"""
    colors = {
        'active': 'success',
        'paused': 'warning',
        'stopped': 'danger',
        'draft': 'secondary',
        'pending': 'info',
        'approved': 'success',
        'rejected': 'danger'
    }
    return colors.get(status.lower(), 'secondary')

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncar texto"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

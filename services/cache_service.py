"""
Cache Service - Nexora Prime
============================

Implementa cache em memória para APIs frequentes.
Melhora performance reduzindo queries ao banco de dados.
"""

import time
from functools import wraps
from typing import Any, Dict, Optional
import threading

class CacheService:
    """Serviço de cache em memória com TTL."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache se existir e não estiver expirado."""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if entry['expires_at'] > time.time():
                    return entry['value']
                else:
                    # Expirado, remover
                    del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        """Define valor no cache com TTL em segundos."""
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl
            }
    
    def delete(self, key: str) -> None:
        """Remove valor do cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def clear(self) -> None:
        """Limpa todo o cache."""
        with self._lock:
            self._cache.clear()
    
    def clear_pattern(self, pattern: str) -> int:
        """Limpa todas as chaves que começam com o padrão."""
        count = 0
        with self._lock:
            keys_to_delete = [k for k in self._cache.keys() if k.startswith(pattern)]
            for key in keys_to_delete:
                del self._cache[key]
                count += 1
        return count


# Instância global do cache
cache = CacheService()


def cached(ttl: int = 60, key_prefix: str = ""):
    """
    Decorator para cache de funções.
    
    Args:
        ttl: Tempo de vida do cache em segundos
        key_prefix: Prefixo para a chave do cache
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Criar chave única baseada nos argumentos
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Verificar cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Executar função e armazenar resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator


def invalidate_cache(pattern: str):
    """
    Decorator para invalidar cache após execução.
    
    Args:
        pattern: Padrão de chaves a invalidar
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            cache.clear_pattern(pattern)
            return result
        return wrapper
    return decorator


# TTLs padrão para diferentes tipos de dados
CACHE_TTL = {
    'dashboard_metrics': 30,      # 30 segundos
    'campaigns_list': 60,         # 1 minuto
    'campaign_detail': 120,       # 2 minutos
    'reports': 300,               # 5 minutos
    'static_data': 3600,          # 1 hora
}

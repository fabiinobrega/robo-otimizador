"""
Sistema Completo de Monitoramento - NEXORA PRIME v11.7
Logging avançado, alertas de erro, monitoramento de performance e analytics
"""

import logging
import time
import json
import os
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
import sqlite3

# Configurar logging avançado
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configurar múltiplos handlers de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Handler para arquivo geral
        logging.FileHandler(LOG_DIR / 'nexora.log'),
        # Handler para erros
        logging.FileHandler(LOG_DIR / 'errors.log', mode='a'),
        # Handler para console
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('nexora_monitoring')

# Handler separado para erros críticos
error_handler = logging.FileHandler(LOG_DIR / 'errors.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
    'File: %(pathname)s:%(lineno)d\n'
    'Function: %(funcName)s\n'
    '---'
))
logger.addHandler(error_handler)


class PerformanceMonitor:
    """Monitor de performance para endpoints e funções"""
    
    def __init__(self):
        self.metrics = {}
        self.db_path = Path(__file__).parent.parent / 'database.db'
    
    def track_request(self, endpoint, method, duration, status_code, user_id=None):
        """Registra métricas de uma requisição"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endpoint TEXT NOT NULL,
                    method TEXT NOT NULL,
                    duration REAL NOT NULL,
                    status_code INTEGER NOT NULL,
                    user_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Inserir métrica
            cursor.execute('''
                INSERT INTO performance_metrics (endpoint, method, duration, status_code, user_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (endpoint, method, duration, status_code, user_id))
            
            conn.commit()
            conn.close()
            
            # Log se performance ruim
            if duration > 2.0:
                logger.warning(f"Slow request: {method} {endpoint} took {duration:.2f}s")
            
        except Exception as e:
            logger.error(f"Error tracking performance: {e}")
    
    def get_metrics_summary(self, hours=24):
        """Retorna resumo de métricas das últimas N horas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_requests,
                    AVG(duration) as avg_duration,
                    MAX(duration) as max_duration,
                    MIN(duration) as min_duration,
                    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as error_count,
                    SUM(CASE WHEN status_code < 400 THEN 1 ELSE 0 END) as success_count
                FROM performance_metrics
                WHERE timestamp >= ?
            ''', (cutoff_time.isoformat(),))
            
            result = cursor.fetchone()
            conn.close()
            
            return {
                'total_requests': result[0] or 0,
                'avg_duration': round(result[1] or 0, 3),
                'max_duration': round(result[2] or 0, 3),
                'min_duration': round(result[3] or 0, 3),
                'error_count': result[4] or 0,
                'success_count': result[5] or 0,
                'error_rate': round((result[4] or 0) / (result[0] or 1) * 100, 2)
            }
        except Exception as e:
            logger.error(f"Error getting metrics summary: {e}")
            return {}
    
    def get_slow_endpoints(self, threshold=1.0, limit=10):
        """Retorna endpoints mais lentos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    endpoint,
                    method,
                    AVG(duration) as avg_duration,
                    COUNT(*) as request_count
                FROM performance_metrics
                WHERE duration > ?
                GROUP BY endpoint, method
                ORDER BY avg_duration DESC
                LIMIT ?
            ''', (threshold, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'endpoint': row[0],
                    'method': row[1],
                    'avg_duration': round(row[2], 3),
                    'request_count': row[3]
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Error getting slow endpoints: {e}")
            return []


class AlertSystem:
    """Sistema de alertas para erros e eventos críticos"""
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / 'database.db'
        self.alert_thresholds = {
            'error_rate': 10,  # % de erros
            'slow_requests': 5,  # requests lentas por minuto
            'high_memory': 80,  # % de uso de memória
            'high_cpu': 80  # % de uso de CPU
        }
    
    def create_alert(self, alert_type, severity, message, details=None):
        """Cria um alerta no sistema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    message TEXT NOT NULL,
                    details TEXT,
                    resolved BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    resolved_at DATETIME
                )
            ''')
            
            # Inserir alerta
            cursor.execute('''
                INSERT INTO system_alerts (alert_type, severity, message, details)
                VALUES (?, ?, ?, ?)
            ''', (alert_type, severity, message, json.dumps(details) if details else None))
            
            conn.commit()
            alert_id = cursor.lastrowid
            conn.close()
            
            # Log baseado na severidade
            if severity == 'critical':
                logger.critical(f"ALERT: {alert_type} - {message}")
            elif severity == 'high':
                logger.error(f"ALERT: {alert_type} - {message}")
            elif severity == 'medium':
                logger.warning(f"ALERT: {alert_type} - {message}")
            else:
                logger.info(f"ALERT: {alert_type} - {message}")
            
            return alert_id
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return None
    
    def get_active_alerts(self, severity=None):
        """Retorna alertas ativos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if severity:
                cursor.execute('''
                    SELECT id, alert_type, severity, message, details, created_at
                    FROM system_alerts
                    WHERE resolved = 0 AND severity = ?
                    ORDER BY created_at DESC
                ''', (severity,))
            else:
                cursor.execute('''
                    SELECT id, alert_type, severity, message, details, created_at
                    FROM system_alerts
                    WHERE resolved = 0
                    ORDER BY created_at DESC
                ''')
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'alert_type': row[1],
                    'severity': row[2],
                    'message': row[3],
                    'details': json.loads(row[4]) if row[4] else None,
                    'created_at': row[5]
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []
    
    def resolve_alert(self, alert_id):
        """Marca um alerta como resolvido"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE system_alerts
                SET resolved = 1, resolved_at = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), alert_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Alert {alert_id} resolved")
            return True
            
        except Exception as e:
            logger.error(f"Error resolving alert: {e}")
            return False
    
    def check_error_rate(self, monitor):
        """Verifica taxa de erros e cria alerta se necessário"""
        metrics = monitor.get_metrics_summary(hours=1)
        error_rate = metrics.get('error_rate', 0)
        
        if error_rate > self.alert_thresholds['error_rate']:
            self.create_alert(
                'high_error_rate',
                'high',
                f'Taxa de erros alta: {error_rate}%',
                {'error_rate': error_rate, 'threshold': self.alert_thresholds['error_rate']}
            )


class AnalyticsTracker:
    """Sistema de analytics para rastrear eventos e comportamento do usuário"""
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / 'database.db'
    
    def track_event(self, event_type, event_name, properties=None, user_id=None):
        """Registra um evento de analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    event_name TEXT NOT NULL,
                    properties TEXT,
                    user_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Inserir evento
            cursor.execute('''
                INSERT INTO analytics_events (event_type, event_name, properties, user_id)
                VALUES (?, ?, ?, ?)
            ''', (event_type, event_name, json.dumps(properties) if properties else None, user_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error tracking event: {e}")
    
    def get_event_stats(self, event_type=None, hours=24):
        """Retorna estatísticas de eventos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            if event_type:
                cursor.execute('''
                    SELECT event_name, COUNT(*) as count
                    FROM analytics_events
                    WHERE event_type = ? AND timestamp >= ?
                    GROUP BY event_name
                    ORDER BY count DESC
                ''', (event_type, cutoff_time.isoformat()))
            else:
                cursor.execute('''
                    SELECT event_type, event_name, COUNT(*) as count
                    FROM analytics_events
                    WHERE timestamp >= ?
                    GROUP BY event_type, event_name
                    ORDER BY count DESC
                ''', (cutoff_time.isoformat(),))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'event_type': row[0] if not event_type else event_type,
                    'event_name': row[1] if not event_type else row[0],
                    'count': row[2] if not event_type else row[1]
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Error getting event stats: {e}")
            return []
    
    def get_user_journey(self, user_id, limit=50):
        """Retorna jornada do usuário (últimos eventos)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT event_type, event_name, properties, timestamp
                FROM analytics_events
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'event_type': row[0],
                    'event_name': row[1],
                    'properties': json.loads(row[2]) if row[2] else None,
                    'timestamp': row[3]
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Error getting user journey: {e}")
            return []


# Decorador para monitorar performance de funções
def monitor_performance(func):
    """Decorador para monitorar performance de funções"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(f"{func.__name__} executed in {duration:.3f}s")
            
            if duration > 1.0:
                logger.warning(f"Slow function: {func.__name__} took {duration:.3f}s")
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Error in {func.__name__} after {duration:.3f}s: {e}")
            raise
    
    return wrapper


# Decorador para rastrear eventos
def track_event(event_type, event_name):
    """Decorador para rastrear eventos de analytics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                
                # Rastrear evento
                tracker = AnalyticsTracker()
                tracker.track_event(event_type, event_name)
                
                return result
            except Exception as e:
                logger.error(f"Error in tracked function {func.__name__}: {e}")
                raise
        
        return wrapper
    return decorator


# Instâncias globais
performance_monitor = PerformanceMonitor()
alert_system = AlertSystem()
analytics_tracker = AnalyticsTracker()


# Função para obter dashboard de monitoramento
def get_monitoring_dashboard():
    """Retorna dashboard completo de monitoramento"""
    return {
        'performance': performance_monitor.get_metrics_summary(hours=24),
        'slow_endpoints': performance_monitor.get_slow_endpoints(threshold=1.0, limit=5),
        'active_alerts': alert_system.get_active_alerts(),
        'critical_alerts': alert_system.get_active_alerts(severity='critical'),
        'event_stats': analytics_tracker.get_event_stats(hours=24),
        'timestamp': datetime.now().isoformat()
    }


# Exportar
__all__ = [
    'logger',
    'performance_monitor',
    'alert_system',
    'analytics_tracker',
    'monitor_performance',
    'track_event',
    'get_monitoring_dashboard'
]

"""
Sistema de Logs Inteligentes
Logging automático com análise e alertas

Autor: Manus AI Agent
Data: 25/11/2024
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any
import sqlite3
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nexora_prime.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('NexoraPrime')


class IntelligentLogger:
    """
    Logger inteligente que analisa padrões e gera alertas
    """
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self._init_logging_tables()
    
    def _init_logging_tables(self):
        """Inicializar tabelas de logging"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabela de logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    category TEXT NOT NULL,
                    message TEXT NOT NULL,
                    data TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de alertas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    severity TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    resolved BOOLEAN DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Erro ao inicializar tabelas de logging: {e}")
    
    def log(self, level: str, category: str, message: str, data: Dict = None):
        """
        Log inteligente com categorização
        """
        try:
            # Log no arquivo
            log_func = getattr(logger, level.lower(), logger.info)
            log_func(f"[{category}] {message}")
            
            # Salvar no banco
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO system_logs (level, category, message, data)
                VALUES (?, ?, ?, ?)
            """, (level, category, message, json.dumps(data) if data else None))
            
            conn.commit()
            conn.close()
            
            # Analisar se precisa gerar alerta
            self._analyze_for_alerts(level, category, message, data)
            
        except Exception as e:
            logger.error(f"Erro ao fazer log: {e}")
    
    def _analyze_for_alerts(self, level: str, category: str, message: str, data: Dict):
        """
        Analisa logs e gera alertas automáticos
        """
        try:
            # Alertas baseados em padrões
            alerts = []
            
            # Erro crítico
            if level == 'ERROR' or level == 'CRITICAL':
                alerts.append({
                    "severity": "HIGH",
                    "title": f"Erro {level} detectado",
                    "description": f"[{category}] {message}"
                })
            
            # Performance ruim
            if data and 'response_time' in data:
                if data['response_time'] > 3000:  # > 3s
                    alerts.append({
                        "severity": "MEDIUM",
                        "title": "Performance degradada",
                        "description": f"Tempo de resposta: {data['response_time']}ms"
                    })
            
            # Taxa de erro alta
            if category == 'API' and data and 'status_code' in data:
                if data['status_code'] >= 500:
                    alerts.append({
                        "severity": "HIGH",
                        "title": "Erro de servidor",
                        "description": f"Status {data['status_code']}: {message}"
                    })
            
            # Salvar alertas
            if alerts:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                for alert in alerts:
                    cursor.execute("""
                        INSERT INTO system_alerts (severity, title, description)
                        VALUES (?, ?, ?)
                    """, (alert['severity'], alert['title'], alert['description']))
                
                conn.commit()
                conn.close()
                
        except Exception as e:
            logger.error(f"Erro ao analisar alertas: {e}")
    
    def get_recent_logs(self, limit: int = 100, category: str = None) -> list:
        """
        Buscar logs recentes
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if category:
                cursor.execute("""
                    SELECT * FROM system_logs
                    WHERE category = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (category, limit))
            else:
                cursor.execute("""
                    SELECT * FROM system_logs
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (limit,))
            
            logs = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return logs
            
        except Exception as e:
            logger.error(f"Erro ao buscar logs: {e}")
            return []
    
    def get_unresolved_alerts(self) -> list:
        """
        Buscar alertas não resolvidos
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM system_alerts
                WHERE resolved = 0
                ORDER BY created_at DESC
            """)
            
            alerts = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return alerts
            
        except Exception as e:
            logger.error(f"Erro ao buscar alertas: {e}")
            return []
    
    def resolve_alert(self, alert_id: int):
        """
        Marcar alerta como resolvido
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE system_alerts
                SET resolved = 1
                WHERE id = ?
            """, (alert_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Alerta {alert_id} resolvido")
            
        except Exception as e:
            logger.error(f"Erro ao resolver alerta: {e}")


# Instância global
intelligent_logger = IntelligentLogger()


# Funções de conveniência
def log_info(category: str, message: str, data: Dict = None):
    """Log de informação"""
    intelligent_logger.log('INFO', category, message, data)


def log_warning(category: str, message: str, data: Dict = None):
    """Log de aviso"""
    intelligent_logger.log('WARNING', category, message, data)


def log_error(category: str, message: str, data: Dict = None):
    """Log de erro"""
    intelligent_logger.log('ERROR', category, message, data)


def log_critical(category: str, message: str, data: Dict = None):
    """Log crítico"""
    intelligent_logger.log('CRITICAL', category, message, data)


# Exportar
__all__ = [
    'intelligent_logger',
    'log_info',
    'log_warning',
    'log_error',
    'log_critical'
]

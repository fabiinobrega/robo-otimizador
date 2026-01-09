"""
📝 LOGGER - Logs Estruturados e Auditáveis
Nexora Prime — FASE 1

Sistema de logging estruturado que registra todas as decisões
e ações do Manus IA de forma auditável e rastreável.

Formato obrigatório:
{
  "timestamp": "",
  "agent": "manus",
  "task_id": "",
  "state": "",
  "action": "",
  "decision": "",
  "reasoning": "",
  "result": "",
  "confidence": 0.0
}

Regras:
- Nenhuma decisão sem log
- Nenhuma falha sem explicação
- Logs humanos + técnicos
- Logs alimentam aprendizado da Velyra Prime

Autor: Manus AI - FASE 1
Data: 08 de Janeiro de 2026
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from enum import Enum


class LogLevel(Enum):
    """Níveis de log"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogCategory(Enum):
    """Categorias de log"""
    SYSTEM = "SYSTEM"
    TASK = "TASK"
    DECISION = "DECISION"
    ERROR = "ERROR"
    AUDIT = "AUDIT"


class ManusLogger:
    """
    Logger Estruturado do Manus IA
    
    Registra todas as ações e decisões de forma auditável.
    Persiste em banco de dados e arquivos JSON.
    """
    
    def __init__(self, db_path: str = "/home/ubuntu/robo-otimizador/data/logs.db"):
        self.db_path = db_path
        self.agent_name = "manus"
        self._ensure_db_exists()
        self._init_database()
        
        print(f"[LOGGER] ✅ Logger inicializado: {self.db_path}")
    
    def _ensure_db_exists(self):
        """Garante que o diretório do banco existe"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """Inicializa o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent TEXT NOT NULL,
                level TEXT NOT NULL,
                category TEXT NOT NULL,
                task_id TEXT,
                state TEXT,
                action TEXT,
                decision TEXT,
                reasoning TEXT,
                result TEXT,
                confidence REAL,
                metadata TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Índices para performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON logs(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category 
            ON logs(category)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_id 
            ON logs(task_id)
        """)
        
        conn.commit()
        conn.close()
    
    def log(
        self,
        level: LogLevel,
        category: LogCategory,
        message: str,
        task_id: Optional[str] = None,
        state: Optional[str] = None,
        action: Optional[str] = None,
        decision: Optional[str] = None,
        reasoning: Optional[str] = None,
        result: Optional[Any] = None,
        confidence: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Registra log estruturado
        
        Args:
            level: Nível do log
            category: Categoria do log
            message: Mensagem principal
            task_id: ID da tarefa relacionada
            state: Estado do agente
            action: Ação executada
            decision: Decisão tomada
            reasoning: Raciocínio da decisão
            result: Resultado da ação
            confidence: Confiança na decisão (0.0 a 1.0)
            metadata: Metadados adicionais
        """
        timestamp = datetime.now().isoformat()
        
        # Cria registro estruturado
        log_entry = {
            "timestamp": timestamp,
            "agent": self.agent_name,
            "level": level.value,
            "category": category.value,
            "message": message,
            "task_id": task_id,
            "state": state,
            "action": action,
            "decision": decision,
            "reasoning": reasoning,
            "result": result,
            "confidence": confidence,
            "metadata": metadata
        }
        
        # Persiste no banco
        self._persist_log(log_entry)
        
        # Imprime no console (formato humano)
        self._print_log(log_entry)
    
    def _persist_log(self, log_entry: Dict[str, Any]):
        """
        Persiste log no banco de dados
        
        Args:
            log_entry: Entrada de log
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO logs (
                    timestamp, agent, level, category, task_id, state, action,
                    decision, reasoning, result, confidence, metadata, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_entry['timestamp'],
                log_entry['agent'],
                log_entry['level'],
                log_entry['category'],
                log_entry.get('task_id'),
                log_entry.get('state'),
                log_entry.get('action'),
                log_entry.get('decision'),
                log_entry.get('reasoning'),
                json.dumps(log_entry.get('result')) if log_entry.get('result') else None,
                log_entry.get('confidence'),
                json.dumps(log_entry.get('metadata')) if log_entry.get('metadata') else None,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"[LOGGER ERROR] ❌ Erro ao persistir log: {e}")
    
    def _print_log(self, log_entry: Dict[str, Any]):
        """
        Imprime log no console em formato humano
        
        Args:
            log_entry: Entrada de log
        """
        level = log_entry['level']
        category = log_entry['category']
        message = log_entry['message']
        
        # Emoji por nível
        emoji = {
            'DEBUG': '🔍',
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'CRITICAL': '🚨'
        }.get(level, 'ℹ️')
        
        # Formato básico
        log_line = f"[{log_entry['timestamp']}] {emoji} [{category}] {message}"
        
        # Adiciona informações extras se disponíveis
        if log_entry.get('task_id'):
            log_line += f" | Task: {log_entry['task_id']}"
        
        if log_entry.get('decision'):
            log_line += f" | Decisão: {log_entry['decision']}"
        
        if log_entry.get('confidence') is not None:
            log_line += f" | Confiança: {log_entry['confidence']:.2%}"
        
        print(log_line)
        
        # Imprime reasoning se disponível (indentado)
        if log_entry.get('reasoning'):
            print(f"  💭 Raciocínio: {log_entry['reasoning']}")
    
    def log_decision(
        self,
        decision: str,
        reasoning: str,
        confidence: float,
        task_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Registra uma decisão do agente
        
        Args:
            decision: Decisão tomada
            reasoning: Raciocínio da decisão
            confidence: Confiança (0.0 a 1.0)
            task_id: ID da tarefa relacionada
            metadata: Metadados adicionais
        """
        self.log(
            level=LogLevel.INFO,
            category=LogCategory.DECISION,
            message=f"Decisão tomada: {decision}",
            task_id=task_id,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            metadata=metadata
        )
    
    def log_error(
        self,
        error: str,
        task_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Registra um erro
        
        Args:
            error: Mensagem de erro
            task_id: ID da tarefa relacionada
            metadata: Metadados adicionais
        """
        self.log(
            level=LogLevel.ERROR,
            category=LogCategory.ERROR,
            message=error,
            task_id=task_id,
            metadata=metadata
        )
    
    def log_audit(
        self,
        action: str,
        result: Any,
        task_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Registra ação auditável
        
        Args:
            action: Ação executada
            result: Resultado da ação
            task_id: ID da tarefa relacionada
            metadata: Metadados adicionais
        """
        self.log(
            level=LogLevel.INFO,
            category=LogCategory.AUDIT,
            message=f"Ação auditável: {action}",
            task_id=task_id,
            action=action,
            result=result,
            metadata=metadata
        )
    
    def get_logs(
        self,
        category: Optional[LogCategory] = None,
        task_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Busca logs
        
        Args:
            category: Filtrar por categoria
            task_id: Filtrar por tarefa
            limit: Limite de resultados
            
        Returns:
            Lista de logs
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM logs WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category.value)
            
            if task_id:
                query += " AND task_id = ?"
                params.append(task_id)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            logs = []
            for row in rows:
                log = dict(zip(columns, row))
                
                # Parse JSON fields
                if log.get('result'):
                    try:
                        log['result'] = json.loads(log['result'])
                    except:
                        pass
                
                if log.get('metadata'):
                    try:
                        log['metadata'] = json.loads(log['metadata'])
                    except:
                        pass
                
                logs.append(log)
            
            conn.close()
            return logs
            
        except Exception as e:
            print(f"[LOGGER ERROR] ❌ Erro ao buscar logs: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas dos logs
        
        Returns:
            Dict com estatísticas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de logs
            cursor.execute("SELECT COUNT(*) FROM logs")
            total = cursor.fetchone()[0]
            
            # Por categoria
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM logs
                GROUP BY category
            """)
            by_category = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Por nível
            cursor.execute("""
                SELECT level, COUNT(*) as count
                FROM logs
                GROUP BY level
            """)
            by_level = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Decisões com baixa confiança
            cursor.execute("""
                SELECT COUNT(*) FROM logs
                WHERE category = 'DECISION' AND confidence < 0.7
            """)
            low_confidence_decisions = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_logs": total,
                "by_category": by_category,
                "by_level": by_level,
                "low_confidence_decisions": low_confidence_decisions
            }
            
        except Exception as e:
            print(f"[LOGGER ERROR] ❌ Erro ao obter estatísticas: {e}")
            return {}


# Instância global do logger
_logger_instance: Optional[ManusLogger] = None


def get_logger() -> ManusLogger:
    """
    Retorna instância global do logger (singleton)
    
    Returns:
        ManusLogger: Instância do logger
    """
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = ManusLogger()
    
    return _logger_instance

"""
📋 TASK MODELS - Modelos de Tarefas
Nexora Prime — FASE 1

Define os modelos de dados para tarefas do sistema.

Autor: Manus AI - FASE 1
Data: 08 de Janeiro de 2026
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
import json


class TaskStatus(Enum):
    """Estados possíveis de uma tarefa"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class TaskPriority(Enum):
    """Prioridades de tarefas"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Task:
    """
    Modelo de tarefa do sistema
    
    Representa uma tarefa que será executada pelo Manus Agent.
    Persiste em banco de dados e sobrevive a restarts.
    """
    
    def __init__(
        self,
        task_id: str = None,
        task_type: str = None,
        payload: Dict[str, Any] = None,
        created_at: Optional[datetime] = None,
        attempts: int = 0,
        max_attempts: int = 3,
        status: TaskStatus = TaskStatus.PENDING,
        priority: TaskPriority = TaskPriority.MEDIUM
    ):
        self.task_id = task_id or f"task_{int(datetime.now().timestamp() * 1000)}"
        self.task_type = task_type
        self.payload = payload or {}
        self.created_at = created_at or datetime.now()
        self.attempts = attempts
        self.max_attempts = max_attempts
        self.status = status
        self.priority = priority
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte tarefa para dicionário
        
        Returns:
            Dict com dados da tarefa
        """
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "payload": self.payload,
            "created_at": self.created_at.isoformat(),
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error_message": self.error_message
        }
    
    def to_json(self) -> str:
        """
        Converte tarefa para JSON
        
        Returns:
            String JSON
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Cria tarefa a partir de dicionário
        
        Args:
            data: Dicionário com dados da tarefa
            
        Returns:
            Instância de Task
        """
        task = cls(
            task_id=data['task_id'],
            task_type=data['task_type'],
            payload=data['payload'],
            created_at=datetime.fromisoformat(data['created_at']),
            attempts=data.get('attempts', 0),
            max_attempts=data.get('max_attempts', 3),
            status=TaskStatus(data.get('status', 'PENDING'))
        )
        
        if data.get('started_at'):
            task.started_at = datetime.fromisoformat(data['started_at'])
        
        if data.get('completed_at'):
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        
        task.result = data.get('result')
        task.error_message = data.get('error_message')
        
        return task
    
    def mark_running(self):
        """Marca tarefa como em execução"""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now()
    
    def mark_success(self, result: Dict[str, Any]):
        """
        Marca tarefa como concluída com sucesso
        
        Args:
            result: Resultado da execução
        """
        self.status = TaskStatus.SUCCESS
        self.completed_at = datetime.now()
        self.result = result
    
    def mark_failed(self, error: str):
        """
        Marca tarefa como falha
        
        Args:
            error: Mensagem de erro
        """
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now()
        self.error_message = error
    
    def increment_attempts(self):
        """Incrementa contador de tentativas"""
        self.attempts += 1
    
    def can_retry(self) -> bool:
        """
        Verifica se a tarefa pode ser retentada
        
        Returns:
            bool: True se pode fazer retry, False caso contrário
        """
        return self.attempts < self.max_attempts
    
    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, type={self.task_type}, status={self.status.value}, attempts={self.attempts}/{self.max_attempts})"


# Tipos de tarefas suportados (FASE 1)
TASK_TYPES = {
    "monitor_system": "Monitorar estado do sistema",
    "check_health": "Verificar saúde do sistema",
    "log_metrics": "Registrar métricas",
    "validate_config": "Validar configuração",
}

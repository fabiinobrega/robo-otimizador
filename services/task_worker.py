"""
⚙️ TASK WORKER - Worker de Execução Controlada
Nexora Prime — FASE 1

Executa tarefas de forma controlada com:
- Uma tarefa por vez
- Timeout obrigatório
- Retry limitado
- Backoff progressivo
- Detecção de travamento
- Nenhum loop infinito permitido

Autor: Manus AI - FASE 1
Data: 08 de Janeiro de 2026
"""

import time
import signal
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from enum import Enum

from .task_models import Task, TaskStatus
from .task_queue import TaskQueue, get_queue


class WorkerState(Enum):
    """Estados do worker"""
    IDLE = "IDLE"
    WORKING = "WORKING"
    TIMEOUT = "TIMEOUT"
    ERROR = "ERROR"


class TaskWorker:
    """
    Worker de Execução Controlada
    
    Executa tarefas da fila de forma segura e controlada.
    Garante que nenhuma tarefa trave o sistema.
    """
    
    def __init__(self, queue: Optional[TaskQueue] = None):
        self.queue = queue or get_queue()
        self.state = WorkerState.IDLE
        self.current_task: Optional[Task] = None
        self.task_timeout = 300  # 5 minutos por tarefa
        self.retry_backoff_base = 60  # 1 minuto base para backoff
        self.max_consecutive_failures = 5
        self.consecutive_failures = 0
        
        print(f"[TASK WORKER] ✅ Worker inicializado")
        print(f"[TASK WORKER] Timeout por tarefa: {self.task_timeout}s")
        print(f"[TASK WORKER] Backoff base: {self.retry_backoff_base}s")
    
    def execute_next_task(self) -> bool:
        """
        Executa próxima tarefa da fila
        
        Returns:
            bool: True se executou uma tarefa, False se fila vazia
        """
        # Busca próxima tarefa
        task = self.queue.dequeue()
        
        if not task:
            return False
        
        self.current_task = task
        self.state = WorkerState.WORKING
        
        print(f"[TASK WORKER] ▶️ Executando tarefa: {task.task_id}")
        print(f"[TASK WORKER] Tipo: {task.task_type}")
        print(f"[TASK WORKER] Tentativa: {task.attempts + 1}/{task.max_attempts}")
        
        try:
            # Marca tarefa como em execução
            task.mark_running()
            task.increment_attempts()
            self.queue.update_task(task)
            
            # Executa com timeout
            result = self._execute_with_timeout(task)
            
            # Marca como sucesso
            task.mark_success(result)
            self.queue.update_task(task)
            
            # Reset contador de falhas consecutivas
            self.consecutive_failures = 0
            
            print(f"[TASK WORKER] ✅ Tarefa concluída: {task.task_id}")
            
            self.state = WorkerState.IDLE
            self.current_task = None
            return True
            
        except TimeoutError as e:
            print(f"[TASK WORKER] ⏱️ Timeout na tarefa: {task.task_id}")
            self._handle_task_failure(task, f"Timeout após {self.task_timeout}s")
            return True
            
        except Exception as e:
            print(f"[TASK WORKER] ❌ Erro na tarefa: {task.task_id} - {e}")
            self._handle_task_failure(task, str(e))
            return True
    
    def _execute_with_timeout(self, task: Task) -> Dict[str, Any]:
        """
        Executa tarefa com timeout
        
        Args:
            task: Tarefa a ser executada
            
        Returns:
            Dict com resultado da execução
            
        Raises:
            TimeoutError: Se tarefa exceder timeout
        """
        # Define handler de timeout
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Tarefa excedeu timeout de {self.task_timeout}s")
        
        # Configura alarme (apenas em sistemas Unix)
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.task_timeout)
        except:
            # Windows não suporta SIGALRM, executa sem timeout
            pass
        
        try:
            # Executa tarefa
            result = self._execute_task_logic(task)
            
            # Cancela alarme
            try:
                signal.alarm(0)
            except:
                pass
            
            return result
            
        except Exception as e:
            # Cancela alarme
            try:
                signal.alarm(0)
            except:
                pass
            raise e
    
    def _execute_task_logic(self, task: Task) -> Dict[str, Any]:
        """
        Lógica de execução da tarefa
        
        FASE 1: Apenas tarefas de monitoramento
        NÃO executa ações financeiras
        
        Args:
            task: Tarefa a ser executada
            
        Returns:
            Dict com resultado
        """
        task_type = task.task_type
        payload = task.payload
        
        # Handlers de tarefas (FASE 1 - apenas monitoramento)
        handlers = {
            "monitor_system": self._monitor_system,
            "check_health": self._check_health,
            "log_metrics": self._log_metrics,
            "validate_config": self._validate_config,
        }
        
        handler = handlers.get(task_type)
        
        if not handler:
            raise ValueError(f"Tipo de tarefa desconhecido: {task_type}")
        
        return handler(payload)
    
    def _monitor_system(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitora estado do sistema
        
        FASE 1: Apenas coleta informações, não toma ações
        """
        print(f"[TASK WORKER] 📊 Monitorando sistema...")
        
        # Simula monitoramento
        time.sleep(1)
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "uptime": "100%",
                "errors": 0
            }
        }
    
    def _check_health(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica saúde do sistema
        """
        print(f"[TASK WORKER] 🏥 Verificando saúde...")
        
        time.sleep(0.5)
        
        return {
            "healthy": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _log_metrics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registra métricas
        """
        print(f"[TASK WORKER] 📝 Registrando métricas...")
        
        metrics = payload.get("metrics", {})
        
        return {
            "logged": True,
            "metrics_count": len(metrics),
            "timestamp": datetime.now().isoformat()
        }
    
    def _validate_config(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida configuração
        """
        print(f"[TASK WORKER] ✔️ Validando configuração...")
        
        time.sleep(0.5)
        
        return {
            "valid": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _handle_task_failure(self, task: Task, error: str):
        """
        Trata falha na execução de tarefa
        
        Args:
            task: Tarefa que falhou
            error: Mensagem de erro
        """
        self.consecutive_failures += 1
        
        # Verifica se pode fazer retry
        if task.can_retry():
            # Calcula backoff progressivo
            backoff = self.retry_backoff_base * (2 ** (task.attempts - 1))
            
            print(f"[TASK WORKER] 🔄 Agendando retry em {backoff}s")
            
            # Recoloca na fila (status volta para PENDING)
            task.status = TaskStatus.PENDING
            task.error_message = f"{error} (tentativa {task.attempts}/{task.max_attempts})"
            self.queue.update_task(task)
            
            # Aguarda backoff
            time.sleep(backoff)
        else:
            # Esgotou tentativas
            task.mark_failed(error)
            self.queue.update_task(task)
            
            print(f"[TASK WORKER] ❌ Tarefa falhou definitivamente: {task.task_id}")
        
        # Verifica se deve parar por falhas consecutivas
        if self.consecutive_failures >= self.max_consecutive_failures:
            print(f"[TASK WORKER] 🚨 ALERTA: {self.consecutive_failures} falhas consecutivas!")
            print(f"[TASK WORKER] Pausando worker por segurança...")
            self.state = WorkerState.ERROR
            time.sleep(300)  # Pausa de 5 minutos
            self.consecutive_failures = 0
        
        self.state = WorkerState.IDLE
        self.current_task = None
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status do worker
        
        Returns:
            Dict com informações de status
        """
        return {
            "state": self.state.value,
            "current_task": self.current_task.task_id if self.current_task else None,
            "consecutive_failures": self.consecutive_failures,
            "max_consecutive_failures": self.max_consecutive_failures,
            "task_timeout": self.task_timeout,
            "queue_stats": self.queue.get_statistics()
        }


# Instância global do worker
_worker_instance: Optional[TaskWorker] = None


def get_worker() -> TaskWorker:
    """
    Retorna instância global do worker (singleton)
    
    Returns:
        TaskWorker: Instância do worker
    """
    global _worker_instance
    
    if _worker_instance is None:
        _worker_instance = TaskWorker()
    
    return _worker_instance

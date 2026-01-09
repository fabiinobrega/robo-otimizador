"""
📥 TASK QUEUE - Fila de Tarefas Persistente
Nexora Prime — FASE 1

Gerencia fila de tarefas com persistência em banco de dados.
Sobrevive a restarts e implementa retry inteligente.

Autor: Manus AI - FASE 1
Data: 08 de Janeiro de 2026
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from .task_models import Task, TaskStatus


class TaskQueue:
    """
    Fila de Tarefas Persistente
    
    Gerencia tarefas com persistência em SQLite.
    Garante que nenhuma tarefa seja perdida em caso de restart.
    """
    
    def __init__(self, db_path: str = "/home/ubuntu/robo-otimizador/data/task_queue.db"):
        self.db_path = db_path
        self._ensure_db_exists()
        self._init_database()
    
    def _ensure_db_exists(self):
        """Garante que o diretório do banco existe"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """Inicializa o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de tarefas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                task_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                status TEXT NOT NULL,
                attempts INTEGER DEFAULT 0,
                max_attempts INTEGER DEFAULT 3,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                result TEXT,
                error_message TEXT
            )
        """)
        
        # Índices para performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON tasks(status)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON tasks(created_at)
        """)
        
        conn.commit()
        conn.close()
        
        print(f"[TASK QUEUE] ✅ Banco de dados inicializado: {self.db_path}")
    
    def enqueue(self, task: Task) -> bool:
        """
        Adiciona tarefa à fila
        
        Args:
            task: Tarefa a ser adicionada
            
        Returns:
            bool: True se adicionada com sucesso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO tasks (
                    task_id, task_type, payload, status, attempts, max_attempts, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id,
                task.task_type,
                json.dumps(task.payload),
                task.status.value,
                task.attempts,
                task.max_attempts,
                task.created_at.isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            print(f"[TASK QUEUE] ✅ Tarefa enfileirada: {task.task_id} ({task.task_type})")
            return True
            
        except Exception as e:
            print(f"[TASK QUEUE] ❌ Erro ao enfileirar tarefa: {e}")
            return False
    
    def dequeue(self) -> Optional[Task]:
        """
        Remove e retorna próxima tarefa pendente
        
        Returns:
            Task ou None se fila vazia
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Busca tarefa pendente mais antiga
            cursor.execute("""
                SELECT * FROM tasks
                WHERE status = 'PENDING'
                ORDER BY created_at ASC
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            # Converte row para Task
            task = self._row_to_task(row)
            
            print(f"[TASK QUEUE] 📤 Tarefa removida da fila: {task.task_id}")
            return task
            
        except Exception as e:
            print(f"[TASK QUEUE] ❌ Erro ao remover tarefa: {e}")
            return None
    
    def update_task(self, task: Task) -> bool:
        """
        Atualiza tarefa no banco
        
        Args:
            task: Tarefa atualizada
            
        Returns:
            bool: True se atualizada com sucesso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE tasks SET
                    status = ?,
                    attempts = ?,
                    started_at = ?,
                    completed_at = ?,
                    result = ?,
                    error_message = ?
                WHERE task_id = ?
            """, (
                task.status.value,
                task.attempts,
                task.started_at.isoformat() if task.started_at else None,
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.result) if task.result else None,
                task.error_message,
                task.task_id
            ))
            
            conn.commit()
            conn.close()
            
            print(f"[TASK QUEUE] 🔄 Tarefa atualizada: {task.task_id} (status: {task.status.value})")
            return True
            
        except Exception as e:
            print(f"[TASK QUEUE] ❌ Erro ao atualizar tarefa: {e}")
            return False
    
    def get_pending_count(self) -> int:
        """
        Retorna quantidade de tarefas pendentes
        
        Returns:
            int: Número de tarefas pendentes
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM tasks
                WHERE status = 'PENDING'
            """)
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            print(f"[TASK QUEUE] ❌ Erro ao contar tarefas pendentes: {e}")
            return 0
    
    def get_all_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """
        Retorna todas as tarefas (opcionalmente filtradas por status)
        
        Args:
            status: Status para filtrar (None = todas)
            
        Returns:
            Lista de tarefas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if status:
                cursor.execute("""
                    SELECT * FROM tasks
                    WHERE status = ?
                    ORDER BY created_at DESC
                """, (status.value,))
            else:
                cursor.execute("""
                    SELECT * FROM tasks
                    ORDER BY created_at DESC
                """)
            
            rows = cursor.fetchall()
            conn.close()
            
            tasks = [self._row_to_task(row) for row in rows]
            return tasks
            
        except Exception as e:
            print(f"[TASK QUEUE] ❌ Erro ao buscar tarefas: {e}")
            return []
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Busca tarefa por ID
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            Task ou None se não encontrada
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM tasks
                WHERE task_id = ?
            """, (task_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return self._row_to_task(row)
            
        except Exception as e:
            print(f"[TASK QUEUE] ❌ Erro ao buscar tarefa: {e}")
            return None
    
    def clear_completed(self, older_than_days: int = 7) -> int:
        """
        Remove tarefas concluídas antigas
        
        Args:
            older_than_days: Remover tarefas mais antigas que X dias
            
        Returns:
            int: Número de tarefas removidas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now().timestamp() - (older_than_days * 86400)
            cutoff_iso = datetime.fromtimestamp(cutoff_date).isoformat()
            
            cursor.execute("""
                DELETE FROM tasks
                WHERE status IN ('SUCCESS', 'FAILED')
                AND completed_at < ?
            """, (cutoff_iso,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            print(f"[TASK QUEUE] 🗑️ Removidas {deleted_count} tarefas antigas")
            return deleted_count
            
        except Exception as e:
            print(f"[TASK QUEUE] ❌ Erro ao limpar tarefas: {e}")
            return 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas da fila
        
        Returns:
            Dict com estatísticas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Conta por status
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM tasks
                GROUP BY status
            """)
            
            status_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Total
            cursor.execute("SELECT COUNT(*) FROM tasks")
            total = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total": total,
                "pending": status_counts.get('PENDING', 0),
                "running": status_counts.get('RUNNING', 0),
                "success": status_counts.get('SUCCESS', 0),
                "failed": status_counts.get('FAILED', 0),
                "by_status": status_counts
            }
            
        except Exception as e:
            print(f"[TASK QUEUE] ❌ Erro ao obter estatísticas: {e}")
            return {}
    
    def _row_to_task(self, row: tuple) -> Task:
        """
        Converte row do banco para Task
        
        Args:
            row: Tupla com dados do banco
            
        Returns:
            Instância de Task
        """
        task = Task(
            task_id=row[0],
            task_type=row[1],
            payload=json.loads(row[2]),
            status=TaskStatus(row[3]),
            attempts=row[4],
            max_attempts=row[5],
            created_at=datetime.fromisoformat(row[6])
        )
        
        if row[7]:  # started_at
            task.started_at = datetime.fromisoformat(row[7])
        
        if row[8]:  # completed_at
            task.completed_at = datetime.fromisoformat(row[8])
        
        if row[9]:  # result
            task.result = json.loads(row[9])
        
        if row[10]:  # error_message
            task.error_message = row[10]
        
        return task


# Instância global da fila
_queue_instance: Optional[TaskQueue] = None


def get_queue() -> TaskQueue:
    """
    Retorna instância global da fila (singleton)
    
    Returns:
        TaskQueue: Instância da fila
    """
    global _queue_instance
    
    if _queue_instance is None:
        _queue_instance = TaskQueue()
    
    return _queue_instance

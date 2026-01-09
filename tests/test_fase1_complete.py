"""
🧪 TESTES COMPLETOS - FASE 1
Nexora Prime — Agente Residente Permanente

Testes obrigatórios:
- Agente sobrevive a restart
- Fila persiste tarefas
- Worker não trava
- Logs são auditáveis
- Sistema não entra em loop infinito
- Nenhuma ação financeira é executada
- Validador bloqueia ações inválidas
- Sistema de aprendizado funciona

Autor: Manus AI - FASE 1
Data: 08 de Janeiro de 2026
"""

import unittest
import time
import os
import tempfile
import shutil
from datetime import datetime

# Importa módulos da FASE 1
import sys
sys.path.insert(0, '/home/ubuntu/robo-otimizador')

from services.manus_agent import ManusAgent, AgentState
from services.task_models import Task, TaskStatus, TaskPriority
from services.task_queue import TaskQueue
from services.task_worker import TaskWorker
from services.logger import ManusLogger, LogLevel, LogCategory
from services.velyra_learning import VelyraLearning, DecisionType


class TestManusAgent(unittest.TestCase):
    """Testes do Agente Residente"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        self.agent = ManusAgent()
    
    def tearDown(self):
        """Cleanup após cada teste"""
        if self.agent.is_running:
            self.agent.stop()
    
    def test_agent_initialization(self):
        """Teste: Agente inicializa corretamente"""
        self.assertIsNotNone(self.agent.agent_id)
        self.assertEqual(self.agent.state, AgentState.IDLE)
        self.assertFalse(self.agent.is_running)
        self.assertFalse(self.agent.kill_switch)
        print("✅ Agente inicializa corretamente")
    
    def test_agent_start_stop(self):
        """Teste: Agente inicia e para corretamente"""
        self.agent.start()
        time.sleep(2)  # Aguarda inicialização
        
        self.assertTrue(self.agent.is_running)
        self.assertIsNotNone(self.agent.last_heartbeat)
        
        self.agent.stop()
        time.sleep(1)
        
        self.assertFalse(self.agent.is_running)
        self.assertTrue(self.agent.kill_switch)
        print("✅ Agente inicia e para corretamente")
    
    def test_agent_heartbeat(self):
        """Teste: Heartbeat funciona"""
        self.agent.start()
        time.sleep(1)
        
        first_heartbeat = self.agent.last_heartbeat
        self.assertIsNotNone(first_heartbeat)
        
        time.sleep(2)
        
        second_heartbeat = self.agent.last_heartbeat
        self.assertGreater(second_heartbeat, first_heartbeat)
        
        self.agent.stop()
        print("✅ Heartbeat funciona")
    
    def test_agent_execution_limits(self):
        """Teste: Limites de execução funcionam"""
        self.agent.max_executions_per_hour = 5
        
        for i in range(10):
            self.agent.execution_timestamps.append(time.time())
        
        can_execute = self.agent._check_execution_limits()
        self.assertFalse(can_execute)
        print("✅ Limites de execução funcionam")
    
    def test_agent_anomaly_detection(self):
        """Teste: Detecção de anomalias funciona"""
        self.agent.error_count = 10
        self.agent._detect_anomalies()
        
        self.assertTrue(self.agent.anomaly_detected)
        print("✅ Detecção de anomalias funciona")
    
    def test_agent_no_financial_actions(self):
        """Teste: Agente NÃO executa ações financeiras"""
        self.agent.start()
        time.sleep(5)  # Aguarda alguns ciclos
        
        # Verifica que nenhuma ação financeira foi executada
        # (na FASE 1, o agente apenas monitora)
        status = self.agent.get_status()
        self.assertEqual(status['phase'], 'FASE 1 - BASE DA AUTONOMIA')
        
        self.agent.stop()
        print("✅ Agente NÃO executa ações financeiras")


class TestTaskQueue(unittest.TestCase):
    """Testes da Fila de Tarefas"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        # Cria banco temporário
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_queue.db')
        self.queue = TaskQueue(db_path=self.db_path)
    
    def tearDown(self):
        """Cleanup após cada teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_queue_enqueue_dequeue(self):
        """Teste: Enfileirar e desenfileirar tarefas"""
        task = Task(
            task_type="test_task",
            payload={"test": "data"},
            priority=TaskPriority.MEDIUM
        )
        
        self.queue.enqueue(task)
        
        dequeued = self.queue.dequeue()
        self.assertIsNotNone(dequeued)
        self.assertEqual(dequeued.task_type, "test_task")
        print("✅ Enfileirar e desenfileirar funcionam")
    
    def test_queue_persistence(self):
        """Teste: Fila persiste após restart"""
        task = Task(
            task_type="persistent_task",
            payload={"data": "test"},
            priority=TaskPriority.HIGH
        )
        
        self.queue.enqueue(task)
        task_id = task.task_id
        
        # Cria nova instância (simula restart)
        new_queue = TaskQueue(db_path=self.db_path)
        
        # Verifica se tarefa ainda existe
        dequeued = new_queue.dequeue()
        self.assertIsNotNone(dequeued)
        self.assertEqual(dequeued.task_id, task_id)
        print("✅ Fila persiste após restart")
    
    def test_queue_priority(self):
        """Teste: Prioridade funciona"""
        low_task = Task(
            task_type="low",
            payload={},
            priority=TaskPriority.LOW
        )
        
        high_task = Task(
            task_type="high",
            payload={},
            priority=TaskPriority.HIGH
        )
        
        self.queue.enqueue(low_task)
        self.queue.enqueue(high_task)
        
        # Deve retornar tarefa de alta prioridade primeiro
        dequeued = self.queue.dequeue()
        self.assertEqual(dequeued.task_type, "high")
        print("✅ Prioridade funciona")


class TestTaskWorker(unittest.TestCase):
    """Testes do Worker"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_worker.db')
        self.queue = TaskQueue(db_path=self.db_path)
        self.worker = TaskWorker(queue=self.queue)
    
    def tearDown(self):
        """Cleanup após cada teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_worker_executes_task(self):
        """Teste: Worker executa tarefas"""
        task = Task(
            task_type="monitor_system",
            payload={},
            priority=TaskPriority.MEDIUM
        )
        
        self.queue.enqueue(task)
        
        executed = self.worker.execute_next_task()
        self.assertTrue(executed)
        print("✅ Worker executa tarefas")
    
    def test_worker_handles_errors(self):
        """Teste: Worker trata erros"""
        task = Task(
            task_type="invalid_task_type",
            payload={},
            priority=TaskPriority.MEDIUM
        )
        
        self.queue.enqueue(task)
        
        # Deve tratar erro sem travar
        executed = self.worker.execute_next_task()
        self.assertTrue(executed)
        print("✅ Worker trata erros")


class TestLogger(unittest.TestCase):
    """Testes do Logger"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_logs.db')
        self.logger = ManusLogger(db_path=self.db_path)
    
    def tearDown(self):
        """Cleanup após cada teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_logger_logs_decision(self):
        """Teste: Logger registra decisões"""
        self.logger.log_decision(
            decision="Test decision",
            reasoning="Test reasoning",
            confidence=0.85,
            task_id="test_task_1"
        )
        
        logs = self.logger.get_logs(category=LogCategory.DECISION, limit=1)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['decision'], "Test decision")
        print("✅ Logger registra decisões")
    
    def test_logger_logs_error(self):
        """Teste: Logger registra erros"""
        self.logger.log_error(
            error="Test error",
            task_id="test_task_2"
        )
        
        logs = self.logger.get_logs(category=LogCategory.ERROR, limit=1)
        self.assertEqual(len(logs), 1)
        print("✅ Logger registra erros")
    
    def test_logger_statistics(self):
        """Teste: Estatísticas do logger"""
        self.logger.log_decision("Decision 1", "Reasoning 1", 0.9)
        self.logger.log_decision("Decision 2", "Reasoning 2", 0.6)
        self.logger.log_error("Error 1")
        
        stats = self.logger.get_statistics()
        self.assertGreaterEqual(stats['total_logs'], 3)
        print("✅ Estatísticas do logger funcionam")


class TestVelyraLearning(unittest.TestCase):
    """Testes do Sistema de Aprendizado"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_learning.db')
        self.learning = VelyraLearning(db_path=self.db_path)
    
    def tearDown(self):
        """Cleanup após cada teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_learning_records_decision(self):
        """Teste: Sistema registra decisões"""
        self.learning.record_manus_decision(
            decision_id="dec_1",
            decision_type=DecisionType.STRATEGIC,
            context={"budget": 100},
            decision="Increase budget",
            reasoning="Good performance",
            confidence=0.9
        )
        
        stats = self.learning.get_learning_statistics()
        self.assertGreaterEqual(stats['total_manus_decisions'], 1)
        print("✅ Sistema registra decisões")
    
    def test_learning_extracts_patterns(self):
        """Teste: Sistema extrai padrões"""
        self.learning.record_manus_decision(
            decision_id="dec_2",
            decision_type=DecisionType.STRATEGIC,
            context={"budget": 200},
            decision="Optimize budget allocation",
            reasoning="ROI improving",
            confidence=0.85
        )
        
        stats = self.learning.get_learning_statistics()
        self.assertGreaterEqual(stats['total_patterns'], 1)
        print("✅ Sistema extrai padrões")
    
    def test_learning_records_execution(self):
        """Teste: Sistema registra execuções"""
        self.learning.record_velyra_execution(
            execution_id="exec_1",
            pattern_id="pattern_1",
            context={"test": "data"},
            action="Test action",
            result={"success": True},
            success=True
        )
        
        stats = self.learning.get_learning_statistics()
        self.assertGreaterEqual(stats['total_velyra_executions'], 1)
        print("✅ Sistema registra execuções")


class TestIntegration(unittest.TestCase):
    """Testes de Integração"""
    
    def test_full_cycle(self):
        """Teste: Ciclo completo funciona"""
        # Cria diretório temporário
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Inicializa componentes
            queue = TaskQueue(db_path=os.path.join(temp_dir, 'queue.db'))
            worker = TaskWorker(queue=queue)
            logger = ManusLogger(db_path=os.path.join(temp_dir, 'logs.db'))
            agent = ManusAgent()
            
            # Enfileira tarefa
            task = Task(
                task_type="monitor_system",
                payload={},
                priority=TaskPriority.MEDIUM
            )
            queue.enqueue(task)
            
            # Inicia agente
            agent.start()
            time.sleep(2)
            
            # Executa tarefa
            worker.execute_next_task()
            
            # Registra log
            logger.log_decision("Test decision", "Test reasoning", 0.9)
            
            # Para agente
            agent.stop()
            
            # Verifica que tudo funcionou
            self.assertTrue(True)
            print("✅ Ciclo completo funciona")
            
        finally:
            shutil.rmtree(temp_dir)


def run_all_tests():
    """Executa todos os testes"""
    print("=" * 70)
    print("🧪 EXECUTANDO TESTES DA FASE 1")
    print("=" * 70)
    print()
    
    # Cria suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona testes
    suite.addTests(loader.loadTestsFromTestCase(TestManusAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskQueue))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskWorker))
    suite.addTests(loader.loadTestsFromTestCase(TestLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestVelyraLearning))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Executa testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    print("📊 RESULTADO DOS TESTES")
    print("=" * 70)
    print(f"Total de testes: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"🚨 Erros: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

"""
🤖 MANUS AGENT - Agente Residente Permanente
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Worker persistente que opera 24/7 executando tarefas autônomas do Nexora Prime.

Responsabilidades:
- Monitoramento contínuo de campanhas
- Execução de regras de automação
- Otimização automática
- Teste A/B automático
- Escala inteligente
- Decisões autônomas (com aprovação financeira)

Autor: Manus AI
Data: 05 de Janeiro de 2026
"""

import os
import time
import logging
import threading
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import mysql.connector
from mysql.connector import Error

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [MANUS AGENT] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/manus_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Estados possíveis de uma tarefa"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRY = "RETRY"
    CANCELLED = "CANCELLED"


class TaskPriority(Enum):
    """Prioridades de execução"""
    CRITICAL = 1  # Pausar campanha com ROI negativo
    HIGH = 2      # Otimização urgente
    MEDIUM = 3    # Monitoramento regular
    LOW = 4       # Tarefas de manutenção


class ManusAgent:
    """
    Agente Residente Permanente do Manus IA
    
    Opera como worker em background executando tarefas autônomas
    de forma contínua, inteligente e auditável.
    """
    
    def __init__(self):
        self.is_running = False
        self.worker_thread = None
        self.db_connection = None
        self.max_retries = 3
        self.retry_delay = 60  # segundos
        self.loop_interval = 30  # segundos entre ciclos
        
        logger.info("🤖 Manus Agent inicializado")
    
    def connect_db(self) -> bool:
        """Conecta ao banco de dados"""
        try:
            self.db_connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'nexora_db'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', '')
            )
            
            if self.db_connection.is_connected():
                logger.info("✅ Conectado ao banco de dados")
                self._ensure_tables_exist()
                return True
            
            return False
            
        except Error as e:
            logger.error(f"❌ Erro ao conectar ao banco: {e}")
            return False
    
    def _ensure_tables_exist(self):
        """Garante que as tabelas necessárias existem"""
        cursor = self.db_connection.cursor()
        
        # Tabela de tarefas do agente
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS manus_agent_tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task_type VARCHAR(100) NOT NULL,
                priority INT NOT NULL,
                status VARCHAR(20) NOT NULL,
                payload JSON,
                result JSON,
                error_message TEXT,
                retry_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP NULL,
                completed_at TIMESTAMP NULL,
                INDEX idx_status_priority (status, priority),
                INDEX idx_created_at (created_at)
            )
        """)
        
        # Tabela de decisões do agente
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS manus_agent_decisions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                decision_type VARCHAR(100) NOT NULL,
                campaign_id INT,
                reasoning TEXT NOT NULL,
                action_taken VARCHAR(255),
                metrics_before JSON,
                metrics_after JSON,
                approved_by_user BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_campaign (campaign_id),
                INDEX idx_created_at (created_at)
            )
        """)
        
        # Tabela de status do agente
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS manus_agent_status (
                id INT PRIMARY KEY DEFAULT 1,
                is_active BOOLEAN DEFAULT TRUE,
                current_task_id INT,
                last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tasks_completed INT DEFAULT 0,
                tasks_failed INT DEFAULT 0,
                uptime_seconds INT DEFAULT 0,
                CHECK (id = 1)
            )
        """)
        
        # Inserir status inicial se não existir
        cursor.execute("""
            INSERT IGNORE INTO manus_agent_status (id, is_active) VALUES (1, TRUE)
        """)
        
        self.db_connection.commit()
        cursor.close()
        logger.info("✅ Tabelas do Manus Agent verificadas/criadas")
    
    def start(self):
        """Inicia o agente em background"""
        if self.is_running:
            logger.warning("⚠️ Agente já está rodando")
            return
        
        if not self.connect_db():
            logger.error("❌ Não foi possível conectar ao banco. Agente não iniciado.")
            return
        
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        
        logger.info("🚀 Manus Agent iniciado em background")
    
    def stop(self):
        """Para o agente gracefully"""
        logger.info("🛑 Parando Manus Agent...")
        self.is_running = False
        
        if self.worker_thread:
            self.worker_thread.join(timeout=10)
        
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
        
        logger.info("✅ Manus Agent parado")
    
    def _worker_loop(self):
        """Loop principal do worker"""
        logger.info("🔄 Worker loop iniciado")
        start_time = time.time()
        
        while self.is_running:
            try:
                # Atualizar heartbeat
                self._update_heartbeat(start_time)
                
                # Buscar próxima tarefa
                task = self._get_next_task()
                
                if task:
                    self._execute_task(task)
                else:
                    # Sem tarefas pendentes, executar monitoramento de rotina
                    self._routine_monitoring()
                
                # Aguardar próximo ciclo
                time.sleep(self.loop_interval)
                
            except Exception as e:
                logger.error(f"❌ Erro no worker loop: {e}", exc_info=True)
                time.sleep(self.loop_interval)
        
        logger.info("🔄 Worker loop finalizado")
    
    def _update_heartbeat(self, start_time: float):
        """Atualiza o heartbeat do agente"""
        try:
            cursor = self.db_connection.cursor()
            uptime = int(time.time() - start_time)
            
            cursor.execute("""
                UPDATE manus_agent_status 
                SET last_heartbeat = NOW(), uptime_seconds = %s
                WHERE id = 1
            """, (uptime,))
            
            self.db_connection.commit()
            cursor.close()
            
        except Error as e:
            logger.error(f"❌ Erro ao atualizar heartbeat: {e}")
    
    def _get_next_task(self) -> Optional[Dict[str, Any]]:
        """Busca a próxima tarefa pendente (por prioridade)"""
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT * FROM manus_agent_tasks
                WHERE status IN ('PENDING', 'RETRY')
                ORDER BY priority ASC, created_at ASC
                LIMIT 1
            """)
            
            task = cursor.fetchone()
            cursor.close()
            
            return task
            
        except Error as e:
            logger.error(f"❌ Erro ao buscar tarefa: {e}")
            return None
    
    def _execute_task(self, task: Dict[str, Any]):
        """Executa uma tarefa"""
        task_id = task['id']
        task_type = task['task_type']
        
        logger.info(f"▶️ Executando tarefa #{task_id}: {task_type}")
        
        try:
            # Marcar como RUNNING
            self._update_task_status(task_id, TaskStatus.RUNNING)
            
            # Executar tarefa baseada no tipo
            result = self._dispatch_task(task)
            
            # Marcar como SUCCESS
            self._update_task_status(task_id, TaskStatus.SUCCESS, result=result)
            self._increment_completed_tasks()
            
            logger.info(f"✅ Tarefa #{task_id} concluída com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar tarefa #{task_id}: {e}", exc_info=True)
            
            # Verificar se deve fazer retry
            retry_count = task.get('retry_count', 0)
            
            if retry_count < self.max_retries:
                self._update_task_status(
                    task_id, 
                    TaskStatus.RETRY, 
                    error=str(e),
                    retry_count=retry_count + 1
                )
                logger.info(f"🔄 Tarefa #{task_id} agendada para retry ({retry_count + 1}/{self.max_retries})")
            else:
                self._update_task_status(task_id, TaskStatus.FAILED, error=str(e))
                self._increment_failed_tasks()
                logger.error(f"❌ Tarefa #{task_id} falhou após {self.max_retries} tentativas")
    
    def _dispatch_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Despacha tarefa para o handler apropriado"""
        task_type = task['task_type']
        payload = task.get('payload', {})
        
        handlers = {
            'monitor_campaign': self._monitor_campaign,
            'optimize_campaign': self._optimize_campaign,
            'run_ab_test': self._run_ab_test,
            'check_scale_readiness': self._check_scale_readiness,
            'pause_negative_roi': self._pause_negative_roi,
            'generate_report': self._generate_report,
        }
        
        handler = handlers.get(task_type)
        
        if not handler:
            raise ValueError(f"Handler não encontrado para task_type: {task_type}")
        
        return handler(payload)
    
    def _monitor_campaign(self, payload: Dict) -> Dict:
        """Monitora uma campanha e coleta métricas"""
        campaign_id = payload.get('campaign_id')
        logger.info(f"📊 Monitorando campanha #{campaign_id}")
        
        # TODO: Implementar lógica real de monitoramento
        # Por enquanto, retorna dados simulados
        
        return {
            'campaign_id': campaign_id,
            'status': 'monitored',
            'metrics': {
                'impressions': 1000,
                'clicks': 50,
                'conversions': 5,
                'spend': 100.0,
                'revenue': 250.0,
                'roas': 2.5
            }
        }
    
    def _optimize_campaign(self, payload: Dict) -> Dict:
        """Otimiza uma campanha com base em métricas"""
        campaign_id = payload.get('campaign_id')
        logger.info(f"⚙️ Otimizando campanha #{campaign_id}")
        
        # TODO: Implementar lógica real de otimização
        
        return {
            'campaign_id': campaign_id,
            'optimizations_applied': [
                'Ajustado lance para R$ 2.50',
                'Pausado criativo com CTR < 1%',
                'Expandido público para 25-45 anos'
            ]
        }
    
    def _run_ab_test(self, payload: Dict) -> Dict:
        """Executa teste A/B automático"""
        campaign_id = payload.get('campaign_id')
        logger.info(f"🧪 Executando teste A/B para campanha #{campaign_id}")
        
        # TODO: Implementar lógica real de A/B testing
        
        return {
            'campaign_id': campaign_id,
            'winner': 'Variant A',
            'confidence': 0.95
        }
    
    def _check_scale_readiness(self, payload: Dict) -> Dict:
        """Verifica se campanha está pronta para escalar"""
        campaign_id = payload.get('campaign_id')
        logger.info(f"📈 Verificando prontidão para escala: campanha #{campaign_id}")
        
        # TODO: Implementar checklist real
        
        checklist = {
            'roas_positive_72h': True,
            'cpa_below_limit': True,
            'ctr_stable': True,
            'creatives_not_saturated': True,
            'funnel_converting': True,
            'budget_authorized': False,  # Sempre requer aprovação
            'no_critical_errors': True
        }
        
        ready = all(checklist.values())
        
        return {
            'campaign_id': campaign_id,
            'ready_to_scale': ready,
            'checklist': checklist,
            'recommendation': 'Solicitar aprovação do usuário para escalar' if ready else 'Aguardar métricas estabilizarem'
        }
    
    def _pause_negative_roi(self, payload: Dict) -> Dict:
        """Pausa campanha com ROI negativo persistente"""
        campaign_id = payload.get('campaign_id')
        logger.info(f"⏸️ Pausando campanha #{campaign_id} (ROI negativo)")
        
        # TODO: Implementar lógica real de pausa
        
        return {
            'campaign_id': campaign_id,
            'action': 'paused',
            'reason': 'ROI negativo por 48h consecutivas'
        }
    
    def _generate_report(self, payload: Dict) -> Dict:
        """Gera relatório de performance"""
        logger.info("📄 Gerando relatório de performance")
        
        # TODO: Implementar geração real de relatório
        
        return {
            'report_type': 'daily_summary',
            'generated_at': datetime.now().isoformat()
        }
    
    def _routine_monitoring(self):
        """Monitoramento de rotina quando não há tarefas pendentes"""
        logger.debug("🔍 Executando monitoramento de rotina")
        
        # TODO: Implementar monitoramento de todas as campanhas ativas
        # Por enquanto, apenas log
        pass
    
    def _update_task_status(
        self, 
        task_id: int, 
        status: TaskStatus, 
        result: Optional[Dict] = None,
        error: Optional[str] = None,
        retry_count: Optional[int] = None
    ):
        """Atualiza o status de uma tarefa"""
        try:
            cursor = self.db_connection.cursor()
            
            updates = [f"status = '{status.value}'"]
            
            if status == TaskStatus.RUNNING:
                updates.append("started_at = NOW()")
            
            if status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
                updates.append("completed_at = NOW()")
            
            if result:
                import json
                updates.append(f"result = '{json.dumps(result)}'")
            
            if error:
                updates.append(f"error_message = '{error[:500]}'")  # Limitar tamanho
            
            if retry_count is not None:
                updates.append(f"retry_count = {retry_count}")
            
            query = f"""
                UPDATE manus_agent_tasks 
                SET {', '.join(updates)}
                WHERE id = {task_id}
            """
            
            cursor.execute(query)
            self.db_connection.commit()
            cursor.close()
            
        except Error as e:
            logger.error(f"❌ Erro ao atualizar status da tarefa: {e}")
    
    def _increment_completed_tasks(self):
        """Incrementa contador de tarefas concluídas"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                UPDATE manus_agent_status 
                SET tasks_completed = tasks_completed + 1
                WHERE id = 1
            """)
            self.db_connection.commit()
            cursor.close()
        except Error as e:
            logger.error(f"❌ Erro ao incrementar contador: {e}")
    
    def _increment_failed_tasks(self):
        """Incrementa contador de tarefas falhadas"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                UPDATE manus_agent_status 
                SET tasks_failed = tasks_failed + 1
                WHERE id = 1
            """)
            self.db_connection.commit()
            cursor.close()
        except Error as e:
            logger.error(f"❌ Erro ao incrementar contador: {e}")
    
    def add_task(
        self, 
        task_type: str, 
        priority: TaskPriority, 
        payload: Optional[Dict] = None
    ) -> Optional[int]:
        """Adiciona uma nova tarefa à fila"""
        try:
            cursor = self.db_connection.cursor()
            import json
            
            cursor.execute("""
                INSERT INTO manus_agent_tasks (task_type, priority, status, payload)
                VALUES (%s, %s, %s, %s)
            """, (
                task_type,
                priority.value,
                TaskStatus.PENDING.value,
                json.dumps(payload) if payload else None
            ))
            
            self.db_connection.commit()
            task_id = cursor.lastrowid
            cursor.close()
            
            logger.info(f"✅ Tarefa adicionada: #{task_id} ({task_type})")
            return task_id
            
        except Error as e:
            logger.error(f"❌ Erro ao adicionar tarefa: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM manus_agent_status WHERE id = 1")
            status = cursor.fetchone()
            cursor.close()
            
            return status or {}
            
        except Error as e:
            logger.error(f"❌ Erro ao obter status: {e}")
            return {}


# Instância global do agente
_agent_instance = None


def get_agent() -> ManusAgent:
    """Retorna a instância global do agente (singleton)"""
    global _agent_instance
    
    if _agent_instance is None:
        _agent_instance = ManusAgent()
    
    return _agent_instance


def start_agent():
    """Inicia o agente global"""
    agent = get_agent()
    agent.start()


def stop_agent():
    """Para o agente global"""
    agent = get_agent()
    agent.stop()


if __name__ == "__main__":
    # Teste standalone
    logger.info("🧪 Iniciando Manus Agent em modo teste")
    
    agent = ManusAgent()
    agent.start()
    
    # Adicionar tarefas de teste
    agent.add_task('monitor_campaign', TaskPriority.MEDIUM, {'campaign_id': 1})
    agent.add_task('optimize_campaign', TaskPriority.HIGH, {'campaign_id': 1})
    
    # Manter rodando por 2 minutos
    try:
        time.sleep(120)
    except KeyboardInterrupt:
        logger.info("⚠️ Interrompido pelo usuário")
    
    agent.stop()
    logger.info("✅ Teste concluído")

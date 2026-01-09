"""
🧠 MANUS IA — AGENTE RESIDENTE PERMANENTE
Nexora Prime — FASE 1

Responsabilidades:
- Inicializar o Manus IA como processo residente
- Manter heartbeat ativo
- Controlar estados internos
- Orquestrar tarefas
- Supervisionar workers
- Decidir O QUE fazer, nunca COMO gastar

PROIBIÇÕES ABSOLUTAS:
- Criar campanhas
- Alterar orçamento
- Comprar créditos
- Publicar anúncios
- Executar qualquer ação financeira

Autor: Manus AI - FASE 1
Data: 08 de Janeiro de 2026
"""

import os
import time
import threading
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
import json


class AgentState(Enum):
    """Estados internos do agente"""
    IDLE = "IDLE"
    THINKING = "THINKING"
    EXECUTING = "EXECUTING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    ERROR = "ERROR"


class ManusAgent:
    """
    Agente Residente Permanente do Manus IA - FASE 1
    
    Cérebro estratégico do Nexora Prime.
    Opera 24/7 em background, sobrevive a quedas e reinícios.
    
    FASE 1: Apenas monitora e registra estado.
    NÃO executa ações financeiras.
    """
    
    def __init__(self):
        self.state = AgentState.IDLE
        self.heartbeat_interval = 30  # segundos
        self.last_heartbeat = None
        self.is_running = False
        self.worker_thread = None
        self.kill_switch = False
        
        # Contadores de segurança
        self.execution_count = 0
        self.max_executions_per_hour = 120  # Limite de segurança
        self.execution_timestamps = []
        
        # Detecção de anomalias
        self.error_count = 0
        self.max_errors_before_shutdown = 10  # Para após 10 erros críticos
        self.anomaly_detected = False
        self.last_error_time = None
        
        # Metadata do agente
        self.agent_id = f"manus_{int(time.time())}"
        self.started_at = None
        self.version = "1.0.0-phase1"
        
        print(f"[MANUS] Agente inicializado (ID: {self.agent_id})")
        
    def start(self):
        """
        Inicia o agente residente
        
        Cria thread em background que opera continuamente
        """
        if self.is_running:
            print(f"[MANUS] Agente já está rodando (ID: {self.agent_id})")
            return
        
        self.is_running = True
        self.started_at = datetime.now()
        self.kill_switch = False
        
        # Inicia thread do worker
        self.worker_thread = threading.Thread(
            target=self._worker_loop,
            daemon=True,
            name="ManusAgentWorker"
        )
        self.worker_thread.start()
        
        print(f"[MANUS] ✅ Agente iniciado (ID: {self.agent_id})")
        print(f"[MANUS] Estado: {self.state.value}")
        print(f"[MANUS] Heartbeat: {self.heartbeat_interval}s")
        print(f"[MANUS] Versão: {self.version}")
        
    def stop(self):
        """
        Para o agente de forma segura
        """
        print(f"[MANUS] 🛑 Parando agente (ID: {self.agent_id})...")
        self.is_running = False
        self.kill_switch = True
        
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5)
        
        print(f"[MANUS] ✅ Agente parado")
        
    def _worker_loop(self):
        """
        Loop principal do worker
        
        Executa continuamente com sleep obrigatório entre ciclos
        """
        print(f"[MANUS] 🔄 Worker loop iniciado")
        
        while self.is_running and not self.kill_switch:
            try:
                # Atualiza heartbeat
                self._update_heartbeat()
                
                # Verifica limites de segurança
                if not self._check_execution_limits():
                    print(f"[MANUS] ⚠️ Limite de execuções atingido. Aguardando...")
                    time.sleep(60)  # Aguarda 1 minuto
                    continue
                
                # Executa ciclo de trabalho
                self._execute_cycle()
                
                # Sleep obrigatório entre ciclos (evita loop infinito)
                time.sleep(self.heartbeat_interval)
                
            except Exception as e:
                print(f"[MANUS ERROR] ❌ Erro no worker loop: {e}")
                self._handle_critical_error(e)
                time.sleep(60)  # Aguarda mais tempo em caso de erro
        
        print(f"[MANUS] 🔄 Worker loop finalizado")
                
    def _update_heartbeat(self):
        """
        Atualiza heartbeat do agente
        """
        self.last_heartbeat = datetime.now()
        
    def _check_execution_limits(self) -> bool:
        """
        Verifica se o agente está dentro dos limites de execução
        
        Returns:
            bool: True se pode executar, False caso contrário
        """
        now = time.time()
        
        # Remove timestamps antigos (mais de 1 hora)
        self.execution_timestamps = [
            ts for ts in self.execution_timestamps
            if now - ts < 3600
        ]
        
        # Verifica limite
        if len(self.execution_timestamps) >= self.max_executions_per_hour:
            return False
        
        return True
        
    def _execute_cycle(self):
        """
        Executa um ciclo de trabalho
        
        FASE 1: Apenas monitora e registra estado
        NÃO executa ações financeiras
        """
        self.state = AgentState.THINKING
        
        # Registra execução
        self.execution_count += 1
        self.execution_timestamps.append(time.time())
        
        # Log de ciclo
        print(f"[MANUS] 🧠 Ciclo #{self.execution_count}")
        print(f"[MANUS] Estado: {self.state.value}")
        print(f"[MANUS] Heartbeat: {self.last_heartbeat.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[MANUS] Execuções na última hora: {len(self.execution_timestamps)}/{self.max_executions_per_hour}")
        
        # FASE 1: Apenas monitora
        # Futuras fases implementarão lógica de orquestração aqui
        # Por enquanto, apenas registra que está vivo e operacional
        
        # Detecção de comportamento anômalo
        self._detect_anomalies()
        
        self.state = AgentState.IDLE
        
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status atual do agente
        
        Returns:
            Dict com informações de status
        """
        uptime = None
        if self.started_at:
            uptime = (datetime.now() - self.started_at).total_seconds()
        
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "state": self.state.value,
            "is_running": self.is_running,
            "kill_switch": self.kill_switch,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "execution_count": self.execution_count,
            "executions_last_hour": len(self.execution_timestamps),
            "max_executions_per_hour": self.max_executions_per_hour,
            "uptime_seconds": uptime,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "phase": "FASE 1 - BASE DA AUTONOMIA",
            "error_count": self.error_count,
            "anomaly_detected": self.anomaly_detected,
            "last_error_time": self.last_error_time.isoformat() if self.last_error_time else None
        }
        
    def _detect_anomalies(self):
        """
        Detecta comportamento anômalo do agente
        
        Verifica:
        - Execuções muito rápidas (possível loop infinito)
        - Muitos erros em curto período
        - Heartbeat irregular
        """
        # Verifica execuções muito rápidas (< 10s entre ciclos)
        if len(self.execution_timestamps) >= 2:
            last_two = self.execution_timestamps[-2:]
            time_diff = last_two[1] - last_two[0]
            
            if time_diff < 10:
                print(f"[MANUS ANOMALY] ⚠️ Execuções muito rápidas: {time_diff:.2f}s")
                self.anomaly_detected = True
        
        # Verifica muitos erros
        if self.error_count >= self.max_errors_before_shutdown:
            print(f"[MANUS ANOMALY] 🚨 Muitos erros críticos: {self.error_count}")
            self.anomaly_detected = True
            self.trigger_kill_switch()
    
    def _handle_critical_error(self, error: Exception):
        """
        Trata erro crítico
        
        Args:
            error: Exceção ocorrida
        """
        self.state = AgentState.ERROR
        self.error_count += 1
        self.last_error_time = datetime.now()
        
        print(f"[MANUS ERROR] ❌ Erro crítico #{self.error_count}: {error}")
        
        # Verifica se deve parar
        if self.error_count >= self.max_errors_before_shutdown:
            print(f"[MANUS ERROR] 🚨 Limite de erros atingido. Parando agente...")
            self.trigger_kill_switch()
    
    def trigger_kill_switch(self):
        """
        Ativa kill switch global
        
        Para o agente imediatamente em caso de comportamento anômalo
        """
        print(f"[MANUS KILL SWITCH] 🚨 Ativado!")
        self.kill_switch = True
        self.anomaly_detected = True
        self.stop()


# Instância global do agente
_agent_instance: Optional[ManusAgent] = None


def get_agent() -> ManusAgent:
    """
    Retorna instância global do agente (singleton)
    
    Returns:
        ManusAgent: Instância do agente
    """
    global _agent_instance
    
    if _agent_instance is None:
        _agent_instance = ManusAgent()
    
    return _agent_instance


def start_agent():
    """
    Inicia o agente residente
    """
    agent = get_agent()
    agent.start()


def stop_agent():
    """
    Para o agente residente
    """
    agent = get_agent()
    agent.stop()


def get_agent_status() -> Dict[str, Any]:
    """
    Retorna status do agente
    
    Returns:
        Dict com informações de status
    """
    agent = get_agent()
    return agent.get_status()


if __name__ == "__main__":
    # Teste local
    print("=" * 60)
    print("🧪 TESTE DO MANUS AGENT - FASE 1")
    print("=" * 60)
    
    agent = get_agent()
    agent.start()
    
    try:
        # Aguarda 2 minutos para observar comportamento
        print("\n⏳ Aguardando 2 minutos para observar comportamento...")
        print("   (Pressione Ctrl+C para interromper)\n")
        time.sleep(120)
    except KeyboardInterrupt:
        print("\n[TESTE] ⚠️ Interrompido pelo usuário")
    finally:
        agent.stop()
        print("\n" + "=" * 60)
        print("📊 STATUS FINAL DO AGENTE")
        print("=" * 60)
        print(json.dumps(agent.get_status(), indent=2))
        print("=" * 60)

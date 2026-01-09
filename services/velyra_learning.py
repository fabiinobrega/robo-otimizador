"""
🎓 VELYRA LEARNING - Sistema de Aprendizado Manus → Velyra Prime
Nexora Prime — FASE 1

Manus IA ensina a Velyra Prime através de:
- Documentação de decisões
- Extração de padrões
- Transferência de conhecimento estratégico
- Supervisão contínua

Fluxo:
1. Manus toma decisão estratégica
2. Manus documenta raciocínio completo
3. Velyra aprende o padrão
4. Velyra executa operacionalmente
5. Manus supervisiona e corrige

Objetivo:
- Velyra aprende a executar tarefas operacionais sozinha
- Manus permanece como supervisor estratégico
- Sistema evolui continuamente

Autor: Manus AI - FASE 1
Data: 08 de Janeiro de 2026
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from enum import Enum


class DecisionType(Enum):
    """Tipos de decisão"""
    STRATEGIC = "STRATEGIC"  # Decisão estratégica (Manus)
    OPERATIONAL = "OPERATIONAL"  # Decisão operacional (Velyra)
    CORRECTIVE = "CORRECTIVE"  # Correção (Manus supervisionando Velyra)


class LearningPattern:
    """Padrão de aprendizado"""
    
    def __init__(
        self,
        pattern_id: str,
        pattern_type: str,
        context: Dict[str, Any],
        decision: str,
        reasoning: str,
        outcome: Optional[str] = None,
        confidence: float = 0.0
    ):
        self.pattern_id = pattern_id
        self.pattern_type = pattern_type
        self.context = context
        self.decision = decision
        self.reasoning = reasoning
        self.outcome = outcome
        self.confidence = confidence
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "context": self.context,
            "decision": self.decision,
            "reasoning": self.reasoning,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat()
        }


class VelyraLearning:
    """
    Sistema de Aprendizado da Velyra Prime
    
    Aprende com as decisões do Manus IA e evolui continuamente.
    """
    
    def __init__(self, db_path: str = "/home/ubuntu/robo-otimizador/data/velyra_learning.db"):
        self.db_path = db_path
        self._ensure_db_exists()
        self._init_database()
        
        print(f"[VELYRA LEARNING] ✅ Sistema de aprendizado inicializado")
    
    def _ensure_db_exists(self):
        """Garante que o diretório do banco existe"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """Inicializa o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de padrões aprendidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT UNIQUE NOT NULL,
                pattern_type TEXT NOT NULL,
                context TEXT NOT NULL,
                decision TEXT NOT NULL,
                reasoning TEXT NOT NULL,
                outcome TEXT,
                confidence REAL NOT NULL,
                times_used INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Tabela de decisões do Manus (para aprendizado)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS manus_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                decision_id TEXT UNIQUE NOT NULL,
                decision_type TEXT NOT NULL,
                context TEXT NOT NULL,
                decision TEXT NOT NULL,
                reasoning TEXT NOT NULL,
                confidence REAL NOT NULL,
                outcome TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Tabela de execuções da Velyra (para supervisão)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS velyra_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_id TEXT UNIQUE NOT NULL,
                pattern_id TEXT,
                context TEXT NOT NULL,
                action TEXT NOT NULL,
                result TEXT,
                success BOOLEAN,
                manus_feedback TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (pattern_id) REFERENCES learned_patterns(pattern_id)
            )
        """)
        
        # Índices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_pattern_type 
            ON learned_patterns(pattern_type)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_decision_type 
            ON manus_decisions(decision_type)
        """)
        
        conn.commit()
        conn.close()
    
    def record_manus_decision(
        self,
        decision_id: str,
        decision_type: DecisionType,
        context: Dict[str, Any],
        decision: str,
        reasoning: str,
        confidence: float
    ):
        """
        Registra decisão do Manus para aprendizado
        
        Args:
            decision_id: ID único da decisão
            decision_type: Tipo da decisão
            context: Contexto da decisão
            decision: Decisão tomada
            reasoning: Raciocínio completo
            confidence: Confiança (0.0 a 1.0)
        """
        print(f"[VELYRA LEARNING] 📝 Registrando decisão do Manus: {decision_id}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO manus_decisions (
                    decision_id, decision_type, context, decision, reasoning,
                    confidence, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                decision_id,
                decision_type.value,
                json.dumps(context),
                decision,
                reasoning,
                confidence,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            # Extrai padrão da decisão
            self._extract_pattern_from_decision(
                decision_id, decision_type, context, decision, reasoning, confidence
            )
            
        except Exception as e:
            print(f"[VELYRA LEARNING ERROR] ❌ Erro ao registrar decisão: {e}")
    
    def _extract_pattern_from_decision(
        self,
        decision_id: str,
        decision_type: DecisionType,
        context: Dict[str, Any],
        decision: str,
        reasoning: str,
        confidence: float
    ):
        """
        Extrai padrão de uma decisão do Manus
        
        Args:
            decision_id: ID da decisão
            decision_type: Tipo da decisão
            context: Contexto
            decision: Decisão tomada
            reasoning: Raciocínio
            confidence: Confiança
        """
        # Gera ID do padrão baseado no contexto
        pattern_type = self._identify_pattern_type(context, decision)
        pattern_id = f"{pattern_type}_{hash(json.dumps(context, sort_keys=True)) % 10000}"
        
        print(f"[VELYRA LEARNING] 🔍 Extraindo padrão: {pattern_id}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verifica se padrão já existe
            cursor.execute("""
                SELECT id, times_used, success_rate FROM learned_patterns
                WHERE pattern_id = ?
            """, (pattern_id,))
            
            existing = cursor.fetchone()
            
            if existing:
                # Atualiza padrão existente
                times_used = existing[1] + 1
                
                cursor.execute("""
                    UPDATE learned_patterns
                    SET times_used = ?, confidence = ?, updated_at = ?
                    WHERE pattern_id = ?
                """, (
                    times_used,
                    confidence,
                    datetime.now().isoformat(),
                    pattern_id
                ))
                
                print(f"[VELYRA LEARNING] ♻️ Padrão atualizado (usado {times_used}x)")
            else:
                # Cria novo padrão
                cursor.execute("""
                    INSERT INTO learned_patterns (
                        pattern_id, pattern_type, context, decision, reasoning,
                        confidence, times_used, success_rate, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pattern_id,
                    pattern_type,
                    json.dumps(context),
                    decision,
                    reasoning,
                    confidence,
                    1,
                    0.0,
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                
                print(f"[VELYRA LEARNING] ✨ Novo padrão aprendido!")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"[VELYRA LEARNING ERROR] ❌ Erro ao extrair padrão: {e}")
    
    def _identify_pattern_type(self, context: Dict[str, Any], decision: str) -> str:
        """
        Identifica o tipo de padrão baseado no contexto e decisão
        
        Args:
            context: Contexto da decisão
            decision: Decisão tomada
            
        Returns:
            str: Tipo do padrão
        """
        # Lógica simples de identificação
        # TODO: Implementar lógica mais sofisticada com ML
        
        if "budget" in decision.lower():
            return "budget_optimization"
        elif "audience" in decision.lower() or "público" in decision.lower():
            return "audience_targeting"
        elif "creative" in decision.lower() or "anúncio" in decision.lower():
            return "creative_optimization"
        elif "bid" in decision.lower() or "lance" in decision.lower():
            return "bid_strategy"
        else:
            return "general_optimization"
    
    def find_similar_pattern(self, context: Dict[str, Any]) -> Optional[LearningPattern]:
        """
        Busca padrão similar ao contexto fornecido
        
        Args:
            context: Contexto atual
            
        Returns:
            LearningPattern se encontrado, None caso contrário
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Busca padrões com contexto similar
            # TODO: Implementar busca por similaridade real
            cursor.execute("""
                SELECT pattern_id, pattern_type, context, decision, reasoning,
                       outcome, confidence
                FROM learned_patterns
                ORDER BY confidence DESC, times_used DESC
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return LearningPattern(
                    pattern_id=row[0],
                    pattern_type=row[1],
                    context=json.loads(row[2]),
                    decision=row[3],
                    reasoning=row[4],
                    outcome=row[5],
                    confidence=row[6]
                )
            
            return None
            
        except Exception as e:
            print(f"[VELYRA LEARNING ERROR] ❌ Erro ao buscar padrão: {e}")
            return None
    
    def record_velyra_execution(
        self,
        execution_id: str,
        pattern_id: Optional[str],
        context: Dict[str, Any],
        action: str,
        result: Optional[Dict[str, Any]] = None,
        success: Optional[bool] = None
    ):
        """
        Registra execução da Velyra para supervisão
        
        Args:
            execution_id: ID da execução
            pattern_id: ID do padrão usado (se houver)
            context: Contexto da execução
            action: Ação executada
            result: Resultado da execução
            success: Se foi bem-sucedida
        """
        print(f"[VELYRA LEARNING] 📊 Registrando execução da Velyra: {execution_id}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO velyra_executions (
                    execution_id, pattern_id, context, action, result,
                    success, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                execution_id,
                pattern_id,
                json.dumps(context),
                action,
                json.dumps(result) if result else None,
                success,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            # Atualiza taxa de sucesso do padrão se aplicável
            if pattern_id and success is not None:
                self._update_pattern_success_rate(pattern_id, success)
            
        except Exception as e:
            print(f"[VELYRA LEARNING ERROR] ❌ Erro ao registrar execução: {e}")
    
    def _update_pattern_success_rate(self, pattern_id: str, success: bool):
        """
        Atualiza taxa de sucesso de um padrão
        
        Args:
            pattern_id: ID do padrão
            success: Se a execução foi bem-sucedida
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Busca execuções do padrão
            cursor.execute("""
                SELECT COUNT(*), SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END)
                FROM velyra_executions
                WHERE pattern_id = ?
            """, (pattern_id,))
            
            row = cursor.fetchone()
            total_executions = row[0]
            successful_executions = row[1] or 0
            
            if total_executions > 0:
                success_rate = successful_executions / total_executions
                
                cursor.execute("""
                    UPDATE learned_patterns
                    SET success_rate = ?, updated_at = ?
                    WHERE pattern_id = ?
                """, (
                    success_rate,
                    datetime.now().isoformat(),
                    pattern_id
                ))
                
                conn.commit()
                
                print(f"[VELYRA LEARNING] 📈 Taxa de sucesso atualizada: {success_rate:.2%}")
            
            conn.close()
            
        except Exception as e:
            print(f"[VELYRA LEARNING ERROR] ❌ Erro ao atualizar taxa de sucesso: {e}")
    
    def provide_manus_feedback(
        self,
        execution_id: str,
        feedback: str
    ):
        """
        Manus fornece feedback sobre execução da Velyra
        
        Args:
            execution_id: ID da execução
            feedback: Feedback do Manus
        """
        print(f"[VELYRA LEARNING] 💬 Manus forneceu feedback: {execution_id}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE velyra_executions
                SET manus_feedback = ?
                WHERE execution_id = ?
            """, (feedback, execution_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"[VELYRA LEARNING ERROR] ❌ Erro ao registrar feedback: {e}")
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de aprendizado
        
        Returns:
            Dict com estatísticas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de padrões aprendidos
            cursor.execute("SELECT COUNT(*) FROM learned_patterns")
            total_patterns = cursor.fetchone()[0]
            
            # Total de decisões do Manus
            cursor.execute("SELECT COUNT(*) FROM manus_decisions")
            total_manus_decisions = cursor.fetchone()[0]
            
            # Total de execuções da Velyra
            cursor.execute("SELECT COUNT(*) FROM velyra_executions")
            total_velyra_executions = cursor.fetchone()[0]
            
            # Taxa de sucesso geral
            cursor.execute("""
                SELECT AVG(success_rate) FROM learned_patterns
                WHERE times_used > 0
            """)
            avg_success_rate = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            return {
                "total_patterns": total_patterns,
                "total_manus_decisions": total_manus_decisions,
                "total_velyra_executions": total_velyra_executions,
                "average_success_rate": avg_success_rate,
                "learning_progress": min(total_patterns / 100.0, 1.0)  # Progresso até 100 padrões
            }
            
        except Exception as e:
            print(f"[VELYRA LEARNING ERROR] ❌ Erro ao obter estatísticas: {e}")
            return {}


# Instância global
_learning_instance: Optional[VelyraLearning] = None


def get_learning_system() -> VelyraLearning:
    """
    Retorna instância global do sistema de aprendizado (singleton)
    
    Returns:
        VelyraLearning: Instância do sistema
    """
    global _learning_instance
    
    if _learning_instance is None:
        _learning_instance = VelyraLearning()
    
    return _learning_instance

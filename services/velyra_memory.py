"""
VELYRA MEMORY - Memória Evolutiva e Aprendizado Longitudinal
Sistema de memória permanente que aprende continuamente com cada campanha
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict
import sqlite3

class VelyraMemory:
    """Sistema de memória evolutiva da IA Velyra."""
    
    def __init__(self, db_path: str = "velyra_memory.db"):
        self.name = "Velyra Memory"
        self.version = "2.0.0"
        self.db_path = db_path
        
        # Memória em cache para acesso rápido
        self.memory_cache = {
            "accounts": defaultdict(dict),
            "niches": defaultdict(dict),
            "countries": defaultdict(dict),
            "products": defaultdict(dict),
            "platforms": defaultdict(dict),
            "strategies": defaultdict(list),
            "patterns": defaultdict(list)
        }
        
        # Pesos de aprendizado
        self.learning_weights = {
            "winner_campaign": 1.5,
            "loser_campaign": 0.8,
            "scaled_campaign": 2.0,
            "failed_scale": 0.5,
            "high_roas": 1.8,
            "low_roas": 0.6
        }
        
        # Inicializar banco de dados
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados de memória."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de campanhas históricas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns_history (
                id TEXT PRIMARY KEY,
                account_id TEXT,
                niche TEXT,
                country TEXT,
                product_type TEXT,
                platform TEXT,
                strategy TEXT,
                budget REAL,
                spend REAL,
                revenue REAL,
                roas REAL,
                cpa REAL,
                conversions INTEGER,
                status TEXT,
                success_score REAL,
                created_at TEXT,
                ended_at TEXT,
                learnings TEXT
            )
        """)
        
        # Tabela de estratégias vencedoras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS winning_strategies (
                id TEXT PRIMARY KEY,
                niche TEXT,
                country TEXT,
                platform TEXT,
                strategy_type TEXT,
                strategy_details TEXT,
                success_rate REAL,
                avg_roas REAL,
                times_used INTEGER,
                times_succeeded INTEGER,
                created_at TEXT,
                last_used TEXT
            )
        """)
        
        # Tabela de padrões aprendidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id TEXT PRIMARY KEY,
                pattern_type TEXT,
                pattern_key TEXT,
                pattern_value TEXT,
                confidence REAL,
                occurrences INTEGER,
                last_seen TEXT,
                context TEXT
            )
        """)
        
        # Tabela de erros históricos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historical_errors (
                id TEXT PRIMARY KEY,
                error_type TEXT,
                context TEXT,
                cause TEXT,
                solution TEXT,
                prevention TEXT,
                occurrences INTEGER,
                last_occurred TEXT
            )
        """)
        
        # Tabela de insights por nicho
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS niche_insights (
                id TEXT PRIMARY KEY,
                niche TEXT,
                insight_type TEXT,
                insight_value TEXT,
                confidence REAL,
                data_points INTEGER,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def learn_from_campaign(self, campaign_data: Dict) -> Dict[str, Any]:
        """Aprende com os resultados de uma campanha."""
        
        campaign_id = campaign_data.get("id", f"camp_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        # Extrair dados relevantes
        account_id = campaign_data.get("account_id", "default")
        niche = campaign_data.get("niche", "geral")
        country = campaign_data.get("country", "BR")
        product_type = campaign_data.get("product_type", "digital")
        platform = campaign_data.get("platform", "facebook")
        strategy = campaign_data.get("strategy", {})
        
        # Métricas
        spend = campaign_data.get("spend", 0)
        revenue = campaign_data.get("revenue", 0)
        conversions = campaign_data.get("conversions", 0)
        roas = revenue / spend if spend > 0 else 0
        cpa = spend / conversions if conversions > 0 else 0
        
        # Calcular score de sucesso
        success_score = self._calculate_success_score(campaign_data)
        
        # Determinar status
        status = "winner" if success_score >= 70 else "average" if success_score >= 50 else "loser"
        
        # Extrair aprendizados
        learnings = self._extract_learnings(campaign_data, status)
        
        # Salvar no banco
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO campaigns_history 
            (id, account_id, niche, country, product_type, platform, strategy, 
             budget, spend, revenue, roas, cpa, conversions, status, success_score,
             created_at, ended_at, learnings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            campaign_id, account_id, niche, country, product_type, platform,
            json.dumps(strategy), campaign_data.get("budget", 0), spend, revenue,
            roas, cpa, conversions, status, success_score,
            campaign_data.get("created_at", datetime.now().isoformat()),
            datetime.now().isoformat(), json.dumps(learnings)
        ))
        
        conn.commit()
        conn.close()
        
        # Atualizar cache
        self._update_memory_cache(campaign_data, learnings, status)
        
        # Atualizar estratégias vencedoras se aplicável
        if status == "winner":
            self._record_winning_strategy(campaign_data, strategy)
        
        # Registrar padrões
        self._record_patterns(campaign_data, status)
        
        return {
            "campaign_id": campaign_id,
            "status": status,
            "success_score": success_score,
            "learnings": learnings,
            "memory_updated": True,
            "patterns_recorded": len(learnings.get("patterns", [])),
            "insights_generated": len(learnings.get("insights", []))
        }
    
    def get_recommendations(
        self,
        niche: str,
        country: str = "BR",
        platform: str = "facebook",
        budget: float = 1000
    ) -> Dict[str, Any]:
        """Obtém recomendações baseadas na memória acumulada."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar estratégias vencedoras para o contexto
        cursor.execute("""
            SELECT strategy_type, strategy_details, success_rate, avg_roas, times_succeeded
            FROM winning_strategies
            WHERE niche = ? AND country = ? AND platform = ?
            ORDER BY success_rate DESC, avg_roas DESC
            LIMIT 5
        """, (niche, country, platform))
        
        winning_strategies = cursor.fetchall()
        
        # Buscar padrões relevantes
        cursor.execute("""
            SELECT pattern_type, pattern_key, pattern_value, confidence
            FROM learned_patterns
            WHERE pattern_key LIKE ? OR pattern_key LIKE ?
            ORDER BY confidence DESC
            LIMIT 10
        """, (f"%{niche}%", f"%{country}%"))
        
        patterns = cursor.fetchall()
        
        # Buscar insights do nicho
        cursor.execute("""
            SELECT insight_type, insight_value, confidence
            FROM niche_insights
            WHERE niche = ?
            ORDER BY confidence DESC
            LIMIT 5
        """, (niche,))
        
        insights = cursor.fetchall()
        
        # Buscar erros a evitar
        cursor.execute("""
            SELECT error_type, cause, prevention
            FROM historical_errors
            WHERE context LIKE ? OR context LIKE ?
            ORDER BY occurrences DESC
            LIMIT 5
        """, (f"%{niche}%", f"%{platform}%"))
        
        errors_to_avoid = cursor.fetchall()
        
        conn.close()
        
        # Formatar recomendações
        recommendations = {
            "timestamp": datetime.now().isoformat(),
            "context": {
                "niche": niche,
                "country": country,
                "platform": platform,
                "budget": budget
            },
            "recommended_strategies": [
                {
                    "type": s[0],
                    "details": json.loads(s[1]) if s[1] else {},
                    "success_rate": s[2],
                    "avg_roas": s[3],
                    "proven_times": s[4]
                }
                for s in winning_strategies
            ],
            "patterns_to_follow": [
                {
                    "type": p[0],
                    "key": p[1],
                    "value": p[2],
                    "confidence": p[3]
                }
                for p in patterns
            ],
            "niche_insights": [
                {
                    "type": i[0],
                    "value": i[1],
                    "confidence": i[2]
                }
                for i in insights
            ],
            "errors_to_avoid": [
                {
                    "type": e[0],
                    "cause": e[1],
                    "prevention": e[2]
                }
                for e in errors_to_avoid
            ],
            "budget_recommendation": self._get_budget_recommendation(niche, country, budget),
            "confidence_level": self._calculate_recommendation_confidence(
                len(winning_strategies), len(patterns), len(insights)
            )
        }
        
        return recommendations
    
    def get_niche_intelligence(self, niche: str) -> Dict[str, Any]:
        """Obtém inteligência acumulada sobre um nicho específico."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Estatísticas gerais do nicho
        cursor.execute("""
            SELECT 
                COUNT(*) as total_campaigns,
                AVG(roas) as avg_roas,
                AVG(cpa) as avg_cpa,
                SUM(CASE WHEN status = 'winner' THEN 1 ELSE 0 END) as winners,
                SUM(spend) as total_spend,
                SUM(revenue) as total_revenue
            FROM campaigns_history
            WHERE niche = ?
        """, (niche,))
        
        stats = cursor.fetchone()
        
        # Melhores estratégias do nicho
        cursor.execute("""
            SELECT strategy, AVG(roas) as avg_roas, COUNT(*) as uses
            FROM campaigns_history
            WHERE niche = ? AND status = 'winner'
            GROUP BY strategy
            ORDER BY avg_roas DESC
            LIMIT 5
        """, (niche,))
        
        best_strategies = cursor.fetchall()
        
        # Países com melhor performance
        cursor.execute("""
            SELECT country, AVG(roas) as avg_roas, COUNT(*) as campaigns
            FROM campaigns_history
            WHERE niche = ?
            GROUP BY country
            ORDER BY avg_roas DESC
            LIMIT 5
        """, (niche,))
        
        best_countries = cursor.fetchall()
        
        conn.close()
        
        return {
            "niche": niche,
            "timestamp": datetime.now().isoformat(),
            "statistics": {
                "total_campaigns": stats[0] if stats else 0,
                "avg_roas": round(stats[1], 2) if stats and stats[1] else 0,
                "avg_cpa": round(stats[2], 2) if stats and stats[2] else 0,
                "winner_rate": round((stats[3] / stats[0] * 100), 1) if stats and stats[0] > 0 else 0,
                "total_spend": round(stats[4], 2) if stats and stats[4] else 0,
                "total_revenue": round(stats[5], 2) if stats and stats[5] else 0
            },
            "best_strategies": [
                {
                    "strategy": json.loads(s[0]) if s[0] else {},
                    "avg_roas": round(s[1], 2),
                    "times_used": s[2]
                }
                for s in best_strategies
            ],
            "best_countries": [
                {
                    "country": c[0],
                    "avg_roas": round(c[1], 2),
                    "campaigns": c[2]
                }
                for c in best_countries
            ],
            "data_quality": "high" if stats and stats[0] >= 50 else "medium" if stats and stats[0] >= 10 else "low"
        }
    
    def get_account_history(self, account_id: str) -> Dict[str, Any]:
        """Obtém histórico completo de uma conta."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_campaigns,
                AVG(roas) as avg_roas,
                SUM(spend) as total_spend,
                SUM(revenue) as total_revenue,
                SUM(conversions) as total_conversions,
                SUM(CASE WHEN status = 'winner' THEN 1 ELSE 0 END) as winners
            FROM campaigns_history
            WHERE account_id = ?
        """, (account_id,))
        
        stats = cursor.fetchone()
        
        cursor.execute("""
            SELECT id, niche, roas, status, created_at
            FROM campaigns_history
            WHERE account_id = ?
            ORDER BY created_at DESC
            LIMIT 20
        """, (account_id,))
        
        recent_campaigns = cursor.fetchall()
        
        conn.close()
        
        return {
            "account_id": account_id,
            "statistics": {
                "total_campaigns": stats[0] if stats else 0,
                "avg_roas": round(stats[1], 2) if stats and stats[1] else 0,
                "total_spend": round(stats[2], 2) if stats and stats[2] else 0,
                "total_revenue": round(stats[3], 2) if stats and stats[3] else 0,
                "total_conversions": stats[4] if stats else 0,
                "success_rate": round((stats[5] / stats[0] * 100), 1) if stats and stats[0] > 0 else 0
            },
            "recent_campaigns": [
                {
                    "id": c[0],
                    "niche": c[1],
                    "roas": round(c[2], 2) if c[2] else 0,
                    "status": c[3],
                    "date": c[4]
                }
                for c in recent_campaigns
            ]
        }
    
    def record_error(self, error_data: Dict) -> Dict[str, Any]:
        """Registra um erro para aprendizado futuro."""
        
        error_id = hashlib.md5(
            f"{error_data.get('type', '')}_{error_data.get('context', '')}".encode()
        ).hexdigest()[:12]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar se erro já existe
        cursor.execute("SELECT occurrences FROM historical_errors WHERE id = ?", (error_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE historical_errors
                SET occurrences = occurrences + 1, last_occurred = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), error_id))
        else:
            cursor.execute("""
                INSERT INTO historical_errors
                (id, error_type, context, cause, solution, prevention, occurrences, last_occurred)
                VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            """, (
                error_id,
                error_data.get("type", "unknown"),
                error_data.get("context", ""),
                error_data.get("cause", ""),
                error_data.get("solution", ""),
                error_data.get("prevention", ""),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        
        return {
            "error_id": error_id,
            "recorded": True,
            "is_new": existing is None
        }
    
    def get_similar_campaigns(self, campaign_params: Dict, limit: int = 5) -> List[Dict]:
        """Encontra campanhas similares no histórico."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, niche, country, platform, strategy, roas, cpa, status, learnings
            FROM campaigns_history
            WHERE niche = ? AND country = ? AND platform = ?
            ORDER BY success_score DESC
            LIMIT ?
        """, (
            campaign_params.get("niche", "geral"),
            campaign_params.get("country", "BR"),
            campaign_params.get("platform", "facebook"),
            limit
        ))
        
        similar = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": c[0],
                "niche": c[1],
                "country": c[2],
                "platform": c[3],
                "strategy": json.loads(c[4]) if c[4] else {},
                "roas": round(c[5], 2) if c[5] else 0,
                "cpa": round(c[6], 2) if c[6] else 0,
                "status": c[7],
                "learnings": json.loads(c[8]) if c[8] else {}
            }
            for c in similar
        ]
    
    def _calculate_success_score(self, campaign_data: Dict) -> float:
        """Calcula score de sucesso da campanha."""
        score = 50  # Base
        
        roas = campaign_data.get("roas", 0)
        if roas >= 3:
            score += 30
        elif roas >= 2:
            score += 20
        elif roas >= 1.5:
            score += 10
        elif roas < 1:
            score -= 20
        
        # CPA vs meta
        cpa = campaign_data.get("cpa", 0)
        target_cpa = campaign_data.get("target_cpa", cpa)
        if target_cpa > 0:
            if cpa <= target_cpa * 0.8:
                score += 15
            elif cpa <= target_cpa:
                score += 10
            elif cpa > target_cpa * 1.5:
                score -= 15
        
        # Volume de conversões
        conversions = campaign_data.get("conversions", 0)
        if conversions >= 100:
            score += 10
        elif conversions >= 50:
            score += 5
        
        return min(100, max(0, score))
    
    def _extract_learnings(self, campaign_data: Dict, status: str) -> Dict:
        """Extrai aprendizados da campanha."""
        learnings = {
            "patterns": [],
            "insights": [],
            "recommendations": []
        }
        
        # Padrões de sucesso/fracasso
        if status == "winner":
            learnings["patterns"].append({
                "type": "success",
                "factor": "strategy",
                "value": campaign_data.get("strategy", {})
            })
            learnings["insights"].append(
                f"Estratégia vencedora no nicho {campaign_data.get('niche')}"
            )
        elif status == "loser":
            learnings["patterns"].append({
                "type": "failure",
                "factor": "strategy",
                "value": campaign_data.get("strategy", {})
            })
            learnings["recommendations"].append(
                "Evitar esta combinação de estratégia no futuro"
            )
        
        # Insights de performance
        roas = campaign_data.get("roas", 0)
        if roas > 0:
            learnings["insights"].append(
                f"ROAS de {roas:.2f} no país {campaign_data.get('country', 'BR')}"
            )
        
        return learnings
    
    def _update_memory_cache(self, campaign_data: Dict, learnings: Dict, status: str):
        """Atualiza cache de memória."""
        niche = campaign_data.get("niche", "geral")
        country = campaign_data.get("country", "BR")
        platform = campaign_data.get("platform", "facebook")
        
        # Atualizar estatísticas do nicho
        if niche not in self.memory_cache["niches"]:
            self.memory_cache["niches"][niche] = {
                "campaigns": 0,
                "winners": 0,
                "total_roas": 0
            }
        
        self.memory_cache["niches"][niche]["campaigns"] += 1
        if status == "winner":
            self.memory_cache["niches"][niche]["winners"] += 1
        self.memory_cache["niches"][niche]["total_roas"] += campaign_data.get("roas", 0)
    
    def _record_winning_strategy(self, campaign_data: Dict, strategy: Dict):
        """Registra estratégia vencedora."""
        strategy_id = hashlib.md5(
            json.dumps(strategy, sort_keys=True).encode()
        ).hexdigest()[:12]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO winning_strategies
            (id, niche, country, platform, strategy_type, strategy_details, 
             success_rate, avg_roas, times_used, times_succeeded, created_at, last_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 
                    COALESCE((SELECT times_used FROM winning_strategies WHERE id = ?), 0) + 1,
                    COALESCE((SELECT times_succeeded FROM winning_strategies WHERE id = ?), 0) + 1,
                    COALESCE((SELECT created_at FROM winning_strategies WHERE id = ?), ?),
                    ?)
        """, (
            strategy_id,
            campaign_data.get("niche", "geral"),
            campaign_data.get("country", "BR"),
            campaign_data.get("platform", "facebook"),
            strategy.get("type", "default"),
            json.dumps(strategy),
            100.0,  # Será recalculado
            campaign_data.get("roas", 0),
            strategy_id, strategy_id, strategy_id,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _record_patterns(self, campaign_data: Dict, status: str):
        """Registra padrões identificados."""
        patterns = []
        
        # Padrão de nicho + país
        patterns.append({
            "type": "niche_country",
            "key": f"{campaign_data.get('niche')}_{campaign_data.get('country')}",
            "value": status,
            "context": json.dumps({"roas": campaign_data.get("roas", 0)})
        })
        
        # Padrão de plataforma + estratégia
        patterns.append({
            "type": "platform_strategy",
            "key": f"{campaign_data.get('platform')}_{campaign_data.get('strategy', {}).get('type', 'default')}",
            "value": status,
            "context": json.dumps({"cpa": campaign_data.get("cpa", 0)})
        })
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for pattern in patterns:
            pattern_id = hashlib.md5(
                f"{pattern['type']}_{pattern['key']}".encode()
            ).hexdigest()[:12]
            
            cursor.execute("""
                INSERT OR REPLACE INTO learned_patterns
                (id, pattern_type, pattern_key, pattern_value, confidence, occurrences, last_seen, context)
                VALUES (?, ?, ?, ?, 
                        COALESCE((SELECT confidence FROM learned_patterns WHERE id = ?), 0.5),
                        COALESCE((SELECT occurrences FROM learned_patterns WHERE id = ?), 0) + 1,
                        ?, ?)
            """, (
                pattern_id,
                pattern["type"],
                pattern["key"],
                pattern["value"],
                pattern_id, pattern_id,
                datetime.now().isoformat(),
                pattern["context"]
            ))
        
        conn.commit()
        conn.close()
    
    def _get_budget_recommendation(self, niche: str, country: str, proposed_budget: float) -> Dict:
        """Recomenda orçamento baseado em histórico."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT AVG(budget), AVG(roas)
            FROM campaigns_history
            WHERE niche = ? AND country = ? AND status = 'winner'
        """, (niche, country))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            avg_winner_budget = result[0]
            avg_winner_roas = result[1]
            
            if proposed_budget < avg_winner_budget * 0.5:
                return {
                    "recommendation": "increase",
                    "suggested_budget": round(avg_winner_budget, 2),
                    "reason": f"Campanhas vencedoras usam em média R$ {avg_winner_budget:.2f}"
                }
            elif proposed_budget > avg_winner_budget * 2:
                return {
                    "recommendation": "decrease",
                    "suggested_budget": round(avg_winner_budget * 1.5, 2),
                    "reason": "Orçamento muito acima da média de sucesso"
                }
            else:
                return {
                    "recommendation": "maintain",
                    "suggested_budget": proposed_budget,
                    "reason": "Orçamento dentro da faixa de sucesso"
                }
        
        return {
            "recommendation": "test",
            "suggested_budget": proposed_budget,
            "reason": "Dados insuficientes - recomendado testar"
        }
    
    def _calculate_recommendation_confidence(
        self, 
        strategies_count: int, 
        patterns_count: int, 
        insights_count: int
    ) -> str:
        """Calcula nível de confiança das recomendações."""
        total_data = strategies_count + patterns_count + insights_count
        
        if total_data >= 20:
            return "high"
        elif total_data >= 10:
            return "medium"
        elif total_data >= 5:
            return "low"
        return "very_low"


# Instância global
velyra_memory = VelyraMemory()

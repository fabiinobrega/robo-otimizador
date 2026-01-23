# services/intelligent_testing_system.py
"""
NEXORA PRIME - Sistema de Testes Inteligentes
CI/CD para marketing com testes automatizados de campanhas
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import random


class IntelligentTestingSystem:
    """Sistema de testes inteligentes para campanhas de marketing."""
    
    def __init__(self):
        self.test_suites = []
        self.test_results = []
        self.test_configurations = {
            "min_sample_size": 1000,
            "confidence_level": 0.95,
            "min_test_duration_hours": 24,
            "max_test_duration_days": 14
        }
        self.active_tests = []
    
    def create_test_suite(self, name: str, campaign_id: str, test_type: str, variations: List[Dict]) -> Dict:
        """Cria uma suite de testes para uma campanha."""
        test_suite = {
            "id": f"TS_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": name,
            "campaign_id": campaign_id,
            "test_type": test_type,  # "ab_test", "multivariate", "bandit"
            "variations": variations,
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "metrics_to_track": ["ctr", "conversion_rate", "cpa", "roas"],
            "traffic_allocation": self._calculate_traffic_allocation(variations)
        }
        
        self.test_suites.append(test_suite)
        return test_suite
    
    def start_test(self, test_suite_id: str) -> Dict:
        """Inicia um teste."""
        test_suite = self._get_test_suite(test_suite_id)
        if not test_suite:
            return {"success": False, "error": "Suite de teste não encontrada"}
        
        test_suite["status"] = "running"
        test_suite["started_at"] = datetime.now().isoformat()
        
        # Inicializar métricas para cada variação
        for variation in test_suite["variations"]:
            variation["metrics"] = {
                "impressions": 0,
                "clicks": 0,
                "conversions": 0,
                "spend": 0
            }
        
        self.active_tests.append(test_suite_id)
        
        return {
            "success": True,
            "test_suite_id": test_suite_id,
            "status": "running",
            "started_at": test_suite["started_at"]
        }
    
    def update_test_metrics(self, test_suite_id: str, variation_id: str, metrics: Dict) -> Dict:
        """Atualiza métricas de uma variação do teste."""
        test_suite = self._get_test_suite(test_suite_id)
        if not test_suite:
            return {"success": False, "error": "Suite de teste não encontrada"}
        
        for variation in test_suite["variations"]:
            if variation.get("id") == variation_id:
                for key, value in metrics.items():
                    if key in variation.get("metrics", {}):
                        variation["metrics"][key] += value
                return {"success": True}
        
        return {"success": False, "error": "Variação não encontrada"}
    
    def analyze_test(self, test_suite_id: str) -> Dict:
        """Analisa os resultados de um teste."""
        test_suite = self._get_test_suite(test_suite_id)
        if not test_suite:
            return {"success": False, "error": "Suite de teste não encontrada"}
        
        analysis = {
            "test_suite_id": test_suite_id,
            "analyzed_at": datetime.now().isoformat(),
            "variations_analysis": [],
            "statistical_significance": False,
            "winner": None,
            "recommendation": ""
        }
        
        best_performance = None
        best_variation = None
        
        for variation in test_suite["variations"]:
            metrics = variation.get("metrics", {})
            
            # Calcular métricas derivadas
            impressions = metrics.get("impressions", 0)
            clicks = metrics.get("clicks", 0)
            conversions = metrics.get("conversions", 0)
            spend = metrics.get("spend", 0)
            
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
            cpa = (spend / conversions) if conversions > 0 else float('inf')
            
            variation_analysis = {
                "variation_id": variation.get("id"),
                "variation_name": variation.get("name"),
                "ctr": round(ctr, 2),
                "conversion_rate": round(conversion_rate, 2),
                "cpa": round(cpa, 2) if cpa != float('inf') else None,
                "sample_size": impressions,
                "is_significant": impressions >= self.test_configurations["min_sample_size"]
            }
            
            analysis["variations_analysis"].append(variation_analysis)
            
            # Determinar melhor variação (baseado em taxa de conversão)
            if variation_analysis["is_significant"]:
                if best_performance is None or conversion_rate > best_performance:
                    best_performance = conversion_rate
                    best_variation = variation_analysis
        
        # Verificar significância estatística
        significant_variations = [v for v in analysis["variations_analysis"] if v["is_significant"]]
        if len(significant_variations) >= 2:
            analysis["statistical_significance"] = True
            analysis["winner"] = best_variation
            analysis["recommendation"] = f"Recomendamos escalar a variação '{best_variation['variation_name']}' com taxa de conversão de {best_variation['conversion_rate']}%"
        else:
            analysis["recommendation"] = "Dados insuficientes para determinar um vencedor. Continue o teste."
        
        # Salvar resultado
        self.test_results.append(analysis)
        
        return analysis
    
    def stop_test(self, test_suite_id: str, apply_winner: bool = False) -> Dict:
        """Para um teste e opcionalmente aplica o vencedor."""
        test_suite = self._get_test_suite(test_suite_id)
        if not test_suite:
            return {"success": False, "error": "Suite de teste não encontrada"}
        
        test_suite["status"] = "completed"
        test_suite["completed_at"] = datetime.now().isoformat()
        
        if test_suite_id in self.active_tests:
            self.active_tests.remove(test_suite_id)
        
        result = {
            "success": True,
            "test_suite_id": test_suite_id,
            "status": "completed"
        }
        
        if apply_winner:
            analysis = self.analyze_test(test_suite_id)
            if analysis.get("winner"):
                result["winner_applied"] = analysis["winner"]
        
        return result
    
    def get_test_recommendations(self, campaign_id: str) -> List[Dict]:
        """Gera recomendações de testes para uma campanha."""
        recommendations = [
            {
                "type": "headline_test",
                "priority": "high",
                "description": "Testar diferentes headlines para melhorar CTR",
                "expected_impact": "+15-25% CTR"
            },
            {
                "type": "cta_test",
                "priority": "high",
                "description": "Testar diferentes CTAs para melhorar conversão",
                "expected_impact": "+10-20% Conversão"
            },
            {
                "type": "audience_test",
                "priority": "medium",
                "description": "Testar diferentes segmentos de audiência",
                "expected_impact": "+20-40% ROAS"
            },
            {
                "type": "creative_format_test",
                "priority": "medium",
                "description": "Testar imagem vs vídeo vs carrossel",
                "expected_impact": "+25-50% Engajamento"
            },
            {
                "type": "bid_strategy_test",
                "priority": "low",
                "description": "Testar diferentes estratégias de lance",
                "expected_impact": "-10-30% CPA"
            }
        ]
        
        return recommendations
    
    def get_active_tests(self) -> List[Dict]:
        """Retorna todos os testes ativos."""
        return [
            self._get_test_suite(test_id) 
            for test_id in self.active_tests 
            if self._get_test_suite(test_id)
        ]
    
    def get_test_history(self, campaign_id: Optional[str] = None) -> List[Dict]:
        """Retorna histórico de testes."""
        if campaign_id:
            return [ts for ts in self.test_suites if ts["campaign_id"] == campaign_id]
        return self.test_suites
    
    def _get_test_suite(self, test_suite_id: str) -> Optional[Dict]:
        """Busca uma suite de teste pelo ID."""
        for ts in self.test_suites:
            if ts["id"] == test_suite_id:
                return ts
        return None
    
    def _calculate_traffic_allocation(self, variations: List[Dict]) -> Dict:
        """Calcula a alocação de tráfego entre variações."""
        num_variations = len(variations)
        equal_split = 100 / num_variations
        
        allocation = {}
        for i, variation in enumerate(variations):
            var_id = variation.get("id", f"var_{i}")
            allocation[var_id] = round(equal_split, 1)
        
        return allocation
    
    def create_ab_test(self, name: str, variants: List[Dict], metric: str, traffic_split: int = 50) -> Dict:
        """Cria um teste A/B simples."""
        test_id = f"AB_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        test = {
            "test_id": test_id,
            "name": name,
            "type": "ab_test",
            "variants": variants,
            "primary_metric": metric,
            "traffic_split": traffic_split,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
        
        self.test_suites.append(test)
        return test
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de testes."""
        return {
            "total_test_suites": len(self.test_suites),
            "active_tests": len(self.active_tests),
            "completed_tests": len([ts for ts in self.test_suites if ts["status"] == "completed"]),
            "test_configurations": self.test_configurations
        }


# Instância global
intelligent_testing = IntelligentTestingSystem()

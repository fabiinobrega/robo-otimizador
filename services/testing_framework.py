"""
TESTING FRAMEWORK - Framework de Testes Automatizados
Sistema de testes A/B, multivariados e experimentos controlados
Nexora Prime V2 - Expansao Unicornio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random
import math

class TestingFramework:
    """Framework de testes automatizados."""
    
    def __init__(self):
        self.name = "Testing Framework"
        self.version = "2.0.0"
        
        # Testes ativos
        self.active_tests = {}
        
        # Historico de testes
        self.test_history = []
        
        # Configuracoes padrao
        self.default_config = {
            "min_sample_size": 100,
            "confidence_level": 0.95,
            "min_duration_days": 7,
            "max_duration_days": 30
        }
        
        # Tipos de teste suportados
        self.test_types = {
            "ab": {"name": "Teste A/B", "variants": 2},
            "abc": {"name": "Teste A/B/C", "variants": 3},
            "multivariate": {"name": "Multivariado", "variants": "unlimited"},
            "split": {"name": "Split Test", "variants": 2},
            "sequential": {"name": "Teste Sequencial", "variants": 2}
        }
    
    def create_test(self, test_config: Dict) -> Dict[str, Any]:
        """Cria um novo teste."""
        
        test_id = f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        test = {
            "id": test_id,
            "name": test_config.get("name", f"Teste {test_id}"),
            "type": test_config.get("type", "ab"),
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "hypothesis": test_config.get("hypothesis", ""),
            "metric_primary": test_config.get("metric_primary", "conversion_rate"),
            "metrics_secondary": test_config.get("metrics_secondary", ["ctr", "cpc"]),
            "variants": [],
            "traffic_allocation": {},
            "results": {},
            "config": {
                "min_sample_size": test_config.get("min_sample_size", self.default_config["min_sample_size"]),
                "confidence_level": test_config.get("confidence_level", self.default_config["confidence_level"]),
                "duration_days": test_config.get("duration_days", 14)
            }
        }
        
        # Configurar variantes
        variants = test_config.get("variants", [])
        if not variants:
            variants = [
                {"name": "Controle", "is_control": True},
                {"name": "Variante A", "is_control": False}
            ]
        
        for i, variant in enumerate(variants):
            test["variants"].append({
                "id": f"v{i}",
                "name": variant.get("name", f"Variante {i}"),
                "is_control": variant.get("is_control", i == 0),
                "config": variant.get("config", {}),
                "metrics": {}
            })
        
        # Alocacao de trafego
        num_variants = len(test["variants"])
        for variant in test["variants"]:
            test["traffic_allocation"][variant["id"]] = round(100 / num_variants, 1)
        
        self.active_tests[test_id] = test
        
        return {
            "status": "created",
            "test_id": test_id,
            "test": test
        }
    
    def start_test(self, test_id: str) -> Dict[str, Any]:
        """Inicia um teste."""
        
        if test_id not in self.active_tests:
            return {"error": "Teste nao encontrado"}
        
        test = self.active_tests[test_id]
        
        if test["status"] != "draft":
            return {"error": f"Teste ja esta em status {test['status']}"}
        
        test["status"] = "running"
        test["started_at"] = datetime.now().isoformat()
        test["expected_end"] = (datetime.now() + timedelta(days=test["config"]["duration_days"])).isoformat()
        
        return {
            "status": "started",
            "test_id": test_id,
            "started_at": test["started_at"],
            "expected_end": test["expected_end"]
        }
    
    def record_data(self, test_id: str, variant_id: str, data: Dict) -> Dict[str, Any]:
        """Registra dados de um teste."""
        
        if test_id not in self.active_tests:
            return {"error": "Teste nao encontrado"}
        
        test = self.active_tests[test_id]
        
        variant = next((v for v in test["variants"] if v["id"] == variant_id), None)
        if not variant:
            return {"error": "Variante nao encontrada"}
        
        # Atualizar metricas
        for metric, value in data.items():
            if metric not in variant["metrics"]:
                variant["metrics"][metric] = {"values": [], "sum": 0, "count": 0}
            
            variant["metrics"][metric]["values"].append(value)
            variant["metrics"][metric]["sum"] += value
            variant["metrics"][metric]["count"] += 1
        
        return {
            "status": "recorded",
            "test_id": test_id,
            "variant_id": variant_id,
            "data_points": len(data)
        }
    
    def analyze_test(self, test_id: str) -> Dict[str, Any]:
        """Analisa resultados de um teste."""
        
        if test_id not in self.active_tests:
            return {"error": "Teste nao encontrado"}
        
        test = self.active_tests[test_id]
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "test_id": test_id,
            "test_name": test["name"],
            "status": test["status"],
            "variants_analysis": {},
            "statistical_significance": False,
            "winner": None,
            "confidence": 0,
            "recommendations": []
        }
        
        # Encontrar controle
        control = next((v for v in test["variants"] if v["is_control"]), test["variants"][0])
        
        # Analisar cada variante
        for variant in test["variants"]:
            variant_analysis = self._analyze_variant(variant, test["metric_primary"])
            analysis["variants_analysis"][variant["id"]] = variant_analysis
        
        # Calcular significancia estatistica
        if len(test["variants"]) >= 2:
            control_data = analysis["variants_analysis"].get(control["id"], {})
            
            for variant in test["variants"]:
                if variant["id"] != control["id"]:
                    variant_data = analysis["variants_analysis"].get(variant["id"], {})
                    
                    significance = self._calculate_significance(
                        control_data.get("conversion_rate", 0),
                        control_data.get("sample_size", 0),
                        variant_data.get("conversion_rate", 0),
                        variant_data.get("sample_size", 0)
                    )
                    
                    analysis["variants_analysis"][variant["id"]]["vs_control"] = significance
                    
                    if significance["is_significant"] and significance["lift"] > 0:
                        if not analysis["winner"] or significance["lift"] > analysis["confidence"]:
                            analysis["winner"] = variant["id"]
                            analysis["confidence"] = significance["confidence"]
                            analysis["statistical_significance"] = True
        
        # Gerar recomendacoes
        analysis["recommendations"] = self._generate_test_recommendations(analysis)
        
        # Salvar resultados
        test["results"] = analysis
        
        return analysis
    
    def get_test_status(self, test_id: str) -> Dict[str, Any]:
        """Obtem status de um teste."""
        
        if test_id not in self.active_tests:
            return {"error": "Teste nao encontrado"}
        
        test = self.active_tests[test_id]
        
        # Calcular progresso
        progress = 0
        if test["status"] == "running" and "started_at" in test:
            started = datetime.fromisoformat(test["started_at"])
            expected_end = datetime.fromisoformat(test["expected_end"])
            total_duration = (expected_end - started).total_seconds()
            elapsed = (datetime.now() - started).total_seconds()
            progress = min(100, (elapsed / total_duration) * 100)
        
        # Calcular amostras coletadas
        total_samples = 0
        for variant in test["variants"]:
            primary_metric = test["metric_primary"]
            if primary_metric in variant["metrics"]:
                total_samples += variant["metrics"][primary_metric]["count"]
        
        return {
            "test_id": test_id,
            "name": test["name"],
            "status": test["status"],
            "progress": round(progress, 1),
            "total_samples": total_samples,
            "min_samples_needed": test["config"]["min_sample_size"] * len(test["variants"]),
            "variants_count": len(test["variants"]),
            "started_at": test.get("started_at"),
            "expected_end": test.get("expected_end")
        }
    
    def stop_test(self, test_id: str, reason: str = "manual") -> Dict[str, Any]:
        """Para um teste."""
        
        if test_id not in self.active_tests:
            return {"error": "Teste nao encontrado"}
        
        test = self.active_tests[test_id]
        test["status"] = "stopped"
        test["stopped_at"] = datetime.now().isoformat()
        test["stop_reason"] = reason
        
        # Mover para historico
        self.test_history.append(test)
        
        return {
            "status": "stopped",
            "test_id": test_id,
            "stopped_at": test["stopped_at"],
            "reason": reason
        }
    
    def declare_winner(self, test_id: str, winner_variant_id: str) -> Dict[str, Any]:
        """Declara vencedor de um teste."""
        
        if test_id not in self.active_tests:
            return {"error": "Teste nao encontrado"}
        
        test = self.active_tests[test_id]
        
        winner = next((v for v in test["variants"] if v["id"] == winner_variant_id), None)
        if not winner:
            return {"error": "Variante nao encontrada"}
        
        test["status"] = "completed"
        test["completed_at"] = datetime.now().isoformat()
        test["winner"] = winner_variant_id
        test["winner_name"] = winner["name"]
        
        # Mover para historico
        self.test_history.append(test)
        del self.active_tests[test_id]
        
        return {
            "status": "completed",
            "test_id": test_id,
            "winner": winner_variant_id,
            "winner_name": winner["name"],
            "completed_at": test["completed_at"]
        }
    
    def calculate_sample_size(self, config: Dict) -> Dict[str, Any]:
        """Calcula tamanho de amostra necessario."""
        
        baseline_rate = config.get("baseline_rate", 0.02)  # 2%
        minimum_effect = config.get("minimum_effect", 0.20)  # 20% lift
        confidence_level = config.get("confidence_level", 0.95)
        power = config.get("power", 0.80)
        
        # Calcular usando formula simplificada
        # n = 2 * ((z_alpha + z_beta)^2 * p * (1-p)) / (delta^2)
        
        z_alpha = 1.96 if confidence_level == 0.95 else 2.58  # 95% ou 99%
        z_beta = 0.84 if power == 0.80 else 1.28  # 80% ou 90%
        
        p = baseline_rate
        delta = baseline_rate * minimum_effect
        
        if delta == 0:
            return {"error": "Efeito minimo nao pode ser zero"}
        
        n = 2 * ((z_alpha + z_beta) ** 2 * p * (1 - p)) / (delta ** 2)
        n = math.ceil(n)
        
        return {
            "sample_size_per_variant": n,
            "total_sample_size": n * 2,
            "baseline_rate": f"{baseline_rate * 100:.1f}%",
            "minimum_detectable_effect": f"{minimum_effect * 100:.0f}%",
            "confidence_level": f"{confidence_level * 100:.0f}%",
            "statistical_power": f"{power * 100:.0f}%",
            "estimated_duration": self._estimate_test_duration(n, config.get("daily_traffic", 1000))
        }
    
    def get_test_recommendations(self, context: Dict) -> Dict[str, Any]:
        """Obtem recomendacoes de testes."""
        
        recommendations = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "recommended_tests": [],
            "priority_order": [],
            "best_practices": []
        }
        
        # Recomendacoes baseadas no contexto
        if context.get("low_ctr"):
            recommendations["recommended_tests"].append({
                "type": "ab",
                "name": "Teste de Headlines",
                "hypothesis": "Headlines mais diretas aumentarao CTR",
                "metric_primary": "ctr",
                "priority": "high"
            })
        
        if context.get("low_conversion"):
            recommendations["recommended_tests"].append({
                "type": "ab",
                "name": "Teste de CTA",
                "hypothesis": "CTAs mais urgentes aumentarao conversao",
                "metric_primary": "conversion_rate",
                "priority": "high"
            })
        
        if context.get("high_cpc"):
            recommendations["recommended_tests"].append({
                "type": "ab",
                "name": "Teste de Publico",
                "hypothesis": "Publicos mais segmentados reduzirao CPC",
                "metric_primary": "cpc",
                "priority": "medium"
            })
        
        # Testes padrao recomendados
        recommendations["recommended_tests"].extend([
            {
                "type": "ab",
                "name": "Teste de Criativo",
                "hypothesis": "Video vs Imagem - qual performa melhor",
                "metric_primary": "conversion_rate",
                "priority": "medium"
            },
            {
                "type": "multivariate",
                "name": "Teste de Landing Page",
                "hypothesis": "Combinacao otima de elementos da LP",
                "metric_primary": "conversion_rate",
                "priority": "low"
            }
        ])
        
        # Ordenar por prioridade
        priority_map = {"high": 0, "medium": 1, "low": 2}
        recommendations["recommended_tests"].sort(key=lambda x: priority_map.get(x["priority"], 3))
        
        recommendations["priority_order"] = [t["name"] for t in recommendations["recommended_tests"]]
        
        # Melhores praticas
        recommendations["best_practices"] = [
            "Teste apenas uma variavel por vez em testes A/B",
            "Aguarde significancia estatistica antes de declarar vencedor",
            "Documente hipoteses e aprendizados de cada teste",
            "Mantenha testes rodando por pelo menos 7 dias",
            "Considere sazonalidade ao analisar resultados"
        ]
        
        return recommendations
    
    def create_multivariate_test(self, config: Dict) -> Dict[str, Any]:
        """Cria teste multivariado."""
        
        test_id = f"mvt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        # Elementos a testar
        elements = config.get("elements", {})
        # Ex: {"headline": ["H1", "H2"], "cta": ["CTA1", "CTA2"], "image": ["Img1", "Img2"]}
        
        # Gerar todas as combinacoes
        combinations = self._generate_combinations(elements)
        
        test = {
            "id": test_id,
            "name": config.get("name", f"MVT {test_id}"),
            "type": "multivariate",
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "elements": elements,
            "combinations": combinations,
            "variants": [],
            "results": {}
        }
        
        # Criar variante para cada combinacao
        for i, combo in enumerate(combinations):
            test["variants"].append({
                "id": f"combo_{i}",
                "combination": combo,
                "metrics": {}
            })
        
        self.active_tests[test_id] = test
        
        return {
            "status": "created",
            "test_id": test_id,
            "total_combinations": len(combinations),
            "combinations": combinations,
            "estimated_sample_size": len(combinations) * self.default_config["min_sample_size"]
        }
    
    def get_testing_report(self, period: str = "30d") -> Dict[str, Any]:
        """Gera relatorio de testes."""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "period": period,
            "summary": {
                "active_tests": len(self.active_tests),
                "completed_tests": len(self.test_history),
                "total_tests": len(self.active_tests) + len(self.test_history)
            },
            "active_tests": [],
            "recent_results": [],
            "insights": [],
            "recommendations": []
        }
        
        # Testes ativos
        for test_id, test in self.active_tests.items():
            status = self.get_test_status(test_id)
            report["active_tests"].append(status)
        
        # Resultados recentes
        for test in self.test_history[-5:]:
            report["recent_results"].append({
                "test_id": test["id"],
                "name": test["name"],
                "winner": test.get("winner_name", "N/A"),
                "completed_at": test.get("completed_at")
            })
        
        # Insights
        if self.test_history:
            winners_with_lift = [t for t in self.test_history if t.get("results", {}).get("confidence", 0) > 0]
            if winners_with_lift:
                avg_lift = sum(t["results"]["confidence"] for t in winners_with_lift) / len(winners_with_lift)
                report["insights"].append(f"Lift medio dos testes vencedores: {avg_lift:.1f}%")
        
        # Recomendacoes
        report["recommendations"] = [
            "Mantenha pelo menos 2-3 testes ativos simultaneamente",
            "Documente todos os aprendizados para referencia futura",
            "Priorize testes de alto impacto (conversao, receita)"
        ]
        
        return report
    
    def _analyze_variant(self, variant: Dict, primary_metric: str) -> Dict[str, Any]:
        """Analisa uma variante."""
        
        analysis = {
            "variant_id": variant["id"],
            "variant_name": variant["name"],
            "is_control": variant["is_control"],
            "sample_size": 0,
            "conversion_rate": 0,
            "metrics": {}
        }
        
        if primary_metric in variant["metrics"]:
            metric_data = variant["metrics"][primary_metric]
            analysis["sample_size"] = metric_data["count"]
            analysis["conversion_rate"] = metric_data["sum"] / metric_data["count"] if metric_data["count"] > 0 else 0
        
        # Outras metricas
        for metric_name, metric_data in variant["metrics"].items():
            if metric_data["count"] > 0:
                analysis["metrics"][metric_name] = {
                    "average": round(metric_data["sum"] / metric_data["count"], 4),
                    "count": metric_data["count"]
                }
        
        return analysis
    
    def _calculate_significance(self, control_rate: float, control_n: int, 
                                variant_rate: float, variant_n: int) -> Dict[str, Any]:
        """Calcula significancia estatistica."""
        
        if control_n == 0 or variant_n == 0:
            return {"is_significant": False, "confidence": 0, "lift": 0}
        
        # Calcular lift
        lift = ((variant_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0
        
        # Calcular z-score simplificado
        pooled_rate = (control_rate * control_n + variant_rate * variant_n) / (control_n + variant_n)
        
        if pooled_rate == 0 or pooled_rate == 1:
            return {"is_significant": False, "confidence": 0, "lift": round(lift, 2)}
        
        se = math.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_n + 1/variant_n))
        
        if se == 0:
            return {"is_significant": False, "confidence": 0, "lift": round(lift, 2)}
        
        z_score = abs(variant_rate - control_rate) / se
        
        # Converter z-score para confianca (aproximacao)
        if z_score >= 2.58:
            confidence = 99
        elif z_score >= 1.96:
            confidence = 95
        elif z_score >= 1.65:
            confidence = 90
        else:
            confidence = min(90, z_score * 50)
        
        return {
            "is_significant": confidence >= 95,
            "confidence": round(confidence, 1),
            "lift": round(lift, 2),
            "z_score": round(z_score, 3)
        }
    
    def _generate_test_recommendations(self, analysis: Dict) -> List[str]:
        """Gera recomendacoes para um teste."""
        
        recommendations = []
        
        if analysis["winner"]:
            recommendations.append(f"Implemente a variante vencedora ({analysis['winner']})")
            recommendations.append("Documente os aprendizados para testes futuros")
        elif not analysis["statistical_significance"]:
            recommendations.append("Continue coletando dados ate atingir significancia")
            recommendations.append("Considere aumentar o tamanho da amostra")
        
        return recommendations
    
    def _estimate_test_duration(self, sample_size: int, daily_traffic: int) -> str:
        """Estima duracao do teste."""
        
        if daily_traffic <= 0:
            return "Indeterminado"
        
        days = math.ceil(sample_size * 2 / daily_traffic)  # *2 para ambas variantes
        
        if days < 7:
            return f"{max(7, days)} dias (minimo recomendado: 7 dias)"
        elif days > 30:
            return f"{days} dias (considere aumentar trafego)"
        else:
            return f"{days} dias"
    
    def _generate_combinations(self, elements: Dict) -> List[Dict]:
        """Gera todas as combinacoes para teste multivariado."""
        
        if not elements:
            return []
        
        keys = list(elements.keys())
        values = list(elements.values())
        
        combinations = []
        
        def generate(index, current):
            if index == len(keys):
                combinations.append(current.copy())
                return
            
            for value in values[index]:
                current[keys[index]] = value
                generate(index + 1, current)
        
        generate(0, {})
        return combinations


# Instancia global
testing_framework = TestingFramework()

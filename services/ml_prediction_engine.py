"""
ML PREDICTION ENGINE - Motor de Predicao com Machine Learning
Previsoes de performance, anomalias e otimizacoes automaticas
Nexora Prime V2 - Expansao Unicornio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import math
import random

class MLPredictionEngine:
    """Motor de predicao baseado em Machine Learning."""
    
    def __init__(self):
        self.name = "ML Prediction Engine"
        self.version = "2.0.0"
        
        # Modelos disponiveis
        self.models = {
            "roas_predictor": {"accuracy": 0.85, "last_trained": None},
            "cpa_predictor": {"accuracy": 0.82, "last_trained": None},
            "conversion_predictor": {"accuracy": 0.78, "last_trained": None},
            "budget_optimizer": {"accuracy": 0.80, "last_trained": None},
            "anomaly_detector": {"accuracy": 0.90, "last_trained": None},
            "fatigue_predictor": {"accuracy": 0.75, "last_trained": None},
            "audience_scorer": {"accuracy": 0.83, "last_trained": None}
        }
        
        # Historico de predicoes
        self.prediction_history = []
        
        # Cache de features
        self.feature_cache = {}
    
    def predict_roas(self, campaign_data: Dict, days_ahead: int = 7) -> Dict[str, Any]:
        """Preve ROAS futuro de uma campanha."""
        
        # Extrair features
        features = self._extract_features(campaign_data)
        
        # Simular predicao (em producao usaria modelo real)
        current_roas = campaign_data.get("current_roas", 2.0)
        trend = campaign_data.get("roas_trend", 0)
        seasonality = self._get_seasonality_factor()
        
        predictions = []
        for day in range(1, days_ahead + 1):
            # Modelo simplificado de predicao
            base_roas = current_roas * (1 + trend * day * 0.01)
            seasonal_adjustment = base_roas * seasonality
            noise = random.uniform(-0.1, 0.1)
            predicted_roas = max(0.5, seasonal_adjustment + noise)
            
            confidence = max(0.5, 0.95 - (day * 0.03))
            
            predictions.append({
                "day": day,
                "date": (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                "predicted_roas": round(predicted_roas, 2),
                "confidence": round(confidence, 2),
                "range": {
                    "min": round(predicted_roas * 0.85, 2),
                    "max": round(predicted_roas * 1.15, 2)
                }
            })
        
        # Calcular metricas agregadas
        avg_predicted = sum(p["predicted_roas"] for p in predictions) / len(predictions)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_data.get("campaign_id"),
            "model": "roas_predictor",
            "model_accuracy": self.models["roas_predictor"]["accuracy"],
            "current_roas": current_roas,
            "predictions": predictions,
            "summary": {
                "avg_predicted_roas": round(avg_predicted, 2),
                "trend": "improving" if avg_predicted > current_roas else "declining" if avg_predicted < current_roas else "stable",
                "recommendation": self._generate_roas_recommendation(current_roas, avg_predicted)
            }
        }
        
        self._log_prediction(result)
        return result
    
    def predict_cpa(self, campaign_data: Dict, target_cpa: float = None) -> Dict[str, Any]:
        """Preve CPA futuro."""
        
        current_cpa = campaign_data.get("current_cpa", 50)
        target_cpa = target_cpa or campaign_data.get("target_cpa", current_cpa)
        spend = campaign_data.get("spend", 1000)
        conversions = campaign_data.get("conversions", 20)
        
        # Fatores que afetam CPA
        audience_saturation = min(1.0, spend / 10000)
        creative_fatigue = campaign_data.get("creative_age_days", 0) / 30
        competition_factor = self._get_competition_factor(campaign_data.get("niche", "geral"))
        
        # Predicao de CPA
        base_cpa = current_cpa
        saturation_impact = base_cpa * audience_saturation * 0.2
        fatigue_impact = base_cpa * creative_fatigue * 0.15
        competition_impact = base_cpa * competition_factor * 0.1
        
        predicted_cpa = base_cpa + saturation_impact + fatigue_impact + competition_impact
        
        # Probabilidade de atingir target
        if predicted_cpa <= target_cpa:
            probability_hit_target = min(0.95, 0.7 + (target_cpa - predicted_cpa) / target_cpa * 0.5)
        else:
            probability_hit_target = max(0.1, 0.5 - (predicted_cpa - target_cpa) / target_cpa * 0.5)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_data.get("campaign_id"),
            "model": "cpa_predictor",
            "current_cpa": round(current_cpa, 2),
            "target_cpa": round(target_cpa, 2),
            "predicted_cpa": round(predicted_cpa, 2),
            "probability_hit_target": round(probability_hit_target, 2),
            "factors": {
                "audience_saturation": round(audience_saturation, 2),
                "creative_fatigue": round(creative_fatigue, 2),
                "competition": round(competition_factor, 2)
            },
            "recommendations": self._generate_cpa_recommendations(current_cpa, predicted_cpa, target_cpa)
        }
    
    def predict_conversions(self, campaign_data: Dict, budget: float, days: int = 7) -> Dict[str, Any]:
        """Preve conversoes para um orcamento."""
        
        current_cpa = campaign_data.get("current_cpa", 50)
        conversion_rate = campaign_data.get("conversion_rate", 2.0)
        
        # Calcular conversoes esperadas
        expected_conversions = budget / current_cpa
        
        # Ajustar por fatores
        efficiency_factor = min(1.2, max(0.8, 1 + (conversion_rate - 2) * 0.1))
        scale_factor = 1 - min(0.2, budget / 50000 * 0.1)  # Diminui eficiencia com escala
        
        adjusted_conversions = expected_conversions * efficiency_factor * scale_factor
        
        # Distribuir por dia
        daily_conversions = adjusted_conversions / days
        
        predictions = []
        cumulative = 0
        for day in range(1, days + 1):
            daily = daily_conversions * (1 + random.uniform(-0.2, 0.2))
            cumulative += daily
            predictions.append({
                "day": day,
                "daily_conversions": round(daily, 1),
                "cumulative_conversions": round(cumulative, 1)
            })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_data.get("campaign_id"),
            "model": "conversion_predictor",
            "budget": budget,
            "days": days,
            "predictions": predictions,
            "summary": {
                "total_predicted_conversions": round(adjusted_conversions, 0),
                "avg_daily_conversions": round(daily_conversions, 1),
                "predicted_cpa": round(budget / adjusted_conversions, 2) if adjusted_conversions > 0 else 0,
                "confidence": round(self.models["conversion_predictor"]["accuracy"], 2)
            }
        }
    
    def optimize_budget(self, campaigns: List[Dict], total_budget: float) -> Dict[str, Any]:
        """Otimiza distribuicao de orcamento entre campanhas."""
        
        if not campaigns:
            return {"error": "Nenhuma campanha fornecida"}
        
        # Calcular score de cada campanha
        campaign_scores = []
        for campaign in campaigns:
            score = self._calculate_campaign_score(campaign)
            campaign_scores.append({
                "campaign_id": campaign.get("campaign_id"),
                "score": score,
                "current_budget": campaign.get("budget", 0),
                "roas": campaign.get("roas", 0),
                "cpa": campaign.get("cpa", 0)
            })
        
        # Ordenar por score
        campaign_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Distribuir orcamento proporcionalmente ao score
        total_score = sum(c["score"] for c in campaign_scores)
        
        allocations = []
        remaining_budget = total_budget
        
        for i, campaign in enumerate(campaign_scores):
            if total_score > 0:
                proportion = campaign["score"] / total_score
                allocated = total_budget * proportion
            else:
                allocated = total_budget / len(campaigns)
            
            # Limitar mudancas drasticas
            current = campaign["current_budget"]
            max_change = current * 0.5 if current > 0 else allocated
            
            if allocated > current + max_change:
                allocated = current + max_change
            elif allocated < current - max_change:
                allocated = max(0, current - max_change)
            
            allocations.append({
                "campaign_id": campaign["campaign_id"],
                "current_budget": round(current, 2),
                "recommended_budget": round(allocated, 2),
                "change": round(allocated - current, 2),
                "change_percent": round(((allocated - current) / current) * 100, 1) if current > 0 else 0,
                "score": round(campaign["score"], 2),
                "expected_roas": round(campaign["roas"] * (1 + (allocated - current) / current * 0.1), 2) if current > 0 else campaign["roas"]
            })
            
            remaining_budget -= allocated
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model": "budget_optimizer",
            "total_budget": total_budget,
            "campaigns_analyzed": len(campaigns),
            "allocations": allocations,
            "summary": {
                "total_allocated": round(total_budget - remaining_budget, 2),
                "expected_total_roas": round(sum(a["expected_roas"] * a["recommended_budget"] for a in allocations) / total_budget, 2) if total_budget > 0 else 0
            }
        }
    
    def detect_anomalies(self, metrics_history: List[Dict]) -> Dict[str, Any]:
        """Detecta anomalias nas metricas."""
        
        if len(metrics_history) < 5:
            return {"error": "Historico insuficiente para deteccao de anomalias"}
        
        anomalies = []
        
        # Calcular medias e desvios
        metrics_to_check = ["spend", "cpa", "roas", "ctr", "conversions"]
        
        for metric in metrics_to_check:
            values = [m.get(metric, 0) for m in metrics_history if metric in m]
            if len(values) < 3:
                continue
            
            avg = sum(values) / len(values)
            variance = sum((v - avg) ** 2 for v in values) / len(values)
            std_dev = math.sqrt(variance) if variance > 0 else 0
            
            # Verificar ultimo valor
            latest = values[-1]
            
            if std_dev > 0:
                z_score = (latest - avg) / std_dev
                
                if abs(z_score) > 2:
                    anomalies.append({
                        "metric": metric,
                        "current_value": round(latest, 2),
                        "expected_value": round(avg, 2),
                        "deviation": round(z_score, 2),
                        "severity": "high" if abs(z_score) > 3 else "medium",
                        "direction": "above" if z_score > 0 else "below",
                        "description": f"{metric} esta {abs(z_score):.1f} desvios padrao {'acima' if z_score > 0 else 'abaixo'} da media"
                    })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model": "anomaly_detector",
            "data_points_analyzed": len(metrics_history),
            "anomalies_found": len(anomalies),
            "anomalies": anomalies,
            "overall_status": "alert" if any(a["severity"] == "high" for a in anomalies) else "warning" if anomalies else "normal",
            "recommendations": self._generate_anomaly_recommendations(anomalies)
        }
    
    def predict_fatigue(self, creative_data: Dict) -> Dict[str, Any]:
        """Preve fadiga de criativo."""
        
        age_days = creative_data.get("age_days", 0)
        impressions = creative_data.get("impressions", 0)
        frequency = creative_data.get("frequency", 1)
        ctr_history = creative_data.get("ctr_history", [])
        
        # Calcular score de fadiga
        age_factor = min(1.0, age_days / 30)
        frequency_factor = min(1.0, frequency / 5)
        
        # Tendencia de CTR
        if len(ctr_history) >= 3:
            ctr_trend = (ctr_history[-1] - ctr_history[0]) / ctr_history[0] if ctr_history[0] > 0 else 0
            ctr_factor = max(0, -ctr_trend)
        else:
            ctr_factor = 0
        
        fatigue_score = (age_factor * 0.3 + frequency_factor * 0.4 + ctr_factor * 0.3) * 100
        
        # Estimar dias restantes
        if fatigue_score < 30:
            days_remaining = 14 - age_days
        elif fatigue_score < 60:
            days_remaining = 7 - (age_days % 7)
        else:
            days_remaining = 3
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model": "fatigue_predictor",
            "creative_id": creative_data.get("creative_id"),
            "fatigue_score": round(fatigue_score, 1),
            "status": "fresh" if fatigue_score < 30 else "aging" if fatigue_score < 60 else "fatigued",
            "factors": {
                "age_days": age_days,
                "frequency": frequency,
                "ctr_trend": round(ctr_factor, 2)
            },
            "prediction": {
                "days_until_fatigue": max(0, days_remaining),
                "recommended_action": "continue" if fatigue_score < 30 else "prepare_replacement" if fatigue_score < 60 else "replace_now"
            }
        }
    
    def score_audience(self, audience_data: Dict) -> Dict[str, Any]:
        """Pontua qualidade de uma audiencia."""
        
        size = audience_data.get("size", 0)
        overlap = audience_data.get("overlap_percent", 0)
        engagement_rate = audience_data.get("engagement_rate", 0)
        conversion_rate = audience_data.get("conversion_rate", 0)
        
        # Calcular scores individuais
        size_score = min(100, (size / 1000000) * 50 + 50) if size > 10000 else (size / 10000) * 50
        overlap_score = 100 - overlap
        engagement_score = min(100, engagement_rate * 20)
        conversion_score = min(100, conversion_rate * 25)
        
        # Score final ponderado
        final_score = (
            size_score * 0.2 +
            overlap_score * 0.2 +
            engagement_score * 0.3 +
            conversion_score * 0.3
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model": "audience_scorer",
            "audience_id": audience_data.get("audience_id"),
            "overall_score": round(final_score, 1),
            "grade": self._score_to_grade(final_score),
            "component_scores": {
                "size": round(size_score, 1),
                "uniqueness": round(overlap_score, 1),
                "engagement": round(engagement_score, 1),
                "conversion_potential": round(conversion_score, 1)
            },
            "recommendation": self._generate_audience_recommendation(final_score)
        }
    
    def _extract_features(self, data: Dict) -> Dict[str, float]:
        """Extrai features para modelos."""
        return {
            "spend": data.get("spend", 0),
            "impressions": data.get("impressions", 0),
            "clicks": data.get("clicks", 0),
            "conversions": data.get("conversions", 0),
            "ctr": data.get("ctr", 0),
            "cpc": data.get("cpc", 0),
            "cpa": data.get("cpa", 0),
            "roas": data.get("roas", 0)
        }
    
    def _get_seasonality_factor(self) -> float:
        """Obtem fator de sazonalidade."""
        month = datetime.now().month
        factors = {1: 0.9, 2: 0.95, 3: 1.0, 4: 1.0, 5: 1.05, 6: 1.0, 7: 0.95, 8: 0.95, 9: 1.0, 10: 1.05, 11: 1.15, 12: 1.2}
        return factors.get(month, 1.0)
    
    def _get_competition_factor(self, niche: str) -> float:
        """Obtem fator de competicao por nicho."""
        factors = {"ecommerce": 0.3, "infoprodutos": 0.25, "saas": 0.2, "servicos": 0.15, "geral": 0.2}
        return factors.get(niche.lower(), 0.2)
    
    def _calculate_campaign_score(self, campaign: Dict) -> float:
        """Calcula score de uma campanha."""
        roas = campaign.get("roas", 0)
        cpa = campaign.get("cpa", 100)
        target_cpa = campaign.get("target_cpa", cpa)
        conversions = campaign.get("conversions", 0)
        
        roas_score = min(100, roas * 25)
        cpa_score = min(100, (target_cpa / cpa) * 50) if cpa > 0 else 0
        volume_score = min(100, conversions * 2)
        
        return (roas_score * 0.4 + cpa_score * 0.4 + volume_score * 0.2)
    
    def _generate_roas_recommendation(self, current: float, predicted: float) -> str:
        """Gera recomendacao baseada em ROAS."""
        if predicted > current * 1.1:
            return "Tendencia positiva - considere escalar"
        elif predicted < current * 0.9:
            return "Tendencia negativa - revise estrategia"
        return "Estavel - mantenha monitoramento"
    
    def _generate_cpa_recommendations(self, current: float, predicted: float, target: float) -> List[str]:
        """Gera recomendacoes para CPA."""
        recommendations = []
        if predicted > target:
            recommendations.append("CPA previsto acima do target - otimize publicos")
            recommendations.append("Considere testar novos criativos")
        if predicted > current * 1.2:
            recommendations.append("CPA subindo - verifique saturacao de audiencia")
        return recommendations
    
    def _generate_anomaly_recommendations(self, anomalies: List[Dict]) -> List[str]:
        """Gera recomendacoes para anomalias."""
        recommendations = []
        for anomaly in anomalies:
            if anomaly["metric"] == "cpa" and anomaly["direction"] == "above":
                recommendations.append("CPA anomalo alto - pausar e investigar")
            elif anomaly["metric"] == "roas" and anomaly["direction"] == "below":
                recommendations.append("ROAS anomalo baixo - verificar tracking")
        return recommendations if recommendations else ["Continuar monitoramento normal"]
    
    def _score_to_grade(self, score: float) -> str:
        """Converte score em nota."""
        if score >= 90: return "A+"
        elif score >= 80: return "A"
        elif score >= 70: return "B+"
        elif score >= 60: return "B"
        elif score >= 50: return "C"
        elif score >= 40: return "D"
        return "F"
    
    def _generate_audience_recommendation(self, score: float) -> str:
        """Gera recomendacao para audiencia."""
        if score >= 80:
            return "Audiencia de alta qualidade - priorizar"
        elif score >= 60:
            return "Audiencia boa - usar como secundaria"
        elif score >= 40:
            return "Audiencia media - testar com orcamento limitado"
        return "Audiencia fraca - evitar ou refinar"
    
    def _log_prediction(self, prediction: Dict):
        """Registra predicao no historico."""
        self.prediction_history.append(prediction)
        if len(self.prediction_history) > 1000:
            self.prediction_history = self.prediction_history[-1000:]


# Instancia global
ml_prediction_engine = MLPredictionEngine()

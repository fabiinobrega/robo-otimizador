"""
PREDICTIVE ANALYTICS ENGINE - Motor de Análise Preditiva
Sistema de Machine Learning para previsão de performance de campanhas
Versão: 1.0 - Expansão Avançada
"""

import os
import json
import math
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionType(Enum):
    """Tipos de predição disponíveis"""
    REVENUE = "revenue"
    CONVERSIONS = "conversions"
    ROAS = "roas"
    CPA = "cpa"
    CTR = "ctr"
    IMPRESSIONS = "impressions"
    CLICKS = "clicks"
    SPEND = "spend"


class TimeHorizon(Enum):
    """Horizontes de tempo para predição"""
    NEXT_HOUR = "1h"
    NEXT_DAY = "24h"
    NEXT_WEEK = "7d"
    NEXT_MONTH = "30d"
    NEXT_QUARTER = "90d"


class TrendDirection(Enum):
    """Direção da tendência"""
    STRONG_UP = "strong_up"
    UP = "up"
    STABLE = "stable"
    DOWN = "down"
    STRONG_DOWN = "strong_down"


@dataclass
class Prediction:
    """Resultado de uma predição"""
    metric: PredictionType
    current_value: float
    predicted_value: float
    confidence: float
    confidence_interval: Tuple[float, float]
    time_horizon: TimeHorizon
    trend: TrendDirection
    factors: List[Dict[str, Any]]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": self.metric.value,
            "current_value": self.current_value,
            "predicted_value": self.predicted_value,
            "change_percent": ((self.predicted_value - self.current_value) / self.current_value * 100) if self.current_value > 0 else 0,
            "confidence": self.confidence,
            "confidence_interval": {
                "lower": self.confidence_interval[0],
                "upper": self.confidence_interval[1]
            },
            "time_horizon": self.time_horizon.value,
            "trend": self.trend.value,
            "factors": self.factors,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class SeasonalPattern:
    """Padrão sazonal detectado"""
    pattern_type: str  # daily, weekly, monthly
    peak_periods: List[str]
    low_periods: List[str]
    amplitude: float  # Variação percentual
    confidence: float


@dataclass
class AnomalyAlert:
    """Alerta de anomalia detectada"""
    metric: str
    severity: str  # low, medium, high, critical
    description: str
    detected_value: float
    expected_range: Tuple[float, float]
    timestamp: datetime = field(default_factory=datetime.now)


class TimeSeriesAnalyzer:
    """Analisador de séries temporais"""
    
    def __init__(self):
        self.history: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)
        
    def add_data_point(self, metric: str, value: float, timestamp: datetime = None):
        """Adiciona ponto de dados"""
        timestamp = timestamp or datetime.now()
        self.history[metric].append((timestamp, value))
        
        # Manter apenas últimos 90 dias
        cutoff = datetime.now() - timedelta(days=90)
        self.history[metric] = [(t, v) for t, v in self.history[metric] if t > cutoff]
        
    def calculate_moving_average(self, metric: str, window: int = 7) -> float:
        """Calcula média móvel"""
        data = self.history.get(metric, [])
        if len(data) < window:
            return sum(v for _, v in data) / len(data) if data else 0
            
        recent = [v for _, v in data[-window:]]
        return sum(recent) / len(recent)
    
    def calculate_trend(self, metric: str, periods: int = 7) -> TrendDirection:
        """Calcula direção da tendência"""
        data = self.history.get(metric, [])
        if len(data) < periods:
            return TrendDirection.STABLE
            
        values = [v for _, v in data[-periods:]]
        
        # Regressão linear simples
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        
        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        slope_percent = (slope / y_mean * 100) if y_mean != 0 else 0
        
        if slope_percent > 10:
            return TrendDirection.STRONG_UP
        elif slope_percent > 3:
            return TrendDirection.UP
        elif slope_percent < -10:
            return TrendDirection.STRONG_DOWN
        elif slope_percent < -3:
            return TrendDirection.DOWN
        else:
            return TrendDirection.STABLE
    
    def detect_seasonality(self, metric: str) -> Optional[SeasonalPattern]:
        """Detecta padrões sazonais"""
        data = self.history.get(metric, [])
        if len(data) < 14:  # Mínimo 2 semanas
            return None
            
        # Análise por dia da semana
        by_weekday = defaultdict(list)
        for timestamp, value in data:
            by_weekday[timestamp.weekday()].append(value)
            
        weekday_avgs = {day: sum(vals)/len(vals) for day, vals in by_weekday.items() if vals}
        
        if not weekday_avgs:
            return None
            
        overall_avg = sum(weekday_avgs.values()) / len(weekday_avgs)
        
        # Identificar picos e vales
        peak_days = [day for day, avg in weekday_avgs.items() if avg > overall_avg * 1.1]
        low_days = [day for day, avg in weekday_avgs.items() if avg < overall_avg * 0.9]
        
        day_names = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        
        amplitude = (max(weekday_avgs.values()) - min(weekday_avgs.values())) / overall_avg * 100 if overall_avg > 0 else 0
        
        return SeasonalPattern(
            pattern_type="weekly",
            peak_periods=[day_names[d] for d in peak_days],
            low_periods=[day_names[d] for d in low_days],
            amplitude=amplitude,
            confidence=0.75 if len(data) > 30 else 0.5
        )


class PredictiveModel:
    """Modelo preditivo base"""
    
    def __init__(self, metric: PredictionType):
        self.metric = metric
        self.weights: Dict[str, float] = {}
        self.bias = 0.0
        self.trained = False
        self.accuracy_history: List[float] = []
        
    def train(self, features: List[Dict[str, float]], targets: List[float]):
        """Treina o modelo com dados históricos"""
        if not features or not targets:
            return
            
        # Inicializar pesos
        feature_names = list(features[0].keys())
        self.weights = {name: random.uniform(-0.1, 0.1) for name in feature_names}
        self.bias = random.uniform(-0.1, 0.1)
        
        # Gradient descent simplificado
        learning_rate = 0.01
        epochs = 100
        
        for _ in range(epochs):
            for i, (feature_dict, target) in enumerate(zip(features, targets)):
                prediction = self._predict_single(feature_dict)
                error = target - prediction
                
                # Atualizar pesos
                for name, value in feature_dict.items():
                    self.weights[name] += learning_rate * error * value
                self.bias += learning_rate * error
                
        self.trained = True
        
    def _predict_single(self, features: Dict[str, float]) -> float:
        """Faz predição para um único exemplo"""
        result = self.bias
        for name, value in features.items():
            result += self.weights.get(name, 0) * value
        return result
    
    def predict(self, features: Dict[str, float], confidence_level: float = 0.95) -> Tuple[float, Tuple[float, float]]:
        """Faz predição com intervalo de confiança"""
        prediction = self._predict_single(features)
        
        # Calcular intervalo de confiança baseado na variância histórica
        std_error = 0.1 * abs(prediction) if prediction != 0 else 1.0
        z_score = 1.96 if confidence_level == 0.95 else 1.645
        
        margin = z_score * std_error
        confidence_interval = (prediction - margin, prediction + margin)
        
        return prediction, confidence_interval


class PredictiveAnalyticsEngine:
    """
    Motor principal de Análise Preditiva
    Coordena modelos de ML para previsões de campanhas
    """
    
    def __init__(self):
        self.models: Dict[PredictionType, PredictiveModel] = {}
        self.time_series_analyzer = TimeSeriesAnalyzer()
        self.predictions_cache: Dict[str, List[Prediction]] = {}
        self.anomaly_alerts: List[AnomalyAlert] = []
        self.feature_importance: Dict[str, float] = {}
        
        # Inicializar modelos
        self._initialize_models()
        
    def _initialize_models(self):
        """Inicializa modelos preditivos"""
        for pred_type in PredictionType:
            self.models[pred_type] = PredictiveModel(pred_type)
            
        logger.info(f"Predictive Analytics Engine inicializado com {len(self.models)} modelos")
        
    def ingest_historical_data(self, campaign_id: str, data: List[Dict[str, Any]]):
        """Ingere dados históricos para treinamento"""
        for record in data:
            timestamp = datetime.fromisoformat(record.get("timestamp", datetime.now().isoformat()))
            
            for metric in ["revenue", "conversions", "spend", "clicks", "impressions"]:
                if metric in record:
                    self.time_series_analyzer.add_data_point(
                        f"{campaign_id}_{metric}",
                        record[metric],
                        timestamp
                    )
                    
    def _extract_features(self, campaign_data: Dict[str, Any]) -> Dict[str, float]:
        """Extrai features para predição"""
        features = {
            "daily_budget": campaign_data.get("daily_budget", 0),
            "bid_amount": campaign_data.get("bid_amount", 0),
            "audience_size": campaign_data.get("audience_size", 0) / 1000000,  # Normalizar
            "days_running": campaign_data.get("days_running", 0),
            "creative_count": campaign_data.get("creative_count", 1),
            "historical_ctr": campaign_data.get("ctr", 0),
            "historical_cvr": campaign_data.get("conversion_rate", 0),
            "competition_level": campaign_data.get("competition_level", 0.5),
            "seasonality_factor": self._get_seasonality_factor(),
            "day_of_week": datetime.now().weekday() / 6,  # Normalizado 0-1
            "hour_of_day": datetime.now().hour / 23,  # Normalizado 0-1
        }
        return features
    
    def _get_seasonality_factor(self) -> float:
        """Calcula fator de sazonalidade atual"""
        hour = datetime.now().hour
        day = datetime.now().weekday()
        
        # Horários de pico (9-12, 19-22)
        hour_factor = 1.2 if 9 <= hour <= 12 or 19 <= hour <= 22 else 0.8
        
        # Dias de semana vs fim de semana
        day_factor = 1.0 if day < 5 else 0.9
        
        return hour_factor * day_factor
    
    def predict_metric(
        self,
        campaign_data: Dict[str, Any],
        metric: PredictionType,
        horizon: TimeHorizon = TimeHorizon.NEXT_DAY
    ) -> Prediction:
        """Gera predição para uma métrica específica"""
        
        features = self._extract_features(campaign_data)
        model = self.models.get(metric)
        
        current_value = campaign_data.get(metric.value, 0)
        
        # Se modelo não treinado, usar heurísticas
        if not model.trained:
            # Predição baseada em tendência e sazonalidade
            trend = self.time_series_analyzer.calculate_trend(
                f"{campaign_data.get('id', '')}_{metric.value}"
            )
            
            trend_multipliers = {
                TrendDirection.STRONG_UP: 1.15,
                TrendDirection.UP: 1.05,
                TrendDirection.STABLE: 1.0,
                TrendDirection.DOWN: 0.95,
                TrendDirection.STRONG_DOWN: 0.85
            }
            
            horizon_multipliers = {
                TimeHorizon.NEXT_HOUR: 1/24,
                TimeHorizon.NEXT_DAY: 1,
                TimeHorizon.NEXT_WEEK: 7,
                TimeHorizon.NEXT_MONTH: 30,
                TimeHorizon.NEXT_QUARTER: 90
            }
            
            base_prediction = current_value * trend_multipliers[trend]
            predicted_value = base_prediction * horizon_multipliers[horizon]
            
            # Adicionar variação baseada em sazonalidade
            seasonality = self._get_seasonality_factor()
            predicted_value *= seasonality
            
            confidence = 0.7
            margin = predicted_value * 0.15
            confidence_interval = (predicted_value - margin, predicted_value + margin)
            
        else:
            predicted_value, confidence_interval = model.predict(features)
            confidence = 0.85
            trend = self.time_series_analyzer.calculate_trend(
                f"{campaign_data.get('id', '')}_{metric.value}"
            )
        
        # Identificar fatores influenciadores
        factors = self._identify_prediction_factors(campaign_data, metric, predicted_value)
        
        return Prediction(
            metric=metric,
            current_value=current_value,
            predicted_value=max(0, predicted_value),  # Não permitir valores negativos
            confidence=confidence,
            confidence_interval=(max(0, confidence_interval[0]), max(0, confidence_interval[1])),
            time_horizon=horizon,
            trend=trend,
            factors=factors
        )
    
    def _identify_prediction_factors(
        self,
        campaign_data: Dict[str, Any],
        metric: PredictionType,
        predicted_value: float
    ) -> List[Dict[str, Any]]:
        """Identifica fatores que influenciam a predição"""
        factors = []
        
        # Fator: Orçamento
        budget = campaign_data.get("daily_budget", 0)
        if budget > 0:
            factors.append({
                "name": "Orçamento Diário",
                "value": f"R$ {budget:.2f}",
                "impact": "positivo" if budget > 50 else "neutro",
                "weight": 0.25
            })
        
        # Fator: CTR histórico
        ctr = campaign_data.get("ctr", 0)
        factors.append({
            "name": "CTR Histórico",
            "value": f"{ctr:.2f}%",
            "impact": "positivo" if ctr > 1.5 else "negativo" if ctr < 0.5 else "neutro",
            "weight": 0.20
        })
        
        # Fator: Sazonalidade
        seasonality = self._get_seasonality_factor()
        factors.append({
            "name": "Sazonalidade",
            "value": f"{seasonality:.2f}x",
            "impact": "positivo" if seasonality > 1 else "negativo",
            "weight": 0.15
        })
        
        # Fator: Tendência
        trend = self.time_series_analyzer.calculate_trend(
            f"{campaign_data.get('id', '')}_{metric.value}"
        )
        factors.append({
            "name": "Tendência",
            "value": trend.value.replace("_", " ").title(),
            "impact": "positivo" if "up" in trend.value else "negativo" if "down" in trend.value else "neutro",
            "weight": 0.20
        })
        
        # Fator: Competição
        competition = campaign_data.get("competition_level", 0.5)
        factors.append({
            "name": "Nível de Competição",
            "value": f"{competition*100:.0f}%",
            "impact": "negativo" if competition > 0.7 else "positivo" if competition < 0.3 else "neutro",
            "weight": 0.20
        })
        
        return factors
    
    def predict_all_metrics(
        self,
        campaign_data: Dict[str, Any],
        horizon: TimeHorizon = TimeHorizon.NEXT_DAY
    ) -> Dict[str, Prediction]:
        """Gera predições para todas as métricas"""
        predictions = {}
        
        for metric in PredictionType:
            try:
                prediction = self.predict_metric(campaign_data, metric, horizon)
                predictions[metric.value] = prediction
            except Exception as e:
                logger.error(f"Erro ao prever {metric.value}: {e}")
                
        return predictions
    
    def detect_anomalies(self, campaign_data: Dict[str, Any]) -> List[AnomalyAlert]:
        """Detecta anomalias nos dados da campanha"""
        alerts = []
        campaign_id = campaign_data.get("id", "")
        
        metrics_to_check = ["ctr", "cpc", "cpa", "roas", "conversion_rate"]
        
        for metric in metrics_to_check:
            current_value = campaign_data.get(metric, 0)
            
            # Calcular média e desvio padrão históricos
            history_key = f"{campaign_id}_{metric}"
            history = self.time_series_analyzer.history.get(history_key, [])
            
            if len(history) < 7:
                continue
                
            values = [v for _, v in history]
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std_dev = variance ** 0.5
            
            if std_dev == 0:
                continue
                
            z_score = (current_value - mean) / std_dev
            
            if abs(z_score) > 3:
                severity = "critical"
            elif abs(z_score) > 2:
                severity = "high"
            elif abs(z_score) > 1.5:
                severity = "medium"
            else:
                continue
                
            direction = "acima" if z_score > 0 else "abaixo"
            
            alerts.append(AnomalyAlert(
                metric=metric,
                severity=severity,
                description=f"{metric.upper()} está {abs(z_score):.1f} desvios padrão {direction} da média",
                detected_value=current_value,
                expected_range=(mean - 2*std_dev, mean + 2*std_dev)
            ))
            
        self.anomaly_alerts.extend(alerts)
        return alerts
    
    def get_forecast_summary(
        self,
        campaign_data: Dict[str, Any],
        horizons: List[TimeHorizon] = None
    ) -> Dict[str, Any]:
        """Gera resumo de previsões para múltiplos horizontes"""
        horizons = horizons or [TimeHorizon.NEXT_DAY, TimeHorizon.NEXT_WEEK, TimeHorizon.NEXT_MONTH]
        
        summary = {
            "campaign_id": campaign_data.get("id", ""),
            "generated_at": datetime.now().isoformat(),
            "forecasts": {}
        }
        
        for horizon in horizons:
            predictions = self.predict_all_metrics(campaign_data, horizon)
            summary["forecasts"][horizon.value] = {
                metric: pred.to_dict() for metric, pred in predictions.items()
            }
            
        # Adicionar insights
        summary["insights"] = self._generate_forecast_insights(summary["forecasts"])
        
        return summary
    
    def _generate_forecast_insights(self, forecasts: Dict[str, Any]) -> List[Dict[str, str]]:
        """Gera insights baseados nas previsões"""
        insights = []
        
        # Analisar tendência de receita
        if "24h" in forecasts and "revenue" in forecasts["24h"]:
            revenue_pred = forecasts["24h"]["revenue"]
            change = revenue_pred.get("change_percent", 0)
            
            if change > 10:
                insights.append({
                    "type": "positive",
                    "title": "Crescimento de Receita Previsto",
                    "description": f"Previsão de aumento de {change:.1f}% na receita nas próximas 24h"
                })
            elif change < -10:
                insights.append({
                    "type": "warning",
                    "title": "Queda de Receita Prevista",
                    "description": f"Previsão de queda de {abs(change):.1f}% na receita nas próximas 24h"
                })
                
        # Analisar ROAS
        if "24h" in forecasts and "roas" in forecasts["24h"]:
            roas_pred = forecasts["24h"]["roas"]
            predicted_roas = roas_pred.get("predicted_value", 0)
            
            if predicted_roas < 2:
                insights.append({
                    "type": "alert",
                    "title": "ROAS Abaixo do Ideal",
                    "description": f"ROAS previsto de {predicted_roas:.2f}x está abaixo do mínimo recomendado de 2x"
                })
                
        return insights
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do motor de análise preditiva"""
        return {
            "models_count": len(self.models),
            "trained_models": len([m for m in self.models.values() if m.trained]),
            "data_points": sum(len(v) for v in self.time_series_analyzer.history.values()),
            "active_alerts": len(self.anomaly_alerts),
            "last_prediction": datetime.now().isoformat()
        }


# Instância global
predictive_engine = PredictiveAnalyticsEngine()


# Funções de conveniência
def predict_campaign_performance(campaign_data: Dict[str, Any], horizon: str = "24h") -> Dict[str, Any]:
    """Prevê performance de uma campanha"""
    horizon_map = {
        "1h": TimeHorizon.NEXT_HOUR,
        "24h": TimeHorizon.NEXT_DAY,
        "7d": TimeHorizon.NEXT_WEEK,
        "30d": TimeHorizon.NEXT_MONTH,
        "90d": TimeHorizon.NEXT_QUARTER
    }
    
    time_horizon = horizon_map.get(horizon, TimeHorizon.NEXT_DAY)
    predictions = predictive_engine.predict_all_metrics(campaign_data, time_horizon)
    
    return {
        metric: pred.to_dict() for metric, pred in predictions.items()
    }

def get_forecast_summary(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """Obtém resumo de previsões"""
    return predictive_engine.get_forecast_summary(campaign_data)

def detect_anomalies(campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Detecta anomalias em uma campanha"""
    alerts = predictive_engine.detect_anomalies(campaign_data)
    return [
        {
            "metric": a.metric,
            "severity": a.severity,
            "description": a.description,
            "value": a.detected_value,
            "expected_range": a.expected_range,
            "timestamp": a.timestamp.isoformat()
        }
        for a in alerts
    ]

"""
REALTIME PIPELINE - Pipeline de Dados em Tempo Real
Coleta, processamento e streaming de dados de campanhas
Nexora Prime V2 - Expansão Unicórnio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from collections import deque
import threading
import time

class RealtimePipeline:
    """Pipeline de dados em tempo real."""
    
    def __init__(self):
        self.name = "Realtime Pipeline"
        self.version = "2.0.0"
        
        # Buffers de dados
        self.data_buffers = {
            "campaigns": deque(maxlen=10000),
            "metrics": deque(maxlen=50000),
            "events": deque(maxlen=100000),
            "alerts": deque(maxlen=5000)
        }
        
        # Streams ativos
        self.active_streams = {}
        
        # Processadores registrados
        self.processors = {}
        
        # Agregadores
        self.aggregators = {
            "1m": {},
            "5m": {},
            "15m": {},
            "1h": {},
            "1d": {}
        }
        
        # Webhooks configurados
        self.webhooks = {}
        
        # Estado do pipeline
        self.pipeline_status = {
            "running": False,
            "started_at": None,
            "events_processed": 0,
            "errors": 0,
            "last_event_at": None
        }
    
    def start_pipeline(self) -> Dict[str, Any]:
        """Inicia o pipeline de dados."""
        
        if self.pipeline_status["running"]:
            return {"status": "already_running"}
        
        self.pipeline_status["running"] = True
        self.pipeline_status["started_at"] = datetime.now().isoformat()
        
        return {
            "status": "started",
            "timestamp": datetime.now().isoformat(),
            "message": "Pipeline de dados iniciado"
        }
    
    def stop_pipeline(self) -> Dict[str, Any]:
        """Para o pipeline de dados."""
        
        self.pipeline_status["running"] = False
        
        return {
            "status": "stopped",
            "timestamp": datetime.now().isoformat(),
            "events_processed": self.pipeline_status["events_processed"]
        }
    
    def ingest_data(self, data_type: str, data: Dict) -> Dict[str, Any]:
        """Ingere dados no pipeline."""
        
        if not self.pipeline_status["running"]:
            return {"error": "Pipeline nao esta rodando"}
        
        # Adicionar timestamp se nao existir
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        
        # Adicionar ao buffer apropriado
        if data_type in self.data_buffers:
            self.data_buffers[data_type].append(data)
        else:
            self.data_buffers["events"].append({"type": data_type, "data": data})
        
        # Atualizar estatisticas
        self.pipeline_status["events_processed"] += 1
        self.pipeline_status["last_event_at"] = data["timestamp"]
        
        # Processar dados
        processed = self._process_data(data_type, data)
        
        # Agregar dados
        self._aggregate_data(data_type, data)
        
        # Disparar webhooks se configurados
        self._trigger_webhooks(data_type, data)
        
        return {
            "status": "ingested",
            "data_type": data_type,
            "processed": processed,
            "buffer_size": len(self.data_buffers.get(data_type, []))
        }
    
    def create_stream(self, stream_id: str, config: Dict) -> Dict[str, Any]:
        """Cria um stream de dados."""
        
        stream = {
            "id": stream_id,
            "config": config,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "subscribers": [],
            "events_sent": 0
        }
        
        self.active_streams[stream_id] = stream
        
        return {
            "stream_id": stream_id,
            "status": "created",
            "config": config
        }
    
    def subscribe_to_stream(self, stream_id: str, subscriber_id: str, callback: Callable = None) -> Dict[str, Any]:
        """Inscreve um subscriber em um stream."""
        
        if stream_id not in self.active_streams:
            return {"error": "Stream nao encontrado"}
        
        self.active_streams[stream_id]["subscribers"].append({
            "id": subscriber_id,
            "subscribed_at": datetime.now().isoformat(),
            "callback": callback
        })
        
        return {
            "status": "subscribed",
            "stream_id": stream_id,
            "subscriber_id": subscriber_id
        }
    
    def get_realtime_metrics(self, campaign_id: str = None, window: str = "5m") -> Dict[str, Any]:
        """Obtem metricas em tempo real."""
        
        # Determinar janela de tempo
        windows = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "1d": 86400}
        seconds = windows.get(window, 300)
        
        cutoff = datetime.now() - timedelta(seconds=seconds)
        
        # Filtrar metricas do buffer
        recent_metrics = []
        for metric in self.data_buffers["metrics"]:
            try:
                metric_time = datetime.fromisoformat(metric.get("timestamp", ""))
                if metric_time >= cutoff:
                    if campaign_id is None or metric.get("campaign_id") == campaign_id:
                        recent_metrics.append(metric)
            except:
                continue
        
        # Calcular agregados
        if recent_metrics:
            total_spend = sum(m.get("spend", 0) for m in recent_metrics)
            total_revenue = sum(m.get("revenue", 0) for m in recent_metrics)
            total_impressions = sum(m.get("impressions", 0) for m in recent_metrics)
            total_clicks = sum(m.get("clicks", 0) for m in recent_metrics)
            total_conversions = sum(m.get("conversions", 0) for m in recent_metrics)
            
            aggregated = {
                "spend": round(total_spend, 2),
                "revenue": round(total_revenue, 2),
                "impressions": total_impressions,
                "clicks": total_clicks,
                "conversions": total_conversions,
                "ctr": round((total_clicks / total_impressions) * 100, 2) if total_impressions > 0 else 0,
                "cpc": round(total_spend / total_clicks, 2) if total_clicks > 0 else 0,
                "cpa": round(total_spend / total_conversions, 2) if total_conversions > 0 else 0,
                "roas": round(total_revenue / total_spend, 2) if total_spend > 0 else 0
            }
        else:
            aggregated = {"spend": 0, "revenue": 0, "impressions": 0, "clicks": 0, "conversions": 0}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "window": window,
            "campaign_id": campaign_id,
            "data_points": len(recent_metrics),
            "metrics": aggregated,
            "trend": self._calculate_trend(recent_metrics)
        }
    
    def get_live_feed(self, limit: int = 100, data_type: str = "events") -> List[Dict]:
        """Obtem feed ao vivo de eventos."""
        
        if data_type not in self.data_buffers:
            return []
        
        buffer = list(self.data_buffers[data_type])
        return buffer[-limit:]
    
    def register_processor(self, processor_id: str, processor_func: Callable, data_types: List[str]) -> Dict[str, Any]:
        """Registra um processador de dados."""
        
        self.processors[processor_id] = {
            "func": processor_func,
            "data_types": data_types,
            "registered_at": datetime.now().isoformat(),
            "invocations": 0
        }
        
        return {
            "status": "registered",
            "processor_id": processor_id,
            "data_types": data_types
        }
    
    def configure_webhook(self, webhook_id: str, url: str, events: List[str], filters: Dict = None) -> Dict[str, Any]:
        """Configura um webhook."""
        
        self.webhooks[webhook_id] = {
            "url": url,
            "events": events,
            "filters": filters or {},
            "created_at": datetime.now().isoformat(),
            "calls_made": 0,
            "last_call": None
        }
        
        return {
            "status": "configured",
            "webhook_id": webhook_id,
            "url": url,
            "events": events
        }
    
    def get_aggregated_data(self, interval: str, metric: str = None, campaign_id: str = None) -> Dict[str, Any]:
        """Obtem dados agregados por intervalo."""
        
        if interval not in self.aggregators:
            return {"error": f"Intervalo invalido: {interval}"}
        
        aggregated = self.aggregators[interval]
        
        if campaign_id:
            aggregated = {k: v for k, v in aggregated.items() if campaign_id in k}
        
        if metric:
            aggregated = {k: v.get(metric) for k, v in aggregated.items() if metric in v}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "interval": interval,
            "data": aggregated
        }
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Obtem status do pipeline."""
        
        buffer_sizes = {name: len(buffer) for name, buffer in self.data_buffers.items()}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "status": self.pipeline_status,
            "buffer_sizes": buffer_sizes,
            "active_streams": len(self.active_streams),
            "registered_processors": len(self.processors),
            "configured_webhooks": len(self.webhooks)
        }
    
    def flush_buffer(self, buffer_name: str = None) -> Dict[str, Any]:
        """Limpa buffers de dados."""
        
        if buffer_name:
            if buffer_name in self.data_buffers:
                self.data_buffers[buffer_name].clear()
                return {"status": "flushed", "buffer": buffer_name}
            return {"error": "Buffer nao encontrado"}
        
        for buffer in self.data_buffers.values():
            buffer.clear()
        
        return {"status": "all_flushed"}
    
    def create_alert_rule(self, rule_id: str, condition: Dict, actions: List[Dict]) -> Dict[str, Any]:
        """Cria regra de alerta."""
        
        rule = {
            "id": rule_id,
            "condition": condition,
            "actions": actions,
            "created_at": datetime.now().isoformat(),
            "triggers": 0,
            "last_triggered": None,
            "active": True
        }
        
        return {
            "status": "created",
            "rule_id": rule_id,
            "rule": rule
        }
    
    def _process_data(self, data_type: str, data: Dict) -> Dict[str, Any]:
        """Processa dados atraves dos processadores registrados."""
        
        results = {}
        
        for proc_id, processor in self.processors.items():
            if data_type in processor["data_types"]:
                try:
                    if processor["func"]:
                        result = processor["func"](data)
                        results[proc_id] = result
                        processor["invocations"] += 1
                except Exception as e:
                    results[proc_id] = {"error": str(e)}
                    self.pipeline_status["errors"] += 1
        
        return results
    
    def _aggregate_data(self, data_type: str, data: Dict):
        """Agrega dados em diferentes intervalos."""
        
        if data_type != "metrics":
            return
        
        timestamp = datetime.now()
        campaign_id = data.get("campaign_id", "unknown")
        
        # Agregar por minuto
        minute_key = f"{campaign_id}_{timestamp.strftime('%Y%m%d%H%M')}"
        if minute_key not in self.aggregators["1m"]:
            self.aggregators["1m"][minute_key] = {"spend": 0, "revenue": 0, "impressions": 0, "clicks": 0, "conversions": 0}
        
        self.aggregators["1m"][minute_key]["spend"] += data.get("spend", 0)
        self.aggregators["1m"][minute_key]["revenue"] += data.get("revenue", 0)
        self.aggregators["1m"][minute_key]["impressions"] += data.get("impressions", 0)
        self.aggregators["1m"][minute_key]["clicks"] += data.get("clicks", 0)
        self.aggregators["1m"][minute_key]["conversions"] += data.get("conversions", 0)
        
        # Limpar agregados antigos (manter apenas ultimas 24h)
        self._cleanup_old_aggregates()
    
    def _cleanup_old_aggregates(self):
        """Limpa agregados antigos."""
        cutoff = datetime.now() - timedelta(hours=24)
        cutoff_str = cutoff.strftime('%Y%m%d%H%M')
        
        for interval in self.aggregators:
            keys_to_remove = [k for k in self.aggregators[interval] if k.split('_')[-1] < cutoff_str]
            for key in keys_to_remove:
                del self.aggregators[interval][key]
    
    def _trigger_webhooks(self, data_type: str, data: Dict):
        """Dispara webhooks configurados."""
        
        for webhook_id, webhook in self.webhooks.items():
            if data_type in webhook["events"]:
                # Aplicar filtros
                if self._apply_filters(data, webhook["filters"]):
                    # Em producao, faria chamada HTTP real
                    webhook["calls_made"] += 1
                    webhook["last_call"] = datetime.now().isoformat()
    
    def _apply_filters(self, data: Dict, filters: Dict) -> bool:
        """Aplica filtros aos dados."""
        
        for key, value in filters.items():
            if key in data:
                if isinstance(value, dict):
                    if "min" in value and data[key] < value["min"]:
                        return False
                    if "max" in value and data[key] > value["max"]:
                        return False
                elif data[key] != value:
                    return False
        
        return True
    
    def _calculate_trend(self, metrics: List[Dict]) -> Dict[str, str]:
        """Calcula tendencia das metricas."""
        
        if len(metrics) < 2:
            return {"overall": "stable"}
        
        # Dividir em duas metades
        mid = len(metrics) // 2
        first_half = metrics[:mid]
        second_half = metrics[mid:]
        
        # Calcular medias
        first_spend = sum(m.get("spend", 0) for m in first_half) / len(first_half) if first_half else 0
        second_spend = sum(m.get("spend", 0) for m in second_half) / len(second_half) if second_half else 0
        
        first_roas = sum(m.get("roas", 0) for m in first_half) / len(first_half) if first_half else 0
        second_roas = sum(m.get("roas", 0) for m in second_half) / len(second_half) if second_half else 0
        
        spend_trend = "increasing" if second_spend > first_spend * 1.1 else "decreasing" if second_spend < first_spend * 0.9 else "stable"
        roas_trend = "increasing" if second_roas > first_roas * 1.1 else "decreasing" if second_roas < first_roas * 0.9 else "stable"
        
        return {
            "spend": spend_trend,
            "roas": roas_trend,
            "overall": "positive" if roas_trend == "increasing" else "negative" if roas_trend == "decreasing" else "stable"
        }


# Instancia global
realtime_pipeline = RealtimePipeline()

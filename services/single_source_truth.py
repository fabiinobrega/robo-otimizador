# services/single_source_truth.py
"""
NEXORA PRIME - Single Source of Truth (SSOT)
Sistema de reconciliação de dados e validação entre múltiplas fontes
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class SingleSourceOfTruth:
    """Sistema de reconciliação de dados entre múltiplas fontes."""
    
    def __init__(self):
        self.data_sources = {
            "meta_ads": {"priority": 1, "status": "active"},
            "google_ads": {"priority": 1, "status": "active"},
            "internal_db": {"priority": 2, "status": "active"},
            "analytics": {"priority": 3, "status": "active"}
        }
        self.reconciliation_logs = []
        self.discrepancy_threshold = 0.05  # 5% de tolerância
        self.canonical_data = {}
    
    def reconcile_data(self, entity_id: str, data_from_sources: Dict[str, Dict]) -> Dict:
        """Reconcilia dados de múltiplas fontes e retorna a versão canônica."""
        discrepancies = []
        reconciled_data = {}
        
        # Obter todas as métricas únicas
        all_metrics = set()
        for source_data in data_from_sources.values():
            all_metrics.update(source_data.keys())
        
        for metric in all_metrics:
            values_by_source = {}
            for source, data in data_from_sources.items():
                if metric in data:
                    values_by_source[source] = data[metric]
            
            if len(values_by_source) > 1:
                # Verificar discrepâncias
                values = list(values_by_source.values())
                if all(isinstance(v, (int, float)) for v in values):
                    max_val = max(values)
                    min_val = min(values)
                    if max_val > 0 and (max_val - min_val) / max_val > self.discrepancy_threshold:
                        discrepancies.append({
                            "metric": metric,
                            "values": values_by_source,
                            "variance": (max_val - min_val) / max_val
                        })
            
            # Usar valor da fonte com maior prioridade
            reconciled_data[metric] = self._get_priority_value(values_by_source)
        
        # Registrar reconciliação
        reconciliation_record = {
            "entity_id": entity_id,
            "timestamp": datetime.now().isoformat(),
            "sources_used": list(data_from_sources.keys()),
            "discrepancies_found": len(discrepancies),
            "discrepancies": discrepancies
        }
        self.reconciliation_logs.append(reconciliation_record)
        
        # Atualizar dados canônicos
        self.canonical_data[entity_id] = {
            "data": reconciled_data,
            "last_reconciled": datetime.now().isoformat(),
            "confidence": 1.0 - (len(discrepancies) * 0.1)
        }
        
        return {
            "success": True,
            "data": reconciled_data,
            "discrepancies": discrepancies,
            "confidence": self.canonical_data[entity_id]["confidence"]
        }
    
    def validate_data(self, entity_id: str, data: Dict) -> Dict:
        """Valida dados contra regras de negócio e integridade."""
        validation_errors = []
        warnings = []
        
        # Validações de integridade
        if "spend" in data and "impressions" in data:
            if data["impressions"] > 0:
                cpm = (data["spend"] / data["impressions"]) * 1000
                if cpm > 500:
                    warnings.append(f"CPM muito alto: R${cpm:.2f}")
                if cpm < 0.01:
                    validation_errors.append("CPM impossível (muito baixo)")
        
        if "clicks" in data and "impressions" in data:
            if data["impressions"] > 0:
                ctr = (data["clicks"] / data["impressions"]) * 100
                if ctr > 50:
                    validation_errors.append(f"CTR impossível: {ctr:.1f}%")
        
        if "conversions" in data and "clicks" in data:
            if data["clicks"] > 0:
                conv_rate = (data["conversions"] / data["clicks"]) * 100
                if conv_rate > 100:
                    validation_errors.append("Taxa de conversão impossível (>100%)")
        
        # Validações de valores negativos
        for key, value in data.items():
            if isinstance(value, (int, float)) and value < 0:
                validation_errors.append(f"Valor negativo não permitido: {key}")
        
        return {
            "valid": len(validation_errors) == 0,
            "errors": validation_errors,
            "warnings": warnings
        }
    
    def get_canonical_data(self, entity_id: str) -> Optional[Dict]:
        """Retorna os dados canônicos de uma entidade."""
        return self.canonical_data.get(entity_id)
    
    def get_all_canonical_data(self) -> Dict:
        """Retorna todos os dados canônicos."""
        return self.canonical_data
    
    def get_reconciliation_history(self, entity_id: Optional[str] = None) -> List[Dict]:
        """Retorna o histórico de reconciliações."""
        if entity_id:
            return [r for r in self.reconciliation_logs if r["entity_id"] == entity_id]
        return self.reconciliation_logs
    
    def get_discrepancy_report(self) -> Dict:
        """Gera relatório de discrepâncias encontradas."""
        total_reconciliations = len(self.reconciliation_logs)
        total_discrepancies = sum(r["discrepancies_found"] for r in self.reconciliation_logs)
        
        discrepancy_by_metric = {}
        for record in self.reconciliation_logs:
            for disc in record["discrepancies"]:
                metric = disc["metric"]
                if metric not in discrepancy_by_metric:
                    discrepancy_by_metric[metric] = 0
                discrepancy_by_metric[metric] += 1
        
        return {
            "total_reconciliations": total_reconciliations,
            "total_discrepancies": total_discrepancies,
            "discrepancy_rate": total_discrepancies / total_reconciliations if total_reconciliations > 0 else 0,
            "discrepancies_by_metric": discrepancy_by_metric,
            "most_problematic_metric": max(discrepancy_by_metric, key=discrepancy_by_metric.get) if discrepancy_by_metric else None
        }
    
    def add_data_source(self, source_name: str, priority: int) -> Dict:
        """Adiciona uma nova fonte de dados."""
        self.data_sources[source_name] = {
            "priority": priority,
            "status": "active",
            "added_at": datetime.now().isoformat()
        }
        return {"success": True, "source": source_name}
    
    def set_source_status(self, source_name: str, status: str) -> Dict:
        """Define o status de uma fonte de dados."""
        if source_name in self.data_sources:
            self.data_sources[source_name]["status"] = status
            return {"success": True}
        return {"success": False, "error": "Fonte não encontrada"}
    
    def _get_priority_value(self, values_by_source: Dict) -> Any:
        """Retorna o valor da fonte com maior prioridade."""
        best_source = None
        best_priority = float('inf')
        
        for source, value in values_by_source.items():
            if source in self.data_sources:
                priority = self.data_sources[source]["priority"]
                if priority < best_priority:
                    best_priority = priority
                    best_source = source
        
        return values_by_source.get(best_source, list(values_by_source.values())[0])
    
    def register_data(self, entity_type: str, entity_id: str, data: Dict) -> Dict:
        """Registra dados no sistema central."""
        full_id = f"{entity_type}_{entity_id}"
        self.canonical_data[full_id] = {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": data,
            "registered_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        return {"success": True, "id": full_id}
    
    def get_data(self, entity_type: str, entity_id: str) -> Optional[Dict]:
        """Recupera dados do sistema central."""
        full_id = f"{entity_type}_{entity_id}"
        return self.canonical_data.get(full_id)
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema SSOT."""
        return {
            "data_sources": self.data_sources,
            "total_canonical_entities": len(self.canonical_data),
            "total_reconciliations": len(self.reconciliation_logs),
            "discrepancy_threshold": self.discrepancy_threshold
        }


# Instâncias globais
single_source_truth = SingleSourceOfTruth()
single_source_of_truth = single_source_truth  # Alias para compatibilidade

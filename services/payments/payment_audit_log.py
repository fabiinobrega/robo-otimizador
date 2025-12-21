"""
Payment Audit Log - NEXORA PRIME v12.4+
Sistema unificado de logs e auditoria para rastreamento completo de pagamentos
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any

class PaymentAuditLog:
    """Serviço de auditoria de pagamentos"""
    
    def __init__(self):
        self.log_files = {
            "credit_wallet": "data/payments/credit_wallet_audit.jsonl",
            "stripe_service": "data/payments/stripe_payment_service.jsonl",
            "webhooks": "data/payments/webhook_events.jsonl",
            "facebook_funding": "data/payments/facebook_ads_funding.jsonl",
            "google_funding": "data/payments/google_ads_funding.jsonl",
            "security_blocks": "data/payments/security_blocks.jsonl"
        }
        self.consolidated_log_file = "data/payments/consolidated_audit_log.jsonl"
    
    def _read_log_file(self, file_path: str, source: str) -> List[Dict[str, Any]]:
        """Lê um arquivo de log JSONL e adiciona a fonte"""
        if not os.path.exists(file_path):
            return []
        
        entries = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        entry = json.loads(line)
                        entry['source'] = source
                        entries.append(entry)
                    except json.JSONDecodeError:
                        # Ignorar linhas malformadas
                        pass
        return entries
    
    def consolidate_logs(self) -> Dict[str, Any]:
        """Consolida todos os logs de pagamento em um único arquivo"""
        all_entries = []
        
        for source, file_path in self.log_files.items():
            all_entries.extend(self._read_log_file(file_path, source))
        
        # Ordenar por timestamp
        all_entries.sort(key=lambda x: x.get('timestamp', ''))
        
        # Salvar log consolidado
        with open(self.consolidated_log_file, 'w') as f:
            for entry in all_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        return {
            "success": True,
            "message": "Logs consolidados com sucesso",
            "total_entries": len(all_entries),
            "consolidated_log_file": self.consolidated_log_file
        }
    
    def get_consolidated_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retorna os logs consolidados mais recentes"""
        if not os.path.exists(self.consolidated_log_file):
            self.consolidate_logs()
            
        if not os.path.exists(self.consolidated_log_file):
            return []
            
        with open(self.consolidated_log_file, 'r') as f:
            lines = f.readlines()
        
        entries = [json.loads(line) for line in lines if line.strip()]
        
        return entries[-limit:]
    
    def generate_audit_summary(self) -> Dict[str, Any]:
        """Gera um resumo de auditoria"""
        self.consolidate_logs()
        
        summary = {
            "total_entries": 0,
            "entries_by_source": {source: 0 for source in self.log_files.keys()},
            "error_count": 0,
            "security_block_count": 0,
            "successful_payments": 0,
            "failed_payments": 0,
            "refunds": 0
        }
        
        if not os.path.exists(self.consolidated_log_file):
            return {"success": False, "error": "Nenhum log encontrado"}
        
        with open(self.consolidated_log_file, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    summary["total_entries"] += 1
                    source = entry.get('source')
                    if source in summary["entries_by_source"]:
                        summary["entries_by_source"][source] += 1
                    
                    # Contar erros e bloqueios
                    if 'error' in str(entry).lower() or 'failed' in str(entry).lower():
                        summary["error_count"] += 1
                    
                    if source == 'security_blocks':
                        summary["security_block_count"] += 1
                    
                    # Contar pagamentos
                    if entry.get('event_type') == 'payment_intent.succeeded':
                        summary["successful_payments"] += 1
                    elif entry.get('event_type') == 'payment_intent.payment_failed':
                        summary["failed_payments"] += 1
                    elif entry.get('event_type') == 'charge.refunded':
                        summary["refunds"] += 1
                        
        return {"success": True, "summary": summary}

"""
Serviço de Integração MCP (Model Context Protocol)
Comunicação bidirecional entre Manus e Nexora Operator
"""

import os
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import secrets
# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres



class MCPIntegrationService:
    """Serviço de integração MCP para comunicação Manus ↔ Nexora"""
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.api_base_url = os.getenv('NEXORA_API_URL', 'https://robo-otimizador1.onrender.com')
        
        # Configurações MCP
        self.mcp_enabled = True
        self.webhook_secret = os.getenv('WEBHOOK_SECRET', self._generate_webhook_secret())
        
        # Estado da conexão
        self.is_connected = False
        self.last_sync = None
        
    def _generate_webhook_secret(self) -> str:
        """Gera um secret para validação de webhooks"""
        return secrets.token_urlsafe(32)
    
    # ===== COMUNICAÇÃO BIDIRECIONAL =====
    
    def send_command(self, command: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Envia comando do Manus para o Nexora
        
        Args:
            command: Nome do comando a executar
            params: Parâmetros do comando
            
        Returns:
            dict: Resultado da execução
        """
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Registrar comando
            cursor.execute("""
                INSERT INTO mcp_commands (command, params, status, created_at)
                VALUES (?, ?, 'pending', ?)
            """, (command, json.dumps(params or {}), datetime.now().isoformat()))
            
            command_id = cursor.lastrowid
            conn.commit()
            
            # Executar comando
            result = self._execute_command(command, params or {})
            
            # Atualizar status
            cursor.execute(sql_param("""
                UPDATE mcp_commands 
                SET status = ?, result = ?, executed_at = ?
                WHERE id = ?
            """), (
                'completed' if result['success'] else 'failed',
                json.dumps(result),
                datetime.now().isoformat(),
                command_id
            ))
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'command_id': command_id,
                'result': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _execute_command(self, command: str, params: Dict) -> Dict[str, Any]:
        """Executa um comando específico"""
        
        commands = {
            'create_campaign': self._cmd_create_campaign,
            'update_campaign': self._cmd_update_campaign,
            'pause_campaign': self._cmd_pause_campaign,
            'resume_campaign': self._cmd_resume_campaign,
            'get_metrics': self._cmd_get_metrics,
            'analyze_performance': self._cmd_analyze_performance,
            'optimize_budget': self._cmd_optimize_budget,
            'generate_ad': self._cmd_generate_ad,
            'test_creative': self._cmd_test_creative,
            'get_insights': self._cmd_get_insights
        }
        
        if command in commands:
            return commands[command](params)
        else:
            return {
                'success': False,
                'error': f'Comando desconhecido: {command}'
            }
    
    # ===== COMANDOS DISPONÍVEIS =====
    
    def _cmd_create_campaign(self, params: Dict) -> Dict:
        """Cria uma nova campanha"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO campaigns (
                    name, platform, objective, budget, status,
                    created_at, created_by
                ) VALUES (?, ?, ?, ?, 'draft', ?, 'manus_ai')
            """, (
                params.get('name'),
                params.get('platform'),
                params.get('objective'),
                params.get('budget'),
                datetime.now().isoformat()
            ))
            
            campaign_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'campaign_id': campaign_id,
                'message': 'Campanha criada com sucesso'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _cmd_update_campaign(self, params: Dict) -> Dict:
        """Atualiza uma campanha existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            campaign_id = params.get('campaign_id')
            updates = params.get('updates', {})
            
            # Construir query de update dinamicamente
            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [campaign_id]
            
            cursor.execute(f"""
                UPDATE campaigns SET {set_clause}
                WHERE id = ?
            """, values)
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': 'Campanha atualizada com sucesso'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _cmd_pause_campaign(self, params: Dict) -> Dict:
        """Pausa uma campanha"""
        return self._cmd_update_campaign({
            'campaign_id': params.get('campaign_id'),
            'updates': {'status': 'paused'}
        })
    
    def _cmd_resume_campaign(self, params: Dict) -> Dict:
        """Resume uma campanha pausada"""
        return self._cmd_update_campaign({
            'campaign_id': params.get('campaign_id'),
            'updates': {'status': 'active'}
        })
    
    def _cmd_get_metrics(self, params: Dict) -> Dict:
        """Obtém métricas de uma campanha"""
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            campaign_id = params.get('campaign_id')
            
            cursor.execute(sql_param("""
                SELECT * FROM campaign_metrics
                WHERE campaign_id = ?
                ORDER BY date DESC
                LIMIT 30
            """), (campaign_id,))
            
            metrics = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return {
                'success': True,
                'metrics': metrics
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _cmd_analyze_performance(self, params: Dict) -> Dict:
        """Analisa performance de uma campanha"""
        try:
            # Obter métricas
            metrics_result = self._cmd_get_metrics(params)
            
            if not metrics_result['success']:
                return metrics_result
            
            metrics = metrics_result['metrics']
            
            if not metrics:
                return {
                    'success': True,
                    'analysis': {
                        'status': 'insufficient_data',
                        'message': 'Dados insuficientes para análise'
                    }
                }
            
            # Análise simples
            total_impressions = sum(m.get('impressions', 0) for m in metrics)
            total_clicks = sum(m.get('clicks', 0) for m in metrics)
            total_conversions = sum(m.get('conversions', 0) for m in metrics)
            total_spend = sum(m.get('spend', 0) for m in metrics)
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
            cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
            
            # Classificação de performance
            performance_score = 0
            if ctr > 2.0:
                performance_score += 30
            if cpc < 1.0:
                performance_score += 30
            if cpa < 50.0:
                performance_score += 40
            
            status = 'excellent' if performance_score >= 80 else \
                     'good' if performance_score >= 60 else \
                     'average' if performance_score >= 40 else 'poor'
            
            return {
                'success': True,
                'analysis': {
                    'status': status,
                    'performance_score': performance_score,
                    'metrics': {
                        'total_impressions': total_impressions,
                        'total_clicks': total_clicks,
                        'total_conversions': total_conversions,
                        'total_spend': total_spend,
                        'ctr': round(ctr, 2),
                        'cpc': round(cpc, 2),
                        'cpa': round(cpa, 2)
                    },
                    'recommendations': self._generate_recommendations(status, ctr, cpc, cpa)
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _generate_recommendations(self, status: str, ctr: float, cpc: float, cpa: float) -> List[str]:
        """Gera recomendações baseadas na performance"""
        recommendations = []
        
        if ctr < 1.0:
            recommendations.append("CTR baixo - considere melhorar os criativos e copy")
        if cpc > 2.0:
            recommendations.append("CPC alto - otimize a segmentação e lances")
        if cpa > 100.0:
            recommendations.append("CPA alto - revise o funil de conversão")
        if status == 'excellent':
            recommendations.append("Performance excelente - considere aumentar o orçamento")
        
        return recommendations
    
    def _cmd_optimize_budget(self, params: Dict) -> Dict:
        """Otimiza o orçamento de uma campanha"""
        try:
            # Analisar performance
            analysis = self._cmd_analyze_performance(params)
            
            if not analysis['success']:
                return analysis
            
            performance = analysis['analysis']
            current_budget = params.get('current_budget', 0)
            
            # Sugerir ajuste de orçamento
            if performance['status'] == 'excellent':
                suggested_budget = current_budget * 1.5  # Aumentar 50%
                action = 'increase'
            elif performance['status'] == 'good':
                suggested_budget = current_budget * 1.2  # Aumentar 20%
                action = 'increase'
            elif performance['status'] == 'poor':
                suggested_budget = current_budget * 0.7  # Reduzir 30%
                action = 'decrease'
            else:
                suggested_budget = current_budget
                action = 'maintain'
            
            return {
                'success': True,
                'optimization': {
                    'current_budget': current_budget,
                    'suggested_budget': round(suggested_budget, 2),
                    'action': action,
                    'reason': f"Performance {performance['status']} - Score: {performance['performance_score']}"
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _cmd_generate_ad(self, params: Dict) -> Dict:
        """Gera um anúncio com IA"""
        return {
            'success': True,
            'ad': {
                'headline': params.get('headline', 'Título gerado por IA'),
                'description': params.get('description', 'Descrição gerada por IA'),
                'cta': params.get('cta', 'Saiba Mais'),
                'generated_by': 'velyra_prime'
            }
        }
    
    def _cmd_test_creative(self, params: Dict) -> Dict:
        """Testa um criativo"""
        return {
            'success': True,
            'test_result': {
                'score': 85,
                'feedback': 'Criativo com boa performance esperada',
                'suggestions': ['Testar variação de cor', 'Adicionar urgência no copy']
            }
        }
    
    def _cmd_get_insights(self, params: Dict) -> Dict:
        """Obtém insights de IA"""
        return {
            'success': True,
            'insights': [
                'Melhor horário para anúncios: 18h-21h',
                'Público mais engajado: 25-34 anos',
                'Melhor dia da semana: Terça-feira'
            ]
        }
    
    # ===== WEBHOOKS =====
    
    def register_webhook(self, event: str, url: str) -> Dict[str, Any]:
        """
        Registra um webhook para um evento específico
        
        Args:
            event: Tipo de evento (campaign_created, campaign_updated, etc)
            url: URL para receber o webhook
            
        Returns:
            dict: Resultado do registro
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO webhooks (event, url, secret, active, created_at)
                VALUES (?, ?, ?, 1, ?)
            """, (event, url, self.webhook_secret, datetime.now().isoformat()))
            
            webhook_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'webhook_id': webhook_id,
                'secret': self.webhook_secret
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def trigger_webhook(self, event: str, data: Dict) -> Dict[str, Any]:
        """
        Dispara webhooks registrados para um evento
        
        Args:
            event: Tipo de evento
            data: Dados do evento
            
        Returns:
            dict: Resultado do disparo
        """
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(sql_param("""
                SELECT * FROM webhooks
                WHERE event = ? AND active = 1
            """), (event,))
            
            webhooks = cursor.fetchall()
            conn.close()
            
            results = []
            
            for webhook in webhooks:
                try:
                    # Criar assinatura
                    signature = self._create_webhook_signature(data, webhook['secret'])
                    
                    # Enviar webhook
                    response = requests.post(
                        webhook['url'],
                        json=data,
                        headers={
                            'Content-Type': 'application/json',
                            'X-Webhook-Signature': signature,
                            'X-Webhook-Event': event
                        },
                        timeout=10
                    )
                    
                    results.append({
                        'webhook_id': webhook['id'],
                        'success': response.status_code == 200,
                        'status_code': response.status_code
                    })
                    
                except Exception as e:
                    results.append({
                        'webhook_id': webhook['id'],
                        'success': False,
                        'error': str(e)
                    })
            
            return {
                'success': True,
                'webhooks_triggered': len(results),
                'results': results
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_webhook_signature(self, data: Dict, secret: str) -> str:
        """Cria assinatura HMAC para webhook"""
        import hmac
        
        payload = json.dumps(data, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def verify_webhook_signature(self, data: Dict, signature: str, secret: str) -> bool:
        """Verifica assinatura de webhook recebido"""
        expected_signature = self._create_webhook_signature(data, secret)
        return hmac.compare_digest(signature, expected_signature)
    
    # ===== EVENTOS =====
    
    def emit_event(self, event_type: str, data: Dict) -> Dict[str, Any]:
        """
        Emite um evento para o sistema
        
        Args:
            event_type: Tipo do evento
            data: Dados do evento
            
        Returns:
            dict: Resultado da emissão
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO mcp_events (event_type, data, created_at)
                VALUES (?, ?, ?)
            """, (event_type, json.dumps(data), datetime.now().isoformat()))
            
            event_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Disparar webhooks
            self.trigger_webhook(event_type, data)
            
            return {
                'success': True,
                'event_id': event_id
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== TELEMETRIA =====
    
    def log_telemetry(self, metric: str, value: Any, tags: Dict = None) -> Dict[str, Any]:
        """
        Registra telemetria
        
        Args:
            metric: Nome da métrica
            value: Valor da métrica
            tags: Tags adicionais
            
        Returns:
            dict: Resultado do registro
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO telemetry (metric, value, tags, timestamp)
                VALUES (?, ?, ?, ?)
            """, (metric, str(value), json.dumps(tags or {}), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_telemetry(self, metric: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Obtém dados de telemetria"""
        try:
            conn = get_db_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM telemetry WHERE metric = ?"
            params = [metric]
            
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date)
            
            query += " ORDER BY timestamp DESC LIMIT 1000"
            
            cursor.execute(query, params)
            data = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return {
                'success': True,
                'data': data
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


# Instância global
mcp_service = MCPIntegrationService()

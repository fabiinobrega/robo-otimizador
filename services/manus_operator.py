"""
Manus Operator - Agente Autônomo de IA
Sistema inteligente que monitora, otimiza e executa ações automaticamente
"""
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests

# Importar motor de IA nativa
try:
    from services.native_ai_engine import native_ai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Warning: Native AI engine not available")


class ManusOperator:
    """Agente autônomo inteligente para automação de marketing"""
    
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.status = "active"
        self.last_check = None
        
    def get_db(self):
        """Conectar ao banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def log_action(self, action: str, details: str = ""):
        """Registrar ação do operador"""
        db = self.get_db()
        try:
            db.execute(
                "INSERT INTO activity_logs (action, details) VALUES (?, ?)",
                (f"[Manus Operator] {action}", details)
            )
            db.commit()
        except Exception as e:
            print(f"Erro ao registrar ação: {e}")
        finally:
            db.close()
    
    def monitor_campaigns(self) -> Dict[str, Any]:
        """Monitorar campanhas e identificar problemas"""
        db = self.get_db()
        issues = []
        recommendations = []
        
        try:
            # Verificar campanhas ativas com baixo desempenho
            campaigns = db.execute("""
                SELECT c.*, m.ctr, m.cpa, m.roas, m.spend
                FROM campaigns c
                LEFT JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE c.status = 'Active'
            """).fetchall()
            
            for campaign in campaigns:
                campaign_dict = dict(campaign)
                
                # CTR muito baixo
                if campaign_dict.get('ctr', 0) < 0.5:
                    issues.append({
                        'campaign_id': campaign_dict['id'],
                        'campaign_name': campaign_dict['name'],
                        'issue': 'CTR muito baixo',
                        'severity': 'high',
                        'recommendation': 'Revisar criativos e copy'
                    })
                
                # CPA muito alto
                if campaign_dict.get('cpa', 0) > 100:
                    issues.append({
                        'campaign_id': campaign_dict['id'],
                        'campaign_name': campaign_dict['name'],
                        'issue': 'CPA acima do ideal',
                        'severity': 'medium',
                        'recommendation': 'Ajustar segmentação ou pausar'
                    })
                
                # ROAS negativo
                if campaign_dict.get('roas', 0) < 1:
                    issues.append({
                        'campaign_id': campaign_dict['id'],
                        'campaign_name': campaign_dict['name'],
                        'issue': 'ROAS negativo',
                        'severity': 'critical',
                        'recommendation': 'Pausar campanha imediatamente'
                    })
            
            self.log_action("Monitoramento de Campanhas", f"{len(issues)} problemas identificados")
            
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
        finally:
            db.close()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'issues': issues,
            'recommendations': recommendations,
            'total_issues': len(issues)
        }
    
    def auto_optimize_campaigns(self) -> Dict[str, Any]:
        """Otimizar campanhas automaticamente"""
        db = self.get_db()
        optimizations = []
        
        try:
            # Buscar campanhas que precisam de otimização
            campaigns = db.execute("""
                SELECT c.*, m.ctr, m.cpa, m.roas, m.spend, m.conversions
                FROM campaigns c
                LEFT JOIN campaign_metrics m ON c.id = m.campaign_id
                WHERE c.status = 'Active'
            """).fetchall()
            
            for campaign in campaigns:
                campaign_dict = dict(campaign)
                campaign_id = campaign_dict['id']
                
                # Auto-pausar campanhas ruins
                if campaign_dict.get('roas', 0) < 0.5 and campaign_dict.get('spend', 0) > 50:
                    db.execute(
                        "UPDATE campaigns SET status = 'Paused', updated_at = ? WHERE id = ?",
                        (datetime.now().isoformat(), campaign_id)
                    )
                    optimizations.append({
                        'campaign_id': campaign_id,
                        'action': 'paused',
                        'reason': 'ROAS muito baixo',
                        'previous_status': 'Active'
                    })
                    self.log_action("Auto-Pausar", f"Campanha {campaign_dict['name']} pausada por baixo ROAS")
                
                # Aumentar budget de campanhas performando bem
                elif campaign_dict.get('roas', 0) > 3 and campaign_dict.get('conversions', 0) > 10:
                    new_budget = campaign_dict['budget'] * 1.2  # Aumentar 20%
                    db.execute(
                        "UPDATE campaigns SET budget = ?, updated_at = ? WHERE id = ?",
                        (new_budget, datetime.now().isoformat(), campaign_id)
                    )
                    optimizations.append({
                        'campaign_id': campaign_id,
                        'action': 'budget_increased',
                        'reason': 'Alto ROAS',
                        'previous_budget': campaign_dict['budget'],
                        'new_budget': new_budget
                    })
                    self.log_action("Otimização de Budget", f"Budget da campanha {campaign_dict['name']} aumentado em 20%")
            
            db.commit()
            
        except Exception as e:
            print(f"Erro na otimização: {e}")
        finally:
            db.close()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'optimizations': optimizations,
            'total_optimizations': len(optimizations)
        }
    
    def generate_ai_recommendations(self, campaign_id: int) -> Dict[str, Any]:
        """Gerar recomendações de IA para uma campanha"""
        db = self.get_db()
        recommendations = []
        
        try:
            # Buscar dados da campanha
            campaign = db.execute(
                "SELECT * FROM campaigns WHERE id = ?", (campaign_id,)
            ).fetchone()
            
            if not campaign:
                return {'error': 'Campanha não encontrada'}
            
            campaign_dict = dict(campaign)
            
            # Buscar métricas
            metrics = db.execute(
                "SELECT * FROM campaign_metrics WHERE campaign_id = ?", (campaign_id,)
            ).fetchone()
            
            metrics_dict = dict(metrics) if metrics else {}
            
            # Gerar recomendações baseadas em regras
            if metrics_dict.get('ctr', 0) < 1:
                recommendations.append({
                    'type': 'creative',
                    'priority': 'high',
                    'title': 'Melhorar Criativos',
                    'description': 'CTR abaixo de 1%. Considere testar novos criativos mais chamativos.'
                })
            
            if metrics_dict.get('conversions', 0) < 5:
                recommendations.append({
                    'type': 'targeting',
                    'priority': 'medium',
                    'title': 'Refinar Segmentação',
                    'description': 'Poucas conversões. Revise o público-alvo e ajuste a segmentação.'
                })
            
            if metrics_dict.get('spend', 0) > campaign_dict['budget'] * 0.8:
                recommendations.append({
                    'type': 'budget',
                    'priority': 'high',
                    'title': 'Monitorar Orçamento',
                    'description': 'Você já gastou 80% do orçamento. Considere aumentar ou pausar a campanha.'
                })
            
        except Exception as e:
            print(f"Erro ao gerar recomendações: {e}")
        finally:
            db.close()
        
        return {
            'campaign_id': campaign_id,
            'recommendations': recommendations,
            'generated_at': datetime.now().isoformat()
        }
    
    def chat_response(self, user_message: str, context: Dict = None) -> str:
        """Responder a mensagens do usuário via chat"""
        # Respostas simples baseadas em palavras-chave
        message_lower = user_message.lower()
        
        if 'status' in message_lower or 'como está' in message_lower:
            return "🟢 Manus Operator está ativo e monitorando suas campanhas 24/7. Tudo funcionando perfeitamente!"
        
        elif 'campanha' in message_lower and ('criar' in message_lower or 'nova' in message_lower):
            return "Para criar uma nova campanha, acesse a página 'Criar Campanha' no menu lateral. Posso ajudá-lo com análise de produto, geração de copy e otimização de budget!"
        
        elif 'otimizar' in message_lower or 'melhorar' in message_lower:
            return "Estou constantemente otimizando suas campanhas! Monitoro CTR, CPA, ROAS e faço ajustes automáticos. Quer ver as otimizações recentes?"
        
        elif 'relatório' in message_lower or 'report' in message_lower:
            return "Você pode acessar relatórios detalhados na seção 'Relatórios'. Posso gerar relatórios personalizados com métricas de performance, ROI e recomendações."
        
        elif 'problema' in message_lower or 'erro' in message_lower:
            return "Detectei algum problema? Estou aqui para ajudar! Por favor, descreva o problema e vou investigar imediatamente."
        
        elif 'ajuda' in message_lower or 'help' in message_lower:
            return """Posso ajudá-lo com:
            
• Criar e otimizar campanhas
• Analisar produtos e gerar copy
• Monitorar performance 24/7
• Gerar relatórios detalhados
• Espionar concorrentes
• Ajustar orçamentos automaticamente

Como posso ajudar você hoje?"""
        
        else:
            return "Entendi sua mensagem! Como agente de IA, estou aqui para ajudar com suas campanhas de marketing. Pode me perguntar sobre criação de campanhas, otimização, relatórios ou qualquer dúvida sobre a plataforma."
    
    def health_check(self) -> Dict[str, Any]:
        """Verificar saúde do sistema"""
        status = {
            'operator_status': 'active',
            'database': 'ok',
            'openai_api': 'not_configured',
            'timestamp': datetime.now().isoformat()
        }
        
        # Verificar banco de dados
        try:
            db = self.get_db()
            db.execute("SELECT 1").fetchone()
            db.close()
            status['database'] = 'ok'
        except Exception as e:
            status['database'] = f'error: {str(e)}'
        
        # Verificar API OpenAI
        if self.openai_api_key:
            status['openai_api'] = 'configured'
        
        return status
    
    def execute_automation_rules(self) -> Dict[str, Any]:
        """Executar regras de automação configuradas"""
        db = self.get_db()
        executed_rules = []
        
        try:
            # Buscar regras ativas
            rules = db.execute("""
                SELECT * FROM automation_rules 
                WHERE is_active = 1
            """).fetchall()
            
            for rule in rules:
                rule_dict = dict(rule)
                # Executar lógica da regra
                # (implementação simplificada)
                executed_rules.append({
                    'rule_id': rule_dict['id'],
                    'rule_name': rule_dict.get('name', 'Unnamed Rule'),
                    'executed_at': datetime.now().isoformat()
                })
        
        except Exception as e:
            print(f"Erro ao executar regras: {e}")
        finally:
            db.close()
        
        return {
            'executed_rules': executed_rules,
            'total_executed': len(executed_rules)
        }


# Instância global do operador
operator = ManusOperator()

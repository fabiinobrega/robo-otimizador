"""
Velyra Prime - Agente Autônomo de IA
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


# Importar sistema de treinamento
try:
    from services.velyra_training_system import velyra_training, check_can_execute
    TRAINING_SYSTEM_AVAILABLE = True
except ImportError:
    TRAINING_SYSTEM_AVAILABLE = False
    velyra_training = None
    print("Warning: Training system not available")


class VelyraPrime:
    """
    Agente autônomo inteligente para automação de marketing.
    
    🔥 IMPORTANTE: Velyra só pode operar após treinamento completo!
    
    Funções FINAIS da Velyra (após treinamento):
    - Analisar mercado e concorrência
    - Definir público-alvo e avatar real
    - Criar estratégia de tráfego e funil
    - Criar anúncios vencedores
    - Otimizar campanhas com base em dados
    - Escalar campanhas com segurança
    - Aprender com resultados reais em produção
    """
    
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.status = "active"
        self.last_check = None
        self.training_system = velyra_training if TRAINING_SYSTEM_AVAILABLE else None
        
        # Status de treinamento
        self.is_trained = False
        self.training_phase = 0
        
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
                (f"[Velyra Prime] {action}", details)
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
    
    # ===== MÉTODOS DE TREINAMENTO =====
    
    def check_training_status(self) -> Dict[str, Any]:
        """Verifica o status do treinamento da Velyra."""
        if not self.training_system:
            return {
                'trained': False,
                'message': 'Sistema de treinamento não disponível',
                'can_execute': True  # Modo legado
            }
        
        status = self.training_system.get_training_status()
        can_execute = self.training_system.check_execution_permission()
        
        return {
            'trained': status['is_authorized'],
            'phase': status['status']['phase'],
            'modules_completed': len(status['status']['modules_completed']),
            'total_modules': 11,
            'can_execute': can_execute['allowed'],
            'status': status
        }
    
    def start_training(self) -> Dict[str, Any]:
        """Inicia o treinamento estratégico da Velyra."""
        if not self.training_system:
            return {'error': 'Sistema de treinamento não disponível'}
        
        self.log_action("Treinamento Iniciado", "Iniciando treinamento estratégico de marketing digital")
        return self.training_system.start_training()
    
    def get_current_training_module(self) -> Dict[str, Any]:
        """Retorna o módulo atual de treinamento."""
        if not self.training_system:
            return {'error': 'Sistema de treinamento não disponível'}
        
        return self.training_system.get_current_module()
    
    def teach_module(self, module_id: int) -> Dict[str, Any]:
        """Ensina um módulo específico."""
        if not self.training_system:
            return {'error': 'Sistema de treinamento não disponível'}
        
        return self.training_system.teach_module(module_id)
    
    def complete_training_module(self, module_id: int) -> Dict[str, Any]:
        """Marca um módulo como completado."""
        if not self.training_system:
            return {'error': 'Sistema de treinamento não disponível'}
        
        result = self.training_system.complete_module(module_id)
        self.log_action(f"Módulo {module_id} Completado", result.get('message', ''))
        return result
    
    def validate_learning(self, module_id: int, response: str) -> Dict[str, Any]:
        """Valida o aprendizado em um módulo."""
        if not self.training_system:
            return {'error': 'Sistema de treinamento não disponível'}
        
        result = self.training_system.validate_learning(module_id, response)
        self.log_action(f"Validação Módulo {module_id}", "Aprovado" if result.get('success') else "Reprovado")
        return result
    
    def can_create_campaign(self) -> Dict[str, Any]:
        """Verifica se a Velyra pode criar campanhas."""
        if not self.training_system:
            # Se não há sistema de treinamento, permitir por padrão
            return {'allowed': True, 'message': 'Modo legado - sem verificação de treinamento'}
        
        return self.training_system.check_execution_permission()
    
    def record_campaign_learning(self, campaign_id: int, metrics: Dict, insights: List[str]) -> Dict[str, Any]:
        """Registra aprendizado de uma campanha em produção."""
        if not self.training_system:
            return {'error': 'Sistema de treinamento não disponível'}
        
        result = self.training_system.record_learning(campaign_id, metrics, insights)
        self.log_action("Aprendizado Registrado", f"Campanha {campaign_id}: {len(insights)} insights")
        return result
    
    # ===== MÉTODOS DE CHAT =====
    
    def chat_response(self, user_message: str, context: Dict = None) -> str:
        """Responder a mensagens do usuário via chat"""
        # Respostas simples baseadas em palavras-chave
        message_lower = user_message.lower()
        
        if 'status' in message_lower or 'como está' in message_lower:
            return "🟢 Velyra Prime está ativo e monitorando suas campanhas 24/7. Tudo funcionando perfeitamente!"
        
        elif 'campanha' in message_lower and ('criar' in message_lower or 'nova' in message_lower):
            # Detectar se é pedido para criar campanha Synadentix
            if 'synadentix' in message_lower or 'google ads' in message_lower:
                try:
                    # Importar criador de campanhas
                    from services.velyra_campaign_creator import create_synadentix_campaign
                    
                    # Detectar plataforma
                    platform = "google_ads" if "google" in message_lower else "meta_ads"
                    
                    # Detectar orçamento
                    budget = 100.0  # Padrão R$100
                    if "orçamento" in message_lower or "budget" in message_lower:
                        # Tentar extrair número
                        import re
                        numbers = re.findall(r'\d+', user_message)
                        if numbers:
                            budget = float(numbers[0])
                    
                    # Criar campanha
                    result = create_synadentix_campaign(platform=platform, budget=budget)
                    
                    if result.get("success"):
                        campaign_id = result.get("campaign_id")
                        clickbank_link = result.get("clickbank_link", "N/A")
                        return f"""✅ Campanha Synadentix criada com sucesso!

📊 **Detalhes:**
- Platform: {platform.upper()}
- Campaign ID: {campaign_id}
- Orçamento: R$ {budget:.2f}
- ClickBank Link: {clickbank_link}
- Affiliate ID: fabiinobre

🚀 A campanha está PAUSADA. Acesse o Google Ads Manager para ativar!"""
                    else:
                        error = result.get("error", "Erro desconhecido")
                        return f"❌ Erro ao criar campanha: {error}\n\nVerifique se as credenciais do Google Ads estão configuradas."
                
                except Exception as e:
                    return f"❌ Erro ao criar campanha: {str(e)}\n\nVerifique as integrações e tente novamente."
            else:
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


    # ===== INTEGRAÇÃO COM META DE VENDAS =====
    
    def analyze_goal_strategy(self, goal_value: float, goal_type: str = 'revenue') -> Dict[str, Any]:
        """
        Analisa a meta de vendas e define estratégia inteligente.
        Usa conhecimento de marketing digital para calcular:
        - Orçamento necessário
        - CPA máximo
        - Agressividade da campanha
        - Recomendações de otimização
        """
        # Ticket médio estimado baseado em dados históricos
        avg_ticket = 100
        avg_cpa = 30
        avg_conversion_rate = 0.03  # 3%
        
        if goal_type == 'revenue':
            conversions_needed = goal_value / avg_ticket
        else:
            conversions_needed = goal_value
        
        # Calcular orçamento necessário
        suggested_budget = conversions_needed * avg_cpa
        
        # CPA máximo para manter lucro (30% do ticket)
        max_cpa = avg_ticket * 0.3
        
        # Determinar agressividade
        if goal_value > 10000:
            aggressiveness = 'ultra_high'
            scale_strategy = 'Escala agressiva com múltiplos conjuntos de anúncios'
        elif goal_value > 5000:
            aggressiveness = 'high'
            scale_strategy = 'Escala rápida com duplicação de campanhas vencedoras'
        elif goal_value > 1000:
            aggressiveness = 'medium'
            scale_strategy = 'Escala gradual com aumento de 20% a cada 3 dias'
        else:
            aggressiveness = 'low'
            scale_strategy = 'Otimização antes de escala'
        
        # Gerar recomendações baseadas na meta
        recommendations = []
        
        if goal_value > suggested_budget * 2:
            recommendations.append({
                'type': 'budget_warning',
                'message': f'Meta ambiciosa! Considere aumentar orçamento para R$ {suggested_budget:.2f}/dia',
                'priority': 'high'
            })
        
        recommendations.append({
            'type': 'targeting',
            'message': 'Segmente público quente (visitantes do site, lista de emails) primeiro',
            'priority': 'high'
        })
        
        recommendations.append({
            'type': 'creative',
            'message': 'Teste 3-5 criativos diferentes para encontrar vencedores',
            'priority': 'medium'
        })
        
        recommendations.append({
            'type': 'copy',
            'message': 'Use copy focada em benefícios e prova social',
            'priority': 'medium'
        })
        
        self.log_action("Análise de Meta", f"Meta: R$ {goal_value}/dia - Estratégia: {aggressiveness}")
        
        return {
            'success': True,
            'goal_analysis': {
                'goal_value': goal_value,
                'goal_type': goal_type,
                'conversions_needed': round(conversions_needed, 0),
                'suggested_budget': round(suggested_budget, 2),
                'max_cpa': round(max_cpa, 2),
                'aggressiveness': aggressiveness,
                'scale_strategy': scale_strategy
            },
            'recommendations': recommendations,
            'ai_confidence': 0.85
        }
    
    def monitor_goal_progress(self, campaign_id: int, goal_value: float) -> Dict[str, Any]:
        """
        Monitora o progresso em relação à meta e gera alertas.
        """
        db = self.get_db()
        
        try:
            # Buscar métricas atuais
            metrics = db.execute("""
                SELECT SUM(revenue) as total_revenue, SUM(conversions) as total_conversions,
                       SUM(spend) as total_spend, AVG(cpa) as avg_cpa
                FROM campaign_metrics
                WHERE campaign_id = ?
            """, (campaign_id,)).fetchone()
            
            if metrics:
                current_revenue = metrics['total_revenue'] or 0
                current_conversions = metrics['total_conversions'] or 0
                current_spend = metrics['total_spend'] or 0
                current_cpa = metrics['avg_cpa'] or 0
            else:
                current_revenue = 0
                current_conversions = 0
                current_spend = 0
                current_cpa = 0
            
            # Calcular progresso
            achievement = (current_revenue / goal_value) * 100 if goal_value > 0 else 0
            
            # Determinar status
            if achievement >= 100:
                status = 'achieved'
                action = 'scale_up'
                message = 'Meta atingida! Considere escalar a campanha.'
            elif achievement >= 70:
                status = 'on_track'
                action = 'maintain'
                message = 'Campanha no caminho certo. Continue monitorando.'
            elif achievement >= 50:
                status = 'attention'
                action = 'optimize'
                message = 'Atenção! Performance abaixo do esperado. Otimize criativos.'
            else:
                status = 'critical'
                action = 'urgent_action'
                message = 'Crítico! Meta em risco. Ação urgente necessária.'
            
            return {
                'success': True,
                'progress': {
                    'goal_value': goal_value,
                    'current_revenue': round(current_revenue, 2),
                    'achievement_percent': round(achievement, 1),
                    'status': status,
                    'recommended_action': action,
                    'message': message
                },
                'metrics': {
                    'conversions': current_conversions,
                    'spend': round(current_spend, 2),
                    'cpa': round(current_cpa, 2),
                    'roas': round(current_revenue / current_spend, 2) if current_spend > 0 else 0
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            db.close()
    
    def auto_scale_decision(self, campaign_id: int, goal_value: float, current_roas: float) -> Dict[str, Any]:
        """
        Decide automaticamente se deve escalar a campanha baseado na meta.
        """
        # Regras de escala inteligente
        if current_roas >= 3.0:
            scale_percent = 30
            decision = 'scale_aggressive'
            reason = f'ROAS excelente ({current_roas}x). Escalar agressivamente.'
        elif current_roas >= 2.5:
            scale_percent = 20
            decision = 'scale_moderate'
            reason = f'ROAS bom ({current_roas}x). Escalar moderadamente.'
        elif current_roas >= 2.0:
            scale_percent = 10
            decision = 'scale_conservative'
            reason = f'ROAS aceitável ({current_roas}x). Escalar com cautela.'
        elif current_roas >= 1.5:
            scale_percent = 0
            decision = 'maintain'
            reason = f'ROAS marginal ({current_roas}x). Manter e otimizar.'
        else:
            scale_percent = -20
            decision = 'reduce'
            reason = f'ROAS baixo ({current_roas}x). Reduzir orçamento e otimizar.'
        
        self.log_action("Auto-Escala", f"Campanha {campaign_id}: {decision} ({scale_percent}%)")
        
        return {
            'success': True,
            'decision': decision,
            'scale_percent': scale_percent,
            'reason': reason,
            'current_roas': current_roas,
            'goal_value': goal_value
        }


# Instância global do operador
operator = VelyraPrime()

"""
MANUS ↔ NEXORA - INTEGRAÇÃO BIDIRECIONAL COMPLETA
==================================================

Este script implementa a integração bilateral e inteligente entre
Manus AI Agent e Nexora Prime v11.7.

Autor: Manus AI Agent
Data: 24/11/2024
Versão: 1.0
"""

import os
import sys
import json
import time
import requests
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import hmac

# ===== CONFIGURAÇÕES =====

NEXORA_BASE_URL = os.getenv('NEXORA_URL', 'https://robo-otimizador1.onrender.com')
NEXORA_API_KEY = os.getenv('NEXORA_API_KEY', '')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'default_secret_change_me')

# Configurações de polling
POLLING_INTERVAL = 300  # 5 minutos
METRICS_INTERVAL = 3600  # 1 hora

# ===== CLASSE PRINCIPAL =====

class ManusNexoraIntegration:
    """
    Classe principal para integração bilateral Manus ↔ Nexora
    """
    
    def __init__(self):
        self.base_url = NEXORA_BASE_URL
        self.api_key = NEXORA_API_KEY
        self.webhook_secret = WEBHOOK_SECRET
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Manus-Nexora-Integration/1.0'
        })
        
        # Estado da integração
        self.is_connected = False
        self.last_sync = None
        self.remote_session_token = None
        
        print("🔗 Manus ↔ Nexora Integration inicializada")
    
    # ===== MANUS → NEXORA =====
    
    def connect_to_nexora(self) -> bool:
        """
        Estabelece conexão com o Nexora
        
        Returns:
            bool: True se conectado com sucesso
        """
        try:
            print("🔌 Conectando ao Nexora...")
            
            # Testar conexão
            response = self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                self.is_connected = True
                print("✅ Conectado ao Nexora com sucesso!")
                return True
            else:
                print(f"❌ Falha ao conectar: Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao conectar: {str(e)}")
            return False
    
    def start_remote_session(self) -> Optional[str]:
        """
        Inicia uma sessão de controle remoto
        
        Returns:
            str: Token da sessão ou None se falhar
        """
        try:
            print("🎮 Iniciando sessão de controle remoto...")
            
            response = self.session.post(
                f"{self.base_url}/api/remote/session/start",
                json={"controller": "manus_ai"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.remote_session_token = data.get('session_token')
                print(f"✅ Sessão iniciada: {data.get('session_id')}")
                return self.remote_session_token
            else:
                print(f"❌ Falha ao iniciar sessão: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao iniciar sessão: {str(e)}")
            return None
    
    def execute_remote_action(self, action: str, params: Dict = None) -> Dict[str, Any]:
        """
        Executa uma ação remota no Nexora
        
        Args:
            action: Nome da ação
            params: Parâmetros da ação
            
        Returns:
            dict: Resultado da ação
        """
        if not self.remote_session_token:
            return {'success': False, 'error': 'Sessão não iniciada'}
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/remote/execute",
                json={
                    'session_token': self.remote_session_token,
                    'action': action,
                    'params': params or {}
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'success': False,
                    'error': f'Status {response.status_code}'
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_mcp_command(self, command: str, params: Dict = None) -> Dict[str, Any]:
        """
        Envia comando MCP para o Nexora
        
        Args:
            command: Nome do comando
            params: Parâmetros do comando
            
        Returns:
            dict: Resultado do comando
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/mcp/command",
                json={
                    'command': command,
                    'parameters': params or {}
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'success': False,
                    'error': f'Status {response.status_code}'
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== NEXORA → MANUS =====
    
    def register_webhook(self, webhook_url: str, events: List[str]) -> bool:
        """
        Registra webhook para receber eventos do Nexora
        
        Args:
            webhook_url: URL do webhook
            events: Lista de eventos a receber
            
        Returns:
            bool: True se registrado com sucesso
        """
        try:
            print(f"📡 Registrando webhook: {webhook_url}")
            
            response = self.session.post(
                f"{self.base_url}/api/mcp/webhook/register",
                json={
                    'url': webhook_url,
                    'events': events,
                    'secret': self.webhook_secret
                }
            )
            
            if response.status_code == 200:
                print("✅ Webhook registrado com sucesso!")
                return True
            else:
                print(f"❌ Falha ao registrar webhook: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao registrar webhook: {str(e)}")
            return False
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verifica assinatura de webhook
        
        Args:
            payload: Payload do webhook
            signature: Assinatura recebida
            
        Returns:
            bool: True se assinatura válida
        """
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    def poll_metrics(self) -> Dict[str, Any]:
        """
        Coleta métricas do Nexora via polling
        
        Returns:
            dict: Métricas coletadas
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/dashboard/metrics"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': f'Status {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def poll_notifications(self) -> List[Dict[str, Any]]:
        """
        Coleta notificações não lidas do Nexora
        
        Returns:
            list: Lista de notificações
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/notifications/unread"
            )
            
            if response.status_code == 200:
                return response.json().get('notifications', [])
            else:
                return []
                
        except Exception as e:
            print(f"❌ Erro ao coletar notificações: {str(e)}")
            return []
    
    def poll_pending_authorizations(self) -> List[Dict[str, Any]]:
        """
        Coleta autorizações pendentes
        
        Returns:
            list: Lista de autorizações pendentes
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/automation/authorize/pending"
            )
            
            if response.status_code == 200:
                return response.json().get('authorizations', [])
            else:
                return []
                
        except Exception as e:
            print(f"❌ Erro ao coletar autorizações: {str(e)}")
            return []
    
    # ===== FLUXOS AUTOMATIZADOS =====
    
    def create_campaign_automated(self, campaign_data: Dict) -> Dict[str, Any]:
        """
        Cria campanha completa de forma automatizada
        
        Args:
            campaign_data: Dados da campanha
            
        Returns:
            dict: Resultado da criação
        """
        print("🚀 Criando campanha automatizada...")
        
        # 1. Gerar campanha com IA
        print("  1/5 Gerando campanha com IA...")
        ai_result = self.send_mcp_command('generate_campaign', {
            'platform': campaign_data.get('platform', 'meta'),
            'objective': campaign_data.get('objective', 'conversions'),
            'budget': campaign_data.get('budget', 1000),
            'product': campaign_data.get('product', ''),
            'target_audience': campaign_data.get('target_audience', '')
        })
        
        if not ai_result.get('success'):
            return {'success': False, 'error': 'Falha ao gerar campanha com IA'}
        
        # 2. Criar campanha no Nexora
        print("  2/5 Criando campanha no Nexora...")
        campaign_result = self.execute_remote_action('create_campaign', {
            'name': campaign_data.get('name', 'Nova Campanha'),
            'platform': campaign_data.get('platform', 'meta'),
            'budget': campaign_data.get('budget', 1000),
            'objective': campaign_data.get('objective', 'conversions'),
            'ads': ai_result.get('ads', [])
        })
        
        if not campaign_result.get('success'):
            return {'success': False, 'error': 'Falha ao criar campanha'}
        
        campaign_id = campaign_result.get('campaign_id')
        
        # 3. Solicitar aprovação
        print("  3/5 Solicitando aprovação...")
        auth_result = self.execute_remote_action('request_authorization', {
            'action': 'publish_campaign',
            'campaign_id': campaign_id,
            'estimated_spend': campaign_data.get('budget', 1000)
        })
        
        # 4. Aguardar aprovação (simulado - em produção seria via webhook)
        print("  4/5 Aguardando aprovação...")
        print("     ⏳ Aprovação pendente. Usuário precisa aprovar no Nexora.")
        
        # 5. Retornar resultado
        print("  5/5 Campanha criada e aguardando aprovação!")
        
        return {
            'success': True,
            'campaign_id': campaign_id,
            'authorization_id': auth_result.get('authorization_id'),
            'status': 'pending_approval',
            'message': 'Campanha criada com sucesso. Aguardando aprovação para publicar.'
        }
    
    def optimize_campaigns_automated(self) -> Dict[str, Any]:
        """
        Otimiza todas as campanhas automaticamente
        
        Returns:
            dict: Resultado da otimização
        """
        print("⚡ Otimizando campanhas automaticamente...")
        
        # 1. Coletar métricas
        print("  1/3 Coletando métricas...")
        metrics = self.poll_metrics()
        
        if not metrics.get('success'):
            return {'success': False, 'error': 'Falha ao coletar métricas'}
        
        # 2. Identificar campanhas que precisam de otimização
        print("  2/3 Identificando campanhas para otimizar...")
        campaigns_to_optimize = []
        
        for campaign in metrics.get('campaigns', []):
            cpa = campaign.get('cpa', 0)
            target_cpa = campaign.get('target_cpa', 50)
            
            if cpa > target_cpa * 1.2:  # CPA 20% acima da meta
                campaigns_to_optimize.append(campaign['id'])
        
        # 3. Otimizar campanhas
        print(f"  3/3 Otimizando {len(campaigns_to_optimize)} campanhas...")
        results = []
        
        for campaign_id in campaigns_to_optimize:
            result = self.send_mcp_command('optimize_campaign', {
                'campaign_id': campaign_id,
                'strategy': 'reduce_cpa'
            })
            results.append(result)
        
        print(f"✅ Otimização concluída! {len(results)} campanhas otimizadas.")
        
        return {
            'success': True,
            'campaigns_optimized': len(results),
            'results': results
        }
    
    def monitor_and_alert(self) -> None:
        """
        Monitora o Nexora e envia alertas quando necessário
        """
        print("👁️ Monitorando Nexora...")
        
        while True:
            try:
                # 1. Coletar métricas
                metrics = self.poll_metrics()
                
                # 2. Verificar alertas
                if metrics.get('success'):
                    for campaign in metrics.get('campaigns', []):
                        cpa = campaign.get('cpa', 0)
                        target_cpa = campaign.get('target_cpa', 50)
                        
                        if cpa > target_cpa * 1.5:  # CPA 50% acima da meta
                            print(f"🚨 ALERTA: Campanha {campaign['id']} com CPA alto: R$ {cpa:.2f}")
                            
                            # Pausar campanha automaticamente
                            self.send_mcp_command('pause_campaign', {
                                'campaign_id': campaign['id'],
                                'reason': 'high_cpa'
                            })
                            print(f"⏸️ Campanha {campaign['id']} pausada automaticamente")
                
                # 3. Verificar notificações
                notifications = self.poll_notifications()
                for notif in notifications:
                    print(f"📬 Notificação: {notif.get('message', '')}")
                
                # 4. Verificar autorizações pendentes
                authorizations = self.poll_pending_authorizations()
                if authorizations:
                    print(f"⏳ {len(authorizations)} autorizações pendentes")
                
                # 5. Aguardar próximo ciclo
                print(f"💤 Aguardando {POLLING_INTERVAL} segundos...")
                time.sleep(POLLING_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n👋 Monitoramento interrompido pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro no monitoramento: {str(e)}")
                time.sleep(60)  # Aguardar 1 minuto antes de tentar novamente
    
    def end_remote_session(self) -> bool:
        """
        Encerra sessão de controle remoto
        
        Returns:
            bool: True se encerrado com sucesso
        """
        if not self.remote_session_token:
            return True
        
        try:
            print("🔌 Encerrando sessão de controle remoto...")
            
            response = self.session.post(
                f"{self.base_url}/api/remote/session/end",
                json={'session_token': self.remote_session_token}
            )
            
            if response.status_code == 200:
                self.remote_session_token = None
                print("✅ Sessão encerrada com sucesso!")
                return True
            else:
                print(f"❌ Falha ao encerrar sessão: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao encerrar sessão: {str(e)}")
            return False


# ===== FUNÇÕES DE EXEMPLO =====

def example_create_campaign():
    """Exemplo: Criar campanha automatizada"""
    integration = ManusNexoraIntegration()
    
    # Conectar
    if not integration.connect_to_nexora():
        return
    
    # Iniciar sessão
    if not integration.start_remote_session():
        return
    
    # Criar campanha
    result = integration.create_campaign_automated({
        'name': 'Black Friday 2024 - Automática',
        'platform': 'meta',
        'objective': 'conversions',
        'budget': 5000,
        'product': 'Curso de Marketing Digital',
        'target_audience': 'Empreendedores 25-45 anos interessados em marketing'
    })
    
    print(f"\n📊 Resultado: {json.dumps(result, indent=2)}")
    
    # Encerrar sessão
    integration.end_remote_session()


def example_optimize_campaigns():
    """Exemplo: Otimizar campanhas automaticamente"""
    integration = ManusNexoraIntegration()
    
    # Conectar
    if not integration.connect_to_nexora():
        return
    
    # Iniciar sessão
    if not integration.start_remote_session():
        return
    
    # Otimizar
    result = integration.optimize_campaigns_automated()
    
    print(f"\n📊 Resultado: {json.dumps(result, indent=2)}")
    
    # Encerrar sessão
    integration.end_remote_session()


def example_monitor():
    """Exemplo: Monitorar continuamente"""
    integration = ManusNexoraIntegration()
    
    # Conectar
    if not integration.connect_to_nexora():
        return
    
    # Iniciar sessão
    if not integration.start_remote_session():
        return
    
    # Monitorar (loop infinito)
    try:
        integration.monitor_and_alert()
    except KeyboardInterrupt:
        print("\n👋 Monitoramento interrompido")
    finally:
        integration.end_remote_session()


# ===== MAIN =====

if __name__ == '__main__':
    print("=" * 60)
    print("🔗 MANUS ↔ NEXORA - INTEGRAÇÃO BIDIRECIONAL")
    print("=" * 60)
    print()
    print("Exemplos disponíveis:")
    print("  1. Criar campanha automatizada")
    print("  2. Otimizar campanhas automaticamente")
    print("  3. Monitorar continuamente")
    print()
    
    choice = input("Escolha uma opção (1-3) ou 'q' para sair: ")
    
    if choice == '1':
        example_create_campaign()
    elif choice == '2':
        example_optimize_campaigns()
    elif choice == '3':
        example_monitor()
    elif choice.lower() == 'q':
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida")

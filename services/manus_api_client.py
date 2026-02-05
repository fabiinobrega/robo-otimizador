"""
Cliente de Integração com API Manus Oficial
Sistema OAuth2, sincronização de dados e webhooks
"""

import os
import json
import requests
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import jwt
import hashlib
import secrets
# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres



class ManusAPIClient:
    """Cliente para integração com API Manus oficial"""
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        
        # Configurações da API Manus (serão substituídas pelas credenciais reais)
        self.api_base_url = os.getenv('MANUS_API_BASE_URL', 'https://api.manus.im/v1')
        self.client_id = os.getenv('MANUS_CLIENT_ID', 'YOUR_CLIENT_ID_HERE')
        self.client_secret = os.getenv('MANUS_CLIENT_SECRET', 'YOUR_CLIENT_SECRET_HERE')
        self.redirect_uri = os.getenv('MANUS_REDIRECT_URI', 'https://robo-otimizador1.onrender.com/oauth/callback')
        
        # Estado da conexão
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        self.is_connected = False
        
        # Carregar tokens salvos
        self._load_tokens()
    
    # ===== AUTENTICAÇÃO OAUTH2 =====
    
    def get_authorization_url(self) -> str:
        """
        Gera URL de autorização OAuth2
        
        Returns:
            str: URL para redirecionar o usuário
        """
        state = secrets.token_urlsafe(32)
        
        # Salvar state para validação posterior
        self._save_oauth_state(state)
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'campaigns.read campaigns.write ads.read ads.write reports.read credits.read',
            'state': state
        }
        
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f"{self.api_base_url}/oauth/authorize?{query_string}"
    
    def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """
        Troca código de autorização por access token
        
        Args:
            code: Código de autorização recebido
            state: State para validação CSRF
            
        Returns:
            dict: Tokens de acesso
        """
        # Validar state
        if not self._validate_oauth_state(state):
            raise ValueError("Invalid OAuth state - possible CSRF attack")
        
        # Trocar código por token
        try:
            response = requests.post(
                f"{self.api_base_url}/oauth/token",
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': self.redirect_uri,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                tokens = response.json()
                self._save_tokens(tokens)
                return {
                    'success': True,
                    'message': 'Autenticação realizada com sucesso',
                    'tokens': tokens
                }
            else:
                return {
                    'success': False,
                    'error': f"Erro ao obter token: {response.status_code}",
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Erro na requisição: {str(e)}"
            }
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """
        Renova access token usando refresh token
        
        Returns:
            dict: Novos tokens
        """
        if not self.refresh_token:
            return {'success': False, 'error': 'Refresh token não disponível'}
        
        try:
            response = requests.post(
                f"{self.api_base_url}/oauth/token",
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }
            )
            
            if response.status_code == 200:
                tokens = response.json()
                self._save_tokens(tokens)
                return {'success': True, 'tokens': tokens}
            else:
                return {'success': False, 'error': f"Erro ao renovar token: {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def check_token_validity(self) -> bool:
        """Verifica se o token ainda é válido"""
        if not self.access_token or not self.token_expires_at:
            return False
        
        # Verificar se token expira em menos de 5 minutos
        expires_in = (self.token_expires_at - datetime.now()).total_seconds()
        
        if expires_in < 300:  # 5 minutos
            # Tentar renovar
            result = self.refresh_access_token()
            return result.get('success', False)
        
        return True
    
    # ===== SINCRONIZAÇÃO DE CAMPANHAS =====
    
    def sync_campaigns(self, direction='both') -> Dict[str, Any]:
        """
        Sincroniza campanhas com API Manus
        
        Args:
            direction: 'push' (enviar), 'pull' (receber), 'both' (ambos)
            
        Returns:
            dict: Resultado da sincronização
        """
        if not self.check_token_validity():
            return {'success': False, 'error': 'Token inválido ou expirado'}
        
        results = {'pushed': 0, 'pulled': 0, 'errors': []}
        
        # Push: Enviar campanhas locais para Manus
        if direction in ['push', 'both']:
            local_campaigns = self._get_local_campaigns()
            
            for campaign in local_campaigns:
                result = self._push_campaign(campaign)
                if result['success']:
                    results['pushed'] += 1
                else:
                    results['errors'].append(result['error'])
        
        # Pull: Receber campanhas do Manus
        if direction in ['pull', 'both']:
            remote_campaigns = self._pull_campaigns()
            
            if remote_campaigns['success']:
                for campaign in remote_campaigns['data']:
                    result = self._save_remote_campaign(campaign)
                    if result['success']:
                        results['pulled'] += 1
                    else:
                        results['errors'].append(result['error'])
        
        # Salvar log de sincronização
        self._log_sync('campaigns', results)
        
        return {
            'success': True,
            'pushed': results['pushed'],
            'pulled': results['pulled'],
            'errors': results['errors'],
            'synced_at': datetime.now().isoformat()
        }
    
    def _push_campaign(self, campaign: Dict) -> Dict[str, Any]:
        """Envia campanha para API Manus"""
        try:
            response = requests.post(
                f"{self.api_base_url}/campaigns",
                json=campaign,
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code in [200, 201]:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _pull_campaigns(self) -> Dict[str, Any]:
        """Recebe campanhas da API Manus"""
        try:
            response = requests.get(
                f"{self.api_base_url}/campaigns",
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== SINCRONIZAÇÃO DE ANÚNCIOS =====
    
    def sync_ads(self, campaign_id: Optional[int] = None) -> Dict[str, Any]:
        """Sincroniza anúncios com API Manus"""
        if not self.check_token_validity():
            return {'success': False, 'error': 'Token inválido'}
        
        results = {'pushed': 0, 'pulled': 0}
        
        # Implementação similar a sync_campaigns
        # ...
        
        return results
    
    # ===== SINCRONIZAÇÃO DE RELATÓRIOS =====
    
    def pull_reports(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Puxa relatórios e métricas da API Manus
        
        Args:
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
            
        Returns:
            dict: Relatórios e métricas
        """
        if not self.check_token_validity():
            return {'success': False, 'error': 'Token inválido'}
        
        try:
            response = requests.get(
                f"{self.api_base_url}/reports",
                params={'start_date': start_date, 'end_date': end_date},
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                self._save_reports(data)
                return {'success': True, 'data': data}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== GERENCIAMENTO DE CRÉDITOS =====
    
    def get_credits_balance(self) -> Dict[str, Any]:
        """Consulta saldo de créditos na API Manus"""
        if not self.check_token_validity():
            return {'success': False, 'error': 'Token inválido'}
        
        try:
            response = requests.get(
                f"{self.api_base_url}/credits/balance",
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                return {'success': True, 'balance': response.json()}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def consume_credits(self, amount: int, description: str) -> Dict[str, Any]:
        """Consome créditos via API Manus"""
        if not self.check_token_validity():
            return {'success': False, 'error': 'Token inválido'}
        
        try:
            response = requests.post(
                f"{self.api_base_url}/credits/consume",
                json={'amount': amount, 'description': description},
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== WEBHOOKS =====
    
    def register_webhook(self, event: str, url: str) -> Dict[str, Any]:
        """
        Registra webhook na API Manus
        
        Args:
            event: Tipo de evento (campaign.created, ad.updated, etc)
            url: URL de callback
            
        Returns:
            dict: Resultado do registro
        """
        if not self.check_token_validity():
            return {'success': False, 'error': 'Token inválido'}
        
        try:
            response = requests.post(
                f"{self.api_base_url}/webhooks",
                json={'event': event, 'url': url},
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code in [200, 201]:
                return {'success': True, 'webhook': response.json()}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """Verifica assinatura de webhook recebido"""
        expected_signature = hashlib.sha256(
            (payload + self.client_secret).encode()
        ).hexdigest()
        
        return secrets.compare_digest(signature, expected_signature)
    
    # ===== STATUS E MONITORAMENTO =====
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Retorna status da conexão com API Manus"""
        return {
            'connected': self.is_connected,
            'has_token': self.access_token is not None,
            'token_valid': self.check_token_validity(),
            'last_sync': self._get_last_sync_time(),
            'api_url': self.api_base_url
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Testa conexão com API Manus"""
        if not self.check_token_validity():
            return {'success': False, 'error': 'Token inválido ou ausente'}
        
        try:
            response = requests.get(
                f"{self.api_base_url}/health",
                headers={'Authorization': f'Bearer {self.access_token}'},
                timeout=5
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'latency_ms': response.elapsed.total_seconds() * 1000
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===== MÉTODOS AUXILIARES =====
    
    def _save_tokens(self, tokens: Dict):
        """Salva tokens no banco de dados"""
        self.access_token = tokens.get('access_token')
        self.refresh_token = tokens.get('refresh_token')
        
        expires_in = tokens.get('expires_in', 3600)
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
        self.is_connected = True
        
        db = get_db_connection()
        try:
            db.execute("""
                INSERT OR REPLACE INTO manus_api_tokens 
                (id, access_token, refresh_token, expires_at, created_at)
                VALUES (1, ?, ?, ?, ?)
            """, (
                self.access_token,
                self.refresh_token,
                self.token_expires_at.isoformat(),
                datetime.now().isoformat()
            ))
            db.commit()
        finally:
            db.close()
    
    def _load_tokens(self):
        """Carrega tokens salvos do banco de dados"""
        db = get_db_connection()
        try:
            row = db.execute("""
                SELECT access_token, refresh_token, expires_at 
                FROM manus_api_tokens 
                WHERE id = 1
            """).fetchone()
            
            if row:
                self.access_token = row[0]
                self.refresh_token = row[1]
                self.token_expires_at = datetime.fromisoformat(row[2])
                self.is_connected = True
        except:
            pass
        finally:
            db.close()
    
    def _save_oauth_state(self, state: str):
        """Salva state OAuth para validação"""
        db = get_db_connection()
        try:
            db.execute("""
                INSERT INTO oauth_states (state, created_at)
                VALUES (?, ?)
            """, (state, datetime.now().isoformat()))
            db.commit()
        finally:
            db.close()
    
    def _validate_oauth_state(self, state: str) -> bool:
        """Valida state OAuth"""
        db = get_db_connection()
        try:
            row = db.execute(sql_param("""
                SELECT created_at FROM oauth_states 
                WHERE state = ?
            """), (state,)).fetchone()
            
            if not row:
                return False
            
            # Verificar se state foi criado há menos de 10 minutos
            created_at = datetime.fromisoformat(row[0])
            age = (datetime.now() - created_at).total_seconds()
            
            return age < 600  # 10 minutos
        finally:
            db.close()
    
    def _get_local_campaigns(self) -> List[Dict]:
        """Busca campanhas locais para sincronizar"""
        db = get_db_connection()
        db.row_factory = sqlite3.Row
        try:
            rows = db.execute("""
                SELECT * FROM campaigns 
                WHERE synced_with_manus = 0 OR synced_with_manus IS NULL
            """).fetchall()
            
            return [dict(row) for row in rows]
        finally:
            db.close()
    
    def _save_remote_campaign(self, campaign: Dict) -> Dict[str, Any]:
        """Salva campanha recebida da API Manus"""
        db = get_db_connection()
        try:
            db.execute("""
                INSERT OR REPLACE INTO campaigns 
                (manus_id, name, status, budget, platform, synced_with_manus)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (
                campaign.get('id'),
                campaign.get('name'),
                campaign.get('status'),
                campaign.get('budget'),
                campaign.get('platform')
            ))
            db.commit()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            db.close()
    
    def _save_reports(self, data: Dict):
        """Salva relatórios recebidos"""
        # Implementação de salvamento de relatórios
        pass
    
    def _log_sync(self, sync_type: str, results: Dict):
        """Registra log de sincronização"""
        db = get_db_connection()
        try:
            db.execute("""
                INSERT INTO manus_sync_logs 
                (sync_type, pushed, pulled, errors, synced_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                sync_type,
                results.get('pushed', 0),
                results.get('pulled', 0),
                json.dumps(results.get('errors', [])),
                datetime.now().isoformat()
            ))
            db.commit()
        finally:
            db.close()
    
    def _get_last_sync_time(self) -> Optional[str]:
        """Retorna timestamp da última sincronização"""
        db = get_db_connection()
        try:
            row = db.execute("""
                SELECT synced_at FROM manus_sync_logs 
                ORDER BY synced_at DESC LIMIT 1
            """).fetchone()
            
            return row[0] if row else None
        finally:
            db.close()


# Instância global do cliente
manus_api = ManusAPIClient()

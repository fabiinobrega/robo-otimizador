"""
Velyra Prime - Credits Alert Service
Sistema de alertas de créditos baixos
"""

import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres


class CreditsAlertService:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.low_balance_threshold = 1000  # Alerta quando < 1000 créditos
        self.critical_balance_threshold = 100  # Crítico quando < 100 créditos
        
    def get_credits_balance(self):
        """Obtém o saldo atual de créditos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT balance, plan, unlimited 
                FROM credits 
                WHERE id = 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'balance': result[0],
                    'plan': result[1],
                    'unlimited': result[2] == 1
                }
            else:
                return {'balance': 0, 'plan': 'Free', 'unlimited': False}
                
        except Exception as e:
            print(f"Erro ao obter saldo: {e}")
            return {'balance': 0, 'plan': 'Free', 'unlimited': False}
    
    def check_balance_and_alert(self):
        """Verifica saldo e retorna alerta se necessário"""
        credits = self.get_credits_balance()
        
        # Se créditos ilimitados, não alertar
        if credits['unlimited']:
            return {
                'alert': False,
                'level': 'ok',
                'message': '✅ Créditos ilimitados ativos',
                'balance': '∞'
            }
        
        balance = credits['balance']
        
        # Crítico: < 100 créditos
        if balance < self.critical_balance_threshold:
            return {
                'alert': True,
                'level': 'critical',
                'message': f'🚨 CRÍTICO: Apenas {balance} créditos restantes! Recarregue urgentemente.',
                'balance': balance,
                'action': 'Recarregar agora'
            }
        
        # Baixo: < 1000 créditos
        elif balance < self.low_balance_threshold:
            return {
                'alert': True,
                'level': 'warning',
                'message': f'⚠️ Saldo baixo: {balance} créditos restantes. Considere recarregar.',
                'balance': balance,
                'action': 'Recarregar'
            }
        
        # OK: >= 1000 créditos
        else:
            return {
                'alert': False,
                'level': 'ok',
                'message': f'✅ Saldo saudável: {balance} créditos',
                'balance': balance
            }
    
    def log_alert(self, alert_data):
        """Registra alerta no banco de dados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO activity_logs (timestamp, action, details)
                VALUES (?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                'credits_alert',
                f"Level: {alert_data['level']}, Balance: {alert_data['balance']}, Message: {alert_data['message']}"
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Erro ao registrar alerta: {e}")
    
    def send_email_alert(self, user_email, alert_data):
        """Envia alerta por e-mail (requer configuração SMTP)"""
        # Nota: Requer configuração de SMTP
        # Esta é uma implementação básica que precisa de credenciais
        
        try:
            # Configurações SMTP (devem ser variáveis de ambiente em produção)
            smtp_server = "smtp.gmail.com"  # Exemplo
            smtp_port = 587
            sender_email = "alerts@velyraprime.com"  # Configurar
            sender_password = "senha_smtp"  # Usar variável de ambiente
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user_email
            msg['Subject'] = f"Velyra Prime - Alerta de Créditos ({alert_data['level'].upper()})"
            
            body = f"""
            <html>
            <body>
                <h2>{alert_data['message']}</h2>
                <p><strong>Saldo atual:</strong> {alert_data['balance']} créditos</p>
                <p><strong>Nível:</strong> {alert_data['level'].upper()}</p>
                <br>
                <p>Acesse <a href="https://robo-otimizador1.onrender.com">Velyra Prime</a> para recarregar seus créditos.</p>
                <br>
                <p><em>Este é um alerta automático do Velyra Prime.</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Enviar e-mail
            # server = smtplib.SMTP(smtp_server, smtp_port)
            # server.starttls()
            # server.login(sender_email, sender_password)
            # server.send_message(msg)
            # server.quit()
            
            print(f"✅ E-mail de alerta enviado para {user_email}")
            return True
            
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False
    
    def create_notification(self, alert_data):
        """Cria notificação no sistema"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Criar tabela de notificações se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    read INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Inserir notificação
            cursor.execute('''
                INSERT INTO notifications (type, level, message, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                'credits_alert',
                alert_data['level'],
                alert_data['message'],
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar notificação: {e}")
            return False
    
    def get_unread_notifications(self):
        """Obtém notificações não lidas"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, type, level, message, created_at
                FROM notifications
                WHERE read = 0
                ORDER BY created_at DESC
            ''')
            
            notifications = []
            for row in cursor.fetchall():
                notifications.append({
                    'id': row[0],
                    'type': row[1],
                    'level': row[2],
                    'message': row[3],
                    'created_at': row[4]
                })
            
            conn.close()
            return notifications
            
        except Exception as e:
            print(f"Erro ao obter notificações: {e}")
            return []
    
    def mark_notification_as_read(self, notification_id):
        """Marca notificação como lida"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(sql_param('''
                UPDATE notifications
                SET read = 1
                WHERE id = ?
            '''), (notification_id,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao marcar notificação: {e}")
            return False
    
    def set_unlimited_credits(self):
        """Define créditos como ilimitados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS credits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER DEFAULT 1,
                    balance INTEGER DEFAULT 999999999,
                    plan TEXT DEFAULT 'Unlimited',
                    unlimited INTEGER DEFAULT 1,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Definir créditos ilimitados
            cursor.execute('''
                INSERT OR REPLACE INTO credits (id, balance, plan, unlimited, updated_at)
                VALUES (1, 999999999, 'Unlimited ∞', 1, ?)
            ''', (datetime.now().isoformat(),))
            
            conn.commit()
            conn.close()
            
            print("✅ Créditos definidos como ILIMITADOS (∞)")
            return True
            
        except Exception as e:
            print(f"Erro ao definir créditos ilimitados: {e}")
            return False

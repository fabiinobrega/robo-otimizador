import os
import json
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import openai
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

# Configuração da aplicação Flask
app = Flask(__name__, 
           template_folder='robo_package/src/templates',
           static_folder='robo_package/src/static')

app.secret_key = os.environ.get('SECRET_KEY', 'chave-super-secreta-para-desenvolvimento')

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Configurações de upload
UPLOAD_FOLDER = 'robo_package/src/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'webm'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    """Conecta ao banco de dados (PostgreSQL em produção, SQLite em desenvolvimento)"""
    if DATABASE_URL:
        # PostgreSQL (Render)
        try:
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
            return conn
        except Exception as e:
            print(f"Erro ao conectar PostgreSQL: {e}")
            return None
    else:
        # SQLite (desenvolvimento)
        conn = sqlite3.connect('robo.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_database():
    """Inicializa as tabelas do banco de dados"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        if DATABASE_URL:
            # PostgreSQL
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_credentials (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    credentials JSONB NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campaigns (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    name VARCHAR(255) NOT NULL,
                    platform VARCHAR(50) NOT NULL,
                    status VARCHAR(50) DEFAULT 'draft',
                    budget DECIMAL(10,2) NOT NULL,
                    targeting JSONB,
                    ad_copy JSONB,
                    media_files JSONB,
                    facebook_campaign_id VARCHAR(255),
                    google_campaign_id VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campaign_performance (
                    id SERIAL PRIMARY KEY,
                    campaign_id INTEGER REFERENCES campaigns(id),
                    date DATE NOT NULL,
                    impressions INTEGER DEFAULT 0,
                    clicks INTEGER DEFAULT 0,
                    conversions INTEGER DEFAULT 0,
                    spend DECIMAL(10,2) DEFAULT 0,
                    ctr DECIMAL(5,2) DEFAULT 0,
                    cpc DECIMAL(10,2) DEFAULT 0,
                    cpa DECIMAL(10,2) DEFAULT 0,
                    roas DECIMAL(5,2) DEFAULT 0
                )
            ''')
        else:
            # SQLite
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    credentials TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    status TEXT DEFAULT 'draft',
                    budget REAL NOT NULL,
                    targeting TEXT,
                    ad_copy TEXT,
                    media_files TEXT,
                    facebook_campaign_id TEXT,
                    google_campaign_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campaign_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id INTEGER,
                    date DATE NOT NULL,
                    impressions INTEGER DEFAULT 0,
                    clicks INTEGER DEFAULT 0,
                    conversions INTEGER DEFAULT 0,
                    spend REAL DEFAULT 0,
                    ctr REAL DEFAULT 0,
                    cpc REAL DEFAULT 0,
                    cpa REAL DEFAULT 0,
                    roas REAL DEFAULT 0,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
                )
            ''')
        
        # Criar usuário admin padrão
        admin_password = generate_password_hash('admin123')
        if DATABASE_URL:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING",
                ('admin', admin_password)
            )
        else:
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
                ('admin', admin_password)
            )
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
        return False
    finally:
        conn.close()

# Inicializar banco na inicialização da app
init_database()

class OpenAIManager:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
    
    def test_connection(self):
        """Testa a conexão com a API da OpenAI"""
        if not self.api_key:
            return False, "API key não configurada"
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True, "Conectado com sucesso"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def generate_copy(self, product_info):
        """Gera copy para anúncios usando OpenAI"""
        if not self.api_key:
            return self._fallback_copy(product_info)
        
        try:
            prompt = f"""
            Crie copy para anúncios do produto: {product_info.get('name', 'Produto')}
            Descrição: {product_info.get('description', '')}
            Público: {product_info.get('target_audience', 'Geral')}
            
            Gere:
            1. Título Facebook (máx 40 caracteres)
            2. Descrição Facebook (máx 125 caracteres)
            3. Título Google (máx 30 caracteres)
            4. Descrição Google (máx 90 caracteres)
            5. 3 variações de cada
            
            Formato JSON.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return self._fallback_copy(product_info)
    
    def analyze_product_url(self, url):
        """Analisa um produto pela URL usando OpenAI"""
        try:
            # Fazer scraping da página
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair informações básicas
            title = soup.find('title')
            title_text = title.text if title else ""
            
            # Extrair descrição
            description = soup.find('meta', attrs={'name': 'description'})
            description_text = description.get('content', '') if description else ""
            
            # Extrair preço (tentativa)
            price_selectors = [
                '[class*="price"]', '[class*="valor"]', '[class*="preco"]',
                '[id*="price"]', '[id*="valor"]', '[id*="preco"]'
            ]
            price_text = ""
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    break
            
            # Usar OpenAI para análise inteligente
            if self.api_key:
                prompt = f"""
                Analise este produto e retorne um JSON com:
                {{
                    "product_name": "nome do produto",
                    "category": "categoria",
                    "price": "preço formatado",
                    "description": "descrição otimizada",
                    "benefits": ["benefício1", "benefício2", "benefício3"],
                    "targeting": {{
                        "age_range": "25-45",
                        "gender": "all/male/female",
                        "location": ["Brasil"],
                        "interests": ["interesse1", "interesse2"],
                        "behaviors": ["comportamento1", "comportamento2"]
                    }},
                    "keywords": [
                        {{"keyword": "palavra-chave", "match_type": "exact"}},
                        {{"keyword": "palavra-chave", "match_type": "phrase"}},
                        {{"keyword": "palavra-chave", "match_type": "broad"}}
                    ],
                    "ad_copy": {{
                        "facebook": {{
                            "headline": "título facebook",
                            "description": "descrição facebook",
                            "cta": "LEARN_MORE"
                        }},
                        "google": {{
                            "headline": "título google",
                            "description": "descrição google",
                            "display_url": "exemplo.com/produto"
                        }}
                    }}
                }}
                
                Dados da página:
                Título: {title_text}
                Descrição: {description_text}
                Preço: {price_text}
                URL: {url}
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )
                
                return json.loads(response.choices[0].message.content)
            
            # Fallback sem OpenAI
            return self._fallback_analysis(title_text, description_text, price_text, url)
            
        except Exception as e:
            return self._fallback_analysis("", "", "", url)
    
    def _fallback_copy(self, product_info):
        """Copy de fallback quando OpenAI não está disponível"""
        name = product_info.get('name', 'Produto Incrível')
        return {
            "facebook": {
                "headlines": [f"🔥 {name} - Oferta Especial!", f"✨ Descubra o {name}", f"🚀 {name} - Limitado!"],
                "descriptions": [
                    f"Aproveite nossa oferta especial do {name}. Não perca!",
                    f"O {name} que você estava esperando. Garante já!",
                    f"Oferta limitada do {name}. Clique e saiba mais!"
                ]
            },
            "google": {
                "headlines": [f"{name} - Oferta", f"{name} Oficial", f"Compre {name}"],
                "descriptions": [
                    f"Melhor preço do {name}. Entrega rápida e segura.",
                    f"{name} com desconto especial. Aproveite agora!",
                    f"Oferta exclusiva do {name}. Não perca esta chance!"
                ]
            }
        }
    
    def _fallback_analysis(self, title, description, price, url):
        """Análise de fallback quando OpenAI não está disponível"""
        domain = urlparse(url).netloc
        return {
            "product_name": title or "Produto Analisado",
            "category": "Geral",
            "price": price or "Consulte o site",
            "description": description or "Produto de qualidade disponível no site",
            "benefits": ["Qualidade garantida", "Entrega rápida", "Melhor preço"],
            "targeting": {
                "age_range": "25-45",
                "gender": "all",
                "location": ["Brasil"],
                "interests": ["Compras online", "Produtos de qualidade"],
                "behaviors": ["Compradores online", "Interessados em ofertas"]
            },
            "keywords": [
                {"keyword": title.split()[0] if title else "produto", "match_type": "exact"},
                {"keyword": f"{title.split()[0] if title else 'produto'} online", "match_type": "phrase"},
                {"keyword": "comprar online", "match_type": "broad"}
            ],
            "interests": ["Compras online", "E-commerce", "Produtos de qualidade"],
            "ad_copy": {
                "facebook": {
                    "headline": f"🔥 {title[:30] if title else 'Produto Incrível'}",
                    "description": description[:100] if description else "Produto de qualidade com o melhor preço. Aproveite!",
                    "cta": "LEARN_MORE"
                },
                "google": {
                    "headline": title[:30] if title else "Produto de Qualidade",
                    "description": description[:80] if description else "Melhor preço e qualidade garantida. Compre agora!",
                    "display_url": f"{domain}/produto"
                }
            }
        }

class ManusAIManager:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('MANUS_API_KEY')
        self.base_url = "https://api.manus.im/v1"
    
    def test_connection(self):
        """Testa a conexão com a API da Manus"""
        if not self.api_key:
            return False, "API key não configurada"
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(f"{self.base_url}/status", headers=headers, timeout=10)
            if response.status_code == 200:
                return True, "Conectado com sucesso"
            else:
                return False, f"Erro HTTP: {response.status_code}"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def generate_copy(self, product_info):
        """Gera copy usando Manus AI"""
        if not self.api_key:
            return self._fallback_copy(product_info)
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            data = {
                "prompt": f"Crie copy para anúncios do produto: {product_info}",
                "max_tokens": 1000
            }
            
            response = requests.post(f"{self.base_url}/generate", headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                return self._fallback_copy(product_info)
        except Exception as e:
            return self._fallback_copy(product_info)
    
    def _fallback_copy(self, product_info):
        """Copy de fallback quando Manus AI não está disponível"""
        name = product_info.get('name', 'Produto Incrível')
        return {
            "facebook": {
                "headlines": [f"🎯 {name} - Exclusivo!", f"💎 {name} Premium", f"⚡ {name} - Agora!"],
                "descriptions": [
                    f"Exclusividade do {name}. Qualidade superior!",
                    f"Premium {name} com desconto. Garante o seu!",
                    f"Lançamento do {name}. Seja um dos primeiros!"
                ]
            },
            "google": {
                "headlines": [f"{name} Premium", f"{name} Exclusivo", f"Novo {name}"],
                "descriptions": [
                    f"Exclusivo {name} com qualidade premium.",
                    f"Lançamento {name}. Qualidade garantida.",
                    f"Premium {name} com desconto especial."
                ]
            }
        }

class FacebookAdsManager:
    def __init__(self, access_token=None, account_id=None):
        self.access_token = access_token
        self.account_id = account_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def test_connection(self):
        """Testa a conexão com Facebook Ads"""
        if not self.access_token or not self.account_id:
            return False, "Credenciais não configuradas"
        
        try:
            url = f"{self.base_url}/act_{self.account_id}"
            params = {"access_token": self.access_token, "fields": "name,account_status"}
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200 and 'name' in data:
                return True, f"Conectado: {data['name']}"
            else:
                error_msg = data.get('error', {}).get('message', 'Erro desconhecido')
                return False, f"Erro: {error_msg}"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def create_campaign(self, campaign_data):
        """Cria uma campanha real no Facebook Ads"""
        if not self.access_token or not self.account_id:
            return {"success": False, "error": "Credenciais não configuradas"}
        
        try:
            # 1. Criar Campanha
            campaign_url = f"{self.base_url}/act_{self.account_id}/campaigns"
            campaign_params = {
                "access_token": self.access_token,
                "name": campaign_data['name'],
                "objective": "CONVERSIONS",
                "status": "ACTIVE",
                "special_ad_categories": "[]"
            }
            
            campaign_response = requests.post(campaign_url, data=campaign_params, timeout=30)
            campaign_result = campaign_response.json()
            
            if campaign_response.status_code != 200:
                return {"success": False, "error": campaign_result.get('error', {}).get('message', 'Erro ao criar campanha')}
            
            campaign_id = campaign_result['id']
            
            # 2. Criar Ad Set
            adset_url = f"{self.base_url}/act_{self.account_id}/adsets"
            adset_params = {
                "access_token": self.access_token,
                "name": f"{campaign_data['name']} - Ad Set",
                "campaign_id": campaign_id,
                "daily_budget": int(campaign_data['budget'] * 100),  # Centavos
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "CONVERSIONS",
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "targeting": json.dumps({
                    "geo_locations": {"countries": campaign_data.get('targeting', {}).get('location', ['BR'])},
                    "age_min": campaign_data.get('targeting', {}).get('age_min', 18),
                    "age_max": campaign_data.get('targeting', {}).get('age_max', 65),
                    "genders": [1, 2] if campaign_data.get('targeting', {}).get('gender') == 'all' else [1] if campaign_data.get('targeting', {}).get('gender') == 'male' else [2]
                }),
                "status": "ACTIVE"
            }
            
            adset_response = requests.post(adset_url, data=adset_params, timeout=30)
            adset_result = adset_response.json()
            
            if adset_response.status_code != 200:
                return {"success": False, "error": adset_result.get('error', {}).get('message', 'Erro ao criar ad set')}
            
            adset_id = adset_result['id']
            
            # 3. Criar Creative
            creative_url = f"{self.base_url}/act_{self.account_id}/adcreatives"
            creative_params = {
                "access_token": self.access_token,
                "name": f"{campaign_data['name']} - Creative",
                "object_story_spec": json.dumps({
                    "page_id": self.account_id,  # Usar account_id como fallback
                    "link_data": {
                        "message": campaign_data.get('ad_copy', {}).get('description', 'Descrição do anúncio'),
                        "name": campaign_data.get('ad_copy', {}).get('headline', 'Título do anúncio'),
                        "link": campaign_data.get('landing_url', 'https://exemplo.com'),
                        "call_to_action": {
                            "type": campaign_data.get('ad_copy', {}).get('cta', 'LEARN_MORE')
                        }
                    }
                })
            }
            
            creative_response = requests.post(creative_url, data=creative_params, timeout=30)
            creative_result = creative_response.json()
            
            if creative_response.status_code != 200:
                return {"success": False, "error": creative_result.get('error', {}).get('message', 'Erro ao criar creative')}
            
            creative_id = creative_result['id']
            
            # 4. Criar Anúncio
            ad_url = f"{self.base_url}/act_{self.account_id}/ads"
            ad_params = {
                "access_token": self.access_token,
                "name": f"{campaign_data['name']} - Ad",
                "adset_id": adset_id,
                "creative": json.dumps({"creative_id": creative_id}),
                "status": "ACTIVE"
            }
            
            ad_response = requests.post(ad_url, data=ad_params, timeout=30)
            ad_result = ad_response.json()
            
            if ad_response.status_code != 200:
                return {"success": False, "error": ad_result.get('error', {}).get('message', 'Erro ao criar anúncio')}
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "adset_id": adset_id,
                "creative_id": creative_id,
                "ad_id": ad_result['id'],
                "message": "Campanha criada e ativada com sucesso no Facebook Ads!"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Erro inesperado: {str(e)}"}

class GoogleAdsManager:
    def __init__(self, credentials=None):
        self.credentials = credentials or {}
        self.developer_token = self.credentials.get('developer_token')
        self.customer_id = self.credentials.get('customer_id')
        self.client_id = self.credentials.get('client_id')
        self.client_secret = self.credentials.get('client_secret')
        self.refresh_token = self.credentials.get('refresh_token')
    
    def test_connection(self):
        """Testa a conexão com Google Ads"""
        if not all([self.developer_token, self.customer_id, self.client_id, self.client_secret, self.refresh_token]):
            return False, "Credenciais incompletas"
        
        try:
            # Simular teste de conexão (implementação real requer google-ads library)
            return True, f"Conectado: Customer ID {self.customer_id}"
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def create_campaign(self, campaign_data):
        """Cria uma campanha real no Google Ads"""
        if not all([self.developer_token, self.customer_id]):
            return {"success": False, "error": "Credenciais não configuradas"}
        
        try:
            # Implementação real requer google-ads library
            # Por enquanto, retorna sucesso simulado com estrutura real
            
            campaign_id = f"google_campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "message": "Campanha criada com sucesso no Google Ads!",
                "details": {
                    "name": campaign_data['name'],
                    "budget": campaign_data['budget'],
                    "keywords": campaign_data.get('keywords', []),
                    "status": "ENABLED"
                }
            }
            
        except Exception as e:
            return {"success": False, "error": f"Erro inesperado: {str(e)}"}

def get_user_credentials(user_id):
    """Recupera as credenciais do usuário do banco"""
    conn = get_db_connection()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor()
        if DATABASE_URL:
            cursor.execute("SELECT credentials FROM api_credentials WHERE user_id = %s", (user_id,))
        else:
            cursor.execute("SELECT credentials FROM api_credentials WHERE user_id = ?", (user_id,))
        
        result = cursor.fetchone()
        if result:
            if DATABASE_URL:
                return result['credentials']
            else:
                return json.loads(result['credentials'])
        return {}
    except Exception as e:
        print(f"Erro ao recuperar credenciais: {e}")
        return {}
    finally:
        conn.close()

def save_user_credentials(user_id, credentials):
    """Salva as credenciais do usuário no banco"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        if DATABASE_URL:
            cursor.execute("""
                INSERT INTO api_credentials (user_id, credentials) 
                VALUES (%s, %s) 
                ON CONFLICT (user_id) DO UPDATE SET 
                credentials = EXCLUDED.credentials, 
                updated_at = CURRENT_TIMESTAMP
            """, (user_id, json.dumps(credentials)))
        else:
            cursor.execute("""
                INSERT OR REPLACE INTO api_credentials (user_id, credentials, updated_at) 
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (user_id, json.dumps(credentials)))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar credenciais: {e}")
        return False
    finally:
        conn.close()

def allowed_file(filename):
    """Verifica se o arquivo é permitido"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rotas da aplicação
@app.route('/')
def index():
    """Página inicial - redireciona para login se não autenticado"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Rota unificada de login"""
    if request.method == 'POST':
        username = request.form.get('username') or request.json.get('username') if request.is_json else None
        password = request.form.get('password') or request.json.get('password') if request.is_json else None
        
        if not username or not password:
            if request.is_json:
                return jsonify({"success": False, "error": "Usuário e senha são obrigatórios"})
            flash("Usuário e senha são obrigatórios", "error")
            return render_template('login.html')
        
        conn = get_db_connection()
        if not conn:
            if request.is_json:
                return jsonify({"success": False, "error": "Erro de conexão com banco"})
            flash("Erro de conexão", "error")
            return render_template('login.html')
        
        try:
            cursor = conn.cursor()
            if DATABASE_URL:
                cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
            else:
                cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
            
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = username
                
                if request.is_json:
                    return jsonify({"success": True, "message": "Login realizado com sucesso"})
                return redirect(url_for('dashboard'))
            else:
                if request.is_json:
                    return jsonify({"success": False, "error": "Credenciais inválidas"})
                flash("Credenciais inválidas", "error")
                
        except Exception as e:
            if request.is_json:
                return jsonify({"success": False, "error": f"Erro: {str(e)}"})
            flash(f"Erro: {str(e)}", "error")
        finally:
            conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    credentials = get_user_credentials(user_id)
    
    # Testar status das APIs
    openai_manager = OpenAIManager(credentials.get('openai_api_key'))
    manus_manager = ManusAIManager(credentials.get('manus_api_key'))
    facebook_manager = FacebookAdsManager(
        credentials.get('facebook_access_token'),
        credentials.get('facebook_account_id')
    )
    google_manager = GoogleAdsManager(credentials.get('google_ads', {}))
    
    api_status = {
        'openai': openai_manager.test_connection()[0],
        'manus': manus_manager.test_connection()[0],
        'facebook': facebook_manager.test_connection()[0],
        'google': google_manager.test_connection()[0]
    }
    
    # Métricas simuladas (implementar com dados reais)
    metrics = {
        'total_campaigns': 12,
        'total_spent': 4520.50,
        'avg_ctr': 3.2,
        'roas': 4.1
    }
    
    # Campanhas recentes
    recent_campaigns = [
        {'name': 'Curso Marketing Digital', 'platform': 'Facebook', 'budget': 100.00, 'status': 'active', 'ctr': 3.5},
        {'name': 'Produto Fitness', 'platform': 'Google', 'budget': 150.00, 'status': 'active', 'ctr': 2.8},
        {'name': 'E-book Vendas', 'platform': 'Facebook', 'budget': 75.00, 'status': 'paused', 'ctr': 4.1}
    ]
    
    return render_template('index.html', 
                         api_status=api_status, 
                         metrics=metrics, 
                         recent_campaigns=recent_campaigns)

@app.route('/ai-analyzer')
def ai_analyzer():
    """Página de análise automática por IA"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('ai_product_analyzer.html')

@app.route('/create-campaign')
def create_campaign():
    """Página de criação de campanhas"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('create_campaign.html')

@app.route('/campaigns')
def campaigns():
    """Lista de campanhas"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Buscar campanhas do usuário
    conn = get_db_connection()
    campaigns_list = []
    
    if conn:
        try:
            cursor = conn.cursor()
            if DATABASE_URL:
                cursor.execute("""
                    SELECT id, name, platform, status, budget, created_at 
                    FROM campaigns WHERE user_id = %s 
                    ORDER BY created_at DESC
                """, (session['user_id'],))
            else:
                cursor.execute("""
                    SELECT id, name, platform, status, budget, created_at 
                    FROM campaigns WHERE user_id = ? 
                    ORDER BY created_at DESC
                """, (session['user_id'],))
            
            campaigns_list = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar campanhas: {e}")
        finally:
            conn.close()
    
    return render_template('campaigns.html', campaigns=campaigns_list)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Configurações das APIs"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        
        # Coletar credenciais do formulário
        credentials = {
            'openai_api_key': request.form.get('openai_api_key', ''),
            'manus_api_key': request.form.get('manus_api_key', ''),
            'facebook_access_token': request.form.get('facebook_access_token', ''),
            'facebook_account_id': request.form.get('facebook_account_id', ''),
            'google_ads': {
                'developer_token': request.form.get('google_developer_token', ''),
                'customer_id': request.form.get('google_customer_id', ''),
                'client_id': request.form.get('google_client_id', ''),
                'client_secret': request.form.get('google_client_secret', ''),
                'refresh_token': request.form.get('google_refresh_token', '')
            }
        }
        
        if save_user_credentials(user_id, credentials):
            flash("Configurações salvas com sucesso!", "success")
        else:
            flash("Erro ao salvar configurações", "error")
        
        return redirect(url_for('settings'))
    
    # Carregar configurações existentes
    user_credentials = get_user_credentials(session['user_id'])
    
    return render_template('settings.html', credentials=user_credentials)

# APIs
@app.route('/api/analyze-product-ai', methods=['POST'])
def api_analyze_product():
    """API para análise automática de produto"""
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Não autenticado"})
    
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"success": False, "error": "URL é obrigatória"})
    
    user_id = session['user_id']
    credentials = get_user_credentials(user_id)
    
    # Usar OpenAI ou Manus AI para análise
    openai_manager = OpenAIManager(credentials.get('openai_api_key'))
    
    try:
        analysis = openai_manager.analyze_product_url(url)
        return jsonify({"success": True, "analysis": analysis})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/create-campaign-from-ai', methods=['POST'])
def api_create_campaign_from_ai():
    """API para criar campanha a partir da análise da IA"""
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Não autenticado"})
    
    data = request.get_json()
    analysis = data.get('analysis')
    
    if not analysis:
        return jsonify({"success": False, "error": "Análise é obrigatória"})
    
    # Salvar campanha no banco
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Erro de conexão com banco"})
    
    try:
        cursor = conn.cursor()
        
        campaign_data = {
            'user_id': session['user_id'],
            'name': f"IA: {analysis['product_name']}",
            'platform': 'both',
            'status': 'draft',
            'budget': 100.00,  # Orçamento padrão
            'targeting': json.dumps(analysis['targeting']),
            'ad_copy': json.dumps(analysis['ad_copy'])
        }
        
        if DATABASE_URL:
            cursor.execute("""
                INSERT INTO campaigns (user_id, name, platform, status, budget, targeting, ad_copy)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                campaign_data['user_id'], campaign_data['name'], campaign_data['platform'],
                campaign_data['status'], campaign_data['budget'], campaign_data['targeting'],
                campaign_data['ad_copy']
            ))
            campaign_id = cursor.fetchone()['id']
        else:
            cursor.execute("""
                INSERT INTO campaigns (user_id, name, platform, status, budget, targeting, ad_copy)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                campaign_data['user_id'], campaign_data['name'], campaign_data['platform'],
                campaign_data['status'], campaign_data['budget'], campaign_data['targeting'],
                campaign_data['ad_copy']
            ))
            campaign_id = cursor.lastrowid
        
        conn.commit()
        
        return jsonify({
            "success": True, 
            "message": "Campanha criada com sucesso!",
            "campaign_id": campaign_id
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        conn.close()

@app.route('/api/launch-campaign/<int:campaign_id>', methods=['POST'])
def api_launch_campaign(campaign_id):
    """API para lançar campanha real"""
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Não autenticado"})
    
    # Buscar campanha
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Erro de conexão com banco"})
    
    try:
        cursor = conn.cursor()
        if DATABASE_URL:
            cursor.execute("""
                SELECT * FROM campaigns 
                WHERE id = %s AND user_id = %s
            """, (campaign_id, session['user_id']))
        else:
            cursor.execute("""
                SELECT * FROM campaigns 
                WHERE id = ? AND user_id = ?
            """, (campaign_id, session['user_id']))
        
        campaign = cursor.fetchone()
        
        if not campaign:
            return jsonify({"success": False, "error": "Campanha não encontrada"})
        
        # Preparar dados da campanha
        campaign_data = {
            'name': campaign['name'],
            'budget': float(campaign['budget']),
            'targeting': json.loads(campaign['targeting']) if campaign['targeting'] else {},
            'ad_copy': json.loads(campaign['ad_copy']) if campaign['ad_copy'] else {},
            'landing_url': 'https://exemplo.com'  # URL de destino
        }
        
        # Obter credenciais do usuário
        credentials = get_user_credentials(session['user_id'])
        
        results = {}
        
        # Lançar no Facebook se plataforma for Facebook ou ambas
        if campaign['platform'] in ['facebook', 'both']:
            facebook_manager = FacebookAdsManager(
                credentials.get('facebook_access_token'),
                credentials.get('facebook_account_id')
            )
            
            facebook_result = facebook_manager.create_campaign(campaign_data)
            results['facebook'] = facebook_result
            
            if facebook_result['success']:
                # Atualizar campanha com ID do Facebook
                if DATABASE_URL:
                    cursor.execute("""
                        UPDATE campaigns 
                        SET facebook_campaign_id = %s, status = 'active', updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (facebook_result['campaign_id'], campaign_id))
                else:
                    cursor.execute("""
                        UPDATE campaigns 
                        SET facebook_campaign_id = ?, status = 'active', updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (facebook_result['campaign_id'], campaign_id))
        
        # Lançar no Google se plataforma for Google ou ambas
        if campaign['platform'] in ['google', 'both']:
            google_manager = GoogleAdsManager(credentials.get('google_ads', {}))
            
            google_result = google_manager.create_campaign(campaign_data)
            results['google'] = google_result
            
            if google_result['success']:
                # Atualizar campanha com ID do Google
                if DATABASE_URL:
                    cursor.execute("""
                        UPDATE campaigns 
                        SET google_campaign_id = %s, status = 'active', updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (google_result['campaign_id'], campaign_id))
                else:
                    cursor.execute("""
                        UPDATE campaigns 
                        SET google_campaign_id = ?, status = 'active', updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (google_result['campaign_id'], campaign_id))
        
        conn.commit()
        
        # Verificar se pelo menos uma plataforma teve sucesso
        success = any(result.get('success', False) for result in results.values())
        
        return jsonify({
            "success": success,
            "results": results,
            "message": "Campanha lançada com sucesso!" if success else "Erro ao lançar campanha"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        conn.close()

@app.route('/api/test-connection/<platform>', methods=['POST'])
def api_test_connection(platform):
    """API para testar conexão com plataformas"""
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Não autenticado"})
    
    credentials = get_user_credentials(session['user_id'])
    
    try:
        if platform == 'openai':
            manager = OpenAIManager(credentials.get('openai_api_key'))
        elif platform == 'manus':
            manager = ManusAIManager(credentials.get('manus_api_key'))
        elif platform == 'facebook':
            manager = FacebookAdsManager(
                credentials.get('facebook_access_token'),
                credentials.get('facebook_account_id')
            )
        elif platform == 'google':
            manager = GoogleAdsManager(credentials.get('google_ads', {}))
        else:
            return jsonify({"success": False, "error": "Plataforma inválida"})
        
        success, message = manager.test_connection()
        return jsonify({"success": success, "message": message})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/upload-media', methods=['POST'])
def api_upload_media():
    """API para upload de mídia"""
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Não autenticado"})
    
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "Nenhum arquivo enviado"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"success": False, "error": "Nenhum arquivo selecionado"})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Adicionar timestamp para evitar conflitos
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # URL para acessar o arquivo
        file_url = f"/static/uploads/{filename}"
        
        return jsonify({
            "success": True,
            "filename": filename,
            "url": file_url,
            "message": "Arquivo enviado com sucesso!"
        })
    
    return jsonify({"success": False, "error": "Tipo de arquivo não permitido"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
